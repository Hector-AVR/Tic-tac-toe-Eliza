# eliza.py
import logging
import random
import re
import webbrowser
import os
import socket
from urllib.parse import urlparse

log = logging.getLogger(__name__)

# === CONFIG ===
# Puedes sobreescribirla con la variable de entorno TICTACTOE_URL
DEFAULT_URL = "http://localhost:3000/"
GAME_URL_ENV = os.getenv("TICTACTOE_URL", "").strip()

# Frases que disparan el juego
TRIGGER_RE = re.compile(
    r"(?i)\b(?:hay\s+que\s+jugar|juguemos|quiero\s+jugar|vamos\s+a\s+jugar)\b.*\b("
    r"tic\s*tac\s*toe|gato|tres\s*en\s*raya)\b"
)

def is_port_open(url: str, timeout=0.75) -> bool:
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def try_open_url(url: str) -> bool:
    """Intenta abrir la URL con varios métodos en Windows y demás."""
    try:
        if webbrowser.open_new_tab(url):
            return True
    except Exception:
        pass
    # Windows fallback: os.startfile
    if os.name == "nt":
        try:
            os.startfile(url)  # type: ignore[attr-defined]
            return True
        except Exception:
            pass
        # Último intento: 'start "" "url"'
        try:
            os.system(f'start "" "{url}"')
            return True
        except Exception:
            pass
    return False

# ====== ELIZA TAL CUAL (recortado lo irrelevante) ======

class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

    def load(self, path):
        key = None
        decomp = None
        with open(path, encoding='utf-8') as file:
            for lineno, raw in enumerate(file, start=1):
                line = raw.strip()
                if not line:
                    continue
                if ':' not in line:
                    raise ValueError(f"Línea {lineno} sin ':': {raw!r}")
                tag, content = [part.strip() for part in line.split(':', 1)]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content.lower())
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word.lower()] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    if decomp:
                        parts = content.split(' ')
                        decomp.reasmbs.append(parts)

    # ... (resto de métodos _match_decomp_r, _reassemble, etc. iguales) ...

    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if root not in self.synons:
                return False
            if words[0].lower() not in [s.lower() for s in self.synons[root]]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword.startswith('(') and reword.endswith(')'):
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    continue
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                continue
            results = [self._sub(r, self.posts) for r in results]
            reasmb = self._next_reasmb(decomp)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if goto_key.lower() not in self.keys:
                    continue
                return self._match_key(words, self.keys[goto_key.lower()])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    def respond(self, text):
        if text.lower() in self.quits:
            return None

        # === DISPARADOR DEL JUEGO ===
        if TRIGGER_RE.search(text):
            # Candidatas: env var > localhost > 127.0.0.1
            candidates = []
            if GAME_URL_ENV:
                candidates.append(GAME_URL_ENV)
            candidates.extend([DEFAULT_URL, "http://127.0.0.1:3000/"])

            # Busca una que esté con puerto abierto
            for url in candidates:
                if is_port_open(url):
                    if try_open_url(url):
                        return f"¡Va! Abriendo el juego en {url}"
                    else:
                        return f"No pude abrir el navegador automáticamente. Entra a: {url}"
            # Si ninguna responde, indica que el server no está arriba
            return ("No parece haber un servidor escuchando en el puerto 3000.\n"
                    "Verifica que tu app esté corriendo (por ejemplo React/Vite) y luego intenta de nuevo.\n"
                    f"URLs probadas: {', '.join(candidates)}")

        # === Eliza normal ===
        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)

        words = [w for w in text.split(' ') if w]
        words = self._sub(words, self.pres)

        words_sub = []
        for w in words:
            found = False
            for syn_root, syn_list in self.synons.items():
                if w.lower() in [s.lower() for s in syn_list]:
                    words_sub.append(syn_root); found = True; break
            if not found:
                words_sub.append(w)

        keys = []
        for w in words_sub:
            if w.lower() in self.keys:
                keys.append(self.keys[w.lower()])
            for syn_root in self.synons:
                if w.lower() in [s.lower() for s in self.synons[syn_root]]:
                    if f"@{syn_root}".lower() in self.keys:
                        keys.append(self.keys[f"@{syn_root}".lower()])
        keys = sorted(keys, key=lambda k: -k.weight)

        output = None
        for key in keys:
            output = self._match_key(words_sub, key)
            if output:
                break

        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])

        return " ".join(output)

    def initial(self):
        return random.choice(self.initials) if self.initials else "Hola, soy Eliza."

    def final(self):
        return random.choice(self.finals) if self.finals else "Adiós."

    def run(self):
        print(self.initial())
        while True:
            sent = input("> ")
            output = self.respond(sent)
            if output is None:
                break
            print(output)
        print(self.final())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Este módulo se usa desde servidor.py")

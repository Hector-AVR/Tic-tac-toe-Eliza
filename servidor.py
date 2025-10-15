import asyncio
import websockets
import re
import logging
import eliza
# o si solo necesitas la clase:
from eliza import Eliza
  # asumiendo que tienes el código de Eliza en el archivo eliza.py

numeros_texto = {
    "cero": "0", "uno": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
    "diez": "10"
}

operadores_texto = {
    "mas": "+",
    "menos": "-",
    "por": "*",
    "multiplicado": "*",
    "entre": "/",
    "dividido": "/"
}

preguntas_respuestas = {
        "como te llamas?": "Luis Gorduardo Recerdo Fatiño",
        "¿cual es la capital de francia?": "No se we",
        "¿quien escribió cien años de soledad?": "Diego Rivera Diego Rivera Diego Rivera",
        "¿cual es el planeta más cercano al sol?": "Mercurio",
        "¿en qué año llegó el hombre a la luna?": "1969",
        "¿cual es el río más largo del mundo?": "El Amazonas",
        "¿quien es el hombre naranja?": "Donaldo Tlump",
        "¿cual es el elemento químico con símbolo o?": "Oxigeno",
        "¿cual es el país más grande del mundo?": "Rusia",
        "¿quien fue el primer presidente de los estados unidos?": "Geooooooooooooorge Washington",
        "¿cual es el océano más grande del mundo?": "El Océano Pacífico",
        "¿cual es la montaña más alta del mundo?": "El Monte Everest",
        "¿quien escribió 1984?": "George Orwell uff libraso porcierto esta muy bueno junto con escape de la granja",
        "¿cual es el animal más grande del mundo?": "La ballena azul",
        "¿cual es la capital de japon?": "Tokio",
        "¿quien descubrió la penicilina?": "Alexander Fleming",
        "¿cual es el metal más conductor de electricidad?": "La plata",
        "¿cual es el pais más poblado del mundo?": "China",
        "¿quien fue el primer hombre en el espacio?": "Yuri Gagarin",
        "¿en que pais hay mas chinos?": "Pos en china",
        "¿quien escribió don quijote de la mancha?": "Miguel de Cervantes",
        "¿cuanto cuesta?": "20 mil dolale",
        "¿cual es el mejor pais de china": "China",
        "¿cuantos pelos tiene un oso panda?": "Los conté y eran 3, pero se me escapó",
        "¿cual es la capital de marte?": "Marcetropolis",
        "¿quien inventó el internet?": "Un señor aburrido que quería memes",
        "¿que pesa más un kilo de plumas o un kilo de plomo?": "El plomo, obvio, aunque me hackees",
        "¿cual es el lenguaje más dificil del mundo?": "El que habla tu ex cuando dice que no está enojada",
        "¿cual es la velocidad de la luz?": "La misma que yo cuando escucho que regalan tacos",
        "¿quien fue primero el huevo o la gallina?": "Fue el gallo, pero nadie lo invita a las pláticas",
        "¿cuantos continentes hay?": "Depende, ¿los de la Tierra o también contamos a Pokémon?",
        "¿cual es el animal más rápido del mundo?": "El WiFi cuando no lo necesitas",
        "¿quien descubrió america?": "Cristobal Colón pero con GPS pirateado",
        "¿cual es el mejor invento de la humanidad?": "El control remoto, sin duda",
        "¿cual es la edad del sol?": "Un poquito más viejo que Chabelo",
        "¿cual es la comida favorita de los programadores?": "Los bytes con salsa",
        "¿quien canta mejor que Shakira?": "Una cabra, pero no le dieron contrato",
        "¿cual es la capital de Wakanda?": "Wakandapolis",
        "¿cuantos litros de agua hay en el mar?": "Muchísimos, los medí y me cansé",
        "¿cual es la fruta más rara del mundo?": "La manzana con sabor a tamal",
        "¿quien es el villano más malo de todos?": "El que se come las orillas de la pizza y deja lo demás",
        "¿cuantos planetas hay en el sistema solar?": "Ocho… y Pluto llorando en la esquina",
        "¿cual es la serie más vista del universo?": "La Rosa de Guadalupe intergaláctica",
        "¿cuantos idiomas hablas?": "Español, inglés y puro sarcasmo",
        "¿cual es el animal más peligroso del mundo?": "La suegra cuando dices que no tienes hambre",
        "¿quien escribió la biblia?": "Un escritor fantasma nivel Dios",
        "¿cual es el trabajo más dificil del mundo?": "Ser optimista en lunes",
        "¿que es un agujero negro?": "Un basurero cósmico de calcetines perdidos",
        "¿cuantos dientes tiene un tiburón?": "Más que tus primos en navidad",
        "¿como estas?": "Pensar en ella me hace recordar la Sustancia",
        "¿cuantos huesos tiene el cuerpo humano?": "Te extraño Nirvana"
}

def limpiar_texto(frase: str) -> list:
    frase = frase.lower()
    frase = re.sub(r"[^a-z0-9áéíóúüñ\s]", "", frase)
    return frase.split()

def texto_a_expresion(frase: str) -> str:
    palabras = limpiar_texto(frase)
    expresion = []
    for palabra in palabras:
        if palabra in numeros_texto:
            expresion.append(numeros_texto[palabra])
        elif palabra in operadores_texto:
            expresion.append(operadores_texto[palabra])
        elif palabra.isdigit():
            expresion.append(palabra)
    return "".join(expresion)

# ✅ Inicializar ELIZA
eliza = Eliza()
eliza.load("doctor.txt")  # usa el script en español que definimos antes

async def handle(websocket):
    # Enviar saludo de arranque
    await websocket.send("Hola, soy Eliza. ¿En qué piensas hoy?")

    async for message in websocket:
        msg = message.strip().lower()
        if msg == "cerrar":
            await websocket.send("Conexión cerrada")
            break

async def handle(websocket):
    async for message in websocket:
        msg = message.strip().lower()
        if msg == "cerrar":
            await websocket.send("Conexión cerrada")
            break

        if msg in preguntas_respuestas:
            response = preguntas_respuestas[msg]
        else:
            expr = texto_a_expresion(msg)
            if expr and all(c in "0123456789+-*/. " for c in expr):
                try:
                    resultado = eval(expr)
                    response = f"Resultado: {resultado}"
                except:
                    response = "Operación inválida."
            else:
                # 👇 Aquí entra ELIZA si no encuentra coincidencia
                response = eliza.respond(msg)

        await websocket.send(response)

async def main():
    async with websockets.serve(handle, "127.0.0.1", 8765):
        print("✅ Servidor WebSocket corriendo en ws://127.0.0.1:8765")
        await asyncio.Future()  # mantiene el servidor vivo

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)  # menos ruido en consola
    asyncio.run(main())
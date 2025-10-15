import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000


    client.connect((server_ip, server_port))
    print("Conectado al servidor.")

    while True:

        pregunta = input("Escribe tu pregunta (o 'cerrar' para salir): ")
        client.send(pregunta.encode("utf-8"))

        respuesta = client.recv(1024).decode("utf-8")
        print(f"Respuesta del servidor: {respuesta}")

        if pregunta.lower() == "cerrar":
            break

    client.close()
    print("Conexión con el servidor cerrada.")

run_client()
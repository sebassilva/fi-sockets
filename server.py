
#!/usr/bin/env python3
# Universidad Nacional Autónoma de México
# Facultad de Ingeniería
# Sistemas distribuidos
# Código de servidor para proyecto de sockets

# Integrantes: 
#    * Silva García, Carlos Sebastián
#    * 
#    *  
#    * 

# Importamos las bibliotecas socket y threading, que ya vienen con la 
# instalación de python.
# Importante correr el programa utilizando python3.


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
UTF_8 = "utf8"
def accept_incoming_connections():
   # Maneja a los nuevos clientes, y los guarda en memoria.
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se ha conectado." % client_address)
        client.send(bytes("Saludos desde la H. Facultad de Ingeniería. Ingresa tu nombre: ", UTF_8))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Toma el socket client como argumento
    # Maneja a cada cliente individualmente
    name = client.recv(BUFSIZ).decode(UTF_8)
    welcome = '¡Bienvenido,  %s! Si quieres salir, escribes "salir" y presiona enviar. ' % name
    client.send(bytes(welcome, UTF_8))
    msg = ":: %s se ha unido al chat." % name
    broadcast(bytes(msg, UTF_8))
    clients[client] = name

    while True:
        # Escucha todo el tiempo a recibir mensajes.
        # Si es la cadena salir, termina la conexión.
        msg = client.recv(BUFSIZ)
        if msg != bytes("salir", UTF_8):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("salir", UTF_8))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, UTF_8))
            break


def broadcast(msg, prefix=""):  # el prefijo es para identificación por nombre
    # Envía un mensaje a todos los clientes.

    # Itera clientes, que es un arreglo de sockets y les envía el mensaje a todos.
    for sock in clients:
        sock.send(bytes(prefix, UTF_8)+msg)

        
clients = {}
addresses = {}

# Levantamos el servidor en 127.0.0.1, que es localhost.
# el puerto es el 8080, que fue elegido aleatoriamente, siempre que sea un puerto disponible.

HOST = '127.0.0.1'
PORT = 8081
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
CLIENTS_LIMIT = 10

if __name__ == "__main__":

    SERVER.listen(CLIENTS_LIMIT)
    print("Esperando nuevas conecciones...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
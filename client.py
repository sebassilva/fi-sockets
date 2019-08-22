#!/usr/bin/env python3
# Universidad Nacional Autónoma de México
# Facultad de Ingeniería
# Sistemas distribuidos
# Código de cliente para proyecto de sockets

# Integrantes: 
#    * Silva García, Carlos Sebastián
#    * 
#    *  
#    * 

# Importamos las bibliotecas socket y threading, que ya vienen con la 
# instalación de python.
# Además, utilizamos tkinter, que nos permite desarrollar una GUI.

# Importante correr el programa utilizando python3.

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
UTF_8 = "utf8"


def receive():
    # Espera recibir mensajes todo el tiempo.
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode(UTF_8)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Probablemente el cliente dejó el chat.
            break


def send(event=None):  # Envía el mensaje
    msg = my_msg.get()
    my_msg.set("")  # Borra el campo de mensaje, porque ya se ha enviado
    client_socket.send(bytes(msg, UTF_8))
    if msg == "salir":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    # Esta función se llama cuando se va a cerrar la ventana.
    my_msg.set("salir")
    send()

top = tkinter.Tk()
top.title("Proyecto de Sockets")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Campo para escribir.
my_msg.set("Escribe aquí...")
scrollbar = tkinter.Scrollbar(messages_frame)  # Agrega una barra de navegación para mensajes anteriores
# Configuraciones para la barra de mensajes
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# --- Configuración de los sockets
# Cambiamos los sockets a los mismos que utiliza el servidor.

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not HOST: 
    HOST = '127.0.0.1'
if not PORT:
    PORT = 8081
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Inicia la ventana

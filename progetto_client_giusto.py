#client:

import socket
import Facilities as F

def manage_list(s):
    s.send(''.encode())
    data=s.recv(2048)
    data=F.bytes_to_list(data)
    for i in data:
        print(i)
    s.send(''.encode())
def manage_input(s):
    s.send(''.encode())
    data=s.recv(1024).decode()
    data=input(data)
    s.send(data.encode())

HOST = 'localhost'  # Indirizzo IP del server
PORT = 50007  # Porta su cui il server sta ascoltando

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def funz_password():
    for _ in range(3):
        password = input("Inserisci la password: ")
        s.send(password.encode())
        response = s.recv(1024).decode()
        if response == "Password corretta. Inizia la comunicazione":
            return True
        else:
            print(response)
    return False

if funz_password():
    print("Autenticazione riuscita. Puoi iniziare a effettuare le operazioni.")
    while True:
            s.send(' '.encode())
            data=s.recv(1024)
            
            if(data.decode()=='#777'):
                 manage_list(s)
            if(data.decode()=='#111'):
                manage_input(s)
            else:
                print('\n', data.decode())
                s.send(' '.encode())

else:
    print("Tentativi massimi raggiunti. Chiudo la connessione.")

s.close()
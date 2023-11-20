import pickle
import socket
import mysql.connector


def string_to_bytes(data):
    """
    metodo per trasformare le stringhe in bytes prima di inviarle con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, str):
        raise Exception("devi passare una stringa alla funzione string_to_bytes")

    return data.encode()


def bytes_to_string(data):
    """
    metodo per trasformare i bytes in stringhe una volta ricevute con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_string")

    return data.decode()


def list_to_bytes(data):
    """
    metodo per trasformare le liste in bytes prima di inviarle con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, list):
        raise Exception("devi passare una lista alla funzione list_to_bytes")
    list_converted = pickle.dumps(data)
    return list_converted



def bytes_to_list(data):
    """
    metodo per trasformare i bytes in liste una volta ricevute con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_list")

    return pickle.loads(data)


def dict_to_bytes(data):
    """
    metodo per trasformare dizionari in bytes prima di inviarli con l'utilizzo del metodo send
    della libreria socket
    """
    if not isinstance(data, dict):
        raise Exception("devi passare una lista alla funzione dict_to_bytes")
    list_converted = pickle.dumps(data, -1)
    return list_converted


def bytes_to_dict(data):
    """
    metodo per trasformare i bytes in dizionari una volta ricevuti con l'utilizzo del metodo recv
    della libreria socket
    """
    if not isinstance(data, bytes):
        raise Exception("devi passare dei bytes alla funzione bytes_to_dict")

    return pickle.loads(data)

def conn_to_database(ip_address,user_name,user_password,database_name,port):
    conn = mysql.connector.connect(
        host=ip_address, #127.0.0.1
        user=user_name,
        password=user_password,
        database=database_name,
        port=port, 
    )
    return conn

def send_a_list(data,conn):
    conn.send('#777'.encode())
    conn.recv(1024)
    data = list_to_bytes(data)
    conn.send(data)
    conn.recv(1024)


def input_send(data,conn):
    conn.send('#111'.encode())
    conn.recv(1024)
    conn.send(data.encode())
    return conn.recv(1024).decode()
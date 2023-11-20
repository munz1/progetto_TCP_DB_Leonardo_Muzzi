import socket
import mysql.connector
import Facilities as F

# Password autorizzata
PASSWORD = "tepsit"

def scegli_porta_logica(cont, listaPL):
    porta_logica = 0
    if cont != 0:
        while porta_logica < 1 or porta_logica > 2:
            porta_logica = int(F.input_send('Scegli la porta logica, Inserisci\n1-AND\n2-OR\n-->', conn))
        if porta_logica == 1:
            listaPL.append('AND')
        else:
            listaPL.append('OR')
    else:
        listaPL.append('AND')
        cont = 1

def crea_menu(nomi_lista):
    frase = ''
    for i in range(0, len(nomi_lista)):
        frase += f'\n{i}-{nomi_lista[i]}'
    return frase

def controllo_inserimento(frase, lista, conn, incr_in, incr_fin):
    scelta = -1
    while scelta < 0 + incr_in or scelta > len(lista) + incr_fin:
        try:
            scelta = int(F.input_send(frase, conn))
        except Exception as e:
            print(e)
            continue
    return scelta        

def crea_query_select(cur, conn):
    nomi_colonne = [i[0] for i in cur.description]
    frase_1 = 'Scegli la colonna su cui fare la condizione:'
    frase_1 += crea_menu(nomi_colonne)
    frase_1 += f'\n{len(nomi_colonne) + 1}-Concludi inserimento colonne\n-->'
    print(frase_1)
    scelta_col = -1
    parametri = []
    listaPL = []
    cont = 0
    while True:
        scelta_col = controllo_inserimento(frase_1, nomi_colonne, conn, 0, 1)
        if scelta_col == len(nomi_colonne) + 1:
            break
        frase_2 = f'Inserisci la condizione da applicare alla colonna {nomi_colonne[scelta_col]}(può essere un nome, una data, una posizione lavorativa, ecc...):'
        scelta_condizione = F.input_send(frase_2, conn)
        parametri.append({nomi_colonne[scelta_col]: scelta_condizione})
        scegli_porta_logica(cont, listaPL)
        cont = 1
    clausole = ''
    l = -1
    for i in parametri:
        l += 1
        for key, value in i.items():
            clausole += f"{listaPL[l]} {key} = '{value}' "
    return clausole

def scegli_nome_tabella(cur, conn):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = '5btepsit'"
    cur.execute(query)
    dati = cur.fetchall()
    F.send_a_list(dati, conn)
    flag = True
    while flag:
        nome_tabella = F.input_send('Inserisci il nome della tabella:', conn)
        for i in dati:
            if nome_tabella == i[0]:
                flag = False
                break
    return nome_tabella

def crea_query_insert(nome, tupla):
    msg = f"""INSERT INTO {nome}("""
    tup = ', '.join(tupla)
    msg += (tup +')')
    msg +=  ' VALUES '
    val = ','.join(['%s']*len(tupla))
    msg += f'({val})'
   
    return msg

def crea_query_update(conn, record, nomi_colonne):
    valori = []
    colonne = []
    attributo = 'SET '

    for i in range(1, len(nomi_colonne)):
        print(f'inizio input di {nomi_colonne[i]}')
        ins = F.input_send(f'Inserisci {nomi_colonne[i]} (inserisci "#" se non vuoi modificarlo):', conn)
        print(f'fine input di {nomi_colonne[i]}')
        if ins != '#':
            valori.append(ins)
            colonne.append(f'{nomi_colonne[i]} = %s')

    attributo += ', '.join(colonne)

    return attributo, tuple(valori)

#---------------funzioni_principali-----------------------------

def db_insert_into(client_conn): #FUNZIONE PER L'INSERIMENTO
    conn = F.conn_to_database('127.0.0.1', 'root', '', '5btepsit', 3306) #mi connetto al database
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur, client_conn) #prendo il nome della tabella richiesta
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()
    nomi_colonne = [i[0] for i in cur.description]
    query = crea_query_insert(nome_tabella, nomi_colonne[1::])
    print(query)
    valori = []
    k = -1
    while True:
        k += 1
        valori.append([])
        
        for i in range(1, len(nomi_colonne)):
            ins = F.input_send(f'Inserisci {nomi_colonne[i]}:', client_conn)
            valori[k].append(ins)
        scelta = 0
        
        while scelta < 1 or scelta > 2:
            scelta = int(F.input_send('Inserisci\n1-Continua\n2-Concludi\n-->', client_conn))
        if scelta == 2:
            break
    
    for i in valori:
        client_conn.send(f"{query}'\n' {i}".encode())
        cur.execute(query, tuple(i))
        conn.commit()

def db_leggi(client_conn):
    conn = F.conn_to_database('127.0.0.1', 'root', '', '5btepsit', 3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur, client_conn)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()        
    clausole = crea_query_select(cur, client_conn)
    query = f"SELECT * FROM {nome_tabella} where 1=1 {clausole}"
    cur.execute(query)
    dati = cur.fetchall()
    client_conn.send('Ecco i dati recuperati dal database date le condizioni inserite precedentemente:'.encode())
    client_conn.recv(1024)
    F.send_a_list(dati, client_conn)

def elimina_record(client_conn):
    conn = F.conn_to_database('127.0.0.1', 'root', '', '5btepsit', 3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur, client_conn)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    client_conn.send(f'Ecco i record presenti sulla tabella {nome_tabella}:'.encode())
    client_conn.recv(1024)
    client_conn.recv(1024)
    F.send_a_list(data, client_conn)

    while True:
        try:
            record_id = int(F.input_send("Scegli l'ID del record che vuoi eliminare:", client_conn))
            break
        except ValueError:
            print("Errore: Inserisci un ID valido.")
        except:
            continue
                  
    if nome_tabella == "dipendenti":  
        query = f'DELETE FROM {nome_tabella} WHERE id = {record_id}'
    else:
        query = f'DELETE FROM {nome_tabella} WHERE id_zona = {record_id}'
    print(f'query: {query}')
    cur.execute(query)
    conn.commit()
    client_conn.send(f"Record con ID {record_id} eliminato correttamente.".encode())
    client_conn.recv(1024)
    client_conn.recv(1024)

def altera_record(client_conn):
    conn = F.conn_to_database('127.0.0.1', 'root', '', '5btepsit', 3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur, client_conn)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    client_conn.send(f'Ecco i record prensenti sulla tabella {nome_tabella}:'.encode())
    client_conn.recv(1024)
    F.send_a_list(data, client_conn)
    client_conn.recv(1024)
    nomi_colonne = [j[0] for j in cur.description]
    while True:
        try:
            scelta = int(F.input_send("Scegli l'ID del record che vuoi modificare:", client_conn))
        except:
            continue

        for i in data:
            
            if(i[0]) == scelta:
                attributo, par = crea_query_update(client_conn, i, nomi_colonne)
                query = f'UPDATE {nome_tabella} {attributo} WHERE {nomi_colonne[0]} =  {scelta}'
                print(query)
                print
                cur.execute(query, par)
                conn.commit()
                return

#----------------------------------------------------main------------------------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 50007))
s.listen(1)

print("In attesa di connessioni...")

conn, addr = s.accept()
print('Connesso da', addr)

i = 0

while i < 3:
    password = conn.recv(1024).decode()
    if password == PASSWORD:
        conn.send("Password corretta. Inizia la comunicazione".encode())
        break
    else:
        i += 1
        tentativi_rimasti = 3 - i
        if i < 3:
            conn.send(f"Errore: Password sbagliata. Tentativi rimasti: {tentativi_rimasti}".encode())
        else:
            conn.send("Tentativi massimi raggiunti. Chiudo la connessione".encode())
            conn.close()
            exit()
data = -1
while data != 5:
    data = controllo_inserimento('Inserisci\n1-Inserire nuovo record\n2-Leggere dati tramite select\n3-Modificare un record\n4-Eliminare un record\n5-Chiudi la connessione\n-->', [1, 2, 3, 4, 5], conn, 0, 0)
    if data == 1:
        print('Eseguo nuovo record') #inserire
        db_insert_into(conn)
    elif data == 2:
        print('Eseguo leggere dati') #leggere
        db_leggi(conn)
    elif data == 3:
        print('Eseguo modifica record') #modificare
        altera_record(conn)
    elif data == 4:
        print('Eseguo eliminare record') #eliminare
        elimina_record(conn)

conn.send('Chiusura connessione...'.encode())
conn.close()

#server:

import socket
import mysql.connector
import Facilities as F

# Password autorizzata
PASSWORD = "tepsit"

def scegli_porta_logica(cont,listaPL):
    porta_logica = 0
    if(cont!=0):
        while(porta_logica<1 or porta_logica>2 ):
            porta_logica = int(F.input_send('Scegli la porta logica, Inserisci\n1-AND\n2-OR\n-->',conn))
        if(porta_logica==1):
            listaPL.append('AND')
        else:
            listaPL.append('OR')
    else:
        listaPL.append('AND')
        cont = 1

def create_menu(name_list):
    frase=''
    for i in range(0,len(name_list)):
        frase+=f'\n{i}-{name_list[i]}'
    return frase

def controllo_inserimento(frase,lista,conn,incr_in,incr_fin):
    scelta=-1
    while(scelta<0+incr_in or scelta>len(lista)+incr_fin):
        try:
            scelta=int(F.input_send(frase,conn))
        except Exception as e:
            print(e)
            continue
    return scelta        

def create_query_select(cur,conn):
    field_names = [i[0] for i in cur.description]
    frase_1 = 'Scegli la colonna su cui fare la condizione:'
    frase_1 += create_menu(field_names)
    frase_1 +=f'\n{len(field_names)+1}-Concludi inserimento colonne\n-->'
    print(frase_1)
    scelta_col=-1
    parametri = []
    listaPL = []
    cont=0
    while(True):
        scelta_col = controllo_inserimento(frase_1,field_names,conn,0,1)
        if scelta_col==len(field_names)+1 : break
        frase_2 = f'Inserisci la condizione da applicare alla colonna {field_names[scelta_col]}(può essere un nome, una data, una posizione lavorativa ect...):'
        scelta_condizione = F.input_send(frase_2,conn)
        parametri.append({field_names[scelta_col] : scelta_condizione})
        scegli_porta_logica(cont,listaPL)
        cont=1
    clausole = ''
    l = -1
    for i in parametri:
        l += 1
        for key,value in i.items():
            clausole += f"{listaPL[l]} {key} = '{value}' "
    return clausole

def scegli_nome_tabella(cur,conn):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = '5btepsit'"
    cur.execute(query)
    dati = cur.fetchall()
    F.send_a_list(dati,conn)
    flag = True
    while(flag):
        nome_tabella = F.input_send('Inserisci il nome della tabella:',conn)
        for i in dati:
            if(nome_tabella==i[0]) : 
                flag=False
                break
    return nome_tabella


def create_query_insert(nome, tupla):
    msg = f"""INSERT INTO {nome}("""
    tup = ', '.join(tupla)
    msg += (tup +')')
    msg +=  ' VALUES '
    val = ','.join(['%s']*len(tupla))
    msg += f'({val})'
   
    return msg

def create_query_update(conn,record,field_names):
    valori = []
    col = []
    attr = 'SET '

    for i in range(1,len(field_names)):
        print(f'inizio input di {field_names[i]}')
        ins = F.input_send(f'Inserisci {field_names[i]} (inserisci "#" se non vuoi modificarlo):',conn)
        print(f'fine input di {field_names[i]}')
        if ins != '#':
            valori.append(ins)
            col.append(f'{field_names[i]} = %s')

    attr += ', '.join(col)

    return attr,tuple(valori)
    

#---------------funzioni_principali-----------------------------

def db_insert_into(con_client): #FUNZIONE PER L'INSERIMENTO
    conn=F.conn_to_database('127.0.0.1','root','','5btepsit',3306) #mi connetto al database
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur,con_client) #prendo il nome della tabella richiesta
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()
    field_names = [i[0] for i in cur.description]
    query = create_query_insert(nome_tabella, field_names[1::])
    print(query)
    valori = []
    k=-1
    while(True):
        k+=1
        valori.append([])
        
        for i in range(1,len(field_names)):
            ins = F.input_send(f'Inserisci {field_names[i]}:',con_client)
            valori[k].append(ins)
        scelta=0
        
        while(scelta<1 or scelta>2):
            scelta=int(F.input_send('Inserisci\n1-Continua\n2-Concludi\n-->',con_client))
        if scelta==2:break
    
    for i in valori:
        con_client.send(f"{query}'\n' {i}".encode())
        cur.execute(query,tuple(i))
        conn.commit()

def db_read(con_client):
    conn=F.conn_to_database('127.0.0.1','root','','5btepsit',3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur,con_client)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()        
    clausole = create_query_select(cur,con_client)
    query = f"SELECT * FROM {nome_tabella} where 1=1 {clausole}"
    cur.execute(query)
    dati = cur.fetchall()
    con_client.send('Ecco i dati recuperati dal database date le condizioni inserite precedentemente:'.encode())
    con_client.recv(1024)
    F.send_a_list(dati,con_client)


def delete_record(con_client):
    conn=F.conn_to_database('127.0.0.1','root','','5btepsit',3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur, con_client)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    con_client.send(f'Ecco i record presenti sulla tabella {nome_tabella}:'.encode())
    con_client.recv(1024)
    con_client.recv(1024)
    F.send_a_list(data, con_client)

    while True:
        try:
            record_id = int(F.input_send("Scegli l'ID del record che vuoi eliminare:", con_client))
            break
        except ValueError:
            print("Errore: Inserisci un ID valido.")
        except:
            continue
                  
    if nome_tabella=="dipendenti":  
        query = f'DELETE FROM {nome_tabella} WHERE id = {record_id}'
    else:
        query = f'DELETE FROM {nome_tabella} WHERE id_zona = {record_id}'
    print(f'query: {query}')
    cur.execute(query)
    conn.commit()
    con_client.send(f"Record con ID {record_id} eliminato correttamente.".encode())
    con_client.recv(1024)
    con_client.recv(1024)



def alter_record(con_client):
    conn=F.conn_to_database('127.0.0.1','root','','5btepsit',3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur,con_client)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    con_client.send(f'Ecco i record prensenti sulla tabella {nome_tabella}:'.encode())
    con_client.recv(1024)
    F.send_a_list(data,con_client)
    con_client.recv(1024)
    field_names = [j[0] for j in cur.description]
    while(True):
        try:
            scelta = int(F.input_send("Scegli l'ID del record che vuoi modificare:",con_client))
        except:
            continue

        for i in data:
            
            if(i[0])==scelta:
                attr, par = create_query_update(con_client,i,field_names)
                query = f'UPDATE {nome_tabella} {attr} WHERE {field_names[0]} =  {scelta}'
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
print('Connected by', addr)

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
while(data!=5):
        data = controllo_inserimento('Inserisci\n1-Inserire nuovo record\n2-Leggere dati tramite select\n3-Modificare un record\n4-Eliminare un record\n5-Chiudi la connessione\n-->',[1,2,3,4,5],conn,0,0)
        if(data==1):
            print('Eseguo nuovo record') #inserire
            db_insert_into(conn)
        elif data==2:
            print('Eseguo leggere dati') #leggere
            db_read(conn)
        elif data==3:
            print('Eseguo modifica record') #modificare
            alter_record(conn)
        elif data==4:
            print('Eseguo eliminare record') #eliminare
            delete_record(conn)

conn.send('Chiusura connessione...'.encode())
conn.close()
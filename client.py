
import socket
import sys
import random
import os
import threading
import multiprocessing

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
NEW_WORKES = 15
def genera_richiesta(address, port):
    start_time_thread = time.time()
    print("client PID: %s, process name: %s, thread nme: %s" % (
        os.getpid()
        multiprocessing.current_process().name,
        threading.current_thread().name)
     )
    try:
        s = socket.socket() 
        s.connect((address, port)) 
        print(f"{threading.current_thread().name}Connessione al server:{address}:{port}")
    except s.error as errore:
        print(f"{threading.current_thread().name}errore... \n{errore}")
        sys.exit()
    comandi=['+','-','*','/']
    operazione = comandi[random.randint(0,3)]
    dati = str(operazione)+";"+str(random.randint(1,100))+";"str(random.randint(1,100))
    dati=dati.encode()
    s.send(dati)
    dati=s.recv(2048)
    if not dati:
        print(f"{threading.current_thread().name}: non risponde. exit")
    dati=dati.decode()
    print(f"{threading.current_thread().name}ricevuto")
    print(dati+'\n')
    dati=dati.encode()
    s.send(dati)
    s.close
    end_time_thread=time.time()
    print(f"{threading.current_thread().name}execution time=", end_time_thread - start_time_thread)
if __name__=='main':

    start_time=time.time()
    for _ in range(0,NUM_WORKERS):
        genera_richieste(SERVER_ADDRESS, SERVER_PORT)
    end_time=time.time()
    print("total SERIAL time=", end_time - start_time)
    
 
    start_time=time.time()
    threads=[threading.Thread(target=genera_richieste,args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time=time.time()
    print("total THREADS time=", end_time - start_time)
    
    
    start_time=time.time()
    processes=[multiprocessing.Process(target=genera_richieste,args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [processes.start() for process in processes]
    [processes.join() for process in processes]
    end_time=time.time()
    print("total PROCESSES time=", end_time - start_time)
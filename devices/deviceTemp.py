import os
import pickle
import random
import sys
import time
import socket
from datetime import datetime
import threading

temp = 20;
randomMode = 0
argumento =0
state = 'desligado'
msgTCP = ""
deviceType = 'temp sensor'
global addressRequisited
addressRequisited = ''
endThread = False
state = 'stand-by'


def conectTCP(addresses):
    while True:
        try:
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientTCP.connect((addresses["IP"], int(addresses["TCP"])))
            clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientUDP.connect((addresses["IP"], int(addresses["UDP"])))
        except:
            print("Não foi possivel conectar nesse endereço/porta")
            #os.remove("IoT-Tec502-PBL/devices/cache/ipServer.rp11")
            #addresses = requestIP()
            sys.exit(0)
        else:
            break
    return clientTCP, clientUDP
    
def IPalready():
    if (not os.path.isdir("IoT-Tec502-PBL/devices/cache/")) or not (os.path.isfile("IoT-Tec502-PBL/devices/cache/ipServer.rp11")):
        addresses = requestIP()
        return addresses
    else:
        return openIPCache()
    
def requestIP():
    print("Endereço IP do servidor não configurado");
    IPaddress = input("Digite o endereço IP do servidor: ")
    TCPport = input("Digite a porta de conexão TCP: ")
    UDPport = input("Digite a porta de conexão UDP: ")
    
    addresses = {"IP":IPaddress, "TCP":TCPport, "UDP": UDPport}
    print(addresses)
    
    return addresses

def openIPCache():
    with open(fr"IoT-Tec502-PBL/devices/cache/ipServer.rp11", 'rb') as addressesArq:
        addresses = pickle.load(addressesArq)
    print(addresses)
    return addresses

def setState(State):
    state = State;

def getState():
    return state

def getTemp(temp):
    if(randomMode):
        return random.randint(10, 50)
    else:
        return temp
    
def setTemp():
    temp = input('Digite o valor que deseja para a temperatura: ')
    while temp.isdigit() == False:
        print('digite o valor em numeros apenas')
        temp = input('Digite o valor que deseja para a temperatura: ')



def requestingTemp():
    if(argumento == 1):
        randomMode = 1
    else:
        randomMode = 0
        setTemp()

def decodeMensage():
    global state
    
    global msgTCP
    global endThread
    while True:
        time.sleep(0.5)
        #manda o dispositivo sair do stand-by
        if(msgTCP == "105"):
            state = 'ligado'
            print('ESTADO ATUAL',state)
            #sendMensageTCP(str(state))
        #manda desligar o dispositivo
        if(msgTCP == "106"):
            state = 'stand-by'
            #sendMensageTCP(str(state))
        if(msgTCP == "107"):
            restartDevice()
        if(msgTCP == '108'):
            shutdownRoutine()
        #requisita o estado do dispositivo
        if(msgTCP == "109"):
            sendMensageTCP(state)
        msgTCP = '400'

def sendMensageTCP(msg):
    msg = str(f"{msg}?{addressRequisited}")
    serverTCP.send(str(msg).encode())
    
       
def sendMensageUDP(msg):
    serverUDP.sendto(str(msg).encode(), (addresses["IP"], int(addresses["UDP"])))

def receiveMensage():
    global endThread
    global addressRequisited
    global msgTCP
    while True and not endThread:
        msg = serverTCP.recv(1024).decode()     
        msg =msg.split("?")
        
        print(msg)
        if isinstance(msg, list):
            addressRequisited = msg[1]
            
            msgTCP = msg[0]

def randomSelection(arg):
    
    if(int(arg) == 1):
        return 1
    elif(int(arg)==0):
        return 0

def restartDevice():
    global state
    
    state = 'reiniciando'
    print(state)
    time.sleep(1)
    state=('ligado')
    print(state)

def clearTerminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")

def sendTempConstantly():
    global endThread
    global state
    global serverUDP
    print(state)
    while True and not endThread:
        if(state == 'stand-by' or state == 'desligado'):
            temperature = 'none'
        else:
            temperature = getTemp(temp)
        # Obtendo a data e hora atual
        timeSend = datetime.now()
        #print(serverTCP.getsockname())
        infoSend = {}
        print(addressDisp)
        #usar o comando 100 para poder indicar no broker que ta mandando aquela informação
        infoSend[addressDisp] = (str(temperature), "100", deviceType, str(timeSend)[0:19], state)
        serverUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))

        time.sleep(1)

def shutdownRoutine():
    timeSend = datetime.now()
    global endThread
    global state
    endThread = True
    infoSend = {}
    state = 'desligado'
    infoSend[addressDisp] = (str(temp), "101", deviceType, str(timeSend)[0:19], state)
    sendMensageUDP(str(infoSend))
    serverTCP.close()
    serverUDP.close()

def menu():
    global state
    global randomMode
    global temp

    while 1 and not endThread:
        print('Menu')
        choice=input('1. Desligar\n2. Ligar\n3. Stand-by\n4. Mudar temperatura\n5. Modo Random Temp\nDigite a sua escolha: ')
        
        choice=int(choice)
        if(choice == 1): #desligamento fisico
            shutdownRoutine()
            print("Sensor desligado")
            break
        elif(choice==2):
            state = 'ligado'
        elif(choice == 3): #coloca o dispositivo em stand-by
            state = 'stand-by'
        elif(choice == 4):
            temp = input("Nova temperatura: ")
            randomMode = 0;
        elif(choice == 5):
            if(randomMode == 1):
                escolha = input("O modo de envio de temperatura aleatorio esta ativo, deseja mudar o estado?\nDigite [S]  para sim, ou [N] para nao\nDigite a sua escolha: ").lower()
                if(escolha == "s"):
                    randomMode = 0;
            else:
                escolha = input("O modo de envio de temperatura aleatorio esta desativado, deseja mudar o estado?\nDigite [S]  para sim, ou [N] para nao\nDigite a sua escolha: ").lower()
                if(escolha == "s"):
                    randomMode = 1;

        clearTerminal()

ipBroker= os.environ.get('IP_BROKER')
addresses = {'IP':ipBroker, 'UDP':'8081', 'TCP':"8080"}
#addresses = requestIP();
serverTCP, serverUDP = conectTCP(addresses)
addressDisp = socket.gethostbyname(socket.getfqdn())
receiverTCP = threading.Thread(target=receiveMensage, daemon=True).start()
sendRetorno = threading.Thread(target=decodeMensage, daemon=True).start()
sendTempFullTime = threading.Thread(target=sendTempConstantly, daemon=True).start()
menu = threading.Thread(target=menu, daemon=False ).start()

import signal
def handle_exit(sig, frame):
    shutdownRoutine()
    # Realize qualquer ação de limpeza necessária aqui
    sys.exit(0)

# Registrar o manipulador de sinal
signal.signal(signal.SIGINT, handle_exit)  # Captura Ctrl + C
signal.signal(signal.SIGTERM, handle_exit) 

    


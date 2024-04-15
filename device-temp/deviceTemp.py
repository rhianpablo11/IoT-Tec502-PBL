import os
import pickle
import random
import sys
import time
import socket
from datetime import datetime
import threading





argumento =sys.argv[1:]
print(argumento[0])
temp = 20;
randomMode = 0
state = 'desligado'
msgTCP = ""
deviceType = 'temp sensor'
global addressRequisited
addressRequisited = ''
def conectTCP(addresses):
    while True:
        try:
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientTCP.connect((addresses["IP"], int(addresses["TCP"])))
            clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientUDP.connect((addresses["IP"], int(addresses["UDP"])))
        except:
            print("Não foi possivel conectar nesse endereço/porta")
            os.remove("/cache/ipServer.rp11")
            addresses = IPalready()
        else:
            break
    return clientTCP, clientUDP
    
def IPalready():
    if (not os.path.isdir("/cache/")) or not (os.path.isfile("/cache/ipServer.rp11")):
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
    if not os.path.isdir('/cache/'):
        os.mkdir('/cache/')
    
    with open (fr"/cache/ipServer.rp11", 'wb') as addressesArq:
        pickle.dump(addresses, addressesArq)
    addressesArq.close()
    return addresses

def openIPCache():
    with open(fr"/cache/ipServer.rp11", 'rb') as addressesArq:
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
    state = state
    global msgTCP
    
    while True:
        if(msgTCP == "107"):
            sendMensageTCP(getTemp(temp))
        if(msgTCP == "105"):
            state = 'ligado'
            sendMensageTCP(str(state))
        if(msgTCP == "106"):
            state = 'desligado'
            sendMensageTCP(str(state))
        if(msgTCP == "108"):
            restartDevice()
            sendMensageTCP(str(state))
        if(msgTCP == "109"):
            sendMensageTCP(state)
        msgTCP = '400'

def sendMensageTCP(msg):
    msg = str(f"{msg}?{addressRequisited}")
    serverTCP.send(str(msg).encode())
    
       
def sendMensageUDP(msg):
    serverUDP.sendto(str(msg).encode(), (addresses["IP"], int(addresses["UDP"])))

def receiveMensage():
    while True:
        msg = serverTCP.recv(1024).decode()     
        msg =msg.split("?")
        global addressRequisited
        print(msg)
        if isinstance(msg, list):
            addressRequisited = msg[1]
            global msgTCP
            msgTCP = msg[0]

def randomSelection(arg):
    
    if(int(arg[0]) == 1):
        return 1
    elif(int(arg[0])==0):
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

    while True:
        temperature = getTemp(temp)
        # Obtendo a data e hora atual
        timeSend = datetime.now()
        addressDisp = socket.gethostbyname(socket.getfqdn())
        infoSend = {}
        #usar o comando 100 para poder indicar no broker que ta mandando aquela informação
        infoSend[addressDisp] = (temperature, "100", deviceType, str(timeSend))
        serverUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))



randomMode = randomSelection(argumento)
addresses = IPalready();
serverTCP, serverUDP = conectTCP(addresses)
receiverTCP = threading.Thread(target=receiveMensage, daemon=True).start()
sendRetorno = threading.Thread(target=decodeMensage, daemon=True).start()
sendTempFullTime = threading.Thread(target=sendTempConstantly, daemon=True).start()

while 1:
    print('Menu')
    choice=input('1. Desligar\n2. Ligar\n3. Reiniciar\n4. Mudar temperatura\n5. Modo Random Temp\nDigite a sua escolha: ')
    
    choice=int(choice)
    if(choice == 1): #desligamento fisico
        sendMensageTCP("desligando")
        serverTCP.close()
        serverUDP.close()
        print("Sensor desligado")
        break
    elif(choice==2):
        state = 'ligado'
    elif(choice == 3):
        restartDevice()
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

    


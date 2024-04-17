import os
import pickle
import random
import sys
import time
import socket
from datetime import datetime
import threading

state = 'desligado'
msgTCP = ""
channel = '3 - globo'
volume = 0
application = 'live Tv'


def conectTCP(addresses):
    while True:
        try:
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientTCP.connect((addresses["IP"], int(addresses["TCP"])))
            clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientUDP.connect((addresses["IP"], int(addresses["UDP"])))
        except:
            print("Não foi possivel conectar nesse endereço/porta")
            os.remove("cache/ipServer.rp11")
            addresses = IPalready()
        else:
            break
    return clientTCP, clientUDP

def IPalready():
    if (not os.path.isdir("cache/")) or not (os.path.isfile("cache/ipServer.rp11")):
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
    if not os.path.isdir('cache/'):
        os.mkdir('cache/')
    
    with open (fr"cache/ipServer.rp11", 'wb') as addressesArq:
        pickle.dump(addresses, addressesArq)
    addressesArq.close()
    return addresses

def openIPCache():
    with open(fr"/cache/ipServer.rp11", 'rb') as addressesArq:
        addresses = pickle.load(addressesArq)
    print(addresses)
    return addresses

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

def clearTerminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")

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

def restartDevice():
    global state
    
    state = 'reiniciando'
    print(state)
    time.sleep(1)
    state=('ligado')
    print(state)

def sendTempConstantly():

    while True:
        temperature = getTemp(temp)
        # Obtendo a data e hora atual
        timeSend = datetime.now()
        addressDisp = serverTCP.getsockname()[0]
        infoSend = {}
        #print(serverTCP.getsockname()[0])
        #usar o comando 100 para poder indicar no broker que ta mandando aquela informação
        infoSend[addressDisp] = (str(temperature), "100", deviceType, str(timeSend)[0:19])
        serverUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))



addresses = IPalready();
serverTCP, serverUDP = conectTCP(addresses);
receiverTCP = threading.Thread(target=receiveMensage, daemon=True).start()
sendRetorno = threading.Thread(target=decodeMensage, daemon=True).start()



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
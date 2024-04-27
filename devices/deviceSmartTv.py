import os
import pickle
import random
import sys
import time
import socket
from datetime import datetime
import threading
import signal

argumento =0
state = 'desligado'
deviceType = 'smart Tv'
addressRequisited = ''
endThread = False
state = 'stand-by'
clientTCP = None
clientUDP = None
msgTCP = ""
global channel
global volume
global application
channel = 3
volume = 0
application = 'Live Tv'
#ipBroker= os.getenv('IP_BROKER')
ipBroker='192.168.0.115'
connected = False
addresses = {'IP':ipBroker, 'UDP':8081, 'TCP':8080}
#addressDisp = socket.gethostbyname(socket.getfqdn())
addressDisp=ipBroker

def conectTCP():
    global clientUDP
    global clientTCP
    global connected
    global state
    count =0
    tempConnect = 0
    while True:
        try:
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientTCP.connect((addresses["IP"], int(addresses["TCP"])))
            clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientUDP.connect((str(addresses["IP"]), int(addresses["UDP"])))
        except:
            print("Não foi possivel conectar nesse endereço/porta\nNova reconexão ocorrerá em: ", tempConnect, "segundos")
            print('Tentativa de reconexão: ', count)
            count +=1
            connected = False
            state ='stand-by'
            time.sleep(tempConnect)
            tempConnect += 3
            clearTerminal()
        else:
            connected= True
            count=0
            break


def sendMensageTCP(msg):
    msg = str(f"{msg}?{addressRequisited}")
    clientTCP.send(str(msg).encode())

def sendMensageUDP(msg):
    clientUDP.sendto(str(msg).encode(), (addresses["IP"], int(addresses["UDP"])))

def receiveMensage():
    global endThread
    global addressRequisited
    global msgTCP
    global state
    global connected
    while True and connected:
        try:
            msg = clientTCP.recv(1024).decode()     
            msg =msg.split("?")
            print(msg)
            if isinstance(msg, list):
                addressRequisited = msg[1]
                msgTCP = msg[0]
                if(msgTCP == "105"):
                    state = 'ligado'
                elif(msgTCP == "106"):
                    state = 'stand-by'
                elif(msgTCP == "107"):
                    restartDevice()
                elif(msgTCP == '108'):
                    shutdownRoutine()
                elif(msgTCP=='109'): #mudar canal da tv
                    setChannel(msg[1])
                elif(msgTCP=='110'): #mudar volume da tv
                    setVolume(msg[1])
                    
                elif(msgTCP =='111'): #mudar app da tv
                    setApplicationOn(msg[1])
                msgTCP = '400'
        except:
            if(state!='desligado'):
                connected = False
                clearTerminal()
                print('Conexão com o servidor foi interrompida!')
                conectTCP()
            else:
                break

def setChannel(upOrDown):
    global channel
    if(channel=='none'):
        channel =1
    if(application == 'Live Tv'):
        if (channel == 5 and upOrDown=='up'):
            channel =1
        elif(channel==1 and upOrDown=='down'):
            channel = 5
        elif(upOrDown=='up'):
            channel+=1
        elif(upOrDown=='down'):
            channel-=1

def setVolume(vol):
    global volume
    volume = vol

def setApplicationOn(app):
    global application
    global channel
    application = app
    print(application)
    if(application !='Live Tv'):
        channel=0
    if(application == 'Live Tv'):
        if(channel=='none'):
            channel=3


def clearTerminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")

def restartDevice():
    global state
    state = 'reiniciando'
    print(state)
    time.sleep(1)
    state=('ligado')
    print(state)

def sendTempConstantly():
    global state
    global connected
    global channel
    global volume
    global application
    while True:
        if(connected):
            if(state == 'stand-by' or state == 'desligado'):
                channel = 0
                application = 'none'
                volume = 0
            else:
                
                if(application=='none'):
                    application='Live Tv'
            # Obtendo a data e hora atual
            timeSend = datetime.now()
            #print(clientTCP.getsockname())
            infoSend = {}
            packetInfo = {}
            packetInfo = {'channel': channel, 'app': application, 'volume': volume}
            
            #usar o comando 100 para poder indicar no broker que ta mandando aquela informação
            infoSend[addressDisp] = (str(packetInfo), "100", deviceType, str(timeSend)[0:19], state)
            
            try:
                clientUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))
            except:
                connected=False
            time.sleep(1)

def shutdownRoutine():
    timeSend = datetime.now()
    global endThread
    global state
    global connected
    endThread = True
    infoSend = {}
    packetInfo = {'channel': channel, 'app': application, 'volume': volume}
    state = 'desligado'
    connected = False
    infoSend[addressDisp] = (str(packetInfo), "101", deviceType, str(timeSend)[0:19], state)
    clientUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))
    clientTCP.close()
    clientUDP.close()

def menu():
    global state
    while 1:
        if(connected):
            print('Menu')
            choice=input('1. Desligar\n2. Ligar\n3. Stand-by\n4. Trocar Canal\n5. Mudar Volume\n6. Trocar App\nDigite a sua escolha: ')
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
                print(f'Canal atual: {channel}')
                newChannel = input('Digite [+] para aumentar de canal, ou [-] para diminuir\nSua escolha: ')
                if(newChannel =='+'):
                    setChannel('up')
                elif(newChannel == '-'):
                    setChannel('down')
            elif(choice == 5):
                print(f'Volume atual: {volume}')
                newVolume = input('Digite [+] para aumentar o volume, ou [-] para diminuir\nSua escolha: ')
                if(newVolume =='+'):
                    setVolume('up')
                elif(newVolume == '-'):
                    setVolume('down')
            elif(choice == 6):
                print(f'App atual: {application}')
                print(f'Lista de apps disponiveis:\n   1. Youtube\n   2. Live Tv\n   3. Amazon Prime Tv\n   4. Netflix')
                newApp = input('Digite o numero do app de desejo\nSua escolha: ')
                if(newApp =='1'):
                    setApplicationOn('Youtube')
                elif(newApp == '2'):
                    setApplicationOn('Live Tv')
                elif(newApp == '3'):
                    setApplicationOn('Amazon Prime')
                elif(newApp == '4'):
                    setApplicationOn('Netflix')
            clearTerminal()  


conectTCP()
receiverTCP = threading.Thread(target=receiveMensage, daemon=True).start()
sendTempFullTime = threading.Thread(target=sendTempConstantly, daemon=True).start()
menu = threading.Thread(target=menu, daemon=True ).start()


def handle_exit(sig, frame):
    shutdownRoutine()
    # Realize qualquer ação de limpeza necessária aqui
    sys.exit(0)

# Registrar o manipulador de sinal
signal.signal(signal.SIGINT, handle_exit)  # Captura Ctrl + C
signal.signal(signal.SIGTERM, handle_exit) 

while 1 and (state != 'desligado'):
    pass
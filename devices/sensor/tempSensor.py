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
global name
name = "sensor de temperatura"
addressRequisited = ''
endThread = False
state = 'stand-by'
clientTCP = None
clientUDP = None
addressDisp =socket.gethostbyname(socket.gethostname())

#ipBroker= os.getenv('IP_BROKER')
ipBroker='192.168.0.115'
connected = False

addresses = {'IP':ipBroker, 'UDP':8081, 'TCP':8080}
addressDisp = socket.gethostbyname(socket.getfqdn())



def conectTCP():
    global clientUDP
    global clientTCP
    global connected
    global state
    global addressDisp
    count =0
    tempConnect = 0
    while True:
        try:
            clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientTCP.connect((addresses["IP"], int(addresses["TCP"])))
            clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientUDP.connect((str(addresses["IP"]), int(addresses["UDP"])))
            clientTCP.settimeout(10)
            #addressDisp=clientTCP.getsockname()[1]
        except:
            clearTerminal()
            print("Não foi possivel conectar nesse endereço/porta\nNova reconexão ocorrerá em: ", tempConnect, "segundos")
            print('Tentativa de reconexão: ', count)
            count +=1
            connected = False
            state ='stand-by'
            time.sleep(tempConnect)
            tempConnect += 3
            
        else:
            clearTerminal()
            print("Conexão estabelecida/restabelecida")
            print('Menu\n1. Desligar\n2. Ligar\n3. Stand-by\n4. Mudar temperatura\n5. Modo Random Temp\nDigite a sua escolha: ')
            connected= True
            count=0
            break
    
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


def receiveMensage():
    global endThread
    global addressRequisited
    global msgTCP
    global state
    global connected
    global name
    while True and connected:
        try:
            msgPadrao =False
            msg = clientTCP.recv(1024).decode()     
            msg =msg.split("?")

            if isinstance(msg, list):
                addressRequisited = msg[1]
                msgTCP = msg[0]
                if(msgTCP == '104'):
                    name = msg[1]
                    msgPadrao =True
                elif(msgTCP == "105"):
                    state = 'ligado'
                    msgPadrao =True
                    #sendMensageTCP(str(state))
                #manda desligar o dispositivo
                elif(msgTCP == "106"):
                    state = 'stand-by'
                    msgPadrao =True
                    #sendMensageTCP(str(state))
                elif(msgTCP == "107"):
                    restartDevice()
                    msgPadrao =True
                elif(msgTCP == '108'):
                    shutdownRoutine()
                    msgPadrao =True
                elif (msgTCP == '103'):
                    msgPadrao =True
                    pass
                msgTCP = '400'
        except:
            if(state!='desligado' or not msgPadrao):
                connected = False
                clearTerminal()
                print('Conexão com o servidor foi interrompida!')
                conectTCP()
            else:
                break

            


def restartDevice():
    global state
    state = 'reiniciando'

    time.sleep(1)
    state=('ligado')


def clearTerminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")

def sendTempConstantly():
    global state
    global connected
    while True:
        if(connected):
            if(state == 'stand-by' or state == 'desligado'):
                temperature = 'none'
            else:
                temperature = getTemp(temp)
            # Obtendo a data e hora atual
            timeSend = datetime.now()
            #print(clientTCP.getsockname())
            infoSend = {}

            #usar o comando 100 para poder indicar no broker que ta mandando aquela informação
            infoSend[addressDisp] = (str(temperature), "100", deviceType, str(timeSend)[0:19], state, name)
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
    state = 'desligado'
    connected = False
    infoSend[addressDisp] = (str(temp), "101", deviceType, str(timeSend)[0:19], state, name)
    clientUDP.sendto(str(infoSend).encode(), (addresses["IP"], int(addresses["UDP"])))
    clientTCP.close()
    clientUDP.close()

def menu():
    global state
    global randomMode
    global temp
    while 1:
        if(connected):
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

    
        




conectTCP()
receiverTCP = threading.Thread(target=receiveMensage, daemon=True).start()
sendTempFullTime = threading.Thread(target=sendTempConstantly, daemon=True).start()
menu = threading.Thread(target=menu, daemon=True ).start()


import signal
def handle_exit(sig, frame):
    shutdownRoutine()
    # Realize qualquer ação de limpeza necessária aqui
    sys.exit(0)

# Registrar o manipulador de sinal
signal.signal(signal.SIGINT, handle_exit)  # Captura Ctrl + C
signal.signal(signal.SIGTERM, handle_exit) 

    
while 1 and (state != 'desligado'):
    pass

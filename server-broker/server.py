import socket
import threading
import os
import sys
import pickle
from datetime import datetime, timedelta, time
from flask import *
import json
import time
from flask_cors import CORS

global devices
devices = {}
msg=''
global mensages
mensages = {}
namePC = socket.gethostname()
ipPC =socket.gethostbyname(socket.gethostname())
#IP = socket.gethostbyname(socket.gethostname())
IP = '0.0.0.0'
print('IP SERVER: ',IP)
print('NOME DO PC: ', namePC)
print('IP DO PC: ', ipPC)
app = Flask(__name__)
CORS(app)

@app.route('/devices', methods=['GET'])
def getDevices():
    devicesList = []
    for device in devices:
        if(device in mensages):
            auxJson = {
                "address": device,
                "name": devices[device][1],
                "lastData": mensages[device][0],
                "type": mensages[device][1],
                "timeLastData":mensages[device][2],
                "deviceState": mensages[device][3]
            }
        else:
            auxJson = {
                "address": device,
                "name": devices[device][1],
                "lastData": "undefined",
                "type": "undefined",
                "timeLastData": "undefined",
                "deviceState": "desligado"
            }
        devicesList.append(auxJson)
    return make_response(jsonify(devicesList))


@app.route("/devices", methods=['PATCH'])
def updateDataInterface():
    elemento = request.json
    for device in devices:
        if (str(device) == elemento["address"]):
            devices[device][1] = elemento["name"]
            return make_response(jsonify(
                {
                    "address": device,
                    "name": devices[device][1],
                    "lastData": mensages[device][0],
                    "type": mensages[device][1],
                    "timeLastData":mensages[device][2],
                    "deviceState": "conected"
                }
            ))
    return make_response(jsonify(elemento))

@app.route('/devices/control', methods=['PATCH'])
def comandsControlDevice():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+IP).encode())
    return make_response(jsonify(elemento))

@app.route('/devices/delete', methods=['DELETE'])
def comandDeleteDevice():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+IP).encode())
    return make_response(jsonify(elemento))


@app.route('/devices/tv/control/app', methods=['PATCH'])
def comandsControlDeviceTv():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+elemento['app']+'?'+IP).encode())
    return make_response(jsonify(elemento))




def saveDevice(connection, address):
    #mandar informando o dispositivo para o CLIENT HTTP
    #receber esse valor e colocar na variavel deviceName
    deviceName = "nomeGenerico"
    hourConnection = datetime.now()
    devices[address[0]] = [connection, deviceName, str(hourConnection)]

def startServer():
    global serverTCP
    global serverUDP
    #SERVIDOR TCP
    serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverTCP.bind((IP, 8080))
    serverTCP.listen(1)

    #SERVIDOR UDP
    serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverUDP.bind((IP, 8081))

def acceptConnection():
    while True:
        connection, address = serverTCP.accept()
        saveDevice(connection, address)

def receiveMensagesUDP():
    global msg
    while True:
        msgUDP = serverUDP.recv(1024).decode()
        msg = eval(msgUDP)
        organizeInfosReceived(msg)

def organizeInfosReceived(dicioMensage):
    for device in dicioMensage:
        #vai verificar se a mensagem é a de envio padrao
        if(dicioMensage[device][1] == '100'):
            if(dicioMensage[device][2] == 'temp sensor'):
                if((device in mensages) and type(mensages[device][0])==list):
                    histTemp = mensages[device][0]
                else:
                    histTemp = []
                if(len(histTemp)>10):
                    histTemp.pop(-1)
                histTemp.insert(0, (dicioMensage[device][0], dicioMensage[device][3]))
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo
                mensages[device] = (histTemp, dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4])
            else:
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo
                dataTv = eval(dicioMensage[device][0])
                mensages[device] = (dataTv, dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4])
            if(device in devices):
                devices[device][2]=dicioMensage[device][3]
        elif (dicioMensage[device][1] == '101'):
            mensages.pop(device)
            devices.pop(device)


def sendMensageTCP(address, mensage):
    devices[address][0].send(str(mensage).encode())

def init():
    startServer()

#se der problema aqui, voltar a olhar pelas mensagens
def deviceStatus():
    while True:
        devicesCopy = devices.copy()
        for device in devicesCopy:
            
            data = datetime.now() -datetime.strptime(devices[device][2][0:19], '%Y-%m-%d %H:%M:%S')
            #print(f'\n{devices[device][2][0:19]}\nDEVICE: {device} TEMPO: {data.total_seconds()}\n')
            time.sleep(1)
            if(int(data.total_seconds() / 10)>=1):
               
                devices.pop(device)
                if(device in mensages):
                    mensages.pop(device)

#manda mensagem constantemente com um codigo para indicar que o server ta conectado na rede
def sendTCPgetStatus():
    while 1:
        devicesCopy = devices.copy()
        for device in devicesCopy:
            sendMensageTCP(device, f'01?{IP}')
        time.sleep(2)

def clearTerminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")


threading.Thread(target=app.run, args=(IP,8082), daemon=True).start()
init()
connecting = threading.Thread(target=acceptConnection, daemon=True).start()
chuvaMensages = threading.Thread(target=receiveMensagesUDP, daemon=True).start()
deviceIsOk = threading.Thread(target=deviceStatus, daemon=True).start()
threading.Thread(target=sendTCPgetStatus, daemon=True).start()

while 1:
    print('IP SERVER: ',IP)
    print('NOME DO PC: ', namePC)
    print('IP DO PC: ', ipPC)
    print('DEVICES: ', devices)
    time.sleep(0.3)
    clearTerminal()
    pass



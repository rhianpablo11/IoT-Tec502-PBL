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
                "name": mensages[device][4],
                "lastData": mensages[device][0],
                "type": mensages[device][1],
                "timeLastData":mensages[device][2],
                "deviceState": mensages[device][3]
            }
        else:
            auxJson = {
                "address": device,
                "name": 'undefined',
                "lastData": "undefined",
                "type": "undefined",
                "timeLastData": devices[device][1],
                "deviceState": "desligado"
            }
        devicesList.append(auxJson)
    response = make_response(jsonify(devicesList))
    response.headers['Cache-Control'] = 'public, max-age=1'
    return response



@app.route("/devices", methods=['PATCH'])
def updateDataInterface():
    elemento = request.json
    for device in devices:
        if (str(device) == elemento["address"]):
            devices[device][1] = elemento["name"]
            sendMensageTCP(device, str("104"+"?"+elemento["name"]+"?"+IP))
            response = make_response(jsonify({
                    "Nome anterior": mensages[device][4],
                    "novo nome": elemento["name"]
                }))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
            
        
    response = make_response(jsonify({"Response":"Endereço invalido, o endereço enviado não existe"}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/devices/control', methods=['PATCH'])
def comandsControlDevice():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+IP).encode())
            response = make_response(jsonify({"comando":elemento['comand']}))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
            
    response = make_response(jsonify({"Response":"Endereço invalido, o endereço enviado não existe"}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response
    

@app.route('/devices/delete', methods=['DELETE'])
def comandDeleteDevice():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+IP).encode())
            response = make_response(jsonify({"comando":elemento['comand']}))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    response = make_response(jsonify({"Response":"Endereço invalido, o endereço enviado não existe"}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


@app.route('/devices/tv/control/app', methods=['PATCH'])
def comandsControlDeviceTv():
    elemento = request.json
    for device in devices:
        if(str(device) == elemento['address']):
            devices[device][0].send(str(elemento['comand']+'?'+elemento['app']+'?'+IP).encode())
            response = make_response(jsonify({"comando":elemento['comand']}))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    response = make_response(jsonify({"Response":"Endereço invalido, o endereço enviado não existe"}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response




def saveDevice(connection, address):
    #mandar informando o dispositivo para o CLIENT HTTP
    #receber esse valor e colocar na variavel deviceName
    hourConnection = datetime.now()
    devices[address[0]] = [connection, str(hourConnection)]

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
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo, nome do dispositivo
                mensages[device] = (histTemp, dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4], dicioMensage[device][5])
            else:
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo, nome do dispositivo
                dataTv = eval(dicioMensage[device][0])
                mensages[device] = (dataTv, dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4], dicioMensage[device][5])
            if(device in devices):
                devices[device][1]=dicioMensage[device][3]
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
            
            data = datetime.now() -datetime.strptime(devices[device][1][0:19], '%Y-%m-%d %H:%M:%S')
            #print(f'\n{devices[device][2][0:19]}\nDEVICE: {device} TEMPO: {data.total_seconds()}\n')
            
            if(int(data.total_seconds() / 10)>=1):
                if(device in devices):
                    devices.pop(device)
                if(device in mensages):
                    mensages.pop(device)

#manda mensagem constantemente com um codigo para indicar que o server ta conectado na rede
def sendTCPgetStatus():
    while 1:
        devicesCopy = devices.copy()
        for device in devicesCopy:
            sendMensageTCP(device, f'103?{IP}')
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
    #print('THREADS: ', threading.enumerate())
    print('\n             DEVICES: ')
    deviceCopy = devices.copy()
    for device in deviceCopy:
        if(device in mensages):
            print('==================================')
            print("=====> HORA ATUAL: ",str(datetime.now())[11:19])
            print(f'=====> NAME: {mensages[device][4]}\n=====> ADDRESS: {device}\n=====> HOUR LAST DATA: {devices[device][1][11:19]}')
            print('==================================')
    time.sleep(0.3)
    clearTerminal()
    pass



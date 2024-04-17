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

IP = socket.gethostbyname(socket.getfqdn())

app = Flask(__name__)
CORS(app)

@app.route('/devices', methods=['GET'])
def getDevices():
    devicesList = []
    print("DEVICES",devices)
    print('MENSAGES', mensages)
    for device in devices:
        print('DEVICE', device)
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


@app.route("/devices", methods=['PUT'])
def updateDataInterface():
    elemento = request.json
    for device in devices:
        if (device == elemento["address"]):
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


threading.Thread(target=app.run, args=(IP,8082), daemon=True).start()


def saveDevice(connection, address):
    #mandar informando o dispositivo para o CLIENT HTTP
    #receber esse valor e colocar na variavel deviceName
    deviceName = "nomeGenerico"
    
    devices[address[1]] = [connection, deviceName]
    print("DISPOSITIVOS ",devices)


'''
Vai tentar mandar uma mensagem requisitando o status do dispositivo,
se ele responder com desligado, vai pedir entao para ligar o dispositivo,
caso nao consiga contado com o dispositivo, ele vai pegar e retirar o dispositivo
do dicionario de dispositivos
'''
def conectionTest():
    for device in devices:
        try:
            devices[device][0].send(str("109").encode())
            try:
                msgReturned =devices[device][0].recv(1024).decode()
            except:
                devices[device][0].send(str("105").encode())
        except:
            #remover do dicionario
            devices.pop(device)
            pass

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
                histTemp.insert(0, dicioMensage[device][0])
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo
                mensages[device] = (histTemp, dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4])
            else:
                #chave o endereço ip do dispositivo = dado enviado, tipo do dispositivo, horario que enviou, estado do dispositivo
                mensages[device] = (dicioMensage[device][0], dicioMensage[device][2], dicioMensage[device][3], dicioMensage[device][4])
        elif (dicioMensage[device][1] == '101'):
            mensages.pop(device)
            devices.pop(device)


def sendMensageTCP(address, mensage):
    devices[address][0].send(str(mensage).encode())

def init():
    startServer()
    conectionTest()

def receiveMensageTCP(address):
    response = devices[address][0].recv(1024).decode()
    #separa a resposta em uma lista, onde:
        #primeiro[0] elemento é sempre o codigo de retorno
        #segundo[1] elemento é o conteudo
        #terceiro[2] elemento é quem pediu 
    response = response.split("?")
    #CHAMAR FUNÇÃO PARA ENVIAR VIA HTTP

def deviceStatus():
    while True:
        mensagesCopy = mensages.copy()
        for mensage in mensagesCopy:
            data = datetime.now() - datetime.strptime(mensages[mensage][2][0:19], '%Y-%m-%d %H:%M:%S')
            if(int(data.total_seconds() / 3600)>=1):
                print("dispositivo deu problema ai viu")
                try:
                    devices[mensage][0].send(str("109").encode())
                    devices[mensage][0].settimout(10)
                    resp = devices[mensage][0].recv(1024).decode()
                except:
                    devices.pop(mensage)
                    mensages.pop(mensage)
    



init()

connecting = threading.Thread(target=acceptConnection, daemon=True).start()
chuvaMensages = threading.Thread(target=receiveMensagesUDP, daemon=True).start()
deviceIsOk = threading.Thread(target=deviceStatus, daemon=True).start()


while 1:
    kk= input("digite: ")
    print(mensages)
    print(devices)
    #print(devices['192.168.0.115'][0].recv(1024).decode())
    if(kk == "1"):
        serverTCP.close()
        serverUDP.close()
        break
    if(kk =='2'):
        mens = input('digita ai mane: ')
        mens += str("?"+socket.gethostbyname(socket.getfqdn()))
        print(mens)
        sendMensageTCP('172.16.103.10', mens )
        #print(devices['192.168.0.115'][0].recv(1024).decode())

'''===================================================================================='''
'''===============================PARTE DA API REST====================================='''
'''===================================================================================='''




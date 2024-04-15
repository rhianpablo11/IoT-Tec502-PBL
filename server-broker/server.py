import socket
import threading
import os
import sys
import pickle
from datetime import datetime, timedelta, time
from flask import *
import json
import time

global devices
devices = {}
msg=''
global mensages
mensages = {}
data = [{}]


app = Flask(__name__)

@app.route('/devices')
def getDevices():
    devicesList = []
    return make_response(jsonify(devicesList))


@app.route("/devices", methods=['PUT'])
def updateDataInterface():
    elemento = request.json
    data = loadBD()
    for device in data:
        if (device["address"] == elemento["address"]):
            device["name"] = elemento["name"]
    saveBD(data)
    return make_response(jsonify(data))


threading.Thread(target=app.run, args=("localhost",8082), daemon=True).start()


def saveDevice(connection, address):
    #mandar informando o dispositivo para o CLIENT HTTP
    #receber esse valor e colocar na variavel deviceName
    deviceName = "nomeGenerico"
    devices[address[0]] = (connection, deviceName)
    print("DISPOSITIVOS ",devices)
    loadData()
    insertData(address)

    
    

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
    serverTCP.bind(('192.168.0.115', 8080))
    serverTCP.listen(1)

    #SERVIDOR UDP
    serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverUDP.bind(("192.168.0.115", 8081))

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
            mensages[device] = (dicioMensage[device][0], dicioMensage[device][2], dicioMensage[device][3])

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
        for mensage in mensages:
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
                    #retirar do json tambem
    

def saveData(data):
    with open (fr"server-broker/data.json", 'w') as dataArq:
        json.dump(data, dataArq, indent=4)
    dataArq.close()

def updateData():
    loadData()
    global data

    for elements in data:
        print(elements)
        print(mensages)
        if('192.168.56.1' in mensages):
            elements["lastData"] = str(mensages['192.168.56.1'][0])
            elements["type"] = str(mensages['192.168.56.1'][1])
    saveData(data)

def callUpdateData():
    time.sleep(1)
    while True:
        updateData()
        time.sleep(3)



init()

connecting = threading.Thread(target=acceptConnection, daemon=True).start()
chuvaMensages = threading.Thread(target=receiveMensagesUDP, daemon=True).start()
deviceIsOk = threading.Thread(target=deviceStatus, daemon=True).start()
threading.Thread(target=callUpdateData, daemon=True).start()

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
        sendMensageTCP('192.168.0.115', mens )
        print(devices['192.168.0.115'][0].recv(1024).decode())

'''===================================================================================='''
'''===============================PARTE DA API REST====================================='''
'''===================================================================================='''

        
#     #print(serverUDP.recv(1024).decode())
#     #connection.send(str("107").encode())
#     print(msg)
#     # print(msg)
#     # if(msg == "desligando"):
#     #     serverTCP.close()
#     #     serverUDP.close()
#     #     break
#     #print(serverUDP.recv(1024).decode())




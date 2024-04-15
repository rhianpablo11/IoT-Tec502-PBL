from flask import *
import socket
import threading
app = Flask(__name__)

lista =[{}]
def loadBD():
    with open('server-broker/data.json', 'r') as file:
        data = json.load(file)
    return data

def saveBD(data):
    with open (fr"server-broker/data.json", 'w') as dataArq:
        json.dump(data, dataArq, indent=4)
    dataArq.close()
# def updateJson():
#     global lista
#     while 1:
#         lista = loadBD()

# threading.Thread(target=updateJson, daemon=True).start()




clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientTCP.connect(('192.168.0.115', 8080))

@app.route('/devices')
def getLivros():
    lista = loadBD()
    return make_response(jsonify(lista))

# @app.route('/livros', methods=['PUT'])
# def pedeTemp():
#     clientTCP.send(str('ENTRE OUTRA VIAS').encode())
#     return str('jsonify(lista)')

@app.route("/devices", methods=['PUT'])
def updateDataInterface():
    elemento = request.json
    data = loadBD()
    for device in data:
        if (device["address"] == elemento["address"]):
            device["name"] = elemento["name"]
    saveBD(data)
    return make_response(jsonify(data))

app.run(port=8082, host="localhost")

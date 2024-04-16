# import threading
# valor =5
# print("primeiro valor: ", valor)
# def somar(n1, n2):
#     print(n1+n2)
#     global valor 
#     valor = n1+n2
#     return n1+n2
# test = threading.Thread(target=somar, args=(2, 2)).start()

# device = {}
# device["oi"] = "lamaour"
# print(device)
# print(test)
# print("ultimo valor: ", valor)
import socket
print(socket.getfqdn())
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
dico={}
dico["ok"] = "valor"
dico['blz'] =" engual"

print(dico)
dico["ok"] = "etecetera"
print(dico)

from datetime import datetime

# Obtendo a data e hora atual
data_hora_atual = datetime.now()

# Extraindo a hora e o dia atual
hora_atual = data_hora_atual.hour
dia_atual = data_hora_atual.day

print("Hora atual:", hora_atual)
print("Dia atual:", dia_atual)
print(data_hora_atual.time())



# Dicionário de exemplo
dicionario = {'chave1': 'valor1', 'chave2': 'valor2', 'chave3': 'valor3'}
print(dicionario)
# Remover um elemento por chave usando pop
valor_removido = dicionario.pop('chave2')

print("Valor removido:", valor_removido)
print(dicionario)
for a in dicionario:
    print(a)


from datetime import *
print(time.fromisoformat('14:46:57.766715').minute)
print((datetime.combine(datetime.today(), datetime.now().time()) - timedelta(hours=time.fromisoformat('14:46:57.766715').hour, minutes=time.fromisoformat('14:46:57.766715').minute)).time())



from datetime import datetime, timedelta

# Definindo duas horas
hora_inicial = datetime.strptime('09:30', '%H:%M')
hora_final = datetime.strptime('13:45', '%H:%M')
print(hora_final)
# Calculando a diferença entre as duas horas
diferenca = hora_final - hora_inicial

# Extraindo a diferença em horas e minutos
diferenca_horas = diferenca.total_seconds() / 3600  # Convertendo segundos para horas
diferenca_minutos = (diferenca.total_seconds() % 3600) / 60  # Convertendo segundos restantes para minutos

print("Diferença total:", diferenca)
print("Diferença em horas:", diferenca_horas)
print("Diferença em minutos:", diferenca_minutos)


import threading

lista = {'id':54}
if(lista['id']):
    print('oia eu aqui')


<div align='center'>

# Problema 1 - IoT System 

</div>

> Este é um projeto da disciplina TEC502 - Modulo Integrador - Concorrencia e Conectividade, em que visa estabelecer comunicação entre computadores ligados na mesma rede, utilizando para isso diferentes protocolos de comunicação.

## Download do repositorio

<div align='center'>
O download pode ser feito via clone do repositorio executando o seguinte comando no terminal:

``` bash
git clone https://github.com/rhianpablo11/IoT-Tec502-PBL.git
```

</div>

## Como executar 
O desenvolvimento do projeto teve como um dos pilares a comunicação via rede entre as 3 partes: [Servidor](#servidor-broker), [Dispositivos](#dispositivo), e [Interface](#)

1. ### Em computadores diferentes
   1. Acesse a pasta geral do projeto pelo terminal
   2. Escolha qual parte do projeto deseja executar na maquina
      1. Para executar a <b>[Servidor Broker](#servidor-broker)</b> use os seguintes comandos:
          ``` bash
          docker build --pull --rm -f "server-broker/Dockerfile" -t server:latest "server-broker"
          ```
          
          ``` bash
          docker container run -it --network host server
          ```
          1. Para executar a <b>[Interface](#interface)</b> use os seguintes comandos:
           ``` bash
           docker build --pull --rm -f "interface/Iot-system/Dockerfile" -t interface:latest "interface/Iot-system"
           ```
           
           ``` bash
           docker container run -it --network host interface
           ```
       2. Para executar o dispositivo <b>[Televisão](#smart-tv)</b> use os seguintes comandos:
          ``` bash
           docker build --pull --rm -f "devices/tv/Dockerfile" -t televisao:latest "devices/tv"
           ```
           
           ``` bash
           docker container run -it --network host televisao
           ```
       3. Para executar o dispositivo <b>[sensor de temperatura](#sensor-de-temperatura)</b> use os seguintes comandos:
          ``` bash
           docker build --pull --rm -f "devices/sensor/Dockerfile" -t sensor:latest "devices/sensor"
           ```
           
           ``` bash
           docker container run -it --network host sensor
           ```
2. ### No mesmo computador
   1. Acesse a pasta geral do projeto pelo terminal
   2. Execute o comando para executar o [Servidor Broker](#servidor-broker):
         ``` bash
         docker compose up server interface --build
         ```
   3. Execute os seguintes comandos em outra guia do terminal para executar o dispositivo, uma guia por dispositivo:
      1. Para executar o dispositivo [Televisão](#smart-tv):
         ``` bash
           docker compose tv --build
         ```
         ``` bash
           docker container run -it --network iot-tec502-pbl_iot-system-network -e IP_BROKER=server iot-tec502-pbl-tv
           ```
         
       2. Para executar o dispositivo [Sensor de temperatura](#sensor-de-temperatura):
           ``` bash
           docker compose sensor --build
           ```
           ``` bash
           docker container run -it --network iot-tec502-pbl_iot-system-network -e IP_BROKER=server iot-tec502-pbl-sensor
           ```
## Estrutura do projeto
A estrutura utilizada na construção do projeto se divide em 3 elementos:
  
- ` Interface:` Responsavel por apresentar os dados enviados pelos dispositivos, além de oferecer opções de gerenciamento de cada um deles
- `` Servidor Broker:`` Responsavel por receber os dados do dispositivo e enviar para a interface quando requisitado, além de receber os comandos da interface para controle de um dispositivo e enviar o que foi selecionado
- ``` Dispositivo:``` Este simula um dispositivo real, oferecendo funções simuladas via software. Ele realiza o envio constante de dados sobre o seu estado atual
  
## Servidor Broker
O servidor Broker é a parte central de todo esse projeto, sendo responsavel por estabelecer comunicação com os dispositivos, sensor de temperatura e Smart TV, assim como com a interface. Para tal ação ele necessita uma conexão, TCP e UDP, com cada dispositivo para que possa enviar comandos e receber os dados do dispositivo. O envio e recebimento de dados com a interface ocorre usando o protocolo HTTP, não exigindo o firmamento de uma conexão com o servidor.
Ainda deve-se pontuar o [gerenciamento dos dados recebidos](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L131), para manter sempre os ultimos dados recebidos salvos, e estruturados. Essa estrutura padrão é um dos pilares que permite o funcionamento em conjunto dos 3 dispositivos. Segue a estrutura padrão utilizada:
- Address: É a chave do dicionario de mensagens. Contém o endereço IP do dispositivo
- LastData: contém o ultimo dado recebido pelo dispositivo
- Type: contém o tipo do dispositivo
- HourLastData: contém o horario em que recebeu o ultimo dado
- DeviceStatus: contém o estado do dispositivo, se está ligado por exemplo
- Name: contém o nome do dispositivo 

### Funcionamento
O servidor broker desenvolvido na linguagem python, tem o papel de realizar multiplas ações ao mesmo tempo. Em decorrencia de precisar lidar com multiplos dispositivos conectados, recebendo requisições HTTP, e dados via UDP, além do processamento dessas informações e envio de dados seja para o dispositivo, seja para a interface. Afim de permitir dinamismo na operação o uso de threads é essencial para o funcionamento.

## Dispositivo
Para realizar a simulação de um dispositivo de Internet das Coisas(*Internet of Things*, IoT), houve a necessidade de criar um programa que realizasse as ações de um.
Os dispotivos haviam uma restrição na sua criação, em que eles só devem ser capazes de realizar comunicação via TCP ou UDP, o que aumentou a necessidade do servidor, já que este faz uma especie de tradução para receber comandos da interface e enviar para o dispositivo.<br>
Com o proposito de padronizar a comunicação para melhor efetividade e escalabilidade, foi decidido usar comandos nas trocas de mensagens. A escolha, permite que sejam enviados um pacote menor de dados pela rede, além de que este simplifica o pedir de ações. Tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos) descreve os comandos e o que cada um realiza.
<div align="center">

#### Possíveis comandos dos dispositivos

| Comandos | Ações dentro do dispositivo                                                                                                                                                |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 103      | Indica para o dispositivo que o servidor ainda esta ativo na rede. Essa mensagem, ou qualquer um dos outros codigos tem que chegar no intervalo de 10 segundos             |
| 104      | Realiza a alteração no nome do dispositivo                                                                                                                                 |
| 105      | Realiza a alteração de estado do dispositivo, <b>ligando-o</b>                                                                                                             |
| 106      | Realiza a altaração de estado do dispositivo, <b>desligando-o</b>                                                                                                          |
| 107      | Pede ao dispositivo para ele se auto reiniciar, trocando de estado para desligado, e após para ligado                                                                      |
| 108      | Pede para o dispositivo entrar na rotina de "shutdown", dessa forma ele proprio se auto desliga, e envia um ultimo comando para que o servidor apague ele dos dados salvos |
| 109*     | Indica que uma troca de canal esta sendo requisitada                                                                                                                       |
| 110*     | Indica que uma troca de volume atual esta sendo requisitada                                                                                                                |
| 111*     | Indica que uma troca de applicativo esta sendo sendo requisitada                                                                                                           |

<p>* comandos que funcionam apenas na SmartTv</p>
</div>
Tais dispositivos precisam estar aptos para realizar operações em segundo plano, como por exemplo escutar o recebimento de novos comandos e realizar a operação desejada. Para que isso fosse possível, o uso de Threads foi essencial, tendo em vista que ao criar um thread para uma funcionalidade, ela opera em paralelo as outras. Nesse projeto, os dispositivos contam com 3 Threads adicionais a Thread principal.

- [Thread Principal]():
  - Mantém o programa ativo por meio de um *while True* e a verificação de estado do dispositivo. Assim que o estado é alterado para desligado, o programa se encerra por sair do loop.
- [Thread "receiverTCP"]():
  - Fica ouvindo a chega de novos comandos vindos do servidor, por meio de conexão TCP. Com o comando recebido ela verifica qual o significado dele para poder executar a determinada operação.
  - Verifica se o servidor ainda se mantem ativo, já que se ele passar mais de 10 segundos sem enviar uma mensagem via socket TCP, é acionado um alerta de desconexão, todos threads são pausados, e é iniciada a [rotina de reconexão]().
- [Thread "sendDataFullTime"]():
  - Realiza o envio de dados continuamente para o servidor, por meio de conexão UDP
- [Thread "menu"]():
  - Permite que a função que apresenta no terminal as funções de controle, e recebe a opção a ser operada, escolhida pelo usuario, fique em execução. Isso simula um comando fisico no dispositivo

Para o funcionamento continuo cada uma dessas threads, executa uma função em que as operações internas estão envolvidas por um *[while True]()*, para que permaneçam executando, saindo apenas quando o programa finalizar. Internamente ao loop, é posto um [*if*, em que a condição é estar conectado com o servidor](), a partir do momento em que a conexão é cortada, o script interno ao *if* deixa de ser realizado.

Os dispositivos, conforme requisito, podem ser controlados via terminal usando linhas de comando. Esta operação simula o uso do dispositivo fisicamente, a exemplo apertar o botão liga e desliga. Sendo assim, há 2 formas de controle: via terminal, simulando o dispositivo fisico, ou pela interface, neste caso o comando trafega pela rede ate chegar ao dispositivo. A depender do comando requisitado, uma função é chamada para poder executar a ação. Essa ocorrencia se tem maior presença na [Smart Tv](#smart-tv) por possuir mais funcionalidades.

O controle desdes dispositivos pela interface possui 4 funcionalidades genericas, conforme descrito na tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos). Contudo, no caso da [Smart Tv](#smart-tv), por possuir funções especificas de controle, ela possui comandos a mais, além de junto com esses comandos receber um argumento descrevendo melhor a operação a ser realizada.

É importante ressaltar que o dispositivo a partir do momento que consegue estabelecer conexão com o servidor, ele inicia a enviar o pacote de informações constantemente para ele. O envio só é encerrado ao realizar o desligamento do dispositivo. Dentre os dados enviados no pacote:

- Address:
  - Endereço IP do dispositivo. É a chave do dicionario enviado.
- Data:
  - informação do dispositivo, por exemplo temperatura atual
- Codigo da mensagem:
  - Informa para o servidor se a mensagem é de envio comum, codigo '100', ou se o dispositivo esta informando o seu desligamento, codigo '101'. No caso do codigo '101', o dispositivo é apagado dos dicionarios do servidor.
- Tipo do dispositivo:
  - Informa qual tipo do dispositivo que esta enviando a mensagem. É importante para o servidor saber como organizar o dado recebido por aquele dipositivo
- Horario:
  - Serve para informar o horário em que a mensagem foi enviada
- Estado do dispositivo:
  - Informa sobre o dispositivo esta ligado, ou em stand-by, ou desligado
- Nome:
  - Informa o nome do dispositivo. Inicialmente esse nome é generico, após troca dele pela interface, o dispositivo recebe um novo nome que passa a ser enviado.


### Sensor de temperatura
Este dispositivo, busca simular um sensor de temperatura que se conecta a rede usando os protocolos TCP e UDP. Por ser um dispositivo mais generico, não possui função de controle externa adicional às padrões. Por conseguinte o dado enviado por ele no campo [Data](#L69) é apenas o valor inteiro da temperatura.

O "Sensor de Temperatura", possui algumas opções de configurações que podem ser realizadas via terminal, graças a um menu que é apresentado na tela. Dentre as opções:

- Liga/Desliga
- Colocar em stand-by
  - Quando nessa opção o dispositivo continua a enviar informações, porém o dado de temperatura enviado é "none"
- Troca da temperatura
  - Nessa opção é possivel a troca do valor pré-definido por o valor escolhido
- Selecionar o modo aleatorio de temperatura
  - Quando essa opção esta ativada, a temperatura enviada para o servidor é um valor aleatorio entre 10 e 50.
### Smart TV
Este dispositivo busca simular uma Televisão Smart, contudo que realiza conexão para troca de dados de controle, apenas via TCP e UDP. Este dispositivo possui mais funcionalidades que o [Sensor de Temperatura](#sensor-de-temperatura), logo mais opções de controle via interface, assim como via terminal estão disponiveis. Dentre as disponiveis estão controle do canal selecionado no momento, o aplicativo que esta rodando na televisao, assim como o volume atual da televisão. Por consequencia o pacote de dados enviado contém mais informações no campo "data". Dentre as informações:
- Canal:
  - informa sobre o canal da televisão que esta selecionado no momento. Sendo disponibilizados 5 canais.
- Aplicativo:
  - informa sobre qual aplicativo esta sendo executado no momento na televisão. Existem 4 possibiveis: "Amazon Prime", "Netflix", "Youtube", "Live Tv"
- Volume:
  - informa sobre o volume atual que esta configurado na televisão. Este que tem o intervalo de 0 a 100.

## Interface

A interface é o componente visual do projeto. Com o funcionamento utilizando protocolo de comunicação HTTP, foi desenvolvida uma interface grafica para facilitar controle das funções dos dispositivos, além da visualização dos dispositivos conectados. Para o desenvolvimento utilizou-se do framework [React JS](), visando dinamismo na apresentação dos elementos na tela.

Uma estrutura foi desenvolvida para poder abacar diferentes situações em que poderiam acontecer tanto em relação ao servidor, como em relação aos dispositivos conectados. Um [componente]() foi criado com o intuito de ser "pai" dos outros subsequentes. Isso decorre deste ser responsável por [requisitar dados para o servidor](), e repassar estes para os componentes filhos.

Diante disso, as telas apresentam uma tela geral que serve de background para os outros componentes. É nesse background em que é apresentado a [informação sobre a conexão com o servidor](), se conectado ou desconectado. Além disso, apresenta [boas vindas para o usuario](), e a data e hora atual. Caso o servidor esteja desconectado, nenhum outro componente é renderizado na tela, contudo com o servidor conectado outras 2 vertentes surgem a depender se há dispositivos conectados ao servidor. Considerando o primeiro caso, um componente é renderizado informando que não há dispositivos conectados, e assim que houver eles irão aparecer. Todavia no segundo caso, de haver dispositivos conectados é apresentado então os componentes para lidar com isso.

A tela com dispositivos conectados, é a principal, tendo em vista que apresenta a lista de dispositivos conectados, as informações atualizadas que os dispositivos enviam, além de na lateral direita apresentar, quando selecionado um dispositivo, opções de controle. Caso não tenha dispositivos selecionados é informado nesse componente.



## Comunicação
Um dos pontos principais do projeto é a comunicação entre os modulos do projeto, para que a informação possa ser 


### Comunicação Servidor-Interface

A comunicação HTTP realizada pela interface para com o [servidor](#servidor-broker) ocorre seguindo os padrões da API Restful.

As requisições feitas pela interface, 
### Comunicação Servidor-Dispositivo

## Testes

A execução de testes foi essencial para a realização do projeto

## Conclusão

## Referencias

<div align='center'>

# Problema 1 - IoT System 

</div>


> Este é um projeto da disciplina TEC502 - Modulo Integrador - Concorrencia e Conectividade. Este há o problema de comunicação entre 2 modulos que utilizam meios diferentes de comunicação na rede. Visando solucionar foi desenvolvido os modulos, além de um servidor broker para poder permitir a comunicação, 2 dispositivos e 1 interface que se conectam com o broker para se comunicarem. Para isso foi feito uso de sockets de comunicação nos protocolos TCP e UDP, para os dispositivos, além de uma API Rest para a interface.


## Download do repositorio

<div align='center'>
O download pode ser feito via clone do repositorio executando o seguinte comando no terminal:

``` bash
git clone https://github.com/rhianpablo11/IoT-Tec502-PBL.git
```

</div>

## Como executar 
O desenvolvimento do projeto teve como um dos pilares a comunicação via rede entre as 3 partes: [Servidor](#servidor-broker), [Dispositivos](#dispositivo), e [Interface](#interface)

### 1. Em computadores diferentes
   1. Acesse a pasta geral do projeto pelo terminal
   2. Escolha qual parte do projeto deseja executar na maquina
      1. Para executar a <b>[Servidor Broker](#servidor-broker)</b> use os seguintes comandos:
          ``` bash
          docker build --pull --rm -f "server-broker/Dockerfile" -t server:latest "server-broker"
          ```
          
          ``` bash
          docker container run -it --network host server
          ```
          1. Para executar a <b>[Interface](#interface)</b> primeiro acesse o arquivo [ipBroker.js](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/interface/Iot-system/src/ipBroker/ipBroker.js) e troque o endereço IP pelo o do servidor, após use os seguintes comandos:
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
           docker container run -it --network host -e IP_BROKER=[ip do dispositivo] televisao
           ```
       3. Para executar o dispositivo <b>[sensor de temperatura](#sensor-de-temperatura)</b> use os seguintes comandos:
           ``` bash
           docker build --pull --rm -f "devices/sensor/Dockerfile" -t sensor:latest "devices/sensor"
           ```
           
           ``` bash
           docker container run -it --network host -e IP_BROKER=[ip do dispositivo]  sensor
           ```
### 2. No mesmo computador
   1. Acesse a pasta geral do projeto pelo terminal
   2. Execute o comando para executar o [**Servidor Broker**](#servidor-broker):
         ``` bash
         docker compose up server interface --build
         ```
   3. Execute os seguintes comandos em outra guia do terminal para executar o dispositivo, uma guia por dispositivo:
      1. Para executar o dispositivo [**Televisão**](#smart-tv):
           ``` bash
           docker compose tv --build
           ```
           ``` bash
           docker container run -it --network iot-tec502-pbl_iot-system-network -e IP_BROKER=server iot-tec502-pbl-tv
           ```
         
       2. Para executar o dispositivo [**Sensor de temperatura**](#sensor-de-temperatura):
           ``` bash
           docker compose sensor --build
           ```
           ``` bash
           docker container run -it --network iot-tec502-pbl_iot-system-network -e IP_BROKER=server iot-tec502-pbl-sensor
           ```



## Introdução

Com o avanço da computação, uma das áreas que vem sofrendo um crescimento expressivo é a de Internet das Coisas(IoT). Esse termo nomeia um sistema de sensores, e/ou dispositivos físicos conectados à internet. Isso permite que estes dispositivos sejam controlados, bem como os dados deles possam ser visualizados pela internet. O uso da IoT pode ser tanto residencial, como pode ser expandido para grandes aplicações industriais.

Um dos pilares da IoT, é a comunicação dos dispositivos com uma aplicação via internet. Diante disso, o meio de comunicação, assim como a forma de se comunicar entre eles tem de estar em consonância. Contudo, uma *startup* do ramo estando com problemas nessa comunicação, ao dispositivo se comunicar de uma maneira diferente da apresentada na aplicação, resolveu contratar uma equipe para desenvolver um serviço *broker*. Esse que por sua vez permite a comunicação, ao receber as mensagens em ambos os formatos, e enviar para o dispositivo de desejo da maneira correta para que seja entendida a mensagem.

Através do contexto apresentado, o projeto descrito neste documento traz informações sobre o desenvolvimento dos softwares necessários, o dispositivo, o servidor broker e a interface, e adjunto as soluções necessárias para solucionar esse problema, e tornar o sistema funcional.

## Fundamentação teorica

Um dos pontos principais do projeto é o uso de sockets de comunicação. Este que por sua vez é um elemento que permite a conexão entre 2 dispositivos utilizando rede, para funcionar precisa de um endereço IP, bem como uma porta de comunicação. Esses sockets trafegam na rede direcionados a um servidor do tipo broker, e deste para o destino, seja aplicação ou dispositivo. Um servidor Broker é um serviço responsável por receber mensagens de dispositivos, realizar o tratamento e por fim disponibilizar para a aplicação. No caso deste projeto, os dados dos dispositivos ficam salvos no servidor aguardando uma requisição pedindo por eles.

Diferentes abordagens desses sockets foram utilizadas de acordo com a necessidade. Dentre elas, houve socket TCP, visando cobrir uma abordagem confiável da troca de mensagens, o socket UDP para a abordagem não confiável da transferência de dados, e por fim para comunicação da aplicação com os dispositivos emulados, houve uso de sockets HTTP por meio de uma API RESTful. As 3 abordagens apresentam representações de camadas diferentes dos protocolos de rede. No caso da HTTP se encontra na camada da aplicação, obtendo maior abstração, enquanto o TCP e UDP se encontram em camadas mais baixas, na de transporte, com menor nível de abstração. Outro ponto a ser ressaltado é no quesito confiabilidade, já que o TCP é orientado a conexão, logo para enviar um dado uma conexão prévia tem de ter sido realizada, além da entrega em sequência dos dados enviados. Entretanto estes pontos não estão presentes no protocolo UDP, tornando-o menos confiável.

Não menos importante, o uso de Threads foi essencial para que o projeto funcionasse. Estas que por sua vez permitiam que num mesmo programa executasse funções em paralelo. Isso se assemelha a separar o programa em várias partes, e executar todas ao mesmo tempo cada uma em seu terminal. Entretanto, caso realizasse a implementação da forma anterior, haveria o problema de comunicação entre as partes. Um dos problemas que não deixou de ocorrer utilizando da maneira correta, por meio de threads no mesmo programa, contudo que pode ser resolvido utilizando variáveis globais. Essa solução permite inicializar uma variável e alterar o valor dela no escopo global do código mesmo estando no escopo da função.



## Metodologia

Visando desenvolver o projeto, os conceitos teóricos apresentados na [Fundamentação teórica](#fundamentação-teorica) foram essenciais para cada parte do projeto. Conforme principal problema a ser resolvido, estava a possibilidade de comunicar a aplicação, que possui comunicação HTTP, aos dispositivos, que se comunicam em baixo nível com sockets TCP e UDP, e vice-versa. Para solução, um servidor do tipo broker foi necessário para permitir a comunicação entre os dispositivos e a interface. Considerando isso, o servidor se faz necessário possuir ambas as formas de comunicação, a de alto nível, como a de baixo nível.

Ademais, no projeto foi feito uso da ferramenta de *Docker*, a fim de permitir que a aplicação seja executada por meio de containers separados. Dessa maneira, cada módulo do projeto foi desenvolvida a sua própria imagem, para poder ser executada em um container separado. Assim um dos requisitos do projeto pode ser contemplado.


## Implementação

  ### Estrutura do projeto
  A estrutura utilizada na construção do projeto se divide em 3 elementos:
    
  - [**`Interface`**](#interface):
    - Responsável por apresentar os dados enviados pelos dispositivos, além de oferecer opções de gerenciamento de cada um deles.
    - Desenvolvido utilizando a framework "React js" para o javascript
  - [**`` Servidor Broker:``**](#servidor-broker)
    - Responsável por receber os dados do dispositivo e enviar para a interface quando requisitado, além de receber os comandos da interface para controle de um dispositivo e enviar o que foi selecionado
    - Desenvolvido utilizando a linguagem python
  - [**``` Dispositivo:```**](#dispositivo)
    - Este simula um dispositivo real, oferecendo funções simuladas via software. Ele realiza o envio constante de dados sobre o seu estado atual
    - Desenvolvido utilizando a linguagem python
    
### Servidor Broker
O servidor Broker é a parte central de todo esse projeto, sendo responsável por estabelecer comunicação com os dispositivos, sensor de temperatura e Smart TV, assim como com a interface. Para tal ação ele necessita de uma conexão, TCP e UDP, com cada dispositivo para que possa enviar comandos e receber os dados do dispositivo. O envio e recebimento de dados com a interface ocorre usando o protocolo HTTP, não exigindo o firmamento de uma conexão com o servidor.
  Ainda deve-se pontuar o [gerenciamento dos dados recebidos](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L151), para manter sempre os últimos dados recebidos salvos, e estruturados. Tal ação permite que as requisições de dados feita pelo cliente sejam respondidas mais rápido, tendo em vista não precisar pedir estes do dispositivo. Essa estrutura padrão de organização dos dados recebidos é um dos pilares que permite o funcionamento em conjunto dos 3 dispositivos. Segue a estrutura padrão utilizada:
  - **Address**: É a chave do dicionário de mensagens. Contém o endereço IP do dispositivo
  - **LastData**: contém o último dado recebido pelo dispositivo
  - **Type**: contém o tipo do dispositivo
  - **HourLastData**: contém o horário em que recebeu o último dado
  - **DeviceStatus**: contém o estado do dispositivo, se está ligado por exemplo
  - **Name**: contém o nome do dispositivo 

  A fim de permitir as diversas funções em conjunto no servidor, foi essencial utilização de Threads, para permitir execução de funções em segundo plano, enquanto outras operam. Essa forma de implementar proporciona maior dinamismo, e execução com maior desempenho em relação a execução de operações sequencialmente, além de que dados poderiam  ser facilmente perdidos nessa última situação. A exemplo do uso dos Threads, a organização das mensagens recebidas enquanto o servidor pode aceitar novas conexões de outros dispositivos. Dentre os Threads utilizados:
  - [**Thread Principal**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L221):
    Tem o papel de executar o código que mantém o sistema ativo por meio de um while True. Nesse [bloco de código](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L221) há impressão de texto na tela com algumas informações principais sobre o servidor. Dentre as informações estão: O endereço IP do servidor, o nome do host em que está rodando o servidor, o ip deste host, e logo após uma lista dos dispositivos, contendo o nome, o endereço IP e a hora do último dado recebido.
  - [**Thread para aceitar conexões**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L216):
    A função dessa thread se concentra em aceitar a conexão de novos dispositivos, e por conseguinte salvá-los no *Hash Map* que contém os dispositivos, e os objetos de conexão. Dessa forma o Hashmap contém o endereço IP do dispositivo como chave, e o objeto de conexão e a hora da última comunicação do dispositivo como valores.
  - [**Thread para receber mensagens**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L217):
    Realiza a função de ficar escutando por novas mensagens provindas dos dispositivos. Estas mensagens chegam via protocolo UDP. Para cada mensagem recebida é chamada a função [organizeInfosReceived](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L151), a qual organiza a mensagem no dicionário de mensagens. Com isso, caso seja a primeira mensagem do dispositivo, ela é adicionada no dicionário, em caso contrário, a mensagem presente é atualizada pela última recebida.
  - [**Thread para verificar se o dispositivo está ativo**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L218):
    Serve para poder verificar se os dispositivos salvos ainda estão ativos, e em caso contrário realiza limpeza deste ao excluí-lo do *Hash Map*. Vale ressaltar que os dispositivos enviam dados continuamente a cada 1 segundo, e essa verificação permite uma pausa de 9 segundos sem recebimento de mensagem no servidor.
  - [**Thread para enviar sinal de atividade para o dispositivo**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L219):
    Sua função é enviar para todos os dispositivos uma mensagem com código "103". Essa mensagem é um dos indicativos para os dispositivos de que o servidor está operante. Assim, quando o servidor cai, os dispositivos conseguem reconhecer e pausar a execução para tentar reconectar-se novamente.
  - [**Thread para executar a API REST**](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/server-broker/server.py#L214):
    Tem o papel de executar a framework Flask, para poder funcionar a API REST, e atender as requisições recebidas via HTTP.



  ### Dispositivo
  Para realizar a simulação de um dispositivo de Internet das Coisas(*Internet of Things*, IoT), houve a necessidade de criar um programa que realizasse as ações de um.
  Os dispositivos haviam uma restrição na sua criação, em que eles só devem ser capazes de realizar comunicação via TCP ou UDP, o que aumentou a necessidade do [servidor broker](#servidor-broker), já que este faz uma espécie de tradução para receber comandos da interface e enviar para o dispositivo.<br>
  Com o propósito de padronizar a comunicação para melhor efetividade e escalabilidade, foi decidido usar comandos nas trocas de mensagens. A escolha, permite que sejam enviados um pacote menor de dados pela rede, além de que este simplifica o pedido de ações, além de permitir que novos dispositivos sigam o mesmo padrão base de funcionamento. Tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos) descreve os comandos que os dispositivos aceitam e o que cada um realiza.

  <div align="center">

  ##### Possíveis comandos dos dispositivos

  | Comandos | Ações dentro do dispositivo                                                                                                                                                |
  | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 103      | Indica para o dispositivo que o servidor ainda está ativo na rede. Essa mensagem, ou qualquer um dos outros códigos tem que chegar no intervalo de 10 segundos             |
  | 104      | Realiza a alteração no nome do dispositivo                                                                                                                                 |
  | 105      | Realiza a alteração de estado do dispositivo, <b>ligando-o</b>                                                                                                             |
  | 106      | Realiza a alteração de estado do dispositivo, <b>desligando-o</b>                                                                                                          |
  | 107      | Pede ao dispositivo para ele se auto reiniciar, trocando de estado para desligado, e após para ligado                                                                      |
  | 108      | Pede para o dispositivo entrar na rotina de "shutdown", dessa forma ele próprio se auto desliga, e envia um último comando para que o servidor apague ele dos dados salvos |
  | 109*     | Indica que uma troca de canal está sendo requisitada                                                                                                                       |
  | 110*     | Indica que uma troca de volume atual está sendo requisitada                                                                                                                |
  | 111*     | Indica que uma troca de aplicativo está sendo sendo requisitada                                                                                                           |


  <p>* comandos que funcionam apenas na SmartTv</p>
  </div>
  Tais dispositivos precisam estar aptos para realizar operações em segundo plano, como por exemplo escutar o recebimento de novos comandos e realizar a operação desejada. Para que isso fosse possível, o uso de Threads foi essencial, tendo em vista que ao criar um thread para uma funcionalidade, ela opera em paralelo às outras. Nesse projeto, os dispositivos contam com 3 Threads adicionais a Thread principal.

  - [Thread Principal](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L277):
    - Mantém o programa ativo por meio de um *while True* e a verificação de estado do dispositivo. Assim que o estado é alterado para desligado, o programa se encerra por sair do loop. Ao realizar essa saída as outras Threads são também encerradas.
  - [Thread "receiverTCP"](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L263):
    - Fica ouvindo a chegada de novos comandos vindos do servidor, por meio de conexão TCP. Com o comando recebido ela verifica qual o significado dele para poder executar determinada operação.
    - Verifica se o servidor ainda se mantém ativo, já que se ele passar mais de 10 segundos sem enviar uma mensagem via socket TCP, é acionado um alerta de desconexão, todos threads são pausados, e é iniciada a [rotina de reconexão]().
  - [Thread "sendDataFullTime"](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L264):
    - Realiza o envio de dados continuamente para o servidor, por meio de conexão UDP
  - [Thread "menu"](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L265):
    - Permite que a função que apresenta no terminal as funções de controle, e recebe a opção a ser operada, escolhida pelo usuário, fique em execução. Isso simula um comando fisico no dispositivo

  Para o funcionamento contínuo cada uma dessas threads, executa uma função em que as operações internas estão envolvidas por um *[while True](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L180)*, para que permaneçam executando, saindo apenas quando o programa finalizar. Internamente ao loop, é posto um [*if*, em que a condição é estar conectado com o servidor](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/devices/tv/television.py#L181), a partir do momento em que a conexão é cortada, o script interno ao *if* deixa de ser realizado. Como efeito disso, o programa pausa suas operações quando a conexão com o servidor é perdida.

  Os dispositivos, conforme requisito, podem ser controlados via terminal usando linhas de comando. Esta operação simula o uso do dispositivo fisicamente, a exemplo apertar o botão liga e desliga. Sendo assim, há 2 formas de controle: via terminal, simulando o dispositivo físico, ou pela interface, neste caso o comando trafega pela rede, passando pelo servidor e após poder chegar ao dispositivo. A depender do comando requisitado, uma função é chamada para poder executar a ação. Essa ocorrência se tem maior presença na [Smart Tv](#smart-tv) por possuir mais funcionalidades.

  O controle desses dispositivos pela interface possui 4 funcionalidades genéricas, conforme descrito na tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos). Contudo, no caso da [Smart Tv](#smart-tv), por possuir funções específicas de controle, ela possui comandos a mais, além de junto com esses comandos receber um argumento descrevendo melhor a operação a ser realizada.

  É importante ressaltar que o dispositivo a partir do momento que consegue estabelecer conexão com o servidor, ele inicia a enviar o pacote de informações constantemente para ele. O envio só é encerrado ao realizar o desligamento do dispositivo. Dentre os dados enviados no pacote:

  - Address:
    - Endereço IP do dispositivo. É a chave do dicionário enviado.
  - Data:
    - informação do dispositivo, por exemplo temperatura atual
  - Código da mensagem:
    - Informa para o servidor se a mensagem é de envio comum, código '100', ou se o dispositivo está informando o seu desligamento, código '101'. No caso do código '101', o dispositivo é apagado dos dicionários do servidor.
  - Tipo do dispositivo:
    - Informa qual tipo do dispositivo que está enviando a mensagem. É importante para o servidor saber como organizar o dado recebido por aquele dispositivo
  - Horário:
    - Serve para informar o horário em que a mensagem foi enviada
  - Estado do dispositivo:
    - Informa sobre o dispositivo está ligado, ou em stand-by, ou desligado
  - Nome:
    - Informa o nome do dispositivo. Inicialmente esse nome é genérico, após troca dele pela interface, o dispositivo recebe um novo nome que passa a ser enviado.


  #### Sensor de temperatura
  Este dispositivo, busca simular um sensor de temperatura que se conecta a rede usando os protocolos TCP e UDP. Por ser um dispositivo mais genérico, não possui função de controle externa adicional às padrões. Por conseguinte o dado enviado por ele no campo *Data* é apenas o valor inteiro da temperatura.

  O "Sensor de Temperatura", possui algumas opções de configurações que podem ser realizadas via terminal, graças a um menu que é apresentado na tela. Dentre as opções:

  - Liga/Desliga
  - Colocar em stand-by
    - Quando nessa opção o dispositivo continua a enviar informações, porém o dado de temperatura enviado é "none"
  - Troca da temperatura
    - Nessa opção é possível a troca do valor pré-definido por o valor escolhido
  - Selecionar o modo aleatório de temperatura
    - Quando essa opção está ativada, a temperatura enviada para o servidor é um valor aleatório entre 10 e 50.

  #### Smart TV
  Este dispositivo busca simular uma Televisão Smart, contudo que realiza conexão para troca de dados de controle, apenas via TCP e UDP. Este dispositivo possui mais funcionalidades que o [Sensor de Temperatura](#sensor-de-temperatura), logo mais opções de controle via interface, assim como via terminal estão disponíveis. Dentre as disponíveis estão controle do canal selecionado no momento, o aplicativo que está rodando na televisão, assim como o volume atual da televisão. Por consequência o pacote de dados enviado contém mais informações no campo "data". Dentre as informações:
  - Canal:
    - informa sobre o canal da televisão que está selecionado no momento. Sendo disponibilizados 5 canais.
  - Aplicativo:
    - informa sobre qual aplicativo está sendo executado no momento na televisão. Existem 4 possíveis: "Amazon Prime", "Netflix", "Youtube", "Live Tv"
  - Volume:
    - informa sobre o volume atual que está configurado na televisão. Este que tem o intervalo de 0 a 100.


  ### Interface

  A interface é o componente visual do projeto. Com o funcionamento utilizando protocolo de comunicação HTTP, foi desenvolvida uma interface gráfica para facilitar controle das funções dos dispositivos, além da visualização dos dispositivos conectados. Para o desenvolvimento utilizou-se do framework [React JS](https://react.dev/), visando dinamismo na apresentação dos elementos na tela.

  Uma estrutura foi desenvolvida para poder abarcar diferentes situações em que poderiam acontecer tanto em relação ao servidor, como em relação aos dispositivos conectados. Um [componente](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/interface/Iot-system/src/AppGetData.jsx) foi criado com o intuito de ser "pai" dos outros subsequentes. Isso decorre deste ser responsável por [requisitar dados para o servidor](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/interface/Iot-system/src/AppGetData.jsx#L11), e repassar estes para os componentes filhos.

  Diante disso, as telas apresentam uma tela geral que serve de background para os outros componentes. É nesse background em que é apresentado a [informação sobre a conexão com o servidor](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/interface/Iot-system/src/Cards/CardBackground.jsx#L110), se conectado ou desconectado. Além disso, apresenta [boas vindas para o usuário](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/interface/Iot-system/src/Cards/CardBackground.jsx#L95), e a data e hora atual. Caso o servidor esteja desconectado, nenhum outro componente é renderizado na tela, contudo com o servidor conectado outras 2 vertentes surgem a depender se há dispositivos conectados ao servidor. Considerando o primeiro caso, um componente é renderizado informando que não há dispositivos conectados, e assim que houver eles irão aparecer. Todavia no segundo caso, de haver dispositivos conectados é apresentado então os componentes para lidar com isso.

  A tela com dispositivos conectados, é a principal, tendo em vista que apresenta a lista de dispositivos conectados, as informações atualizadas que os dispositivos enviam, além de na lateral direita apresentar, quando selecionado um dispositivo, opções de controle. Caso não tenha dispositivos selecionados é apresentado o texto na tela para que selecione um dispositivo para poder realizar o controle.


  ### Comunicação
  Um dos pontos principais do projeto é a comunicação entre os módulos utilizando diferentes protocolos. Seguindo um dos requisitos do projeto, a interface realiza comunicações via HTTP por meio de uma API Restful, e os dispositivos utilizam uma abordagem com protocolos TCP e UDP. Tendo em vista que a interface apresenta as informações dos dispositivos, além de controlá-los, logo a comunicação entre eles é necessária. A fim de permitir essa ocorrência, é necessário o uso de um servidor broker, para receber as informações e fazer os devidos encaminhamentos quando necessário, utilizando o protocolo adequado de comunicação. Dessa forma o servidor atende tanto a protocolos HTTP, como TCP e UDP. O fluxo com o protocolo de cada mensagem, adjunto seu remetente e destinatario pode ser vista na Figura 1.

  <p align="center">
    <img width="" src="https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/assets/diagrama_comunicacao.png" />
    Fig 1. Fluxo dos protocolos das mensagens
  </p>

  #### Comunicação Servidor-Interface

  A comunicação HTTP realizada pela interface para com o [servidor](#servidor-broker) ocorre seguindo os padrões da API Restful. Na implementação foi utilizado o framework "Flask" para auxiliar nessa questão. Para poder atender a esse padrão foram criadas algumas rotas de conexão para poder organizar melhor a troca de informações. Tais rotas podem ser apresentadas na Tabela de rotas.

  <div align="center">

  #### Rotas da API REST

  | Comandos | Metodo | Retorno                   | Dado enviado                         |
  | :------- |:----------|:-------------------|:--------------------------|
  | "IP:8082/devices" | GET | Retorna uma lista de objetos contendo as informações de cada dispositivo. Caso não tenha dispositivos é retornado uma lista vazia| None|
  | "IP:8082/devices" | PATCH | Realiza a troca de nome do dispositivo indicado| {"name": "novo nome", "address": "IP do dispositivo a ser alterado"}|
  | "IP:8082/devices/control" | PATCH | Envia os comandos básicos de controle do dispositivo, seja para ligar/stand-by, ou reiniciar| {"comand": "código do comando", "address": "IP do dispositivo a ser alterado"}|
  | "IP:8082/devices/delete" | DELETE | Envia o comando para o dispositivo realizar o desligamento, essa operação que já gera a retirada dele dos dados no servidor| {"comand": "108", "address": "IP do dispositivo a ser alterado"}|
  | "IP:8082/devices/tv/control/app" | PATCH | Envia comandos específicos para o dispositivo [Smart TV](#smart-tv)| {"comand": "código do comando", "address": "IP do dispositivo a ser alterado", "app": "informação de volume, canal ou aplicativo"}|


  </div>
  Com o recebimento dessas requisições, é verificado dentro da lista, se o dispositivo está presente, e em caso positivo, é enviada a requisição utilizando o objeto de conexão adquirido quando o dispositivo se conecta. Em caso contrário é retornado que o dispositivo não existe.

  Vale ressaltar que essa comunicação funciona com a interface realizando as requisições e recebendo as respostas. O servidor não envia dados para a interface caso não tenha sido requisitado. 


  #### Comunicação Servidor-Dispositivo
  A comunicação entre o servidor ocorreu conforme requisito do projeto, utilizando os protocolos TCP e UDP. Isso decorre por conta dos dispositivos simulados virtualmente não possuírem compatibilidade com comunicação HTTP.

  Visando possibilitar essa comunicação entre esses 2 módulos, foi necessário o uso de sockets em ambos os módulos, contudo com abordagens diferentes. No que diz respeito ao servidor, houve a necessidade de criar um socket em que no endereço IP e na porta especificada fica ouvindo por novas conexões, e aceitando-as. Já relativo aos dispositivos, é criado um socket para se conectar com o servidor nos endereços especificados. Sendo assim, o servidor tem a capacidade de se conectar com vários sockets de clientes, que são os dispositivos.

  Uma vez que o servidor consegue aceitar conexões de vários dispositivos, ele necessita salvar os sockets de conexão criados, para comunicações futuras. Para isso, um *HashMap* é mantido, no qual a chave é o endereço IP do dispositivo conectado, e como valor há uma lista com o socket de conexão, e o horário em que ela ocorreu. Este último é sempre atualizado quando recebe nova mensagem do dispositivo. No dispositivo, ao conseguir estabelecer a conexão, o socket criado é mantido numa variável utilizada durante a execução para receber informações, o socket TCP, e para enviar com o socket UDP. Caso o dispositivo não consiga estabelecer uma conexão naquele momento, ele permanece em loop realizando novas tentativas.

  Estabelecida conexão entre servidor e dispositivo, duas abordagens acontecem: uma abordagem confiável, e outra abordagem não confiável. Para a abordagem confiável foi escolhido utilizar um socket de comunicação TCP, por conta que este só troca mensagens após firmada conexão. Em contrapartida, na abordagem não confiável foi utilizado socket UDP, este envia dados independente de estar conectado ou não, fazendo apenas o envio.

  Com base nisso, o servidor por ser o responsável de enviar comandos para o dispositivos, realiza o envio dessas mensagens via TCP. Escolha decorrente a importância desses dados de gerenciamento do dispositivo. Contudo, por o dispositivo enviar dados sobre seu estado constantemente, e esses dados serem de menor importância, utilizou-se UDP para envio das mensagens. Esta, caso ocorra, a perda de uma por algum erro não irá gerar grandes problemas, apenas um dado desatualizado no servidor, que logo será atualizado com a próxima mensagem.


## Testes

A realização de testes ocorreram e mediaram o desenvolvimento em todas as etapas, essenciais para saber se a etapa estava concluída, e em caso afirmativo progredir para a próxima. Dentre os primeiros testes, envolveu a troca de mensagens usando sockets TCP e UDP entre o dispositivo e o servidor. Visando entender na prática o funcionamento, e posterior desenvolvimento de algoritmos para estes módulos. 

Por conseguinte, houve o teste de funcionamento das threads no algoritmo. Estas essenciais para permitir operações diversas tanto no servidor como dispositivo operarem em segundo plano. A exemplo o recebimento de novas mensagens, assim como o envio delas. Essas operações podem acontecer sem alterar o fluxo normal apresentado para o usuário. Contudo houve um problema nessa abordagem, a falta da possibilidade de capturar o retorno de uma função, algo que foi resolvido utilizando variáveis globais.

A fim de simular a chegada de um comando da interface cliente, e o envio deste para o dispositivo, visualizando a ação tomada pelo dispositivo diante do comando foi utilizado uma entrada para o usuário no servidor. Essa ação permite escolher qual comando enviar, baseado nos comandos da Tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos), e qual ação do dispositivo ao enviar um comando não válido. Este que por sua vez simplesmente ignora ele.

Com o avanço do projeto, e a criação da API RESTful, foi necessário verificar o funcionamento das rotas e o uso dos argumentos. Previamente, foi feito o uso do software *Insomnia* para realizar essa comunicação. Esta aplicação permite enviar comandos e realizar requisições para a API presente no servidor. [Um arquivo com os testes](https://github.com/rhianpablo11/IoT-Tec502-PBL/blob/main/testesAPI.json) esta disponivel no respositorio para realizar importação na aplicação e testar a API sem utilizar a interface. Realizando apenas alterações nos endereços IP da API e do dispositivo que deseja alterar.

Os testes com relação a interface foram mais genéricos, diante que ocorreram sobre o envio de requisições e o recebimento, além de apresentação correta dos itens na tela. Contudo, após verificado o funcionamento, os testes de confiabilidade do sistema ocorreram com o uso dela, por conta da melhor visibilidade do tráfego de mensagens. E além de já ter sido validada a amostragem desses dados.

Tratando de confiabilidade, uma série de testes ocorreram com o objetivo de simular falhas no sistema, e como os 3 módulos agem diante disso. Dessa forma, testou-se a perda de conexão, ao retirar cada máquina, que rodava um dos módulos, da rede, outro teste simulou o fechamento/desligamento abrupto dos módulos, ao parar determinado módulo. Esses testes permitiram tratar o sistema contra essas falhas, permitindo um uso mais confiável para o usuário. Com isso, ao retirar a interface da rede, ela perde conexão com o servidor e para de apresentar dados, no caso de retirar o dispositivo, o servidor verifica o tempo de inatividade e se maior que 10 segundos retira da lista de dispositivos salvos, e em último caso retirar uma falha no servidor, tanto a interface como o dispositivo param e novas tentativas de reconexão começam a acontecer. Contudo nestes testes de confiabilidade, um problema foi detectado na verificação de inatividade do dispositivo pelo servidor, em que a thread responsável por isso ocorre um erro na execução e ela é terminada.


## Conclusão

Tendo como base o que foi apresentado, e obtido como produto final, observa-se que o projeto foi concluído com sucesso, atingindo os requisitos definidos no início do projeto, bem como com os objetivos. Dessa forma foi possível comunicar 2 módulos, a interface e os dispositivos, mesmo estes utilizados modos de comunicação diferentes e incompatíveis entre si, utilizando para isso um servidor broker. 

Entretanto melhorias no projeto ainda podem ser desenvolvidas, e implementadas, como a criptografia de mensagens trocadas com o servidor, tanto por parte do dispositivo, como por parte da interface. Esta última ainda há outros métodos adicionais de segurança para ter acesso a informação, como o uso de *token de acesso* nas requisições. Ainda sobre a interface, o uso de criação de usuário, com o objetivo de tornar a experiência para o usuário mais especial.*


## Referencias
> - [1] Python Software Foundation. Python Documentation. Biblioteca Socket. Versão 3.12. Disponível em: https://docs.python.org/3/library/socket.html. Acesso em: 06 abril 2024.
> - [2] Flask . Flask Documentation. Versão 3.0. Disponível em: https://flask.palletsprojects.com/en/3.0.x/#. Acesso em: 20 abril 2024.
> - [3] Code, Bro. "React Full Course for free ⚛️ (2024)". Bro Code. Publicado em: 16 de jan. de 2024. Disponível em: https://youtu.be/CgkZ7MvWUAA?si=9-qf7T9tSUz1W9N7. Acesso em: 17 de abril de 2024.
> - [4] Teddesco, Kennedy. "Uma introdução a TCP, UDP e Sockets". Treina Web. Publicado em: jun. de 2020. Disponível em: https://www.treinaweb.com.br/blog/uma-introducao-a-tcp-udp-e-sockets#:~:text=O%20que%20%C3%A9%20um%20Socket,0.1%3A4477%20(IPv4). Acesso em: 06 de abril de 2024.
> - [5] Redhat. "O que é um broker de serviços?". Publicado em: 07 de fev. de 2022. Disponível em: https://www.redhat.com/pt-br/topics/cloud-native-apps/service-brokers. Acesso em: 07 de abril de 2024.


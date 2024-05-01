# IoT-Tec502-PBL

## Como executar
A primeira etapa diz respeito a clonar o repositorio para o seu dispositivo, o que pode ser feito usando o comando no terminal:

``
git clone https://github.com/rhianpablo11/IoT-Tec502-PBL.git
``

## Estrutura do projeto
A estrutura utilizada na construção do projeto se divide em 3 elementos:
  
- ` Interface:` Responsavel por apresentar os dados enviados pelos dispositivos, além de oferecer opções de gerenciamento de cada um deles
- `` Servidor Broker:`` Responsavel por receber os dados do dispositivo e enviar para a interface quando requisitado, além de receber os comandos da interface para controle de um dispositivo e enviar o que foi selecionado
- ``` Dispositivo:``` Este simula um dispositivo real, oferecendo funções simuladas via software. Ele realiza o envio constante de dados sobre o seu estado atual
  
## Servidor Broker
    Falar sobre a parte do TCP e a parte do HTTP
    ele tem uso com aquela parada dos comandos
O servidor Broker é a parte central de todo esse projeto, sendo responsavel por estabelecer comunicação com os dispositivos, sensor de temperatura e Smart TV, assim como com a interface. Para tal ação ele necessita uma conexão, TCP e UDP, com cada dispositivo para que possa enviar comandos e receber os dados do dispositivo. O envio e recebimento de dados com a interface ocorre usando o protocolo HTTP, não exigindo o firmamento de uma conexão com o servidor.
Ainda deve-se pontuar o gerenciamento dos dados recebidos, para manter sempre os ultimos dados recebidos salvos, e estruturados. Essa estrutura padrão é um dos pilares que permite o funcionamento em conjunto dos 3 dispositivos. Segue a estrutura padrão utilizada:
- Address: É a chave do dicionario de mensagens. Contém o endereço IP do dispositivo
  - LastData: contém o ultimo dado recebido pelo dispositivo
  - Type: contém o tipo do dispositivo
  - HourLastData: contém o horario em que recebeu o ultimo dado
  - DeviceStatus: contém o estado do dispositivo, se está ligado por exemplo
  - Name: contém o nome do dispositivo 

## Dispositivo
Para realizar a simulação de um dispositivo de IoT, Internet das Coisas, houve a necessidade de criar um programa que realizasse as ações de um.
Os dispotivos haviam uma restrição na sua criação, em que eles só devem ser capazes de realizar comunicação via TCP ou UDP, o que aumentou a necessidade do servidor, já que este faz uma especie de tradução para receber comandos da interface e enviar para o dispositivo.<br>
Com o proposito de padronizar a comunicação para melhor efetividade e escalabilidade, foi decidido usar comandos nas trocas de mensagens. A escolha, permite que sejam enviados um pacote menor de dados pela rede, além de que este simplifica o pedir de ações. Na tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos-comandos-que-funcionam-apenas-na-smarttv) é possível ver os comandos e o que cada um realiza.
<div align="center">
	
| Comandos| Ações dentro do dispositivo|
:----------| :-------------|
| 103           | Indica para o dispositivo que o servidor ainda esta ativo na rede. Essa mensagem, ou qualquer um dos outros codigos tem que chegar no intervalo de 10 segundos|
| 104           | Realiza a alteração no nome do dispositivo|
| 105             | Realiza a alteração de estado do dispositivo, <b>ligando-o</b>
| 106 | Realiza a altaração de estado do dispositivo, <b>desligando-o</b>   |
| 107            | Pede ao dispositivo para ele se auto reiniciar, trocando de estado para desligado, e após para ligado|
| 108 | Pede para o dispositivo entrar na rotina de "shutdown", dessa forma ele proprio se auto desliga, e envia um ultimo comando para que o servidor apague ele dos dados salvos |
| 109*            | Indica que uma troca de canal esta sendo requisitada     |
| 110*           | Indica que uma troca de volume atual esta sendo requisitada    |
| 111*           | Indica que uma troca de applicativo esta sendo sendo requisitada    |
#### Possíveis comandos dos dispositivos<p>* comandos que funcionam apenas na SmartTv</p>
</div>
Tais dispositivos precisam estar aptos para realizar operações em segundo plano, como por exemplo escutar o recebimento de novos comandos e realizar a operação desejada. Para que isso fosse possível, o uso de Threads foi essencial, tendo em vista que ao criar um thread para uma funcionalidade, ela opera em paralelo as outras. Nesse projeto, os dispositivos contam com 3 Threads adicionais a Thread principal.

- Thread Principal:
  - Mantém o programa ativo - while true
- Thread "receiverTCP":
  - Fica ouvindo a chega de novos comandos vindos do servidor, por meio de conexão TCP
- Thread "sendDataFullTime":
  - Realiza o envio de dados continuamente para o servidor, por meio de conexão UDP
- Thread "menu":
  - Permite que a função que apresenta no terminal as funções de controle, e recebe a opção a ser operada, escolhida pelo usuario, fique em execução. Isso simula um comando fisico no dispositivo

Os dispositivos, conforme requisito, podem ser controlados via terminal usando linhas de comando. Esta operação simula o uso do dispositivo fisicamente, a exemplo apertar o botão liga e desliga. Sendo assim, há 2 formas de controle: via terminal, simulando o dispositivo fisico, ou pela interface, neste caso o comando trafega pela rede ate chegar ao dispositivo. 

O controle desdes dispositivos pela interface possui 4 funcionalidades genericas, conforme descrito na tabela [Possíveis comandos dos dispositivos](#possíveis-comandos-dos-dispositivos-comandos-que-funcionam-apenas-na-smarttv). Contudo, no caso da [Smart Tv](#smart-tv), por possuir funções especificas de controle, ela possui comandos a mais, além de junto com esses comandos receber um argumento descrevendo melhor a operação a ser realizada.

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
    falar das telas que tem de controle do dispositivo, e as telas quando nao tem dispositivo, e quando nao tem 

## Comunicação

### Casos de erro
# **SimilaridadeTextos**

Repositório destinado a implementação do cálculo de similaridade entre dois textos, utilizando Similaridade entre Grafos e Similaridade de Cossenos.

## **Configuração:**
Sabendo que o código utiliza de elementos externos, como a ferramenta [SOBEK]() e sendo desevolvido em Python, é necessário fazer a instalação de alguns elementos. Primeiramente devemos instalar as dependências de Java, para execução da ferramenta SOBEK, em que iremos instalar a linguagem Java, e seu exeucutador JDK, usando dos comandos abaixo:

```
sudo apt install default-jre
```
```
sudo apt install default-jdk
```

<br>

Além disso, é necessário que o arquivo executavél da ferramenta tenha permissão para rodar no sistema, de forma que devemos ir até a pasta do arquivo ```SobekCommandLineJava```, e executar o comando:

```
chmod +x SobekCommandLineJava
```

<br>

Olhando agora para os elementos da linguagem Python 3, e para sua formação foi necessário a presença de diversas bibliotecas, em que foi criado um arquivo, ```requirements.txt``` que irá instalar todas as dependências necessárias, bastando apenas ter instalado o [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/), após isso, basta executar o comando:

```
pip3 install -r requirements.txt
```

<br>

Além disso, a biblioteca [NLTK](https://www.nltk.org/) necessita de instalar externamente alguns itens, bastando executar o arquivo ```nltkmodule.py``` como mostrado abaixo.

```
python3 nltkmodules.py
```

## **Como Executar**

Para executar, primeiro é necessário navegar até o arquivo main do programa a partir do diretório onde clonou o repositório.

```
cd Similaridade/SobekCommandLineJava-1.5/bin/main.py
```

Após isso, no terminal digite o seguinte comando para executar a aplicação:

```
python3 main.py "Texto1.txt,Texto2.txt"
```
Sendo "Texto1.txt" e "Texto2.txt" o nome dos arquivos de texto a serem comparados, e eles precisam estar na pasta localizada em Similaridade/Textos.
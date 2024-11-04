# **SimilaridadeTextos**

Repositório destinado a implementação do cálculo de similaridade entre dois textos, utilizando Similaridade de Cossenos.

## **Configuração:**


Olhando para os elementos da linguagem Python 3, e para sua formação foi necessário a presença de uma biblioteca. Dessa forma, foi criado um arquivo, ```requirements.txt``` que irá instalar todas as dependências necessárias, bastando apenas ter instalado o [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/), após isso, basta executar o comando:

```
pip3 install -r requirements.txt
```

## **Como Executar**

No terminal basta digitar o seguinte comando para executar a aplicação:

```
python3 main.py "Texto1.txt,Texto2.txt"
```
- Sendo "Texto1.txt" e "Texto2.txt" o nome dos arquivos de texto a serem comparados, e eles precisam estar na pasta localizada em Similaridade/Textos.
- Caso a pasta não exista, será necessário criá-la.
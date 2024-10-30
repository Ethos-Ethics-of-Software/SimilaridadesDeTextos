import subprocess
import sys
from xml.dom import minidom
import networkx as nx
import matplotlib.pyplot as plt

# Biblioteca para remover stopwords
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize

# Biblioteca para remover pontuação
import string

from preProcessamento import PreProcessamento

class ControladoraSOBEK:
    # Verificamos se o SOBEK retorna um grafo vazio, se sim, iremos gerar
    # internamente o grafo
    @classmethod
    def gerarGrafo(cls, texto, idioma):
        # Para evitar erros, as pontuações como : e () são retiradas
        texto = texto.translate(str.maketrans('', '', string.punctuation))

        # Além disso, devemos retirar os /n
        texto = texto.replace("\n", " ")

        identificador = 0
        trecho = ''

        for letra in texto:
            if(letra == '`' and identificador == 0):
                trecho += letra
                identificador = 1

            elif(letra == '`' and identificador == 1):
                trecho += letra
                texto = texto.replace(trecho, '')
                trecho = ''
                identificador = 0

            elif(identificador == 1):
                trecho += letra

        comando = "./SobekCommandLineJava -x -t " + texto
        respostaTexto = subprocess.check_output(comando, shell=True).decode("utf-8")
        xml = minidom.parseString(respostaTexto)
        return ControladoraSOBEK.gerarGrafoSOBEK(xml, texto, idioma)

    @classmethod
    def gerarGrafoSOBEK(cls, xml, texto, idioma):
        G = nx.Graph()
        aresta = xml.getElementsByTagName("nodo")

        for staff in aresta:
            # Gerando os dados do XML para passar para o grafo
            palavra = staff.getAttribute("name")
            sid = staff.getElementsByTagName("id")[0]
            ocorrencia = staff.getElementsByTagName("ocorrencia")[0]
            frequencia = staff.getElementsByTagName("frequencia")[0]

            G.add_node(palavra, id=sid.firstChild.data, ocorrencia=ocorrencia.firstChild.data, frequencia=frequencia.firstChild.data)

            # Caso a aresta tenha ligações, é extraido os dados do xml do mesmo
            relacao = staff.getElementsByTagName("relacoes")
            if(relacao):
                for dado in relacao:
                    nome = dado.getAttribute("name")
                    idName = dado.getElementsByTagName("name_ID")[0]
                    conexao = dado.getElementsByTagName("conexoes")[0]

                    G.add_edge(palavra, nome, ocorrencia=conexao.firstChild.data)

        if G.number_of_nodes() == 0:
            return ControladoraSOBEK.gerarGrafoInterno(texto, idioma)
        else:
            return G

    @classmethod
    def gerarGrafoInterno(cls, texto, idioma):
        stop_words = " "

        if(idioma == 'pt'):
            # Escolhe a lista de stop words em português
            stop_words = set(stopwords.words('portuguese'))

        if(idioma == 'en'):
         # Escolhe a lista de stop words em inglês
            stop_words = set(stopwords.words('english'))
        
        palavras = word_tokenize(texto)
        palavras = [palavras.lower() for palavras in palavras]
        palavras_semstopword = [palavra for palavra in palavras if not palavra in stop_words]

        G = nx.Graph()
        pos = 0

        if len(palavras_semstopword) == 1:
            G.add_node(palavras_semstopword[0])

        elif len(palavras_semstopword) == 2:
            G.add_node(palavras_semstopword[0])
            G.add_node(palavras_semstopword[1])
            G.add_edge(palavras_semstopword[0], palavras_semstopword[1])

        elif len(palavras_semstopword) == 3:
            for palavra in palavras_semstopword:
                if pos == 0:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos == 1:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos+1])

                elif pos == 2:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])

                pos += 1

        elif len(palavras_semstopword) == 4:
            for palavra in palavras_semstopword:
                if pos == 0:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos == 1:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos == 2:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])
                    G.add_edge(palavra, palavras_semstopword[pos+1])

                elif pos == 3:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])

        elif len(palavras_semstopword) >= 5:
            for palavra in palavras_semstopword:
                if pos == 0:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos == 1:
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos >= 3 and pos < (len(palavras_semstopword) - 2):
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])
                    G.add_edge(palavra, palavras_semstopword[pos+1])
                    G.add_edge(palavra, palavras_semstopword[pos+2])

                elif pos == (len(palavras_semstopword) - 2):
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])
                    G.add_edge(palavra, palavras_semstopword[pos+1])

                elif pos == (len(palavras_semstopword) - 1):
                    G.add_node(palavra)
                    G.add_edge(palavra, palavras_semstopword[pos-1])
                    G.add_edge(palavra, palavras_semstopword[pos-2])

                pos += 1

        # Número total de Vértices
        totalVertices = G.number_of_nodes()
        nosGrafo = list(G.nodes)

        # Gerando Grafo Real, com Base no Grafo Modelo
        G1 = nx.Graph()
        pos = 0

        if len(palavras_semstopword) == 1:
            G1.add_node(palavras_semstopword[0], ocorrencia=1, frequencia=1)

        elif len(palavras_semstopword) == 2:
            G1.add_node(palavras_semstopword[0], ocorrencia=1, frequencia=1)
            G1.add_node(palavras_semstopword[1], ocorrencia=1, frequencia=1)
            G1.add_edge(palavras_semstopword[0], palavras_semstopword[1], ocorrencia=1)

        elif len(palavras_semstopword) == 3:
            for palavra in palavras_semstopword:
                if pos == 0:
                    G1.add_node(palavra, ocorrencia=1, frequencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos == 1:
                    G1.add_node(palavra, ocorrencia=1, frequencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)

                elif pos == 2:
                    G1.add_node(palavra, ocorrencia=1, frequencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)

                pos += 1

        elif len(palavras_semstopword) == 4:
            for palavra in palavras_semstopword:
                # Fazendo Cálculo da Frequência e Ocorrencia da Palavra
                frequencia = palavras_semstopword.count(palavra)
                vizinhos = PreProcessamento.contarVerticesVizinhos(G, palavra)
                ocorrencia = vizinhos/(totalVertices-1)

                #print("No: "+palavra+" Ocorrência: "+str(ocorrencia)+" Frequência: "+str(frequencia))

                if pos == 0:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos == 1:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos == 2:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)

                elif pos == 3:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)

        elif len(palavras_semstopword) >= 5:
            for palavra in palavras_semstopword:
                # Fazendo Cálculo da Frequência e Ocorrencia da Palavra
                frequencia = palavras_semstopword.count(palavra)
                vizinhos = PreProcessamento.contarVerticesVizinhos(G, palavra)
                ocorrencia = vizinhos/(totalVertices-1)

                #print("No: "+palavra+" Ocorrência: "+str(ocorrencia)+" Frequência: "+str(frequencia))

                if pos == 0:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos == 1:
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos >= 3 and pos < (len(palavras_semstopword) - 2):
                    G1.add_node(palavra,ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+2], ocorrencia=1)

                elif pos == (len(palavras_semstopword) - 2):
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos+1], ocorrencia=1)

                elif pos == (len(palavras_semstopword) - 1):
                    G1.add_node(palavra, ocorrencia=ocorrencia, frequencia=frequencia)
                    G1.add_edge(palavra, palavras_semstopword[pos-1], ocorrencia=1)
                    G1.add_edge(palavra, palavras_semstopword[pos-2], ocorrencia=1)

                pos += 1

        return G1
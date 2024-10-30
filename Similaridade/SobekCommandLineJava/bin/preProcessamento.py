# Biblioteca Usada no Dicionário de Sinônimos em Português
from pysinonimos.sinonimos import Search, historic

# Biblioteca Usada no Dicionário de Sinônimos em Inglês
from nltk.corpus import wordnet

# Biblioteca usada no Dicionário de Sinônimos em Inglês
# e Algoritmo de Stemming em Português e Inglês
import nltk 
from nltk.stem import RSLPStemmer
from nltk.stem import PorterStemmer

# Biblioteca usada para gerar e analisar os grafos
import networkx as nx
import matplotlib.pyplot as plt

class PreProcessamento:
    @classmethod
    def dicionarioSinonimosPortugues(cls, palavra1, palavra2):
        palavra1 = Search(palavra1)
        sinonimos = palavra1.synonyms()

        for i in sinonimos:
            if(i == palavra2):
                return 1

        return 0

    @classmethod
    def dicionarioSinonimosIngles(cls, palavra1, palavra2):
        palavra1 = palavra1 + '.n.1'
        sinonimos = wordnet.synset(palavra1).lemma_names()

        print(sinonimos)

        for i in sinonimos:
            i = i.lower()

            if(i.replace("_", " ") == palavra2):
                return 1

        return 0

    @classmethod
    def tokenize(cls, sentence):
        sentence = sentence.lower()
        sentence = nltk.word_tokenize(sentence)
        return sentence

    @classmethod
    def algoritmoStemming(cls, sentence, idioma):
        stemmer = RSLPStemmer()

        if(idioma == 'pt'):
            stemmer = RSLPStemmer()
        elif(idioma == 'en'):
            stemmer = PorterStemmer()
        frase = []

        for word in sentence:
            frase.append(stemmer.stem(word.lower()))

        return frase

    @classmethod
    def contarVerticesVizinhos(cls, grafo, no):
        contador = 0

        for i in nx.neighbors(grafo, no):
            contador += 1

        return contador

    @classmethod
    def frequenciaGrafo(cls, grafo):
        contador = 0.0
        nosGrafo = list(grafo.nodes)

        for i in nosGrafo:
            try:
                contador += float(grafo.nodes[i]['frequencia'])
            except KeyError:
                contador += 0

        return contador
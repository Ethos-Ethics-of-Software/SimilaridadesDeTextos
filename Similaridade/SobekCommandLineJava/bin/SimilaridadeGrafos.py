# Biblioteca usada para gerar e analisar os grafos
import networkx as nx
import matplotlib.pyplot as plt

from preProcessamento import PreProcessamento

class SimilaridadeGrafos:
    @classmethod
    def simGrafos(cls, grafoTexto1, grafoTexto2, idioma):
        # Variaveis usadas para RC e os demais calculos
        RC = 0
        nosGrafoTexto1 = list(grafoTexto1.nodes)
        nosGrafoTexto2 = list(grafoTexto2.nodes)
        frequenciaGrafoTexto1 = PreProcessamento.frequenciaGrafo(grafoTexto1)

        # Variaveis para calculo de DC
        DC = 0
        listaVerticesTexto1 = []
        listaVerticesTexto2 = []
        dicionarioDistanciaTexto1 = dict(nx.all_pairs_shortest_path_length(grafoTexto1))
        dicionarioDistanciaTexto2 = dict(nx.all_pairs_shortest_path_length(grafoTexto2))
        distanciaGrafoTexto1 = 0
        distanciaGrafoTexto2 = 0

        # Variaveis usadas para o calculo de PC
        PC = 0
        verticesgrafoTexto1 = grafoTexto1.number_of_nodes()
        verticesgrafoTexto2 = grafoTexto2.number_of_nodes()
        somatorioVerticesTexto1 = 0
        somatorioVerticesTexto2 = 0

        # Encontrando valores das variaveis de RC e DC
        for noTexto1 in nosGrafoTexto1:
            for noTexto2 in nosGrafoTexto2:
                if(noTexto1 == noTexto2):
                    try:
                        RC += float(grafoTexto1.nodes[noTexto1]['frequencia']) / frequenciaGrafoTexto1
                    except KeyError:
                        RC += 0
                     
                    listaVerticesTexto1.append(noTexto1)
                    listaVerticesTexto2.append(noTexto2)

                # Dependendo do Idioma usado no Projeto iremos fazer uma chamada diferente
                # para a função de dicionario de sinonimos
                elif('' in noTexto1 == 0 and '' in noTexto2 == 0):
                    if(idioma == 'pt'):
                        if(PreProcessamento.dicionarioSinonimosPortugues(noTexto1, noTexto2) == 1):
                            try:
                                RC += float(grafoTexto1.nodes[noTexto1]['frequencia']) / frequenciaGrafoTexto1
                            except KeyError:
                                RC += 0
                            
                            listaVerticesTexto1.append(noTexto1)
                            listaVerticesTexto2.append(noTexto2)

                    elif(idioma == 'en'):
                        if(PreProcessamento.dicionarioSinonimosIngles(noTexto1, noTexto2) == 1):
                            try:
                                RC += float(grafoTexto1.nodes[noTexto1]['frequencia']) / frequenciaGrafoTexto1
                            except KeyError:
                                RC += 0
                            
                            listaVerticesTexto1.append(noTexto1)
                            listaVerticesTexto2.append(noTexto2)

                else:
                    palavra = PreProcessamento.tokenize(noTexto1)
                    palavra = PreProcessamento.algoritmoStemming(palavra, idioma)

                    palavra1 = PreProcessamento.tokenize(noTexto2)
                    palavra1 = PreProcessamento.algoritmoStemming(palavra1, idioma)

                    if(palavra == palavra1):
                        try:
                            RC += float(grafoTexto1.nodes[noTexto1]['frequencia']) / frequenciaGrafoTexto1
                        except KeyError:
                            RC += 0
                        
                        listaVerticesTexto1.append(noTexto1)
                        listaVerticesTexto2.append(noTexto2)

        # Verificamos se a lista é maior que 1, se sim podemos calcular DC
        if(len(listaVerticesTexto1) > 1):
            # Encontrando o caminho dos nos similares em cada grafo
            for Texto1 in listaVerticesTexto1:
                for Texto1Comparado in listaVerticesTexto1:
                    try:
                        distanciaGrafoTexto1 += int(dicionarioDistanciaTexto1[Texto1][Texto1Comparado])
                    except KeyError:
                        distanciaGrafoTexto1 += 0

            for Texto2 in listaVerticesTexto2:
                for Texto2Comparado in listaVerticesTexto2:
                    try:
                        distanciaGrafoTexto2 += int(dicionarioDistanciaTexto2[Texto2][Texto2Comparado])
                    except KeyError:
                        distanciaGrafoTexto2 += 0

        # Após calculado o valor do somatorio de distancia de cada grafo
        # calculamos, e verificamos se esta dentro do modulo
        DC = distanciaGrafoTexto2 - distanciaGrafoTexto1

        if(DC < 0):
            DC = DC * -1

        DC = 1/(1 + DC)

        # Fazendo os calculos de vertices vizinhos para o calculo de PC
        for Texto1 in listaVerticesTexto1:
            somatorioVerticesTexto1 += PreProcessamento.contarVerticesVizinhos(grafoTexto1, Texto1)/verticesgrafoTexto1

        for Texto2 in listaVerticesTexto2:
            somatorioVerticesTexto2 += PreProcessamento.contarVerticesVizinhos(grafoTexto2, Texto2)/verticesgrafoTexto2

        # Após calculado o valor do somatorio de distancia de cada grafo
        # calculamos, e verificamos se esta dentro do modulo
        PC = somatorioVerticesTexto2 - somatorioVerticesTexto1

        if(PC < 0):
            PC = PC * -1

        PC = 1/(1 + PC)

        return ((RC + DC + PC)/3)
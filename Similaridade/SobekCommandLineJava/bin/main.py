from sys import argv
from ControladoraSimilaridade import ControladoraSimilaridade
import networkx as nx
import matplotlib.pyplot as plt



path = argv[1].split(',')
path[0] = "../../Textos/" + path[0]
path[1] = "../../Textos/" + path[1]

with open(path[0], 'r') as arquivo:
    arquivo1 = arquivo.read()

with open(path[1], 'r') as arquivo:
    arquivo2 = arquivo.read()

print("------------------------------------------------------------")
print("1 - Cálculo de Similaridade de Cossenos")
print("2 - Cálculo de Similaridade por Grafos")
tipoCalculo = int(input("Digite o Tipo de Cálculo: "))
print("------------------------------------------------------------")

nivelSimilaridade = ControladoraSimilaridade.calcularSimilaridade(arquivo1, arquivo2, tipoCalculo)
print(nivelSimilaridade)
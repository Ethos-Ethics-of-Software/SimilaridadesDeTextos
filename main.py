from sys import argv
from Similaridade.src.ControladoraSimilaridade import ControladoraSimilaridade



path = argv[1].split(',')
path[0] = "Similaridade/Textos/" + path[0]
path[1] = "Similaridade/Textos/" + path[1]

with open(path[0], 'r') as arquivo:
    arquivo1 = arquivo.read()

with open(path[1], 'r') as arquivo:
    arquivo2 = arquivo.read()


nivelSimilaridade = ControladoraSimilaridade.calcularSimilaridade(arquivo1, arquivo2)
print("Cálculo de Similaridade de Cossenos: " + str(nivelSimilaridade))
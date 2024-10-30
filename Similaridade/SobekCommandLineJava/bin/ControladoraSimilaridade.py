from SimilaridadeCossenos import SimilaridadeCossenos
from SimilaridadeGrafos import SimilaridadeGrafos
from controladoraSOBEK import ControladoraSOBEK
import networkx as nx
import matplotlib.pyplot as plt

class ControladoraSimilaridade:
    
    @classmethod
    def calcularSimilaridade(cls, texto1, texto2, tipoCalculo):
        
        if (tipoCalculo == 1):
            similaridade = SimilaridadeCossenos.simCossenos(texto1, texto2)
        
        if (tipoCalculo == 2):
            print("------------------------------------------------------------")
            print("Português - pt")
            print("Inglês - en")
            idioma = input("Digite o idioma do texto: ")
            if (idioma != "pt" and idioma != "en"):
                print("Idioma Inválido!")
                return
            print("------------------------------------------------------------\n")
            
            texto1 = ControladoraSOBEK.gerarGrafo(texto1, idioma)
            texto2 = ControladoraSOBEK.gerarGrafo(texto2, idioma)
            print("------------------------------------------------------------")
            print("Deseja visualizar os grafos dos textos? \n0 - Não \n1 - Sim")
            exebirGrafos = int(input("Digite sua Resposta: "))
            print("------------------------------------------------------------\n")
            
            if(exebirGrafos == 1):
                nx.draw(texto1, with_labels=True, font_weight='bold')
                plt.show()
                nx.draw(texto2, with_labels=True, font_weight='bold')
                plt.show()
            
            similaridade = SimilaridadeGrafos.simGrafos(texto1, texto2, idioma)
        
        return similaridade
        
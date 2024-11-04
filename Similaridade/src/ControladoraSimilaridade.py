from Similaridade.src.SimilaridadeCossenos import SimilaridadeCossenos

class ControladoraSimilaridade:
    
    @classmethod
    def calcularSimilaridade(cls, texto1, texto2):
        
        similaridade = SimilaridadeCossenos.simCossenos(texto1, texto2)
        return similaridade
        
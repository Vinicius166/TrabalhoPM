from .persistencia.banco import BancoDeDados
from .visao.cli import CLI
from .modelo.models import Destino

def main():
    banco = BancoDeDados()
    cli = CLI(banco)
    
    destinos_iniciais = [
        Destino(1, "Itacaré", "Barracuda Boutique", 185.00),
        Destino(2, "Salvador", "Fera Palace Hotel", 150.00),
        Destino(3, "Porto Seguro", "La Torre Resort", 130.00),
        Destino(4, "Arraial d'Ajuda", "Pousada Maria Pitanga", 110.00),
        Destino(5, "Maraú", "Brisa da Barra Suítes", 175.00),
        Destino(6, "Valença", "Hotel Galeão", 95.00)
]
    
    for d in destinos_iniciais:
        banco.destinos.inserir(d)
    
    print("Inicializando sistema de viagens...")
    cli.menu_principal()

if __name__ == "__main__":
    main()

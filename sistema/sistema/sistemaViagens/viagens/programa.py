from .persistencia.banco import BancoDeDados
from .visao.cli import GUI
from .modelo.models import Destino, Cliente

def main():
    banco = BancoDeDados()
    
    
    destinos_iniciais = [
        Destino(1, "Itacaré", "Barracuda Boutique", 185.00),
        Destino(25244, "Salvador", "Fera Palace Hotel", 150.00),
        Destino(39782, "Porto Seguro", "La Torre Resort", 130.00),
        Destino(45497, "Arraial d'Ajuda", "Pousada Maria Pitanga", 110.00),
        Destino(55484, "Maraú", "Brisa da Barra Suítes", 175.00),
        Destino(65484, "Valença", "Hotel Galeão", 95.00)
    ]
   
    for d in destinos_iniciais:
        banco.destinos.inserir(d)
    #teste abaixo
    cliente_inicial = [
        Cliente(10, 'Vinicius', 'vinicius@email.com'),
        Cliente(11, 'Matheus', 'matheus@email.com')
    ]

    for d in cliente_inicial:
        banco.clientes.inserir(d)
    #test acima

    gui = GUI(banco)
    print("Inicializando sistema de viagens...")
    gui._menu_principal()

if __name__ == "__main__":
    main()

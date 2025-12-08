from .persistencia.banco import BancoDeDados
from .visao.cli import GUI
from .modelo.models import Destino, Cliente

def main():
    banco = BancoDeDados()
    
    
    destinos_iniciais = [
        Destino(00000, "Itacaré", "Barracuda Boutique", 185.00),
        Destino(11111, "Salvador", "Fera Palace Hotel", 150.00),
        Destino(22222, "Porto Seguro", "La Torre Resort", 130.00),
        Destino(33333, "Arraial d'Ajuda", "Pousada Maria Pitanga", 110.00),
        Destino(44444, "Maraú", "Brisa da Barra Suítes", 175.00),
        Destino(55555, "Valença", "Hotel Galeão", 95.00)
    ]
   
    for d in destinos_iniciais:
        banco.destinos.inserir(d)
    #teste abaixo
    cliente_inicial = [
        Cliente(1, 'Vinicius', 'vinicius@email.com'),
        Cliente(2, 'Matheus', 'matheus@email.com')
    ]

    for d in cliente_inicial:
        banco.clientes.inserir(d)
    #test acima

    gui = GUI(banco)
    print("Inicializando sistema de viagens...")
    gui._menu_principal()

if __name__ == "__main__":
    main()

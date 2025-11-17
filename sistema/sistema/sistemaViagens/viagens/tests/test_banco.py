import unittest
from viagens.persistencia.banco import Persistente, NaoEncontrada
from viagens.modelo.models import Cliente

class TestBanco(unittest.TestCase):

    def setUp(self):   # criando os dados pros testes
        self.p = Persistente[Cliente]()
        self.c1 = Cliente(1, "Vinicius", "vini@gmail.com")
        self.c2 = Cliente(2, "Maria Eduarda", "maria@gmail.com")
    
    def test_inserir(self):   # testes de inserção e de inserção repetida
        self.p.inserir(self.c1)
        self.assertEqual(len(self.p.listar_todos()), 1)
        self.assertEqual(self.p.buscar_por_id(1), self.c1)

    def test_id_repetido(self):
        self.p.inserir(self.c1)
        with self.assertRaises(ValueError):
            self.p.inserir(self.c1)

    def test_alterar(self):   # testes de alteração seja ele um id inexistente ou não
        self.p.inserir(self.c1)
        cliente_modificado = Cliente(1, "Matheus", "matheus@gmail.com")
        self.p.alterar(cliente_modificado)

        resultado = self.p.buscar_por_id(1)
        self.assertEqual(resultado.nome, "Matheus")
        self.assertEqual(resultado.email, "matheus@gmail.com")

    def test_alterar_id_inexistente(self): 
        with self.assertRaises(NaoEncontrada):
            self.p.alterar(self.c1)

    def test_excluir(self):   # testes de exclusão seja ele um id inexistente ou não
        self.p.inserir(self.c1)
        self.p.excluir(1)
        self.assertEqual(len(self.p.listar_todos()), 0)

    def test_excluir_id_inexistente(self): 
        with self.assertRaises(NaoEncontrada):
            self.p.excluir(123)

    def test_busca(self):   # testes de busca seja ele um id inexistente ou não
        self.p.inserir(self.c1)
        self.assertEqual(self.p.buscar_por_id(1), self.c1)

    def test_busca_id_inexistente(self):
        with self.assertRaises(NaoEncontrada):
            self.p.buscar_por_id(999)
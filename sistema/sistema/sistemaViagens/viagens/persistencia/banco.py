from typing import List
from ...viagens.modelo.models import Entidade, Cliente, Destino, Reserva

class Persistente:
    def __init__(self):
        self._lista: List[Entidade] = []

    def inserir(self, obj: Entidade) -> None:
        if any(o.id == obj.id for o in self._lista):
            raise ValueError(f"Objeto com id {obj.id} já existe")
        self._lista.append(obj)

    def alterar(self, obj: Entidade) -> None:
        for i, o in enumerate(self._lista):
            if o.id == obj.id:
                self._lista[i] = obj
                return
        raise ValueError(f"Objeto com id {obj.id} não encontrado")

    def excluir(self, id: int) -> None:
        for i, o in enumerate(self._lista):
            if o.id == id:
                del self._lista[i]
                return
        raise ValueError(f"Objeto com id {id} não encontrado")

    def buscar_por_id(self, id: int):
        for o in self._lista:
            if o.id == id:
                return o
        return None

    def listar_todos(self) -> List[Entidade]:
        return list(self._lista)

    def __str__(self) -> str:
        return "\n".join(str(o) for o in self._lista)

class BancoDeDados:
    def __init__(self):
        self.clientes = Persistente()
        self.destinos = Persistente()
        self.reservas = Persistente()
        
    def __str__(self) -> str:
        parts = []
        parts.append("=== CLIENTES ===")
        parts.append(str(self.clientes))
        parts.append("=== DESTINOS ===")
        parts.append(str(self.destinos))
        parts.append("=== RESERVAS ===")
        parts.append(str(self.reservas))
        return "\n".join(parts)
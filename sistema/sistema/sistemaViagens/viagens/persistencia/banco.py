from typing import List, TypeVar, Generic
from ..modelo.models import Entidade, Cliente, Destino, Reserva

T = TypeVar('T', bound=Entidade)

class NaoEncontrada(Exception):
    def __init__(self, id: int):
        super().__init__(f"Entidade com id {id} não encontrada.")
        self.id = id


class Persistente(Generic[T]):
    def __init__(self) -> None:
        self._lista: List[T] = []

    def inserir(self, obj: T) -> None:
        if any(o.id == obj.id for o in self._lista):
            raise ValueError(f"Objeto com id {obj.id} já existe.")
        self._lista.append(obj)

    def alterar(self, obj: T) -> None:
        for i, o in enumerate(self._lista):
            if o.id == obj.id:
                self._lista[i] = obj
                return
        raise NaoEncontrada(obj.id)

    def excluir(self, id: int) -> None:
        for i, o in enumerate(self._lista):
            if o.id == id:
                del self._lista[i]
                return
        raise NaoEncontrada(id)

    def buscar_por_id(self, id: int) -> T:
        for o in self._lista:
            if o.id == id:
                return o
        raise NaoEncontrada(id)

    def listar_todos(self) -> List[T]:
        return list(self._lista)

    def __str__(self) -> str:
        return "\n".join(str(o) for o in self._lista)


class BancoDeDados:
    def __init__(self):
        self.clientes = Persistente[Cliente]()
        self.destinos = Persistente[Destino]()
        self.reservas = Persistente[Reserva]()

    def __str__(self) -> str:
        parts = []
        parts.append("=== CLIENTES ===")
        parts.append(str(self.clientes))
        parts.append("=== DESTINOS ===")
        parts.append(str(self.destinos))
        parts.append("=== RESERVAS ===")
        parts.append(str(self.reservas))
        return "\n".join(parts)

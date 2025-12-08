from abc import ABC
from typing import List

class Entidade(ABC):
    def __init__(self, id: int):
        self._id = int(id)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, novo_id: int) -> None:
        self._id = int(novo_id)

    def __str__(self) -> str:
        return f"Id = '{self.id}'"

class Cliente(Entidade):
    def __init__(self, id: int, nome: str, email: str):
        super().__init__(id)
        self.nome = nome
        self.email = email

    def __str__(self) -> str:
        return f"Cliente({super().__str__()}, Nome = '{self.nome}', Email = '{self.email}')"

class Destino(Entidade):
    def __init__(self, id: int, cidade: str, hotel: str, valor_diaria: float):
        super().__init__(id)
        self.cidade = cidade
        self.hotel = hotel
        self.valor_diaria = float(valor_diaria)

    def __str__(self) -> str:
       return f"Destino ({super().__str__()}, Cidade = '{self.cidade}', Hotel = '{self.hotel}', Valor da diaria = '{self.valor_diaria:.2f}')"

class ItemReserva:
    def __init__(self, destino: Destino, dias: int):
        if dias <= 0:
            raise ValueError('dias deve ser > 0')
        self.destino = destino
        self.dias = int(dias)

    def custo(self) -> float:
        return self.destino.valor_diaria * self.dias

    def __str__(self) -> str:
        return f"\n    Id do destino = {self.destino.id}, Cidade = '{self.destino.cidade}', Dias = '{self.dias}', Custo = '{self.custo():.2f}')"

class Reserva(Entidade):
    def __init__(self, id: int, cliente: Cliente, metodo_pagamento: int = 2):
        super().__init__(id)
        self.cliente = cliente
        self.itens: List[ItemReserva] = []
        self.metodo_pagamento = int(metodo_pagamento) 

    def adicionar_item(self, item: ItemReserva) -> None:
        if not isinstance(item, ItemReserva):
            raise TypeError('item deve ser ItemReserva')
        self.itens.append(item)

    def remover_item(self, index: int) -> None:
        if index < 0 or index >= len(self.itens):
            raise IndexError('índice de item inválido')
        del self.itens[index]

    def custo_bruto(self) -> float:
        return sum(i.custo() for i in self.itens)

    def custo_total(self) -> float:
        bruto = self.custo_bruto()
        if self.metodo_pagamento == 1:
            return bruto * 0.98
        elif self.metodo_pagamento == 2:
            return bruto
        elif self.metodo_pagamento == 3:
            return bruto * 1.03
        else:
            raise ValueError('Método de pagamento inválido')

    def __str__(self) -> str:
        itens = '; '.join(str(i) for i in self.itens)
        return f"Reserva ({super().__str__()}, Cliente = '{self.cliente.nome}',Itens:{itens},\nTotal (Com ajustes) = '{self.custo_total():.2f}')"

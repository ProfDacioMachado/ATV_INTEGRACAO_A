"""Módulo mínimo para demonstrar operações CRUD em memória.

Fornece uma classe InMemoryStore com métodos create, read, delete.
Projetado para ser pequena e testável com pytest.
"""

from typing import Dict, Any, Optional


class InMemoryStore:
    """Armazenamento simples em memória indexado por int id."""

    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id = 1

    def create(self, payload: Dict[str, Any]) -> int:
        """Cria um novo registro e retorna seu id."""
        _id = self._next_id
        self._next_id += 1
        # store a shallow copy to avoid accidental external mutation
        self._data[_id] = dict(payload)
        return _id

    def read(self, _id: int) -> Optional[Dict[str, Any]]:
        """Retorna o registro por id ou None se não existir."""
        item = self._data.get(_id)
        return dict(item) if item is not None else None

    def delete(self, _id: int) -> bool:
        """Remove o registro por id. Retorna True se removido, False se não existir."""
        if _id in self._data:
            del self._data[_id]
            return True
        return False


__all__ = ["InMemoryStore"]

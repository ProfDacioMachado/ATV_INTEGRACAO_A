import pytest
from datetime import datetime
from typing import Optional
import sys
import os

# Adicionando o path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from View_and_Interface import view
from Controller import usuario as uc
from Model import Usuario as u

lista_usuarios = [
    u.Usuario(
        id=1,
        nome="Joao",
        matricula="ESOFT01-C",
        tipo="ALUNO",
        email="joao@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=2,
        nome="Ana",
        matricula="ESOFT01-A",
        tipo="ALUNO",
        email="ana@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
    u.Usuario(
        id=3,
        nome="Jose",
        matricula="ESOFT01-B",
        tipo="ALUNO",
        email="jose@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="SUSPENSO",
    ),
    u.Usuario(
        id=4,
        nome="Maria",
        matricula="ESOFT01-B",
        tipo="ALUNO",
        email="maria@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=5,
        nome="Carlos",
        matricula="PROF01",
        tipo="PROFESSOR",
        email="carlos@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=6,
        nome="Beatriz",
        matricula="PROF02",
        tipo="PROFESSOR",
        email="beatriz@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=7,
        nome="Fernando",
        matricula="PROF03",
        tipo="PROFESSOR",
        email="fernando@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
    u.Usuario(
        id=8,
        nome="Lucia",
        matricula="PROF04",
        tipo="PROFESSOR",
        email="luciana@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=9,
        nome="Paulo",
        matricula="FUNC01",
        tipo="FUNCIONARIO",
        email="paulo@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=10,
        nome="Sofia",
        matricula="FUNC01",
        tipo="FUNCIONARIO",
        email="sofia@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
]

userController = uc.UsuarioController(usuarios = lista_usuarios.copy())

@pytest.mark.parametrize("tipo_busca, expected_count", [
    ("ALUNO", 4),
    ("PROFESSOR", 4),
    ("FUNCIONARIO", 2),
])
def test_obter_por_tipo(tipo_busca, expected_count):
    result = userController.buscar_por_tipo(tipo_busca)
    assert isinstance(result, list)
    assert len(result) == expected_count
    for usuario in result:
        assert isinstance(usuario, u.Usuario)
        assert usuario.get_tipo() == tipo_busca

@pytest.mark.parametrize("matricula_busca, expected_count", [
    ("FUNC01", 2),
    ("ESOFT01", 4),
    ("PROF04", 1),
])
def test_obter_por_matricula(matricula_busca, expected_count):
    result = userController.buscar_por_matricula(matricula_busca)
    assert isinstance(result, list)
    assert len(result) == expected_count
    for usuario in result:
        assert isinstance(usuario, u.Usuario)


@pytest.mark.parametrize("usuario_id,expected_nome, expected_status", [
    (1, "Joao", "ATIVO"),
    (2, "Ana", "INATIVO"),
    (3, "Jose", "SUSPENSO"),
])
def test_usuario_por_id(usuario_id, expected_nome, expected_status):
    usuarios = userController.buscar_por_nome(expected_nome)
    assert len(usuarios) == 1

    usuario = usuarios[0]
    assert usuario.get_id() == usuario_id
    assert usuario.get_nome() == expected_nome
    assert usuario.get_status() == expected_status


def test_usuario_nao_encontrado():
    result = userController.buscar_por_nome("NomeInvalido")
    assert len(result) is 0


def test_listar_lista_vazia():
    empty_client = uc.UsuarioController(usuarios=[])
    result = empty_client.listar()
    print("Lista retornada:", result)
    assert isinstance(result, list)
    assert len(result) == 0

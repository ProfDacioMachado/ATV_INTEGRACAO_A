import uuid
import pytest
from datetime import datetime, timezone, timedelta

from View_and_Interface import view
from Controller import usuario as uc
from Model import Usuario as u

usuarioController = uc.UsuarioController()

def make_payload(**overrides):
    base = {
        "id": 1,
        "nome": "Fulano de Tal",
        "matricula": f"M{uuid.uuid4().hex[:8]}",
        "tipo": "ALUNO", 
        "email": f"user.{uuid.uuid4().hex[:8]}@example.com",
        "ativoDeRegistro": "2025-01-15T10:30:00Z",
        "status": "ATIVO"
    }

    base.update(overrides)
    return base

def create_user(dados: dict):
    return usuarioController.criar(dados)


def test_create_user_success():
    payload = make_payload()
    resp = create_user(payload)
    assert resp.get_matricula() == payload["matricula"]
    assert resp.get_tipo() == payload["tipo"]
    assert resp.get_nome() == payload["nome"]
    assert resp.get_email() == payload["email"]
    assert resp.get_status() == payload["status"]


@pytest.mark.parametrize("length,valid", [
    (0, False),    
    (1, True),
    (100, True),
    (101, False),
])
def test_nome_validacao_tamanho(length, valid):
    nome = "A" * length
    payload = make_payload(nome=nome)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_nome() == nome, f"Expected nome {nome} but got {resp.get_nome()}"
        else:
            pytest.fail("Should have raised ValueError for invalid name length")
    except ValueError as e:
        assert not valid, f"Unexpected ValueError for valid name: {str(e)}"
        assert "Nome deve ter entre 1 e 100 caracteres" in str(e)


@pytest.mark.parametrize("matricula,valid", [
    ("1234", False),                 
    ("1" * 5, True),                 
    ("1" * 20, True),                
    ("1" * 21, False),               
])
def test_matricula_validacao_tamanho(matricula, valid):
    payload = make_payload(matricula=matricula)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_matricula() == matricula, f"Expected matricula {matricula} but got {resp.get_matricula()}"
        else:
            pytest.fail("Should have raised ValueError for invalid matricula")
    except ValueError as e:
        assert not valid, f"Unexpected ValueError for valid matricula: {str(e)}"
        assert "Matrícula deve ser alfanumérica com 5 a 20 caracteres" in str(e)


def test_matricula_unico():
    unique = f"M{uuid.uuid4().hex[:8]}"
    p1 = make_payload(matricula=unique)
    p2 = make_payload(matricula=unique)
    r1 = create_user(p1)
    assert r1.get_matricula() == unique, f"Expected matricula {unique} but got {r1.get_matricula()}"
    try:
        r2 = create_user(p2)
        pytest.fail("Should have raised ValueError for duplicate matricula")
    except ValueError as e:
        assert "Matrícula já cadastrada" in str(e)


@pytest.mark.parametrize("tipo,valid", [
    ("ALUNO", True),
    ("PROFESSOR", True),
    ("FUNCIONARIO", True),
    ("STAGIARE", False),
    ("", False),
    (None, False),
])
def test_tipo_enum(tipo, valid):
    payload = make_payload(tipo=tipo)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_tipo() == tipo, f"Expected tipo {tipo} but got {resp.get_tipo()}"
        else:
            pytest.fail("Should have raised ValueError for invalid tipo")
    except ValueError as e:
        if tipo == None:
            assert "Campo obrigatório ausente:" in str(e)
        else:
            assert not valid, f"Unexpected ValueError for valid tipo: {str(e)}"
            assert "Tipo inválido" in str(e)


@pytest.mark.parametrize("email,valid", [
    ("valid.email@example.com", True),
    ("invalid-email", False),
    ("no-at-sign.com", False),
    ("@missing-local.com", False),
])
def test_email_formato_valido(email, valid):
    payload = make_payload(email=email)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_email() == email, f"Expected email {email} but got {resp.get_email()}"
        else:
            pytest.fail("Should have raised ValueError for invalid email")
    except ValueError as e:
        assert not valid, f"Unexpected ValueError for valid email: {str(e)}"
        assert "Email inválido" in str(e)


def test_email_unico():
    email = f"user.testando@example.com"
    p1 = make_payload(email=email)
    p2 = make_payload(email=email)
    r1 = create_user(p1)
    assert r1.get_email() == email, f"Expected email {email} but got {r1.get_email()}"
    try:
        r2 = create_user(p2)
        pytest.fail("Should have raised ValueError for duplicate email")
    except ValueError as e:
        assert "Email já cadastrado" in str(e)


@pytest.mark.parametrize("date_str,valid", [
    ("2025-01-15T10:30:00Z", True),
    ("2020-01-01", True),                 
    ("01-01-2020", False),
    ("2020/01/01", False),
    ("not-a-date", False),
    ("", False),
])
def test_ativoDeRegistro_iso8601_validation(date_str, valid):
    payload = make_payload(ativoDeRegistro=date_str)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_ativoDeRegistro() == date_str, f"Expected ativoDeRegistro {date_str} but got {resp.get_ativoDeRegistro()}"
        else:
            pytest.fail("Should have raised ValueError for invalid date format")
    except ValueError as e:
        assert not valid, f"Unexpected ValueError for valid date: {str(e)}"
        assert "ativoDeRegistro deve estar em formato ISO 8601" in str(e)


@pytest.mark.parametrize("status,valid", [
    ("ATIVO", True),
    ("INATIVO", True),
    ("SUSPENSO", True),
    ("DEMITIDO", False),
    ("", False),
    (None, False),
])
def test_validacao_status_enum(status, valid):
    payload = make_payload(status=status)
    try:
        resp = create_user(payload)
        if valid:
            assert resp.get_status() == status
        else:
            pytest.fail("Should have raised ValueError for invalid for invalid status")
    except ValueError as e:
        if status == None:
            assert "Campo obrigatório ausente:" in str(e)
        else:
            assert not valid, f"Unexpected ValueError for valid status: {str(e)}"
            assert "inválido" in str(e)


@pytest.mark.parametrize("missing_field", [
    "nome", "matricula", "tipo", "email", "ativoDeRegistro", "status"
])
def test_falta_de_campo(missing_field):
    payload = make_payload()
    payload.pop(missing_field, None)
    try:
        resp = create_user(payload)
        pytest.fail("Should have raised ValueError")
    except ValueError as e:
        assert str(e) == f"Campo obrigatório ausente: {missing_field}"
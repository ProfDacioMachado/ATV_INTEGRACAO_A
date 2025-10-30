"""
Testes para o módulo de livros
Autor: Equipe 2 - Catálogo de Livros
Esses testes foram escritos ANTES do código (TDD Red)
"""

import pytest
from livro import Livro, criar_livro, listar_livros, buscar_livro_por_isbn, atualizar_livro, deletar_livro, _limpar_db

@pytest.fixture(autouse=True)
def limpar_base_de_dados_a_cada_teste():
    """
    O 'autouse=True' faz com que ela seja executada automaticamente
    ANTES de cada função de teste deste arquivo.
    Isso garante que um teste não suje o ambiente para o próximo.
    """
    _limpar_db()

def test_criar_livro_com_dados_validos():
    
    titulo = "1984"
    autor = "George Orwell"
    isbn = "978-0451524935"
    
    livro = Livro(titulo=titulo, autor=autor, isbn=isbn)
    
    assert livro.titulo == titulo
    assert livro.autor == autor
    assert livro.isbn == isbn
    assert livro.status == "disponivel"  # status padrão deve ser "disponivel"


def test_criar_livro_sem_titulo_deve_lancar_erro():
    with pytest.raises(ValueError, match="Título é obrigatório"):
        Livro(titulo="", autor="George Orwell", isbn="123")


def test_criar_livro_sem_autor_deve_lancar_erro():
    with pytest.raises(ValueError, match="Autor é obrigatório"):
        Livro(titulo="1984", autor="", isbn="123")


def test_criar_livro_sem_isbn_deve_lancar_erro():
    with pytest.raises(ValueError, match="ISBN é obrigatório"):
        Livro(titulo="1984", autor="George Orwell", isbn="")


def test_alterar_status_livro_para_emprestado():
    livro = Livro(titulo="1984", autor="George Orwell", isbn="123")
    
    livro.emprestar()
    
    assert livro.status == "emprestado"


def test_alterar_status_livro_para_disponivel():
    livro = Livro(titulo="1984", autor="George Orwell", isbn="123")
    livro.emprestar()
    
    livro.devolver()
    
    assert livro.status == "disponivel"



def test_criar_livro_no_sistema():

    livro = criar_livro(titulo="1984", autor="George Orwell", isbn="123")
    
    assert livro is not None
    assert livro.titulo == "1984"
    assert livro.autor == "George Orwell"


def test_listar_todos_livros_sistema_vazio():
    livros = listar_livros()
    
    assert isinstance(livros, list)
    assert len(livros) == 0


def test_listar_todos_livros_com_dados():
    criar_livro("1984", "George Orwell", "123")
    criar_livro("Dune", "Frank Herbert", "456")
    
    livros = listar_livros()
    
    assert len(livros) == 2
    assert livros[0].titulo == "1984"
    assert livros[1].titulo == "Dune"


def test_buscar_livro_por_isbn_existente():
    criar_livro("1984", "George Orwell", "123")
    
    livro = buscar_livro_por_isbn("123")
    
    assert livro is not None
    assert livro.isbn == "123"
    assert livro.titulo == "1984"


def test_buscar_livro_por_isbn_inexistente():

    livro = buscar_livro_por_isbn("999")
    
    assert livro is None


def test_atualizar_livro_existente():

    criar_livro("1984", "George Orwell", "123")
    
    livro_atualizado = atualizar_livro(
        isbn="123",
        novo_titulo="1984 - Edição Especial",
        novo_autor="George Orwell"
    )
    
    assert livro_atualizado.titulo == "1984 - Edição Especial"


def test_deletar_livro_existente():
    criar_livro("1984", "George Orwell", "123")
    
    resultado = deletar_livro("123")
    
    assert resultado is True
    assert buscar_livro_por_isbn("123") is None


def test_deletar_livro_inexistente():
    
    resultado = deletar_livro("999")
    
    assert resultado is False
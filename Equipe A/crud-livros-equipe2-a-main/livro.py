"""
Módulo de gerenciamento de livros - Catálogo da Biblioteca
Equipe 2 - Sistema de Gestão de Biblioteca Universitária (SGBU)

Este módulo fornece funcionalidades completas de CRUD para o catálogo de livros,
incluindo validações, controle de status e persistência em memória.
"""

from typing import List, Optional


# ==================== Constantes ====================

STATUS_DISPONIVEL = "disponivel"
STATUS_EMPRESTADO = "emprestado"


# ==================== Banco de Dados (Memória) ====================

_db_livros: List['Livro'] = []


def _limpar_db() -> None:
    """
    Limpa toda a base de dados de livros.
    
    Nota: Função interna utilizada principalmente para testes.
    """
    _db_livros.clear()


# ==================== Classe Livro ====================

class Livro:
    """
    Representa um livro no catálogo da biblioteca.
    
    Attributes:
        titulo (str): Título do livro
        autor (str): Nome do autor
        isbn (str): Código ISBN do livro
        status (str): Status atual do livro ('disponivel' ou 'emprestado')
    
    Raises:
        ValueError: Se algum campo obrigatório estiver vazio
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str) -> None:
        """
        Inicializa um novo livro com validações.
        
        Args:
            titulo: Título do livro (obrigatório)
            autor: Nome do autor (obrigatório)
            isbn: Código ISBN (obrigatório)
        
        Raises:
            ValueError: Se titulo, autor ou isbn estiverem vazios
        """
        self._validar_campo(titulo, "Título")
        self._validar_campo(autor, "Autor")
        self._validar_campo(isbn, "ISBN")
        
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.status = STATUS_DISPONIVEL
    
    @staticmethod
    def _validar_campo(valor: str, nome_campo: str) -> None:
        """
        Valida se um campo não está vazio.
        
        Args:
            valor: Valor a ser validado
            nome_campo: Nome do campo para mensagem de erro
        
        Raises:
            ValueError: Se o valor estiver vazio
        """
        if not valor or not valor.strip():
            raise ValueError(f"{nome_campo} é obrigatório")
    
    def emprestar(self) -> None:
        """
        Marca o livro como emprestado.
        """
        self.status = STATUS_EMPRESTADO
    
    def devolver(self) -> None:
        """
        Marca o livro como disponível (devolução).
        """
        self.status = STATUS_DISPONIVEL
    
    def esta_disponivel(self) -> bool:
        """
        Verifica se o livro está disponível para empréstimo.
        
        Returns:
            bool: True se disponível, False caso contrário
        """
        return self.status == STATUS_DISPONIVEL
    
    def __repr__(self) -> str:
        """
        Representação legível do objeto Livro.
        
        Returns:
            str: Representação formatada do livro
        """
        return f"Livro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}', status='{self.status}')"


# ==================== Funções CRUD ====================

def criar_livro(titulo: str, autor: str, isbn: str) -> Optional[Livro]:
    """
    Cria e adiciona um novo livro ao sistema.
    
    Args:
        titulo: Título do livro
        autor: Nome do autor
        isbn: Código ISBN (deve ser único)
    
    Returns:
        Livro criado ou None se houve erro (ISBN duplicado ou validação falhou)
    """
    # Verifica se já existe um livro com o mesmo ISBN
    if buscar_livro_por_isbn(isbn):
        return None
    
    try:
        livro = Livro(titulo=titulo, autor=autor, isbn=isbn)
        _db_livros.append(livro)
        return livro
    except ValueError:
        return None


def listar_livros() -> List[Livro]:
    """
    Lista todos os livros cadastrados no sistema.
    
    Returns:
        Lista de livros (pode estar vazia)
    """
    return _db_livros.copy()  # Retorna cópia para evitar modificação externa


def buscar_livro_por_isbn(isbn: str) -> Optional[Livro]:
    """
    Busca um livro pelo código ISBN.
    
    Args:
        isbn: Código ISBN a ser buscado
    
    Returns:
        Livro encontrado ou None se não existir
    """
    for livro in _db_livros:
        if livro.isbn == isbn:
            return livro
    return None


def atualizar_livro(isbn: str, novo_titulo: str, novo_autor: str) -> Optional[Livro]:
    """
    Atualiza informações de um livro existente.
    
    Args:
        isbn: ISBN do livro a ser atualizado
        novo_titulo: Novo título
        novo_autor: Novo autor
    
    Returns:
        Livro atualizado ou None se não encontrado
    """
    livro = buscar_livro_por_isbn(isbn)
    
    if not livro:
        return None
    
    livro.titulo = novo_titulo
    livro.autor = novo_autor
    return livro


def deletar_livro(isbn: str) -> bool:
    """
    Remove um livro do sistema.
    
    Args:
        isbn: ISBN do livro a ser removido
    
    Returns:
        True se removido com sucesso, False se não encontrado
    """
    livro = buscar_livro_por_isbn(isbn)
    
    if not livro:
        return False
    
    _db_livros.remove(livro)
    return True 
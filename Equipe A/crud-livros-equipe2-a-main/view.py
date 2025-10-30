"""
Controlador de Views - Interface HTTP
Sistema de Gestão de Biblioteca Universitária (SGBU)
Equipe 2 - Catálogo de Livros

Gerencia requisições HTTP e renderiza templates HTML
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from html import escape
from typing import Dict, List
import json
import livro


def _esc(valor: str) -> str:
    """
    Escapa HTML para prevenir ataques XSS.
    
    Args:
        valor: String a ser escapada
        
    Returns:
        String com caracteres HTML escapados
    """
    return escape("" if valor is None else str(valor))


class LivroController(BaseHTTPRequestHandler):
    """
    Controlador HTTP para o sistema de gerenciamento de livros.
    
    Processa requisições GET (páginas) e POST (formulários/AJAX).
    """
    
    def do_GET(self) -> None:
        """
        Processa requisições GET (visualização de páginas).
        
        Rotas disponíveis:
        - / : Redireciona para página principal
        - /menu : Página principal
        - /listar : Página principal com lista de livros
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path in ["/", "/menu", "/listar"]:
            self._servir_pagina_unica()
        else:
            self._servir_404()
    
    def do_POST(self) -> None:
        """
        Processa requisições POST (submissão de formulários e AJAX).
        
        Rotas disponíveis:
        - /cadastrar : Cadastra novo livro
        - /deletar : Remove livro
        - /atualizar : Atualiza dados do livro
        - /buscar : Busca livro por ISBN (retorna JSON)
        """
        rotas = {
            "/cadastrar": self._processar_cadastro,
            "/deletar": self._processar_delecao,
            "/atualizar": self._processar_atualizacao,
            "/buscar": self._processar_busca_ajax,
        }
        
        handler = rotas.get(self.path)
        if handler:
            handler()
        else:
            self._servir_404()
    
    # ==================== Métodos GET ====================
    
    def _servir_pagina_unica(self) -> None:
        """
        Serve a página principal com formulário de cadastro, busca e lista de livros.
        
        A tabela é gerada dinamicamente com base nos livros cadastrados.
        """
        livros = livro.listar_livros()
        linhas_html = self._gerar_linhas_tabela(livros)
        
        try:
            with open("templates/pagina_unica.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            
            conteudo = conteudo.replace("<!--LINHAS_TABELA-->", linhas_html)
            
            self._enviar_resposta_html(200, conteudo)
        except FileNotFoundError:
            self._servir_erro("Template não encontrado", 500)
    
    def _gerar_linhas_tabela(self, livros: List) -> str:
        """
        Gera o HTML das linhas da tabela de livros.
        
        Args:
            livros: Lista de objetos Livro
            
        Returns:
            HTML das linhas da tabela
        """
        if not livros:
            return '<tr><td colspan="4" style="text-align:center;">Nenhum livro cadastrado</td></tr>'
        
        linhas = []
        for liv in livros:
            linha = f"""
                <tr>
                    <td>{_esc(liv.isbn)}</td>
                    <td>{_esc(liv.titulo)}</td>
                    <td>{_esc(liv.autor)}</td>
                    <td class="acoes">
                        <form method="post" action="/deletar" style="display:inline;">
                            <input type="hidden" name="isbn" value="{_esc(liv.isbn)}">
                            <button type="submit">Deletar</button>
                        </form>
                        <button onclick="editarLivro('{_esc(liv.isbn)}', '{_esc(liv.titulo)}', '{_esc(liv.autor)}')">Atualizar</button>
                    </td>
                </tr>
            """
            linhas.append(linha)
        
        return "".join(linhas)
    
    def _servir_404(self) -> None:
        """Serve página de erro 404 - Página não encontrada."""
        html = """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Página não encontrada</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                h1 { color: #333; }
                a { color: #000; text-decoration: none; border: 1px solid #000; padding: 10px 20px; display: inline-block; }
            </style>
        </head>
        <body>
            <h1>404 - Página não encontrada</h1>
            <p>A página que você procura não existe.</p>
            <a href="/">Voltar à página inicial</a>
        </body>
        </html>
        """
        self._enviar_resposta_html(404, html)
    
    def _servir_erro(self, mensagem: str, codigo: int = 500) -> None:
        """
        Serve uma página de erro genérica.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
            codigo: Código HTTP do erro (padrão: 500)
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Erro</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                h1 {{ color: #d32f2f; }}
            </style>
        </head>
        <body>
            <h1>Erro {codigo}</h1>
            <p>{_esc(mensagem)}</p>
            <a href="/" style="color: #000; text-decoration: none; border: 1px solid #000; padding: 10px 20px;">Voltar</a>
        </body>
        </html>
        """
        self._enviar_resposta_html(codigo, html)
    
    # ==================== Métodos POST ====================
    
    def _processar_cadastro(self) -> None:
        """
        Processa o cadastro de um novo livro.
        
        Lê os dados do formulário (título, autor, ISBN) e cria um novo livro.
        Redireciona para a página principal após o cadastro.
        """
        params = self._ler_parametros_post()
        
        titulo = params.get("titulo", [""])[0]
        autor = params.get("autor", [""])[0]
        isbn = params.get("isbn", [""])[0]
        
        livro.criar_livro(titulo=titulo, autor=autor, isbn=isbn)
        self._redirecionar("/")
    
    def _processar_delecao(self) -> None:
        """
        Processa a deleção de um livro.
        
        Lê o ISBN do formulário e remove o livro correspondente.
        Redireciona para a página principal após a deleção.
        """
        params = self._ler_parametros_post()
        isbn = params.get("isbn", [""])[0]
        
        livro.deletar_livro(isbn)
        self._redirecionar("/")
    
    def _processar_atualizacao(self) -> None:
        """
        Processa a atualização de dados de um livro.
        
        Lê o ISBN, novo título e novo autor do formulário e atualiza o livro.
        Redireciona para a página principal após a atualização.
        """
        params = self._ler_parametros_post()
        
        isbn = params.get("isbn", [""])[0]
        novo_titulo = params.get("titulo", [""])[0]
        novo_autor = params.get("autor", [""])[0]
        
        livro.atualizar_livro(isbn, novo_titulo, novo_autor)
        self._redirecionar("/")
    
    def _processar_busca_ajax(self) -> None:
        """
        Processa a busca de livro por ISBN via AJAX.
        
        Retorna JSON com os dados do livro encontrado ou indicação de não encontrado.
        Formato de resposta:
        - Encontrado: {"encontrado": true, "isbn": "...", "titulo": "...", "autor": "...", "status": "..."}
        - Não encontrado: {"encontrado": false}
        """
        params = self._ler_parametros_post()
        isbn = params.get("isbn", [""])[0]
        
        livro_encontrado = livro.buscar_livro_por_isbn(isbn)
        
        if livro_encontrado:
            resultado = {
                "encontrado": True,
                "isbn": livro_encontrado.isbn,
                "titulo": livro_encontrado.titulo,
                "autor": livro_encontrado.autor,
                "status": livro_encontrado.status
            }
        else:
            resultado = {"encontrado": False}
        
        self._enviar_resposta_json(resultado)
    
    # ==================== Métodos Auxiliares ====================
    
    def _ler_parametros_post(self) -> Dict[str, List[str]]:
        """
        Lê e decodifica os parâmetros de uma requisição POST.
        
        Returns:
            Dicionário com os parâmetros do formulário
        """
        tamanho = int(self.headers["Content-Length"])
        dados = self.rfile.read(tamanho).decode("utf-8")
        return parse_qs(dados)
    
    def _enviar_resposta_html(self, codigo: int, conteudo: str) -> None:
        """
        Envia uma resposta HTTP com conteúdo HTML.
        
        Args:
            codigo: Código de status HTTP
            conteudo: Conteúdo HTML a ser enviado
        """
        self.send_response(codigo)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo.encode("utf-8"))
    
    def _enviar_resposta_json(self, dados: Dict) -> None:
        """
        Envia uma resposta HTTP com conteúdo JSON.
        
        Args:
            dados: Dicionário a ser serializado como JSON
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        resultado_json = json.dumps(dados, ensure_ascii=False)
        self.wfile.write(resultado_json.encode("utf-8"))
    
    def _redirecionar(self, url: str) -> None:
        """
        Redireciona para uma URL específica (HTTP 302).
        
        Args:
            url: URL de destino do redirecionamento
        """
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()
    
    def log_message(self, format: str, *args) -> None:
        """
        Sobrescreve o método de log para desabilitar logs automáticos.
        
        Mantém o terminal limpo durante a execução do servidor.
        """
        pass

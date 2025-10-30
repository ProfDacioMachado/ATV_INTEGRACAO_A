"""
Sistema de Gestão de Biblioteca - SGBU
Equipe 2 - Catálogo de Livros
Servidor HTTP Principal
"""

from http.server import HTTPServer
import view

def main():
    print("iniciando Sistema de Gestão de Biblioteca...")
    
    servidor = HTTPServer(("localhost", 8002), view.LivroController)
    print("servidor rodando em http://localhost:8002")

    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nservidor encerrado.")

if __name__ == "__main__":
    main()

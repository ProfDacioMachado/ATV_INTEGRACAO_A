# Testes (pytest) - Delete TDD

Instruções rápidas para rodar os testes TDD de delete usando pytest no Windows PowerShell.

Requisitos:
- Python 3.8+ instalado
- (Opcional) um virtualenv

Instalar dependências:

```powershell
python -m pip install --upgrade pip; \
python -m pip install -r requirements.txt
```

Rodar os testes:

```powershell
cd "g:\\Peng Compartilhada\\Repositories\\CrudUsu-rio-TrabalhoD-cio"; \
python -m pytest -q
```

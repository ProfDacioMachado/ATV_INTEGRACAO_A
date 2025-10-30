Equipe 2-A: 
Gabriel Andrade Garcia 23271855-2; 
Thiago Nunes 23000383-2;
Murilo Silva Barbosa 23135193-2;
Matheus Lopes 23202883-2;
Marcos Vinicios 23015485-2

# 🧪 Atividade Prática — Teste de Integração
## 📚 Descrição da Aplicação

A **Universidade Tabajara “TecLearn TABAJARA”** decidiu informatizar o controle de sua biblioteca.  
O sistema deve permitir:

- Empréstimo de livros  
- Cadastro de usuários  
- Controle de acervo  
- Relatórios de uso

A universidade contratou uma empresa de desenvolvimento júnior (os alunos) para criar o sistema em **módulos**, sendo que cada equipe é responsável por uma parte.  
A **integração e os testes finais** determinarão se o sistema será aprovado.

---

## 🧭 Visão Geral do Sistema

O **SGBU** fará o controle de:

- Usuários  
- Acervo (livros)  
- Empréstimos  
- Relatórios

O sistema final será composto pela integração dos módulos desenvolvidos por cada equipe.

| Equipe | Módulo / Responsabilidade | Principais Funcionalidades | Exemplo de Integração |
|--------|----------------------------|----------------------------|------------------------|
| Equipe 1 | Cadastro de Usuários | CRUD de usuários: cadastrar, editar, remover e listar usuários (nome, matrícula, tipo de usuário) | Se integra com o módulo de Empréstimo |
| Equipe 2 | Catálogo de Livros | CRUD de livros: cadastrar livros, autores, estoque, status (disponível/emprestado) | Se integra com o módulo de Empréstimo |
| Equipe 3 | Empréstimo e Devolução | Controle de empréstimos: registrar empréstimos e devoluções, verificar disponibilidade | Depende dos módulos de Usuários e Catálogo |
| Equipe 4 | Relatórios | Geração de relatórios simples: livros mais emprestados, usuários mais ativos | Depende dos dados das outras equipes |

---

## 🧑‍🏫 Disciplina

**Prof.:** Dacio Machado  
**Disciplina:** Projeto, Implementação e Teste de Software  
**Turma:** ESOFT - 6 - N  
**Valor:** +01 ATV  
**Atividade:** Teste de Integração  
**Aluno:** ___________________________

---

## 📌 Informações Gerais

Cada equipe deve:

- Seguir as **regras, interfaces e requisitos** definidos
- Desenvolver seu módulo com **TDD (Test Driven Development)**  
- Focar na **integração entre módulos**  
- Criar **testes de integração** que provem o bom funcionamento do sistema composto.

---

## 💻 Código-fonte

- Repositório: **Git (GitHub)** — cada equipe cria um repositório privado com colaboração do professor.  
- Projeto base:  
  [https://replit.com/@daciofrancisco/PersonalExpenseOrganizer](https://replit.com/@daciofrancisco/PersonalExpenseOrganizer)

---

## 📝 Formato dos Commits (Obrigatório — Evidência de TDD)

Cada teste deve conter:

1. **Commit que cria o teste (falha)**  
2. **Commit que faz o teste passar**  
3. **Commit de refactor**

**Padrão de mensagem:**

```

[TDD red] <descrição do teste>
[TDD green] <descrição do teste>
[TDD refactor] <descrição>

```

---

## 🧪 Testes Automatizados — Requisitos

Cada equipe deve prover pelo menos:

- ✅ **10 testes unitários** cobrindo casos de borda (validações, erros, sucesso)  
- ✅ **5 testes de contrato/integridade**  
  - Ex.: serialização correta, contratos de campos obrigatórios

---

## 📎 Referência

- Projeto base disponível em:  
  [https://replit.com/@daciofrancisco/PersonalExpenseOrganizer](https://replit.com/@daciofrancisco/PersonalExpenseOrganizer)
```

import pytest
from datetime import datetime
import sys
import os

# Adicionando o path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Model import Usuario
from Controller import usuario as uc


class TestUpdateUsuario:
    """Classe de testes para operações de atualizar de usuário seguindo TDD"""
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.usuario_valido = Usuario.Usuario(
            id=1,
            nome="João Silva",
            matricula="ALU12345",
            tipo="ALUNO",
            email="joao@email.com",
            ativoDeRegistro="2025-01-15T10:30:00Z",
            status="ATIVO"
        )
        self.usuario_existente = Usuario.Usuario(
            id=2,
            nome="Maria Silva",
            matricula="PROF54321",  # Matrícula que será testada como duplicada
            tipo="PROFESSOR",
            email="maria@email.com",  # Email que será testado como duplicado
            ativoDeRegistro="2025-01-15T10:30:00Z",
            status="ATIVO"
        )
        # Inicializa o controller com os usuários de teste
        self.client = uc.UsuarioController(usuarios=[self.usuario_valido, self.usuario_existente])
    
    def test_update_usuario_dados_validos(self):
        """Teste: deve atualizar usuário com dados válidos"""
        dados_atualizacao = {
            "nome": "João Santos Silva",
            "email": "joao.santos@email.com",
            "status": "ATIVO"
        }
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_nome_valido(self):
        """Teste: deve atualizar nome com string válida (1-100 caracteres)"""
        dados_atualizacao = {"nome": "Maria da Silva Santos"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_nome_muito_longo(self):
        """Teste: deve falhar ao tentar atualizar nome com mais de 100 caracteres"""
        nome_longo = "a" * 101
        dados_atualizacao = {"nome": nome_longo}
        
        with pytest.raises(ValueError, match="Nome deve ter entre 1 e 100 caracteres"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_nome_vazio(self):
        """Teste: deve falhar ao tentar atualizar nome vazio"""
        dados_atualizacao = {"nome": ""}
        
        with pytest.raises(ValueError, match="Nome deve ter entre 1 e 100 caracteres"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_matricula_valida(self):
        """Teste: deve atualizar matrícula válida (5-20 caracteres alfanuméricos)"""
        dados_atualizacao = {"matricula": "PROF98765"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_matricula_muito_curta(self):
        """Teste: deve falhar ao tentar atualizar matrícula muito curta"""
        dados_atualizacao = {"matricula": "A123"}
        
        with pytest.raises(ValueError, match="Matrícula deve ter entre 5 e 20 caracteres alfanuméricos"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_matricula_muito_longa(self):
        """Teste: deve falhar ao tentar atualizar matrícula muito longa"""
        matricula_longa = "A" * 21
        dados_atualizacao = {"matricula": matricula_longa}
        
        with pytest.raises(ValueError, match="Matrícula deve ter entre 5 e 20 caracteres alfanuméricos"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_matricula_caracteres_especiais(self):
        """Teste: deve falhar ao tentar atualizar matrícula com caracteres especiais"""
        dados_atualizacao = {"matricula": "ALU123@#"}
        
        with pytest.raises(ValueError, match="Matrícula deve conter apenas caracteres alfanuméricos"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_tipo_valido_aluno(self):
        """Teste: deve atualizar tipo para ALUNO"""
        dados_atualizacao = {"tipo": "ALUNO"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_tipo_valido_professor(self):
        """Teste: deve atualizar tipo para PROFESSOR"""
        dados_atualizacao = {"tipo": "PROFESSOR"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_tipo_valido_funcionario(self):
        """Teste: deve atualizar tipo para FUNCIONARIO"""
        dados_atualizacao = {"tipo": "FUNCIONARIO"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_tipo_invalido(self):
        """Teste: deve falhar ao tentar atualizar tipo inválido"""
        dados_atualizacao = {"tipo": "DIRETOR"}
        
        with pytest.raises(ValueError, match="Tipo deve ser ALUNO, PROFESSOR ou FUNCIONARIO"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_email_formato_valido(self):
        """Teste: deve atualizar email com formato válido"""
        dados_atualizacao = {"email": "usuario@dominio.com.br"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_email_formato_invalido(self):
        """Teste: deve falhar ao tentar atualizar email com formato inválido"""
        emails_invalidos = [
            "emailsemarroba.com",
            "@dominio.com",
            "email@",
            "email.com",
            "email@dominio",
        ]
        
        for email_invalido in emails_invalidos:
            dados_atualizacao = {"email": email_invalido}
            with pytest.raises(ValueError, match="Email deve ter formato válido"):
                self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_status_ativo(self):
        """Teste: deve atualizar status para ATIVO"""
        dados_atualizacao = {"status": "ATIVO"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_status_inativo(self):
        """Teste: deve atualizar status para INATIVO"""
        dados_atualizacao = {"status": "INATIVO"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_status_suspenso(self):
        """Teste: deve atualizar status para SUSPENSO"""
        dados_atualizacao = {"status": "SUSPENSO"}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_status_invalido(self):
        """Teste: deve falhar ao tentar atualizar status inválido"""
        dados_atualizacao = {"status": "PENDENTE"}
        
        with pytest.raises(ValueError, match="Status deve ser ATIVO, INATIVO ou SUSPENSO"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_atualizar_inexistente(self):
        """Teste: deve falhar ao tentar atualizar usuário que não existe"""
        dados_atualizacao = {"nome": "Novo Nome"}
        id_inexistente = 999
        
        with pytest.raises(ValueError, match="Usuário não encontrado"):
            self.client.atualizar(id_inexistente, dados_atualizacao)
    
    def test_update_id_invalido(self):
        """Teste: deve falhar ao tentar atualizar com ID inválido"""
        dados_atualizacao = {"nome": "Novo Nome"}
        
        with pytest.raises(ValueError, match="ID deve ser um número inteiro positivo"):
            self.client.atualizar(0, dados_atualizacao)
        
        with pytest.raises(ValueError, match="ID deve ser um número inteiro positivo"):
            self.client.atualizar(-1, dados_atualizacao)
    
    def test_update_dados_vazios(self):
        """Teste: deve falhar ao tentar atualizar sem dados"""
        dados_atualizacao = {}
        
        with pytest.raises(ValueError, match="Dados de atualização não podem estar vazios"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_tentativa_alterar_id(self):
        """Teste: deve falhar ao tentar alterar o ID do usuário"""
        dados_atualizacao = {"id": 999}
        
        with pytest.raises(ValueError, match="ID não pode ser alterado"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_tentativa_alterar_ativo_de_registro(self):
        """Teste: deve falhar ao tentar alterar a data de registro"""
        dados_atualizacao = {"ativoDeRegistro": "2025-10-23T10:30:00Z"}
        
        with pytest.raises(ValueError, match="Data de registro não pode ser alterada"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_matricula_duplicada(self):
        """Teste: deve falhar ao tentar atualizar para matrícula já existente"""
        dados_atualizacao = {"matricula": "PROF54321"}  # Assumindo que já existe
        
        with pytest.raises(ValueError, match="Matrícula já está em uso"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_email_duplicado(self):
        """Teste: deve falhar ao tentar atualizar para email já existente"""
        dados_atualizacao = {"email": "maria@email.com"}  # Assumindo que já existe
        
        with pytest.raises(ValueError, match="Email já está em uso"):
            self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
    
    def test_update_multiplos_campos_validos(self):
        """Teste: deve atualizar múltiplos campos válidos simultaneamente"""
        dados_atualizacao = {
            "nome": "João Santos da Silva",
            "email": "joao.santos.silva@email.com",
            "status": "ATIVO",
            "tipo": "PROFESSOR"
        }
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_email_opcional_none(self):
        """Teste: deve permitir remover email (campo opcional)"""
        dados_atualizacao = {"email": None}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True
    
    def test_update_email_opcional_vazio(self):
        """Teste: deve permitir email vazio (campo opcional)"""
        dados_atualizacao = {"email": ""}
        
        resultado = self.client.atualizar(self.usuario_valido.id, dados_atualizacao)
        assert resultado is True

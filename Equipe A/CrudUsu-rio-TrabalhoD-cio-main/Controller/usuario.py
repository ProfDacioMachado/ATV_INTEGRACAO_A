from dataclasses import dataclass, asdict, replace
from typing import List
from Model import Usuario as u
from View_and_Interface.interfaces import usuario as uv
import re
from datetime import datetime
from enum import Enum

class UsuarioController:
    """
    Controller em memória para CRUD de Usuário.
    A lista é pré-populada com 3 usuários ao primeiro uso.
    """

    _usuarios: List[u.Usuario] = []

    def __init__(self, usuarios: List[u.Usuario] = None):
        # popula apenas uma vez
        if not self._usuarios and usuarios is None:
            self._seed()
        else:
            self._usuarios = usuarios or []


    def _seed(self):
        self._usuarios = [
            u.Usuario(
                id=1,
                nome="Joao",
                matricula="ESOFT",
                tipo="ALUNO",
                email="jp@fromTheSouth",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="ATIVO",
            ),
            u.Usuario(
                id=2,
                nome="Ana",
                matricula="ABC123",
                tipo="ALUNO",
                email="ana@domain",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="INATIVO",
            ),
            u.Usuario(
                id=3,
                nome="Jose",
                matricula="PSICO",
                tipo="PROFESSOR",
                email="jose@domain",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="SUSPENSO",
            ),
        ]

    def listar(self) -> List[u.Usuario]:
        return [self._usuarios] if self._usuarios and len(self._usuarios) > 0 else []

    def obter_por_id(self, usuario_id: int) -> u.Usuario:
        u = next((x for x in self._usuarios if x.id == usuario_id), None)
        return u if u else None

    def criar(self, dados: dict) -> u.Usuario:
        # validações

        # campos obrigatórios
        required = ["nome", "email", "matricula", "tipo", "status", "ativoDeRegistro"]
        for field in required:
            if field not in dados or dados[field] is None:
                raise ValueError(f"Campo obrigatório ausente: {field}")

        # nome: 1-100 caracteres
        nome = str(dados["nome"]).strip()
        if not (1 <= len(nome) <= 100):
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")

        # email: formato básico e único (case-insensitive)
        email = str(dados["email"]).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("Email inválido")
        if any((usr.email or "").lower() == email.lower() for usr in self._usuarios):
            raise ValueError("Email já cadastrado")

        # matricula: alfanumérica 5-20 e única (case-insensitive)
        matricula = str(dados["matricula"]).strip()
        if not (5 <= len(matricula) and len(matricula) <= 20):
            raise ValueError("Matrícula deve ser alfanumérica com 5 a 20 caracteres")
        if any((usr.matricula or "").lower() == matricula.lower() for usr in self._usuarios):
            raise ValueError("Matrícula já cadastrada")

        # tipo e status: devem existir nos enums em Model.Usuario (se os enums estiverem definidos)
        tipo_val = str(dados["tipo"]).strip()
        status_val = str(dados["status"]).strip()

        # validação flexível: se existem enums u.Tipo / u.Status, validamos contra eles; caso contrário, exigimos string não vazia
        def _validate_enum_or_nonempty(enum_cls, value, name):
            if hasattr(u, enum_cls):
                enum_type = getattr(u, enum_cls)
                try:
                    if isinstance(enum_type, type) and issubclass(enum_type, Enum):
                        valid_names = {e.name for e in enum_type}
                        valid_values = {str(e.value) for e in enum_type}
                        if value not in valid_names and value not in valid_values:
                            raise ValueError(f"{name} inválido; valores válidos: {sorted(valid_names | valid_values)}")
                        return
                except TypeError:
                    # enum_cls exists but is not a subclass of Enum -> fallthrough to non-empty check
                    pass
            if not value:
                raise ValueError(f"{name} inválido")

        _validate_enum_or_nonempty("Tipo", tipo_val, "Tipo")
        _validate_enum_or_nonempty("Status", status_val, "Status")

        # ativoDeRegistro: aceitar ISO 8601 com Z ou com offset ou sem timezone (validação simples)
        ativo = str(dados["ativoDeRegistro"]).strip()
        iso_parsed = False
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                datetime.strptime(ativo, fmt)
                iso_parsed = True
                break
            except Exception:
                continue
        if not iso_parsed:
            raise ValueError("ativoDeRegistro deve estar em formato ISO 8601 (ex: 2025-01-15T10:30:00Z)")

        # criar id
        next_id = max((usr.id for usr in self._usuarios), default=0) + 1
        usuario = u.Usuario(
            id=dados.get("id", next_id),
            nome=nome,
            matricula=matricula,
            tipo=tipo_val,
            email=email,
            ativoDeRegistro=ativo,
            status=status_val,
        )
        self._usuarios.append(usuario)
        return usuario

    def atualizar(self, usuario_id: int, dados: dict) -> bool:
        # Validação do ID
        if not isinstance(usuario_id, int) or usuario_id <= 0:
            raise ValueError("ID deve ser um número inteiro positivo")

        # Validação dos dados
        if not dados:
            raise ValueError("Dados de atualização não podem estar vazios")

        usuario = next((u for u in self._usuarios if u.id == usuario_id), None)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        # Validações dos campos
        if "nome" in dados:
            nome = str(dados["nome"]).strip()
            if not (1 <= len(nome) <= 100):
                raise ValueError("Nome deve ter entre 1 e 100 caracteres")

        if "matricula" in dados:
            matricula = str(dados["matricula"]).strip()
            if not (5 <= len(matricula) <= 20):
                raise ValueError("Matrícula deve ter entre 5 e 20 caracteres alfanuméricos")
            if not matricula.isalnum():
                raise ValueError("Matrícula deve conter apenas caracteres alfanuméricos")
            # Verificar duplicata de matrícula
            if any((u.matricula or "").lower() == matricula.lower() for u in self._usuarios if u.id != usuario_id):
                raise ValueError("Matrícula já está em uso")

        if "email" in dados and dados["email"] is not None and dados["email"] != "":
            email = str(dados["email"]).strip()
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError("Email deve ter formato válido")
            # Verificar duplicata de email
            if any((u.email or "").lower() == email.lower() for u in self._usuarios if u.id != usuario_id):
                raise ValueError("Email já está em uso")

        if "tipo" in dados:
            tipo = str(dados["tipo"]).strip().upper()
            tipos_validos = ["ALUNO", "PROFESSOR", "FUNCIONARIO"]
            if tipo not in tipos_validos:
                raise ValueError("Tipo deve ser ALUNO, PROFESSOR ou FUNCIONARIO")

        if "status" in dados:
            status = str(dados["status"]).strip().upper()
            status_validos = ["ATIVO", "INATIVO", "SUSPENSO"]
            if status not in status_validos:
                raise ValueError("Status deve ser ATIVO, INATIVO ou SUSPENSO")

        # Atualizar os campos
        idx = self._usuarios.index(usuario)
        atualizado = usuario.replace(
            nome=dados.get("nome", usuario.nome),
            matricula=dados.get("matricula", usuario.matricula),
            tipo=dados.get("tipo", usuario.tipo),
            email=dados.get("email", usuario.email),
            status=dados.get("status", usuario.status)
        )
        self._usuarios[idx] = atualizado
        return True

    def deletar(self, usuario_id: int) -> bool:
        for idx, u in enumerate(self._usuarios):
            print(f"Checking user with ID: {u.id} against target ID: {usuario_id}")
            if u.id == usuario_id:
                del self._usuarios[idx]
                return True
        return False

    # utilitários
    def buscar_por_matricula(self, matricula: str) -> List[u.Usuario]:
        """Busca por matrícula usando regex (case-insensitive, permite busca por pedaço).
        Se o padrão informado for inválido como regex, faz escape e busca literal.
        """
        if not matricula:
            return []
        try:
            pattern = re.compile(matricula, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(matricula), re.IGNORECASE)
        return [usr for usr in self._usuarios if usr.matricula and pattern.search(usr.matricula)]


    def buscar_por_tipo(self, tipo: str) -> List[u.Usuario]:
        if tipo is None:
            return []
        input_tipo = str(tipo).upper()

        return [usr for usr in self._usuarios if usr.get_tipo().upper() == input_tipo.upper()]

    def buscar_por_nome(self, nome: str) -> List[u.Usuario]:
        """Busca por nome usando regex (case-insensitive, permite busca por pedaço da palavra).
        Se o padrão informado for inválido como regex, faz escape e busca literal.
        """
        if not nome or nome.strip() == "":
            return []
        try:
            pattern = re.compile(nome, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(nome), re.IGNORECASE)
        return [usr for usr in self._usuarios if usr.get_nome() and pattern.search(usr.get_nome())]

    def contar(self) -> int:
        return len(self._usuarios)

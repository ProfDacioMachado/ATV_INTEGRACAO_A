from html import escape
from Model import Usuario as u
from Controller import usuario as uc


def _esc(v):
    return escape("" if v is None else str(v))


class UsuarioViewer:

    @staticmethod
    def create_usuario_element(usuario: u.Usuario) -> str:

        return (
            f"<tr onclick='window.location.href=\"/atualizar_usuario?id="f"{_esc(usuario.id)}\"'>"
            f"<td>{_esc(usuario.id)}</td>"
            f"<td>{_esc(usuario.nome)}</td>"
            f"<td>{_esc(usuario.tipo)}</td>"
            f"<td>{_esc(usuario.email)}</td>"
            f"<td>{_esc(usuario.status)}</td>"
            "</tr>"
        )

    @staticmethod
    def call_listar(controller) -> str:
        lista = ""

        with open("View_and_Interface/views/lista_user.html", "r",
                  encoding="utf-8") as f:
            print("Leu Pagina")
            conteudo = f.read()

            users = controller.listar()
            # controller may return nested list in some implementations; normalize
            if isinstance(users, list) and len(users) == 1 and isinstance(users[0], list):
                users = users[0]

            for usuario in users:
                print(f'Iterou com user -> {getattr(usuario, "nome", None)}')
                newElement = UsuarioViewer.create_usuario_element(usuario)
                lista += newElement

            conteudo = conteudo.replace("<!-- Dados -->", lista)

        return conteudo
    
    @staticmethod
    def call_cadastrar() -> str:
        lista = ""

        with open("View_and_Interface/views/cadastro_user.html", "r",
                  encoding="utf-8") as f:
            conteudo = f.read()

            conteudo = conteudo.replace("<!-- Dados -->", lista)

        return conteudo
    
    @staticmethod
    def call_atualizar(user_id, controller) -> str:
        with open("View_and_Interface/views/atualizar_usuario.html", "r",
                  encoding="utf-8") as f:
            conteudo = f.read()

            user = controller.obter_por_id(int(user_id))

            if user:
                # Preencher o campo ID
                conteudo = conteudo.replace('id="id" name="id" readonly>', 
                                          f'id="id" name="id" readonly value="{_esc(user.id)}">')
                
                # Preencher o campo Nome
                conteudo = conteudo.replace('id="nome" name="nome" required>', 
                                          f'id="nome" name="nome" required value="{_esc(user.nome)}">')
                
                # Preencher o campo Matrícula
                conteudo = conteudo.replace('id="matricula" name="matricula" required>', 
                                          f'id="matricula" name="matricula" required value="{_esc(user.matricula)}">')
                
                # Preencher o campo Email
                conteudo = conteudo.replace('id="email" name="email" required>', 
                                          f'id="email" name="email" required value="{_esc(user.email)}">')
                
                # Preencher o campo Data de Registro
                data_registro = ""
                if user.ativoDeRegistro:
                    # Extrair apenas a data (YYYY-MM-DD) se estiver no formato ISO
                    data_str = str(user.ativoDeRegistro)
                    if 'T' in data_str:
                        data_registro = data_str.split('T')[0]  # Pega apenas a parte antes do 'T'
                    else:
                        data_registro = _esc(user.ativoDeRegistro)
                conteudo = conteudo.replace('id="ativoDeRegistro" name="ativoDeRegistro" required>', 
                                          f'id="ativoDeRegistro" name="ativoDeRegistro" required value="{data_registro}">')
                
                # Preencher o campo Tipo (select)
                tipo_value = user.tipo.value if hasattr(user.tipo, 'value') else str(user.tipo)
                conteudo = conteudo.replace(f'<option value="{tipo_value}">', 
                                          f'<option value="{tipo_value}" selected>')
                
                # Preencher o campo Status (select)
                status_value = user.status.value if hasattr(user.status, 'value') else str(user.status)
                conteudo = conteudo.replace(f'<option value="{status_value}">', 
                                          f'<option value="{status_value}" selected>')

        return conteudo

    @staticmethod
    def call_menu():
        with open("View_and_Interface/views/menu_user.html", "rb") as f:
            conteudo = f.read()

        return conteudo
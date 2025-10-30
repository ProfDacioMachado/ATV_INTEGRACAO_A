from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from Model.Despesa import Despesa
import controler as ctl
from html import escape
from Controller import usuario as uc
from View_and_Interface.interfaces import usuario as uv
from urllib.parse import urlparse, parse_qs

def _esc(v):
    return escape("" if v is None else str(v))


comTrole = ctl.Controler(True)
itens_list = comTrole.Get_Despesas()
bancos = comTrole.get_Bancos_List()
controller = uc.UsuarioController()


class MainController(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        elif self.path == "/menu":
            with open("View_and_Interface/menu.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/cadastrar_despesa":
            with open("View_and_Interface/visao.html", "r",
                      encoding="utf-8") as f:
                conteudo = f.read()

            opcoes = ""
            for banco in bancos:
                opcoes += f"<option value='{banco}'>{banco}</option>"

            conteudo = conteudo.replace("<!--BANCOS-->", opcoes)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_despesas":
            resposta = ""
            for i, d in enumerate(itens_list, start=1):
                valor_fmt = f"R$ {d.get('valor', 0):.2f}".replace('.', ',')
                descricao = _esc(d.get("descricao", ""))
                resposta += ('<a href="/detalhe_despesa?id={i}" class="item">'
                             '<span class="valor">{valor_fmt}</span>'
                             '<span class="descricao">{descricao}</span>'
                             '</a>')
            with open("View_and_Interface/visao_despesa.html",
                      "r",
                      encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--itens-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_conta":
            with open("View_and_Interface/cadastrar_banco.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)
        
        elif self.path == "/usuarios":
            conteudo = uv.UsuarioViewer.call_menu()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/listar_usuarios":
            conteudo = uv.UsuarioViewer.call_listar(controller=controller)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_usuario":
            conteudo = uv.UsuarioViewer.call_cadastrar()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif  "/atualizar_usuario" in self.path:
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            user_id = query_params.get('id', [''])[0]

            conteudo = uv.UsuarioViewer.call_atualizar(controller=controller, user_id=user_id)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

    def do_POST(self):
        if self.path == "/cadastrar":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            despesa = {
                "data": params.get("dat_despesa", [""])[0],
                "valor": float(params.get("valor", [0])[0]),
                "categoria": params.get("cat_despesa", [""])[0],
                "descricao": params.get("descricao", [""])[0],
                "tag": params.get("tag", [""])[0],
                "forma_pgmt": params.get("forma_pgmt", [""])[0],
                "banco": params.get("banco", [""])[0]
            }

            comTrole.Ctr_Adiciona_Despesa(despesa)
            item_formatado = (
                f"<p><span class='label'>Data:</span> {_esc(despesa.get('data'))}</p>"
                f"<p><span class='label'>Valor:</span> {_esc(despesa.get('valor'))}</p>"
                f"<p><span class='label'>Categoria:</span> {_esc(despesa.get('categoria'))}</p>"
                f"<p><span class='label'>Descrição:</span> {_esc(despesa.get('descricao'))}</p>"
                f"<p><span class='label'>Tag:</span> {_esc(despesa.get('tag'))}</p>"
                f"<p><span class='label'>Forma de Pagamento:</span> {_esc(despesa.get('forma_pgmt'))}</p>"
                f"<p><span class='label'>Banco:</span> {_esc(despesa.get('banco'))}</p>"
            )
            with open("View_and_Interface/visao_cadastrada.html",
                      "r",
                      encoding="utf-8") as f:
                conteudo = f.read()

            conteudo = conteudo.replace("<!--DADO-->", item_formatado)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        # Check for POST request to /atualizar_usuario and which button was pressed
        elif "/atualizar_usuario" in self.path:
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)
            
            # Check which button was pressed
            if "btn_atualizar" in params:
                # Handle update button
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                user_id = query_params.get('id', [''])[0]
                
                # Validate user_id
                if not user_id or not user_id.strip():
                    self.send_response(400)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"<h1>400 - ID do usuario nao fornecido</h1>")
                    return
                
                # Extract form data for updating
                nome = params.get("nome", [""])[0]
                matricula = params.get("matricula", [""])[0]
                tipo = params.get("tipo", [""])[0]
                email = params.get("email", [""])[0]
                ativoDeRegistro = params.get("ativoDeRegistro", [""])[0]
                status = params.get("status", [""])[0]
                
                user_dict = {
                    "nome": nome,
                    "matricula": matricula,
                    "tipo": tipo,
                    "email": email,
                    "ativoDeRegistro": ativoDeRegistro,
                    "status": status
                }
                
                try:
                    controller.atualizar(int(user_id), user_dict)
                    # Redirect to user list after successful update
                    self.send_response(302)
                    self.send_header("Location", "/listar_usuarios")
                    self.end_headers()
                except Exception as e:
                    # Handle update error
                    conteudo = uv.UsuarioViewer.call_atualizar(controller=controller, user_id=user_id)
                    conteudo = conteudo.replace("<!--MENSAGEM_ERRO-->", f"<p class='erro'>Erro ao atualizar usuário: {e}</p>")
                    
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(conteudo.encode("utf-8"))
                    
            elif "btn_excluir" in params:
                # Handle delete button
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                user_id = query_params.get('id', [''])[0]
                
                # Validate user_id
                if not user_id or not user_id.strip():
                    self.send_response(400)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"<h1>400 - ID do usuario nao fornecido</h1>")
                    return
                
                try:
                    controller.deletar(int(user_id))
                    # Redirect to user list after successful deletion
                    self.send_response(302)
                    self.send_header("Location", "/listar_usuarios")
                    self.end_headers()
                except Exception as e:
                    # Handle deletion error
                    conteudo = uv.UsuarioViewer.call_atualizar(controller=controller, user_id=user_id)
                    conteudo = conteudo.replace("<!--MENSAGEM_ERRO-->", f"<p class='erro'>Erro ao excluir usuário: {e}</p>")
                    
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/calcular_total":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)
            mes = params.get("mes", [""])[0]

            total = comTrole.Get_Total_Mensal(mes)
            resposta = f"""
            <h1>Total do mês {mes}: R$ {total:.2f}</h1>
            <a href="/">Voltar ao Menu</a>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/login":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            user = params.get("user", [""])[0]
            senha = params.get("senha", [""])[0]

            if comTrole.Atutenticar(user, senha):
                # Login OK → manda para menu
                self.send_response(302)
                self.send_header("Location", "/menu")
                self.end_headers()
            else:
                # Login falhou → recarrega tela com erro
                with open("View_and_Interface/login.html",
                          "r",
                          encoding="utf-8") as f:
                    conteudo = f.read()
                conteudo = conteudo.replace(
                    "<!--MENSAGEM_ERRO-->",
                    "<p class='erro'>Usuário ou senha incorretos.</p>")
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))
        elif self.path == "/cadastrar_usuario":
            try:
                tamanho = int(self.headers["Content-Length"])
                dados = self.rfile.read(tamanho).decode("utf-8")
                params = parse_qs(dados)


                nome = params.get("nome", "")
                matricula = params.get("matricula", "")
                tipo = params.get("tipo", "")
                email = params.get("email", "")
                ativoDeRegistro = params.get("ativoDeRegistro", "")
                status = params.get("status", "")

                print(f"Recebeu dados: {nome}, {matricula}, {tipo}, {email}, {ativoDeRegistro}, {status}")

                user_dict = {
                    "nome": nome[0] if nome else "",
                    "matricula": matricula[0] if matricula else "",
                    "tipo": tipo[0] if tipo else "",
                    "email": email[0] if email else "",
                    "ativoDeRegistro": ativoDeRegistro[0] if ativoDeRegistro else "",
                    "status": status[0] if status else ""
                }

                controller.criar(dados=user_dict)
                print("Usuário criado com sucesso.")
                # Redireciona para a lista de usuários
                self.send_response(302)
                self.send_header("Location", "/listar_usuarios")
                self.end_headers()
            except Exception as e:
                # Redireciona para a página de cadastro com erro
                conteudo = uv.UsuarioViewer.call_cadastrar()
                # Substitui placeholder de erro se existir no template
                conteudo = conteudo.replace("<!--MENSAGEM_ERRO-->", f"<p class='erro'>Erro ao cadastrar usuário: {e}</p>")
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))
                print(f"Erro ao criar usuário: {e}")

            

        elif self.path == "/cadastrar_conta":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = dict(x.split("=") for x in post_data.split("&"))

            bank = params.get("bank", "")
            ag = params.get("ag", "")
            cc = params.get("cc", "")
            tipo = params.get("tipo", "")

            vet_dados = [bank, ag, cc, tipo]

            bancos.append(vet_dados)
            comTrole.Ctr_Cadastra_Conta(bank, ag, cc, tipo)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h3>Conta bancaria cadastrada com sucesso!</h3>")
            self.wfile.write(b'<a href="/menu">Voltar ao menu</a>')

        elif self.path == "/user":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>User endpoint</h1>")


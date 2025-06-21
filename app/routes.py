import os  # Importa módulo para manipulação de caminhos e diretórios
from flask import redirect, render_template, url_for # Importa funções do Flask para renderização de templates, redirecionamento, etc.
from flask_login import current_user, login_required, login_user, logout_user # Importa funções para gerenciamento de login de usuários
from werkzeug.utils import secure_filename  # Importa função para garantir nomes de arquivos seguros
from app import app, bcrypt, db  # Importa instâncias do app, bcrypt e banco de dados
from app.forms import FormLogin, FormRegistrar, FormFotoPost # Importa os formulários de login e registro
from app.models import Usuario, Post # Importa os modelos de usuário e post


@app.route('/', methods=['GET', 'POST']) 
def index():
    """
    Rota principal do aplicativo, exibe o formulário de login e registra usuários.
    Se o usuário já estiver logado, redireciona para o perfil.
    Se o formulário de login for enviado e válido, verifica as credenciais do usuário.
    Se as credenciais forem válidas, loga o usuário e redireciona para o perfil.
    Se o usuário não existir ou as credenciais forem inválidas, permanece na página de login.
    """
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        # Verifica se o usuário existe
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', usuario_id=usuario.id))
    return render_template('index.html', form=formLogin)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """
    Rota para registrar um novo usuário.
    Se o usuário já estiver logado, redireciona para o perfil.
    Se o formulário de registro for enviado e válido, cria um novo usuário e o loga automaticamente.
    Se o registro for bem-sucedido, redireciona para o perfil do usuário recém-criado.
    Se o formulário não for válido, permanece na página de registro.
    """
    formRegistrar = FormRegistrar()
    if formRegistrar.validate_on_submit():
        # Cria um novo usuário
        novo_usuario = Usuario(
            username=formRegistrar.username.data,
            email=formRegistrar.email.data,
            senha=bcrypt.generate_password_hash(formRegistrar.senha.data).decode('utf-8')
        )
        db.session.add(novo_usuario)
        db.session.commit()
        login_user(novo_usuario, remember=True)  # Loga o usuário automaticamente após o registro
        return redirect(url_for('perfil', usuario_id=novo_usuario.id))
    return render_template('registrar.html', form=formRegistrar)

@app.route('/perfil/<int:usuario_id>', methods=['GET', 'POST'])
@login_required  # Garante que o usuário esteja logado para acessar esta rota
def perfil(usuario_id):
    """
    Rota para exibir o perfil de um usuário.
    Se o usuário logado for o mesmo do perfil solicitado, permite que ele envie uma foto.
    Se o formulário de foto for enviado e válido, salva a foto no diretório especificado e cria um novo post.
    Se o usuário logado não for o dono do perfil, exibe o perfil sem a opção de enviar foto.
    """
    if int(usuario_id) == int(current_user.id):
        form_foto = FormFotoPost()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo dentro da pasta certa
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # criar a foto no banco com o item "imagem" sendo o nome do arqivo
            foto = Post(imagem=nome_seguro, usuario_id=current_user.id)
            db.session.add(foto)
            db.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(usuario_id)
        return render_template('perfil.html', usuario=usuario, is_owner=False, form=None)

@app.route('/logout')
@login_required
def logout():
    """
    Rota para fazer logout do usuário.
    Se o usuário estiver logado, faz logout e redireciona para a página inicial.
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/feed')
@login_required
def feed():
    """
    Rota para exibir o feed de posts.
    Exibe todos os posts ordenados pela data de criação em ordem decrescente.
    Se o usuário não estiver logado, redireciona para a página inicial.
    """
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('feed.html', posts=posts)
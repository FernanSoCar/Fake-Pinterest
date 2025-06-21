from flask_login import UserMixin  # Importa classe para integração com Flask-Login
from app import db, login_manager # Importa instâncias do banco de dados e do login manager

@login_manager.user_loader
def load_user(usuario_id):
    """
    Função de callback para carregar o usuário com base no ID do usuário.
    Esta função é usada pelo Flask-Login para recuperar o usuário atual da sessão.
    Args:
        usuario_id (int): ID do usuário a ser carregado.
    Returns:
        Usuario: Instância do modelo Usuario correspondente ao ID fornecido, ou None se não encontrado.
    """
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
    """
    Modelo de usuário para o aplicativo Fake Pinterest.
    Atributos:
        id (int): ID único do usuário.
        username (str): Nome de usuário único.
        email (str): Email único do usuário.
        senha (str): Senha do usuário, armazenada de forma segura.
        fotos (relationship): Relacionamento com o modelo Post, representando as fotos postadas pelo usuário.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    fotos = db.relationship('Post', backref='usuario', lazy=True)
    
class Post(db.Model):
    """
    Modelo de post para o aplicativo Fake Pinterest.
    Atributos:
        id (int): ID único do post.
        imagem (str): Caminho da imagem do post, com um valor padrão de 'default.jpg'.
        data_criacao (datetime): Data e hora de criação do post, com valor padrão para o momento atual.
        usuario_id (int): ID do usuário que criou o post, referenciando o modelo Usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), nullable=True, default='default.jpg')
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
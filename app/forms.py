from flask_wtf import FlaskForm  # Importa a classe base para formulários Flask
from wtforms import StringField, PasswordField, SubmitField  # Importa campos de formulário
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError  # Importa validadores
from app.models import Usuario  # Importa o modelo de usuário
from flask_wtf.file import FileField, FileAllowed  # Importa campos e validadores para upload de arquivos

class FormLogin(FlaskForm):
    """
    Formulário para login de usuários.
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="O email é obrigatório"),
            Email(message="Email inválido"),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="A senha é obrigatória"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres"),
        ],
    )
    submit_login = SubmitField("Entrar")
    
    def validate_email(self, email):
        """
        Valida se o email está cadastrado no banco de dados.
        Parâmetros:
            email (Field): Campo de email do formulário.
        Levanta:
            ValidationError: Se o email não estiver cadastrado.
        """
        usuario = Usuario.query.filter_by(email=email.data).first()  # Busca usuário pelo email
        if not usuario:
            raise ValidationError(
                "Usuário inexistente, crie uma conta ou verifique o email digitado."
            )

class FormRegistrar(FlaskForm):
    """
    Formulário para registro de novos usuários.
    """
    username = StringField(
        "Nome de Usuário",
        validators=[DataRequired(message="O nome de usuário é obrigatório")],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="O email é obrigatório"),
            Email(message="Email inválido"),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="A senha é obrigatória"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres"),
        ],
    )
    confirmar_senha = PasswordField(
        "Confirmar Senha",
        validators=[
            DataRequired(message="A confirmação da senha é obrigatória"),
            EqualTo("senha", message="As senhas não coincidem"),
        ],
    )
    submit_registrar = SubmitField("Criar Conta")
    
    def validate_username(self, username):
        """
        Valida se o nome de usuário já está cadastrado no banco de dados.
        Parâmetros:
            username (Field): Campo de nome de usuário do formulário.
        Levanta:
            ValidationError: Se o nome de usuário já estiver em uso.
        """
        usuario = Usuario.query.filter_by(username=username.data).first()  # Busca usuário pelo nome de usuário
        if usuario:
            raise ValidationError(
                "Já existe uma conta com esse nome de usuário. Por favor, escolha outro."
            )

    def validate_email(self, email):
        """
        Valida se o email já está cadastrado no banco de dados.
        Parâmetros:
            email (Field): Campo de email do formulário.
        Levanta:
            ValidationError: Se o email já estiver em uso.
        """
        usuario = Usuario.query.filter_by(email=email.data).first()  # Busca usuário pelo email
        if usuario:
            raise ValidationError(
                "Já existe uma conta com esse email. Por favor, escolha outro."
            )
            
class FormFotoPost(FlaskForm):
    """
    Formulário para upload de fotos de posts.
    """
    foto = FileField(
        "Foto do Post",
        validators=[
            FileAllowed(["jpg", "png", "jpeg"], "Somente imagens são permitidas"),
        ],
    )
    submit_foto_post = SubmitField("Publicar")
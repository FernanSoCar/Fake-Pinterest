import os # Importa o módulo os para manipulação de variáveis de ambiente
from flask import Flask  # Importa a classe principal do Flask
from flask_bcrypt import Bcrypt  # Importa a extensão para hash de senhas
from flask_login import LoginManager  # Importa a extensão para gerenciamento de login
from flask_sqlalchemy import SQLAlchemy  # Importa a extensão para banco de dados SQLAlchemy
from flask_wtf.csrf import CSRFProtect  # Importa proteção CSRF para formulários

app = Flask(__name__)  # Cria a instância principal do Flask

app.config['SECRET_KEY'] = 'f379c1341d0882abcb5fd24700903771'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"  # Define o diretório para uploads de arquivos

bcrypt = Bcrypt(app)  # Inicializa a extensão Bcrypt
login_manager = LoginManager(app)  # Inicializa a extensão de gerenciamento de login
login_manager.login_view = 'index'  # Define a rota de login
db = SQLAlchemy(app)  # Inicializa a extensão SQLAlchemy
csrf = CSRFProtect(app)  # Inicializa a proteção CSRF

from app import routes  # Importa as rotas do aplicativo
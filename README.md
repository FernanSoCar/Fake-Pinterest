# FakePinterest

FakePinterest é um projeto educacional que replica funcionalidades básicas do Pinterest utilizando Flask. O objetivo é demonstrar conceitos de desenvolvimento web, autenticação de usuários, upload de imagens e manipulação de banco de dados.

## Aviso

- **Este projeto é apenas para fins educacionais.**
- **Não utilize fotos ou dados pessoais reais.**
- **A chave secreta utilizada no projeto é pública e não deve ser usada em ambientes de produção.**

## Funcionalidades

- Cadastro e autenticação de usuários
- Upload de fotos para o perfil
- Visualização de feed com as imagens postadas por todos os usuários
- Visualização de perfil com as fotos postadas pelo usuário
- Logout seguro

## Tecnologias Utilizadas

- Python 3.12+
- Flask
- Flask-WTF
- Flask-Login
- Flask-Bcrypt
- Flask-SQLAlchemy
- SQLite
- HTML5 e CSS3 para o front-end
- Heroku para deploy

## Estrutura do Projeto

```
Fake_Pinterest/
│
├── app.py
├── create_db.py
├── pyproject.toml
├── README.md
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── templates/
│   └── static/
└── instance/
    └── comunidade.db
```

## Deploy

Cheque o deploy do projeto no Heroku: [FakePinterest](https://fake-pinterest-a24aae7cd238.herokuapp.com/).

---

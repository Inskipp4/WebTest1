# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
#Объект БД
db = SQLAlchemy(app)
#Объект мехенизма миграции при изменении стуктуры БД
migrate = Migrate(app, db)
#Объект механизма контролья пользователя в системе
login = LoginManager(app)
#создание ссылки на имя стриници авторизации для не зарегистрировавшихся пользователей
login.login_view = 'login'
login.login_message = 'Пожалуйста авторизуйтесь в системе'
#Объект модуля css
bootstrap = Bootstrap(app)


from app import routes

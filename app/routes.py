from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TestForm
from flask_login import current_user, login_user, logout_user, login_required
#current_user - статус пользователя
#login_user - метод авторизации пользователя
#logout_user - метод логаут
#login_required - проверка права доступа пользователя к странице
from app.models import User, Test, Answer, Attempt
from werkzeug.urls import url_parse
from random import shuffle, choices


@app.route('/login', methods=['GET', 'POST'])
def login():
    #Проверка возвращает True если пользователь имеет действительные учетные данные
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #Проверка метода запроса (Ждем POST) и соблюдения правил заполения формы
    if form.validate_on_submit():
        #запрос к БД пользователей, по введеному значению в поле Логин, взять первое значение
        user = User.query.filter_by(username=form.username.data).first()
        #проверка наличия пользователя в базе и введеного пароля
        if user is None or not user.check_password(form.password.data):
            flash("Неверный пользователь или пароль")
            return redirect(url_for('login'))
        #Функция регистрации пользоватея во время входа в систему устанавливает переменную current_user
        login_user(user, remember=form.remember_me.data)
        #получение из flask значение запрашивоемой страницы
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    attempts = Attempt().query.filter_by(user_id=current_user.id)

    return render_template('index.html', title='Главная', attempts=attempts)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Поздравляем, теперь вы зарегистрированный пользователь!")
        return redirect(url_for("login"))
    return render_template('register.html', title="Регистрация", form=form)

@app.route('/test', methods=["GET", "POST"])
def test():

    form = TestForm()
    questions = Test.query.order_by(Test.id).all()
    form.question_l = choices(questions, k=5)
    b = Answer.query.order_by(Answer.question_id).all()
    shuffle(b)
    form.question_ans = b

    if request.method == "POST":
        count = 0
        a = request.form
        for i in a.values():
            if i.isdigit():
                corr_ans = Answer.query.filter_by(id=int(i)).first()
                if corr_ans.correctly_ans:
                    count += 1
        attempt = Attempt(result=count, user_id=current_user.id)
        db.session.add(attempt)
        db.session.commit()
        return redirect(url_for('index'))
    #for quest in questions:
        #form.question_ans.append([ans for ans in answers if ans.question_id == quest.id])
    return render_template('test.html', title="Тестирование", form=form)

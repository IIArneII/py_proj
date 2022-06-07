from flask import Blueprint, redirect, render_template, request
from forms.forms import LoginForm, RegisterForm, SearchForm, WriterForm
from flask_login import logout_user, login_required, login_user
from entitis.user import User
from util import api_requests


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.post('/login')
def login_processing():
    login_form = LoginForm()

    resp = api_requests.check_password(login_form.login.data, login_form.password.data)
    if resp:
        if 'error' in resp:
            return render_template('login.html',
                                   title='Авторизация',
                                   login_form=login_form,
                                   search_form=SearchForm(),
                                   writer_form=WriterForm(),
                                   message='Неправильный логин или пароль')
        login_user(User(resp['user']), remember=login_form.remember.data)
        return redirect("/")

    return render_template('login.html',
                           title='Авторизация',
                           login_form=login_form,
                           search_form=SearchForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@login_blueprint.route('/logout')
@login_required
def logout_processing():
    logout_user()
    return redirect('/')


@login_blueprint.post('/register')
def register_processing():
    register_form = RegisterForm()

    resp = api_requests.register(register_form.login.data, register_form.password.data,
                                 register_form.email.data, register_form.birthday.data,
                                 register_form.last_name.data, register_form.first_name.data)

    if resp:
        if 'error' in resp:
            return render_template('register.html',
                                   title='Регистрация',
                                   register_form=register_form,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   message='Логин уже существует')
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           register_form=register_form,
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')

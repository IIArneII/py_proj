from flask import Blueprint, redirect, render_template
from forms.forms import LoginForm, RegisterForm, SearchForm
from flask_login import logout_user, login_required, login_user
from consts import api_root
import requests
from entitis.user import User


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.post('/login')
def login_processing():
    login_form = LoginForm()
    try:
        resp = requests.post(f'{api_root}/users/{login_form.login.data}/check_password',
                             json={'password': login_form.password.data}).json()
        if 'error' in resp:
            return render_template('login.html',
                                   title='Авторизация',
                                   login_form=login_form,
                                   search_form=SearchForm(),
                                   message='Неправильный логин или пароль')

        login_user(User(resp['user']), remember=login_form.remember.data)

        return redirect("/")
    except Exception as e:
        print(f'Error at post {api_root}/users?sort=rating&direction=decrease: {e}')
        return render_template('login.html',
                               title='Авторизация',
                               login_form=login_form,
                               search_form=SearchForm(),
                               message='Сервер не отвечает')


@login_blueprint.route('/logout')
@login_required
def logout_processing():
    logout_user()
    return redirect('/')


@login_blueprint.post('/register')
def register_processing():
    register_form = RegisterForm()
    try:
        resp = requests.post(f'{api_root}/users', json={
            'login': register_form.login.data,
            'password': register_form.password.data,
            'email': register_form.email.data,
            'birthday': str(register_form.birthday.data),
            'last_name': register_form.last_name.data,
            'first_name': register_form.first_name.data
        }).json()
        if 'error' in resp:
            return render_template('register.html',
                                   title='Регистрация',
                                   register_form=register_form,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   message='Логин уже существует')
        return redirect('/login')
    except Exception as e:
        print(f'Error at post {api_root}/users: {e}')
        return render_template('register.html',
                               title='Регистрация',
                               register_form=register_form,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')

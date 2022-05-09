from flask import Blueprint, render_template
from forms.forms import SearchForm, LoginForm, RegisterForm, WriterForm
from flask_login import login_required, current_user
import requests
from consts import api_root


pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.get('/')
def main():
    try:
        resp = requests.get(f'{api_root}/posts', params={
            'for_user_id': current_user.id,
            'post': 'post'
        }).json()
        if 'error' not in resp:
            return render_template('main.html',
                                   title='Главная',
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   posts=resp['posts'],
                                   writer_form=WriterForm())
        return render_template('main.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')
    except Exception as e:
        print(f'Error at get {api_root}/posts: {e}')
        return render_template('main.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')


@pages_blueprint.get('/register')
def register():
    return render_template('register.html',
                           title='Регистрация',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           register_form=RegisterForm())


@pages_blueprint.get('/login')
def login():
    return render_template('login.html',
                           title='Авторизация',
                           search_form=SearchForm(),
                           login_form=LoginForm())


@pages_blueprint.route('/users')
def users():
    try:
        resp = requests.get(f'{api_root}/users?sort=rating&direction=decrease').json()
        return render_template('users.html',
                               title='Пользователи',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               users=resp['users'],)
    except Exception as e:
        print(f'Error at {api_root}/users?sort=rating&direction=decrease: {e}')
        return render_template('users.html',
                               title='Пользователи',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>')
def user(user_login):
    try:
        if current_user.is_authenticated and current_user.login == user_login:
            posts = requests.get(f'{api_root}/posts', params={
                'user_id': current_user.id,
                'post': True
            }).json()
            return render_template('user.html',
                                   title=user_login,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   user=current_user,
                                   posts=posts['posts'])

        user = requests.get(f'{api_root}/users/{user_login}').json()
        if 'error' in user:
            return render_template('user.html',
                                   title=user_login,
                                   search_form=SearchForm(),
                                   message='Пользователь не найден')
        posts = requests.get(f'{api_root}/posts', params={
            'user_id': user['user']['id'],
            'post': True
        }).json()
        return render_template('user.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               user=user['user'],
                               posts=posts['posts'])
    except Exception as e:
        print(f'Error at get {api_root}/users/{user_login}: {e}')
        return render_template('user.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/following')
def user_following(user_login):
    if current_user.is_authenticated and current_user.login == user_login:
        return render_template('user_following.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               users=current_user.read,
                               user=current_user)
    try:
        resp = requests.get(f'{api_root}/users/{user_login}').json()
        if 'error' in resp:
            return render_template('user.html',
                                   title=user_login,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   message='Пользователь не найден')
        return render_template('user_following.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               users=resp['user']['read'],
                               user=resp['user'])
    except Exception as e:
        print(f'Error at get {api_root}/users/{user_login}: {e}')
        return render_template('user.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/followers')
def user_followers(user_login):
    if current_user.is_authenticated and current_user.login == user_login:
        return render_template('user_followers.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               users=current_user.readers,
                               user=current_user)
    try:
        resp = requests.get(f'{api_root}/users/{user_login}').json()
        if 'error' in resp:
            return render_template('user.html',
                                   title=user_login,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   message='Пользователь не найден')
        return render_template('user_followers.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               users=resp['user']['readers'],
                               user=resp['user'])
    except Exception as e:
        print(f'Error at get {api_root}/users/{user_login}: {e}')
        return render_template('user.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/<int:post_id>')
def post(user_login, post_id):
    try:
        post = requests.get(f'{api_root}/posts/{post_id}').json()
        comments = requests.get(f'{api_root}/posts/', params={'parent_id': post_id, 'post': 'comment'}).json()
        if 'error' not in post and 'error' not in comments:
            return render_template('post.html',
                                   title=post['post']['user']['name'],
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   post=post['post'],
                                   comments=comments['posts'])
        return render_template('main.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Пост не найден')
    except Exception as e:
        print(f'Error at get {api_root}/posts: {e}')
        return render_template('main.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               message='Сервер не отвечает')

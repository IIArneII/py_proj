from flask import Blueprint, render_template, request
from forms.forms import SearchForm, LoginForm, RegisterForm, WriterForm, SettingsForm
from flask_login import current_user, login_required
from util import api_requests
from  datetime import datetime

pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.get('/')
def main():
    if current_user.is_authenticated:
        resp = api_requests.posts(for_user_id=current_user.id, post='post')
        print(resp)
        if resp and 'error' not in resp:
            return render_template('main.html',
                                   title='Главная',
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   posts=resp['posts'])
        return render_template('main.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               message='Сервер не отвечает')
    return render_template('main.html',
                           title='Главная',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Тут пока нет постов.'
                                   'Авторизируйтесь и подпишитесь на кого-нибудь, чтобы увидеть их посты')


@pages_blueprint.get('/register')
def register():
    return render_template('register.html',
                           title='Регистрация',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           register_form=RegisterForm(),
                           writer_form=WriterForm())


@pages_blueprint.get('/login')
def login():
    return render_template('login.html',
                           title='Авторизация',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm())


@pages_blueprint.route('/users')
def users():
    resp = api_requests.users()
    if resp:
        return render_template('users.html',
                               title='Пользователи',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               users=resp['users'], )
    return render_template('users.html',
                           title='Пользователи',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>')
def user(user_login):
    if current_user.is_authenticated and current_user.login == user_login:
        posts = api_requests.posts(user_id=current_user.id, post='post')
        return render_template('user.html',
                               title=current_user.name,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               user=current_user,
                               posts=posts['posts'])

    user = api_requests.user(user_login)
    if user:
        if 'error' not in user:
            posts = api_requests.posts(user_id=user['user']['id'], post='post')
            return render_template('user.html',
                                   title=current_user.name,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   user=user['user'],
                                   posts=posts['posts'])
        return render_template('user.html',
                               title=user_login,
                               search_form=SearchForm(),
                               writer_form=WriterForm(),
                               message='Пользователь не найден')
    return render_template('user.html',
                           title=user_login,
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/following')
def user_following(user_login):
    if current_user.is_authenticated and current_user.login == user_login:
        users = api_requests.user_following(user_login)
        if users:
            return render_template('user_following.html',
                                   title=current_user.name,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   users=users['users'],
                                   user=current_user)
        else:
            return render_template('user_following.html',
                                   title=current_user.name,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   message='Сервер не отвечает')

    user = api_requests.user(user_login)
    users = api_requests.user_following(user_login)
    if user and users:
        if 'error' not in user and 'error' not in users:
            return render_template('user_following.html',
                                   title=user['user']['name'],
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   users=users['users'],
                                   user=user['user'])
        return render_template('user_following.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               message='Пользователь не найден')
    return render_template('user_following.html',
                           title=user_login,
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/followers')
def user_followers(user_login):
    if current_user.is_authenticated and current_user.login == user_login:
        users = api_requests.user_following(user_login)
        if users:
            return render_template('user_followers.html',
                                   title=current_user.name,
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   users=users['users'],
                                   user=current_user)

    user = api_requests.user(user_login)
    users = api_requests.user_followers(user_login)
    if user and users:
        if 'error' not in user and 'error' not in users:
            return render_template('user_followers.html',
                                   title=user['user']['name'],
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   users=users['users'],
                                   user=user['user'])
        return render_template('user_followers.html',
                               title=user_login,
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               message='Пользователь не найден')
    return render_template('user_followers.html',
                           title=user_login,
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/<user_login>/<int:post_id>')
def post(user_login, post_id):
    post = api_requests.post(post_id)
    comments = api_requests.posts(parent_id=post_id, post='post_and_comment')

    if post and comments:
        if 'error' not in post and 'error' not in comments:
            return render_template('post.html',
                                   title=post['post']['author']['name'],
                                   search_form=SearchForm(),
                                   login_form=LoginForm(),
                                   writer_form=WriterForm(),
                                   post=post['post'],
                                   comments=comments['posts'])
        return render_template('post.html',
                               title='Главная',
                               search_form=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               message='Пост не найден')

    return render_template('post.html',
                           title='Главная',
                           search_form=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/search')
def search():
    resp = api_requests.posts(post='post', substring=request.args.get('search'))
    if resp and 'error' not in resp:
        return render_template('search.html',
                               title='Поиск',
                               search_form_on_page=SearchForm(),
                               login_form=LoginForm(),
                               writer_form=WriterForm(),
                               posts=resp['posts'])
    return render_template('search.html',
                           title='Поиск',
                           search_form_on_page=SearchForm(),
                           login_form=LoginForm(),
                           writer_form=WriterForm(),
                           message='Сервер не отвечает')


@pages_blueprint.route('/settings')
@login_required
def settings():
    form = SettingsForm()
    form.login.data = current_user.login
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.birthday.data = datetime.strptime(current_user.birthday, '%Y-%m-%d')
    return render_template('settings.html',
                           title='Настройки',
                           search_form=SearchForm(),
                           writer_form=WriterForm(),
                           settings_form=form)

from flask import Blueprint, render_template, redirect, jsonify, abort, request
from forms.forms import SearchForm, LoginForm, RegisterForm, WriterForm
from flask_login import login_required, current_user
import requests
from consts import api_root
import uuid
from util import photo
from distutils.util import strtobool

commands_blueprint = Blueprint('commands', __name__, template_folder='templates')


@commands_blueprint.put('/<user_login>/subscribe')
@login_required
def subscribe(user_login):
    try:
        resp = requests.put(f'{api_root}/users/{current_user.login}/subscribe',
                            json={'target_user_login': user_login}).json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/{current_user.login}/subscribe: {e}')
        return abort(500, error=str(e))


@commands_blueprint.put('/<user_login>/unsubscribe')
@login_required
def unsubscribe(user_login):
    try:
        resp = requests.put(f'{api_root}/users/{current_user.login}/unsubscribe',
                            json={'target_user_login': user_login}).json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/{current_user.login}/unsubscribe: {e}')
        return abort(500, error=str(e))


@commands_blueprint.put('/<user_login>/<int:post_id>/like')
@login_required
def like(user_login, post_id):
    try:
        resp = requests.put(f'{api_root}/posts/{current_user.login}/like/{post_id}').json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/posts/{current_user.login}/like/{post_id}: {e}')
        return abort(500, error=str(e))


@commands_blueprint.put('/<user_login>/<int:post_id>/unlike')
@login_required
def unlike(user_login, post_id):
    try:
        resp = requests.put(f'{api_root}/posts/{current_user.login}/unlike/{post_id}').json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/posts/{current_user.login}/unlike/{post_id}: {e}')
        return abort(500, error=str(e))


@commands_blueprint.post('/')
@login_required
def post():
    try:
        form = WriterForm()
        uid = None
        if request.files['photo']:
            uid = str(uuid.uuid4()) + '.jpg'
        resp = requests.post(f'{api_root}/posts/{current_user.login}', json={
            'parent_id': int(form.parent_id.data),
            'post': strtobool(form.post.data),
            'content': form.content.data,
            'photo': uid
        }).json()
        if resp['success'] and uid:
            photo.save_photo(request.files['photo'].read(), 'static/img/' + uid)
        return jsonify(resp)
    except Exception as e:
        print(f'Error at post {api_root}/posts/{current_user.login}: {e}')
        return abort(500, error=str(e))

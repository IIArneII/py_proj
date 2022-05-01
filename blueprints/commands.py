from flask import Blueprint, render_template, redirect, jsonify, abort
from forms.forms import SearchForm, LoginForm, RegisterForm
from flask_login import login_required, current_user
import requests
from consts import api_root


commands_blueprint = Blueprint('commands', __name__, template_folder='templates')


@commands_blueprint.route('/<user_login>/subscribe')
@login_required
def subscribe(user_login):
    try:
        resp = requests.put(f'{api_root}/users/{current_user.login}/subscribe',
                            json={'target_user_login': user_login}).json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/{current_user.login}/subscribe: {e}')
        return abort(500, error=str(e))


@commands_blueprint.route('/<user_login>/unsubscribe')
@login_required
def unsubscribe(user_login):
    try:
        resp = requests.put(f'{api_root}/users/{current_user.login}/unsubscribe',
                            json={'target_user_login': user_login}).json()
        return jsonify(resp)
    except Exception as e:
        print(f'Error at put {api_root}/{current_user.login}/unsubscribe: {e}')
        return abort(500, error=str(e))

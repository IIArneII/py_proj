from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from api import users_resource
from data.tables import User
from data import db_session
from blueprints import pages, login, commands
from entitis.user import User
from consts import api_root
from requests import get


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'my_secret_key'


@login_manager.user_loader
def load_user(user_id):
    print('Загрузка пользователя', user_id)
    try:
        resp = get(f'{api_root}/users/{user_id}/id').json()
        if 'error' in resp:
            return User({})
        return User(resp['user'])
    except Exception as e:

        print(f'Error at get {api_root}/users/{user_id}/id: {e}')
    return User({})


def register_resources():
    api.add_resource(users_resource.UsersResource, '/api/v1/users/<user_login>')
    api.add_resource(users_resource.UsersByIDResource, '/api/v1/users/<int:user_id>/id')
    api.add_resource(users_resource.UsersListResource, '/api/v1/users')
    api.add_resource(users_resource.UsersCheckPasswordResource, '/api/v1/users/<user_login>/check_password')
    api.add_resource(users_resource.UsersSubscribeResource, '/api/v1/users/<user_login>/subscribe')
    api.add_resource(users_resource.UsersUnsubscribeResource, '/api/v1/users/<user_login>/unsubscribe')


def register_blueprints():
    app.register_blueprint(pages.pages_blueprint)
    app.register_blueprint(login.login_blueprint)
    app.register_blueprint(commands.commands_blueprint)


if __name__ == '__main__':
    db_session.global_init('sqlite', 'db/screatter.db')  # driver://user:pass@localhost/dbname
    register_resources()
    register_blueprints()
    app.run(port=8080, host='127.0.0.1')

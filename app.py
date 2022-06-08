from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from api import users_resource, posts_resource
from data import db_session
from data.tables import normalization
from blueprints import pages, login, commands
from entitis.user import User
from consts import api_api_root
from util.api_requests import user


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'my_secret_key'


@login_manager.user_loader
def load_user(user_id):
    resp = user(user_id)
    if resp:
        if 'error' in resp:
            return User({})
        return User(resp['user'])
    return User({})


def register_resources():
    api.add_resource(users_resource.UsersByIDResource, f'{api_api_root}/users/<int:user_id>')
    api.add_resource(users_resource.UsersResource, f'{api_api_root}/users/<user_login>')
    api.add_resource(users_resource.UsersListResource, f'{api_api_root}/users')
    api.add_resource(users_resource.UsersCheckPasswordResource, f'{api_api_root}/users/<user_login>/check_password')
    api.add_resource(users_resource.UsersFollowingResource, f'{api_api_root}/users/<user_login>/following')
    api.add_resource(users_resource.UsersFollowersResource, f'{api_api_root}/users/<user_login>/followers')
    api.add_resource(users_resource.UsersLikesResource, f'{api_api_root}/users/<user_login>/likes')

    api.add_resource(posts_resource.PostsResource, f'{api_api_root}/posts/<int:post_id>')
    api.add_resource(posts_resource.PostsListResource, f'{api_api_root}/posts')
    for i in api.resources:
        print(i)


def register_blueprints():
    app.register_blueprint(pages.pages_blueprint)
    app.register_blueprint(login.login_blueprint)
    app.register_blueprint(commands.commands_blueprint)


if __name__ == '__main__':
    db_session.global_init('sqlite', 'db/screatter.db')  # driver://user:pass@localhost/dbname
    normalization()
    register_resources()
    register_blueprints()
    app.run(debug=False)

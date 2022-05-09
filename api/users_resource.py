from flask import jsonify
from flask_restful import Resource, abort
from datetime import datetime
from data import db_session
from data.tables import User
from api import parsers


class UsersByIDResource(Resource):
    @staticmethod
    def get(user_id):
        db = db_session.create_session()
        user = db.query(User).get(user_id)
        if not user:
            db.close()
            abort(404, error='User is not found')
        user = user.to_dict(
                only=('id', 'login', 'email', 'first_name', 'last_name', 'modified_date',
                      'birthday', 'register_date', 'name', 'profile_photo', 'likes.id', 'retweets.parent_id',
                      'comments.parent_id',
                      'read.id', 'read.login', 'read.name', 'read.profile_photo',
                      'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo'))
        db.close()
        return jsonify({
            'user': user
        })


class UsersResource(Resource):
    @staticmethod
    def get(user_login):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            abort(404, error='User is not found')
        user = user.to_dict(
                only=('id', 'login', 'email', 'first_name', 'last_name', 'modified_date',
                      'birthday', 'register_date', 'name', 'profile_photo', 'description',
                      'read.id', 'read.login', 'read.name', 'read.profile_photo',
                      'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo'))
        db.close()
        return jsonify({
            'user': user
        })

    @staticmethod
    def delete(user_login):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')
        db.delete(user)
        db.commit()
        db.close()
        return jsonify({'success': True})

    @staticmethod
    def put(user_login):
        db = db_session.create_session()
        json = parsers.user_put_parser.parse_args()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        if json['login']:
            u = db.query(User).filter(User.login == json['login']).first()
            if u:
                db.close()
                return abort(412, error='Login already in use')
            user.name = json['login']

        if json['email']:
            user.surname = json['email']
        if json['first_name']:
            user.age = json['first_name']
        if json['last_name']:
            user.position = json['last_name']
        if json['birthday']:
            user.modified_date = datetime.strptime(json['birthday'], '%Y-%m-%d %H:%M:%S.%f')
        if json['password']:
            user.set_password(json['password'])
        if json['name']:
            user.set_password(json['name'])

        if any(json.values()):
            user.modified_date = datetime.now()

        db = db_session.create_session()
        db.add(user)
        db.commit()
        db.close()

        return jsonify({
            'success': True,
            'user': user.to_dict(only=('id', 'login', 'email', 'first_name', 'last_name', 'modified_date',
                                       'birthday', 'register_date', 'name', 'profile_photo',
                                       'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo'))
        })


class UsersListResource(Resource):
    @staticmethod
    def get():
        db = db_session.create_session()
        users = db.query(User).all()
        users = list(map(lambda x: x.to_dict(only=('id', 'login', 'name', 'description', 'profile_photo')), users))
        db.close()
        return jsonify({
            'users': users
        })

    @staticmethod
    def post():
        json = parsers.user_post_parser.parse_args()
        db = db_session.create_session()
        user = db.query(User).filter(User.login == json['login']).first()
        if user:
            db.close()
            return abort(412, error='Login already in use')

        user = User()
        user.login = json['login']
        user.email = json['email']
        user.first_name = json['first_name']
        user.last_name = json['last_name']
        user.birthday = datetime.strptime(json['birthday'], '%Y-%m-%d')
        user.set_password(json['password'])
        user.modified_date = datetime.now()
        user.register_date = datetime.now()
        user.name = json['login']
        if json['name']:
            user.name = json['name']
        db.add(user)
        db.commit()
        user = user.to_dict(
            only=('id', 'login', 'email', 'first_name', 'last_name', 'modified_date',
                  'birthday', 'register_date', 'name', 'profile_photo',
                  'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo'))
        db.close()
        return jsonify({
            'success': True,
            'user': user
        })


class UsersCheckPasswordResource(Resource):
    @staticmethod
    def post(user_login):
        json = parsers.user_password_parser.parse_args()

        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()

        if not user:
            db.close()
            return abort(404, error='User is not found')
        if not user.check_password(json['password']):
            db.close()
            return abort(404, error='Incorrect password')
        user = user.to_dict(only=('id', 'login', 'email', 'first_name', 'last_name', 'modified_date',
                                  'birthday', 'register_date', 'name', 'profile_photo',
                                  'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo',
                                  'readers.id', 'readers.login', 'readers.name', 'readers.profile_photo'))
        db.close()
        return jsonify({
            'success': True,
            'user': user
        })


class UsersSubscribeResource(Resource):
    @staticmethod
    def put(user_login):
        json = parsers.user_subscribe_parser.parse_args()
        if user_login == json['target_user_login']:
            return abort(412, error='Users match')

        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        target_user = db.query(User).filter(User.login == json['target_user_login']).first()
        if not target_user:
            db.close()
            return abort(404, error='Target user is not found')

        if target_user in user.read:
            db.close()
            return jsonify({'success': True})

        user.read.append(target_user)
        db.commit()
        db.close()
        return jsonify({'success': True})


class UsersUnsubscribeResource(Resource):
    @staticmethod
    def put(user_login):
        json = parsers.user_subscribe_parser.parse_args()

        if user_login == json['target_user_login']:
            return abort(412, error='Users match')

        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        target_user = db.query(User).filter(User.login == json['target_user_login']).first()
        if not target_user:
            db.close()
            return abort(404, error='Target user is not found')

        if target_user not in user.read:
            db.close()
            return jsonify({'success': True})

        user.read.remove(target_user)
        db.commit()
        db.close()
        return jsonify({'success': True})

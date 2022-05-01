from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('login', required=True, type=str)
user_post_parser.add_argument('email', required=True, type=str)
user_post_parser.add_argument('first_name', required=False, type=str)
user_post_parser.add_argument('last_name', required=False, type=str)
user_post_parser.add_argument('name', required=False, type=str)
user_post_parser.add_argument('birthday', required=True, type=str)
user_post_parser.add_argument('password', required=True, type=str)

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument('login', required=False, type=str)
user_post_parser.add_argument('email', required=False, type=str)
user_post_parser.add_argument('first_name', required=False, type=str)
user_post_parser.add_argument('last_name', required=False, type=str)
user_post_parser.add_argument('birthday', required=False, type=str)
user_post_parser.add_argument('password', required=False, type=str)
user_post_parser.add_argument('name', required=False, type=str)

user_password_parser = reqparse.RequestParser()
user_password_parser.add_argument('password', required=True, type=str)

user_subscribe_parser = reqparse.RequestParser()
user_subscribe_parser.add_argument('target_user_login', required=True, type=str)

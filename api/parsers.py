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
user_put_parser.add_argument('email', required=False, type=str)
user_put_parser.add_argument('first_name', required=False, type=str)
user_put_parser.add_argument('last_name', required=False, type=str)
user_put_parser.add_argument('birthday', required=False, type=str)
user_put_parser.add_argument('password', required=False, type=str)
user_put_parser.add_argument('name', required=False, type=str)
user_put_parser.add_argument('description', required=False, type=str)
user_put_parser.add_argument('profile_photo', required=False, type=str)

user_password_parser = reqparse.RequestParser()
user_password_parser.add_argument('password', required=True, type=str)

user_follow_parser = reqparse.RequestParser()
user_follow_parser.add_argument('target_user_login', required=True, type=str)

user_like_parser = reqparse.RequestParser()
user_like_parser.add_argument('target_post_id', required=True, type=int)

post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument('user_login', required=True, type=str)
post_post_parser.add_argument('parent_id', required=False, type=int)
post_post_parser.add_argument('post', required=True, type=bool)
post_post_parser.add_argument('content', required=False, type=str)
post_post_parser.add_argument('photo', required=False, type=str)

post_list_parser = reqparse.RequestParser()
post_list_parser.add_argument('parent_id', required=False, type=int)
post_list_parser.add_argument('user_id', required=False, type=int)
post_list_parser.add_argument('post', required=False, type=str)
post_list_parser.add_argument('for_user_id', required=False, type=int)
post_list_parser.add_argument('substring', required=False, type=str)

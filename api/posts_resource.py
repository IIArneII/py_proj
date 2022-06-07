from flask import jsonify, request
from flask_restful import Resource, abort
from datetime import datetime
from data import db_session
from data.tables import Post, User, Readership
from api import parsers


class PostsResource(Resource):
    @staticmethod
    def get(post_id):
        db = db_session.create_session()
        post = db.query(Post).get(post_id)
        if not post:
            db.close()
            abort(404, error='Post is not found')

        post = post.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date',
                  'comments_count', 'likes_count', 'retweets_count',
                  'author.id', 'author.login', 'author.name', 'author.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes_count', 'parent.comments_count', 'parent.retweets_count',
                  'parent.author.id', 'parent.author.login', 'parent.author.name', 'parent.author.profile_photo'))
        db.close()
        return jsonify({
            'success': True,
            'post': post
        })


class PostsListResource(Resource):
    @staticmethod
    def get():
        json = request.args
        print(json)
        db = db_session.create_session()

        query = db.query(Post)
        if json.get('for_user_id'):
            query = query.join(Readership, Post.user_id == Readership.c.user_id, isouter=True).filter(
                (Readership.c.reader_id == json['for_user_id']) | (Post.user_id == json['for_user_id']))
        if json.get('parent_id'):
            query = query.filter(Post.parent_id == json['parent_id'])
        if json.get('substring'):
            query = query.filter(Post.content.ilike(f'%{json["substring"]}%'))
        if json.get('user_id'):
            query = query.filter(Post.user_id == json['user_id'])
        if json.get('post') == 'post':
            query = query.filter(Post.post == True)
        elif json.get('post') == 'comment':
            query = query.filter(Post.post == False)
        elif json.get('post') == 'post_and_comment':
            query = query.filter(Post.content != '', Post.photo != None)
        posts = query.order_by(Post.publication_date.desc()).all()
        print(query)

        posts = list(map(lambda x: x.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date',
                  'comments_count', 'likes_count', 'retweets_count',
                  'author.id', 'author.login', 'author.name', 'author.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes_count', 'parent.comments_count', 'parent.retweets_count',
                  'parent.author.id', 'parent.author.login', 'parent.author.name', 'parent.author.profile_photo')),
                         posts))

        db.close()
        return jsonify({
            'success': True,
            'posts': posts
        })

    @staticmethod
    def post():
        json = parsers.post_post_parser.parse_args()

        db = db_session.create_session()
        user = db.query(User).filter(User.login == json['user_login']).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        if json['parent_id']:
            parent = db.query(Post).get(json['parent_id'])
            if not parent:
                db.close()
                return abort(404, error='Parent post is not found')
            if json['post']:
                parent.retweets_count += 1
            else:
                parent.comments_count += 1

        post = Post()
        post.user_id = user.id
        post.parent_id = json['parent_id']
        post.post = json['post']
        post.content = json['content']
        post.photo = json['photo']
        post.publication_date = datetime.now()
        db.add(post)
        db.commit()

        post = post.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date',
                  'comments_count', 'likes_count', 'retweets_count',
                  'author.id', 'author.login', 'author.name', 'author.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes_count', 'parent.comments_count', 'parent.retweets_count',
                  'parent.author.id', 'parent.author.login', 'parent.author.name', 'parent.author.profile_photo'))

        db.close()
        return jsonify({
            'success': True,
            'post': post
        })

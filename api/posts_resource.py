from flask import jsonify
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
            only=('id', 'post', 'content', 'photo', 'publication_date', 'likes', 'comments', 'retweets',
                  'user.id', 'user.login', 'user.name', 'user.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes', 'parent.comments', 'parent.retweets',
                  'parent.user.id', 'parent.user.login', 'parent.user.name',
                  'parent.user.profile_photo'))
        db.close()
        return jsonify({
            'post': post
        })


class PostsUserResource(Resource):
    @staticmethod
    def get(user_login):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        posts = user.posts
        posts = list(map(lambda x: x.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date', 'likes', 'comments', 'retweets',
                  'user.id', 'user.login', 'user.name', 'user.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes', 'parent.comments', 'parent.retweets',
                  'parent.user.id', 'parent.user.login', 'parent.user.name',
                  'parent.user.profile_photo')), posts))

        db.close()
        return jsonify({
            'success': True,
            'post': posts
        })

    @staticmethod
    def post(user_login):
        db = db_session.create_session()
        json = parsers.post_post_parser.parse_args()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        if json['parent_id']:
            parent = db.query(Post).get(json['parent_id'])
            if not parent:
                db.close()
                return abort(404, error='Parent post is not found')
            if json['post']:
                parent.retweets += 1
            else:
                parent.comments += 1

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
            only=('id', 'post', 'content', 'photo', 'publication_date', 'likes',
                  'user.id', 'user.login', 'user.name', 'user.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.user.id', 'parent.user.login', 'parent.user.name',
                  'parent.user.profile_photo')) | {'comments': len(post.children)}

        db.close()
        return jsonify({
            'success': True,
            'post': post
        })


class PostLikeResource(Resource):
    @staticmethod
    def put(user_login, post_id):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')
        post = db.query(Post).get(post_id)
        if not post:
            db.close()
            return abort(404, error='Post is not found')

        if post in user.likes:
            db.close()
            return jsonify({'success': True})

        user.likes.append(post)
        post.likes += 1
        db.commit()
        db.close()
        return jsonify({'success': True})


class PostUnlikeResource(Resource):
    @staticmethod
    def put(user_login, post_id):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')
        post = db.query(Post).get(post_id)
        if not post:
            db.close()
            return abort(404, error='Post is not found')

        if post not in user.likes:
            db.close()
            return jsonify({'success': True})

        user.likes.remove(post)
        post.likes -= 1
        db.commit()
        db.close()
        return jsonify({'success': True})


class PostsUserLikesResource(Resource):
    @staticmethod
    def get(user_login):
        db = db_session.create_session()
        user = db.query(User).filter(User.login == user_login).first()
        if not user:
            db.close()
            return abort(404, error='User is not found')

        likes = user.likes
        posts = list(map(lambda x: x.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date', 'likes',
                  'user.id', 'user.login', 'user.name', 'user.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.user.id', 'parent.user.login', 'parent.user.name',
                  'parent.user.profile_photo')) | {'comments': len(x.children)}, likes))

        db.close()
        return jsonify({
            'success': True,
            'post': posts
        })


class PostsListResource(Resource):
    @staticmethod
    def get():
        json = parsers.post_list_parser.parse_args()
        db = db_session.create_session()

        query = db.query(Post)
        if json['for_user_id']:
            query = query.join(Readership, Post.user_id == Readership.c.user_id).filter(
                (Readership.c.reader_id == json['for_user_id']) | (Post.user_id == json['for_user_id']))
        if json['parent_id']:
            query = query.filter(Post.parent_id == json['parent_id'])
        if json['user_id']:
            query = query.filter(Post.user_id == json['user_id'])
        if json['post'] == 'post':
            query = query.filter(Post.post == True)
        elif json['post'] == 'comment':
            query = query.filter(Post.post == False)
        posts = query.order_by(Post.publication_date.desc()).all()

        posts = list(map(lambda x: x.to_dict(
            only=('id', 'post', 'content', 'photo', 'publication_date', 'likes', 'comments', 'retweets',
                  'user.id', 'user.login', 'user.name', 'user.profile_photo',
                  'parent.id', 'parent.post', 'parent.photo', 'parent.content', 'parent.publication_date',
                  'parent.likes', 'parent.comments', 'parent.retweets',
                  'parent.user.id', 'parent.user.login', 'parent.user.name',
                  'parent.user.profile_photo')), posts))

        db.close()
        return jsonify({
            'success': True,
            'posts': posts
        })

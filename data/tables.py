from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Table
from sqlalchemy import orm, and_
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from data import db_session
from werkzeug.security import generate_password_hash, check_password_hash

Readership = Table('Readership', db_session.SqlAlchemyBase.metadata,
                   Column('reader_id', ForeignKey('Users.id')),
                   Column('user_id', ForeignKey('Users.id')))

Like = Table('Likes', db_session.SqlAlchemyBase.metadata,
             Column('user_id', ForeignKey('Users.id')),
             Column('post_id', ForeignKey('Posts.id')))


class User(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    modified_date = Column(DateTime, nullable=False, default=datetime.now())
    birthday = Column(Date, nullable=False)
    register_date = Column(DateTime, nullable=False, default=datetime.now())
    profile_photo = Column(String, nullable=False, default='default.jpg')
    description = Column(String, nullable=True)
    following_count = Column(Integer, nullable=False, default=0)
    followers_count = Column(Integer, nullable=False, default=0)

    following = orm.relationship('User', secondary=Readership,
                                 primaryjoin=id == Readership.c.reader_id,
                                 secondaryjoin=id == Readership.c.user_id,
                                 backref='followers_')
    followers = orm.relationship('User', secondary=Readership,
                                 primaryjoin=id == Readership.c.user_id,
                                 secondaryjoin=id == Readership.c.reader_id,
                                 backref='following_')

    posts = orm.relationship("Post", back_populates="author",
                             primaryjoin="and_(User.id == Post.user_id, Post.post == True)")
    retweets = orm.relationship("Post", back_populates="author",
                                primaryjoin="and_(User.id == Post.user_id, Post.post == True, Post.parent_id != None)")
    comments = orm.relationship("Post", back_populates="author",
                                primaryjoin="and_(User.id == Post.user_id, Post.post == False)")
    likes = orm.relationship("Post", secondary=Like)

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, name={self.name})'

    def __str__(self):
        return self.__repr__()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Post(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('Posts.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    post = Column(Boolean, nullable=False)
    content = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    publication_date = Column(DateTime, nullable=False)
    likes_count = Column(Integer, nullable=False, default=0)
    retweets_count = Column(Integer, nullable=False, default=0)
    comments_count = Column(Integer, nullable=False, default=0)

    author = orm.relationship("User", back_populates="posts")
    parent = orm.relationship("Post", remote_side=[id])
    comments = None
    retweets = None

    def __repr__(self):
        return f'Post(id={self.id}, content={self.content})'

    def __str__(self):
        return self.__repr__()


post_alias_1 = orm.aliased(Post)
Post.comments = orm.relationship(post_alias_1,
                                 primaryjoin=and_(Post.id == post_alias_1.parent_id, post_alias_1.post == False))
Post.retweets = orm.relationship(post_alias_1,
                                 primaryjoin=and_(Post.id == post_alias_1.parent_id, post_alias_1.post == True))


def normalization():
    db = db_session.create_session()
    posts = db.query(Post).all()
    for post in posts:
        post.retweets_count = db.query(Post).filter(Post.parent_id == post.id, Post.post == True).count()
        post.comments_count = db.query(Post).filter(Post.parent_id == post.id, Post.post == False).count()
        post.likes_count = db.query(Like).filter(Like.c.post_id == post.id).count()
    users = db.query(User).all()
    for user in users:
        user.following_count = db.query(User).join(Readership, User.id == Readership.c.reader_id).filter(
            User.id == user.id).count()
        user.followers_count = db.query(User).join(Readership, User.id == Readership.c.user_id).filter(
            User.id == user.id).count()
    db.commit()
    db.close()

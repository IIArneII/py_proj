from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Table
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

Readership = Table('Readership', SqlAlchemyBase.metadata,
                   Column('reader_id', ForeignKey('Users.id')),
                   Column('user_id', ForeignKey('Users.id')))


class User(SqlAlchemyBase, SerializerMixin):
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

    read = orm.relationship('User', secondary=Readership,
                            primaryjoin=id == Readership.c.reader_id,
                            secondaryjoin=id == Readership.c.user_id,
                            backref='readers_')
    readers = orm.relationship('User', secondary=Readership,
                               primaryjoin=id == Readership.c.user_id,
                               secondaryjoin=id == Readership.c.reader_id,
                               backref='read_')

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, email={self.name})'

    def __str__(self):
        return self.__repr__()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


# class Post(SqlAlchemyBase, SerializerMixin):
#     __tablename__ = 'Posts'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
#     parent_id = None
#     user_id = None

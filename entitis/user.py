from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, json):
        print(json)
        self.id = json.get('id')
        self.login = json.get('login')
        self.email = json.get('email')
        self.first_name = json.get('first_name')
        self.last_name = json.get('last_name')
        self.name = json.get('name')
        self.modified_date = json.get('modified_date')
        self.birthday = json.get('birthday')
        self.register_date = json.get('register_date')
        self.profile_photo = json.get('profile_photo')
        self.description = json.get('description')
        self.read = json.get('read')
        self.readers = json.get('readers')
        self.likes = json.get('likes')
        self.retweets = json.get('retweets')
        self.comments = json.get('comments')
        if self.read != None:
            self.read_logins = list(map(lambda x: x['login'], self.read))
        else:
            self.read_logins = None
        if self.readers != None:
            self.readers_logins = list(map(lambda x: x['login'], self.readers))
        else:
            self.readers_logins = None
        if self.likes != None:
            self.likes_id = list(map(lambda x: x['id'], self.likes))
        else:
            self.likes_id = None
        if self.retweets != None:
            self.retweets_id = list(map(lambda x: x['parent_id'], self.retweets))
        else:
            self.retweets_id = None
        if self.comments != None:
            self.comments_id = list(map(lambda x: x['parent_id'], self.comments))
        else:
            self.comments_id = None

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, email={self.name})'

    def __str__(self):
        return self.__repr__()

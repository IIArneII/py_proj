from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, json):
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
        self.description = 'Опсиание профиля'
        self.read = json.get('read')
        self.readers = json.get('readers')
        if self.read != None:
            self.read_logins = list(map(lambda x: x['login'], self.read))
        else:
            self.read_logins = None
        if self.readers != None:
            self.readers_logins = list(map(lambda x: x['login'], self.readers))
        else:
            self.readers_logins = None

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, email={self.name})'

    def __str__(self):
        return self.__repr__()

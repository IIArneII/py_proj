from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, json: dict):
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
        self.following = json.get('following')
        self.followers = json.get('followers')
        self.likes = json.get('likes')
        self.retweets = json.get('retweets')
        self.comments = json.get('comments')
        self.following_count = json.get('following_count')
        self.followers_count = json.get('followers_count')

        self.following_logins = None
        if self.following != None:
            self.following_logins = list(map(lambda x: x['login'], self.following))

        self.followers_logins = None
        if self.followers != None:
            self.followers_logins = list(map(lambda x: x['login'], self.followers))

        self.likes_id = None
        if self.likes != None:
            self.likes_id = list(map(lambda x: x['id'], self.likes))

        self.retweets_id = None
        if self.retweets != None:
            self.retweets_id = list(map(lambda x: x['parent_id'], self.retweets))

        self.comments_id = None
        if self.comments != None:
            self.comments_id = list(map(lambda x: x['parent_id'], self.comments))

    def __repr__(self):
        return f'User(id={self.id}, login={self.login})'

    def __str__(self):
        return self.__repr__()

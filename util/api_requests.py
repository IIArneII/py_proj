import requests
from consts import api_root
from datetime import datetime
from typing import Union


def unlike(user_login: str, post_id: int):
    try:
        return requests.delete(f'{api_root}/users/{user_login}/likes', json={
            'target_post_id': post_id
        }).json()
    except Exception as e:
        print(f'Error at delete {api_root}/users/{user_login}/likes: {e}')


def like(user_login: str, post_id: int):
    try:
        return requests.put(f'{api_root}/users/{user_login}/likes', json={
            'target_post_id': post_id
        }).json()
    except Exception as e:
        print(f'Error at put {api_root}/users/{user_login}/likes: {e}')


def subscribe(user_login: str, target_user_login: str):
    try:
        return requests.put(f'{api_root}/users/{user_login}/following', json={
            'target_user_login': target_user_login
        }).json()
    except Exception as e:
        print(f'Error at put {api_root}/users/{user_login}/following: {e}')


def unsubscribe(user_login: str, target_user_login: str):
    try:
        return requests.delete(f'{api_root}/users/{user_login}/following', json={
            'target_user_login': target_user_login
        }).json()
    except Exception as e:
        print(f'Error at delete {api_root}/users/{user_login}/following: {e}')


def check_password(user_login: str, password: str):
    try:
        return requests.post(f'{api_root}/users/{user_login}/check_password',
                             json={'password': password}).json()
    except Exception as e:
        print(f'Error at post {api_root}/users/{user_login}/check_password: {e}')


def register(user_login: str, password: str, email: str, birthday: datetime,
             last_name: str = None, first_name: str = None):
    try:
        return requests.post(f'{api_root}/users', json={
            'login': user_login,
            'password': password,
            'email': email,
            'birthday': str(birthday),
            'last_name': last_name,
            'first_name': first_name
        }).json()
    except Exception as e:
        print(f'Error at post {api_root}/users: {e}')


def new_post(user_login: str, is_post: bool = True, content: str = None, photo: str = None, parent_id: int = None):
    try:
        return requests.post(f'{api_root}/posts', json={
            'user_login': user_login,
            'parent_id': parent_id,
            'post': is_post,
            'content': content,
            'photo': photo
        }).json()
    except Exception as e:
        print(f'Error at post {api_root}/posts: {e}')


def posts(for_user_id: int = None,
          post: str = None,
          user_id: int = None,
          parent_id: int = None,
          substring: str = None):
    try:
        return requests.get(f'{api_root}/posts', params={
            'for_user_id': for_user_id,
            'post': post,
            'user_id': user_id,
            'parent_id': parent_id,
            'substring': substring
        }).json()
    except Exception as e:
        print(f'Error at get {api_root}/posts: {e}')


def post(post_id):
    try:
        return requests.get(f'{api_root}/posts/{post_id}').json()
    except Exception as e:
        print(f'Error at get {api_root}/posts: {e}')


def users():
    try:
        return requests.get(f'{api_root}/users').json()
    except Exception as e:
        print(f'Error at {api_root}/users: {e}')


def user(u: Union[str, int]):
    try:
        return requests.get(f'{api_root}/users/{u}').json()
    except Exception as e:
        print(f'Error at get {api_root}/users/{u}: {e}')


def user_following(user_login: str):
    try:
        return requests.get(f'{api_root}/users/{user_login}/following').json()
    except Exception as e:
        print(f'Error at get {api_root}/users/{user_login}/following: {e}')


def user_followers(user_login: str):
    try:
        return requests.get(f'{api_root}/users/{user_login}/followers').json()
    except Exception as e:
        print(f'Error at get {api_root}/users/{user_login}/followers: {e}')


def user_edit(user_login: str,
              login: str = None,
              name: str = None,
              profile_photo: str = None,
              email: str = None,
              birthday: datetime = None,
              password: str = None,
              description: str = None):
    try:
        return requests.put(f'{api_root}/users/{user_login}', json={
            'login': login,
            'name': name,
            'profile_photo': profile_photo,
            'email': email,
            'birthday': birthday if birthday is None else str(birthday),
            'password': password,
            'description': description
        })
    except Exception as e:
        print(f'Error at put {api_root}/users/{user_login}: {e}')

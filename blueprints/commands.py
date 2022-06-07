from flask import Blueprint, jsonify, abort, request, render_template
from forms.forms import WriterForm, SettingsForm, SearchForm
from flask_login import login_required, current_user
import uuid
from util.photo import save_photo
from distutils.util import strtobool
from util import api_requests


commands_blueprint = Blueprint('commands', __name__, template_folder='templates')


@commands_blueprint.put('/<user_login>/subscribe')
@login_required
def subscribe(user_login):
    if resp := api_requests.subscribe(current_user.login, user_login):
        return jsonify(resp)
    return abort(500)


@commands_blueprint.put('/<user_login>/unsubscribe')
@login_required
def unsubscribe(user_login):
    if resp := api_requests.unsubscribe(current_user.login, user_login):
        return jsonify(resp)
    return abort(500)


@commands_blueprint.put('/<user_login>/<int:post_id>/like')
@login_required
def like(user_login, post_id):
    if resp := api_requests.like(current_user.login, post_id):
        return jsonify(resp)
    return abort(500)


@commands_blueprint.put('/<user_login>/<int:post_id>/unlike')
@login_required
def unlike(user_login, post_id):
    if resp := api_requests.unlike(current_user.login, post_id):
        return jsonify(resp)
    return abort(500)


@commands_blueprint.post('/')
@login_required
def post():
    form = WriterForm()

    photo_name = None
    if request.files['photo']:
        photo_name = str(uuid.uuid4()) + '.jpg'
    parent_id = None
    if form.parent_id.data:
        parent_id = int(form.parent_id.data)

    if resp := api_requests.new_post(current_user.login, strtobool(form.post.data),
                                     form.content.data, photo_name, parent_id):
        if 'error' not in resp and photo_name:
            save_photo(request.files['photo'].read(), 'static/img/' + photo_name)
        return jsonify(resp)

    return abort(500)


@commands_blueprint.post('/settings')
@login_required
def settings():
    form = SettingsForm()

    login = form.login.data if form.login.data != current_user.login else None
    name = form.name.data if form.name.data != current_user.name else None
    profile_photo = str(uuid.uuid4()) + '.jpg' if request.files['profile_photo'] else None
    email = form.email.data if form.email.data != current_user.email else None
    birthday = form.birthday.data if str(form.birthday.data) != current_user.birthday else None

    print(profile_photo)
    print(request.files['profile_photo'])

    if form.password.data != form.password_again.data:
        return render_template('settings.html',
                               title='Настройки',
                               search_form=SearchForm(),
                               writer_form=WriterForm(),
                               settings_form=form,
                               message='Пароли не совпадают')
    password = form.password.data if form.password.data else None

    if resp := api_requests.user_edit(current_user.login, login=login, name=name, profile_photo=profile_photo,
                                      email=email, birthday=birthday, password=password).json():
        if 'error' not in resp:
            if profile_photo:
                save_photo(request.files['profile_photo'].read(), 'static/profile_photos/' + profile_photo, square=True)
            return render_template('settings.html',
                                   title='Настройки',
                                   search_form=SearchForm(),
                                   writer_form=WriterForm(),
                                   settings_form=form)

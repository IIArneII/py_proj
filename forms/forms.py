from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField, SearchField, EmailField, DateField, \
    HiddenField, TextAreaField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    birthday = DateField('День рождения', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Регистрация')


class WriterForm(FlaskForm):
    parent_id = HiddenField()
    post = HiddenField()
    content = TextAreaField()
    photo = FileField()
    submit = SubmitField('Твитт')


class SearchForm(FlaskForm):
    search = SearchField('Запрос')
    submit = SubmitField('Поиск')

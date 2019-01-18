from flask import session
from sqlalchemy.sql.expression import union_all
from marshmallow import fields, post_load
from marshmallow import validate, ValidationError, pre_load
from marshmallow.decorators import validates_schema
from marshmallow_sqlalchemy import field_for
from CTFd.models import ma, Users
from CTFd.utils.validators import unique_email, validate_country_code
from CTFd.utils.user import is_admin, get_current_user
from CTFd.utils.countries import lookup_country_code
from CTFd.utils.crypto import verify_password, hash_password


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Users
        include_fk = True
        dump_only = ('id', 'oauth_id', 'created')
        load_only = ('password',)

    name = field_for(
        Users,
        'name',
        required=True,
        validate=[
            validate.Length(min=1, max=128, error='Название команды не должно быть пустым')
        ]
    )
    email = field_for(
        Users,
        'email',
        validate=[
            validate.Email('Недействительный формат почты'),
            validate.Length(min=1, max=128, error='Адрес электронной почты не должен быть пустым'),
        ]
    )
    website = field_for(
        Users,
        'website',
        validate=validate.URL(
            error='Веб-сайт должен иметь правильный URL-адрес, начинающийся с http или https',
            schemes={'http', 'https'}
        )
    )
    country = field_for(
        Users,
        'country',
        validate=[
            validate_country_code
        ]
    )
    password = field_for(
        Users,
        'password',
        validate=[
            validate.Length(min=1, error='Пароль не должен быть пустым'),
        ]
    )

    @pre_load
    def validate_name(self, data):
        name = data.get('name')
        if name is None:
            return

        existing_user = Users.query.filter_by(name=name).first()
        user_id = data.get('id')

        if user_id and is_admin():
            if existing_user and existing_user.id != user_id:
                raise ValidationError('Имя пользователя уже занято', field_names=['name'])
        else:
            current_user = get_current_user()
            if name == current_user.name:
                return data
            else:
                if existing_user:
                    raise ValidationError('Имя пользователя уже занято', field_names=['name'])

    @pre_load
    def validate_email(self, data):
        email = data.get('email')
        if email is None:
            return

        existing_user = Users.query.filter_by(email=email).first()
        user_id = data.get('id')

        if user_id and is_admin():
            if existing_user and existing_user.id != user_id:
                raise ValidationError('Данный адрес электронной почты уже используется', field_names=['email'])
        else:
            current_user = get_current_user()
            if email == current_user.email:
                return data
            else:
                if existing_user:
                    raise ValidationError('Данный адрес электронной почты уже используется', field_names=['email'])

    @pre_load
    def validate_password_confirmation(self, data):
        password = data.get('password')
        confirm = data.get('confirm')
        target_user = get_current_user()
        user_id = data.get('id')

        if is_admin():
            pass
        else:
            if password and (confirm is None):
                raise ValidationError('Пожалуйста, подтвердите ваш текущий пароль', field_names=['confirm'])

            if password and confirm:
                test = verify_password(plaintext=confirm, ciphertext=target_user.password)
                if test is True:
                    return data
                else:
                    raise ValidationError('Ваш текущий пароль неверен', field_names=['confirm'])

    views = {
        'user': [
            'website',
            'name',
            'country',
            'affiliation',
            'bracket',
            'id',
            'oauth_id',
        ],
        'self': [
            'website',
            'name',
            'email',
            'country',
            'affiliation',
            'bracket',
            'id',
            'oauth_id',
            'password'
        ],
        'admin': [
            'website',
            'name',
            'created',
            'country',
            'banned',
            'email',
            'affiliation',
            'secret',
            'bracket',
            'hidden',
            'id',
            'oauth_id',
            'password',
            'type',
            'verified'
        ]
    }

    def __init__(self, view=None, *args, **kwargs):
        if view:
            if type(view) == str:
                kwargs['only'] = self.views[view]
            elif type(view) == list:
                kwargs['only'] = view

        super(UserSchema, self).__init__(*args, **kwargs)

import warnings
import  uuid

from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
    except:
        username_field = 'username'

    return username_field

def get_username(user):
    try:
        username = user.get_username()

    except AttributeError:
        username = user.get_username

    return username

def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'This following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
    }
    if isinstance(user.pk, uuid.UUID):
        payload['id'] = str(user.pk)

    payload['role'] = user.role.name
    payload['team'] = user.team.pk

    payload[username_field] = username

    return payload

class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    team = models.IntegerField()
    role = models.CharField(max_length=255)
    exp = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'username'

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return True if self.role == 'admin' else False


class MicroServerJSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate_credentials(self, payload):
        user = User(**payload)
        user.save()
        return user


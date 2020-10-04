import requests
from django.core.files.base import ContentFile


def fill_user_model(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        if "picture" in response.keys():
            img = response["picture"]
            # тут сделать сохранение в user
    user.save()

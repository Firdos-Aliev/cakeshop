from urllib.request import urlopen

import requests
from django.core.files.base import ContentFile


def fill_user_model(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        if "picture" in response.keys():
            img = response["picture"]
            user.img.save(f'avatar_{user.username}.jpg', ContentFile(urlopen(img).read()))
    user.save()

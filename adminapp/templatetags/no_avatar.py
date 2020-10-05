from django import template
from django.conf import settings

register = template.Library()


def check_img(img):
    if img == '':
        img = 'user_img/no_user.png'
    return f'{img}'


register.filter("avatar", check_img)

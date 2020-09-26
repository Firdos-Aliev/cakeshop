from django.core.management.base import BaseCommand
from authapp.models import CakeShopUser

import json, os

JSON_PATH = 'mainapp/dumps'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:# открываем файл, если он сущесвует
        return json.load(infile)# делаем модель Json


class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = CakeShopUser.objects.create_superuser(username='django', password='geekbrains', email='email@gamil.com')
        print("test")


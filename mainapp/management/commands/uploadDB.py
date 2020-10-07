from django.core.management.base import BaseCommand
from mainapp.models import Catalog, Product
from authapp.models import CakeShopUser
import json, os

JSON_PATH = 'json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:  # открываем файл, если он сущесвует
        return json.load(infile)  # делаем модель Json


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('catalog')

        Catalog.objects.all().delete()
        for category in categories:
            new_category = Catalog(**category['fields'], pk=category['pk'])
            new_category.save()

        products = load_from_json('product')

        Product.objects.all().delete()
        for product in products:
            category_id = product['fields']['category']
            catalog_obj = Catalog.objects.get(id=category_id)
            product['fields']['category'] = catalog_obj
            new_product = Product(**product['fields'], pk=product['pk'])
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        CakeShopUser.objects.all().delete()
        super_user = CakeShopUser.objects.create_superuser(username='django', password='geekbrains', email='')
        user = CakeShopUser.objects.create_user(username='user', password='geekbrains', email='')
        print("Данные успешно загружены")

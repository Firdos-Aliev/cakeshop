from random import choice

from django.shortcuts import render, get_object_or_404
from mainapp.models import Catalog, Product


# все контролеры
# относительно папки шаблонов соответсвуещего приложения

def rand_product():
    return choice(Product.objects.all())


def index(request):
    # print("index:", request.resolver_match.url_name) тут находим для request.resolver_match.url_name для active
    print(request)

    content = {
        "main_title": "главная",
        'product': rand_product(),
    }
    return render(request, 'mainapp/index.html', content)


def contacts(request):
    content = {
        "main_title": "контакты",
    }
    return render(request, 'mainapp/contacts.html', content)


def catalog(request):  # например пришел pk=1 (торты)
    catalogs = Catalog.objects.all()  # тут есть поле pk, которое мы передаем

    content = {
        "main_title": "каталог",
        "catalogs": catalogs,
    }
    return render(request, 'mainapp/catalog.html', content)


def products(request, pk):
    category = get_object_or_404(Catalog, pk=pk)
    products = Product.objects.filter(category=category)
    content = {
        "main_title": category.name,
        "products": products
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    content = {
        "main_title": product.name,
        "product": product
    }
    return render(request, 'mainapp/product.html', content)

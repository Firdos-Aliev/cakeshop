from random import choice

from django.shortcuts import render, get_object_or_404

from cakeshop import settings
from django.core.cache import cache

from mainapp.models import Catalog, Product


# все контролеры
# относительно папки шаблонов соответсвуещего приложения

def get_product_list():
    if settings.LOW_CACHE:
        key = 'products'
        product_list = cache.get(key)
        if product_list is None:
            product_list = Product.objects.filter(is_active=True).select_related()
            cache.set(key, product_list)
        return product_list
    else:
        return Product.objects.filter(is_active=True).select_related()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk, is_active=True)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk, is_active=True)


def get_catalog(pk):
    if settings.LOW_CACHE:
        key = f'catalog{pk}'
        catalog = cache.get(key)
        if catalog is None:
            catalog = Catalog.objects.filter(is_active=True, pk=pk).first()
            cache.set(key, catalog)
        return catalog
    else:
        return Catalog.objects.filter(is_active=True, pk=pk).first()


def get_catalog_list():
    if settings.LOW_CACHE:
        key = 'catalog'
        catalog_list = cache.get(key)
        if catalog_list is None:
            catalog_list = Catalog.objects.filter(is_active=True).select_related()
            cache.set(key, catalog_list)
        return catalog_list
    else:
        return Catalog.objects.filter(is_active=True).select_related()


def rand_product():
    return choice(get_product_list())


def index(request):
    # print("index:", request.resolver_match.url_name) тут находим для request.resolver_match.url_name для active
    # print(request)
    # print(rand_product()) при вызове метода появляется дуаликат, ведь мы 2 раза делем запрос
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
    catalogs = get_catalog_list()  # тут есть поле pk, которое мы передаем

    content = {
        "main_title": "каталог",
        "catalogs": catalogs,
    }
    return render(request, 'mainapp/catalog.html', content)


def products(request, pk):
    category = get_catalog(pk)
    products = Product.objects.filter(category=category, is_active=True)
    content = {
        "main_title": category.name,
        "products": products
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    product = get_product(pk)
    content = {
        "main_title": product.name,
        "product": product
    }
    return render(request, 'mainapp/product.html', content)

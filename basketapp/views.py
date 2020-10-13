from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def index(request):
    products = request.user.basket_set.select_related('product').all()

    content = {
        "main_title": "корзина",
        "basket_products": products
    }

    return render(request, 'basketapp/index.html', content)


@login_required
def new_product(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if basket is None:
        basket = Basket(user=request.user, product=product)

    basket.count += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # на предыдущую


@login_required
def add(request, pk, count):
    if request.is_ajax():
        basket_product = Basket.objects.filter(pk=pk).first()
        basket_product.count += 1
        basket_product.save()

    basket_products = request.user.basket_set.all()
    context = {
        'main_title': "увеличить количество",
        'basket_products': basket_products,
    }

    basket_list = loader.render_to_string(
        'basketapp/includes/inc__basket_list.html',
        context=context,
        request=request,  # для csrf token (безопастность)
    )

    return JsonResponse({
        'basket_list': basket_list,
    })


@login_required
def pop(request, pk, count):
    if request.is_ajax():
        basket_product = Basket.objects.filter(pk=pk).first()
        if basket_product.count == 1:
            basket_product.delete()
        else:
            basket_product.count -= 1
            basket_product.save()

    basket_products = request.user.basket_set.all()
    context = {
        'main_title': "уменьшить количество",
        'basket_products': basket_products,
    }

    basket_list = loader.render_to_string(
        'basketapp/includes/inc__basket_list.html',
        context=context,
        request=request,  # для csrf token (безопастность)
    )

    return JsonResponse({
        'basket_list': basket_list,
    })
from django.db import models
from authapp.models import CakeShopUser
from mainapp.models import Product
import datetime


class Basket(models.Model):
    user = models.ForeignKey(CakeShopUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь')  # можно вместо пользователя сделать get_user_model()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(default=0, verbose_name="Количество")
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

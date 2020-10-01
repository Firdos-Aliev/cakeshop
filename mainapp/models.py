from django.db import models


# модели для миграция (БД)

class Catalog(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64, null=True)
    text = models.TextField(verbose_name='Описание', blank=True)
    img = models.ImageField(verbose_name='Картинка', upload_to="catalog_img", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(verbose_name='Название', max_length=64, null=True)
    text = models.TextField(verbose_name='Описание', blank=True)
    img = models.ImageField(verbose_name='Картинка', upload_to="product_img", blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=6,decimal_places=2, null=False, default=0)
    count = models.IntegerField(default=0, verbose_name="Количество")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

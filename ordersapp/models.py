from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    PAID = 'P'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    @cached_property
    def order_items(self):
        return self.orderitem_set.all()

    def get_total_sum(self):
        # order = self.orderitem_set.all() # каждая модкль поучить свой заказ
        sum = 0
        for i in self.order_items:
            sum += i.product.price * i.quantity
        return sum

    def get_items_count(self):
        count = 0
        for i in self.order_items:
            count += i.quantity
        return count


class OrderItem(models.Model):
    # related_name я обратной связи по ключю orederitem_set
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # related_name="items"
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

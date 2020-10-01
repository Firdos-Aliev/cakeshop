from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class PageMainTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):  # для измениния контекста
        data = super().get_context_data(object_list=None, **kwargs)
        data['main_title'] = self.main_title
        return data


class UsersOrderMixin:
    def get_queryset(self):  # для получения request
        return Order.objects.filter(user=self.request.user)


class OrdersRead(PageMainTitleMixin, UsersOrderMixin, ListView):
    main_title = "заказ"
    model = Order


class OrderCreate(PageMainTitleMixin, CreateView):
    main_title = "создать заказ"
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:list")

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            form_set = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket = self.request.user.basket_set.all()
            # basket = Basket.objects.filter(user = self.request.user)
            if len(basket) > 0:
                # это класс для списка форм
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket))
                # обьект списка форм
                form_set = OrderFormSet()
                for i in range(len(basket)):
                    form_set.forms[i].initial['product'] = basket[i].product
                    form_set.forms[i].initial['quantity'] = basket[i].count
            else:
                form_set = OrderFormSet()
        # передаем в контекст
        data['order_form_set'] = form_set
        # print(data['order_form_set'])
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_item = context['order_form_set']

        with transaction.atomic():
            # self.object = form.save() erorr user = NONE
            # print(self.request.user)
            # print("____________________________________________")
            form.instance.user = self.request.user
            # print(form)
            self.object = form.save()
            if order_item.is_valid():
                order_item.instance = self.object
                order_item.save()
            self.request.user.basket_set.all().delete()
            return super().form_valid(form)


class OrderDetail(PageMainTitleMixin, DetailView):
    main_title = "просмотреть заказ"
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        #print("____________________________________________")
        order = data['object']
        order_item = OrderItem.objects.filter(order=order)
        #print(order_item)
        data['object_list'] = order_item
        #print(data['object'])
        return data
    # def get_queryset(self):  # для получения request
    # order = get_object_or_404(Order, pk=pk)
    # order_items = OrderItem.objects.filter(order=order)
    # return order_items


def orderItemRead(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    content = {
        "main_title": "Заказ " + pk,
        "object_list": order_items
    }
    return render(request, 'ordersapp/order_detail.html', content)

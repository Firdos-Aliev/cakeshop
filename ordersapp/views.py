from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class OptimizationQueriesMixin:
    def get_queryset(self):
        return Order.objects.select_related().all()


class OrdersRead(PageMainTitleMixin, UsersOrderMixin, LoginRequiredMixin, ListView):
    main_title = "заказ"
    model = Order


class OrderCreate(PageMainTitleMixin, LoginRequiredMixin, CreateView):
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
            basket = self.request.user.basket_set.select_related().all()
            # basket = Basket.objects.filter(user = self.request.user)
            if len(basket) > 0:
                # это класс для списка форм
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket))
                # обьект списка форм
                form_set = OrderFormSet()
                for i in range(len(basket)):
                    form_set.forms[i].initial['product'] = basket[i].product
                    form_set.forms[i].initial['quantity'] = basket[i].count
                    form_set.forms[i].initial['price'] = basket[i].product.price
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


class OrderDetail(PageMainTitleMixin, LoginRequiredMixin, DetailView):
    main_title = "просмотреть заказ"
    model = Order


#  исправил по законам фреймворка
#    def get_context_data(self, *, object_list=None, **kwargs):
#        data = super().get_context_data(object_list=None, **kwargs)
#        order = data['object']
#        order_item = OrderItem.objects.filter(order=order)
#        data['object_list'] = order_item
#        # print(data['object'])
#        return data
# def get_queryset(self):  # для получения request
# order = get_object_or_404(Order, pk=pk)
# order_items = OrderItem.objects.filter(order=order)
# return order_items


class OrderUpdate(PageMainTitleMixin, LoginRequiredMixin, UpdateView):
    main_title = "изменить заказ"
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:list")

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.method == 'POST':
            form_set = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object
                                    )
        else:
            form_set = OrderFormSet(instance=self.object)
            for form in form_set.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                else:
                    form.initial['price'] = 0
        data['order_form_set'] = form_set

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['order_form_set']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        return super().form_valid(form)


class OrderDelete(PageMainTitleMixin, LoginRequiredMixin, DeleteView):
    main_title = "Отмена заказа"
    model = Order
    success_url = reverse_lazy("orders:list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.status = self.object.CANCEL

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def order_confirm(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.PAID
    order.save()

    return HttpResponseRedirect(reverse('orders:list'))

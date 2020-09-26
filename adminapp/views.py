from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserRegisterForm, AdminShopUserChangeForm
from mainapp.forms import CatalogCreateForm, CatalogChangeForm, ProductCreateForm, ProductChangeForm
from mainapp.models import Catalog, Product


def user_check(user):
    return user.is_superuser


@user_passes_test(user_check)
def users(request):
    user_list = get_user_model().objects.all()

    content = {
        "main_title": "Пользователи админка",
        "users": user_list
    }

    return render(request, "adminapp/users.html", content)


@user_passes_test(user_check)
def user_create(request):
    if request.method == "POST":
        form = AdminShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:user'))
    else:
        form = AdminShopUserRegisterForm()
    content = {
        'title': "регистрация пользователя",
        "button_title": "создать",
        'form': form
    }

    return render(request, 'adminapp/form.html', content)


@user_passes_test(user_check)
def user_change(request, pk):
    # возвращает список с фильтвром, а нам нужен обьект так что берем первый
    user_obj = get_user_model().objects.filter(pk=pk).first()
    if request.method == "POST":
        form = AdminShopUserChangeForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = AdminShopUserChangeForm(instance=user_obj)
    content = {
        'title': "профиль пользователя",
        "button_title": "изменить",
        'form': form
    }

    return render(request, 'adminapp/form.html', content)


@user_passes_test(user_check)
def user_delete(request, pk):
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), pk=pk)
        user.is_active = False
        user.save()
    return HttpResponseRedirect(reverse('adminapp:users'))


@user_passes_test(user_check)
def catalogs(request):
    catalog_list = Catalog.objects.all()

    content = {
        "main_title": "Каталоги админка",
        "catalogs": catalog_list
    }

    return render(request, "adminapp/catalogs.html", content)


@user_passes_test(user_check)
def catalog_create(request):
    if request.method == "POST":
        form = CatalogCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:catalogs'))
    else:
        form = CatalogCreateForm()

    content = {
        "main_title": "новый каталог админка",
        "button_title": "создать",
        "form": form,
    }
    return render(request, "adminapp/form.html", content)


@user_passes_test(user_check)
def catalog_change(request, pk):
    catalog = Catalog.objects.filter(pk=pk).first()
    if request.method == "POST":
        form = CatalogChangeForm(request.POST, request.FILES, instance=catalog)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:catalogs'))
    else:
        form = CatalogChangeForm(instance=catalog)

    content = {
        "main_title": "профиль каталога админка",
        "button_title": "изменить",
        "form": form,
    }
    return render(request, "adminapp/form.html", content)


@user_passes_test(user_check)
def catalog_delete(request, pk):
    Catalog.objects.filter(pk=pk).first().delete()
    return HttpResponseRedirect(reverse('adminapp:catalogs'))


@user_passes_test(user_check)
def products(request):
    product_list = Product.objects.all()

    content = {
        "main_title": "продукты",
        'products': product_list,
    }

    return render(request, "adminapp/products.html", content)


@user_passes_test(user_check)
def product_create(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products'))
    else:
        form = ProductCreateForm()

    content = {
        "main_title": "новый продукт админка",
        "button_title": "создать",
        "form": form,
    }
    return render(request, "adminapp/form.html", content)


@user_passes_test(user_check)
def product_change(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if request.method == "POST":
        form = ProductChangeForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products'))
    else:
        form = ProductChangeForm(instance=product)

    content = {
        "main_title": "профиль продукта админка",
        "button_title": "изменить",
        "form": form,
    }
    return render(request, "adminapp/form.html", content)


@user_passes_test(user_check)
def product_delete(request, pk):
    product = Product.objects.filter(pk=pk).first().delete()
    return HttpResponseRedirect(reverse('adminapp:products'))


class SuperUserClassMixin:
    @method_decorator(user_passes_test(user_check))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageMainTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['main_title'] = self.main_title
        return data


class PageButtonTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['button_title'] = self.button_title
        return data


class UsersRead(SuperUserClassMixin, PageMainTitleMixin, ListView):
    main_title = "Users Read"
    model = get_user_model()
    paginate_by = 1


class UsersList(SuperUserClassMixin, PageMainTitleMixin, ListView):
    main_title = "Users Read"
    model = get_user_model()


class UserDetail(SuperUserClassMixin, PageMainTitleMixin, DetailView):
    main_title = "Users Detail"
    model = get_user_model()


class UserCreate(SuperUserClassMixin, PageMainTitleMixin, PageButtonTitleMixin, CreateView):
    main_title = "User Create"
    button_title = "создать"
    model = get_user_model()
    form_class = AdminShopUserRegisterForm

    # success_url = reverse_lazy("adminapp:user_list",kwargs={'pk': 1,}) # не понял почему именновано не могу передать
    success_url = reverse_lazy("adminapp:users", args=[1])
    # потом попробую сделать переход на страницу где был пользоваль (передать нужны пк а не 1)


class UserChange(SuperUserClassMixin, PageMainTitleMixin, PageButtonTitleMixin, UpdateView):
    main_title = "User Change"
    button_title = "изменить"
    model = get_user_model()
    form_class = AdminShopUserChangeForm
    success_url = reverse_lazy("adminapp:users", args=[1])


class UserDelete(SuperUserClassMixin, PageMainTitleMixin, PageButtonTitleMixin, DeleteView):
    main_title = "User Delete"
    button_title = "удалить"
    model = get_user_model()
    success_url = reverse_lazy("adminapp:users", args=[1])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CatalogRead(SuperUserClassMixin, PageMainTitleMixin, ListView):
    main_title = "CatalogRead"
    model = Catalog


class ProductsRead(SuperUserClassMixin, PageMainTitleMixin, ListView):
    main_title = "ProductsRead"
    model = Product
    # paginate_by = 2

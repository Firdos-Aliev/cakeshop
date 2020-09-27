from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm, CakeShopUserProfileForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)  # обьект формы, которую мы создали с собвенными полями
        if form.is_valid():  # при этом данные все валидны для входа
            username = request.POST['username']  # берем данные
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                     password=password)  # создаем обьект пользователя с эго парметрами (логин, пароль)
            if user and user.is_active:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # авторизируемся
                return HttpResponseRedirect(reverse('main:index'))  # должно перекинуть на главную
    else:
        form = ShopUserLoginForm()
    content = {
        "main_title": "авторизация",
        "button_title": "войти",
        "form": form,
    }

    return render(request, "authapp/login.html", content)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == "POST":
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.verification_email()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserRegisterForm()
    content = {
        "main_title": "регистрация",
        "button_title": "зарегестрировать",
        "form": form,
    }
    return render(request, "authapp/register.html", content)


@login_required
def profile(request):
    if request.method == "POST":
        form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        profile = CakeShopUserProfileForm(request.POST, request.FILES, instance=request.user.cakeshopuserprofile)
        if form.is_valid() and profile.is_valid():
            form.save()
            profile.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserChangeForm(instance=request.user)
        profile = CakeShopUserProfileForm(instance=request.user.cakeshopuserprofile)
    print(request.user)
    print("----------------------------------------")
    print(request.user.cakeshopuserprofile)
    content = {
        "main_title": "профиль",
        "button_title": "изменить",
        "form": form,
        "profile": profile
    }
    return render(request, "authapp/profile.html", content)


def verify(request, pk, key):
    global main_title, text
    user = get_user_model().objects.filter(pk=pk).first()
    if user.is_active:
        main_title = "Повторная верификация"
        text = "Вы уже верефицированы"
    if user.valid_activation_key and key == user.activation_key and user.is_active == False:
        user.is_active = True
        user.save()
        main_title = "Успех"
        text = "Вы успешно активировали свой аккаунт"

    content = {
        "main_title": main_title,
        "text": text,
    }
    return render(request, "authapp/verify.html", content)

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as forms

# форма на основе модели
from authapp.models import CakeShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'age', 'img', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''

    def save(self, commit=True):
        user = super().save(commit)
        user.is_active = False
        # salt = user.activation_key можно ли так? задать соль сразу в БД
        user.save()
        # user.save_user_profile()
        # CakeShopUserProfile.objects.create(user=user) # при захоже через google+ не заходит сюда
        return user


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class CakeShopUserProfileForm(forms.ModelForm):
    class Meta:
        model = CakeShopUserProfile
        fields = ("gender", "text")

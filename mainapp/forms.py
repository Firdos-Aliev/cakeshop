import django.forms as forms
from mainapp.models import Catalog, Product


class CatalogCreateForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('name', 'img', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''


class CatalogChangeForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('name', 'img', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'img', 'text', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''


class ProductChangeForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'img', 'text', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''

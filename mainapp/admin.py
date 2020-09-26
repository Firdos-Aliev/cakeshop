from django.contrib import admin

from mainapp.models import Catalog, Product

# отображение в админке
admin.site.register(Catalog)
admin.site.register(Product)

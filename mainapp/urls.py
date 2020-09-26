from django.urls import path
import mainapp.views as mainapp

app_name = "mainapp"

# локальный диспетчер имен
urlpatterns = [
    path('', mainapp.index, name="index"),
    path('catalog/', mainapp.catalog, name="catalog"),
    path('catalog/<int:pk>/', mainapp.products, name="products"),
    path('product/<int:pk>/', mainapp.product, name="product"),
    path('contacts/', mainapp.contacts, name="contacts"),
]

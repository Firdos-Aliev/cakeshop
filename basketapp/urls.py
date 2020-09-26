from django.urls import path
import basketapp.views as basketapp

app_name = "basketapp"

# локальный диспетчер имен
urlpatterns = [
    path('basket_page/', basketapp.index, name="index"),
    path('new_product/<int:pk>/', basketapp.new_product, name="new_product"),
    path('product/<int:pk>/add/<int:count>/ajax/', basketapp.add),  # для ajax
    path('product/<int:pk>/pop/<int:count>/ajax/', basketapp.pop),
]

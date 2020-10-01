from django.urls import path
import ordersapp.views as ordersapp

app_name = "ordersapp"

# локальный диспетчер имен
urlpatterns = [
    path('list/', ordersapp.OrdersRead.as_view(), name="list"),
    path('create/', ordersapp.OrderCreate.as_view(), name="create"),
    path('list/<int:pk>/', ordersapp.OrderDetail.as_view(), name="read"),
]

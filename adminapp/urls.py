from django.urls import path
import adminapp.views as adminapp

app_name = "adminapp"

urlpatterns = [
    #path("users/", adminapp.users, name="users"),
    #path("user/create/", adminapp.user_create, name="user_create"),
    #path("user/change/<int:pk>/", adminapp.user_change, name="user_change"),
    #path("user/delete/<int:pk>/", adminapp.user_delete, name="user_delete"),
    #path("users/", adminapp.UsersRead.as_view(), name="users"),
    path("users/<int:page>/", adminapp.UsersRead.as_view(), name="users"),
    path("user/create/", adminapp.UserCreate.as_view(), name="user_create"),
    path("user/change/<int:pk>/", adminapp.UserChange.as_view(), name="user_change"),
    path("user/delete/<int:pk>/", adminapp.UserDelete.as_view(), name="user_delete"),
    path("user/<int:pk>/detail/", adminapp.UserDetail.as_view(), name="user_detail"),

    #path("catalogs/", adminapp.catalogs, name="catalogs"),
    path("catalogs/", adminapp.CatalogRead.as_view(), name="catalogs"),
    path("catalog/create/", adminapp.catalog_create, name="catalog_create"),
    path("catalog/change/<int:pk>/", adminapp.catalog_change, name="catalog_change"),
    path("catalog/delete/<int:pk>/", adminapp.catalog_delete, name="catalog_delete"),

    # добавить crud продуктов
    #path("products/", adminapp.products, name="products"),
    path("products/", adminapp.ProductsRead.as_view(), name="products"),
    path("products/create/", adminapp.product_create, name="product_create"),
    path("products/delete/<int:pk>", adminapp.product_delete, name="product_delete"),
    path("products/change/<int:pk>", adminapp.product_change, name="product_change"),



]
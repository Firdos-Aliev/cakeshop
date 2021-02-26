from django.urls import path
import authapp.views as authapp

app_name = "authapp"

# локальный диспетчер имен
urlpatterns = [
    path("login/", authapp.login, name="login"),
    path("logout/", authapp.logout, name="logout"),
    path("register/", authapp.register, name="register"),
    path("profile/", authapp.profile, name="profile"),
    path("user/<int:pk>/verify/<str:key>/", authapp.verify, name="user_verify"),
]

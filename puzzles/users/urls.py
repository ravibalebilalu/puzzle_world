from django.urls import path
from users import views

urlpatterns = [
    path("",views.user,name="user"),
    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
]

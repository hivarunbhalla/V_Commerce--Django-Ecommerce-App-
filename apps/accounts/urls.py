from django.urls import path
from . import views

urlpatterns= [
    path("login/", view= views.login_view, name= "login"),
    path('register/' , views.register_page , name="register"),
    path('activate/<email_token>/' , views.activate_email , name="activate_email"),
]
from django.urls import path
from . import views

urlpatterns= [
    path('activate/<email_token>/' , views.activate_email , name="activate_email"),
    path("login/", view= views.login_view, name= "login"),
    path('register/' , views.register_page , name="register"),
    # path('logout/', views.logout_view, name='logout'),
    # path('profile/', views.profile_view, name='profile'),
]
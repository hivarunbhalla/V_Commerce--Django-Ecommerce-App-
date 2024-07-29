from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns= [
    path('activate/<email_token>/' , views.activate_email , name="activate_email"),
    path("login/", view= views.login_view, name= "login"),
    path('register/' , views.register_page , name="register"),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter( email = email)

        if not user.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)

        if not user[0].profile.is_email_verified :
            messages.warning(request, 'Your email is not verified')
            return HttpResponseRedirect(request.path_info)

        
        #Authenticating User
        user_obj = authenticate(request=request, username=email, password=password)
        if user is not None:
            login(request, user_obj) 
            return redirect('/')
        messages.warning(request, "Invalid Credentials")

    return render(request=request, template_name= 'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter( email = email)

        if user.exists():
            messages.warning(request, 'User with same email alredy exists. You will be redirecting to login page')
            return redirect('login')
            

        #Creating new User
        user = User.objects.create(
            first_name= first_name,
            last_name = last_name,
            email = email,
            username = email,
        )
        user.set_password(password)
        user.save()

        messages.warning(request, "Check your inbox! A verification email sent to your mail")
        return HttpResponseRedirect(request.path_info)

    return render(request=request, template_name= 'accounts/register.html')


def activate_email(request):
    pass
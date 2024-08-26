from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '')
        password = request.POST.get('password', '')

        if name and password:
            user = authenticate(request, username=name, password=password)
            print('Usuario autenticado')
            if user is not None:
                login(request, user)
                print('Inicio de sesion correcto')
                print(request.user.is_authenticated)
                return redirect('/')
            else:
                print('algo anda mal')
        else:
            print('faltan datos')

    return render(request, 'user/user_login.html')


def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '')
        email = request.POST.get('user_email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if name and email and password1 and password2:
            print('Todos los datos fueron introducidos')
            if password1 == password2:
                print('contrasenas iguales')
                user = User.objects.create_user(username=name, email=email, password=password1)
                print('Created user: ', user)
                return redirect('/login/')
            else:
                print('contrasenas no coinciden')
        else:
            print('faltan datos')

    return render(request, 'user/user_signup.html')


def user_logout(request):
    logout(request)
    return redirect('/')

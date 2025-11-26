from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not password:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('/login/')

        user = authenticate(request, username=name, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'user/user_login.html')


def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '')
        email = request.POST.get('user_email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not all([name, email, password1, password2]):
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('/signup/')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('/signup/')
        
        if User.objects.filter(username=name).exists():
            messages.error(request, "Nombre de usuario ya esta en uso.")
            return redirect('/signup/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('/signup/')

        user = User.objects.create_user(username=name, email=email, password=password1)
        messages.success(request, "Cuenta creada exitosamente. Inicia sesión.")
        return redirect('/login/')

    return render(request, 'user/user_signup.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('/')

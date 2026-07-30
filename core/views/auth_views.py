"""Views de autenticação — Login, Registo, Logout."""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import LoginForm, RegistoUtilizadorForm


def pagina_login(request):
    """Página de login do sistema."""
    if request.user.is_authenticated:
        return redirect('redirecionar_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.nome_completo}!')
                return redirect('redirecionar_dashboard')
            else:
                messages.error(request, 'E-mail ou senha incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def pagina_registo(request):
    """Página de registo para novos pescadores."""
    if request.user.is_authenticated:
        return redirect('redirecionar_dashboard')

    if request.method == 'POST':
        form = RegistoUtilizadorForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
    else:
        form = RegistoUtilizadorForm()

    return render(request, 'core/registar.html', {'form': form})


def logout_view(request):
    """Logout do sistema."""
    logout(request)
    messages.info(request, 'Sessão terminada com sucesso.')
    return redirect('login')


@login_required
def redirecionar_dashboard(request):
    """Redireciona para o dashboard correcto conforme o tipo de utilizador."""
    tipo = request.user.tipo_utilizador
    if tipo == 'pescador':
        return redirect('dashboard_pescador')
    elif tipo == 'intransmar':
        return redirect('dashboard_intransmar')
    elif tipo == 'admin':
        return redirect('dashboard_admin')
    return redirect('login')

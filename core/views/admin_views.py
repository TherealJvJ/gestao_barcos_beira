"""Views do Administrador do Sistema."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import admin_required
from core.models import Utilizador, Embarcacao, Alerta, ConfiguracaoAlerta
from core.forms import ConfiguracaoAlertaForm, RegistoUtilizadorForm, PerfilForm


@login_required
@admin_required
def dashboard_admin(request):
    """Dashboard do administrador."""
    total_utilizadores = Utilizador.objects.filter(activo=True).count()
    total_pescadores = Utilizador.objects.filter(tipo_utilizador='pescador', activo=True).count()
    total_intransmar = Utilizador.objects.filter(tipo_utilizador='intransmar', activo=True).count()
    total_alertas = Alerta.objects.filter(estado='enviado').count()

    utilizadores_recentes = Utilizador.objects.order_by('-data_criacao')[:10]

    return render(request, 'core/dashboard_admin.html', {
        'total_utilizadores': total_utilizadores,
        'total_pescadores': total_pescadores,
        'total_intransmar': total_intransmar,
        'total_alertas': total_alertas,
        'utilizadores_recentes': utilizadores_recentes,
    })


@login_required
@admin_required
def lista_utilizadores(request):
    """Lista de todos os utilizadores."""
    from django.core.paginator import Paginator
    utilizadores_list = Utilizador.objects.all().order_by('nome_completo')
    tipo = request.GET.get('tipo', '')
    if tipo:
        utilizadores_list = utilizadores_list.filter(tipo_utilizador=tipo)

    paginator = Paginator(utilizadores_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/utilizador_lista.html', {
        'utilizadores': page_obj,
        'page_obj': page_obj,
    })


@login_required
@admin_required
def criar_utilizador(request):
    """Criar novo utilizador."""
    if request.method == 'POST':
        form = RegistoUtilizadorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            tipo = request.POST.get('tipo_utilizador', 'pescador')
            user.tipo_utilizador = tipo
            user.save()
            messages.success(request, f'Utilizador {user.nome_completo} criado com sucesso!')
            return redirect('lista_utilizadores')
    else:
        form = RegistoUtilizadorForm()

    return render(request, 'core/utilizador_form.html', {
        'form': form,
        'titulo_pagina': 'Criar Utilizador',
        'is_new': True,
    })


@login_required
@admin_required
def editar_utilizador(request, pk):
    """Editar utilizador existente."""
    utilizador = get_object_or_404(Utilizador, pk=pk)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=utilizador)
        if form.is_valid():
            user = form.save(commit=False)
            tipo = request.POST.get('tipo_utilizador', utilizador.tipo_utilizador)
            user.tipo_utilizador = tipo
            user.save()
            messages.success(request, 'Utilizador actualizado!')
            return redirect('lista_utilizadores')
    else:
        form = PerfilForm(instance=utilizador)

    return render(request, 'core/utilizador_form.html', {
        'form': form,
        'utilizador': utilizador,
        'titulo_pagina': f'Editar — {utilizador.nome_completo}',
        'is_new': False,
    })


@login_required
@admin_required
def desactivar_utilizador(request, pk):
    """Desactivar/activar um utilizador."""
    utilizador = get_object_or_404(Utilizador, pk=pk)
    utilizador.activo = not utilizador.activo
    utilizador.is_active = utilizador.activo
    utilizador.save()
    estado = 'activado' if utilizador.activo else 'desactivado'
    messages.success(request, f'Utilizador {utilizador.nome_completo} {estado}.')
    return redirect('lista_utilizadores')


@login_required
@admin_required
def alertas_config(request):
    """Configuração de alertas automáticos."""
    configs = ConfiguracaoAlerta.objects.all()

    if request.method == 'POST':
        form = ConfiguracaoAlertaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuração de alerta adicionada!')
            return redirect('alertas_config')
    else:
        form = ConfiguracaoAlertaForm()

    return render(request, 'core/alertas_config.html', {
        'form': form,
        'configs': configs,
    })


@login_required
@admin_required
def alertas_log(request):
    """Log de todas as notificações enviadas."""
    from django.core.paginator import Paginator
    alertas_list = Alerta.objects.all().order_by('-data_criacao')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')

    if tipo:
        alertas_list = alertas_list.filter(tipo_alerta=tipo)
    if estado:
        alertas_list = alertas_list.filter(estado=estado)

    paginator = Paginator(alertas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/alertas_log.html', {
        'alertas': page_obj,
        'page_obj': page_obj,
        'titulo_pagina': 'Log de Notificações',
        'is_admin': True,
    })

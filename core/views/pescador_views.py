"""Views do Pescador/Proprietário."""

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from core.decorators import pescador_required
from core.models import Embarcacao, LicencaNavegacao, TituloPropriedade, Alerta
from core.forms import EmbarcacaoForm, PerfilForm
from core.services.pdf_service import gerar_pdf_licenca, gerar_pdf_titulo


@login_required
@pescador_required
def dashboard_pescador(request):
    """Dashboard principal do pescador."""
    embarcacoes = Embarcacao.objects.filter(
        proprietario=request.user, estado_registo='aprovado'
    )
    total_embarcacoes = embarcacoes.count()

    licencas_activas = 0
    for emb in embarcacoes:
        lic = emb.licenca_activa
        if lic and lic.estado == 'activa':
            licencas_activas += 1

    alertas_pendentes = Alerta.objects.filter(
        destinatario=request.user, estado='pendente'
    ).count()

    alertas_recentes = Alerta.objects.filter(
        destinatario=request.user
    ).order_by('-data_criacao')[:5]

    return render(request, 'core/dashboard_pescador.html', {
        'embarcacoes': embarcacoes,
        'total_embarcacoes': total_embarcacoes,
        'licencas_activas': licencas_activas,
        'alertas_pendentes': alertas_pendentes,
        'alertas_recentes': alertas_recentes,
    })


@login_required
@pescador_required
def lista_embarcacoes_pescador(request):
    """Lista de embarcações do pescador."""
    from django.core.paginator import Paginator
    embarcacoes_list = Embarcacao.objects.filter(proprietario=request.user)
    paginator = Paginator(embarcacoes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/embarcacao_lista.html', {
        'embarcacoes': page_obj,
        'page_obj': page_obj,
        'titulo_pagina': 'Minhas Embarcações',
    })


@login_required
@pescador_required
def solicitar_registo_embarcacao(request):
    """Formulário para o pescador solicitar registo de uma embarcação."""
    if request.method == 'POST':
        form = EmbarcacaoForm(request.POST)
        if form.is_valid():
            embarcacao = form.save(commit=False)
            embarcacao.proprietario = request.user
            embarcacao.estado_registo = 'pendente'
            embarcacao.save()
            messages.success(request, 'Solicitação de registo enviada! Aguarde aprovação da INTRANSMAR.')
            return redirect('lista_embarcacoes')
    else:
        form = EmbarcacaoForm()

    return render(request, 'core/embarcacao_form.html', {
        'form': form,
        'titulo_pagina': 'Solicitar Registo de Embarcação',
        'is_new': True,
    })


@login_required
def detalhe_embarcacao(request, pk):
    """Detalhe de uma embarcação."""
    embarcacao = get_object_or_404(Embarcacao, pk=pk)

    # Verificar acesso
    if request.user.eh_pescador and embarcacao.proprietario != request.user:
        messages.error(request, 'Não tem permissão para ver esta embarcação.')
        return redirect('dashboard_pescador')

    licenca_actual = embarcacao.licenca_activa
    titulo = None
    try:
        titulo = embarcacao.titulo
    except TituloPropriedade.DoesNotExist:
        pass

    vistorias = embarcacao.vistorias.all()[:10]
    manutencoes = embarcacao.manutencoes.all()[:10]
    licencas = embarcacao.licencas.all()[:5]

    return render(request, 'core/embarcacao_detalhe.html', {
        'embarcacao': embarcacao,
        'licenca_actual': licenca_actual,
        'titulo': titulo,
        'vistorias': vistorias,
        'manutencoes': manutencoes,
        'licencas': licencas,
    })


@login_required
def baixar_licenca_pdf(request, pk):
    """Baixa o PDF de uma licença de navegação."""
    licenca = get_object_or_404(LicencaNavegacao, pk=pk)

    if request.user.eh_pescador and licenca.embarcacao.proprietario != request.user:
        messages.error(request, 'Sem permissão.')
        return redirect('dashboard_pescador')

    pdf_buffer = gerar_pdf_licenca(licenca)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Licenca_{licenca.numero_licenca}.pdf"'
    return response


@login_required
def baixar_titulo_pdf(request, pk):
    """Baixa o PDF de um título de propriedade."""
    titulo = get_object_or_404(TituloPropriedade, pk=pk)

    if request.user.eh_pescador and titulo.embarcacao.proprietario != request.user:
        messages.error(request, 'Sem permissão.')
        return redirect('dashboard_pescador')

    pdf_buffer = gerar_pdf_titulo(titulo)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Titulo_{titulo.numero_titulo}.pdf"'
    return response


@login_required
def editar_perfil(request):
    """Editar o perfil do utilizador."""
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'core/perfil.html', {'form': form})


@login_required
def lista_alertas(request):
    """Lista de alertas recebidos pelo utilizador."""
    from django.core.paginator import Paginator
    alertas_list = Alerta.objects.filter(destinatario=request.user)
    paginator = Paginator(alertas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/alertas_log.html', {
        'alertas': page_obj,
        'page_obj': page_obj,
        'titulo_pagina': 'Meus Alertas',
    })

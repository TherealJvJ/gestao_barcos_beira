"""Views dos funcionários INTRANSMAR."""

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from core.decorators import intransmar_required, intransmar_ou_admin_required
from core.models import (
    Embarcacao, LicencaNavegacao, TituloPropriedade,
    Vistoria, Manutencao, Alerta, Utilizador
)
from core.forms import (
    EmbarcacaoForm, LicencaNavegacaoForm, TituloPropriedadeForm,
    VistoriaForm, ManutencaoForm, BuscaAvancadaForm
)
from core.services.notificacao_service import notificar_documento_pronto
from core.services.pdf_service import gerar_pdf_relatorio


@login_required
@intransmar_required
def dashboard_intransmar(request):
    """Dashboard do funcionário INTRANSMAR com estatísticas."""
    total_embarcacoes = Embarcacao.objects.filter(estado_registo='aprovado').count()
    pendentes = Embarcacao.objects.filter(estado_registo='pendente').count()

    hoje = datetime.date.today()
    licencas_activas = LicencaNavegacao.objects.filter(
        activa=True, data_validade__gte=hoje
    ).count()

    licencas_expirando = LicencaNavegacao.objects.filter(
        activa=True,
        data_validade__gte=hoje,
        data_validade__lte=hoje + datetime.timedelta(days=30)
    ).count()

    # Dados para gráficos
    por_tipo = list(Embarcacao.objects.filter(estado_registo='aprovado')
                    .values('tipo_embarcacao').annotate(total=Count('id')))

    registos_pendentes = Embarcacao.objects.filter(
        estado_registo='pendente'
    ).order_by('-data_criacao')[:5]

    return render(request, 'core/dashboard_intransmar.html', {
        'total_embarcacoes': total_embarcacoes,
        'pendentes': pendentes,
        'licencas_activas': licencas_activas,
        'licencas_expirando': licencas_expirando,
        'por_tipo': por_tipo,
        'registos_pendentes': registos_pendentes,
    })


@login_required
@intransmar_required
def lista_embarcacoes_intransmar(request):
    """Lista de todas as embarcações (INTRANSMAR)."""
    from django.core.paginator import Paginator
    embarcacoes_list = Embarcacao.objects.all()
    estado = request.GET.get('estado', '')
    if estado:
        embarcacoes_list = embarcacoes_list.filter(estado_registo=estado)

    paginator = Paginator(embarcacoes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/embarcacao_lista.html', {
        'embarcacoes': page_obj,
        'page_obj': page_obj,
        'titulo_pagina': 'Todas as Embarcações',
        'is_intransmar': True,
    })


@login_required
@intransmar_required
def registos_pendentes(request):
    """Lista de registos de embarcações pendentes de aprovação."""
    from django.core.paginator import Paginator
    pendentes_list = Embarcacao.objects.filter(estado_registo='pendente').order_by('-data_criacao')
    
    paginator = Paginator(pendentes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/registos_pendentes.html', {
        'pendentes': page_obj,
        'page_obj': page_obj,
    })


@login_required
@intransmar_required
def aprovar_embarcacao(request, pk):
    """Aprovar registo de uma embarcação."""
    embarcacao = get_object_or_404(Embarcacao, pk=pk, estado_registo='pendente')
    embarcacao.estado_registo = 'aprovado'
    embarcacao.save()
    messages.success(request, f'Embarcação "{embarcacao.nome}" aprovada com sucesso!')
    return redirect('registos_pendentes')


@login_required
@intransmar_required
def rejeitar_embarcacao(request, pk):
    """Rejeitar registo de uma embarcação."""
    embarcacao = get_object_or_404(Embarcacao, pk=pk, estado_registo='pendente')
    embarcacao.estado_registo = 'rejeitado'
    embarcacao.save()
    messages.warning(request, f'Embarcação "{embarcacao.nome}" rejeitada.')
    return redirect('registos_pendentes')


@login_required
@intransmar_required
def emitir_licenca(request, embarcacao_pk):
    """Emitir licença de navegação para uma embarcação."""
    embarcacao = get_object_or_404(Embarcacao, pk=embarcacao_pk)
    
    if embarcacao.estado_registo != 'aprovado':
        messages.error(request, 'Não é possível emitir documentos para uma embarcação pendente ou rejeitada. Aprove-a primeiro.')
        return redirect('detalhe_embarcacao', pk=embarcacao_pk)

    if request.method == 'POST':
        form = LicencaNavegacaoForm(request.POST)
        if form.is_valid():
            licenca = form.save(commit=False)
            licenca.embarcacao = embarcacao
            licenca.emitida_por = request.user
            licenca.data_emissao = datetime.date.today()

            # Gerar número de licença automático
            ano = licenca.ano_referencia
            ultimo = LicencaNavegacao.objects.filter(ano_referencia=ano).count() + 1
            licenca.numero_licenca = f"LN-{ano}-{ultimo:06d}"

            licenca.save()

            # Notificar proprietário (SMS + Email com PDF)
            notificar_documento_pronto('licenca_pronta', licenca)

            messages.success(request, f'Licença {licenca.numero_licenca} emitida! Proprietário notificado por SMS e e-mail.')
            return redirect('detalhe_embarcacao', pk=embarcacao_pk)
    else:
        form = LicencaNavegacaoForm(initial={'ano_referencia': datetime.date.today().year})

    return render(request, 'core/licenca_emitir.html', {
        'form': form,
        'embarcacao': embarcacao,
    })


@login_required
@intransmar_required
def emitir_titulo(request, embarcacao_pk):
    """Emitir título de propriedade para uma embarcação."""
    embarcacao = get_object_or_404(Embarcacao, pk=embarcacao_pk)

    if embarcacao.estado_registo != 'aprovado':
        messages.error(request, 'Não é possível emitir documentos para uma embarcação pendente ou rejeitada. Aprove-a primeiro.')
        return redirect('detalhe_embarcacao', pk=embarcacao_pk)

    # Verificar se já tem título
    if embarcacao.tem_titulo:
        messages.warning(request, 'Esta embarcação já possui um título de propriedade.')
        return redirect('detalhe_embarcacao', pk=embarcacao_pk)

    if request.method == 'POST':
        form = TituloPropriedadeForm(request.POST)
        if form.is_valid():
            titulo = form.save(commit=False)
            titulo.embarcacao = embarcacao
            titulo.emitido_por = request.user
            titulo.data_emissao = datetime.date.today()

            # Gerar número de título automático
            total = TituloPropriedade.objects.count() + 1
            titulo.numero_titulo = f"TP-{datetime.date.today().year}-{total:06d}"

            titulo.save()

            # Notificar proprietário (SMS + Email com PDF)
            notificar_documento_pronto('titulo_pronto', titulo)

            messages.success(request, f'Título {titulo.numero_titulo} emitido! Proprietário notificado por SMS e e-mail.')
            return redirect('detalhe_embarcacao', pk=embarcacao_pk)
    else:
        form = TituloPropriedadeForm()

    return render(request, 'core/titulo_emitir.html', {
        'form': form,
        'embarcacao': embarcacao,
    })


@login_required
@intransmar_required
def registar_vistoria(request):
    """Registar uma vistoria técnica."""
    if request.method == 'POST':
        form = VistoriaForm(request.POST)
        if form.is_valid():
            vistoria = form.save(commit=False)
            vistoria.inspector = request.user
            vistoria.save()
            messages.success(request, 'Vistoria registada com sucesso!')
            return redirect('detalhe_embarcacao', pk=vistoria.embarcacao.pk)
    else:
        form = VistoriaForm()
        # Filtrar apenas embarcações aprovadas
        form.fields['embarcacao'].queryset = Embarcacao.objects.filter(estado_registo='aprovado')

    return render(request, 'core/vistoria_form.html', {'form': form})


@login_required
@intransmar_required
def registar_manutencao(request):
    """Registar uma manutenção."""
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção registada com sucesso!')
            return redirect('detalhe_embarcacao', pk=form.cleaned_data['embarcacao'].pk)
    else:
        form = ManutencaoForm()
        form.fields['embarcacao'].queryset = Embarcacao.objects.filter(estado_registo='aprovado')

    return render(request, 'core/manutencao_form.html', {'form': form})


@login_required
@intransmar_required
def busca_avancada(request):
    """Busca avançada de embarcações."""
    from django.core.paginator import Paginator
    form = BuscaAvancadaForm(request.GET or None)
    resultados_list = Embarcacao.objects.filter(estado_registo='aprovado')

    if form.is_valid():
        matricula = form.cleaned_data.get('numero_matricula')
        nome = form.cleaned_data.get('nome_embarcacao')
        prop = form.cleaned_data.get('nome_proprietario')
        tipo = form.cleaned_data.get('tipo_embarcacao')

        if matricula:
            resultados_list = resultados_list.filter(numero_matricula__icontains=matricula)
        if nome:
            resultados_list = resultados_list.filter(nome__icontains=nome)
        if prop:
            resultados_list = resultados_list.filter(proprietario__nome_completo__icontains=prop)
        if tipo:
            resultados_list = resultados_list.filter(tipo_embarcacao=tipo)

    paginator = Paginator(resultados_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/busca_avancada.html', {
        'form': form,
        'resultados': page_obj,
        'page_obj': page_obj,
    })


@login_required
@intransmar_required
def relatorio(request):
    """Página de geração de relatórios."""
    from django.core.paginator import Paginator
    embarcacoes_list = Embarcacao.objects.filter(estado_registo='aprovado')
    tipo = request.GET.get('tipo', '')
    if tipo:
        embarcacoes_list = embarcacoes_list.filter(tipo_embarcacao=tipo)

    paginator = Paginator(embarcacoes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/relatorio.html', {
        'embarcacoes': page_obj,
        'page_obj': page_obj,
    })


@login_required
@intransmar_required
def gerar_relatorio_pdf(request):
    """Gera e baixa o relatório em PDF."""
    embarcacoes = Embarcacao.objects.filter(estado_registo='aprovado')
    tipo = request.GET.get('tipo', '')
    if tipo:
        embarcacoes = embarcacoes.filter(tipo_embarcacao=tipo)

    pdf_buffer = gerar_pdf_relatorio(embarcacoes)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Relatorio_Embarcacoes.pdf"'
    return response


@login_required
@intransmar_ou_admin_required
def dados_graficos(request):
    """Endpoint JSON para gráficos do dashboard."""
    por_tipo = list(Embarcacao.objects.filter(estado_registo='aprovado')
                    .values('tipo_embarcacao').annotate(total=Count('id')))

    hoje = datetime.date.today()
    licencas_status = {
        'activas': LicencaNavegacao.objects.filter(activa=True, data_validade__gt=hoje + datetime.timedelta(days=30)).count(),
        'expirando': LicencaNavegacao.objects.filter(activa=True, data_validade__lte=hoje + datetime.timedelta(days=30), data_validade__gte=hoje).count(),
        'expiradas': LicencaNavegacao.objects.filter(activa=True, data_validade__lt=hoje).count(),
    }

    return JsonResponse({
        'por_tipo': por_tipo,
        'licencas_status': licencas_status,
    })

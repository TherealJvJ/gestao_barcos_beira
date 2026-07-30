"""Context processor global — dados disponíveis em todos os templates."""

from .models import Alerta, Embarcacao


def dados_globais(request):
    """Adiciona dados globais ao contexto de todos os templates."""
    contexto = {
        'nome_sistema': 'INTRANSMAR',
        'subtitulo_sistema': 'Sistema de Gestão de Barcos — Pesca Artesanal, Beira',
    }

    if request.user.is_authenticated:
        contexto['tipo_utilizador'] = request.user.tipo_utilizador

        # Alertas não lidos do utilizador
        contexto['alertas_nao_lidos'] = Alerta.objects.filter(
            destinatario=request.user,
            estado='pendente'
        ).count()

        # Contagem de pendentes (para badge na sidebar de intransmar/admin)
        tipo = request.user.tipo_utilizador
        if tipo in ('intransmar', 'admin'):
            contexto['pendentes_count'] = Embarcacao.objects.filter(
                estado_registo='pendente'
            ).count()
        else:
            contexto['pendentes_count'] = 0

    return contexto

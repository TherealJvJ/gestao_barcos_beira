"""Template tags personalizadas do sistema."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def estado_badge(estado):
    """Retorna badge HTML colorido conforme o estado."""
    mapa = {
        'activa': ('Activa', 'badge-activa'),
        'expirando': ('A Expirar', 'badge-pendente'),
        'expirada': ('Expirada', 'badge-expirada'),
        'inactiva': ('Inactiva', 'badge-expirada'),
        'pendente': ('Pendente', 'badge-pendente'),
        'aprovado': ('Aprovado', 'badge-activa'),
        'rejeitado': ('Rejeitado', 'badge-expirada'),
        'aprovada': ('Aprovada', 'badge-activa'),
        'reprovada': ('Reprovada', 'badge-expirada'),
        'enviado': ('Enviado', 'badge-activa'),
        'falhou': ('Falhou', 'badge-expirada'),
    }
    texto, classe = mapa.get(estado, (estado, 'badge-pendente'))
    return mark_safe(f'<span class="badge {classe}">{texto}</span>')


@register.filter
def formato_telefone(telefone):
    """Formata número de telefone moçambicano."""
    if not telefone:
        return ''
    t = telefone.replace('+', '').replace(' ', '')
    if t.startswith('258') and len(t) == 12:
        return f"+258 {t[3:5]} {t[5:8]} {t[8:]}"
    return telefone


@register.filter
def formato_moeda(valor):
    """Formata valor em Meticais (MZN)."""
    if valor is None:
        return '0,00 MZN'
    try:
        return f"{float(valor):,.2f} MZN".replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return '0,00 MZN'

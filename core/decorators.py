"""Decoradores de controlo de acesso por tipo de utilizador."""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def tipo_utilizador_required(tipos_permitidos):
    """Restringe o acesso a utilizadores com o tipo especificado."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.tipo_utilizador not in tipos_permitidos:
                messages.error(request, 'Não tem permissão para aceder a esta página.')
                return redirect('redirecionar_dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def pescador_required(view_func):
    """Acesso apenas para pescadores."""
    return tipo_utilizador_required(['pescador'])(view_func)


def intransmar_required(view_func):
    """Acesso apenas para funcionários INTRANSMAR."""
    return tipo_utilizador_required(['intransmar'])(view_func)


def admin_required(view_func):
    """Acesso apenas para administradores."""
    return tipo_utilizador_required(['admin'])(view_func)


def intransmar_ou_admin_required(view_func):
    """Acesso para INTRANSMAR ou administradores."""
    return tipo_utilizador_required(['intransmar', 'admin'])(view_func)

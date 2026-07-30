"""URLs da aplicação core."""

from django.urls import path
from django.contrib.auth import views as django_auth_views
from core.views import auth_views, pescador_views, intransmar_views, admin_views

urlpatterns = [
    # === Autenticação ===
    path('login/', auth_views.pagina_login, name='login'),
    path('registar/', auth_views.pagina_registo, name='registar'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('redirecionar/', auth_views.redirecionar_dashboard, name='redirecionar_dashboard'),

    # === Pescador ===
    path('pescador/dashboard/', pescador_views.dashboard_pescador, name='dashboard_pescador'),
    path('embarcacoes/', pescador_views.lista_embarcacoes_pescador, name='lista_embarcacoes'),
    path('embarcacoes/nova/', pescador_views.solicitar_registo_embarcacao, name='criar_embarcacao'),
    path('embarcacoes/<int:pk>/', pescador_views.detalhe_embarcacao, name='detalhe_embarcacao'),
    path('licencas/<int:pk>/pdf/', pescador_views.baixar_licenca_pdf, name='baixar_licenca_pdf'),
    path('titulos/<int:pk>/pdf/', pescador_views.baixar_titulo_pdf, name='baixar_titulo_pdf'),
    path('perfil/', pescador_views.editar_perfil, name='perfil'),
    path('alertas/', pescador_views.lista_alertas, name='lista_alertas'),

    # === INTRANSMAR ===
    path('intransmar/dashboard/', intransmar_views.dashboard_intransmar, name='dashboard_intransmar'),
    path('intransmar/embarcacoes/', intransmar_views.lista_embarcacoes_intransmar, name='lista_embarcacoes_intransmar'),
    path('intransmar/pendentes/', intransmar_views.registos_pendentes, name='registos_pendentes'),
    path('intransmar/aprovar/<int:pk>/', intransmar_views.aprovar_embarcacao, name='aprovar_embarcacao'),
    path('intransmar/rejeitar/<int:pk>/', intransmar_views.rejeitar_embarcacao, name='rejeitar_embarcacao'),
    path('intransmar/licenca/<int:embarcacao_pk>/', intransmar_views.emitir_licenca, name='emitir_licenca'),
    path('intransmar/titulo/<int:embarcacao_pk>/', intransmar_views.emitir_titulo, name='emitir_titulo'),
    path('intransmar/vistoria/', intransmar_views.registar_vistoria, name='registar_vistoria'),
    path('intransmar/manutencao/', intransmar_views.registar_manutencao, name='registar_manutencao'),
    path('intransmar/busca/', intransmar_views.busca_avancada, name='busca_avancada'),
    path('intransmar/relatorio/', intransmar_views.relatorio, name='relatorio'),
    path('intransmar/relatorio/pdf/', intransmar_views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('intransmar/graficos/', intransmar_views.dados_graficos, name='dados_graficos'),

    # === Administrador ===
    path('admin-sistema/dashboard/', admin_views.dashboard_admin, name='dashboard_admin'),
    path('admin-sistema/utilizadores/', admin_views.lista_utilizadores, name='lista_utilizadores'),
    path('admin-sistema/utilizadores/novo/', admin_views.criar_utilizador, name='criar_utilizador'),
    path('admin-sistema/utilizadores/<int:pk>/editar/', admin_views.editar_utilizador, name='editar_utilizador'),
    path('admin-sistema/utilizadores/<int:pk>/desactivar/', admin_views.desactivar_utilizador, name='desactivar_utilizador'),
    path('admin-sistema/alertas/config/', admin_views.alertas_config, name='alertas_config'),
    path('admin-sistema/alertas/log/', admin_views.alertas_log, name='alertas_log'),

    # === Recuperação de Senha ===
    path('recuperar-senha/', django_auth_views.PasswordResetView.as_view(
        template_name='core/registration/password_reset_form.html',
        email_template_name='core/registration/password_reset_email.html',
        subject_template_name='core/registration/password_reset_subject.txt',
        success_url='/recuperar-senha/enviado/'
    ), name='password_reset'),
    path('recuperar-senha/enviado/', django_auth_views.PasswordResetDoneView.as_view(
        template_name='core/registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('recuperar-senha/confirmar/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(
        template_name='core/registration/password_reset_confirm.html',
        success_url='/recuperar-senha/concluido/'
    ), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', django_auth_views.PasswordResetCompleteView.as_view(
        template_name='core/registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]

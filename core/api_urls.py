"""URLs da API REST do DRF."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import api_views

router = DefaultRouter()
router.register('embarcacoes', api_views.EmbarcacaoViewSet, basename='api_embarcacoes')
router.register('alertas', api_views.AlertaViewSet, basename='api_alertas')
router.register('configuracoes', api_views.ConfiguracaoAlertaViewSet, basename='api_configuracoes')

urlpatterns = [
    path('login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('perfil/', api_views.PerfilAPIView.as_view(), name='api_perfil'),
    path('licencas/<int:pk>/pdf/', api_views.DescarregarPDFLicencaAPIView.as_view(), name='api_pdf_licenca'),
    path('titulos/<int:pk>/pdf/', api_views.DescarregarPDFTituloAPIView.as_view(), name='api_pdf_titulo'),
    path('password-reset/', api_views.PasswordResetAPIView.as_view(), name='api_password_reset'),
    path('', include(router.urls)),
]

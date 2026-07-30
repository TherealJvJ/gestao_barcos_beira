"""Views da API REST do DRF para a App Móvel (Flutter)."""

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from core.models import Embarcacao, LicencaNavegacao, TituloPropriedade, Alerta, Utilizador, ConfiguracaoAlerta
from core.serializers import (
    EmbarcacaoSerializer, LicencaNavegacaoSerializer,
    TituloPropriedadeSerializer, AlertaSerializer, UtilizadorSerializer, ConfiguracaoAlertaSerializer
)
from core.services.pdf_service import gerar_pdf_licenca, gerar_pdf_titulo


class LoginAPIView(ObtainAuthToken):
    """Autenticação e geração de token para a app móvel."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'nome': user.nome_completo,
            'tipo_utilizador': user.tipo_utilizador
        })


class PerfilAPIView(APIView):
    """Ver e actualizar perfil do utilizador via API."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UtilizadorSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UtilizadorSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmbarcacaoViewSet(viewsets.ModelViewSet):
    """Endpoints para gerir embarcações."""
    serializer_class = EmbarcacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Pescadores vêem apenas as suas próprias embarcações
        if self.request.user.eh_pescador:
            return Embarcacao.objects.filter(proprietario=self.request.user)
        # Funcionários INTRANSMAR vêem todas as aprovadas
        return Embarcacao.objects.filter(estado_registo='aprovado')

    def perform_create(self, serializer):
        # Forçar o proprietário a ser o utilizador autenticado se for pescador
        if self.request.user.eh_pescador:
            serializer.save(proprietario=self.request.user, estado_registo='pendente')
        else:
            serializer.save(estado_registo='aprovado')


class AlertaViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoints para ver alertas do utilizador."""
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alerta.objects.filter(destinatario=self.request.user)


class DescarregarPDFLicencaAPIView(APIView):
    """Descarregar PDF da Licença via API."""
    permission_classes = [permissions.AllowAny] # Permite verificar o token na view

    def get(self, request, pk):
        token_key = request.query_params.get('token')
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                return Response({'erro': 'Token inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
                
        if not request.user.is_authenticated:
            return Response({'erro': 'Não autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        licenca = get_object_or_404(LicencaNavegacao, pk=pk)
        # Pescador só pode baixar a sua
        if request.user.eh_pescador and licenca.embarcacao.proprietario != request.user:
            return Response({'erro': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        
        pdf_buffer = gerar_pdf_licenca(licenca)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Licenca_{licenca.numero_licenca}.pdf"'
        return response


class DescarregarPDFTituloAPIView(APIView):
    """Descarregar PDF do Título via API."""
    permission_classes = [permissions.AllowAny] # Permite verificar o token na view

    def get(self, request, pk):
        token_key = request.query_params.get('token')
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                return Response({'erro': 'Token inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
                
        if not request.user.is_authenticated:
            return Response({'erro': 'Não autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        titulo = get_object_or_404(TituloPropriedade, pk=pk)
        if request.user.eh_pescador and titulo.embarcacao.proprietario != request.user:
            return Response({'erro': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        
        pdf_buffer = gerar_pdf_titulo(titulo)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Titulo_{titulo.numero_titulo}.pdf"'
        return response


class ConfiguracaoAlertaViewSet(viewsets.ModelViewSet):
    """Endpoints para gerir preferências de alerta do utilizador (apenas funcionários/admins)."""
    serializer_class = ConfiguracaoAlertaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.eh_pescador:
            return ConfiguracaoAlerta.objects.none()
        return ConfiguracaoAlerta.objects.all().order_by('tipo_documento')

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.user.is_authenticated and request.user.eh_pescador:
            self.permission_denied(request, message="Apenas funcionários da instituição podem gerir configurações de alertas.")

    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)


class PasswordResetAPIView(APIView):
    """Envia o e-mail padrão de recuperação de palavra-passe do Django via API."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'erro': 'O email é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            # Retornamos sucesso mesmo que o e-mail não exista (boa prática de segurança)
            return Response({'sucesso': 'Se o e-mail existir na nossa base de dados, receberá um link de recuperação.'})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

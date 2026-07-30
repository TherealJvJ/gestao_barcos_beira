"""Serializers do Django REST Framework para a App Móvel."""

from rest_framework import serializers
from core.models import (
    Utilizador, Embarcacao, LicencaNavegacao,
    TituloPropriedade, Vistoria, Manutencao, Alerta, ConfiguracaoAlerta
)


class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = ['id', 'nome_completo', 'email', 'telefone', 'numero_documento', 'tipo_utilizador']
        read_only_fields = ['tipo_utilizador']


class LicencaNavegacaoSerializer(serializers.ModelSerializer):
    estado = serializers.ReadOnlyField()
    dias_restantes = serializers.ReadOnlyField()

    class Meta:
        model = LicencaNavegacao
        fields = [
            'id', 'numero_licenca', 'data_emissao', 'data_validade',
            'ano_referencia', 'activa', 'estado', 'dias_restantes', 'observacoes'
        ]


class TituloPropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TituloPropriedade
        fields = ['id', 'numero_titulo', 'data_emissao', 'activo', 'observacoes']


class VistoriaSerializer(serializers.ModelSerializer):
    inspector_nome = serializers.CharField(source='inspector.nome_completo', read_only=True)

    class Meta:
        model = Vistoria
        fields = ['id', 'data_vistoria', 'proxima_vistoria', 'resultado', 'inspector_nome', 'observacoes']


class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = ['id', 'descricao', 'data_manutencao', 'custo', 'tipo_manutencao', 'observacoes']


class EmbarcacaoSerializer(serializers.ModelSerializer):
    proprietario_detalhe = UtilizadorSerializer(source='proprietario', read_only=True)
    licenca_activa = LicencaNavegacaoSerializer(read_only=True)
    titulo = TituloPropriedadeSerializer(read_only=True)
    vistorias = VistoriaSerializer(many=True, read_only=True)
    manutencoes = ManutencaoSerializer(many=True, read_only=True)

    class Meta:
        model = Embarcacao
        fields = [
            'id', 'nome', 'numero_matricula', 'tipo_embarcacao',
            'comprimento', 'potencia_motor', 'ano_construcao', 'material',
            'estado_registo', 'observacoes', 'proprietario_detalhe',
            'licenca_activa', 'titulo', 'vistorias', 'manutencoes'
        ]
        read_only_fields = ['estado_registo']


class AlertaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_alerta_display', read_only=True)

    class Meta:
        model = Alerta
        fields = ['id', 'tipo_alerta', 'tipo_display', 'mensagem', 'estado', 'data_criacao']


class ConfiguracaoAlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoAlerta
        fields = ['id', 'dias_antecedencia', 'canal', 'activo', 'tipo_documento']

"""Admin do Sistema de Gestão de Barcos — INTRANSMAR."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilizador, Embarcacao, LicencaNavegacao,
    TituloPropriedade, Vistoria, Manutencao,
    Alerta, ConfiguracaoAlerta
)


@admin.register(Utilizador)
class UtilizadorAdmin(UserAdmin):
    list_display = ('nome_completo', 'email', 'telefone', 'tipo_utilizador', 'activo')
    list_filter = ('tipo_utilizador', 'activo')
    search_fields = ('nome_completo', 'email', 'telefone', 'numero_documento')
    ordering = ('nome_completo',)
    fieldsets = UserAdmin.fieldsets + (
        ('Dados INTRANSMAR', {
            'fields': ('nome_completo', 'telefone', 'tipo_utilizador', 'numero_documento', 'activo')
        }),
    )


@admin.register(Embarcacao)
class EmbarcacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero_matricula', 'tipo_embarcacao', 'proprietario', 'estado_registo', 'data_criacao')
    list_filter = ('tipo_embarcacao', 'estado_registo', 'material')
    search_fields = ('nome', 'numero_matricula', 'proprietario__nome_completo')
    date_hierarchy = 'data_criacao'


@admin.register(LicencaNavegacao)
class LicencaNavegacaoAdmin(admin.ModelAdmin):
    list_display = ('numero_licenca', 'embarcacao', 'data_emissao', 'data_validade', 'activa', 'estado')
    list_filter = ('activa', 'ano_referencia')
    search_fields = ('numero_licenca', 'embarcacao__nome')
    date_hierarchy = 'data_emissao'


@admin.register(TituloPropriedade)
class TituloPropriedadeAdmin(admin.ModelAdmin):
    list_display = ('numero_titulo', 'embarcacao', 'data_emissao', 'activo')
    list_filter = ('activo',)
    search_fields = ('numero_titulo', 'embarcacao__nome')


@admin.register(Vistoria)
class VistoriaAdmin(admin.ModelAdmin):
    list_display = ('embarcacao', 'inspector', 'data_vistoria', 'resultado', 'proxima_vistoria')
    list_filter = ('resultado',)
    search_fields = ('embarcacao__nome',)
    date_hierarchy = 'data_vistoria'


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('embarcacao', 'descricao', 'data_manutencao', 'custo', 'tipo_manutencao')
    list_filter = ('tipo_manutencao',)
    search_fields = ('embarcacao__nome', 'descricao')
    date_hierarchy = 'data_manutencao'


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo_alerta', 'destinatario', 'canal', 'estado', 'data_envio', 'data_criacao')
    list_filter = ('tipo_alerta', 'canal', 'estado')
    search_fields = ('destinatario__nome_completo', 'mensagem')
    date_hierarchy = 'data_criacao'


@admin.register(ConfiguracaoAlerta)
class ConfiguracaoAlertaAdmin(admin.ModelAdmin):
    list_display = ('dias_antecedencia', 'canal', 'activo')
    list_filter = ('activo', 'canal')

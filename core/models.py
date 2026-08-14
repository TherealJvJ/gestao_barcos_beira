"""
Models do Sistema de Gestão de Barcos — INTRANSMAR
Todas as tabelas e colunas em português.
"""

import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Utilizador(AbstractUser):
    """Utilizador do sistema — Pescador, INTRANSMAR ou Administrador."""

    TIPO_CHOICES = [
        ('pescador', 'Pescador'),
        ('intransmar', 'INTRANSMAR'),
        ('admin', 'Administrador'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_utilizador')
    nome_completo = models.CharField('Nome Completo', max_length=255)
    email = models.EmailField('E-mail Gmail', unique=True)
    telefone = models.CharField('Telefone (+258)', max_length=20)
    tipo_utilizador = models.CharField(
        'Tipo de Utilizador', max_length=20,
        choices=TIPO_CHOICES, default='pescador'
    )
    numero_documento = models.CharField(
        'Nº Documento (BI/NUIT)', max_length=50, blank=True
    )
    activo = models.BooleanField('Activo', default=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome_completo', 'telefone']

    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'
        db_table = 'utilizador'

    def __str__(self):
        return self.nome_completo

    @property
    def eh_pescador(self):
        return self.tipo_utilizador == 'pescador'

    @property
    def eh_intransmar(self):
        return self.tipo_utilizador == 'intransmar'

    @property
    def eh_admin(self):
        return self.tipo_utilizador == 'admin'


class Embarcacao(models.Model):
    """Embarcação de pesca artesanal."""

    TIPO_CHOICES = [
        ('canoa', 'Canoa'),
        ('canoa_motor', 'Canoa a Motor'),
        ('lancha', 'Lancha'),
    ]
    MATERIAL_CHOICES = [
        ('madeira', 'Madeira'),
        ('fibra', 'Fibra de Vidro'),
        ('aluminio', 'Alumínio'),
    ]
    ESTADO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_embarcacao')
    nome = models.CharField('Nome da Embarcação', max_length=100)
    numero_matricula = models.CharField(
        'Nº Matrícula', max_length=50, unique=True
    )
    tipo_embarcacao = models.CharField(
        'Tipo de Embarcação', max_length=20, choices=TIPO_CHOICES
    )
    comprimento = models.FloatField(
        'Comprimento (m)', help_text='Máximo 10 metros para pesca artesanal'
    )
    potencia_motor = models.IntegerField(
        'Potência do Motor (CV)', default=0,
        help_text='Máximo 100 CV. Coloque 0 se não tiver motor.'
    )
    ano_construcao = models.IntegerField('Ano de Construção')
    material = models.CharField(
        'Material', max_length=20,
        choices=MATERIAL_CHOICES, default='madeira'
    )
    proprietario = models.ForeignKey(
        Utilizador, on_delete=models.CASCADE,
        related_name='embarcacoes_proprias', verbose_name='Proprietário',
        db_column='id_utilizador'
    )
    pescadores = models.ManyToManyField(
        Utilizador, related_name='embarcacoes_pesca',
        blank=True, verbose_name='Pescadores Associados'
    )
    estado_registo = models.CharField(
        'Estado do Registo', max_length=20,
        choices=ESTADO_CHOICES, default='pendente'
    )
    observacoes = models.TextField('Observações', blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Embarcação'
        verbose_name_plural = 'Embarcações'
        db_table = 'embarcacao'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.nome} ({self.numero_matricula})"

    def clean(self):
        """Validação de regras da pesca artesanal."""
        if self.comprimento and self.comprimento > 10:
            raise ValidationError({
                'comprimento': 'Embarcação artesanal deve ter comprimento inferior a 10 metros.'
            })
        if self.potencia_motor and self.potencia_motor > 100:
            raise ValidationError({
                'potencia_motor': 'Embarcação artesanal deve ter potência máxima de 100 CV.'
            })

    @property
    def licenca_activa(self):
        """Retorna a licença activa mais recente."""
        return self.licencas.filter(activa=True).order_by('-data_emissao').first()

    @property
    def tem_titulo(self):
        """Verifica se a embarcação tem título de propriedade."""
        return hasattr(self, 'titulo') and self.titulo is not None


class LicencaNavegacao(models.Model):
    """Licença de Navegação — válida até 31 de Dezembro do ano de emissão."""

    id = models.AutoField(primary_key=True, db_column='id_licenca_navegacao')
    embarcacao = models.ForeignKey(
        Embarcacao, on_delete=models.CASCADE,
        related_name='licencas', verbose_name='Embarcação',
        db_column='id_embarcacao'
    )
    numero_licenca = models.CharField('Nº Licença', max_length=50, unique=True)
    data_emissao = models.DateField('Data de Emissão', default=timezone.now)
    data_validade = models.DateField('Data de Validade')
    ano_referencia = models.IntegerField('Ano de Referência')
    activa = models.BooleanField('Activa', default=True)
    emitida_por = models.ForeignKey(
        Utilizador, on_delete=models.SET_NULL, null=True,
        related_name='licencas_emitidas', verbose_name='Emitida por',
        db_column='id_utilizador'
    )
    observacoes = models.TextField('Observações', blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Licença de Navegação'
        verbose_name_plural = 'Licenças de Navegação'
        db_table = 'licenca_navegacao'
        ordering = ['-data_emissao']

    def __str__(self):
        return f"{self.numero_licenca} — {self.embarcacao.nome}"

    def save(self, *args, **kwargs):
        """Calcula automaticamente a data de validade como 31/12 do ano."""
        if not self.ano_referencia:
            self.ano_referencia = self.data_emissao.year if self.data_emissao else timezone.now().date().year
        self.data_validade = datetime.date(self.ano_referencia, 12, 31)
        super().save(*args, **kwargs)

    @property
    def estado(self):
        """Retorna o estado actual da licença."""
        hoje = datetime.date.today()
        if not self.activa:
            return 'inactiva'
        if hoje > self.data_validade:
            return 'expirada'
        dias = (self.data_validade - hoje).days
        if dias <= 30:
            return 'expirando'
        return 'activa'

    @property
    def dias_restantes(self):
        """Dias até a expiração."""
        return max(0, (self.data_validade - datetime.date.today()).days)

    @property
    def cor_estado(self):
        """Retorna a classe CSS para o estado."""
        mapa = {
            'activa': 'badge-activa',
            'expirando': 'badge-pendente',
            'expirada': 'badge-expirada',
            'inactiva': 'badge-expirada',
        }
        return mapa.get(self.estado, 'badge-pendente')


class TituloPropriedade(models.Model):
    """Título de Propriedade — permanente, sem prazo de validade."""

    id = models.AutoField(primary_key=True, db_column='id_titulo_propriedade')
    embarcacao = models.OneToOneField(
        Embarcacao, on_delete=models.CASCADE,
        related_name='titulo', verbose_name='Embarcação',
        db_column='id_embarcacao'
    )
    numero_titulo = models.CharField('Nº Título', max_length=50, unique=True)
    data_emissao = models.DateField('Data de Emissão', default=timezone.now)
    data_validade = models.DateField('Data de Validade', null=True, blank=True, db_column='data_validade')
    activo = models.BooleanField('Activo', default=True)
    emitido_por = models.ForeignKey(
        Utilizador, on_delete=models.SET_NULL, null=True,
        related_name='titulos_emitidos', verbose_name='Emitido por',
        db_column='id_utilizador'
    )
    observacoes = models.TextField('Observações', blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Título de Propriedade'
        verbose_name_plural = 'Títulos de Propriedade'
        db_table = 'titulo_propriedade'

    def __str__(self):
        return f"{self.numero_titulo} — {self.embarcacao.nome}"


class Vistoria(models.Model):
    """Vistoria técnica realizada a uma embarcação."""

    RESULTADO_CHOICES = [
        ('aprovada', 'Aprovada'),
        ('reprovada', 'Reprovada'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_vistoria')
    embarcacao = models.ForeignKey(
        Embarcacao, on_delete=models.CASCADE,
        related_name='vistorias', verbose_name='Embarcação',
        db_column='id_embarcacao'
    )
    inspector = models.ForeignKey(
        Utilizador, on_delete=models.SET_NULL, null=True,
        related_name='vistorias_realizadas', verbose_name='Inspector',
        db_column='id_utilizador'
    )
    data_vistoria = models.DateField('Data da Vistoria', default=timezone.now)
    proxima_vistoria = models.DateField(
        'Próxima Vistoria', null=True, blank=True,
        db_column='data_proxima_vistoria'
    )
    resultado = models.CharField(
        'Resultado', max_length=20, choices=RESULTADO_CHOICES
    )
    observacoes = models.TextField('Observações', blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Vistoria'
        verbose_name_plural = 'Vistorias'
        db_table = 'vistoria'
        ordering = ['-data_vistoria']

    def __str__(self):
        return f"Vistoria {self.data_vistoria} — {self.embarcacao.nome}"


class Manutencao(models.Model):
    """Registo de manutenção de uma embarcação."""

    TIPO_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('correctiva', 'Correctiva'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_manutencao')
    embarcacao = models.ForeignKey(
        Embarcacao, on_delete=models.CASCADE,
        related_name='manutencoes', verbose_name='Embarcação',
        db_column='id_embarcacao'
    )
    descricao = models.CharField('Descrição', max_length=255)
    data_manutencao = models.DateField(
        'Data da Manutenção', default=timezone.now
    )
    custo = models.DecimalField(
        'Custo (MZN)', max_digits=10, decimal_places=2, default=0
    )
    tipo_manutencao = models.CharField(
        'Tipo de Manutenção', max_length=20,
        choices=TIPO_CHOICES, default='preventiva'
    )
    observacoes = models.TextField('Observações', blank=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        db_table = 'manutencao'
        ordering = ['-data_manutencao']

    def __str__(self):
        return f"{self.descricao} — {self.embarcacao.nome}"


class Alerta(models.Model):
    """Alerta/notificação enviada ao utilizador via SMS ou e-mail."""

    TIPO_CHOICES = [
        ('licenca_pronta', 'Licença Pronta'),
        ('titulo_pronto', 'Título Pronto'),
        ('licenca_expirando', 'Licença a Expirar'),
        ('vistoria_expirando', 'Vistoria a Expirar'),
        ('relatorio', 'Relatório Gerado'),
    ]
    CANAL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'E-mail'),
        ('ambos', 'Ambos'),
    ]
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('pendente', 'Pendente'),
        ('falhou', 'Falhou'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_alerta')
    embarcacao = models.ForeignKey(
        Embarcacao, on_delete=models.CASCADE,
        related_name='alertas', verbose_name='Embarcação',
        null=True, blank=True,
        db_column='id_embarcacao'
    )
    destinatario = models.ForeignKey(
        Utilizador, on_delete=models.CASCADE,
        related_name='alertas_recebidos', verbose_name='Destinatário',
        db_column='id_utilizador'
    )
    tipo_alerta = models.CharField(
        'Tipo de Alerta', max_length=30, choices=TIPO_CHOICES
    )
    mensagem = models.TextField('Mensagem')
    canal = models.CharField(
        'Canal', max_length=10, choices=CANAL_CHOICES, default='ambos'
    )
    numero_telefone = models.CharField('Telefone', max_length=20, blank=True)
    email_destino = models.EmailField('E-mail Destino', blank=True)
    estado = models.CharField(
        'Estado', max_length=10, choices=ESTADO_CHOICES, default='pendente'
    )
    data_envio = models.DateTimeField('Data de Envio', null=True, blank=True)
    configuracao = models.ForeignKey(
        'ConfiguracaoAlerta', on_delete=models.SET_NULL,
        related_name='alertas_gerados', verbose_name='Configuração de Alerta',
        null=True, blank=True,
        db_column='id_configuracao_alerta'
    )
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        db_table = 'alerta'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.get_tipo_alerta_display()} — {self.destinatario.nome_completo}"


class ConfiguracaoAlerta(models.Model):
    """Configuração de alertas automáticos de expiração."""

    CANAL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'E-mail'),
        ('ambos', 'Ambos'),
    ]

    id = models.AutoField(primary_key=True, db_column='id_configuracao_alerta')
    utilizador = models.ForeignKey(
        Utilizador, on_delete=models.CASCADE,
        related_name='configuracoes_alerta', verbose_name='Utilizador',
        null=True, blank=True,
        db_column='id_utilizador'
    )
    tipo_documento = models.CharField(
        'Tipo de Documento', max_length=20,
        choices=[('licenca', 'Licença de Navegação'), ('vistoria', 'Vistoria')],
        default='licenca'
    )
    dias_antecedencia = models.IntegerField(
        'Dias de Antecedência', default=30,
        help_text='Enviar alerta X dias antes da expiração'
    )
    canal = models.CharField(
        'Canal de Envio', max_length=10,
        choices=CANAL_CHOICES, default='ambos'
    )
    activo = models.BooleanField('Activo', default=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Configuração de Alerta'
        verbose_name_plural = 'Configurações de Alerta'
        db_table = 'configuracao_alerta'

    def __str__(self):
        return f"Alertar {self.dias_antecedencia} dias antes via {self.get_canal_display()}"

"""Formulários do Sistema de Gestão de Barcos — INTRANSMAR."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Utilizador, Embarcacao, LicencaNavegacao,
    TituloPropriedade, Vistoria, Manutencao, ConfiguracaoAlerta
)


class RegistoUtilizadorForm(UserCreationForm):
    """Formulário de registo para novos pescadores."""

    nome_completo = forms.CharField(
        max_length=255, label='Nome Completo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'})
    )
    email = forms.EmailField(
        label='E-mail Gmail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seuemail@gmail.com'})
    )
    telefone = forms.CharField(
        max_length=20, label='Telefone (+258)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+258 84 XXX XXXX'})
    )
    numero_documento = forms.CharField(
        max_length=50, label='Nº Documento (BI/NUIT)', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do BI ou NUIT'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crie uma senha'})
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'})
    )

    class Meta:
        model = Utilizador
        fields = ['nome_completo', 'email', 'telefone', 'numero_documento', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]
        user.tipo_utilizador = 'pescador'
        user.activo = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Formulário de login."""

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seuemail@gmail.com'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'})
    )


class EmbarcacaoForm(forms.ModelForm):
    """Formulário de registo/edição de embarcação."""

    class Meta:
        model = Embarcacao
        fields = [
            'nome', 'numero_matricula', 'tipo_embarcacao',
            'comprimento', 'potencia_motor', 'ano_construcao',
            'material', 'observacoes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_embarcacao': forms.Select(attrs={'class': 'form-select'}),
            'comprimento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'max': '10'}),
            'potencia_motor': forms.NumberInput(attrs={'class': 'form-control', 'max': '100'}),
            'ano_construcao': forms.NumberInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_comprimento(self):
        valor = self.cleaned_data.get('comprimento')
        if valor and valor > 10:
            raise forms.ValidationError('Embarcação artesanal: comprimento máximo de 10 metros.')
        return valor

    def clean_potencia_motor(self):
        valor = self.cleaned_data.get('potencia_motor')
        if valor and valor > 100:
            raise forms.ValidationError('Embarcação artesanal: potência máxima de 100 CV.')
        return valor


class LicencaNavegacaoForm(forms.ModelForm):
    """Formulário para emitir licença de navegação."""

    class Meta:
        model = LicencaNavegacao
        fields = ['ano_referencia', 'observacoes']
        widgets = {
            'ano_referencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TituloPropriedadeForm(forms.ModelForm):
    """Formulário para emitir título de propriedade."""

    class Meta:
        model = TituloPropriedade
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VistoriaForm(forms.ModelForm):
    """Formulário de registo de vistoria."""

    class Meta:
        model = Vistoria
        fields = ['embarcacao', 'data_vistoria', 'proxima_vistoria', 'resultado', 'observacoes']
        widgets = {
            'embarcacao': forms.Select(attrs={'class': 'form-select'}),
            'data_vistoria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proxima_vistoria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resultado': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ManutencaoForm(forms.ModelForm):
    """Formulário de registo de manutenção."""

    class Meta:
        model = Manutencao
        fields = ['embarcacao', 'descricao', 'data_manutencao', 'custo', 'tipo_manutencao', 'observacoes']
        widgets = {
            'embarcacao': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'data_manutencao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tipo_manutencao': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ConfiguracaoAlertaForm(forms.ModelForm):
    """Formulário de configuração de alertas."""

    class Meta:
        model = ConfiguracaoAlerta
        fields = ['dias_antecedencia', 'canal', 'activo']
        widgets = {
            'dias_antecedencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'canal': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PerfilForm(forms.ModelForm):
    """Formulário de edição do perfil."""

    class Meta:
        model = Utilizador
        fields = ['nome_completo', 'email', 'telefone', 'numero_documento']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BuscaAvancadaForm(forms.Form):
    """Formulário de busca avançada de embarcações."""

    numero_matricula = forms.CharField(
        max_length=50, required=False, label='Nº Matrícula',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'})
    )
    nome_embarcacao = forms.CharField(
        max_length=100, required=False, label='Nome da Embarcação',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do barco'})
    )
    nome_proprietario = forms.CharField(
        max_length=255, required=False, label='Proprietário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do proprietário'})
    )
    estado_licenca = forms.ChoiceField(
        required=False, label='Estado da Licença',
        choices=[('', 'Todos'), ('activa', 'Activa'), ('expirando', 'A Expirar'), ('expirada', 'Expirada')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo_embarcacao = forms.ChoiceField(
        required=False, label='Tipo de Embarcação',
        choices=[('', 'Todos')] + Embarcacao.TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

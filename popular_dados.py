import os
import django
import datetime

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_barcos.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Utilizador, Embarcacao, LicencaNavegacao, TituloPropriedade, Vistoria, ConfiguracaoAlerta

def popular():
    print("Iniciando a criação de dados de demonstração...")
    
    # 1. Criar utilizadores
    print("Criando utilizadores padrão...")
    
    # Admin
    admin, created = Utilizador.objects.get_or_create(
        email='admin@gmail.com',
        defaults={
            'username': 'admin',
            'nome_completo': 'Administrador do Sistema',
            'telefone': '+258841111111',
            'tipo_utilizador': 'admin',
            'numero_documento': 'BI01928374M',
            'is_superuser': True,
            'is_staff': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("  -> Admin criado: admin@gmail.com / admin123")
        
    # Funcionário INTRANSMAR
    funcionario, created = Utilizador.objects.get_or_create(
        email='intransmar@gmail.com',
        defaults={
            'username': 'intransmar',
            'nome_completo': 'João da INTRANSMAR',
            'telefone': '+258842222222',
            'tipo_utilizador': 'intransmar',
            'numero_documento': 'BI09876543K'
        }
    )
    if created:
        funcionario.set_password('intransmar123')
        funcionario.save()
        print("  -> Funcionário INTRANSMAR criado: intransmar@gmail.com / intransmar123")
        
    # Pescador / Proprietário
    pescador, created = Utilizador.objects.get_or_create(
        email='pescador@gmail.com',
        defaults={
            'username': 'pescador',
            'nome_completo': 'Manuel Silva Pescador',
            'telefone': '+258843333333',
            'tipo_utilizador': 'pescador',
            'numero_documento': 'BI11223344J'
        }
    )
    if created:
        pescador.set_password('pescador123')
        pescador.save()
        print("  -> Pescador criado: pescador@gmail.com / pescador123")

    # 2. Criar Configuração de Alertas
    config_alerta, created = ConfiguracaoAlerta.objects.get_or_create(
        dias_antecedencia=30,
        defaults={
            'canal': 'ambos',
            'activo': True
        }
    )
    if created:
        print("  -> Configuração de Alerta padrão criada (30 dias antes, via SMS e Email)")

    # 3. Criar Embarcações
    print("Criando embarcações de exemplo...")
    
    # Barco 1: Aprovado com Licença e Título
    b1, created = Embarcacao.objects.get_or_create(
        numero_matricula='MC-001-B',
        defaults={
            'nome': 'Estrela do Mar',
            'tipo_embarcacao': 'canoa_motor',
            'comprimento': 8.5,
            'potencia_motor': 40,
            'ano_construcao': 2022,
            'material': 'fibra',
            'proprietario': pescador,
            'estado_registo': 'aprovado',
            'observacoes': 'Barco em bom estado de conservação.'
        }
    )
    if created:
        print("  -> Embarcação 'Estrela do Mar' criada.")
        
        # Emitir Título de Propriedade
        t1 = TituloPropriedade.objects.create(
            embarcacao=b1,
            numero_titulo='TP-2026-000001',
            data_emissao=datetime.date.today(),
            activo=True,
            emitido_por=funcionario
        )
        print("    -> Título de Propriedade permanente emitido.")
        
        # Emitir Licença de Navegação
        l1 = LicencaNavegacao.objects.create(
            embarcacao=b1,
            numero_licenca='LN-2026-000001',
            data_emissao=datetime.date.today(),
            ano_referencia=2026,
            activa=True,
            emitida_por=funcionario
        )
        print("    -> Licença de Navegação anual (até 31/12/2026) emitida.")

        # Registar Vistoria
        v1 = Vistoria.objects.create(
            embarcacao=b1,
            inspector=funcionario,
            data_vistoria=datetime.date.today(),
            proxima_vistoria=datetime.date.today() + datetime.timedelta(days=180),
            resultado='aprovada',
            observacoes='Equipamentos de segurança válidos.'
        )
        print("    -> Vistoria aprovada registada.")

    # Barco 2: Pendente de Aprovação
    b2, created = Embarcacao.objects.get_or_create(
        numero_matricula='MC-002-B',
        defaults={
            'nome': 'Vento Leste',
            'tipo_embarcacao': 'canoa',
            'comprimento': 6.2,
            'potencia_motor': 0,
            'ano_construcao': 2024,
            'material': 'madeira',
            'proprietario': pescador,
            'estado_registo': 'pendente',
            'observacoes': 'Aguardando vistoria inicial.'
        }
    )
    if created:
        print("  -> Embarcação 'Vento Leste' criada (Pendente de Aprovação).")

    print("\nDados populados com sucesso!")

if __name__ == "__main__":
    popular()

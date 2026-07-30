"""Comando para verificar e enviar alertas automáticos de expiração."""

import datetime
import logging
from django.core.management.base import BaseCommand
from core.models import LicencaNavegacao, Vistoria, ConfiguracaoAlerta, Embarcacao
from core.services.notificacao_service import notificar_expiracao

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Verifica licenças e vistorias a expirar e envia alertas automáticos baseados nas preferências do utilizador ou globais'

    def handle(self, *args, **options):
        self.stdout.write('A verificar alertas de expiracao...')
        
        # Obter configurações globais padrão
        global_licenca = ConfiguracaoAlerta.objects.filter(activo=True, utilizador=None, tipo_documento='licenca').first()
        global_vistoria = ConfiguracaoAlerta.objects.filter(activo=True, utilizador=None, tipo_documento='vistoria').first()

        # Se não houver configurações globais, criamos uma de fallback implícita
        if not global_licenca:
            global_licenca = ConfiguracaoAlerta(dias_antecedencia=30, canal='ambos', activo=True, tipo_documento='licenca')
        if not global_vistoria:
            global_vistoria = ConfiguracaoAlerta(dias_antecedencia=30, canal='ambos', activo=True, tipo_documento='vistoria')

        hoje = datetime.date.today()
        total_enviados = 0

        # Iterar por todas as embarcações aprovadas
        embarcacoes = Embarcacao.objects.filter(estado_registo='aprovado')

        for emb in embarcacoes:
            prop = emb.proprietario
            
            # Buscar a configuração de alerta customizada do proprietário ou usar a global
            lic_config = ConfiguracaoAlerta.objects.filter(
                activo=True, utilizador=prop, tipo_documento='licenca'
            ).first() or global_licenca
            
            vist_config = ConfiguracaoAlerta.objects.filter(
                activo=True, utilizador=prop, tipo_documento='vistoria'
            ).first() or global_vistoria

            # 1. Verificar Licença de Navegação
            licenca = emb.licenca_activa
            if licenca and lic_config.activo:
                data_limite_lic = hoje + datetime.timedelta(days=lic_config.dias_antecedencia)
                if hoje <= licenca.data_validade <= data_limite_lic:
                    dias = (licenca.data_validade - hoje).days
                    notificar_expiracao(
                        destinatario=prop,
                        tipo_alerta='licenca_expirando',
                        embarcacao=emb,
                        documento_info={
                            'numero': licenca.numero_licenca,
                            'data_validade': licenca.data_validade.strftime('%d/%m/%Y'),
                            'dias_restantes': dias,
                        },
                        configuracao=lic_config if lic_config.pk else None
                    )
                    total_enviados += 1
                    self.stdout.write(f'  SMS/Email: Licenca {licenca.numero_licenca} - {dias} dias - {prop.nome_completo}')

            # 2. Verificar Vistoria
            # Pegar a última vistoria do barco
            vistoria = emb.vistorias.order_by('-data_vistoria').first()
            if vistoria and vist_config.activo and vistoria.proxima_vistoria:
                data_limite_vist = hoje + datetime.timedelta(days=vist_config.dias_antecedencia)
                if hoje <= vistoria.proxima_vistoria <= data_limite_vist:
                    dias = (vistoria.proxima_vistoria - hoje).days
                    notificar_expiracao(
                        destinatario=prop,
                        tipo_alerta='vistoria_expirando',
                        embarcacao=emb,
                        documento_info={
                            'numero': f'Vistoria de {vistoria.data_vistoria.strftime("%d/%m/%Y")}',
                            'data_validade': vistoria.proxima_vistoria.strftime('%d/%m/%Y'),
                            'dias_restantes': dias,
                        },
                        configuracao=vist_config if vist_config.pk else None
                    )
                    total_enviados += 1
                    self.stdout.write(f'  SMS/Email: Vistoria {emb.nome} - {dias} dias - {prop.nome_completo}')

        self.stdout.write(self.style.SUCCESS(f'Check concluido: {total_enviados} alerta(s) processado(s).'))

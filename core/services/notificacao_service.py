"""Serviço unificado de notificações — SMS + E-mail."""

import logging
from django.utils import timezone
from core.models import Alerta

logger = logging.getLogger(__name__)


def notificar_documento_pronto(tipo, documento):
    """
    Envia SMS + E-mail ao proprietário quando um documento fica pronto.

    Args:
        tipo: 'licenca_pronta' ou 'titulo_pronto'
        documento: Instância de LicencaNavegacao ou TituloPropriedade
    """
    from .sms_service import enviar_sms
    from .email_service import enviar_notificacao_licenca, enviar_notificacao_titulo

    proprietario = documento.embarcacao.proprietario
    embarcacao = documento.embarcacao

    # Definir mensagem SMS
    if tipo == 'licenca_pronta':
        numero = documento.numero_licenca
        msg_sms = (
            f"INTRANSMAR: A sua Licenca de Navegacao {numero} "
            f"para a embarcacao {embarcacao.nome} foi emitida. "
            f"Valida ate 31/12/{documento.ano_referencia}."
        )
    elif tipo == 'titulo_pronto':
        numero = documento.numero_titulo
        msg_sms = (
            f"INTRANSMAR: O Titulo de Propriedade {numero} "
            f"da embarcacao {embarcacao.nome} foi emitido. "
            f"Documento permanente (sem prazo)."
        )
    else:
        return

    # Criar registo de alerta
    alerta = Alerta.objects.create(
        embarcacao=embarcacao,
        destinatario=proprietario,
        tipo_alerta=tipo,
        mensagem=msg_sms,
        canal='ambos',
        numero_telefone=proprietario.telefone,
        email_destino=proprietario.email,
        estado='pendente',
    )

    # Enviar SMS
    resultado_sms = enviar_sms(proprietario.telefone, msg_sms)

    # Enviar E-mail com PDF
    if tipo == 'licenca_pronta':
        resultado_email = enviar_notificacao_licenca(documento)
    else:
        resultado_email = enviar_notificacao_titulo(documento)

    # Actualizar estado do alerta
    sms_ok = resultado_sms.get('sucesso', False)
    email_ok = resultado_email.get('sucesso', False)

    if sms_ok or email_ok:
        alerta.estado = 'enviado'
        alerta.data_envio = timezone.now()
    else:
        alerta.estado = 'falhou'
    alerta.save()

    logger.info(f"Notificação {tipo}: SMS={'OK' if sms_ok else 'FALHOU'}, Email={'OK' if email_ok else 'FALHOU'}")
    return alerta


def notificar_expiracao(destinatario, tipo_alerta, embarcacao, documento_info, configuracao=None):
    """
    Envia alerta de expiração via SMS + E-mail.

    Args:
        destinatario: Instância de Utilizador
        tipo_alerta: 'licenca_expirando' ou 'vistoria_expirando'
        embarcacao: Instância de Embarcacao
        documento_info: Dict com dados do documento (numero, data_validade, dias_restantes)
        configuracao: Instância de ConfiguracaoAlerta (opcional)
    """
    from .sms_service import enviar_sms
    from .email_service import enviar_email

    dias = documento_info.get('dias_restantes', 0)
    canal = configuracao.canal if configuracao else 'ambos'

    if tipo_alerta == 'licenca_expirando':
        msg_sms = (
            f"INTRANSMAR ALERTA: A Licenca de Navegacao {documento_info['numero']} "
            f"da embarcacao {embarcacao.nome} expira em {dias} dias "
            f"({documento_info['data_validade']}). Renove a sua licenca."
        )
        assunto = f"⚠️ Licença a Expirar — {embarcacao.nome}"
    else:
        msg_sms = (
            f"INTRANSMAR ALERTA: A Vistoria da embarcacao {embarcacao.nome} "
            f"expira em {dias} dias ({documento_info['data_validade']}). "
            f"Agende uma nova vistoria."
        )
        assunto = f"⚠️ Vistoria a Expirar — {embarcacao.nome}"

    mensagem_html = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; color: #4A5568;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #E8834A; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h2>⚠️ ALERTA — INTRANSMAR</h2>
            </div>
            <div style="background: white; padding: 30px; border: 1px solid #e2e8f0;">
                <p>Prezado(a) <strong>{destinatario.nome_completo}</strong>,</p>
                <p>{msg_sms}</p>
                <p>Dirija-se à INTRANSMAR — Delegação da Beira para regularizar a sua situação.</p>
            </div>
            <div style="background: #F5F0E8; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; font-size: 12px;">
                INTRANSMAR — Delegação da Beira, Moçambique
            </div>
        </div>
    </body>
    </html>
    """

    # Criar alerta
    alerta = Alerta.objects.create(
        embarcacao=embarcacao,
        destinatario=destinatario,
        tipo_alerta=tipo_alerta,
        mensagem=msg_sms,
        canal=canal,
        numero_telefone=destinatario.telefone,
        email_destino=destinatario.email,
        estado='pendente',
        configuracao=configuracao,
    )

    resultado_sms = enviar_sms(destinatario.telefone, msg_sms)
    resultado_email = enviar_email(destinatario.email, assunto, mensagem_html)

    sms_ok = resultado_sms.get('sucesso', False)
    email_ok = resultado_email.get('sucesso', False)

    if sms_ok or email_ok:
        alerta.estado = 'enviado'
        alerta.data_envio = timezone.now()
    else:
        alerta.estado = 'falhou'
    alerta.save()

    return alerta

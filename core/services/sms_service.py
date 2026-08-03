"""Serviço de envio de SMS via MozeSMS — Moçambique (+258)."""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_sms(telefone, mensagem):
    """
    Envia SMS via API REST do MozeSMS.

    Args:
        telefone: Número no formato +258XXXXXXXXX ou 258XXXXXXXXX
        mensagem: Texto da mensagem (máx. 160 caracteres para 1 segmento)

    Returns:
        dict com 'sucesso' (bool) e 'resposta' ou 'erro'
    """
    # Verificar se as credenciais estão configuradas
    if not settings.MOZESMS_API_KEY or settings.MOZESMS_API_KEY == 'your_api_key_here':
        logger.warning(f"MozeSMS não configurado. SMS para {telefone} registado mas não enviado.")
        return {'sucesso': False, 'erro': 'MozeSMS não configurado. Configure MOZESMS_API_KEY no .env'}

    # Formatar o número (remover + se existir)
    numero_formatado = telefone.replace('+', '').replace(' ', '')
    if not numero_formatado.startswith('258'):
        numero_formatado = '258' + numero_formatado

    url = "https://api.mozesms.com/v1/sms/send"
    
    # Se o SENDER_ID estiver vazio, usar o padrão da plataforma
    sender_id = getattr(settings, 'MOZESMS_SENDER_ID', None)
    if not sender_id:
        sender_id = "MozeSMS"
        
    payload = {
        "to": numero_formatado,
        "message": mensagem,
        "from": sender_id
    }
    headers = {
        "X-API-Key": settings.MOZESMS_API_KEY,
        "X-API-Secret": settings.MOZESMS_API_SECRET,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        dados = response.json()
        logger.info(f"SMS enviado com sucesso para {telefone}: {dados}")
        return {'sucesso': True, 'resposta': dados}
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar SMS para {telefone}: {e}")
        return {'sucesso': False, 'erro': str(e)}

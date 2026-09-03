"""Serviço de envio de e-mails via Gmail SMTP."""

import logging
from io import BytesIO
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_email(destinatario_email, assunto, mensagem_html, anexo_pdf_bytes=None, nome_anexo=None):
    """
    Envia e-mail via Gmail SMTP usando formato multipart (texto puro + HTML)
    para garantir alta entregabilidade e evitar filtros de spam.

    Args:
        destinatario_email: E-mail do destinatário
        assunto: Assunto do e-mail
        mensagem_html: Corpo do e-mail em HTML
        anexo_pdf_bytes: BytesIO do PDF a anexar (opcional)
        nome_anexo: Nome do ficheiro PDF (opcional)

    Returns:
        dict com 'sucesso' (bool) e 'erro' se falhou
    """
    if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == 'sistema.barcos@gmail.com':
        logger.warning(f"Gmail SMTP não configurado. E-mail para {destinatario_email} não enviado.")
        return {'sucesso': False, 'erro': 'Gmail SMTP não configurado. Configure EMAIL_HOST_USER no .env'}

    try:
        # Gerar versão em texto simples alternativa para filtros antispam
        corpo_texto = strip_tags(mensagem_html).strip()

        email = EmailMultiAlternatives(
            subject=assunto,
            body=corpo_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destinatario_email],
        )
        email.attach_alternative(mensagem_html, 'text/html')

        # Anexar PDF se fornecido
        if anexo_pdf_bytes and nome_anexo:
            if isinstance(anexo_pdf_bytes, BytesIO):
                anexo_pdf_bytes.seek(0)
                email.attach(nome_anexo, anexo_pdf_bytes.read(), 'application/pdf')
            else:
                email.attach(nome_anexo, anexo_pdf_bytes, 'application/pdf')

        email.send(fail_silently=False)
        logger.info(f"E-mail enviado com sucesso para {destinatario_email}: {assunto}")
        return {'sucesso': True}
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {destinatario_email}: {e}")
        return {'sucesso': False, 'erro': str(e)}


def enviar_notificacao_licenca(licenca):
    """Envia e-mail ao proprietário quando a licença de navegação é emitida."""
    from .pdf_service import gerar_pdf_licenca

    proprietario = licenca.embarcacao.proprietario
    pdf_bytes = gerar_pdf_licenca(licenca)
    assunto = f"Licença de Navegação Emitida — {licenca.numero_licenca}"
    mensagem = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; color: #4A5568;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #063B4F; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h2>⚓ INTRANSMAR</h2>
                <p>Sistema de Gestão de Barcos — Beira</p>
            </div>
            <div style="background: white; padding: 30px; border: 1px solid #e2e8f0;">
                <h3 style="color: #0A6B8A;">Licença de Navegação Emitida ✅</h3>
                <p>Prezado(a) <strong>{proprietario.nome_completo}</strong>,</p>
                <p>A sua Licença de Navegação foi emitida com sucesso:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Nº Licença:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{licenca.numero_licenca}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Embarcação:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{licenca.embarcacao.nome}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Matrícula:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{licenca.embarcacao.numero_matricula}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Data de Emissão:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{licenca.data_emissao.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Válida até:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{licenca.data_validade.strftime('%d/%m/%Y')}</td></tr>
                </table>
                <p>O PDF da licença encontra-se em anexo.</p>
            </div>
            <div style="background: #F5F0E8; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; font-size: 12px; color: #718096;">
                INTRANSMAR — Delegação da Beira, Moçambique
            </div>
        </div>
    </body>
    </html>
    """
    return enviar_email(
        proprietario.email, assunto, mensagem,
        anexo_pdf_bytes=pdf_bytes,
        nome_anexo=f"Licenca_{licenca.numero_licenca}.pdf"
    )


def enviar_notificacao_titulo(titulo):
    """Envia e-mail ao proprietário quando o título de propriedade é emitido."""
    from .pdf_service import gerar_pdf_titulo

    proprietario = titulo.embarcacao.proprietario
    pdf_bytes = gerar_pdf_titulo(titulo)
    assunto = f"Título de Propriedade Emitido — {titulo.numero_titulo}"
    mensagem = f"""
    <html>
    <body style="font-family: 'Inter', sans-serif; color: #4A5568;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #063B4F; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h2>⚓ INTRANSMAR</h2>
                <p>Sistema de Gestão de Barcos — Beira</p>
            </div>
            <div style="background: white; padding: 30px; border: 1px solid #e2e8f0;">
                <h3 style="color: #0A6B8A;">Título de Propriedade Emitido ✅</h3>
                <p>Prezado(a) <strong>{proprietario.nome_completo}</strong>,</p>
                <p>O Título de Propriedade da sua embarcação foi emitido com sucesso:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Nº Título:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{titulo.numero_titulo}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Embarcação:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{titulo.embarcacao.nome}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Matrícula:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{titulo.embarcacao.numero_matricula}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Data de Emissão:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{titulo.data_emissao.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Validade:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>SEM PRAZO (Permanente)</strong></td></tr>
                </table>
                <p>O PDF do título encontra-se em anexo.</p>
            </div>
            <div style="background: #F5F0E8; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; font-size: 12px; color: #718096;">
                INTRANSMAR — Delegação da Beira, Moçambique
            </div>
        </div>
    </body>
    </html>
    """
    return enviar_email(
        proprietario.email, assunto, mensagem,
        anexo_pdf_bytes=pdf_bytes,
        nome_anexo=f"Titulo_{titulo.numero_titulo}.pdf"
    )

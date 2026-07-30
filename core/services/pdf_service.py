"""Serviço de geração de PDFs — Licenças, Títulos e Relatórios."""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def _estilos_base():
    """Retorna os estilos base para os PDFs."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='TituloDoc', fontSize=16, leading=20,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#063B4F')
    ))
    styles.add(ParagraphStyle(
        name='Subtitulo', fontSize=12, leading=16,
        alignment=TA_CENTER, fontName='Helvetica',
        textColor=colors.HexColor('#0A6B8A')
    ))
    styles.add(ParagraphStyle(
        name='Cabecalho', fontSize=14, leading=18,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#063B4F')
    ))
    styles.add(ParagraphStyle(
        name='Seccao', fontSize=11, leading=14,
        fontName='Helvetica-Bold', textColor=colors.HexColor('#0A6B8A'),
        spaceBefore=12, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='Campo', fontSize=10, leading=13,
        fontName='Helvetica', textColor=colors.HexColor('#4A5568')
    ))
    return styles


def _cabecalho(elements, styles):
    """Adiciona o cabeçalho INTRANSMAR ao PDF."""
    elements.append(Paragraph("REPÚBLICA DE MOÇAMBIQUE", styles['Subtitulo']))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph("⚓ INTRANSMAR ⚓", styles['TituloDoc']))
    elements.append(Paragraph("Delegação da Beira", styles['Subtitulo']))
    elements.append(Spacer(1, 6 * mm))
    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor('#0A6B8A'), spaceAfter=10
    ))


def gerar_pdf_licenca(licenca):
    """
    Gera o PDF da Licença de Navegação.

    Args:
        licenca: Instância de LicencaNavegacao

    Returns:
        BytesIO com o conteúdo do PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm
    )
    styles = _estilos_base()
    elements = []

    # Cabeçalho
    _cabecalho(elements, styles)

    # Título do documento
    elements.append(Paragraph("LICENÇA DE NAVEGAÇÃO ARTESANAL", styles['Cabecalho']))
    elements.append(Spacer(1, 8 * mm))

    # Número da licença
    elements.append(Paragraph(f"Nº Licença: <b>{licenca.numero_licenca}</b>", styles['Campo']))
    elements.append(Spacer(1, 6 * mm))

    # Dados do proprietário
    prop = licenca.embarcacao.proprietario
    elements.append(Paragraph("PROPRIETÁRIO", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_prop = [
        ['Nome:', prop.nome_completo],
        ['Documento:', prop.numero_documento or 'N/A'],
        ['Telefone:', prop.telefone],
        ['E-mail:', prop.email],
    ]
    tabela_prop = Table(dados_prop, colWidths=[4 * cm, 12 * cm])
    tabela_prop.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(tabela_prop)
    elements.append(Spacer(1, 6 * mm))

    # Dados da embarcação
    emb = licenca.embarcacao
    elements.append(Paragraph("EMBARCAÇÃO", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_emb = [
        ['Nome:', emb.nome],
        ['Matrícula:', emb.numero_matricula],
        ['Tipo:', emb.get_tipo_embarcacao_display()],
        ['Comprimento:', f'{emb.comprimento} m'],
        ['Potência Motor:', f'{emb.potencia_motor} CV' if emb.potencia_motor else 'Sem motor'],
        ['Material:', emb.get_material_display()],
        ['Ano de Construção:', str(emb.ano_construcao)],
    ]
    tabela_emb = Table(dados_emb, colWidths=[4 * cm, 12 * cm])
    tabela_emb.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(tabela_emb)
    elements.append(Spacer(1, 8 * mm))

    # Validade
    elements.append(Paragraph("VALIDADE", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_val = [
        ['Data de Emissão:', licenca.data_emissao.strftime('%d/%m/%Y')],
        ['Válida até:', licenca.data_validade.strftime('%d/%m/%Y')],
        ['Estado:', 'ACTIVA' if licenca.activa else 'INACTIVA'],
    ]
    tabela_val = Table(dados_val, colWidths=[4 * cm, 12 * cm])
    tabela_val.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#2A9D6F') if licenca.activa else colors.HexColor('#D94F4F')),
        ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(tabela_val)
    elements.append(Spacer(1, 20 * mm))

    # Assinatura
    elements.append(HRFlowable(width="40%", thickness=1, color=colors.HexColor('#063B4F')))
    elements.append(Paragraph("Responsável INTRANSMAR", styles['Campo']))
    elements.append(Paragraph("Delegação da Beira", styles['Campo']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def gerar_pdf_titulo(titulo):
    """
    Gera o PDF do Título de Propriedade.

    Args:
        titulo: Instância de TituloPropriedade

    Returns:
        BytesIO com o conteúdo do PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm
    )
    styles = _estilos_base()
    elements = []

    _cabecalho(elements, styles)

    elements.append(Paragraph("TÍTULO DE PROPRIEDADE DE EMBARCAÇÃO", styles['Cabecalho']))
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph(f"Nº Título: <b>{titulo.numero_titulo}</b>", styles['Campo']))
    elements.append(Spacer(1, 6 * mm))

    # Proprietário
    prop = titulo.embarcacao.proprietario
    elements.append(Paragraph("PROPRIETÁRIO", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_prop = [
        ['Nome:', prop.nome_completo],
        ['Documento:', prop.numero_documento or 'N/A'],
        ['Telefone:', prop.telefone],
        ['E-mail:', prop.email],
    ]
    tabela = Table(dados_prop, colWidths=[4 * cm, 12 * cm])
    tabela.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabela)
    elements.append(Spacer(1, 6 * mm))

    # Embarcação
    emb = titulo.embarcacao
    elements.append(Paragraph("EMBARCAÇÃO", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_emb = [
        ['Nome:', emb.nome],
        ['Matrícula:', emb.numero_matricula],
        ['Tipo:', emb.get_tipo_embarcacao_display()],
        ['Comprimento:', f'{emb.comprimento} m'],
        ['Potência Motor:', f'{emb.potencia_motor} CV' if emb.potencia_motor else 'Sem motor'],
        ['Material:', emb.get_material_display()],
        ['Ano de Construção:', str(emb.ano_construcao)],
    ]
    tabela2 = Table(dados_emb, colWidths=[4 * cm, 12 * cm])
    tabela2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabela2)
    elements.append(Spacer(1, 8 * mm))

    # Validade
    elements.append(Paragraph("VALIDADE", styles['Seccao']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0A6B8A')))

    dados_val = [
        ['Data de Emissão:', titulo.data_emissao.strftime('%d/%m/%Y')],
        ['Validade:', 'SEM PRAZO (Documento Permanente)'],
    ]
    tabela3 = Table(dados_val, colWidths=[4 * cm, 12 * cm])
    tabela3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4A5568')),
        ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#2A9D6F')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabela3)
    elements.append(Spacer(1, 20 * mm))

    elements.append(HRFlowable(width="40%", thickness=1, color=colors.HexColor('#063B4F')))
    elements.append(Paragraph("Responsável INTRANSMAR", styles['Campo']))
    elements.append(Paragraph("Delegação da Beira", styles['Campo']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def gerar_pdf_relatorio(embarcacoes, titulo_relatorio="Relatório de Embarcações"):
    """
    Gera relatório consolidado em PDF.

    Args:
        embarcacoes: QuerySet de embarcações
        titulo_relatorio: Título do relatório

    Returns:
        BytesIO com o conteúdo do PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=1.5 * cm, leftMargin=1.5 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm
    )
    styles = _estilos_base()
    elements = []

    _cabecalho(elements, styles)
    elements.append(Paragraph(titulo_relatorio.upper(), styles['Cabecalho']))
    elements.append(Spacer(1, 8 * mm))

    # Tabela de embarcações
    header = ['Nome', 'Matrícula', 'Tipo', 'Proprietário', 'Estado']
    dados = [header]
    for emb in embarcacoes:
        licenca = emb.licenca_activa
        estado_lic = licenca.estado if licenca else 'Sem licença'
        dados.append([
            emb.nome,
            emb.numero_matricula,
            emb.get_tipo_embarcacao_display(),
            emb.proprietario.nome_completo,
            estado_lic,
        ])

    tabela = Table(dados, colWidths=[3.5 * cm, 3 * cm, 3 * cm, 4.5 * cm, 3 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#063B4F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F0E8')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabela)
    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph(f"Total: {len(embarcacoes)} embarcação(ões)", styles['Campo']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

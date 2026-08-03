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
    Gera o PDF da Licença de Navegação no formato oficial da ITRANSMAR.

    Args:
        licenca: Instância de LicencaNavegacao

    Returns:
        BytesIO com o conteúdo do PDF
    """
    from reportlab.pdfgen import canvas
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4 # 595.27 x 841.89
    
    # Cores
    cor_pre_impresso = colors.HexColor('#5C6F77') # Verde/cinza desbotado oficial
    cor_preenchido = colors.HexColor('#063B4F')   # Azul escuro do sistema
    
    # 1. Marca de Água (Selo de Fundo Translúcido)
    c.saveState()
    c.setFillColor(colors.HexColor('#F2F4F5'))
    c.setStrokeColor(colors.HexColor('#F2F4F5'))
    c.setLineWidth(1)
    
    cx, cy = width / 2, height / 2 - 50
    c.circle(cx, cy, 110, stroke=True, fill=False)
    c.circle(cx, cy, 102, stroke=True, fill=False)
    
    # Desenho da Âncora central
    c.setLineWidth(3)
    c.line(cx, cy - 50, cx, cy + 50)
    c.line(cx - 35, cy + 25, cx + 35, cy + 25)
    c.circle(cx, cy + 55, 10, stroke=True, fill=False)
    
    p = c.beginPath()
    p.moveTo(cx - 55, cy - 15)
    p.arcTo(cx - 60, cy - 65, cx + 60, cy - 65, cx + 55, cy - 15)
    c.drawPath(p, stroke=True, fill=False)
    c.restoreState()
    
    # 2. Cabeçalho Oficial
    # Brasão do topo (Âncora e Timão)
    c.saveState()
    c.setStrokeColor(cor_pre_impresso)
    c.setLineWidth(1)
    c.circle(width/2, 775, 22, stroke=True, fill=False)
    c.circle(width/2, 775, 15, stroke=True, fill=False)
    c.circle(width/2, 775, 5, stroke=True, fill=True)
    for angle in range(0, 360, 45):
        c.saveState()
        c.translate(width/2, 775)
        c.rotate(angle)
        c.line(0, 0, 0, 20)
        c.restoreState()
    c.restoreState()
    
    c.saveState()
    c.setFillColor(cor_pre_impresso)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, 735, "ITRANSMAR, IP")
    
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(width/2, 725, "Autoridade Reguladora do Transporte Marítimo")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, 702, "INSTITUTO DE TRANSPORTE MARÍTIMO, IP")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, 683, "LICENÇA DE NAVEGAÇÃO")
    c.restoreState()
    
    # Número da Licença (Estilo carimbo vermelho oficial)
    c.saveState()
    c.setFillColor(colors.HexColor('#D94F4F'))
    c.setFont("Helvetica-Bold", 11)
    # Extrai a numeração serial simples para o topo
    numero_limpo = licenca.numero_licenca.split('-')[-1]
    c.drawString(425, 683, f"N.º {numero_limpo}")
    c.restoreState()
    
    # Helpers de desenho de campos
    def d_linha_pontilhada(x1, x2, y_l):
        c.saveState()
        c.setStrokeColor(colors.HexColor('#A0AEC0'))
        c.setLineWidth(0.5)
        c.setDash(1, 2)
        c.line(x1, y_l - 2, x2, y_l - 2)
        c.restoreState()
        
    def d_campo(label, val, x_label, x_val, x_fim, y_l):
        c.setFont("Helvetica", 10)
        c.setFillColor(cor_pre_impresso)
        c.drawString(x_label, y_l, label)
        
        d_linha_pontilhada(x_val, x_fim, y_l)
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(cor_preenchido)
        c.drawString(x_val + 2, y_l, str(val))

    # 3. Corpo do Formulário
    emb = licenca.embarcacao
    prop = emb.proprietario
    
    y = 630
    # Da [Nome] , « [Tipo] », n.º [Matrícula]
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Da")
    
    d_linha_pontilhada(70, 310, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(72, y, emb.nome)
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(315, y, "«")
    
    d_linha_pontilhada(325, 445, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(327, y, emb.get_tipo_embarcacao_display())
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(450, y, "», n.º")
    
    d_linha_pontilhada(475, 545, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(477, y, emb.numero_matricula)
    
    # Para efectuar o serviço de
    y -= 32
    d_campo("Para efectuar o serviço de", "Pesca Artesanal", 50, 165, 545, y)
    
    # Na zona de actividade
    y -= 32
    d_campo("Na zona de actividade", "Delegação da Beira / Província de Sofala", 50, 145, 545, y)
    
    # Registada na Delegação Provincial... livro... a fls...
    y -= 32
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Registada na Delegação Provincial de")
    d_linha_pontilhada(215, 345, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(217, y, "Sofala")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(350, y, "livro")
    d_linha_pontilhada(375, 450, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(377, y, f"A-{licenca.ano_referencia}")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(455, y, "a fls.")
    d_linha_pontilhada(480, 545, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    # Folha determinística com base na licença
    c.drawString(482, y, str((licenca.id % 150) + 1))
    
    # Propulsão... Arqueação bruta... tons
    y -= 32
    propulsao = f"A Motor ({emb.potencia_motor} CV)" if emb.potencia_motor > 0 else "Remos"
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Propulsão")
    d_linha_pontilhada(105, 330, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(107, y, propulsao)
    
    ab = f"{emb.comprimento * 0.15:.1f}"
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(335, y, "Arqueação bruta:")
    d_linha_pontilhada(420, 520, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(422, y, ab)
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(525, y, "tons")
    
    # Propriedade de
    y -= 32
    d_campo("Propriedade de", prop.nome_completo, 50, 120, 545, y)
    
    # Residente em
    y -= 32
    morada = f"Beira (Tel: {prop.telefone})"
    d_campo("Residente em", morada, 50, 115, 545, y)
    
    # Localidade e Data por extenso
    y -= 45
    d_linha_pontilhada(50, 180, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(52, y, "Beira")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(182, y, ",")
    
    d_linha_pontilhada(195, 220, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(197, y, f"{licenca.data_emissao.day:02d}")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(222, y, "de")
    
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    mes_nome = meses.get(licenca.data_emissao.month, "Janeiro")
    d_linha_pontilhada(240, 320, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(242, y, mes_nome)
    
    c.setFont("Helvetica", 10)
    c.setFillColor(cor_pre_impresso)
    c.drawString(322, y, "de 20")
    
    d_linha_pontilhada(348, 380, y)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(cor_preenchido)
    c.drawString(350, y, str(licenca.data_emissao.year % 100))
    
    # Validade
    y -= 32
    d_campo("Validade", licenca.data_validade.strftime('%d/%m/%Y'), 50, 95, 300, y)
    
    # 4. Assinaturas e Carimbo Oficial
    y_assinaturas = 200
    c.setStrokeColor(cor_pre_impresso)
    c.setLineWidth(0.5)
    c.line(70, y_assinaturas + 15, 230, y_assinaturas + 15)
    c.line(365, y_assinaturas + 15, 525, y_assinaturas + 15)
    
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(cor_pre_impresso)
    c.drawCentredString(150, y_assinaturas, "O Delegado Provincial")
    c.drawCentredString(445, y_assinaturas, "O Escrivão")
    
    # Carimbo oficial inclinado translúcido
    c.saveState()
    c.translate(450, y_assinaturas - 5)
    c.rotate(15)
    c.setStrokeColor(colors.HexColor('#D94F4F'))
    c.setFillColor(colors.HexColor('#D94F4F'))
    c.setLineWidth(1.2)
    c.circle(0, 0, 36, stroke=True, fill=False)
    c.circle(0, 0, 32, stroke=True, fill=False)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(0, 11, "ITRANSMAR, I.P.")
    c.setFont("Helvetica", 4.5)
    c.drawCentredString(0, 3, "DELEGAÇÃO PROVINCIAL")
    c.drawCentredString(0, -4, "DE SOFALA")
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(0, -14, "APROVADO")
    c.restoreState()
    
    # 5. Notas de Rodapé
    y = 110
    c.setFont("Helvetica", 9)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Licença industrial n.º")
    d_linha_pontilhada(140, 350, y)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(cor_preenchido)
    c.drawString(142, y, f"IND-{licenca.ano_referencia}/{(licenca.id % 900) + 100}")
    
    y -= 22
    c.setFont("Helvetica", 9)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Pagou os respectivos emolumentos pelo")
    d_linha_pontilhada(225, 450, y)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(cor_preenchido)
    c.drawString(227, y, "Recibo de Emolumentos Marítimos")
    
    y -= 22
    c.setFont("Helvetica", 9)
    c.setFillColor(cor_pre_impresso)
    c.drawString(50, y, "Recibo n.º")
    d_linha_pontilhada(100, 300, y)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(cor_preenchido)
    c.drawString(102, y, f"REC-{licenca.ano_referencia}-{(licenca.id * 7 % 9000) + 1000}")
    
    c.showPage()
    c.save()
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

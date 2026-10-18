import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Fonts
pdfmetrics.registerFont(TTFont('TNR', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TNR-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('TNR-Italic', 'C:/Windows/Fonts/timesi.ttf'))
pdfmetrics.registerFont(TTFont('TNR-BoldItalic', 'C:/Windows/Fonts/timesbi.ttf'))

# Page Geometry
P_WIDTH, P_HEIGHT = A4  # 595.27 x 841.89 pt
LEFT_M = 40
RIGHT_M = P_WIDTH - 40
CONTENT_W = RIGHT_M - LEFT_M  # 515.27 pt

styles = getSampleStyleSheet()

# Typography Styles
title_style = ParagraphStyle(
    'ExamTitle',
    parent=styles['Normal'],
    fontName='TNR-Bold',
    fontSize=10.5,
    leading=13.5,
    alignment=1,
    textColor=colors.black
)

sec_hdr_style = ParagraphStyle(
    'SecHeader',
    parent=styles['Normal'],
    fontName='TNR-Bold',
    fontSize=9.5,
    leading=12.5,
    alignment=0,
    textColor=colors.black
)

q_stem_style = ParagraphStyle(
    'QStem',
    parent=styles['Normal'],
    fontName='TNR-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.black
)

sub_q_style = ParagraphStyle(
    'SubQ',
    parent=styles['Normal'],
    fontName='TNR',
    fontSize=9,
    leading=12,
    textColor=colors.black
)

mark_style = ParagraphStyle(
    'Mark',
    parent=styles['Normal'],
    fontName='TNR-Italic',
    fontSize=8.5,
    leading=10,
    alignment=2,
    textColor=colors.black
)

box_text_style = ParagraphStyle(
    'BoxText',
    parent=styles['Normal'],
    fontName='TNR-Italic',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.black
)

tbl_cell_center = ParagraphStyle(
    'TblCellC',
    parent=styles['Normal'],
    fontName='TNR',
    fontSize=8.5,
    leading=11,
    alignment=1,
    textColor=colors.black
)

tbl_cell_bold = ParagraphStyle(
    'TblCellB',
    parent=styles['Normal'],
    fontName='TNR-Bold',
    fontSize=8.5,
    leading=11,
    alignment=1,
    textColor=colors.black
)

tbl_cell_left = ParagraphStyle(
    'TblCellL',
    parent=styles['Normal'],
    fontName='TNR',
    fontSize=8.5,
    leading=11,
    textColor=colors.black
)

class SPMNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page_data in self.pages:
            self.__dict__.update(page_data)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        p = self._pageNumber
        
        # TOP HEADER
        self.setFont('TNR-Bold', 9)
        self.drawString(LEFT_M, P_HEIGHT - 28, 'SULIT')
        self.setFont('TNR', 9)
        self.drawCentredString(P_WIDTH / 2.0, P_HEIGHT - 28, str(p))
        self.setFont('TNR-Bold', 9)
        self.drawRightString(RIGHT_M, P_HEIGHT - 28, '1223/1')
        
        # TOP LINE
        self.setLineWidth(0.6)
        self.line(LEFT_M, P_HEIGHT - 32, RIGHT_M, P_HEIGHT - 32)
        
        # BOTTOM LINE
        self.line(LEFT_M, 34, RIGHT_M, 34)
        
        # BOTTOM FOOTER
        self.setFont('TNR', 8)
        self.drawString(LEFT_M, 24, '1223/1 © Peperiksaan Akhir Tahun Tingkatan 4 KSSM')
        
        if p < total_pages:
            self.setFont('TNR-Italic', 8.5)
            self.drawRightString(RIGHT_M, 24, '[Lihat halaman sebelah')
        else:
            self.setFont('TNR-Bold', 8.5)
            self.drawCentredString(P_WIDTH / 2.0, 42, 'KERTAS PEPERIKSAAN TAMAT')
            self.drawRightString(RIGHT_M, 24, 'SULIT')
            
        self.restoreState()

def make_answer_lines(num_lines=2, line_height=15):
    data = [[''] for _ in range(num_lines)]
    t = Table(data, colWidths=[CONTENT_W], rowHeights=[line_height]*num_lines)
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#777777')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

def make_sub_item_lines(labels=['1.', '2.'], line_height=15):
    lbl_style = ParagraphStyle('Lbl', parent=styles['Normal'], fontName='TNR-Bold', fontSize=8.5, leading=11)
    data = []
    for lbl in labels:
        data.append([Paragraph(lbl, lbl_style), ''])
    t = Table(data, colWidths=[20, CONTENT_W - 20], rowHeights=[line_height]*len(labels))
    t.setStyle(TableStyle([
        ('LINEBELOW', (1,0), (1,-1), 0.5, colors.HexColor('#777777')),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

def make_boxed_stimulus(text_list, title=None, width=CONTENT_W):
    flowables = []
    if title:
        flowables.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('BoxHdr', parent=styles['Normal'], fontName='TNR-Bold', fontSize=8.5, leading=11)))
        flowables.append(Spacer(1, 1.5))
    for t in text_list:
        flowables.append(Paragraph(t, box_text_style))
        flowables.append(Spacer(1, 1.5))
    if flowables and isinstance(flowables[-1], Spacer):
        flowables.pop()

    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fbfbfb')),
    ]))
    return t

def build_pdf():
    pdf_filename = "C:/Users/User/.gemini/antigravity/scratch/pendidikan-islam-tingkatan4/Soalan_Peperiksaan_Pendidikan_Islam_Tingkatan_4.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=LEFT_M,
        rightMargin=P_WIDTH - RIGHT_M,
        topMargin=38,
        bottomMargin=42
    )
    
    story = []
    
    # =========================================================
    # PAGE 1: HEADER + BAHAGIAN A (TILAWAH, HADIS, TAJWID)
    # =========================================================
    header_table_data = [
        [
            Paragraph("<b>PEPERIKSAAN AKHIR TAHUN TINGKATAN 4</b><br/><b>PENDIDIKAN ISLAM (KERTAS 1)</b><br/>Masa: 2 Jam 30 Minit", title_style),
            Table([
                [Paragraph("<b>NAMA:</b>", ParagraphStyle('H1', fontName='TNR-Bold', fontSize=8, leading=10)), Paragraph(".........................................................................", ParagraphStyle('H2', fontName='TNR', fontSize=8, leading=10))],
                [Paragraph("<b>TINGKATAN:</b>", ParagraphStyle('H1', fontName='TNR-Bold', fontSize=8, leading=10)), Paragraph(".........................................................................", ParagraphStyle('H2', fontName='TNR', fontSize=8, leading=10))],
                [Paragraph("<b>ANGKA GILIRAN:</b>", ParagraphStyle('H1', fontName='TNR-Bold', fontSize=8, leading=10)), Paragraph("[ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ]", ParagraphStyle('H2', fontName='TNR', fontSize=8, leading=10))]
            ], colWidths=[80, 160])
        ]
    ]
    hdr_t = Table(header_table_data, colWidths=[260, 255])
    hdr_t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.7, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBEFORE', (1,0), (1,0), 0.7, colors.black),
    ]))
    story.append(hdr_t)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<i>Arahan: Kertas ini mengandungi tiga bahagian. Jawab semua soalan dalam ruangan yang disediakan.</i>", ParagraphStyle('Ins', fontName='TNR-Italic', fontSize=8, leading=10)))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>BAHAGIAN A: AL-QURAN (TILAWAH & TAJWID) DAN HADIS</b> [20 Markah]", sec_hdr_style))
    story.append(Spacer(1, 3))
    
    # Soalan 1 (a) - Tilawah
    story.append(Paragraph("<b>1</b> (a) Firman Allah SWT dalam Surah Al-An'am ayat 70 melarang umat Islam bergaul rapat dengan golongan yang mempersendakan agama:", q_stem_style))
    story.append(Spacer(1, 2))
    story.append(make_boxed_stimulus([
        "\"Dan tinggalkanlah orang yang menjadikan agama mereka sebagai main-main dan gurau senda, dan mereka telah ditipu oleh kehidupan dunia...\" (Surah Al-An'am: 70)"
    ]))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("(i) Nyatakan <b>dua</b> bentuk perbuatan mempersendakan agama yang kerap berlaku pada masa kini.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_sub_item_lines(['1.', '2.'], line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Terangkan <b>dua</b> kesan perbuatan mempersendakan hukum Islam terhadap individu.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 1 (b) - Hukum Tajwid (Mad Lazim)
    story.append(Paragraph("(b) Tentukan hukum tajwid bagi bahagian ayat al-Quran di bawah sama ada <b>Mad Lazim Kalimi Mukhaffaf</b>, <b>Mad Lazim Kalimi Muthaqqal</b>, atau <b>Mad Lazim Harfi Muthaqqal</b>.", q_stem_style))
    story.append(Spacer(1, 2))
    
    tajwid_data = [
        [Paragraph("<b>No.</b>", tbl_cell_bold), Paragraph("<b>Kalimah / Huruf Awal Surah Berkenaan</b>", tbl_cell_bold), Paragraph("<b>Hukum Tajwid (Mad Lazim)</b>", tbl_cell_bold)],
        [Paragraph("1", tbl_cell_center), Paragraph("Kalimah <b>\"Ad-Dhaallin\"</b> <i>(Surah Al-Fatihah, ayat 7)</i>", tbl_cell_left), Paragraph(".........................................................................", tbl_cell_center)],
        [Paragraph("2", tbl_cell_center), Paragraph("Kalimah <b>\"Aaall-aana\"</b> <i>(Surah Yunus, ayat 51)</i>", tbl_cell_left), Paragraph(".........................................................................", tbl_cell_center)],
        [Paragraph("3", tbl_cell_center), Paragraph("Huruf <b>\"Alif Laaam Miiim\"</b> <i>(Surah Al-Baqarah, ayat 1)</i>", tbl_cell_left), Paragraph(".........................................................................", tbl_cell_center)]
    ]
    tajwid_tbl = Table(tajwid_data, colWidths=[25, 235, 255], rowHeights=[14, 15, 15, 15])
    tajwid_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#999999')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
    ]))
    story.append(tajwid_tbl)
    story.append(Paragraph("[3 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 1 (c) - Hadis (7 Dosa Besar)
    story.append(Paragraph("(c) Sabda Rasulullah SAW: <i>\"Jauhilah tujuh perkara yang membinasakan (Al-Mubiqaat)...\"</i> (Riwayat Al-Bukhari & Muslim)", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Senaraikan <b>dua</b> daripada tujuh dosa besar yang membinasakan selain perbuatan syirik dan sihir.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_sub_item_lines(['1.', '2.'], line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Terangkan mengapakah perbuatan <b>memakan harta anak yatim secara zalim</b> dilarang keras dalam Islam.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    
    # End of Page 1
    story.append(PageBreak())
    
    # =========================================================
    # PAGE 2: BAHAGIAN B (AKIDAH & IBADAH)
    # =========================================================
    story.append(Paragraph("<b>BAHAGIAN B: AKIDAH DAN IBADAH</b> [20 Markah]", sec_hdr_style))
    story.append(Spacer(1, 3))
    
    # Soalan 2: Akidah
    story.append(Paragraph("<b>2</b> (a) Allah SWT memiliki nama-nama yang mulia termasuklah nama <b>Al-Jabbar</b>.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Nyatakan pengertian nama Allah SWT <i>Al-Jabbar</i>.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=15))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Jelaskan <b>dua</b> bukti keimanan seseorang terhadap sifat Al-Jabbar dalam kehidupan seharian.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_sub_item_lines(['1.', '2.'], line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 2 (b) - Ajaran Sesat (KBAT)
    story.append(Paragraph("(b) Baca dan teliti situasi berikut:", q_stem_style))
    story.append(Spacer(1, 2))
    story.append(make_boxed_stimulus([
        "Terdapat sekumpulan individu menyebarkan amalan ritual baharu di media sosial yang mendakwa pengikutnya tidak perlu lagi menunaikan solat fardhu lima waktu secara fizikal, sebaliknya memadai dengan niat di dalam hati sahaja. Mereka juga mendakwa pemimpin kumpulan tersebut menerima ilham ghaib memansuhkan syariat."
    ], title="SITUASI: PENYEBARAN DOKTRIN SESAT"))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("Berdasarkan kefahaman anda mengenai <b>ciri-ciri ajaran sesat</b>, kemukakan <b>dua</b> hujah mengapa amalan tersebut bercanggah dengan akidah Islam, dan huraikan langkah anda sebagai remaja bagi membendung fahaman ini daripada merosakkan rakan sebaya.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=4, line_height=15))
    story.append(Paragraph("[4 markah]", mark_style))
    story.append(Spacer(1, 5))
    
    # Soalan 3: Ibadah (Muamalat & Solat Gerhana)
    story.append(Paragraph("<b>3</b> (a) Muamalat Islam bermatlamat mewujudkan sistem ekonomi yang adil dan diredai Allah SWT.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Nyatakan maksud akad muamalat berikut:", sub_q_style))
    story.append(Spacer(1, 1))
    
    akad_data = [
        [Paragraph("<b>Al-Ijarah (Sewaan):</b>", ParagraphStyle('A1', fontName='TNR-Bold', fontSize=8.5, leading=11)), Paragraph("........................................................................................................................................", ParagraphStyle('A2', fontName='TNR', fontSize=8.5, leading=11))],
        [Paragraph("<b>Ar-Rahnu (Gadaian):</b>", ParagraphStyle('A1', fontName='TNR-Bold', fontSize=8.5, leading=11)), Paragraph("........................................................................................................................................", ParagraphStyle('A2', fontName='TNR', fontSize=8.5, leading=11))]
    ]
    akad_tbl = Table(akad_data, colWidths=[120, 395], rowHeights=[15, 15])
    akad_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(akad_tbl)
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Terangkan <b>dua</b> hikmah muamalat Islam mengharamkan unsur riba dan gharar.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 3 (b) - Solat Sunat Gerhana
    story.append(Paragraph("(b) Solat Sunat Gerhana merupakan ibadah yang sangat dituntut (sunat muakkad) ketika berlaku gerhana.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Nyatakan <b>dua</b> amalan sunat yang digalakkan semasa fenomena gerhana matahari atau bulan.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_sub_item_lines(['1.', '2.'], line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Jelaskan kaifiat (tatacara) Solat Sunat Gerhana dari segi <b>bilangan rukuk</b> dan <b>bacaan surah</b> dalam setiap rakaat.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    
    # End of Page 2
    story.append(PageBreak())
    
    # =========================================================
    # PAGE 3: BAHAGIAN C (SIRAH & ADAB ISLAMIAH)
    # =========================================================
    story.append(Paragraph("<b>BAHAGIAN C: SIRAH DAN ADAB ISLAMIAH</b> [20 Markah]", sec_hdr_style))
    story.append(Spacer(1, 3))
    
    # Soalan 4: Sirah (Imam Syafie & Kerajaan Umaiyyah)
    story.append(Paragraph("<b>4</b> (a) Imam Asy-Syafi'i r.a. merupakan tokoh fuqaha' agung dan pengasas Mazhab Syafi'i.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Nyatakan <b>tempat kelahiran</b> dan <b>tahun kewafatan</b> Imam Asy-Syafi'i r.a.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Namakan <b>dua</b> karya agung yang dikarang oleh beliau dalam bidang ilmu Islam.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_sub_item_lines(['1.', '2.'], line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 4 (b) - Kerajaan Umaiyyah
    story.append(Paragraph("(b) Kerajaan Umaiyyah telah mencatatkan sejarah ketamadunan Islam selama 91 tahun berpusat di Damsyik.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Siapakah <b>pengasas</b> Kerajaan Umaiyyah dan pada tahun berapakah ia diasaskan?", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Terangkan <b>dua</b> sumbangan penting Khalifah <b>Umar bin Abdul Aziz</b> sehingga pemerintahannya dianggap zaman keadilan sosial.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 4))
    
    # Soalan 5: Adab (Khauf & Raja', Adab Orang Sakit)
    story.append(Paragraph("<b>5</b> (a) Konsep <b>Khauf</b> (takut) dan <b>Raja'</b> (harap) hendaklah diamalkan secara seimbang dalam kehidupan muslim.", q_stem_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(i) Jelaskan mengapakah sifat <i>Khauf</i> dan <i>Raja'</i> diumpamakan seperti <b>dua sayap bagi seekor burung</b>.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("(ii) Terangkan <b>satu</b> kesan negatif sekiranya seseorang hanya memiliki sifat <i>Raja'</i> tanpa diimbangi dengan sifat <i>Khauf</i>.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=2, line_height=14.5))
    story.append(Paragraph("[2 markah]", mark_style))
    story.append(Spacer(1, 3))
    
    # Soalan 5 (b) - Adab Menziarahi Orang Sakit (KBAT)
    story.append(Paragraph("(b) Fahami situasi di bawah:", q_stem_style))
    story.append(Spacer(1, 2))
    story.append(make_boxed_stimulus([
        "Rakan sekelas anda telah terlibat dalam kemalangan jalan raya dan terlantar di hospital. Semasa anda menziarahinya, beliau meluahkan rasa sedih yang mendalam, tertekan dengan kesakitan, serta berasa keliru mengenai cara menunaikan solat kerana anggota badannya bersimen."
    ], title="SITUASI: ZIARAH RAKAN DI WAD HOSPITAL"))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("Berdasarkan situasi di atas, bagaimanakah anda mengaplikasikan <b>adab terhadap orang sakit dari aspek rohani dan emosi</b> bagi membantu serta mententeramkan rakan anda? Huraikan.", sub_q_style))
    story.append(Spacer(1, 1))
    story.append(make_answer_lines(num_lines=4, line_height=15))
    story.append(Paragraph("[4 markah]", mark_style))
    
    # Build Document
    doc.build(story, canvasmaker=SPMNumberedCanvas)
    print("PDF build successful:", pdf_filename)

if __name__ == "__main__":
    build_pdf()

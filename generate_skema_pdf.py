import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('TNR', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TNR-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('TNR-Italic', 'C:/Windows/Fonts/timesi.ttf'))
pdfmetrics.registerFont(TTFont('TNR-BoldItalic', 'C:/Windows/Fonts/timesbi.ttf'))

P_WIDTH, P_HEIGHT = A4
LEFT_M = 40
RIGHT_M = P_WIDTH - 40
CONTENT_W = RIGHT_M - LEFT_M

styles = getSampleStyleSheet()

hdr_title = ParagraphStyle('HdrTitle', parent=styles['Normal'], fontName='TNR-Bold', fontSize=11, leading=14, alignment=1)
hdr_sub = ParagraphStyle('HdrSub', parent=styles['Normal'], fontName='TNR-Bold', fontSize=9.5, leading=12.5, alignment=1)

tbl_hdr = ParagraphStyle('THdr', parent=styles['Normal'], fontName='TNR-Bold', fontSize=8.5, leading=11, alignment=1)
cell_c = ParagraphStyle('CC', parent=styles['Normal'], fontName='TNR', fontSize=8, leading=10.5, alignment=1)
cell_cb = ParagraphStyle('CCB', parent=styles['Normal'], fontName='TNR-Bold', fontSize=8, leading=10.5, alignment=1)
cell_l = ParagraphStyle('CL', parent=styles['Normal'], fontName='TNR', fontSize=8, leading=10.5)
cell_lb = ParagraphStyle('CLB', parent=styles['Normal'], fontName='TNR-Bold', fontSize=8, leading=10.5)

class SkemaCanvas(canvas.Canvas):
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
        self.setFont('TNR-Bold', 9)
        self.drawString(LEFT_M, P_HEIGHT - 28, 'SULIT')
        self.setFont('TNR', 9)
        self.drawCentredString(P_WIDTH / 2.0, P_HEIGHT - 28, f'- {p} -')
        self.setFont('TNR-Bold', 9)
        self.drawRightString(RIGHT_M, P_HEIGHT - 28, '1223/1(PP)')
        self.setLineWidth(0.6)
        self.line(LEFT_M, P_HEIGHT - 32, RIGHT_M, P_HEIGHT - 32)
        self.line(LEFT_M, 34, RIGHT_M, 34)
        self.setFont('TNR', 8)
        self.drawString(LEFT_M, 24, '1223/1(PP) © Skema Pemarkahan Peperiksaan Akhir Tahun Tingkatan 4')
        self.drawRightString(RIGHT_M, 24, 'SULIT')
        self.restoreState()

def build_skema_pdf():
    pdf_filename = "C:/Users/User/.gemini/antigravity/scratch/pendidikan-islam-tingkatan4/Skema_Jawapan_Pendidikan_Islam_Tingkatan_4.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=LEFT_M,
        rightMargin=P_WIDTH - RIGHT_M,
        topMargin=38,
        bottomMargin=42
    )
    
    story = []
    
    # Title
    story.append(Paragraph("<b>SKEMA PEMARKAHAN PEPERIKSAAN AKHIR TAHUN</b>", hdr_title))
    story.append(Paragraph("<b>PENDIDIKAN ISLAM TINGKATAN 4 (KERTAS 1 - 1223/1)</b>", hdr_sub))
    story.append(Spacer(1, 6))
    
    skema_data = [
        [
            Paragraph("<b>No.</b>", tbl_hdr),
            Paragraph("<b>Pecahan</b>", tbl_hdr),
            Paragraph("<b>Panduan Penskoran &amp; Cadangan Jawapan Lengkap</b>", tbl_hdr),
            Paragraph("<b>Sub</b>", tbl_hdr),
            Paragraph("<b>Markah</b>", tbl_hdr)
        ],
        # BAHAGIAN A
        [Paragraph("<b>BAHAGIAN A: AL-QURAN DAN HADIS [20 MARKAH]</b>", cell_lb), "", "", "", ""],
        
        # 1(a)(i)
        [Paragraph("<b>1</b>", cell_cb), Paragraph("(a)(i)", cell_c), Paragraph("<b>Dua bentuk perbuatan mempersendakan agama:</b><br/>• Meremehkan tuntutan hukum syarak (solat, puasa, menutup aurat). (1m)<br/>• Menjadikan ayat suci al-Quran dan hadis bahan gurauan / komedi. (1m)<br/>• Berbangga menunjuk-nunjuk maksiat di khalayak / media sosial. (1m)<br/>• Mentafsir al-Quran mengikut hawa nafsu / akal semata-mata. (1m)<br/><i>(Mana-mana 2 jawapan betul)</i>", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 1(a)(ii)
        ["", Paragraph("(a)(ii)", cell_c), Paragraph("<b>Dua kesan perbuatan mempersendakan agama terhadap individu:</b><br/>• Boleh membatalkan iman / terkeluar daripada Islam (murtad). (1m)<br/>• Dilaknat oleh Allah SWT dan hilang keberkatan hidup. (1m)<br/>• Diseksa dengan azab api neraka dan minuman air menggelegak. (1m)<br/>• Jiwa berasa gelisah dan hilang petunjuk hidayah Ilahi. (1m)<br/><i>(Mana-mana 2 jawapan betul)</i>", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 1(b)
        ["", Paragraph("(b)", cell_c), Paragraph("<b>Hukum Tajwid (Mad Lazim):</b><br/>1. <i>\"Ad-Dhaallin\"</i> : <b>Mad Lazim Kalimi Muthaqqal</b> (1m)<br/>2. <i>\"Aaall-aana\"</i> : <b>Mad Lazim Kalimi Mukhaffaf</b> (1m)<br/>3. <i>\"Alif Laaam Miiim\"</i> : <b>Mad Lazim Harfi Muthaqqal</b> (1m)", cell_l), Paragraph("3m", cell_c), Paragraph("<b>3m</b>", cell_cb)],
        
        # 1(c)(i)
        ["", Paragraph("(c)(i)", cell_c), Paragraph("<b>Dua dosa besar selain syirik dan sihir:</b><br/>• Membunuh jiwa yang diharamkan Allah tanpa hak. (1m)<br/>• Memakan riba. (1m)<br/>• Memakan harta anak yatim secara zalim. (1m)<br/>• Lari dari medan peperangan jihad. (1m)<br/>• Menuduh wanita mukminah berzina (Qazaf). (1m)<br/><i>(Mana-mana 2 jawapan betul)</i>", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 1(c)(ii)
        ["", Paragraph("(c)(ii)", cell_c), Paragraph("<b>Sebab dilarang makan harta anak yatim secara zalim:</b><br/>• Menganiaya golongan lemah yang kehilangan tempat bergantung. (1m)<br/>• Menafikan hak anak yatim untuk kelangsungan hidup dan pendidikan. (1m)<br/>• Mengundang kemurkaan Allah SWT dan balasan api neraka. (1m)<br/><i>[Isi (1m) + Huraian (1m)]</i>", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # BAHAGIAN B
        [Paragraph("<b>BAHAGIAN B: AKIDAH DAN IBADAH [20 MARKAH]</b>", cell_lb), "", "", "", ""],
        
        # 2(a)(i)
        [Paragraph("<b>2</b>", cell_cb), Paragraph("(a)(i)", cell_c), Paragraph("<b>Pengertian nama Allah SWT Al-Jabbar:</b><br/>Allah SWT Maha Berkuasa Memaksa sekalian makhluk menurut kehendak-Nya yang mutlak, dan tiada sesiapa pun mampu menghalang ketetapan-Nya, serta Maha Memperbaiki kerosakan makhluk-Nya. (2m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 2(a)(ii)
        ["", Paragraph("(a)(ii)", cell_c), Paragraph("<b>Dua bukti beriman kepada Al-Jabbar:</b><br/>• Sentiasa tunduk dan patuh mentaati segala perintah Allah SWT. (1m)<br/>• Menjauhi sifat sombong, takabbur, dan angkuh sesama manusia. (1m)<br/>• Bersikap reda dan sabar menghadapi segala ketentuan takdir Ilahi. (1m)<br/><i>(Mana-mana 2 jawapan betul)</i>", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 2(b)
        ["", Paragraph("(b)", cell_c), Paragraph("<b>Rubrik KBAT Ajaran Sesat (4 Markah):</b><br/>• <b>[Isi]:</b> Amalan tersebut jelas bercanggah dengan rukun Islam kerana solat wajib dilakukan dengan rukun fi'li dan qauli, manakala wahyu telah terputus selepas kewafatan Nabi SAW. (1m)<br/>• <b>[Huraian]:</b> Golongan ini memanipulasi ajaran untuk menyesatkan masyarakat yang cetek ilmu agama. (1m)<br/>• <b>[Huraian Lengkap]:</b> Remaja hendaklah menasihati rakan menyemak kesahihan ajaran dengan pihak JAIS / mufti serta menjauhi kumpulan tersebut. (1m)<br/>• <b>[Kesimpulan]:</b> Kesimpulannya, kita hendaklah sentiasa mendalami ilmu Ahli Sunnah Wal Jamaah agar akidah sentiasa terpelihara. (1m)", cell_l), Paragraph("4m", cell_c), Paragraph("<b>4m</b>", cell_cb)],
        
        # 3(a)(i)
        [Paragraph("<b>3</b>", cell_cb), Paragraph("(a)(i)", cell_c), Paragraph("<b>Maksud akad muamalat:</b><br/>• <b>Al-Ijarah:</b> Akad mengambil manfaat daripada sesuatu benda atau perkhidmatan dengan bayaran sewa. (1m)<br/>• <b>Ar-Rahnu:</b> Menjadikan sesuatu barang berharga sebagai cagaran bagi jaminan hutang sekiranya gagal melunaskannya. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 3(a)(ii)
        ["", Paragraph("(a)(ii)", cell_c), Paragraph("<b>Dua hikmah mengharamkan riba dan gharar:</b><br/>• Mencegah penindasan dan eksploitasi terhadap golongan yang susah. (1m)<br/>• Memastikan urus niaga berjalan secara telus, jujur, dan reda-meredai. (1m)<br/>• Membina kestabilan ekonomi ummah yang diredai Allah SWT. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 3(b)(i)
        ["", Paragraph("(b)(i)", cell_c), Paragraph("<b>Dua amalan sunat ketika gerhana:</b><br/>• Memperbanyakkan istighfar, zikir, dan takbir. (1m)<br/>• Berdoa dan bersedekah kepada fakir miskin. (1m)<br/>• Mendengar dua khutbah selepas solat sunat gerhana. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 3(b)(ii)
        ["", Paragraph("(b)(ii)", cell_c), Paragraph("<b>Kaifiat Solat Sunat Gerhana:</b><br/>Setiap satu rakaat mempunyai <b>2 kali rukuk dan 2 kali qiam</b> membaca surah al-Fatihah dan surah pilihan, menjadikan jumlahnya <b>4 rukuk dan 4 qiam</b> dalam 2 rakaat solat. (2m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # BAHAGIAN C
        [Paragraph("<b>BAHAGIAN C: SIRAH DAN ADAB ISLAMIAH [20 MARKAH]</b>", cell_lb), "", "", "", ""],
        
        # 4(a)(i)
        [Paragraph("<b>4</b>", cell_cb), Paragraph("(a)(i)", cell_c), Paragraph("• Tempat lahir: <b>Gaza, Palestin</b> (tahun 150H). (1m)<br/>• Tahun kewafatan: <b>204 Hijrah</b> di Mesir. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 4(a)(ii)
        ["", Paragraph("(a)(ii)", cell_c), Paragraph("<b>Dua karya agung Imam Asy-Syafi'i r.a.:</b><br/>• <b>Kitab Al-Umm</b> (rujukan fiqh mazhab Syafi'i). (1m)<br/>• <b>Kitab Ar-Risalah</b> (kitab usul fiqh pertama). (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 4(b)(i)
        ["", Paragraph("(b)(i)", cell_c), Paragraph("• Pengasas: <b>Muawiyah bin Abi Sufyan</b>. (1m)<br/>• Tahun diasaskan: <b>41 Hijrah (661 Masihi)</b>. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 4(b)(ii)
        ["", Paragraph("(b)(ii)", cell_c), Paragraph("<b>Dua sumbangan Khalifah Umar bin Abdul Aziz:</b><br/>• Memerintahkan pembukuan hadis Rasulullah SAW secara rasmi. (1m)<br/>• Mengembalikan wang dan harta ke dalam Baitulmal secara adil. (1m)<br/>• Menghapuskan cukai yang membebankan rakyat dan memecat pegawai zalim. (1m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 5(a)(i)
        [Paragraph("<b>5</b>", cell_cb), Paragraph("(a)(i)", cell_c), Paragraph("<b>Umpama dua sayap burung:</b><br/>Khauf (takut azab) dan Raja' (harap rahmat) mesti seimbang agar manusia tidak berputus asa daripada rahmat Allah dan tidak berani melakukan maksiat. (2m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 5(a)(ii)
        ["", Paragraph("(a)(ii)", cell_c), Paragraph("<b>Kesan negatif jika hanya ada Raja' tanpa Khauf:</b><br/>Seseorang akan menjadi lalai, leka, dan berani berbuat dosa secara berterusan kerana terlalu yakin Allah Maha Pengampun tanpa rasa takut terhadap azab-Nya. (2m)", cell_l), Paragraph("2m", cell_c), Paragraph("<b>2m</b>", cell_cb)],
        
        # 5(b)
        ["", Paragraph("(b)", cell_c), Paragraph("<b>Rubrik KBAT Adab Terhadap Orang Sakit (4 Markah):</b><br/>• <b>[Fakta - Rohani]:</b> Saya akan membimbing rakan cara rukhsah bersuci (tayamum) dan rukhsah solat secara duduk atau baring mengikut kemampuannya. (1m)<br/>• <b>[Huraian - Emosi]:</b> Saya juga memberikan kata-kata motivasi dan mendoakan kesembuhannya agar tidak berasa sedih dan putus asa. (1m)<br/>• <b>[Huraian Lengkap]:</b> Kesannya, emosi rakan menjadi lebih tenang dan kewajipan ibadah kepada Allah SWT tidak diabaikan walaupun ketika sakit. (1m)<br/>• <b>[Kesimpulan]:</b> Kesimpulannya, kita hendaklah sentiasa cakna terhadap kebajikan sahabat seagama demi mengukuhkan ukhuwah Islamiah. (1m)", cell_l), Paragraph("4m", cell_c), Paragraph("<b>4m</b>", cell_cb)]
    ]
    
    table = Table(skema_data, colWidths=[24, 38, 385, 34, 34])
    table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.7, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#999999')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e6e6e6')),
        ('SPAN', (0,1), (-1,1)),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f5f5f5')),
        ('SPAN', (0,7), (-1,7)),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor('#f5f5f5')),
        ('SPAN', (0,15), (-1,15)),
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor('#f5f5f5')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    
    story.append(table)
    doc.build(story, canvasmaker=SkemaCanvas)
    print("Skema build successful:", pdf_filename)

if __name__ == "__main__":
    build_skema_pdf()

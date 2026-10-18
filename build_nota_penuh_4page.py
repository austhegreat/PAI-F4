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
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))

# Page Geometry
P_WIDTH, P_HEIGHT = A4  # 595.27 x 841.89 pt
LEFT_M = 32
RIGHT_M = P_WIDTH - 32
CONTENT_W = RIGHT_M - LEFT_M  # 531.27 pt

styles = getSampleStyleSheet()

# Typography Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=11,
    leading=14,
    alignment=1,
    textColor=colors.HexColor('#064e3b')
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Arial',
    fontSize=7.5,
    leading=10,
    alignment=1,
    textColor=colors.HexColor('#334155')
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.white
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#0f172a')
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Arial',
    fontSize=7.2,
    leading=9.4,
    textColor=colors.HexColor('#1e293b')
)

body_bold = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=7.2,
    leading=9.4,
    textColor=colors.HexColor('#0f172a')
)

tip_style = ParagraphStyle(
    'TipText',
    parent=styles['Normal'],
    fontName='Arial-Italic',
    fontSize=6.8,
    leading=8.8,
    textColor=colors.HexColor('#854d0e')
)

tbl_cell_hdr = ParagraphStyle(
    'TblHdr',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=7,
    leading=9,
    alignment=1,
    textColor=colors.HexColor('#0f172a')
)

tbl_cell = ParagraphStyle(
    'TblCell',
    parent=styles['Normal'],
    fontName='Arial',
    fontSize=6.8,
    leading=8.8,
    textColor=colors.HexColor('#1e293b')
)

tbl_cell_bold = ParagraphStyle(
    'TblCellB',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=6.8,
    leading=8.8,
    textColor=colors.HexColor('#0f172a')
)

class StudentNotesCanvas(canvas.Canvas):
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
        
        # TOP RUNNING HEADER
        self.setFont('Arial-Bold', 7.5)
        self.setFillColor(colors.HexColor('#065f46'))
        self.drawString(LEFT_M, P_HEIGHT - 22, 'MODUL NOTA LENGKAP PENDIDIKAN ISLAM TINGKATAN 4 (KSSM / SPM)')
        
        self.setFont('Arial', 7.5)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawRightString(RIGHT_M, P_HEIGHT - 22, f'Halaman {p} daripada {total_pages}')
        
        self.setLineWidth(0.6)
        self.setStrokeColor(colors.HexColor('#059669'))
        self.line(LEFT_M, P_HEIGHT - 25, RIGHT_M, P_HEIGHT - 25)
        
        # BOTTOM RUNNING FOOTER
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.line(LEFT_M, 26, RIGHT_M, 26)
        
        self.setFont('Arial', 7)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(LEFT_M, 17, 'Disusun mengikut Dokumen Standard Kurikulum & Pentaksiran (DSKP) KSSM Tingkatan 4')
        self.drawRightString(RIGHT_M, 17, 'e-Kalam T4 • Mudah Faham, Lengkap & Padat')
        
        self.restoreState()

def make_header_banner(title, color_hex='#065f46'):
    p = Paragraph(f"<b>{title}</b>", h1_style)
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(color_hex)),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def make_card(flowables, border_color='#cbd5e1', bg_color='#ffffff'):
    t = Table([[flowables]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def make_tip_box(tip_text):
    p = Paragraph(f"<b>💡 Tips Peperiksaan &amp; Memori:</b> {tip_text}", tip_style)
    t = Table([[p]], colWidths=[CONTENT_W - 14])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fefce8')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#facc15')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def build_pdf():
    pdf_filename = "C:/Users/User/.gemini/antigravity/scratch/pendidikan-islam-tingkatan4/Nota_Lengkap_Pendidikan_Islam_Tingkatan_4.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=LEFT_M,
        rightMargin=P_WIDTH - RIGHT_M,
        topMargin=32,
        bottomMargin=34
    )
    
    story = []
    
    # =========================================================================
    # MUKA SURAT 1: TILAWAH AL-QURAN & HUKUM TAJWID
    # =========================================================================
    # Header Module Info
    mod_info = [
        Paragraph("<b>PANDUAN ULANG KAJI PANTAS PENDIDIKAN ISLAM TINGKATAN 4 (KSSM / SPM)</b>", title_style),
        Paragraph("<b>Rujukan Lengkap Berdasarkan Silibus Rasmi Kementerian Pendidikan Malaysia (KPM)</b><br/>Disusun dengan bahasa mudah, huraian lengkap tanpa pemotongan fakta, peta konsep, dan formula skor markah tinggi.", subtitle_style)
    ]
    hdr_box = Table([[mod_info]], colWidths=[CONTENT_W])
    hdr_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ecfdf5')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(hdr_box)
    story.append(Spacer(1, 4))
    
    # --- TAJUK 1: TILAWAH - LARANGAN MEMPERSENDAKAN AGAMA ---
    story.append(make_header_banner("BAHAGIAN TILAWAH: LARANGAN MEMPERSENDAKAN AGAMA (Surah Al-An'am: 70)", '#047857'))
    story.append(Spacer(1, 2))
    
    tilawah_content = [
        Paragraph("<b>1. Intisari &amp; Tuntutan Surah Al-An'am Ayat 70:</b><br/>"
                  "Allah SWT melarang keras setiap orang yang beriman daripada bersahabat rapat, bersekongkol, atau bertoleransi dengan golongan yang menjadikan syiar agama Islam sebagai bahan permainan, lawak jenaka, dan senda gurau. Golongan ini telah terpedaya dengan tipu daya kemewahan dan keseronokan kehidupan dunia yang sementara sehingga mengabaikan hari akhirat.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Empat Bentuk Perbuatan Mempersendakan Agama (Fokus Soalan Struktur):</b><br/>"
                  "• <b>Menghina atau meremehkan hukum syarak:</b> Menganggap ibadah fardhu seperti solat lima waktu, puasa Ramadan, kewajipan menutup aurat dengan sempurna, atau undang-undang jenayah syariah (hudud dan qisas) sebagai amalan kolot, membebankan, atau tidak sesuai pada zaman moden.<br/>"
                  "• <b>Mempersenda al-Quran dan Sunnah:</b> Menjadikan ayat suci kalamullah atau sabda Rasulullah SAW sebagai bahan ejekan, komedi, satira politik, atau parodi di media sosial semata-mata demi mengejar tontonan dan populariti.<br/>"
                  "• <b>Mentafsir agama mengikut hawa nafsu:</b> Menolak huraian ijmak para ulama muktabar dan mencipta fatwa sendiri mengikut logik akal manusia yang terbatas, contohnya menghalalkan pergaulan bebas atau menganggap semua agama adalah sama taraf.<br/>"
                  "• <b>Berbangga menzahirkan maksiat:</b> Melakukan perkara maksiat secara terang-terangan di hadapan khalayak ramai atau memuat naik video berbuat dosa tanpa sedikit pun berasa malu atau berdosa.", body_style),
        Spacer(1, 2),
        Paragraph("<b>3. Kesan Buruk Mempersendakan Agama:</b><br/>"
                  "• <b>Terhadap Individu:</b> Boleh merosakkan akidah dan membatalkan iman (menjadi murtad jika mengingkari hukum syarak), dilaknat oleh Allah SWT, hilang ketenangan jiwa, serta di akhirat diazab dengan minuman air panas yang menggelegak dan dibakar dalam neraka jahannam.<br/>"
                  "• <b>Terhadap Masyarakat &amp; Negara:</b> Hilang keberkatan dan mengundang bencana alam, mencetuskan permusuhan dan perpecahan ummah, serta menjatuhkan maruah umat Islam di mata penganut agama lain.", body_style),
        Spacer(1, 2),
        Paragraph("<b>4. Tindakan &amp; Cara Menjauhi:</b> Menjaga pertuturan daripada perkataan yang menghina agama, segera meninggalkan majlis orang fasiq yang mempermainkan hukum Islam, menegur kemungkaran secara berhikmah, serta sentiasa menuntut ilmu daripada guru yang bertauliah.", body_style),
        Spacer(1, 2),
        make_tip_box("Soalan KBAT sering meminta pandangan murid tentang trend mempersenda agama di media sosial. Gunakan formula jawapan: Menasihati secara berhikmah + Menyemak fakta sahih + Melaporkan kepada pihak berkuasa JAIS agar maruah agama Islam sentiasa terpelihara.")
    ]
    story.append(make_card(tilawah_content, border_color='#a7f3d0', bg_color='#f0fdf4'))
    story.append(Spacer(1, 4))
    
    # --- TAJUK 2: HUKUM TAJWID - MAD LAZIM ---
    story.append(make_header_banner("HUKUM TAJWID: MAD LAZIM (Kadar Bacaan: Wajib 6 Harakat Secara Ijmak)", '#581c87'))
    story.append(Spacer(1, 2))
    
    tajwid_table_data = [
        [
            Paragraph("<b>Bahagian Mad Lazim</b>", tbl_cell_hdr),
            Paragraph("<b>Maksud &amp; Cara Bacaan</b>", tbl_cell_hdr),
            Paragraph("<b>Contoh Kalimah / Huruf</b>", tbl_cell_hdr),
            Paragraph("<b>Penjelasan Kaedah Tajwid</b>", tbl_cell_hdr)
        ],
        [
            Paragraph("<b>1. Mad Lazim Kalimi Mukhaffaf</b>", tbl_cell_bold),
            Paragraph("Huruf mad bertemu huruf bertanda <b>sukun asli tanpa sabdu</b> dalam satu kalimah. Dibaca 6 harakat secara ringan (tanpa dengung).", tbl_cell),
            Paragraph("<b>\"Aaall-aana\"</b><br/><i>(Surah Yunus: 51 &amp; 91)</i>", tbl_cell_bold),
            Paragraph("Satu-satunya contoh dalam al-Quran. Huruf Alif mad bertemu huruf Lam sukun tanpa tasydid.", tbl_cell)
        ],
        [
            Paragraph("<b>2. Mad Lazim Kalimi Muthaqqal</b>", tbl_cell_bold),
            Paragraph("Huruf mad bertemu huruf bertanda <b>tasydid (sabdu)</b> dalam satu kalimah. Dibaca 6 harakat secara berat dengan menekan sebutan.", tbl_cell),
            Paragraph("<b>\"Ad-Dhaallin\"</b><br/><b>\"Al-Haaqqah\"</b><br/><b>\"As-Saakhkhah\"</b>", tbl_cell_bold),
            Paragraph("Huruf Alif mad bertemu huruf Lam bersabdu. Wajib dipanjangkan 6 harakat sebelum mengidghamkan sebutan ke huruf bersabdu.", tbl_cell)
        ],
        [
            Paragraph("<b>3. Mad Lazim Harfi Mukhaffaf</b>", tbl_cell_bold),
            Paragraph("Huruf mad pada <b>fawatih as-suwar</b> (awal surah) yang bertemu sukun asli <b>tanpa idgham</b> (tidak berdengung). Dibaca 6 harakat.", tbl_cell),
            Paragraph("Huruf <b>\"Qaf\"</b><br/>Huruf <b>\"Nun\"</b><br/>Huruf <b>\"Sad\"</b><br/>Huruf <i>Lam</i> dlm <b>\"Alif Laam Raa\"</b>", tbl_cell_bold),
            Paragraph("Dieja dengan 3 huruf di mana huruf tengahnya mad dan huruf akhirnya sukun tanpa diidghamkan ke huruf seterusnya.", tbl_cell)
        ],
        [
            Paragraph("<b>4. Mad Lazim Harfi Muthaqqal</b>", tbl_cell_bold),
            Paragraph("Huruf mad pada fawatih as-suwar yang bertemu sukun asli dan <b>diidghamkan</b> (ada tasydid &amp; dengung 2 harakat). Dibaca 6 harakat.", tbl_cell),
            Paragraph("Sebutan huruf <b>Lam ke Mim</b> dalam:<br/><b>\"Alif Laaam Miiim\"</b>", tbl_cell_bold),
            Paragraph("Huruf Lam diakhiri huruf Mim sukun, bertemu huruf Mim pada kalimah seterusnya lalu berlaku Idgham Maal Ghunnah (berdengung).", tbl_cell)
        ]
    ]
    tajwid_tbl = Table(tajwid_table_data, colWidths=[105, 150, 115, 145])
    tajwid_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#6b21a8')),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d8b4fe')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3e8ff')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    
    tajwid_content = [
        Paragraph("<b>Konsep Utama:</b> 'Mad' bermaksud memanjangkan suara, manakala 'Lazim' bermaksud wajib dibaca panjang 6 harakat secara sepakat ulama qiraat. Kalimi bermaksud dalam perkataan biasa, manakala Harfi bermaksud pada huruf ringkas di permulaan surah.", body_style),
        Spacer(1, 2),
        tajwid_tbl,
        Spacer(1, 2),
        make_tip_box("Hafal 8 huruf Mad Harfi melalui formula kata: <b>\"Naqasa 'Asalukum\" (N-Q-S-'A-S-L-K-M)</b> iaitu Nun, Qaf, Sad, 'Ain, Sin, Lam, Kaf, Mim. Jika huruf fawatih as-suwar selain huruf ini (seperti Ha, Ya, Tha, Ha, Ra - 'Hayyun Tahara'), ia dibaca 2 harakat sahaja (Mad Asli Harfi), BUKAN 6 harakat!")
    ]
    story.append(make_card(tajwid_content, border_color='#d8b4fe', bg_color='#faf5ff'))
    
    # End of Page 1
    story.append(PageBreak())
    
    # =========================================================================
    # MUKA SURAT 2: HADIS & AKIDAH
    # =========================================================================
    story.append(make_header_banner("BAHAGIAN HADIS: 7 DOSA BESAR YANG MEMBINASAKAN (Al-Mubiqaat)", '#0f766e'))
    story.append(Spacer(1, 2))
    
    hadis_content = [
        Paragraph("<b>Teks &amp; Pengenalan Hadis:</b> Rasulullah SAW bersabda: <i>\"Jauhilah tujuh perkara yang membinasakan (Al-Mubiqaat)...\"</i> (Riwayat Al-Bukhari &amp; Muslim daripada Saidina Abu Hurairah r.a.). Dosa besar ialah dosa yang diberi ancaman azab neraka yang keras, kemurkaan Allah, atau hukuman had di dunia.", body_style),
        Spacer(1, 2),
        Paragraph("<b>Huraian Lengkap 7 Dosa Besar Yang Mesti Dijauhi:</b><br/>"
                  "<b>1. Syirik Kepada Allah SWT (Dosa Paling Berat):</b> Menyekutukan Allah dalam kekuasaan atau ibadah. Terbahagi kepada <b>Syirik Jali</b> (nyata seperti menyembah patung berhala, menyembah matahari, atau memuja kubur keramat) dan <b>Syirik Khafi</b> (tersembunyi seperti riyak menunjuk-nunjuk amal dan ujub membanggakan diri). Kesannya membatalkan seluruh pahala amalan.<br/>"
                  "<b>2. Melakukan Amalan Sihir:</b> Perbuatan memudaratkan orang lain secara tersembunyi dengan bantuan jin, syaitan, atau tangkal khurafat untuk memisahkan suami isteri (sihir tafriq) atau merosakkan kesihatan. Hukumnya haram dan boleh membawa kepada murtad.<br/>"
                  "<b>3. Membunuh Jiwa Tanpa Hak:</b> Menghilangkan nyawa manusia yang diharamkan Allah membunuhnya tanpa sebab syarak yang sah seperti hukuman qisas. Perbuatan ini menghancurkan hak asasi kehidupan manusia.<br/>"
                  "<b>4. Memakan Riba:</b> Faedah atau bayaran tambahan yang disyaratkan dalam urusan pinjaman wang atau pertukaran barangan ribawi. Riba menindas golongan susah dan mengkayakan golongan pemodal secara zalim.<br/>"
                  "<b>5. Memakan Harta Anak Yatim Secara Zalim:</b> Menyalahgunakan, membelanjakan, atau merampas harta peninggalan anak yang kematian bapa sebelum baligh untuk keseronokan sendiri. Al-Quran mengumpamakannya seperti menelan api neraka ke dalam perut.<br/>"
                  "<b>6. Lari Dari Medan Peperangan Jihad:</b> Berpaling tadah dan meninggalkan barisan pertahanan negara Islam apabila berhadapan dengan tentera musuh. Tindakan pengecut ini melemahkan semangat pejuang lain dan mendedahkan negara kepada kehancuran.<br/>"
                  "<b>7. Qazaf (Menuduh Wanita Mukminah Berzina):</b> Melemparkan tuduhan zina kepada perempuan Islam yang suci maruahnya tanpa membawa 4 orang saksi lelaki yang adil. Hukumannya di dunia ialah disebat 80 kali dan kesaksiannya ditolak selama-lamanya.", body_style),
        Spacer(1, 2),
        Paragraph("<b>Faktor Terjebak &amp; Cara Membenteng Diri:</b> Faktor utama ialah kelemahan iman, kejahilan ilmu syariat, desakan hawa nafsu, dan pengaruh rakan sebaya yang rosak akhlak. Murid hendaklah mendampingi sahabat soleh, memperbanyakkan taubat nasuha, dan sentiasa mengingati azab kubur serta hari akhirat.", body_style),
        Spacer(1, 2),
        make_tip_box("Dalam soalan peperiksaan, pastikan anda TIDAK tertukar antara maksud Riba (faedah tambahan dalam pinjaman) dan Qazaf (menuduh wanita suci berzina). Hafal turutan tujuh dosa ini kerana ia kerap ditanya dalam soalan struktur dan padanan!")
    ]
    story.append(make_card(hadis_content, border_color='#99f6e4', bg_color='#f0fdfa'))
    story.append(Spacer(1, 4))
    
    # --- TAJUK 4: AKIDAH - AL-JABBAR & AJARAN SESAT ---
    story.append(make_header_banner("BAHAGIAN AKIDAH: NAMA ALLAH AL-JABBAR & BAHAYA AJARAN SESAT", '#0284c7'))
    story.append(Spacer(1, 2))
    
    akidah_content = [
        Paragraph("<b>1. Asmaul Husna: Nama Allah SWT Al-Jabbar:</b><br/>"
                  "• <b>Pengertian Lengkap:</b> Allah SWT Maha Berkuasa Memaksa sekalian makhluk-Nya menurut kehendak-Nya yang mutlak, dan tiada sesiapa pun makhluk yang mampu menghalang, menolak, atau mencabar ketetapan-Nya. Dalam masa yang sama, perkataan Al-Jabbar juga berasal daripada perkataan 'jabara' yang membawa erti Allah Maha Memperbaiki kerosakan makhluk, merawat hati yang hancur, dan mencukupkan keperluan hamba-Nya yang serba kekurangan.<br/>"
                  "• <b>Dalil Naqli:</b> Firman Allah SWT: <i>\"...Huwallahul-ladzi la ilaha illa Huwa, Al-Malikul Quddusus Salamul Mu'minul Muhaiminul 'Azizul Jabbarul Mutakabbir...\"</i> (Surah Al-Hasyr: 23).<br/>"
                  "• <b>Kesan &amp; Bukti Beriman Dalam Kehidupan:</b> Sentiasa tunduk dan patuh melaksanakan perintah Allah tanpa banyak alasan, menjauhi sifat sombong, angkuh, dan takabbur sesama manusia, bersikap tawaduk (rendah hati), serta reda dan tabah menerima takdir hidup kerana yakin setiap takdir Ilahi mempunyai hikmah yang agung.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Bahaya Ajaran Sesat &amp; Penyimpangan Akidah:</b><br/>"
                  "• <b>Definisi Ajaran Sesat:</b> Ajaran atau amalan yang dibawa oleh orang Islam atau bukan Islam yang mendakwa berlandaskan ajaran Islam sedangkan hakikatnya bercanggah dengan al-Quran, as-Sunnah, dan ijmak para ulama Ahli Sunnah Wal Jamaah.<br/>"
                  "• <b>Ciri-Ciri Ajaran Sesat (Empat Dimensi Wajib Tahu):</b><br/>"
                  "  1. <i>Aspek Akidah:</i> Mengaku diri sebagai nabi baharu, rasul akhir zaman, jelmaan tuhan, atau Imam Mahdi; serta mendakwa menerima wahyu ghaib secara langsung yang memansuhkan syariat Nabi Muhammad SAW.<br/>"
                  "  2. <i>Aspek Ibadah:</i> Mengubah cara pelaksanaan ibadah fardhu, seperti mendakwa solat lima waktu memadai dengan sekadar berniat di dalam hati tanpa rukun fi'li (rukuk dan sujud), menolak kewajipan solat Jumaat, atau menghapuskan ibadah haji.<br/>"
                  "  3. <i>Aspek Akhlak &amp; Syariat:</i> Menghalalkan perkara yang jelas diharamkan syarak, contohnya amalan nikah batin tanpa wali dan saksi, pergaulan bebas lelaki dan perempuan, serta menyerahkan harta dan wang kepada ketua ajaran.<br/>"
                  "  4. <i>Taksub Melampau (Taasub):</i> Mentafsir ayat al-Quran mengikut khayalan nafsu, mengkafirkan umat Islam lain yang tidak menyertai kumpulan mereka, serta menganggap hanya ketua mereka yang memegang kunci syurga.<br/>"
                  "• <b>Cara Membendung:</b> Mempelajari ilmu asas akidah Ahli Sunnah Wal Jamaah daripada guru bertauliah, sentiasa merujuk kemusykilan agama kepada Jabatan Agama Islam Negeri (MAIN/JAIS) atau pejabat Mufti, serta segera membuat aduan jika mengesan amalan pelik dalam kalangan rakan sebaya.", body_style),
        Spacer(1, 2),
        make_tip_box("Soalan KBAT sering bertanyakan: 'Bagaimanakah remaja boleh terhindar daripada ajaran sesat di internet?' Jawapan cemerlang: Menyemak kesahihan sumber maklumat di laman web rasmi pihak berkuasa agama dan tidak mudah terpesona dengan dakwaan mimpi atau amalan pelik tanpa dalil sahih.")
    ]
    story.append(make_card(akidah_content, border_color='#bae6fd', bg_color='#f0f9ff'))
    
    # End of Page 2
    story.append(PageBreak())
    
    # =========================================================================
    # MUKA SURAT 3: IBADAH (MUAMALAT & SOLAT GERHANA)
    # =========================================================================
    story.append(make_header_banner("BAHAGIAN IBADAH: SISTEM MUAMALAT ISLAM & ENAM JENIS AKAD", '#1e40af'))
    story.append(Spacer(1, 2))
    
    muamalat_tbl_data = [
        [
            Paragraph("<b>Nama Akad Muamalat</b>", tbl_cell_hdr),
            Paragraph("<b>Maksud &amp; Konsep Syarak</b>", tbl_cell_hdr),
            Paragraph("<b>Contoh Situasi Sebenar Dalam Kehidupan</b>", tbl_cell_hdr)
        ],
        [
            Paragraph("<b>1. Al-Bai'</b><br/>(Jual Beli)", tbl_cell_bold),
            Paragraph("Akad pertukaran sesuatu harta dengan harta yang lain atas dasar persetujuan dan kerelaan kedua-dua pihak mengikut syarat sah syarak.", tbl_cell),
            Paragraph("Murid membeli buku rujukan atau makanan di kantin sekolah dengan menyerahkan wang bayaran kepada penjual.", tbl_cell)
        ],
        [
            Paragraph("<b>2. Al-Ijarah</b><br/>(Sewaan)", tbl_cell_bold),
            Paragraph("Akad mengambil manfaat daripada sesuatu benda atau perkhidmatan orang lain dengan bayaran sewa atau upah yang dipersetujui bersama.", tbl_cell),
            Paragraph("Menyewa rumah kediaman bulanan, menaiki bas sekolah dengan membayar tambang, atau mengupah tukang jahit baju sekolah.", tbl_cell)
        ],
        [
            Paragraph("<b>3. Ar-Rahnu</b><br/>(Gadaian)", tbl_cell_bold),
            Paragraph("Menjadikan sesuatu barang yang berharga sebagai cagaran bagi jaminan sesuatu hutang sekiranya penghutang tidak dapat melunaskan hutang tersebut.", tbl_cell),
            Paragraph("Menyerahkan barang kemas emas ke institusi Ar-Rahnu bagi mendapatkan pinjaman tunai segera untuk menampung perniagaan kecil.", tbl_cell)
        ],
        [
            Paragraph("<b>4. Al-Mudharabah</b><br/>(Pelaburan Modal)", tbl_cell_bold),
            Paragraph("Akad perkongsian perniagaan antara pemilik modal (rab al-mal) dengan pengusaha (mudharib). Untung dibahagi ikut nisbah, rugi modal ditanggung pemodal.", tbl_cell),
            Paragraph("Seorang peniaga memberi modal RM10,000 kepada tukang masak untuk berniaga kuih, keuntungan dibahagi 60:40 mengikut perjanjian awal.", tbl_cell)
        ],
        [
            Paragraph("<b>5. Al-Musyarakah</b><br/>(Perkongsian Bersama)", tbl_cell_bold),
            Paragraph("Akad penggabungan modal antara dua pihak atau lebih bagi membiayai satu perniagaan, di mana keuntungan dan kerugian dikongsi bersama.", tbl_cell),
            Paragraph("Tiga orang rakan mengeluarkan modal RM5,000 seorang untuk membuka kedai buku dan menanggung untung atau rugi secara bersama.", tbl_cell)
        ],
        [
            Paragraph("<b>6. Al-Wadiah</b><br/>(Simpanan Amanah)", tbl_cell_bold),
            Paragraph("Akad menyerahkan sesuatu harta bernilai kepada pihak lain untuk disimpan, dijaga keselamatannya, dan dipulangkan semula bila diminta.", tbl_cell),
            Paragraph("Menyimpan wang tunai ke dalam akaun simpanan bank Islam di bawah prinsip Wadiah Yad Dhamanah (simpanan dengan jaminan).", tbl_cell)
        ]
    ]
    muamalat_tbl = Table(muamalat_tbl_data, colWidths=[90, 240, 185])
    muamalat_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#1e40af')),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#bfdbfe')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dbeafe')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    
    muamalat_content = [
        Paragraph("<b>1. Prinsip &amp; Asas Muamalat Islam:</b> Islam mensyariatkan urusan muamalat bagi memenuhi keperluan kebendaan manusia atas dasar reda-meredai, tolong-menolong, dan keadilan. Muamalat Islam mengharamkan empat perkara utama: <b>Riba</b> (tambahan modal pinjaman), <b>Gharar</b> (ketidakpastian atau penipuan barangan), <b>Maisir</b> (perjudian atau pertaruhan nasib), dan <b>Dharar</b> (sebarang bentuk kemudaratan kepada pihak lain).", body_style),
        Spacer(1, 2),
        muamalat_tbl,
        Spacer(1, 2),
        Paragraph("<b>Hikmah Pensyariatan:</b> Menghapuskan penindasan ekonomi oleh golongan kaya terhadap orang miskin, memastikan setiap urus niaga diberkati Allah, serta mengelakkan pertikaian dan permusuhan dalam masyarakat.", body_style)
    ]
    story.append(make_card(muamalat_content, border_color='#bfdbfe', bg_color='#eff6ff'))
    story.append(Spacer(1, 4))
    
    # --- TAJUK 6: IBADAH - SOLAT SUNAT GERHANA ---
    story.append(make_header_banner("BAHAGIAN IBADAH: SOLAT SUNAT GERHANA MATAHARI & BULAN (Kusuf & Khusuf)", '#3730a3'))
    story.append(Spacer(1, 2))
    
    gerhana_content = [
        Paragraph("<b>1. Pengenalan &amp; Hukum:</b><br/>"
                  "Solat Sunat Gerhana ialah solat sunat yang disyariatkan ketika berlaku fenomena alam gerhana matahari (dinamakan <b>Solat Al-Kusuf</b>) atau gerhana bulan (dinamakan <b>Solat Al-Khusuf</b>). Hukumnya ialah <b>Sunat Muakkad</b> (sangat dituntut) dan sangat digalakkan dilakukan secara berjemaah di masjid.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Kaifiat (Tatacara) Solat Gerhana Yang Unik &amp; Kerap Ditanya:</b><br/>"
                  "Solat ini berbeza daripada solat sunat biasa kerana mempunyai <b>dua kali rukuk dan dua kali berdiri (qiam) membaca surah bagi setiap satu rakaat</b>. Ringkasan kaifiat dua rakaat:<br/>"
                  "• <b>Rakaat Pertama:</b> Berniat solat gerhana, takbiratul ihram, membaca doa iftitah, membaca surah Al-Fatihah dan surah pilihan &gt; <b>Rukuk Pertama</b> &gt; Iktidal (bangkit berdiri semula) &gt; Membaca semula surah Al-Fatihah dan surah pilihan kedua &gt; <b>Rukuk Kedua</b> &gt; Iktidal semula &gt; Sujud dua kali seperti biasa.<br/>"
                  "• <b>Rakaat Kedua:</b> Dilakukan sama persis seperti rakaat pertama (berdiri membaca surah, rukuk, iktidal berdiri membaca surah, rukuk kedua, iktidal, dan sujud dua kali) &gt; Duduk membaca Tahiyyat Akhir &gt; Memberi salam.<br/>"
                  "• <b>Jumlah Rukun Istimewa:</b> Mempunyai <b>4 kali rukuk dan 4 kali qiam membaca surah</b> dalam dua rakaat solat.<br/>"
                  "• <b>Khutbah Gerhana:</b> Selepas solat selesai, imam disunatkan menyampaikan <b>dua khutbah</b> (seperti khutbah hari raya) yang mengandungi nasihat taubat, peringatan hari kiamat, serta seruan beramal soleh.", body_style),
        Spacer(1, 2),
        Paragraph("<b>3. Amalan Sunat Semasa Gerhana:</b> Memperbanyakkan istighfar memohon keampunan, memperbanyakkan doa, bertakbir membesarkan Allah, serta bersedekah kepada fakir miskin.", body_style),
        Spacer(1, 2),
        Paragraph("<b>4. Hikmah Pensyariatan:</b> Menolak mitos jahiliah kononnya gerhana berlaku kerana kelahiran atau kematian seseorang tokoh agung, menzahirkan rasa kerdil diri di hadapan keagungan Allah yang menguasai pergerakan cakerawala, dan menginsafi kedatangan hari kiamat.", body_style),
        Spacer(1, 2),
        make_tip_box("Hafal perbezaan istilah: <b>Kusuf</b> (dimulai huruf K) untuk Gerhana <b>Matahari</b>; manakala <b>Khusuf</b> (dimulai huruf Kh) untuk Gerhana <b>Bulan</b>. Jangan terbalikkan istilah ini dalam ujian!")
    ]
    story.append(make_card(gerhana_content, border_color='#c7d2fe', bg_color='#eef2ff'))
    
    # End of Page 3
    story.append(PageBreak())
    
    # =========================================================================
    # MUKA SURAT 4: SIRAH & ADAB ISLAMIAH
    # =========================================================================
    story.append(make_header_banner("BAHAGIAN SIRAH: TOKOH IMAM ASY-SYAFI'I R.A. & TAMADUN UMAIYYAH", '#92400e'))
    story.append(Spacer(1, 2))
    
    sirah_content = [
        Paragraph("<b>1. Tokoh Agong: Imam Asy-Syafi'i r.a. (Mujaddid Abad Ke-2 Hijrah):</b><br/>"
                  "• <b>Nama Penuh &amp; Nasab:</b> Muhammad bin Idris bin Al-Abbas bin Uthman bin Syafi'. Keturunan bangsawan Quraisy yang bertemu nasabnya dengan Rasulullah SAW pada datuknya Abd Manaf.<br/>"
                  "• <b>Kelahiran &amp; Kewafatan:</b> Dilahirkan di <b>Gaza, Palestin pada tahun 150 Hijrah</b> (tahun kewafatan Imam Abu Hanifah) dan membesar sebagai anak yatim dalam kemiskinan di Mekah. Beliau wafat di <b>Fustat, Mesir pada malam Jumaat, tahun 204 Hijrah</b> pada usia 54 tahun.<br/>"
                  "• <b>Kehebatan &amp; Genius Keilmuan:</b> Telah menghafal seluruh 30 juzuk al-Quran seawal usia <b>7 tahun</b>, menghafal kitab hadis tersohor <i>Al-Muwatta'</i> karya gurunya Imam Malik seawal usia <b>10 tahun</b>, dan diberi tauliah rasmi mengeluarkan fatwa pada usia belasan tahun oleh gurunya mufti Mekah, Imam Muslim bin Khalid az-Zanji.<br/>"
                  "• <b>Karya Agung Yang Terkenal:</b> 1. <b>Kitab Al-Umm</b> (rujukan terulung ilmu fiqh mazhab Syafi'i) dan 2. <b>Kitab Ar-Risalah</b> (kitab kaedah Usul Fiqh yang pertama ditulis di dunia).<br/>"
                  "• <b>Iktibar Buat Murid:</b> Kegigihan menuntut ilmu sejak kecil, menghormati para guru, mengutamakan hafalan al-Quran, serta sentiasa beradab tinggi ketika berbeza pandangan fiqh.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Tamadun Kerajaan Umaiyyah (41H - 132H / 661M - 750M):</b><br/>"
                  "• <b>Pengasasan &amp; Pusat:</b> Diasaskan oleh <b>Muawiyah bin Abi Sufyan</b> pada tahun 41 Hijrah selepas peristiwa penyerahan kuasa (Amul Jamaah) oleh Saidina Hasan bin Ali. Berpusat di kota <b>Damsyik, Syria</b> dan memerintah selama <b>91 tahun</b> di bawah 14 orang khalifah.<br/>"
                  "• <b>Empat Khalifah Terkenal &amp; Sumbangannya:</b><br/>"
                  "  1. <i>Muawiyah bin Abi Sufyan (Pengasas):</i> Memperkemas angkatan tentera laut Islam serta menubuhkan Diwanul Barid (pos) dan Diwanul Khatam.<br/>"
                  "  2. <i>Abdul Malik bin Marwan:</i> Menetapkan bahasa Arab sebagai bahasa rasmi urusan pentadbiran kerajaan, membina Masjid Qubbah as-Sakhrah di Baitulmaqdis, serta mencetak mata wang dinar Islam pertama bertulisan Arab.<br/>"
                  "  3. <i>Al-Walid bin Abdul Malik:</i> Mencapai zaman kegemilangan perluasan wilayah Islam hingga ke benua Eropah (Andalusia/Sepanyol) dan benua Asia (India), serta membina institusi khas menjaga kebajikan pesakit kusta dan orang buta.<br/>"
                  "  4. <i>Umar bin Abdul Aziz (Pemerintah Adil):</i> Digelar Khalifah ar-Rasyidin kelima kerana keadilan pemerintahannya. Beliau menghapuskan cukai yang membebankan rakyat, mengembalikan harta Baitulmal yang disalah guna, memecat pegawai zalim, dan mengarahkan pembukuan hadis secara rasmi.<br/>"
                  "• <b>Faktor Kejatuhan:</b> Perebutan takhta dalam kalangan kerabat istana, kelemahan khalifah akhir yang leka dengan kemewahan dunia, dan kemunculan revolusi Bani Abbasiyyah.", body_style)
    ]
    story.append(make_card(sirah_content, border_color='#fde68a', bg_color='#fffbeb'))
    story.append(Spacer(1, 4))
    
    # --- TAJUK 8: ADAB ISLAMIAH: KHAUF & RAJA' DAN ADAB TERHADAP ORANG SAKIT ---
    story.append(make_header_banner("BAHAGIAN ADAB: KHAUF & RAJA' SERTA ADAB TERHADAP ORANG SAKIT", '#9f1239'))
    story.append(Spacer(1, 2))
    
    adab_content = [
        Paragraph("<b>1. Konsep Khauf dan Raja' (Mizan Keseimbangan Jiwa):</b><br/>"
                  "• <b>Maksud Khauf:</b> Rasa takut yang mendalam kepada kemurkaan, balasan, dan azab siksa Allah SWT dengan cara menjauhi segala larangan-Nya.<br/>"
                  "• <b>Maksud Raja':</b> Mengharap keredaan, rahmat, keampunan, pertolongan, dan syurga Allah SWT dengan bersungguh-sungguh mentaati segala suruhan-Nya.<br/>"
                  "• <b>Analogi Dua Sayap Burung:</b> Sifat Khauf dan Raja' mesti sentiasa seimbang dalam jiwa mukmin ibarat dua sayap bagi seekor burung. Jika burung hanya mempunyai sebelah sayap, ia tidak akan dapat terbang dan jatuh menyembah bumi. Begitu juga manusia: Jika hanya ada <i>Khauf</i>, manusia akan mudah berputus asa daripada rahmat Allah apabila terlanjur berdosa. Jika hanya ada <i>Raja'</i>, manusia akan bersikap lalai, sombong, dan berani berbuat maksiat kerana yakin kononnya Allah Maha Pengampun tanpa perlu bertaubat.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Adab Menziarahi Orang Sakit (Tiga Dimensi Utama Wajib Skor):</b><br/>"
                  "Menziarahi orang sakit adalah fardhu kifayah dan sunnah yang sangat dituntut. Adabnya merangkumi 3 dimensi penting:<br/>"
                  "• <b>1. Aspek Rohani:</b> Mengingatkan pesakit tentang kewajipan menunaikan solat fardhu, membimbingnya melakukan rukhsah bersuci (tayamum jika tidak boleh terkena air) dan rukhsah solat (solat secara duduk atau mengiring mengikut kemampuan), mendoakan kesembuhan pesakit dengan doa yang ma'thur, menasihatinya agar reda dan sabar menghadapi ujian, serta mentalqinkan kalimah tauhid <i>\"La ilaha illallah\"</i> sekiranya pesakit sedang nazak.<br/>"
                  "• <b>2. Aspek Jasmani:</b> Membawa buah tangan yang sesuai dan berkhasiat (seperti buah-buahan segar atau makanan kesihatan), membantu menguruskan keperluan ubat atau rawatan pesakit, serta memastikan kebersihan, pengudaraan, dan keselesaan tempat tinggal pesakit.<br/>"
                  "• <b>3. Aspek Emosi:</b> Bertutur dengan kata-kata yang lemah lembut dan menyenangkan hati, memberikan kata-kata motivasi dan semangat untuk cepat sembuh, tidak bercakap perkara negatif yang merisaukan pesakit, serta memendekkan waktu ziarah agar tidak mengganggu rehat pesakit.", body_style),
        Spacer(1, 2),
        make_tip_box("<b>Formula Menjawab Soalan KBAT 4 Markah SPM:</b> Gunakan formula <b>I + H + HL + K</b>:<br/>"
                     "<b>[Isi (1m)]:</b> Nyatakan fakta utama secara tepat. &gt; <b>[Huraian (1m)]:</b> Berikan hujah/sebab (gunakan kata hubung 'kerana / dengan cara'). &gt; <b>[Huraian Lengkap (1m)]:</b> Terangkan kesan/contoh (gunakan 'kesannya / contohnya'). &gt; <b>[Kesimpulan (1m)]:</b> Berikan cadangan penutup (gunakan 'Kesimpulannya, kita hendaklah... agar...').")
    ]
    story.append(make_card(adab_content, border_color='#fecdd3', bg_color='#fff1f2'))
    
    # Build Document
    doc.build(story, canvasmaker=StudentNotesCanvas)
    print("Nota Lengkap 4 Pages build successful:", pdf_filename)

if __name__ == "__main__":
    build_pdf()

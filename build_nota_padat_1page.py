import os
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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

# Page Geometry: A4 (595.27 x 841.89 pt)
P_WIDTH, P_HEIGHT = A4
MARGIN = 14
CONTENT_W = P_WIDTH - (2 * MARGIN)  # 567.27 pt
COL_W = (CONTENT_W - 8) / 2.0        # 279.63 pt per column

styles = getSampleStyleSheet()

# Typography Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=10,
    leading=12,
    alignment=1,
    textColor=colors.HexColor('#064e3b')
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Arial',
    fontSize=6.5,
    leading=8.5,
    alignment=1,
    textColor=colors.HexColor('#334155')
)

box_hdr_style = ParagraphStyle(
    'BoxHdr',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=7.2,
    leading=9,
    textColor=colors.white
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Arial',
    fontSize=6.2,
    leading=7.8,
    textColor=colors.HexColor('#0f172a')
)

bold_style = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Arial-Bold',
    fontSize=6.2,
    leading=7.8,
    textColor=colors.HexColor('#0f172a')
)

def make_section_box(title, paragraphs, bg_header='#065f46', bg_body='#f8fafc', border_color='#cbd5e1'):
    """Creates a beautifully styled micro-card with a solid header and full content."""
    flow = []
    # Header
    hdr_p = Paragraph(f"<b>{title}</b>", box_hdr_style)
    hdr_t = Table([[hdr_p]], colWidths=[COL_W])
    hdr_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_header)),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    flow.append(hdr_t)
    
    # Body Content
    body_flow = []
    for p in paragraphs:
        if isinstance(p, str):
            body_flow.append(Paragraph(p, body_style))
        else:
            body_flow.append(p)
            
    body_t = Table([[body_flow]], colWidths=[COL_W])
    body_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_body)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    flow.append(body_t)
    return flow

def generate_pdf():
    pdf_filename = "C:/Users/User/.gemini/antigravity/scratch/pendidikan-islam-tingkatan4/Nota_Padat_Lengkap_Pendidikan_Islam_Tingkatan_4.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    
    story = []
    
    # --- TOP HEADER BANNER ---
    header_content = [
        Paragraph("<b>NOTA POKET LENGKAP PENDIDIKAN ISLAM TINGKATAN 4 (KSSM / SPM)</b>", title_style),
        Paragraph("<b>Kuasai 7 Bahagian Utama:</b> Tilawah (Larangan Mempersenda Agama) • Hadis (7 Dosa Besar) • Tajwid (Mad Lazim) • Akidah (Al-Jabbar & Ajaran Sesat) • Ibadah (Muamalat & Solat Gerhana) • Sirah (Imam Asy-Syafi'i & Umaiyyah) • Adab (Khauf-Raja' & Adab Orang Sakit)", subtitle_style)
    ]
    hdr_box = Table([[header_content]], colWidths=[CONTENT_W])
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
    
    # --- LEFT COLUMN CARDS ---
    left_flow = []
    
    # 1. TILAWAH: LARANGAN MEMPERSENDAKAN AGAMA
    left_flow.extend(make_section_box(
        "1. TILAWAH: LARANGAN MEMPERSENDAKAN AGAMA (Surah Al-An'am: 70)",
        [
            "<b>Tuntutan Ayat:</b> Allah SWT memerintahkan umat Islam agar memutuskan hubungan persahabatan dan menjauhi golongan yang menjadikan agama Islam sebagai senda gurau dan permainan duniawi semata-mata.",
            "<b>Bentuk-Bentuk Perbuatan Mempersendakan Agama:</b><br/>"
            "• <b>Menghina hukum syarak:</b> Meremehkan kewajipan solat fardhu, puasa Ramadan, kewajipan menutup aurat secara sempurna, serta mempertikaikan hukum jenayah syariah (hudud/qisas).<br/>"
            "• <b>Mempersenda al-Quran &amp; Sunnah:</b> Mempermainkan ayat suci al-Quran atau hadis Nabi SAW sebagai bahan lawak jenaka, satira, komedi, atau ejekan.<br/>"
            "• <b>Mentafsir mengikut hawa nafsu:</b> Menolak ketetapan hukum ijmak ulama muktabar dan menghalalkan perkara haram mengikut logik akal manusia.<br/>"
            "• <b>Berbangga dengan maksiat:</b> Menunjuk-nunjuk perbuatan dosa secara terbuka di khalayak ramai atau memuat naiknya di media sosial tanpa rasa bersalah.",
            "<b>Kesan Perbuatan:</b> Batal iman dan terkeluar daripada Islam (murtad) jika menolak ketetapan agama, dilaknat oleh Allah SWT, jiwa sentiasa gelisah, dan di akhirat diseksa dengan minuman air panas menggelegak serta azab neraka yang amat pedih.",
            "<b>Tindakan Muslim:</b> Menjauhi majlis orang fasik yang meremehkan agama, mengingkari kemungkaran dengan lisan atau hati, serta mendalami ilmu Ahli Sunnah Wal Jamaah."
        ],
        bg_header='#047857', bg_body='#f0fdf4', border_color='#a7f3d0'
    ))
    left_flow.append(Spacer(1, 3.5))
    
    # 2. HADIS: 7 DOSA BESAR YANG MESTI DIJAUHI
    left_flow.extend(make_section_box(
        "2. HADIS: 7 DOSA BESAR YANG MEMBINASAKAN (Al-Mubiqaat)",
        [
            "<b>Hadis Sahih (Bukhari &amp; Muslim):</b> Rasulullah SAW bersabda: <i>\"Jauhilah tujuh perkara yang membinasakan (Al-Mubiqaat)...\"</i>",
            "<b>Senarai Lengkap 7 Dosa Besar &amp; Pengertiannya:</b><br/>"
            "1. <b>Syirik kepada Allah SWT:</b> Menyekutukan Allah dalam ibadah, sifat, atau kekuasaan-Nya. Terbahagi kepada <i>Syirik Jali</i> (nyata seperti menyembah berhala/jin) dan <i>Syirik Khafi</i> (tersembunyi seperti riyak, takabbur, dan menunjuk amal).<br/>"
            "2. <b>Melakukan Sihir:</b> Perbuatan yang memudaratkan orang lain secara tersembunyi dengan bantuan jin, iblis, dan syaitan yang boleh merosakkan akidah.<br/>"
            "3. <b>Membunuh Jiwa Tanpa Hak:</b> Meragut nyawa manusia yang diharamkan Allah membunuhnya tanpa sebab syarak yang sah seperti qisas.<br/>"
            "4. <b>Memakan Riba:</b> Sebarang faedah atau penambahan modal yang disyaratkan dalam urusan pinjaman wang atau pertukaran barangan ribawi.<br/>"
            "5. <b>Memakan Harta Anak Yatim Secara Zalim:</b> Menggunakan atau menghabiskan harta anak yang kematian bapa sebelum baligh demi kepentingan peribadi.<br/>"
            "6. <b>Lari dari Medan Perang:</b> Meninggalkan barisan jihad mempertahankan kedaulatan Islam dan tanah air semasa berhadapan dengan serangan musuh.<br/>"
            "7. <b>Menuduh Perempuan Beriman Berzina (Qazaf):</b> Menuduh wanita mukminah yang suci dan terpelihara maruahnya berzina tanpa membawa 4 saksi adil.",
            "<b>Pengajaran Hadis:</b> Dosa besar meruntuhkan maruah individu, memporak-perandakan masyarakat, serta menghalang rahmat dan keberkatan hidup di dunia dan akhirat."
        ],
        bg_header='#0f766e', bg_body='#f0fdfa', border_color='#99f6e4'
    ))
    left_flow.append(Spacer(1, 3.5))
    
    # 3. HUKUM TAJWID: MAD LAZIM
    left_flow.extend(make_section_box(
        "3. HUKUM TAJWID: MAD LAZIM (Kadar Panjang: Wajib 6 Harakat)",
        [
            "<b>Maksud Mad Lazim:</b> Huruf mad bertemu dengan huruf bertanda sukun asli ketika bacaan wasal (sambung) atau waqaf (berhenti). Wajib dibaca 6 harakat secara ijmak ulama qiraat.",
            "<b>Empat Pembahagian Mad Lazim &amp; Contoh Lengkap:</b><br/>"
            "• <b>1. Mad Lazim Kalimi Mukhaffaf:</b> Huruf mad bertemu huruf bertanda sukun asli tanpa sabdu dalam satu perkataan. Dibaca ringan 6 harakat tanpa idgham. Contoh tunggal dalam al-Quran: perkataan <b>\"Aaall-aana\"</b> (Surah Yunus: ayat 51 &amp; 91).<br/>"
            "• <b>2. Mad Lazim Kalimi Muthaqqal:</b> Huruf mad bertemu huruf bertasydid (sabdu) dalam satu perkataan. Dibaca berat 6 harakat dengan memberatkan sebutan huruf bersabdu. Contoh: <b>\"Ad-Dhaallin\"</b> (Surah Al-Fatihah), <b>\"Al-Haaqqah\"</b>, <b>\"As-Saakhkhah\"</b>.<br/>"
            "• <b>3. Mad Lazim Harfi Mukhaffaf:</b> Huruf mad pada huruf fawatih as-suwar (awal surah) yang bertemu sukun asli tanpa diidghamkan (tiada dengung/sabdu). Contoh sebutan huruf: <b>\"Qaf\"</b>, <b>\"Nun\"</b>, <b>\"Sad\"</b>, dan huruf <b>\"Lam\"</b> dalam <i>\"Alif Laaam Raa\"</i>.<br/>"
            "• <b>4. Mad Lazim Harfi Muthaqqal:</b> Huruf mad pada huruf awal surah yang bertemu sukun asli dan diidghamkan (ada tasydid serta dengung 2 harakat). Contoh: Sebutan huruf <b>\"Lam\" ke \"Mim\"</b> dalam kalimah <b>\"Alif Laaam Miiim\"</b> (dibaca: <i>Lāāāmmīīīm</i>).",
            "<b>Formula 8 Huruf Mad Harfi:</b> Terkumpul dalam rangkai kata: <b>\"Naqasa 'Asalukum\"</b> (8 Huruf: Nun, Qaf, Sad, 'Ain, Sin, Lam, Kaf, Mim)."
        ],
        bg_header='#6b21a8', bg_body='#faf5ff', border_color='#e9d5ff'
    ))
    left_flow.append(Spacer(1, 3.5))
    
    # 4. AKIDAH: AL-JABBAR & AJARAN SESAT
    left_flow.extend(make_section_box(
        "4. AKIDAH: NAMA ALLAH AL-JABBAR &amp; BAHAYA AJARAN SESAT",
        [
            "<b>Nama Allah SWT Al-Jabbar:</b> Allah SWT Maha Berkuasa Memaksa sekalian makhluk menurut kehendak-Nya yang mutlak, dan tiada sesiapa pun mampu menghalang pelaksanaan ketetapan-Nya. Dia juga Maha Memperbaiki segala kerosakan dan kesusahan makhluk-Nya.",
            "• <b>Dalil Naqli:</b> Firman Allah: <i>\"...Al-Azizul Jabbarul Mutakabbir...\"</i> (Surah Al-Hasyr: 23).<br/>"
            "• <b>Bukti Beriman:</b> Tunduk dan patuh mentaati segala syariat Allah, menjauhi sikap sombong (takabbur) dan angkuh sesama manusia, reda terhadap takdir Ilahi, serta sentiasa memohon pertolongan hanya kepada Allah ketika ditimpa kesusahan.",
            "<b>Ajaran Sesat:</b> Ajaran atau amalan yang dibawa oleh orang Islam atau bukan Islam yang mendakwa bersumberkan Islam sedangkan hakikatnya bercanggah dengan al-Quran, as-Sunnah, dan ijmak ulama.",
            "• <b>Ciri-Ciri Utama:</b> 1. <i>Akidah:</i> Mengaku diri sebagai nabi, rasul, Imam Mahdi, jelmaan tuhan, atau mendakwa menerima wahyu baharu. 2. <i>Ibadah:</i> Meminda syariat (seperti solat memadai dengan niat di dalam hati tanpa rukun fi'li, memansuhkan solat Jumaat/haji). 3. <i>Akhlak:</i> Menghalalkan perkara haram seperti nikah batin, pergaulan bebas, dan penyerahan harta kepada ketua kumpulan secara taksub.<br/>"
            "• <b>Cara Membendung:</b> Memperkukuh asas tauhid Ahli Sunnah Wal Jamaah, menyemak latar belakang guru dan tauliah mengajar dengan Jabatan Agama Islam Negeri (MAIN/JAIS), serta melaporkan sebarang aktiviti mencurigakan kepada pihak berkuasa agama."
        ],
        bg_header='#0369a1', bg_body='#f0f9ff', border_color='#bae6fd'
    ))
    
    # --- RIGHT COLUMN CARDS ---
    right_flow = []
    
    # 5. IBADAH: MUAMALAT ISLAM & JENIS AKAD
    right_flow.extend(make_section_box(
        "5. IBADAH: MUAMALAT ISLAM &amp; ENAM JENIS AKAD UTAMA",
        [
            "<b>Matlamat Muamalat Islam:</b> Mengatur urusan harta dan kewangan sesama manusia berlandaskan prinsip keadilan, ketelusan, keredaan dua pihak, serta bebas daripada penindasan demi menjamin keharmonian ekonomi ummah.",
            "<b>Unsur Haram Yang Dilarang:</b> <b>Riba</b> (faedah pinjaman), <b>Gharar</b> (ketidakpastian/samar dalam akad), <b>Maisir</b> (perjudian/pertaruhan), dan <b>Dharar</b> (kemudaratan/kezaliman).",
            "<b>Enam Akad Muamalat Utama (Wajib Faham &amp; Hafal):</b><br/>"
            "• 1. <b>Al-Bai' (Jual Beli):</b> Akad pertukaran sesuatu harta dengan harta yang lain atas persetujuan bersama mengikut syarat sah syarak.<br/>"
            "• 2. <b>Al-Ijarah (Sewaan):</b> Akad mengambil manfaat daripada sesuatu barangan atau perkhidmatan dengan bayaran sewa tertentu.<br/>"
            "• 3. <b>Ar-Rahnu (Gadaian):</b> Menjadikan sesuatu barang berharga sebagai cagaran bagi jaminan sesuatu hutang sekiranya penghutang tidak dapat melunaskannya.<br/>"
            "• 4. <b>Al-Mudharabah (Pelaburan):</b> Akad perkongsian perniagaan antara pemilik modal (rab al-mal) yang menyediakan modal dengan pengusaha (mudharib) yang menguruskan perniagaan, di mana keuntungan dikongsi mengikut nisbah dipersetujui manakala kerugian modal ditanggung pemilik.<br/>"
            "• 5. <b>Al-Musyarakah (Perkongsian):</b> Akad perkongsian antara dua pihak atau lebih untuk mengeluarkan modal bersama bagi sesuatu projek perniagaan, di mana untung dan rugi ditanggung bersama mengikut kadar modal.<br/>"
            "• 6. <b>Al-Wadiah (Simpanan):</b> Menyerahkan sesuatu harta bernilai kepada pihak lain untuk disimpan dan dipelihara keselamatannya dengan amanah."
        ],
        bg_header='#1e40af', bg_body='#eff6ff', border_color='#bfdbfe'
    ))
    right_flow.append(Spacer(1, 3.5))
    
    # 6. IBADAH: SOLAT SUNAT GERHANA
    right_flow.extend(make_section_box(
        "6. IBADAH: SOLAT SUNAT GERHANA (Kusuf &amp; Khusuf)",
        [
            "<b>Pengertian:</b> Solat sunat yang dituntut ketika berlakunya fenomena gerhana matahari (<b>Kusuf</b>) atau gerhana bulan (<b>Khusuf</b>). Hukumnya adalah <b>Sunat Muakkad</b> (sangat dituntut secara berjemaah).",
            "<b>Kaifiat Solat Gerhana (Sangat Unik &amp; Kerap Ditanya):</b><br/>"
            "• Dilakukan sebanyak <b>2 rakaat</b>.<br/>"
            "• Setiap satu rakaat mempunyai <b>dua kali berdiri (qiam) membaca surah dan dua kali rukuk</b>. (Jumlah keseluruhan: <b>4 kali rukuk dan 4 kali qiam</b> dalam 2 rakaat).<br/>"
            "• Disunatkan membaca <b>dua khutbah</b> selepas selesai solat (seperti khutbah hari raya) untuk memberi peringatan, taubat, dan nasihat.<br/>"
            "• <b>Amalan Sunat Tambahan:</b> Memperbanyakkan istighfar, bertakbir, berdoa memohon keampunan, dan bersedekah kepada fakir miskin.",
            "<b>Hikmah:</b> Menginsafi keagungan dan kekuasaan mutlak Allah SWT yang mentadbir cakerawala, menolak kepercayaan khurafat jahiliah, serta mengingatkan manusia tentang kedatangan hari kiamat."
        ],
        bg_header='#3730a3', bg_body='#eef2ff', border_color='#c7d2fe'
    ))
    right_flow.append(Spacer(1, 3.5))
    
    # 7. SIRAH: IMAM ASY-SYAFI'I & KERAJAAN UMAIYYAH
    right_flow.extend(make_section_box(
        "7. SIRAH: IMAM ASY-SYAFI'I R.A. &amp; TAMADUN KERAJAAN UMAIYYAH",
        [
            "<b>Imam Asy-Syafi'i r.a. (Tokoh Mazhab Syafi'i):</b><br/>"
            "• <i>Nama Penuh:</i> Muhammad bin Idris bin Al-Abbas bin Uthman bin Syafi'. Keturunan Quraisy nasab bertemu Rasulullah SAW pada Abd Manaf.<br/>"
            "• <i>Kelahiran &amp; Kewafatan:</i> Lahir di <b>Gaza, Palestin pada tahun 150 Hijrah</b> (tahun wafat Imam Abu Hanifah) dan wafat di <b>Mesir pada tahun 204 Hijrah</b> (usia 54 tahun).<br/>"
            "• <i>Keilmuan:</i> Hafal al-Quran usia <b>7 tahun</b>, hafal kitab <i>Al-Muwatta'</i> usia <b>10 tahun</b>, diberi tauliah berfatwa pada usia belasan tahun oleh mufti Mekah Imam Muslim bin Khalid az-Zanji.<br/>"
            "• <i>Karya Agung:</i> <b>Kitab Al-Umm</b> (rujukan fiqh agung mazhab Syafi'i) dan <b>Kitab Ar-Risalah</b> (kitab kaedah Usul Fiqh terawal di dunia).",
            "<b>Kerajaan Umaiyyah (41H - 132H / 661M - 750M):</b><br/>"
            "• Diasaskan oleh <b>Muawiyah bin Abi Sufyan</b> berpusat di <b>Damsyik, Syria</b> dan memerintah selama <b>91 tahun</b>.<br/>"
            "• <b>Khalifah Unggul:</b> 1. <i>Abdul Malik bin Marwan:</i> Menetapkan bahasa Arab bahasa rasmi, membina Masjid Qubbah as-Sakhrah, dan mencetak mata wang dinar Islam pertama. 2. <i>Al-Walid bin Abdul Malik:</i> Memperluas wilayah ke Andalusia dan membina institusi kebajikan. 3. <i>Umar bin Abdul Aziz:</i> Zaman keadilan sosial keemasan, memulihkan Baitulmal, dan memulakan pembukuan hadis secara rasmi.<br/>"
            "• <i>Faktor Kejatuhan:</i> Perebutan takhta keluarga diraja dan kebangkitan Revolusi Abbasiyyah."
        ],
        bg_header='#92400e', bg_body='#fffbeb', border_color='#fde68a'
    ))
    right_flow.append(Spacer(1, 3.5))
    
    # 8. ADAB: KHAUF & RAJA' SERTA ADAB ORANG SAKIT
    right_flow.extend(make_section_box(
        "8. ADAB: KHAUF &amp; RAJA' SERTA ADAB TERHADAP ORANG SAKIT",
        [
            "<b>Konsep Khauf dan Raja' (Mizan / Keseimbangan):</b><br/>"
            "• <b>Khauf:</b> Rasa takut kepada kemurkaan dan azab Allah SWT dengan meninggalkan segala bentuk maksiat dan larangan-Nya.<br/>"
            "• <b>Raja':</b> Mengharap keredaan, rahmat, keampunan, dan syurga Allah SWT dengan bersungguh-sungguh melaksanakan segala perintah-Nya.<br/>"
            "• <b>Umpama Dua Sayap Burung:</b> Khauf dan Raja' wajib seimbang. Jika hanya ada <i>Khauf</i>, manusia akan mudah berputus asa daripada rahmat Allah. Jika hanya ada <i>Raja'</i>, manusia akan lalai, leka, dan berani berbuat dosa kerana menyangka Allah pasti mengampunkan tanpa bertaubat.",
            "<b>Adab Terhadap Orang Sakit (Tiga Aspek Utama Wajib Kuasai):</b><br/>"
            "• 1. <b>Aspek Rohani:</b> Mengingatkan pesakit tentang kewajipan solat fardhu serta membimbing rukhsah bersuci (tayamum) dan rukhsah solat (secara duduk/baring), mendoakan kesembuhan, menasihati agar reda dengan ujian, serta mentalqinkan kalimah syahadah sekiranya pesakit sedang nazak.<br/>"
            "• 2. <b>Aspek Jasmani:</b> Membawa buah tangan yang bermanfaat dan berkhasiat, membantu menguruskan keperluan ubat atau rawatan pesakit, serta memastikan kebersihan dan keselesaan tempat tinggal pesakit.<br/>"
            "• 3. <b>Aspek Emosi:</b> Bertutur dengan kata-kata yang lemah lembut dan menyenangkan hati, memberikan kata-kata motivasi dan semangat untuk sembuh, tidak bercakap perkara yang membimbangkan pesakit, serta memilih waktu ziarah yang sesuai agar tidak mengganggu waktu rehat pesakit."
        ],
        bg_header='#9f1239', bg_body='#fff1f2', border_color='#fecdd3'
    ))
    
    # --- COMBINE INTO TWO COLUMNS ---
    columns_table = Table([[left_flow, right_flow]], colWidths=[COL_W, COL_W])
    columns_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(columns_table)
    
    # Build Document
    doc.build(story)
    print("Nota Padat 1 Page build successful:", pdf_filename)

if __name__ == "__main__":
    generate_pdf()

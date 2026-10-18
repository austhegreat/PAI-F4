# e-Kalam T4: Gerbang Ulang Kaji Pendidikan Islam Tingkatan 4 🕌📚

Landing page interaktif dan responsif khusus untuk murid **Tingkatan 4** bagi menguasai kata kunci peperiksaan subjek **Pendidikan Islam (KSSM / SPM)**.

---

## 🌟 Kandungan & Topik Silibus Yang Diliputi

Laman web ini merangkumi kesemua 7 bahagian utama dan tajuk wajib peperiksaan yang diminta:

1. **Bhgn Tilawah Al-Quran**:
   - *Larangan Mempersendakan Agama* (Surah Al-An'am: 70)
2. **Bhgn Hadis**:
   - *7 Dosa Besar Yang Mesti Dijauhi* (Al-Mubiqaat: Syirik, Sihir, Membunuh, Riba, Harta Anak Yatim, Lari Medan Perang, Qazaf)
3. **Hukum Tajwid**:
   - *Mad Lazim (6 Harakat)*: Kalimi Mukhaffaf/Muthaqqal & Harfi Mukhaffaf/Muthaqqal (Formula: نقص عسلكم)
4. **Bhgn Akidah**:
   - *Nama Allah: Al-Jabbar* (Maha Berkuasa Memaksa & Memperbaiki)
   - *Ajaran Sesat* (Ciri-ciri, kesan, dan cara membendung)
5. **Bhgn Ibadah**:
   - *Muamalat Islam* (Al-Bai', Al-Ijarah, Ar-Rahnu, Mudharabah, Musyarakah, Wadiah)
   - *Solat Sunat Gerhana* (Kusuf & Khusuf, kaifiat 4 rukuk 4 qiam, 2 khutbah)
6. **Bhgn Sirah**:
   - *Imam Asy-Syafi'i r.a.* (Riwayat hidup, Gaza 150H - Mesir 204H, Kitab Al-Umm & Ar-Risalah)
   - *Kerajaan Umaiyyah* (Muawiyah bin Abi Sufyan, Damsyik, Umar bin Abdul Aziz, mata wang dinar)
7. **Bhgn Adab**:
   - *Khauf dan Raja'* (Konsep mizan seimbang dua sayap burung)
   - *Adab Terhadap Orang Sakit* (Aspek Rohani, Jasmani, Emosi)

---

## 🚀 Ciri-Ciri Utama Laman Web

- 🔍 **Carian Pantas Kata Kunci**: Taip nama tokoh, hukum tajwid, atau istilah untuk saringan segera.
- 📂 **Modal Deep-Dive**: Tekan mana-mana kad untuk membaca nota lengkap, dalil naqli, dan kata kunci skema pemarkahan.
- 🎴 **Kad Imbasan (Flashcards)**: Mod latihan pantas menguji ingatan soalan & jawapan.
- 📝 **Kuiz Interaktif SPM (10 Soalan)**: Soalan aneka pilihan dengan maklum balas segera dan skema jawapan.
- 🎯 **Panduan Menjawab KBAT (4 Markah)**: Format I + H + HL + K berserta contoh jawapan sebenar.
- 📋 **Penjejak Kemajuan (Tracker)**: Tanda topik yang telah dikuasai dan disimpan automatik pada *localStorage* pelayar.
- 🖨️ **Mesra Cetakan (Print / PDF)**: Sedia dicetak untuk kegunaan fizikal di dalam kelas atau dewan peperiksaan.

---

## 💻 Cara Menguji / Preview di Komputer Sendiri

Fail ini adalah **Static HTML** kendiri tanpa sebarang prapemasangan yang rumit. Anda boleh buka secara terus:

### Pilihan 1: Buka Terus Dalam Pelayar
Klik dua kali pada fail `index.html` dalam komputer anda (akan dibuka melalui Google Chrome, Edge, atau Firefox).

### Pilihan 2: Guna Local Server (Python / Node)
Dalam folder projek ini, jalankan arahan terminal:
```bash
# Menggunakan Python
python -m http.server 3000
```
Buka pelayar di: `http://localhost:3000`

---

## 📦 Panduan Push ke GitHub

Apabila anda berpuas hati dengan reka bentuk dan kandungan laman:

1. Buka terminal PowerShell / Git Bash di folder ini:
   ```powershell
   cd C:\Users\User\.gemini\antigravity\scratch\pendidikan-islam-tingkatan4
   ```

2. Jalankan arahan Git:
   ```bash
   git init
   git add .
   git commit -m "feat: landing page pendidikan islam tingkatan 4 kssm"
   git branch -M main
   ```

3. Cipta repositori baharu di akaun [GitHub](https://github.com/new).
4. Sambungkan dan hantar kod ke GitHub:
   ```bash
   git remote add origin https://github.com/<USERNAME-ANDA>/<NAMA-REPO>.git
   git push -u origin main
   ```

---

## ☁️ Panduan Deploy ke Render (Static Site)

Oleh kerana laman web ini berasaskan HTML/CSS/JS statik yang ringan, ia sangat pantas untuk di-deploy secara percuma di Render:

1. Pergi ke dashboard [Render](https://dashboard.render.com).
2. Tekan butang **New +** > pilih **Static Site**.
3. Sambungkan (Connect) repositori GitHub anda yang telah di-push tadi.
4. Masukkan tetapan berikut:
   - **Name**: `pendidikan-islam-tingkatan4` (atau nama pilihan anda)
   - **Branch**: `main`
   - **Build Command**: *(Biarkan kosong / leave blank)*
   - **Publish Directory**: `.` *(atau biarkan kosong / root)*
5. Tekan butang **Create Static Site**.
6. Render akan menjana pautan percuma dalam beberapa saat (contoh: `https://pendidikan-islam-tingkatan4.onrender.com`).

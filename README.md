# 🛑 Study Stop

**Study Stop**, öğrencilerin yapamadığı soruları ve eksik olduğu konuları kaydedip takip edebileceği, seçtiği konulardan **5 soruluk yeni nesil (yeni dönem / mantık ve beceri temelli)** mini testler çözerek eksiklerini pekiştirebileceği modern ve pratik bir Python uygulamasıdır.

---

## 🌟 Temel Özellikler

1. **📌 Eksik Konular Bölümü:**
   - Sınıf Düzeyi (örn: *5. Sınıf*, *8. Sınıf / LGS*, *9. Sınıf*, *12. Sınıf / YKS*, *Üniversite* vb.)
   - Ders (örn: *Matematik*, *Fen Bilimleri*, *Türkçe*, *Fizik*, *Kimya*, *Biyoloji* vb.)
   - Eksik Konu Adı (örn: *Çarpanlar ve Katlar*, *Basınç*, *Paragrafta Anlam*)
   - Yapılamayan Soru Notu (Zorlandığınız noktalar veya soru tipleri)
   - Konuları ekleme, listeleme, silme ve her konudan kaç kez test çözüldüğünü takip etme.

2. **📝 Yeni Nesil 5 Soruluk Mini Test:**
   - Eksik konular listenizden dilediğiniz konuyu tek tıkla seçin.
   - Sistem seçilen sınıf, ders ve konuya özel **5 adet yeni nesil, A-B-C-D şıklı** soru hazırlar.
   - Gerçek hayat senaryoları, kontrollü deneyler, tablo/veri analizleri ve mantık muhakeme kurguları içerir.
   - Şıkkı işaretleyip "Cevabı Onayla" dediğinizde anında **Doğru/Yanlış kontrolü** ve **detaylı adım adım çözüm açıklaması** sunulur.
   - Test bitiminde başarı yüzdesi, karne ve seviyeye uygun geri bildirim verilir.

3. **📊 Test Geçmişi:**
   - Çözülen tüm mini testlerin sonuçları (Tarih, Ders, Konu, Doğru/Soru ve Başarı Yüzdesi) otomatik olarak kaydedilir.

4. **🌐 Türkçe ve İngilizce Dil Desteği:**
   - Sağ üstteki buton ile tek tıkla **Türkçe (🇹🇷)** ve **İngilizce (🇬🇧)** arasında geçiş yapabilirsiniz. Tüm arayüz, sorular ve test mekanizması seçilen dile göre dinamik olarak güncellenir.

5. **💾 Kalıcı Veri Depolama:**
   - Verileriniz `data/studystop_data.json` dosyasında yerel olarak saklanır. Uygulamayı kapatsanız dahi konularınız ve test geçmişiniz kaybolmaz.

---

## 🚀 Kurulum ve Çalıştırma

Uygulama standart Python kütüphaneleri (`tkinter`, `json`, `uuid`) ile geliştirilmiştir. Ekstra hiçbir ağır kütüphane kurmanıza gerek yoktur!

### 1. Grafik Arayüz (Masaüstü Uygulaması)
Windows'ta doğrudan **`run.bat`** dosyasına çift tıklayabilir veya terminalden şu komutu verebilirsiniz:

```bash
python main.py
```

### 2. Komut Satırı Arayüzü (Terminal / CLI)
Eğer uygulamayı terminalden metin tabanlı kullanmak isterseniz:

```bash
python cli.py
```

---

## 📁 Proje Dosya Yapısı

```
StudyStop/
│
├── main.py                 # Tkinter tabanlı modern grafik arayüz (GUI)
├── cli.py                  # Terminal tabanlı alternatif komut satırı arayüzü
├── question_engine.py      # 5 adet yeni nesil soru üreten akıllı soru motoru
├── storage.py              # Konuları ve test geçmişini saklayan veri yöneticisi
├── localization.py         # Türkçe ve İngilizce dil çevirileri
├── run.bat                 # Windows için tek tıkla başlatma kısayolu
├── README.md               # Kullanım kılavuzu ve proje dökümanı
└── data/
    └── studystop_data.json # Kullanıcı verileri (otomatik kaydedilir)
```

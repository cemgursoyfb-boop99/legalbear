# 🐻 legalbear

**legalbear**, kişisel veri koruma süreçlerini kolaylaştırmak için geliştirilmiş açık kaynaklı bir hukuk asistanıdır. KVKK (Kişisel Verilerin Korunması Kanunu) ve GDPR (General Data Protection Regulation) kapsamında veri analizi, şablon metin üretimi ve yasal soruları yanıtlamak için tasarlanmıştır.

## ✨ Özellikler

### 🔍 KVKK Risk Analizi
- Metin içerisindeki kişisel verileri otomatik tespit eder
- TCKN, ad-soyad, e-posta, telefon, IP adresi, adres gibi verileri tanır
- Özel nitelikli verileri (sağlık, biyometrik, ceza mahkumiyet) tespit eder
- PxI (Olasılık x Etki) mantığına göre risk skoru hesaplar
- Hukuki risk ifadelerini analiz eder ve öneriler sunar

### 📄 Şablon Metin Üretimi
- **KVKK Açık Rıza Metni**: Kişisel veri işleme için açık rıza metni
- **KVKK Bilgilendirme Metni**: Veri sorumlusu aydınlatma metni
- **GDPR Açık Rıza Metni**: GDPR uyumlu consent form
- **Ziyaretçi Aydınlatma Metni**: Ziyaretçi verilerinin işlenmesine dair bilgilendirme

### 🤖 KVKK Arama Motoru
- KVKK hakkında sık sorulan soruları yanıtlar
- Yapay zeka destekli soru-cevap sistemi
- Hızlı ve doğru yasal bilgi erişimi

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)

### Adımlar

1. **Projeyi klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/legalbear.git
   cd legalbear
   ```

2. **Bağımlılıkları yükleyin:**
   ```bash
   pip install fastapi uvicorn jinja2 pydantic
   ```

3. **Uygulamayı başlatın:**
   ```bash
   uvicorn api:app --reload
   ```

4. **Tarayıcınızda açın:**
   ```
   http://localhost:8000
   ```

## 📖 Kullanım

### Web Arayüzü
1. Uygulamayı başlattıktan sonra tarayıcınızda `http://localhost:8000` adresine gidin
2. Sol menüden istediğiniz modülü seçin:
   - **KVKK Risk Analizi**: Metin analizi yapın
   - **KVKK Arama Motoru**: Sorularınızı sorun
   - **Şablon Üretimi**: KVKK/GDPR metinleri oluşturun

### API Kullanımı

#### Risk Analizi
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ali Yılmaz, TCKN: 12345678901, e-posta: ali@example.com"}'
```

#### Şablon Üretimi
```bash
curl -X POST "http://localhost:8000/template/kvkk-consent" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ali Yılmaz", "company": "VeriTech"}'
```

## 🛠️ Teknolojiler

- **Backend**: FastAPI, Python
- **Frontend**: HTML, JavaScript, CSS
- **Analiz**: Regular Expressions, Pattern Matching
- **Şablonlar**: Python String Formatting

## 📁 Proje Yapısı

```
legalbear/
├── api.py                 # FastAPI backend uygulaması
├── text_analyzer.py       # KVKK risk analizi modülü
├── templates.py           # Şablon metin üreticileri
├── legal_info.py          # KVKK/GDPR bilgi modülü
├── main.py                # Konsol uygulaması (test için)
├── frontend/
│   ├── index.html         # Web arayüzü
│   └── legalbear.png      # Logo
├── knowledge/
│   ├── knowledge_base.py  # Bilgi tabanı modülü
│   └── data/
│       └── kvkk_qa.txt    # Soru-cevap verisi
├── LICENSE                # MIT Lisansı
└── README.md              # Bu dosya
```

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: Sözleşme Analizi
Bir hizmet sözleşmesini analiz ederek kişisel veri işleme risklerini tespit edin.

### Senaryo 2: Açık Rıza Metni
Müşterileriniz için KVKK uyumlu açık rıza metni oluşturun.

### Senaryo 3: Bilgilendirme Metni
Veri sorumlusu olarak ilgili kişileri bilgilendirmek için aydınlatma metni hazırlayın.

### Senaryo 4: Yasal Sorular
KVKK hakkında merak ettiğiniz soruları hızlıca yanıtlayın.

## ⚠️ Önemli Notlar

- Bu araç **hukuki tavsiye** vermez. Yasal danışmanlık için mutlaka bir avukata başvurun.
- Tespit edilen riskler ve öneriler **bilgilendirme amaçlıdır**.
- KVKK ve GDPR düzenlemeleri sürekli güncellenmektedir. Mevcut mevzuatı takip edin.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 👥 Geliştiriciler

- legalbear Ekibi

## 📧 İletişim

Sorularınız ve önerileriniz için issue açabilirsiniz.

## 🙏 Teşekkürler

- Açık kaynak topluluğuna
- KVKK ve GDPR mevzuatını takip eden tüm kuruluşlara

---

**⚠️ Yasal Uyarı**: Bu yazılım, kişisel veri koruma süreçlerini kolaylaştırmak için tasarlanmıştır ancak yasal danışmanlık yerine geçmez. Önemli hukuki kararlar için mutlaka bir avukata danışın.


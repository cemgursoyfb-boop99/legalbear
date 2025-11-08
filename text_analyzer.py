import re
from typing import List, Dict, Any

# --- KVKK Veri ve Risk Tanımları ---

# 1. Kişisel Veri Örüntüleri ve Nitelikleri
# Özel Nitelikli Veriler (Gizlilik Etkisi Yüksek)
OZEL_NITELIKLI_VERI_PATTERNS = {
    "Sağlık Verisi": {
        "pattern": r"\b(hastalık|tanı|tedavi|ameliyat|ilaç|epükriz|sağlık raporu|tıbbi)\b",
        "gizlilik_etkisi": 5 # Etki (Impact) Puanı
    },
    "Biyometrik Veri": {
        "pattern": r"\b(parmak izi|retina taraması|yüz tanıma|ses kaydı|iris)\b",
        "gizlilik_etkisi": 5
    },
    "Ceza Mahk. Verisi": {
        "pattern": r"\b(mahkumiyet|hüküm|ceza kaydı|adli sicil)\b",
        "gizlilik_etkisi": 4
    }
}

# Genel Nitelikli Veri Örüntüleri (Gizlilik Etkisi Orta/Düşük)
# text_analyzer.py dosyasında 2. ve son kez güncellenecek GENEL_VERI_PATTERNS kısmı:

# Genel Nitelikli Veri Örüntüleri (Gizlilik Etkisi Orta/Düşük)
GENEL_VERI_PATTERNS = {
    "TCKN": {"pattern": r"\b\d{11}\b", "gizlilik_etkisi": 4},
    
    # Ad Soyad Regex'i Güncellendi: Daha esnek bir yapıya döndük. 2 veya 3 kelimeyi büyük harfle başlayan (kişi adı/soyadı formatında) yakalar.
    # Negatif lookahead'i kaldırıyoruz ve adresi Adres regex'ine bırakıyoruz.
    "Ad Soyad": {
        "pattern": r"\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,}\s){1,2}[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}\b", 
        "gizlilik_etkisi": 3
    },
    
    "E-posta": {"pattern": r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", "gizlilik_etkisi": 2},
    "Telefon": {"pattern": r"\b(?:0\s*|\+90\s*|\(0\d{3}\)\s*|\d{3}\s*)\d{3}\s*\d{2}\s*\d{2}\b", "gizlilik_etkisi": 2},
    "IP Adresi": {"pattern": r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "gizlilik_etkisi": 1},
    
    # Adres Regex'i Güncellendi: Adres kısaltmalarını ve No/Sokak gibi anahtar kelimeleri daha agresif yakalar.
    # Bu, "Cihan Cad" gibi ifadelerin burada yakalanma olasılığını artırır.
    "Adres": {
        "pattern": r"\b\d{1,5}\s*(?:Cadde|Sokak|Mahallesi|Cd\.|Sk\.|Mh\.)[\s\S]{1,50}\b(?:No|Apt|Daire)\b|\b(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,5}(?:\s*(?:Cad\.|Sok\.|Sk\.|Mah\.|Mh\.|Blok|Apt\.|No:|Cd\.))\s*\d+",
        "gizlilik_etkisi": 2
    }
}

# Hukuki/İdari Risk İfadeleri ve Olasılık Puanları
RISK_PATTERNS = {
    "Açık Rıza Eksikliği": {
        "pattern": r"\baçık rıza alınmaksızın\b|\baçık rıza yok\b|\baçık rıza alınmadan\b",
        "olasılık_etkisi": 4, # Olasılık (Probability) Puanı
        "suggestion": "Veri işleme faaliyetleri için mutlaka geçerli bir açık rıza veya hukuki dayanak bulunmalıdır."
    },
    "Aydınlatma Yükümlülüğü İhlali": {
        "pattern": r"\bbilgilendirme yapılmaksızın\b|\bbilgilendirme yok\b|\baydınlatma yapılmadı\b",
        "olasılık_etkisi": 3,
        "suggestion": "İlgili kişilere veri işleme hakkında KVKK 10. maddeye uygun aydınlatma yapılmalıdır."
    },
    "Yurtdışı Aktarım Kriter Eksikliği": {
        "pattern": r"\byurtdışındaki\b|\byurtdışına aktarım\b",
        "olasılık_etkisi": 4,
        "suggestion": "Yurtdışına veri aktarımı için Kurul Kararlarına uygun taahhüt/rızalar veya güvenlik önlemleri gereklidir."
    },
    "Silme/Yok Etme Zorunluluğu İhlali": {
        "pattern": r"\bsaklama süresi belirsiz\b|\bsüre belirtilmemiş\b|\bimha edilmedi\b",
        "olasılık_etkisi": 2,
        "suggestion": "Veri saklama süreleri açıkça tanımlanmalı ve süresi dolan veriler derhal imha edilmelidir."
    }
}

# --- Risk Hesaplama Fonksiyonu ---

def derecelendir_risk_seviyesi(risk_skoru: int) -> str:
    """Hesaplanan PxI skoruna göre risk seviyesini belirler."""
    if risk_skoru >= 18:  # Yüksek olasılıklı x Özel Nitelikli veri (örn. 4x5=20)
        return "KRİTİK"
    elif risk_skoru >= 10: # Yüksek olasılıklı x Genel Veri (örn. 4x3=12)
        return "YÜKSEK"
    elif risk_skoru >= 4:
        return "ORTA"
    else:
        return "DÜŞÜK"

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Verilen metni analiz eder, kişisel veri örüntülerini ve KVKK risk ifadelerini bulur,
    PxI (Olasılık x Etki) mantığına göre bir risk skoru hesaplar ve öneriler sunar.
    """
    all_findings = []
    risks_detected = []
    total_risk_score = 0
    
    # Geçici Risk Skoru Tutucusu (En yüksek riski belirlemek için)
    max_risk_puan = 0

    # 1. Kişisel Veri Örüntülerini Tespit Etme (Etki (I) Belirleme)
    
    # Önce Özel Nitelikli Verileri kontrol et (Yüksek Gizlilik Etkisi)
    for label, info in OZEL_NITELIKLI_VERI_PATTERNS.items():
        matches = re.findall(info["pattern"], text, re.IGNORECASE)
        if matches:
            for match in set(matches): # Tekrarları önlemek için set kullanıldı
                all_findings.append({
                    "type": f"Özel Nitelikli Veri: {label}",
                    "match": match,
                    "etki": info["gizlilik_etkisi"]
                })
            # En yüksek gizlilik etkisini (I) kaydet
            max_risk_puan = max(max_risk_puan, info["gizlilik_etkisi"])

    # Genel Nitelikli Verileri kontrol et
    for label, info in GENEL_VERI_PATTERNS.items():
        matches = re.findall(info["pattern"], text)
        if matches:
            # "Ad Soyad" için ek filtreleme: "KVKK", "Kanunu" gibi kelimeleri içerenleri hariç tutar (yanlış pozitif azaltma)
            if label == "Ad Soyad":
                 matches = [m for m in matches if not any(word in m for word in ["Verilerin", "Kanunu", "KVKK", "Kurumu"])]
            
            for match in set(matches):
                all_findings.append({
                    "type": label,
                    "match": match,
                    "etki": info["gizlilik_etkisi"]
                })
            max_risk_puan = max(max_risk_puan, info["gizlilik_etkisi"])
    
    # Eğer hiç kişisel veri bulunamazsa, risk analizi yapmanın anlamı düşer.
    if max_risk_puan == 0:
        return {
            "findings": [],
            "risk_score": 0,
            "risk_level": "VERİ TESPİT EDİLMEDİ",
            "risks_detected": [],
        }

    # 2. Risk İfadelerini Tespit Etme (Olasılık (P) Belirleme)
    
    max_olasılık_puan = 0 # Metindeki en yüksek olasılık puanını tutar

    for risk_label, info in RISK_PATTERNS.items():
        if re.search(info["pattern"], text, re.IGNORECASE):
            risks_detected.append({
                "risk_type": risk_label,
                "suggestion": info["suggestion"],
                "olasılık": info["olasılık_etkisi"]
            })
            max_olasılık_puan = max(max_olasılık_puan, info["olasılık_etkisi"])

    # Metinde risk ifadesi bulunamazsa, varsayılan düşük bir olasılık (P=1) alınır
    if max_olasılık_puan == 0:
        max_olasılık_puan = 1

    # 3. P x I Risk Skoru Hesaplama
    # Risk Skoru = Metinde tespit edilen en yüksek Olasılık (P) x Metinde tespit edilen en yüksek Etki (I)
    total_risk_score = max_olasılık_puan * max_risk_puan
    
    # 4. Sonuçları Hazırlama
    return {
        "findings": all_findings,
        "risk_score": total_risk_score,
        "risk_level": derecelendir_risk_seviyesi(total_risk_score),
        "risks_detected": risks_detected,
    }

# --- Kullanım Örneği (API/JS bağlantısı simülasyonu) ---

if __name__ == "__main__":
    # Örnek metin (Özel Nitelikli Veri + Yüksek Risk İfadesi içeriyor)
    sample_text = """
    Sayın [Ali Veli], 12345678901 TCKN'niz ile başvurduğunuz sağlık raporunuz incelenmiştir.
    Epükriz sonucu [kalp hastalığı] teşhisi konmuştur. Şirketimiz, bu hassas verileri
    hukuki dayanak ve **açık rıza alınmaksızın** yurtdışındaki X firmasına aktarmayı planlamaktadır.
    İletişim için ali.veli@sirket.com adresini kullanabilirsiniz.
    """

    print("--- KVKK Metin Analizi Başlatılıyor ---")
    
    analysis_result = analyze_text(sample_text)
    
    print(f"\n✅ Analiz Sonucu (Risk Skoru: {analysis_result['risk_score']} - Seviye: {analysis_result['risk_level']})")
    print("-" * 50)
    
    print("\n### 🔍 Tespit Edilen Kişisel Veriler (Etki Puanları) ###")
    for item in analysis_result['findings']:
        print(f"[{item['etki']}] {item['type']}: {item['match']}")
        
    print("\n### 🚨 Tespit Edilen KVKK Hukuki Riskleri (Olasılık Puanları) ###")
    for risk in analysis_result['risks_detected']:
        print(f"[{risk['olasılık']}] Risk: {risk['risk_type']}")
        print(f"   Öneri: {risk['suggestion']}")

    # Bu çıktı, web arayüzündeki JS koduna API üzerinden JSON formatında gönderilecektir.
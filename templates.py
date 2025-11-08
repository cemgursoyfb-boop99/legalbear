# templates.py

def get_kvkk_consent_template(name="...", company="..."):
    return f"""
AÇIK RIZA METNİ (KVKK)

Tarafınıza ait kişisel veriler, {company} tarafından 6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında işlenmektedir.

Bu metin ile, {name} olarak kişisel verilerimin;
- İşlenmesine,
- Saklanmasına,
- İlgili mevzuat çerçevesinde üçüncü kişilerle paylaşılmasına

açık rıza verdiğimi beyan ederim.
"""

def get_kvkk_info_template(company="...", purpose="..."):
    return f"""
AYDINLATMA METNİ (KVKK)

{company} olarak kişisel verilerinizi aşağıdaki amaçlarla işlemekteyiz:
- {purpose}

Veri sorumlusu sıfatıyla, KVKK madde 10 kapsamında sizi bilgilendiriyor;
- Verilerinizi hukuka uygun şekilde işlediğimizi,
- İlgili kişi olarak haklarınızı kullanabileceğinizi

bildiriyoruz.
"""

def get_gdpr_consent_template(name="...", organization="..."):
    return f"""
GDPR CONSENT FORM

I, {name}, hereby give my explicit consent to {organization} for the processing of my personal data in accordance with the General Data Protection Regulation (EU) 2016/679.

This includes:
- Collection and storage of personal data
- Sharing with authorized third parties
- Use for specified lawful purposes

I understand my rights under GDPR and confirm my informed consent.
"""

def get_visitor_info_template(
    company="...",
    contact="...",
    purpose="Bina güvenliğinin sağlanması",
    method="kamera kaydı ve ziyaretçi kayıt defteri",
    legal_basis="KVKK m.5/2-ç (hukuki yükümlülük)",
    transfer="yetkili kamu kurum ve kuruluşları"
):
    return f"""
ZİYARETÇİ AYDINLATMA METNİ

{company} olarak, ofisimize gelen ziyaretçilerin kişisel verilerini 6698 sayılı Kişisel Verilerin Korunması Kanunu (“KVKK”) kapsamında işlemekteyiz.

Ziyaret sırasında alınan kişisel veriler (ad-soyad, giriş-çıkış saati, kamera kaydı vb.), {purpose} amacıyla {method} yoluyla işlenmektedir. İşleme hukuki dayanağı: {legal_basis}.

Kişisel verileriniz, {transfer} ile paylaşılabilir. KVKK’nın 11. maddesi kapsamında sahip olduğunuz haklarınızı kullanmak için {contact} üzerinden bizimle iletişime geçebilirsiniz.
"""
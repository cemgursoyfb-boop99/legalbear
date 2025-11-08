import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from difflib import get_close_matches
from pydantic import BaseModel
from text_analyzer import analyze_text
from knowledge.knowledge_base import load_kvkk_documents, answer_kvkk_question
from templates import (
    get_kvkk_consent_template,
    get_kvkk_info_template,
    get_gdpr_consent_template,
    get_visitor_info_template
)
KVKK_QA_PATH = os.path.join(os.path.dirname(__file__), "knowledge", "data", "kvkk_data.json")

# FastAPI uygulaması ve frontend bağlantısı
app = FastAPI(title="legalbear API", description="KVKK & GDPR metin analiz ve şablon API'si", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Global Veri Yükleme ---
try:
    DOCUMENTS_DATA = load_kvkk_documents()
    print(f"Bilgi tabanı yüklendi. Bölüm Sayısı: {len(DOCUMENTS_DATA)}")
except Exception as e:
    DOCUMENTS_DATA = {}
    print(f"UYARI: Bilgi tabanı yüklenirken hata oluştu: {e}")

# --- Pydantic Modelleri ---
class TextInput(BaseModel):
    text: str

class InfoRequest(BaseModel):
    company: str
    purpose: str

class TemplateRequest(BaseModel):
    name: str
    company: str
    purpose: str = None

# --- Risk Analizi Endpoint'i ---
@app.post("/analyze")
def analyze_personal_data(input: TextInput):
    analysis_result = analyze_text(input.text)
    return analysis_result

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# --- Şablon Üretme Endpoint'leri ---
@app.post("/template/kvkk-consent")
def kvkk_consent(payload: dict):
    name = payload.get("name", "...")
    company = payload.get("company", "...")
    return {"template": get_kvkk_consent_template(name, company)}


@app.post("/template/kvkk-info")
def kvkk_info(req: dict):
    company = req.get("company", "...")
    purpose = req.get("purpose", "...")
    return {"template": get_kvkk_info_template(company, purpose)}

@app.post("/template/gdpr-consent")
def gdpr_consent(req: dict):
    name = req.get("name", "...")
    company = req.get("company", "...")
    return {"template": get_gdpr_consent_template(name, company)}

@app.post("/generate-visitor-text")
async def visitor_info(req: Request):
    try:
        data = await req.json()
        text = get_visitor_info_template(
            company=data.get("company", "..."),
            contact=data.get("contact", "..."),
            purpose=data.get("purpose", "Bina güvenliğinin sağlanması"),
            method=data.get("method", "kamera kaydı ve ziyaretçi kayıt defteri"),
            legal_basis=data.get("legal_basis", "KVKK m.5/2-ç (hukuki yükümlülük)"),
            transfer=data.get("transfer", "yetkili kamu kurum ve kuruluşları")
        )
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

@app.post("/kvkk-qa")
def kvkk_qa(payload: dict):
    question = payload.get("question", "").lower().strip()

    try:
        with open("knowledge/data/kvkk_qa.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return {"answer": "Veri dosyası yüklenemedi."}

    # 🔹 Doğrudan parça eşleşmesi
    for line in lines:
        line = line.strip()
        if not line or ":" not in line:
            continue
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        key, value = parts
        if question in key.lower() or any(word in key.lower() for word in question.split()):
            return {"answer": value.strip()}

    # 🔹 Fuzzy eşleşme
    from difflib import get_close_matches
    keys = [line.split(":")[0].strip().lower() for line in lines if ":" in line]
    matches = get_close_matches(question, keys, n=1, cutoff=0.5)
    if matches:
        for line in lines:
            if line.lower().startswith(matches[0]):
                return {"answer": line.split(":", 1)[1].strip()}

    return {"answer": "Bu konuda daha fazla bilgiye ihtiyacım var. Lütfen daha ayrıntılı sorun."}

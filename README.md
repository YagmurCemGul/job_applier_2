# AutoApply Asistanı

**AutoApply Asistanı**, kullanıcıların LinkedIn, Indeed ve hiring.cafe gibi platformlarda iş başvuru süreçlerini otomatikleştiren, üretim kalitesinde bir masaüstü uygulamasıdır.

Bu uygulama, akıllı otomasyon ve **doğrudan yapay zeka web arayüzü otomasyonunu** bir araya getirerek, her bir iş ilanı için özelleştirilmiş CV'ler ve ön yazılar oluşturur, başvuru formlarını otomatik olarak doldurur ve tüm süreci kullanıcı dostu bir arayüz üzerinden yönetir.

## Mimari Yaklaşımı: Web Arayüzü Otomasyonu

Bu proje, LLM'lerle etkileşim kurmak için API'leri kullanmak yerine, **doğrudan yapay zeka servislerinin (ChatGPT, Gemini, Claude) web arayüzlerini otomatikleştiren** bir yaklaşım benimser. Bu, kullanıcının kendi hesabıyla oturum açarak, prompt'ları metin kutusuna yazarak ve sonuçları doğrudan sayfadan kazıyarak yapılır.

### Temel Özellikler

*   **Çoklu Platform Otomasyonu:** Popüler iş platformlarında otomatik iş arama ve başvuru.
*   **Yapay Zeka Web Arayüzü Otomasyonu:** API'ler yerine ChatGPT, Gemini, Claude gibi servislerin web sitelerini doğrudan otomatize eder.
*   **Akıllı Doküman Üretimi:** Her başvuru için ilana özel CV ve ön yazı oluşturma.
*   **Güvenlik ve Gizlilik:** Tüm kullanıcı verileri ve **hassas kimlik bilgileri (parolalar)**, işletim sisteminin yerel anahtar zincirinde (keychain) güvenli bir şekilde saklanır.

## Teknolojiler

*   **Frontend:** Electron + React
*   **Backend:** Python (FastAPI)
*   **Otomasyon:** Playwright
*   **Veritabanı:** SQLite (şifrelenmiş)

---

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Önkoşullar

*   [Node.js](https://nodejs.org/) (LTS sürümü tavsiye edilir)
*   [Python](https://www.python.org/downloads/) (3.9 veya üstü)

### 1. Backend Bağımlılıklarını Yükleme

```bash
# Proje kök dizinindeyken
pip install -r backend/requirements.txt
playwright install
```

### 2. Frontend Bağımlılıklarını Yükleme

```bash
# Proje kök dizinindeyken
cd frontend
npm install
cd ..
```

---

## Çalıştırma

### 1. Backend Sunucusunu Başlatma

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Uygulamasını Başlatma

Ayrı bir terminalde:
```bash
cd frontend
npm start
```

Uygulama açıldığında, **Ayarlar (Settings)** menüsünden, otomatize etmek istediğiniz yapay zeka servisleri (ChatGPT, Gemini vb.) için **kullanıcı adı ve parolanızı** girerek başlayabilirsiniz. Bu bilgiler, işletim sisteminizin anahtar zincirinde güvenli bir şekilde saklanacaktır.

---

## Proje Yapısı

Proje, frontend ve backend olarak iki ana parçaya ayrılmıştır. Önemli dosyalar şunlardır:

```
/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── security.py       # Kimlik bilgilerini OS anahtar zincirinde yönetir.
│   │   │   ├── selectors.json    # Web otomasyonu için CSS seçicilerini saklar.
│   │   │   └── prompt_library.py # Gelişmiş prompt şablonları.
│   │   └── services/
│   │       ├── ai_engine.py      # Playwright ile AI web arayüzlerini otomatize eder.
│   │       └── automation_service.py # İş platformlarını otomatize eder.
│   └── main.py                 # Ana FastAPI uygulaması.
│
├── frontend/
│   ├── public/
│   │   ├── electron.js         # Electron ana işlem (backend'e HTTP istekleri yapar).
│   │   └── preload.js          # Güvenli IPC köprüsü.
│   └── src/
│       └── components/
│           └── Settings.js     # Kullanıcı kimlik bilgilerini girmek için UI.
│
└── README.md
```

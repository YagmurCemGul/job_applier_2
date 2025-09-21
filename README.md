# AutoApply Asistanı

**AutoApply Asistanı**, kullanıcıların LinkedIn, Indeed ve hiring.cafe gibi platformlarda iş başvuru süreçlerini otomatikleştiren, üretim kalitesinde bir masaüstü uygulamasıdır.

Bu uygulama, akıllı otomasyon ve çoklu yapay zeka (LLM) entegrasyonunu bir araya getirerek, her bir iş ilanı için özelleştirilmiş CV'ler ve ön yazılar oluşturur, başvuru formlarını otomatik olarak doldurur ve tüm süreci kullanıcı dostu bir arayüz üzerinden yönetir.

## Temel Özellikler

*   **Çoklu Platform Otomasyonu:** Popüler iş platformlarında otomatik iş arama ve başvuru.
*   **Akıllı Doküman Üretimi:** Her başvuru için ilana özel CV ve ön yazı oluşturma.
*   **Çoklu LLM Desteği:** En iyi sonuçlar için OpenAI, Google ve Anthropic modellerini kullanma.
*   **Etkileşimli Form Doldurma:** Bilinmeyen soruları kullanıcıya sorarak öğrenme ve Soru-Cevap Bankası'na kaydetme.
*   **Güvenlik ve Gizlilik:** Tüm kullanıcı verileri yerel olarak ve şifrelenmiş bir şekilde saklanır.

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

### 1. Projeyi Klonlama

```bash
git clone <proje-repo-url>
cd <proje-klasoru>
```

### 2. Backend Bağımlılıklarını Yükleme

```bash
pip install -r backend/requirements.txt
```
Ayrıca, Playwright için tarayıcıları yüklemeniz gerekmektedir:
```bash
playwright install
```

### 3. Frontend Bağımlılıklarını Yükleme

```bash
cd frontend
npm install
cd ..
```

---

## Çalıştırma

Uygulamayı çalıştırmak için hem backend sunucusunun hem de frontend uygulamasının aynı anda çalışması gerekir.

### 1. Backend Sunucusunu Başlatma

Yeni bir terminal penceresi açın ve aşağıdaki komutu çalıştırın:
```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Sunucu şimdi `http://127.0.0.1:8000` adresinde çalışıyor olacaktır.

### 2. Frontend Uygulamasını Başlatma

Başka bir terminal penceresi açın ve aşağıdaki komutu çalıştırın:
```bash
cd frontend
npm start
```
Bu komut, React geliştirme sunucusunu başlatacak ve ardından Electron masaüstü uygulamasını açacaktır.

Uygulama açıldığında, Ayarlar (Settings) menüsünden LLM sağlayıcılarınız için API anahtarlarınızı girerek başlayabilirsiniz.

---

## Proje Yapısı

```
/
├── backend/                # Python/FastAPI backend kodu
│   ├── app/                # Ana uygulama modülleri
│   │   ├── api/            # API endpoint'leri (router'lar)
│   │   ├── core/           # Çekirdek mantık (güvenlik, prompt'lar)
│   │   ├── models/         # Pydantic veri modelleri
│   │   ├── services/       # İş mantığı (AI, otomasyon)
│   │   └── main.py         # Ana FastAPI uygulama dosyası
│   └── requirements.txt    # Python bağımlılıkları
│
├── frontend/               # Electron/React frontend kodu
│   ├── public/             # Statik dosyalar ve Electron ana betiği
│   │   ├── electron.js     # Electron ana işlem dosyası
│   │   └── preload.js      # Electron context bridge
│   ├── src/                # React kaynak kodu
│   │   ├── components/     # React bileşenleri
│   │   ├── App.js          # Ana React bileşeni
│   │   └── index.js        # React başlangıç noktası
│   └── package.json        # Node.js bağımlılıkları ve script'ler
│
└── README.md               # Bu dosya
```

# RestoOps - Backend API

RestoOps-API adalah platform backend untuk manajemen operasional restoran end-to-end: mulai dari reservasi meja + pre-order, pencatatan & orkestrasi pesanan ke dapur, pembayaran, sinkronisasi stok/bahan, hingga pelaporan bisnis—dibangun modular sehingga mudah diskalakan dan diobservasi. Fondasi domainnya mengikuti enam service inti (Order, Reservation, Payment, Catalog, Warehouse, Reporting) yang saling terintegrasi untuk efisiensi operasional dan keputusan manajerial yang lebih cepat.

## 📁 **Project Structure**

```
restoops-api/
├── api/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── menu_router.py
│   │   ├── reservation_router.py
│   │   └── sync_router.py
│   └── services/
│       ├── __init__.py
│       └── database_service.py
├── data/
│   ├── processed/
│   └── raw/
├── scripts/
│   ├── run_scraper.py
│   ├── run_reservation_seeder.py
│   └── run_preprocessing.py
├── src/
│   ├── scraper.py
│   ├── reservation_seeder.py
│   └── preprocessing.py
├── sql/
│   ├── init-database.sql
│   └── init-tables.sql
├── docker-compose.yml
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## 🚀 **Quick Start (Docker)**

### **Prerequisites**

- Docker Desktop installed
- Docker Compose installed

1.  **Clone Repository**

```bash
git clone https://github.com/QwAct225/restoops-api.git
cd restoops-api
```

2. **Setup Environment Variables**

```bash
cp .env.example .env
```

Edit `.env` file jika diperlukan (default sudah siap digunakan):

```env
DB_NAME=restoops
DB_USER=postgres
DB_PASS=restoops123
DB_HOST=postgres
DB_PORT=5432
API_PORT=8001
```

3. **Jalankan Preprocessing (Generate Data)**

Sebelum menjalankan Docker, pastikan data sudah di-preprocessing terlebih dahulu:

```bash
# Setup virtual environment (optional untuk preprocessing)
python -m venv venv
source venv/bin/activate      # Mac/Linux
./venv/Scripts/Activate.ps1   # Windows (PowerShell)
venv\Scripts\activate.bat     # Windows (CMD)

# Install dependencies
pip install -r requirements.txt

# Jalankan scraper dan preprocessing
python scripts/run_scraper.py
python scripts/run_reservation_seeder.py
python scripts/run_preprocessing.py
```

Ini akan generate file:

- `data/processed/menu_data.csv`
- `data/processed/reservation_data.csv`

4. **Build & Run Docker Containers**

```bash
# Build dan jalankan semua services
docker-compose up --build -d
```

Services yang akan berjalan:

- **PostgreSQL**: `localhost:5432`
- **FastAPI**: `localhost:8001`

5. **Akses API Documentation**

Buka browser dan akses:

- **API Docs (Swagger)**: http://localhost:8001/docs
- **API Root**: http://localhost:8001
- **Health Check**: http://localhost:8001/health

## 🔧 **Troubleshooting**

### **Port Already in Use**

```bash
# Check what's using port 5432
netstat -ano | findstr :5432  # Windows
lsof -i :5432                 # Mac/Linux

# Change port in .env file
DB_PORT=5433
API_PORT=8001
```

### **Database Connection Error**

```bash
# Check PostgreSQL container health
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### **API Not Responding**

```bash
# Check API container logs
docker-compose logs api

# Restart API container
docker-compose restart api

# Rebuild API container
docker-compose up --build -d api
```

## 📝 **Notes**

- Data preprocessing harus dilakukan **sebelum** menjalankan Docker pertama kali
- Data **otomatis ter-load** ke PostgreSQL dari CSV saat container pertama kali dibuat
- Jika ingin update data setelah preprocessing ulang, ada 2 cara:
  1. **Restart container**: `docker-compose down -v && docker-compose up --build -d` (data otomatis reload)
  2. **Manual sync**: Gunakan endpoint `POST /sync/all` (tanpa restart)
- Database schema otomatis dibuat saat container pertama kali dijalankan
- Volume PostgreSQL akan persist data meskipun container dihapus (kecuali dengan `docker-compose down -v`)

## 👨‍💻 **Development Mode**

Untuk development, API sudah dikonfigurasi dengan `--reload` flag, sehingga perubahan code akan otomatis ter-reload:

```bash
# Edit files in api/ directory
# Changes will be automatically reloaded
docker-compose logs -f api
```

## 📄 **License**

MIT License - Feel free to use this project for learning and development purposes

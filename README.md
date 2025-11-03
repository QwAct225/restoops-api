# RestoOps - Backend API
adalah platform backend untuk manajemen operasional restoran end-to-end: mulai dari reservasi meja + pre-order, pencatatan & orkestrasi pesanan ke dapur, pembayaran, sinkronisasi stok/bahan, hingga pelaporan bisnis—dibangun modular sehingga mudah diskalakan dan diobservasi. Fondasi domainnya mengikuti enam service inti (Order, Reservation, Payment, Catalog, Warehouse, Reporting) yang saling terintegrasi untuk efisiensi operasional dan keputusan manajerial yang lebih cepat.

## 🚀 **Quick Start**

1. **Clone Repository**

   ```bash
   git clone https://github.com/QwAct225/restoops-api.git
   cd restoops-api
   ```

2. **Setup Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   ./venv/Scripts/Activate.ps1   # Windows
   ```
   
3. **Instalasi Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan Scraper:**

    ```bash
    python scripts/run_scraper.py
    ```

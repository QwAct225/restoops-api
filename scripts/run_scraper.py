import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import MenuScraper


def main():
    url = "https://esborder.qs.esb.co.id/APP/1209/order?mode=dinein&tableNumber=1&id=859"
    
    print("="*60)
    print("MENU SCRAPER")
    print("="*60)
    print(f"URL Target: {url}")
    print("="*60)
    
    try:
        scraper = MenuScraper(url)
        
        print("\nMemulai scraping...")
        print("Gunakan headless=False jika ada masalah dengan headless mode")
        menu_data = scraper.scrape_menu(headless=False) 
        
        if menu_data:
            print("\n" + "="*60)
            print("HASIL SCRAPING")
            print("="*60)
            
            df = scraper.get_dataframe()
            print(df.to_string(index=False))
            
            data_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
            os.makedirs(data_folder, exist_ok=True)
            
            raw_csv_path = os.path.join(data_folder, "raw_menu_data.csv")
            raw_json_path = os.path.join(data_folder, "raw_menu_data.json")
            scraper.save_to_csv(raw_csv_path)
            scraper.save_to_json(raw_json_path)
            
            print("\n" + "="*60)
            print("SCRAPING SELESAI!")
            print("="*60)
            
        else:
            print("\nTidak ada data yang berhasil di-scrape")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPastikan:")
        print("1. Chrome browser sudah terinstall")
        print("2. Koneksi internet aktif")
        print("3. URL dapat diakses")
        sys.exit(1)

if __name__ == "__main__":
    main()

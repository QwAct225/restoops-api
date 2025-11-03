import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import MenuPreprocessing, ReservationPreprocessing


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    raw_menu_path = os.path.join(base_dir, 'data', 'raw', 'raw_menu_data.csv')
    raw_reservation_path = os.path.join(base_dir, 'data', 'raw', 'raw_reservation_data.csv')
    
    processed_menu_csv = os.path.join(base_dir, 'data', 'processed', 'menu_data.csv')
    processed_menu_json = os.path.join(base_dir, 'data', 'processed', 'menu_data.json')
    processed_reservation_csv = os.path.join(base_dir, 'data', 'processed', 'reservation_data.csv')
    processed_reservation_json = os.path.join(base_dir, 'data', 'processed', 'reservation_data.json')
    
    print("\n" + "="*80)
    print(" "*25 + "DATA PREPROCESSING PIPELINE")
    print("="*80)
    
    try:
        print("\n🔧 Processing Menu Data...")
        menu_processor = MenuPreprocessing(raw_menu_path)
        menu_clean = menu_processor.preprocess()
        menu_processor.save_to_csv(processed_menu_csv)
        menu_processor.save_to_json(processed_menu_json)
        print(f"   ✓ Menu data cleaned: {len(menu_clean)} records")
        
        print("\n🔧 Processing Reservation Data...")
        reservation_processor = ReservationPreprocessing(raw_reservation_path)
        reservation_clean = reservation_processor.preprocess()
        reservation_processor.save_to_csv(processed_reservation_csv)
        reservation_processor.save_to_json(processed_reservation_json)
        print(f"   ✓ Reservation data cleaned: {len(reservation_clean)} records")
        
        print("\n" + "="*80)
        print("✓ PREPROCESSING COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\n📊 Summary:")
        print(f"   • Menu: {len(menu_clean)} records")
        print(f"   • Reservation: {len(reservation_clean)} records")
        print(f"\n📂 Output Location: data/processed/")
        print("="*80 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: File not found - {str(e)}")
        print("\n💡 Pastikan raw data files ada di folder data/raw/")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

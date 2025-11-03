import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.reservation_seeder import ReservationSeeder


def main():
    print("="*80)
    print("RESERVATION SEEDER")
    print("="*80)
    print("Generating sample reservation data...")
    print("="*80)
    
    try:
        seeder = ReservationSeeder()
        print("\n1. Generating sample data...")
        seeder.seed_sample_data()
        seeder.display_data()
        
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
        os.makedirs(data_folder, exist_ok=True)
        
        csv_path = os.path.join(data_folder, "raw_reservation_data.csv")
        json_path = os.path.join(data_folder, "raw_reservation_data.json")
        
        print("\n2. Saving to CSV...")
        seeder.save_to_csv(csv_path)
        
        print("\n3. Saving to JSON...")
        seeder.save_to_json(json_path)
        
        print("\n" + "="*80)
        print("✓ SEEDING COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\nOutput files:")
        print(f"  - CSV:  {csv_path}")
        print(f"  - JSON: {json_path}")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

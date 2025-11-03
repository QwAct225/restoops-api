import random
import string
import pandas as pd
import json
from datetime import datetime


class ReservationSeeder:
    def __init__(self):
        self.reservations = []
        
    def generate_token(self, length=10):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def format_ordered_menu(self, menu_items):
        formatted_items = []
        
        for item in menu_items:
            menu_id = item['menu_id']
            variant = item.get('variant', None)
            
            if variant:
                formatted_items.append(f"{menu_id}[{variant}]")
            else:
                formatted_items.append(f"[{menu_id}]")
        
        return "[" + ", ".join(formatted_items) + "]"
    
    def add_reservation(self, name, table_number, menu_items, duration_hours):
        reservation_id = len(self.reservations) + 1
        token = self.generate_token()
        ordered_menu = self.format_ordered_menu(menu_items)
        
        reservation = {
            'id': reservation_id,
            'name': name,
            'reservation_table': table_number,
            'token': token,
            'ordered_menu': ordered_menu,
            'duration': duration_hours
        }
        
        self.reservations.append(reservation)
        
        return reservation
    
    def seed_sample_data(self):
        self.add_reservation(
            name='John Doe',
            table_number=11,
            menu_items=[
                {'menu_id': 3, 'variant': 'LEVEL 2'},
                {'menu_id': 16}
            ],
            duration_hours=5
        )
        
        self.add_reservation(
            name='Bob Hob',
            table_number=7,
            menu_items=[
                {'menu_id': 4, 'variant': 'LEVEL 4'},
                {'menu_id': 8}  
            ],
            duration_hours=4
        )
        
        self.add_reservation(
            name='Alice Smith',
            table_number=3,
            menu_items=[
                {'menu_id': 1, 'variant': 'CHOCOLATE'},
                {'menu_id': 16, 'variant': 'HOT'},
                {'menu_id': 6}
            ],
            duration_hours=3
        )
        
        self.add_reservation(
            name='Michael Chen',
            table_number=15,
            menu_items=[
                {'menu_id': 3, 'variant': 'LEVEL 0'},
                {'menu_id': 11},
                {'menu_id': 19, 'variant': 'ICED'}
            ],
            duration_hours=6
        )
        
        self.add_reservation(
            name='Sarah Johnson',
            table_number=8,
            menu_items=[
                {'menu_id': 4, 'variant': 'LEVEL 6 (+Rp 910)'},
                {'menu_id': 7},
                {'menu_id': 22, 'variant': 'ICED'}
            ],
            duration_hours=4
        )
        
        print(f"✓ Generated {len(self.reservations)} sample reservations")
    
    def save_to_csv(self, output_path):
        if not self.reservations:
            print("Tidak ada data untuk disimpan")
            return
        
        df = pd.DataFrame(self.reservations)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"✓ Data CSV disimpan ke: {output_path}")
        print(f"  Total reservations: {len(self.reservations)}")
    
    def save_to_json(self, output_path):
        if not self.reservations:
            print("Tidak ada data untuk disimpan")
            return
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.reservations, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Data JSON disimpan ke: {output_path}")
        print(f"  Total reservations: {len(self.reservations)}")
    
    def get_dataframe(self):
        return pd.DataFrame(self.reservations)
    
    def display_data(self):
        if not self.reservations:
            print("Tidak ada data reservation")
            return
        
        df = self.get_dataframe()
        print("\n" + "="*80)
        print("RESERVATION DATA")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)

import pandas as pd
import numpy as np
import json
import os
class MenuPreprocessing:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
        self.df_clean = None
        
    def load_data(self):
        self.df = pd.read_csv(self.input_path)
        return self.df
    
    def clean_id(self):
        if 'id' in self.df.columns:
            self.df['id'] = pd.to_numeric(self.df['id'], errors='coerce').astype('Int64')
        return self.df
    
    def clean_harga(self):
        if 'harga' in self.df.columns:
            self.df['harga'] = pd.to_numeric(self.df['harga'], errors='coerce').astype('Int64')
        return self.df
    
    def clean_variants(self):
        if 'variants' in self.df.columns:
            def process_variant(value):
                if pd.isna(value):
                    return None
                
                if isinstance(value, str):
                    if value.strip() in ['[]', '[ ]', '']:
                        return None
                    
                    try:
                        value_json = value.replace("'", '"')
                        parsed = json.loads(value_json)
                        
                        if not parsed or len(parsed) == 0:
                            return None
                        
                        return json.dumps(parsed)
                    except:
                        return value if value.strip() != '[]' else None
                
                if isinstance(value, list):
                    if len(value) == 0:
                        return None
                    return json.dumps(value)
                
                return value
            
            self.df['variants'] = self.df['variants'].apply(process_variant)
        
        return self.df
    
    def clean_sold_out(self):
        if 'sold_out' in self.df.columns:
            self.df['sold_out'] = self.df['sold_out'].str.strip().str.title()
        return self.df
    
    def preprocess(self):
        self.load_data()
        self.clean_id()
        self.clean_harga()
        self.clean_variants()
        self.clean_sold_out()
        self.df_clean = self.df.copy()
        
        return self.df_clean
    
    def get_cleaned_data(self):
        return self.df_clean if self.df_clean is not None else self.df
    
    def save_to_csv(self, output_path):
        df_to_save = self.get_cleaned_data()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_to_save.to_csv(output_path, index=False)
        
    def save_to_json(self, output_path):
        df_to_save = self.get_cleaned_data()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        records = df_to_save.to_dict('records')
        for record in records:
            if 'variants' in record and record['variants'] is not None:
                if isinstance(record['variants'], str):
                    try:
                        record['variants'] = json.loads(record['variants'])
                    except:
                        pass
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def display_summary(self):
        df = self.get_cleaned_data()
        
        print("\n" + "="*60)
        print("CLEANED DATA SUMMARY")
        print("="*60)
        print(f"\nShape: {df.shape}")
        print(f"\nData types:")
        print(df.dtypes)
        print(f"\nNull values:")
        print(df.isnull().sum())
        print(f"\nFirst 5 rows:")
        print(df.head().to_string(index=False))
        print("="*60)

class ReservationPreprocessing:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
        self.df_clean = None
        
    def load_data(self):
        self.df = pd.read_csv(self.input_path)
        return self.df
    
    def clean_id(self):
        if 'id' in self.df.columns:
            self.df['id'] = pd.to_numeric(self.df['id'], errors='coerce').astype('Int64')
        return self.df
    
    def clean_reservation_table(self):
        if 'reservation_table' in self.df.columns:
            self.df['reservation_table'] = pd.to_numeric(
                self.df['reservation_table'], 
                errors='coerce'
            ).astype('Int64')
        return self.df
    
    def clean_duration(self):
        if 'duration' in self.df.columns:
            self.df['duration'] = pd.to_numeric(
                self.df['duration'], 
                errors='coerce'
            ).astype('Int64')
        return self.df
    
    def clean_name(self):
        if 'name' in self.df.columns:
            self.df['name'] = self.df['name'].str.strip()
        return self.df
    
    def clean_token(self):
        if 'token' in self.df.columns:
            self.df['token'] = self.df['token'].str.strip().str.upper()
        return self.df
    
    def clean_ordered_menu(self):
        if 'ordered_menu' in self.df.columns:
            self.df['ordered_menu'] = self.df['ordered_menu'].str.strip()
        return self.df
    
    def preprocess(self):
        self.load_data()
        self.clean_id()
        self.clean_reservation_table()
        self.clean_duration()
        self.clean_name()
        self.clean_token()
        self.clean_ordered_menu()
        self.df_clean = self.df.copy()
        
        return self.df_clean
    
    def get_cleaned_data(self):
        return self.df_clean if self.df_clean is not None else self.df
    
    def save_to_csv(self, output_path):
        df_to_save = self.get_cleaned_data()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_to_save.to_csv(output_path, index=False)
        
    def save_to_json(self, output_path):
        df_to_save = self.get_cleaned_data()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        records = df_to_save.to_dict('records')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def display_summary(self):
        df = self.get_cleaned_data()
        
        print("\n" + "="*60)
        print("CLEANED DATA SUMMARY")
        print("="*60)
        print(f"\nShape: {df.shape}")
        print(f"\nData types:")
        print(df.dtypes)
        print(f"\nNull values:")
        print(df.isnull().sum())
        print(f"\nFirst 5 rows:")
        print(df.head().to_string(index=False))
        print("="*60)

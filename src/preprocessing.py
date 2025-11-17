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
        """Remove quotes from ID and convert to numeric"""
        if 'id' in self.df.columns:
            # Remove quotes if present
            self.df['id'] = self.df['id'].astype(str).str.strip().str.replace('"', '', regex=False).str.replace("'", '', regex=False)
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
    
    def clean_image_url(self):
        if 'image_url' in self.df.columns:
            def process_url(value):
                if pd.isna(value) or value == 'N/A' or value == '':
                    return None
                return value.strip()
            
            self.df['image_url'] = self.df['image_url'].apply(process_url)
        return self.df
    
    def preprocess(self):
        self.load_data()
        self.clean_id()
        self.clean_harga()
        self.clean_variants()
        self.clean_sold_out()
        self.clean_image_url()
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
        """Remove quotes from ID and convert to numeric"""
        if 'id' in self.df.columns:
            # Remove quotes if present
            self.df['id'] = self.df['id'].astype(str).str.strip().str.replace('"', '', regex=False).str.replace("'", '', regex=False)
            self.df['id'] = pd.to_numeric(self.df['id'], errors='coerce').astype('Int64')
        return self.df
    
    def clean_reservation_table(self):
        """Remove quotes from reservation_table and convert to numeric"""
        if 'reservation_table' in self.df.columns:
            # Remove quotes if present
            self.df['reservation_table'] = self.df['reservation_table'].astype(str).str.strip().str.replace('"', '', regex=False).str.replace("'", '', regex=False)
            self.df['reservation_table'] = pd.to_numeric(
                self.df['reservation_table'], 
                errors='coerce'
            ).astype('Int64')
        return self.df
    
    def clean_duration(self):
        """Remove quotes from duration and convert to numeric"""
        if 'duration' in self.df.columns:
            # Remove quotes if present
            self.df['duration'] = self.df['duration'].astype(str).str.strip().str.replace('"', '', regex=False).str.replace("'", '', regex=False)
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
        """Convert ordered_menu to JSON format keeping menu_id[variant] structure"""
        if 'ordered_menu' in self.df.columns:
            def process_ordered_menu(value):
                if pd.isna(value):
                    return None
                
                if isinstance(value, str):
                    value = value.strip()
                    
                    if not value or value == '[]':
                        return None
                    
                    # Remove outer quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    # Try to parse format like "[3[LEVEL 2], [16]]"
                    try:
                        import re
                        
                        # Extract all items within the outer brackets
                        if value.startswith('[') and value.endswith(']'):
                            inner = value[1:-1]  # Remove outer brackets
                            
                            # Split by comma but be careful with nested brackets
                            items = []
                            current_item = ''
                            bracket_depth = 0
                            
                            for char in inner:
                                if char == '[':
                                    bracket_depth += 1
                                    current_item += char
                                elif char == ']':
                                    bracket_depth -= 1
                                    current_item += char
                                elif char == ',' and bracket_depth == 0:
                                    if current_item.strip():
                                        items.append(current_item.strip())
                                    current_item = ''
                                else:
                                    current_item += char
                            
                            # Don't forget the last item
                            if current_item.strip():
                                items.append(current_item.strip())
                            
                            # Now clean each item - KEEP the full format menu_id[variant]
                            cleaned_items = []
                            for item in items:
                                # Remove outer brackets if they wrap the entire item
                                item = item.strip()
                                if item.startswith('[') and item.endswith(']'):
                                    # This is like "[16]" - extract just the content
                                    item = item[1:-1]
                                
                                # Keep as-is: "3[LEVEL 2]" stays "3[LEVEL 2]"
                                # Just a number like "16" stays "16"
                                if item.strip():
                                    cleaned_items.append(item.strip())
                            
                            return json.dumps(cleaned_items) if cleaned_items else None
                    except Exception as e:
                        # If parsing fails, try simple approach
                        if value:
                            return json.dumps([value])
                        return None
                    
                    return None
                
                if isinstance(value, list):
                    return json.dumps(value) if value else None
                
                return value
            
            self.df['ordered_menu'] = self.df['ordered_menu'].apply(process_ordered_menu)
        
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
        
        # Parse ordered_menu JSON strings back to objects
        for record in records:
            if 'ordered_menu' in record and record['ordered_menu'] is not None:
                if isinstance(record['ordered_menu'], str):
                    try:
                        record['ordered_menu'] = json.loads(record['ordered_menu'])
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

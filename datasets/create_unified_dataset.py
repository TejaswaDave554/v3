"""
Unified Dataset Creator - Merge Excel and CSV files into one clean dataset
Run this to create consolidated datasets from all sources
"""

import pandas as pd
import os
from typing import Dict, List
import openpyxl

class UnifiedDatasetCreator:
    """Create unified datasets from Excel and CSV files"""
    
    def __init__(self, datasets_dir: str = r"D:\Tejaswa_Dave_Projects\v3\v3\app\datasets\unified"):
        self.datasets_dir = datasets_dir
        self.unified_data = {}
        self.excel_files = {
            'household': 'D03-Households_35.xls',
            'digital': 'D45-DigitalAvailability_20.xls',
            'city_profile': 'D01-CityProfile_25.xls'
        }
        self.csv_files = {
            'water_sanitation': 'D11-waterAndsanitation_1_1_1.csv',
            'environment': 'D04-Environment_6_2_2.csv',
            'crimes': 'D47-Crimes_13_1.csv',
            'intersections': 'D35-Intersections_6_1.csv',
            'employment': 'D02-UnemploymentRate_17_0.csv'
        }
    
    def load_excel_file(self, file_key: str, filename: str) -> pd.DataFrame:
        """Load an Excel file"""
        filepath = os.path.join(self.datasets_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  Excel file not found: {filepath}")
            return None
        
        try:
            # Try reading with openpyxl first (for .xls files)
            df = pd.read_excel(filepath, engine='openpyxl')
            print(f"✅ Loaded Excel: {filename} ({len(df)} rows, {len(df.columns)} cols)")
            return df
        except Exception as e1:
            try:
                # Fallback to default engine
                df = pd.read_excel(filepath)
                print(f"✅ Loaded Excel: {filename} ({len(df)} rows, {len(df.columns)} cols)")
                return df
            except Exception as e2:
                print(f"❌ Error loading Excel {filename}: {str(e2)}")
                return None
    
    def load_csv_file(self, file_key: str, filename: str) -> pd.DataFrame:
        """Load a CSV file"""
        filepath = os.path.join(self.datasets_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  CSV file not found: {filepath}")
            return None
        
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Loaded CSV: {filename} ({len(df)} rows, {len(df.columns)} cols)")
            return df
        except Exception as e:
            print(f"❌ Error loading CSV {filename}: {str(e)}")
            return None
    
    def load_all_files(self):
        """Load all Excel and CSV files"""
        print("\n" + "=" * 80)
        print("📊 LOADING ALL FILES (Excel + CSV)")
        print("=" * 80)
        
        # Load Excel files
        print("\n📑 Excel Files:")
        print("─" * 80)
        for key, filename in self.excel_files.items():
            df = self.load_excel_file(key, filename)
            if df is not None:
                self.unified_data[key] = df
        
        # Load CSV files
        print("\n📄 CSV Files:")
        print("─" * 80)
        for key, filename in self.csv_files.items():
            df = self.load_csv_file(key, filename)
            if df is not None:
                self.unified_data[key] = df
        
        print("\n" + "=" * 80)
        print(f"✅ Total datasets loaded: {len(self.unified_data)}")
        print("=" * 80)
    
    def inspect_all_datasets(self):
        """Show details of all loaded datasets"""
        print("\n" + "=" * 80)
        print("📊 DATASET INSPECTION - All Files")
        print("=" * 80)
        
        for dataset_name, df in self.unified_data.items():
            print(f"\n{'─' * 80}")
            print(f"📋 {dataset_name.upper()}")
            print(f"{'─' * 80}")
            print(f"Rows: {len(df)} | Columns: {len(df.columns)}")
            
            print(f"\nColumn Names:")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i:2d}. '{col}'")
            
            print(f"\nData Types:")
            for col, dtype in df.dtypes.items():
                print(f"  '{col}': {dtype}")
            
            print(f"\nFirst 3 rows:")
            print(df.head(3).to_string())
        
        print("\n" + "=" * 80)
    
    def save_unified_datasets(self, output_dir: str = None):
        """Save unified datasets to CSV for dashboard"""
        if output_dir is None:
            output_dir = self.datasets_dir
        
        print("\n" + "=" * 80)
        print("💾 SAVING UNIFIED DATASETS")
        print("=" * 80)
        
        unified_dir = os.path.join(output_dir, 'unified')
        os.makedirs(unified_dir, exist_ok=True)
        
        for dataset_name, df in self.unified_data.items():
            filename = f"unified_{dataset_name}.csv"
            filepath = os.path.join(unified_dir, filename)
            
            try:
                df.to_csv(filepath, index=False)
                print(f"✅ Saved: {filename}")
            except Exception as e:
                print(f"❌ Error saving {filename}: {str(e)}")
        
        print(f"\n✅ All unified datasets saved to: {unified_dir}")
        print("=" * 80)
        
        return unified_dir
    
    def generate_column_mapping(self):
        """Generate a mapping of all column names for reference"""
        print("\n" + "=" * 80)
        print("📋 COLUMN MAPPING - For Dashboard Code Updates")
        print("=" * 80)
        
        mapping = {}
        
        for dataset_name, df in self.unified_data.items():
            mapping[dataset_name] = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict()
            }
            
            print(f"\n### {dataset_name.upper()}")
            print(f"Rows: {len(df)} | Columns: {len(df.columns)}")
            for i, col in enumerate(df.columns, 1):
                dtype = df[col].dtype
                print(f"  {i:2d}. '{col}' ({dtype})")
        
        print("\n" + "=" * 80)
        return mapping


def main():
    """Main execution"""
    
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " UNIFIED DATASET CREATOR - Merge Excel + CSV Files ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Create unified dataset creator
    creator = UnifiedDatasetCreator()
    
    # Load all files
    creator.load_all_files()
    
    # Inspect all datasets
    creator.inspect_all_datasets()
    
    # Save unified datasets
    unified_dir = creator.save_unified_datasets()
    
    # Generate column mapping
    mapping = creator.generate_column_mapping()
    
    # Create a reference document
    create_reference_document(mapping, unified_dir)
    
    print("\n" + "=" * 80)
    print("🎉 UNIFIED DATASET CREATION COMPLETE!")
    print("=" * 80)
    print(f"\n✅ Unified datasets saved to: {unified_dir}")
    print("✅ Column mapping document created: column_mapping.txt")
    print("\n📝 Next steps:")
    print("  1. Update app/pages.py with column names from above")
    print("  2. Run: streamlit run main.py")
    print("  3. Visualizations will show with all data sources combined!")
    print("=" * 80)


def create_reference_document(mapping: Dict, output_dir: str):
    """Create a reference document with all column mappings"""
    
    filepath = os.path.join(output_dir, 'column_mapping.txt')
    
    with open(filepath, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("COLUMN MAPPING REFERENCE - For Dashboard Updates\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("Use these exact column names in app/pages.py\n\n")
        
        for dataset_name, info in mapping.items():
            f.write(f"\n### {dataset_name.upper()}\n")
            f.write(f"Total Rows: {info['total_rows']}\n")
            f.write(f"Total Columns: {info['total_columns']}\n")
            f.write(f"\nColumns:\n")
            for i, col in enumerate(info['columns'], 1):
                dtype = info['dtypes'].get(col, 'unknown')
                f.write(f"  {i:2d}. '{col}' ({dtype})\n")
            f.write("\n" + "-" * 80 + "\n")
    
    print(f"✅ Reference document created: {filepath}")


if __name__ == "__main__":
    main()

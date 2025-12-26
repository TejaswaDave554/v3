import os
import pandas as pd
import numpy as np
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    def __init__(self, datasets_dir: str = r"D:\Tejaswa_Dave_Projects\v3\datasets\unified"):
        self.datasets_dir = datasets_dir
        self.data = {}
        
    def load_all(self) -> Dict[str, pd.DataFrame]:
        files = {
            'water_sanitation': 'unified_water_sanitation.csv',
            'environment': 'unified_environment.csv',
            'crimes': 'unified_crimes.csv',
            'intersections': 'unified_intersections.csv',
            'employment': 'unified_employment.csv'
        }
        
        for key, filename in files.items():
            path = os.path.join(self.datasets_dir, filename)
            try:
                if os.path.exists(path):
                    self.data[key] = pd.read_csv(path)
                else:
                    self.data[key] = None
            except:
                self.data[key] = None
        
        return self.data


class DataProcessor:
    @staticmethod
    def clean_numeric(value):
        if isinstance(value, str) and value.upper() in ['NA', 'NAN']:
            return np.nan
        try:
            return float(value)
        except:
            return np.nan
    
    @staticmethod
    def get_zone_summary(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        if df is None or df.empty:
            return None
        try:
            result = df.groupby('Zone Name')[value_col].sum().reset_index()
            result.columns = ['Zone Name', 'Value']
            return result.sort_values('Value', ascending=False)
        except:
            return None
    
    @staticmethod
    def get_ward_summary(df: pd.DataFrame, value_col: str, top_n: int = 15) -> pd.DataFrame:
        if df is None or df.empty:
            return None
        try:
            result = df.groupby('Ward Name')[value_col].sum().reset_index()
            result.columns = ['Ward Name', 'Value']
            return result.sort_values('Value', ascending=False).head(top_n)
        except:
            return None
    
    @staticmethod
    def calculate_coverage(numerator: float, denominator: float) -> float:
        if denominator == 0 or pd.isna(denominator):
            return 0
        return round((numerator / denominator) * 100, 2)


class DashboardApp:
    def __init__(self):
        self.loader = DataLoader()
        self.processor = DataProcessor()
        self.data = self.loader.load_all()
        
    def get_water_sanitation_stats(self) -> Dict:
        ws = self.data['water_sanitation']
        if ws is None or ws.empty:
            return {}
        
        stats = {
            'total_households': int(ws['Total number of households (HH)'].sum()),
            'sewerage_coverage': int(ws['HH part of the city sewerage network'].sum()),
            'toilet_coverage': int(ws['Number of Households with toilets'].sum()),
            'public_toilets': int(ws['Number of Public Toilet '].sum()),
            'free_toilets_female': int(ws['Number of free public toilets - Female'].sum()),
            'free_toilets_male': int(ws['Number of free public toilets - Male'].sum()),
            'paid_toilets_female': int(ws['Number of paid public toilets - Female'].sum()),
            'paid_toilets_male': int(ws['Number of paid public toilets - Male'].sum()),
        }
        
        stats['sewerage_pct'] = self.processor.calculate_coverage(
            stats['sewerage_coverage'], stats['total_households']
        )
        stats['toilet_pct'] = self.processor.calculate_coverage(
            stats['toilet_coverage'], stats['total_households']
        )
        
        return stats
    
    def get_environment_stats(self) -> Dict:
        env = self.data['environment']
        if env is None or env.empty:
            return {}
        
        env['PM2.5'] = env['Monthly mean/average concentration - PM2.5'].apply(self.processor.clean_numeric)
        env['PM10'] = env['Monthly mean concentration - PM10'].apply(self.processor.clean_numeric)
        env['NO2'] = env['Monthly mean concentration - NO2'].apply(self.processor.clean_numeric)
        env['SO2'] = env['Monthly mean concentration - SO2'].apply(self.processor.clean_numeric)
        env['O3'] = env['Monthly mean concentration - O3'].apply(self.processor.clean_numeric)
        
        return {
            'pm25_avg': round(env['PM2.5'].mean(), 2),
            'pm10_avg': round(env['PM10'].mean(), 2),
            'no2_avg': round(env['NO2'].mean(), 2),
            'so2_avg': round(env['SO2'].mean(), 2),
            'o3_avg': round(env['O3'].mean(), 2),
        }
    
    def get_crimes_trend(self) -> pd.DataFrame:
        crimes = self.data['crimes']
        if crimes is None or crimes.empty:
            return None
        
        result = crimes[['Year', 'Total number of crimes recorded']].copy()
        return result.sort_values('Year')
    
    def get_intersections_summary(self) -> Dict:
        intr = self.data['intersections']
        if intr is None or intr.empty:
            return {}
        
        return {
            'total_intersections': int(intr['No. of intersections / junctions'].sum()),
            'signalized_intersections': int(intr['Total number of operational signalized intersections'].sum()),
            'by_zone': self.processor.get_zone_summary(intr, 'No. of intersections / junctions'),
            'signalized_by_zone': self.processor.get_zone_summary(intr, 'Total number of operational signalized intersections'),
        }
    
    def get_employment_stats(self) -> Dict:
        emp = self.data['employment']
        if emp is None or emp.empty:
            return {}
        
        row = emp.iloc[0]
        unemployed = row['No. of unemployed persons (seeking or available for work)']
        employed = row['No. of employed persons']
        labour_force = row['Total labour force in the city (age 15-59) [Employed + Unemployed Persons)']
        
        return {
            'unemployed': int(unemployed),
            'employed': int(employed),
            'labour_force': int(labour_force),
            'unemployment_rate': round((unemployed / labour_force) * 100, 2),
            'employment_rate': round((employed / labour_force) * 100, 2),
        }
    
    def get_water_by_zone(self) -> pd.DataFrame:
        ws = self.data['water_sanitation']
        if ws is None or ws.empty:
            return None
        return self.processor.get_zone_summary(ws, 'Total number of households (HH)')
    
    def get_water_by_ward(self) -> pd.DataFrame:
        ws = self.data['water_sanitation']
        if ws is None or ws.empty:
            return None
        return self.processor.get_ward_summary(ws, 'Number of Public Toilet ', top_n=15)
    
    def get_environment_trend(self) -> pd.DataFrame:
        env = self.data['environment']
        if env is None or env.empty:
            return None
        
        env_copy = env.copy()
        env_copy['PM2.5'] = env_copy['Monthly mean/average concentration - PM2.5'].apply(self.processor.clean_numeric)
        env_copy['PM10'] = env_copy['Monthly mean concentration - PM10'].apply(self.processor.clean_numeric)
        
        return env_copy[['Month -Year', 'PM2.5', 'PM10']].tail(12)
    
    def get_intersections_by_zone(self) -> pd.DataFrame:
        intr = self.data['intersections']
        if intr is None or intr.empty:
            return None
        return self.processor.get_zone_summary(intr, 'No. of intersections / junctions')


import os
import pandas as pd
import numpy as np
from typing import Dict

class DataHandler:
    def __init__(self, data_path: str = "datasets/unified"):
        self.data_path = data_path
        self.datasets = {}
        self.load_data()
    
    def load_data(self):
        """Load all CSV files from the data directory"""
        files = {
            'water': 'unified_water_sanitation.csv',
            'environment': 'unified_environment.csv',
            'crimes': 'unified_crimes.csv',
            'infrastructure': 'unified_intersections.csv',
            'employment': 'unified_employment.csv'
        }
        
        for key, filename in files.items():
            filepath = os.path.join(self.data_path, filename)
            try:
                if os.path.exists(filepath):
                    self.datasets[key] = pd.read_csv(filepath)
                else:
                    self.datasets[key] = None
            except Exception:
                self.datasets[key] = None
    
    def get_water_stats(self) -> Dict:
        """Get water and sanitation statistics"""
        df = self.datasets['water']
        if df is None or df.empty:
            return {}
        
        total_households = int(df['Total number of households (HH)'].sum())
        sewerage = int(df['HH part of the city sewerage network'].sum())
        toilets = int(df['Number of Households with toilets'].sum())
        public_toilets = int(df['Number of Public Toilet '].sum())
        
        return {
            'total_households': total_households,
            'sewerage_coverage': sewerage,
            'toilet_coverage': toilets,
            'public_toilets': public_toilets,
            'sewerage_pct': round((sewerage / total_households) * 100, 1) if total_households > 0 else 0,
            'toilet_pct': round((toilets / total_households) * 100, 1) if total_households > 0 else 0
        }
    
    def get_environment_stats(self) -> Dict:
        """Get air quality statistics"""
        df = self.datasets['environment']
        if df is None or df.empty:
            return {}
        
        def clean_numeric(val):
            try:
                return float(val) if pd.notna(val) else np.nan
            except:
                return np.nan
        
        pm25 = df['Monthly mean/average concentration - PM2.5'].apply(clean_numeric).mean()
        pm10 = df['Monthly mean concentration - PM10'].apply(clean_numeric).mean()
        no2 = df['Monthly mean concentration - NO2'].apply(clean_numeric).mean()
        
        return {
            'pm25_avg': round(pm25, 1) if not np.isnan(pm25) else 0,
            'pm10_avg': round(pm10, 1) if not np.isnan(pm10) else 0,
            'no2_avg': round(no2, 2) if not np.isnan(no2) else 0
        }
    
    def get_crime_data(self) -> pd.DataFrame:
        """Get crime trend data"""
        df = self.datasets['crimes']
        if df is None or df.empty:
            return None
        return df[['Year', 'Total number of crimes recorded']].sort_values('Year')
    
    def get_infrastructure_stats(self) -> Dict:
        """Get infrastructure statistics"""
        df = self.datasets['infrastructure']
        if df is None or df.empty:
            return {}
        
        total = int(df['No. of intersections / junctions'].sum())
        signalized = int(df['Total number of operational signalized intersections'].sum())
        
        return {
            'total_intersections': total,
            'signalized_intersections': signalized,
            'signalization_pct': round((signalized / total) * 100, 1) if total > 0 else 0
        }
    
    def get_employment_stats(self) -> Dict:
        """Get employment statistics"""
        df = self.datasets['employment']
        if df is None or df.empty:
            return {}
        
        row = df.iloc[0]
        unemployed = int(row['No. of unemployed persons (seeking or available for work)'])
        employed = int(row['No. of employed persons'])
        labour_force = int(row['Total labour force in the city (age 15-59) [Employed + Unemployed Persons)'])
        
        return {
            'labour_force': labour_force,
            'employed': employed,
            'unemployed': unemployed,
            'unemployment_rate': round((unemployed / labour_force) * 100, 2) if labour_force > 0 else 0
        }
    
    def get_zone_data(self, dataset: str, value_col: str) -> pd.DataFrame:
        """Get data grouped by zone"""
        df = self.datasets[dataset]
        if df is None or df.empty or 'Zone Name' not in df.columns:
            return None
        
        try:
            result = df.groupby('Zone Name')[value_col].sum().reset_index()
            result.columns = ['Zone', 'Value']
            return result.sort_values('Value', ascending=False)
        except:
            return None
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class WaterPage:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("💧 Water & Sanitation")
        
        stats = self.data.get_water_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Households", f"{stats['total_households']:,}")
        col2.metric("Sewerage Coverage", f"{stats['sewerage_pct']:.1f}%")
        col3.metric("Toilet Coverage", f"{stats['toilet_pct']:.1f}%")
        col4.metric("Public Toilets", f"{stats['public_toilets']:,}")
        
        st.divider()
        
        # Zone-wise data
        zone_data = self.data.get_zone_data('water', 'Total number of households (HH)')
        if zone_data is not None:
            st.subheader("Households by Zone")
            fig = px.bar(zone_data, x='Zone', y='Value', title="Total Households by Zone")
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

class EnvironmentPage:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("🌍 Environment")
        
        stats = self.data.get_environment_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3 = st.columns(3)
        col1.metric("PM2.5 Average", f"{stats['pm25_avg']:.1f} µg/m³")
        col2.metric("PM10 Average", f"{stats['pm10_avg']:.1f} µg/m³")
        col3.metric("NO2 Average", f"{stats['no2_avg']:.2f} µg/m³")
        
        st.divider()
        
        # Air quality comparison
        st.subheader("Air Quality vs WHO Guidelines")
        comparison_data = pd.DataFrame({
            'Pollutant': ['PM2.5', 'PM10'],
            'Current': [stats['pm25_avg'], stats['pm10_avg']],
            'WHO Guideline': [15, 35]
        })
        
        fig = px.bar(comparison_data, x='Pollutant', y=['Current', 'WHO Guideline'],
                     title="Current Levels vs WHO Guidelines", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

class CrimePage:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("🚔 Crime Statistics")
        
        crime_data = self.data.get_crime_data()
        if crime_data is None or crime_data.empty:
            st.error("No crime data available")
            return
        
        latest = crime_data.iloc[-1]
        avg_crimes = crime_data['Total number of crimes recorded'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Year", int(latest['Year']))
        col2.metric("Recent Crimes", f"{int(latest['Total number of crimes recorded']):,}")
        col3.metric("Average", f"{int(avg_crimes):,}")
        
        st.divider()
        
        st.subheader("Crime Trend")
        fig = px.line(crime_data, x='Year', y='Total number of crimes recorded',
                      title="Crime Trend Over Years", markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

class InfrastructurePage:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("🛣️ Infrastructure")
        
        stats = self.data.get_infrastructure_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Intersections", f"{stats['total_intersections']:,}")
        col2.metric("Signalized", f"{stats['signalized_intersections']:,}")
        col3.metric("Signalization Rate", f"{stats['signalization_pct']:.1f}%")
        
        st.divider()
        
        # Zone-wise intersections
        zone_data = self.data.get_zone_data('infrastructure', 'No. of intersections / junctions')
        if zone_data is not None:
            st.subheader("Intersections by Zone")
            fig = px.bar(zone_data, x='Zone', y='Value', title="Intersections by Zone")
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

class EmploymentPage:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("💼 Employment")
        
        stats = self.data.get_employment_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Labour Force", f"{stats['labour_force']:,}")
        col2.metric("Employed", f"{stats['employed']:,}")
        col3.metric("Unemployed", f"{stats['unemployed']:,}")
        col4.metric("Unemployment Rate", f"{stats['unemployment_rate']:.1f}%")
        
        st.divider()
        
        # Employment distribution
        st.subheader("Employment Distribution")
        emp_data = pd.DataFrame({
            'Status': ['Employed', 'Unemployed'],
            'Count': [stats['employed'], stats['unemployed']]
        })
        
        fig = px.pie(emp_data, values='Count', names='Status',
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)

class DataExplorer:
    def __init__(self, data_handler):
        self.data = data_handler
    
    def render(self):
        st.header("📊 Data Explorer")
        
        dataset_names = {
            'water': 'Water & Sanitation',
            'environment': 'Environment',
            'crimes': 'Crime Data',
            'infrastructure': 'Infrastructure',
            'employment': 'Employment'
        }
        
        selected = st.selectbox("Select Dataset", list(dataset_names.values()))
        
        # Find the key for selected dataset
        dataset_key = None
        for key, name in dataset_names.items():
            if name == selected:
                dataset_key = key
                break
        
        if dataset_key and self.data.datasets[dataset_key] is not None:
            df = self.data.datasets[dataset_key]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric("Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            st.divider()
            
            st.subheader("Data Preview")
            st.dataframe(df.head(100), use_container_width=True)
            
            st.subheader("Column Info")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Non-Null': df.count().values
            })
            st.dataframe(col_info, use_container_width=True)
        else:
            st.error("Dataset not available")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from abc import ABC, abstractmethod


class BasePage(ABC):
    def __init__(self, app):
        self.app = app
        self.data = app.data
    
    @abstractmethod
    def render(self):
        pass


class WaterSanitationPage(BasePage):
    def render(self):
        st.header("💧 Water & Sanitation")
        
        stats = self.app.get_water_sanitation_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Households", f"{stats['total_households']:,}")
        with col2:
            st.metric("Sewerage Coverage", f"{stats['sewerage_pct']:.1f}%")
        with col3:
            st.metric("Toilet Coverage", f"{stats['toilet_pct']:.1f}%")
        with col4:
            st.metric("Public Toilets", f"{stats['public_toilets']:,}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Households by Zone")
            by_zone = self.app.get_water_by_zone()
            if by_zone is not None:
                fig = px.bar(by_zone, x='Zone Name', y='Value', title='Total Households by Zone')
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Public Toilets (Top 15 Wards)")
            by_ward = self.app.get_water_by_ward()
            if by_ward is not None:
                by_ward_sorted = by_ward.sort_values('Value')
                fig = px.bar(by_ward_sorted, x='Value', y='Ward Name',
                            title='Public Toilets by Ward', orientation='h')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Detailed Statistics")
        stats_table = pd.DataFrame({
            'Metric': [
                'Total Households', 'Sewerage Network Connected', 'Households with Toilets',
                'Free Public Toilets (Female)', 'Free Public Toilets (Male)',
                'Paid Public Toilets (Female)', 'Paid Public Toilets (Male)', 'Total Public Toilets'
            ],
            'Count': [
                f"{stats['total_households']:,}", f"{stats['sewerage_coverage']:,}",
                f"{stats['toilet_coverage']:,}", f"{stats['free_toilets_female']:,}",
                f"{stats['free_toilets_male']:,}", f"{stats['paid_toilets_female']:,}",
                f"{stats['paid_toilets_male']:,}", f"{stats['public_toilets']:,}"
            ]
        })
        st.dataframe(stats_table, use_container_width=True)


class EnvironmentPage(BasePage):
    def render(self):
        st.header("🌍 Environment & Air Quality")
        
        stats = self.app.get_environment_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("PM2.5 Avg", f"{stats['pm25_avg']:.1f}", "µg/m³")
        with col2:
            st.metric("PM10 Avg", f"{stats['pm10_avg']:.1f}", "µg/m³")
        with col3:
            st.metric("NO2 Avg", f"{stats['no2_avg']:.2f}", "µg/m³")
        with col4:
            st.metric("SO2 Avg", f"{stats['so2_avg']:.2f}", "µg/m³")
        with col5:
            st.metric("O3 Avg", f"{stats['o3_avg']:.2f}", "µg/m³")
        
        st.divider()
        
        st.subheader("Air Quality Trends (Last 12 Months)")
        trend_data = self.app.get_environment_trend()
        
        if trend_data is not None:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=trend_data['Month -Year'], y=trend_data['PM2.5'],
                name='PM2.5', mode='lines+markers'
            ))
            
            fig.add_trace(go.Scatter(
                x=trend_data['Month -Year'], y=trend_data['PM10'],
                name='PM10', mode='lines+markers'
            ))
            
            fig.update_layout(
                title='PM2.5 and PM10 Concentrations Over Time',
                xaxis_title='Month-Year', yaxis_title='Concentration (µg/m³)',
                height=400, hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Air Quality Standards")
        air_quality = pd.DataFrame({
            'Pollutant': ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3'],
            'Current Avg': [
                f"{stats['pm25_avg']:.1f}", f"{stats['pm10_avg']:.1f}",
                f"{stats['no2_avg']:.2f}", f"{stats['so2_avg']:.2f}", f"{stats['o3_avg']:.2f}"
            ],
            'Unit': ['µg/m³', 'µg/m³', 'µg/m³', 'µg/m³', 'µg/m³'],
            'WHO Guideline': ['15', '35', '40', '20', '100']
        })
        st.dataframe(air_quality, use_container_width=True)


class CrimesPage(BasePage):
    def render(self):
        st.header("🚔 Crime Statistics")
        
        crimes_data = self.app.get_crimes_trend()
        if crimes_data is None or crimes_data.empty:
            st.error("No crime data available")
            return
        
        latest_year = crimes_data.iloc[-1]
        latest_crimes = latest_year['Total number of crimes recorded']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Year", latest_year['Year'])
        with col2:
            st.metric("Crimes Recorded", f"{int(latest_crimes):,}")
        with col3:
            avg_crimes = crimes_data['Total number of crimes recorded'].mean()
            st.metric("Average (4 Years)", f"{int(avg_crimes):,}")
        
        st.divider()
        
        st.subheader("Crime Trend Over Years")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=crimes_data['Year'], y=crimes_data['Total number of crimes recorded'],
            name='Total Crimes', marker_color='indianred'
        ))
        
        fig.add_trace(go.Scatter(
            x=crimes_data['Year'], y=crimes_data['Total number of crimes recorded'],
            name='Trend', mode='lines', line=dict(color='darkred', width=2)
        ))
        
        fig.update_layout(
            title='Crime Records Trend', xaxis_title='Year', yaxis_title='Number of Crimes',
            height=400, hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Yearly Crime Data")
        crimes_display = crimes_data.copy()
        crimes_display['Total number of crimes recorded'] = crimes_display['Total number of crimes recorded'].astype(int)
        st.dataframe(crimes_display, use_container_width=True)


class InfrastructurePage(BasePage):
    def render(self):
        st.header("🛣️ Infrastructure - Intersections")
        
        stats = self.app.get_intersections_summary()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Intersections", f"{stats['total_intersections']:,}")
        with col2:
            st.metric("Signalized", f"{stats['signalized_intersections']:,}")
        with col3:
            pct_signalized = (stats['signalized_intersections'] / stats['total_intersections']) * 100
            st.metric("Signalization %", f"{pct_signalized:.1f}%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Intersections by Zone")
            by_zone = stats['by_zone']
            if by_zone is not None:
                fig = px.bar(by_zone, x='Zone Name', y='Value', title='Total Intersections')
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Signalized Intersections by Zone")
            sig_zone = stats['signalized_by_zone']
            if sig_zone is not None:
                fig = px.bar(sig_zone, x='Zone Name', y='Value',
                            title='Signalized Intersections', color_discrete_sequence=['#1f77b4'])
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)


class EmploymentPage(BasePage):
    def render(self):
        st.header("💼 Employment Statistics")
        
        stats = self.app.get_employment_stats()
        if not stats:
            st.error("No data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Labour Force", f"{stats['labour_force']:,}")
        with col2:
            st.metric("Employed", f"{stats['employed']:,}")
        with col3:
            st.metric("Unemployed", f"{stats['unemployed']:,}")
        with col4:
            st.metric("Unemployment Rate", f"{stats['unemployment_rate']:.2f}%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Employment Distribution")
            emp_data = pd.DataFrame({
                'Status': ['Employed', 'Unemployed'],
                'Count': [stats['employed'], stats['unemployed']]
            })
            fig = px.pie(emp_data, values='Count', names='Status',
                        color_discrete_sequence=['#2ecc71', '#e74c3c'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Labour Force Breakdown")
            breakdown = pd.DataFrame({
                'Category': ['Employed', 'Unemployed'],
                'Percentage': [stats['employment_rate'], stats['unemployment_rate']]
            })
            fig = px.bar(breakdown, x='Category', y='Percentage', title='Employment Rates')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Employment Summary")
        summary_table = pd.DataFrame({
            'Metric': [
                'Total Labour Force', 'Employed Persons', 'Unemployed Persons',
                'Employment Rate', 'Unemployment Rate'
            ],
            'Value': [
                f"{stats['labour_force']:,}", f"{stats['employed']:,}", f"{stats['unemployed']:,}",
                f"{stats['employment_rate']:.2f}%", f"{stats['unemployment_rate']:.2f}%"
            ]
        })
        st.dataframe(summary_table, use_container_width=True)


class DataExplorerPage(BasePage):
    def render(self):
        st.header("📊 Data Explorer")
        
        dataset = st.selectbox(
            "Select Dataset",
            ['Water & Sanitation', 'Environment', 'Crimes', 'Intersections', 'Employment']
        )
        
        dataset_map = {
            'Water & Sanitation': 'water_sanitation',
            'Environment': 'environment',
            'Crimes': 'crimes',
            'Intersections': 'intersections',
            'Employment': 'employment'
        }
        
        df = self.data[dataset_map[dataset]]
        
        if df is None or df.empty:
            st.error("No data available for this dataset")
            return
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        st.divider()
        
        st.subheader("Data Table")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null': df.count().values,
            'Unique': df.nunique().values
        })
        st.dataframe(col_info, use_container_width=True)

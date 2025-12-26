import streamlit as st
import pandas as pd
from dashboard_complete import DashboardApp
from pages_complete import (
    WaterSanitationPage,
    EnvironmentPage,
    CrimesPage,
    InfrastructurePage,
    EmploymentPage,
    DataExplorerPage
)

def main():
    st.set_page_config(
        page_title="Indore Analytics",
        page_icon="🏙️",
        layout="wide"
    )
    
    st.markdown("""
        <style>
            .main { padding: 0rem 0rem; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; }
        </style>
    """, unsafe_allow_html=True)
    
    app = DashboardApp()
    
    st.sidebar.title("🏙️ Indore Analytics")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        [
            "Overview",
            "💧 Water & Sanitation",
            "🌍 Environment",
            "🚔 Crime Data",
            "🛣️ Infrastructure",
            "💼 Employment",
            "📊 Raw Data"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("City data dashboard for Indore")
    
    if page == "Overview":
        show_overview(app)
    elif page == "💧 Water & Sanitation":
        WaterSanitationPage(app).render()
    elif page == "🌍 Environment":
        EnvironmentPage(app).render()
    elif page == "🚔 Crime Data":
        CrimesPage(app).render()
    elif page == "🛣️ Infrastructure":
        InfrastructurePage(app).render()
    elif page == "💼 Employment":
        EmploymentPage(app).render()
    elif page == "📊 Raw Data":
        DataExplorerPage(app).render()

def show_overview(app):
    st.title("🏙️ Indore City Dashboard")
    
    st.markdown("Analytics and insights for Indore city data across multiple sectors.")
    
    st.divider()
    
    st.header("Key Metrics")
    
    ws_stats = app.get_water_sanitation_stats()
    env_stats = app.get_environment_stats()
    crimes_data = app.get_crimes_trend()
    intr_stats = app.get_intersections_summary()
    emp_stats = app.get_employment_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Households", f"{ws_stats.get('total_households', 0):,}")
        st.metric("Intersections", f"{intr_stats.get('total_intersections', 0):,}")
    
    with col2:
        st.metric("PM2.5 Average", f"{env_stats.get('pm25_avg', 0):.1f} µg/m³")
        st.metric("Labour Force", f"{emp_stats.get('labour_force', 0):,}")
    
    with col3:
        crime_count = "N/A"
        if crimes_data is not None and not crimes_data.empty:
            crime_count = f"{int(crimes_data.iloc[-1]['Total number of crimes recorded']):,}"
        st.metric("Recent Crimes", crime_count)
        st.metric("Unemployment", f"{emp_stats.get('unemployment_rate', 0):.1f}%")
    
    st.divider()
    
    st.header("Available Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**💧 Water & Sanitation**")
        st.write("Household coverage, sewerage network, public facilities")
        
        st.write("**🚔 Crime Data**")
        st.write("Historical crime statistics and trends")
        
        st.write("**💼 Employment**")
        st.write("Labour force and unemployment statistics")
    
    with col2:
        st.write("**🌍 Environment**")
        st.write("Air quality monitoring (PM2.5, PM10, pollutants)")
        
        st.write("**🛣️ Infrastructure**")
        st.write("Traffic intersections and signalization data")
        
        st.write("**📊 Raw Data**")
        st.write("Browse and explore all datasets")
    
    st.divider()
    
    st.header("Dataset Status")
    
    datasets = ['water_sanitation', 'environment', 'crimes', 'intersections', 'employment']
    names = ['Water & Sanitation', 'Environment', 'Crime Data', 'Infrastructure', 'Employment']
    
    status_data = []
    for i, key in enumerate(datasets):
        count = len(app.data[key]) if app.data[key] is not None else 0
        status_data.append({'Dataset': names[i], 'Records': count})
    
    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True)

if __name__ == "__main__":
    main()
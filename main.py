import streamlit as st
import pandas as pd
from data_handler import DataHandler
from pages import WaterPage, EnvironmentPage, CrimePage, InfrastructurePage, EmploymentPage, DataExplorer

def main():
    st.set_page_config(
        page_title="Indore Analytics",
        page_icon="🏙️",
        layout="wide"
    )
    
    # Load data
    data_handler = DataHandler()
    
    # Sidebar navigation
    st.sidebar.title("🏙️ Indore Analytics")
    
    pages = {
        "Overview": None,
        "💧 Water & Sanitation": WaterPage(data_handler),
        "🌍 Environment": EnvironmentPage(data_handler),
        "🚔 Crime Data": CrimePage(data_handler),
        "🛣️ Infrastructure": InfrastructurePage(data_handler),
        "💼 Employment": EmploymentPage(data_handler),
        "📊 Data Explorer": DataExplorer(data_handler)
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.info("City analytics dashboard for Indore")
    
    # Render selected page
    if selected_page == "Overview":
        show_overview(data_handler)
    else:
        pages[selected_page].render()

def show_overview(data_handler):
    st.title("🏙️ Indore City Dashboard")
    st.markdown("Analytics and insights for Indore city data")
    
    st.divider()
    
    # Get all stats
    water_stats = data_handler.get_water_stats()
    env_stats = data_handler.get_environment_stats()
    crime_data = data_handler.get_crime_data()
    infra_stats = data_handler.get_infrastructure_stats()
    emp_stats = data_handler.get_employment_stats()
    
    # Key metrics
    st.header("Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Households", f"{water_stats.get('total_households', 0):,}")
        st.metric("Total Intersections", f"{infra_stats.get('total_intersections', 0):,}")
    
    with col2:
        st.metric("PM2.5 Average", f"{env_stats.get('pm25_avg', 0):.1f} µg/m³")
        st.metric("Labour Force", f"{emp_stats.get('labour_force', 0):,}")
    
    with col3:
        crime_count = "N/A"
        if crime_data is not None and not crime_data.empty:
            crime_count = f"{int(crime_data.iloc[-1]['Total number of crimes recorded']):,}"
        st.metric("Recent Crimes", crime_count)
        st.metric("Unemployment Rate", f"{emp_stats.get('unemployment_rate', 0):.1f}%")
    
    st.divider()
    
    # Dataset overview
    st.header("Available Datasets")
    
    datasets_info = []
    dataset_names = {
        'water': 'Water & Sanitation',
        'environment': 'Environment',
        'crimes': 'Crime Data',
        'infrastructure': 'Infrastructure',
        'employment': 'Employment'
    }
    
    for key, name in dataset_names.items():
        df = data_handler.datasets[key]
        record_count = len(df) if df is not None else 0
        datasets_info.append({
            'Dataset': name,
            'Records': record_count,
            'Status': '✅ Available' if record_count > 0 else '❌ No Data'
        })
    
    status_df = pd.DataFrame(datasets_info)
    st.dataframe(status_df, use_container_width=True)
    
    st.divider()
    
    # Quick insights
    st.header("Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Infrastructure")
        if infra_stats:
            signalization_rate = infra_stats.get('signalization_pct', 0)
            st.write(f"• {signalization_rate:.1f}% of intersections are signalized")
            st.write(f"• {infra_stats.get('total_intersections', 0):,} total intersections in the city")
    
    with col2:
        st.subheader("Environment")
        if env_stats:
            pm25 = env_stats.get('pm25_avg', 0)
            who_guideline = 15
            if pm25 > who_guideline:
                st.write(f"• PM2.5 levels ({pm25:.1f}) exceed WHO guidelines ({who_guideline})")
            else:
                st.write(f"• PM2.5 levels ({pm25:.1f}) are within WHO guidelines")

if __name__ == "__main__":
    main()
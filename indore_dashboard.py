import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indore City Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme toggle function
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Custom CSS for styling
def apply_custom_css(theme):
    if theme == 'dark':
        bg_color = "#0e1117"
        text_color = "#fafafa"
        card_bg = "#1e2130"
        accent_color = "#00d4ff"
        border_color = "#2e3548"
    else:
        bg_color = "#ffffff"
        text_color = "#262730"
        card_bg = "#f0f2f6"
        accent_color = "#ff4b4b"
        border_color = "#e0e0e0"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .main {{
            background-color: {bg_color};
        }}
        
        .header-container {{
            background: linear-gradient(135deg, {accent_color} 0%, #667eea 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        .header-title {{
            color: white;
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header-subtitle {{
            color: white;
            font-size: 1.2rem;
            font-weight: 300;
            margin-top: 0.5rem;
        }}
        
        .metric-card {{
            background-color: {card_bg};
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid {accent_color};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        
        .info-box {{
            background-color: {card_bg};
            padding: 1rem;
            border-radius: 10px;
            border: 2px solid {border_color};
            margin: 1rem 0;
        }}
        </style>
    """, unsafe_allow_html=True)

# Apply theme
apply_custom_css(st.session_state.theme)

# Theme toggle button
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(f"{theme_icon} Theme", key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏙️ Indore City Dashboard</h1>
        <p class="header-subtitle">Comprehensive Urban Data Analytics & Insights</p>
    </div>
""", unsafe_allow_html=True)

# Load all datasets
@st.cache_data
def load_data():
    data = {}
    errors = []
    
    file_map = {
        'city_profile': ('D01-CityProfile_25.xls', 'excel'),
        'unemployment': ('D02-UnemploymentRate_17_0.csv', 'csv'),
        'households': ('D03-Households_35.xls', 'excel'),
        'environment': ('D04-Environment_6_2_2.csv', 'csv'),
        'water_sanitation': ('D11-waterAndsanitation_1_1_1.csv', 'csv'),
        'intersections': ('D35-Intersections_6_1.csv', 'csv'),
        'digital': ('D45-DigitalAvailability_20.xls', 'excel'),
        'crimes': ('D47-Crimes_13_1.csv', 'csv')
    }
    
    for key, (filename, file_type) in file_map.items():
        try:
            if file_type == 'excel':
                data[key] = pd.read_excel(filename)
            else:
                data[key] = pd.read_csv(filename)
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
    
    return data, errors

data, loading_errors = load_data()

# Check if data loaded successfully
if loading_errors:
    st.error("⚠️ Error loading some datasets:")
    for error in loading_errors:
        st.error(f"• {error}")
    st.info("📝 Make sure all data files are in the same directory as this script:")
    st.code("""
D01-CityProfile_25.xls
D02-UnemploymentRate_17_0.csv
D03-Households_35.xls
D04-Environment_6_2_2.csv
D11-waterAndsanitation_1_1_1.csv
D35-Intersections_6_1.csv
D45-DigitalAvailability_20.xls
D47-Crimes_13_1.csv
    """)
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "Select a page:",
        ["🏠 Overview", "👥 Demographics", "🌍 Environment", "💧 Water & Sanitation", 
         "🚦 Traffic", "🔒 Crime Analysis", "💻 Digital Services"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    if 'city_profile' in data and len(data['city_profile']) > 0:
        total_wards = len(data['city_profile'])
        total_pop = data['city_profile']['Total Population (in thousands)'].sum()/1000
        st.markdown(f"""
        - **Total Wards:** {total_wards}
        - **Total Population:** {total_pop:.1f}M
        - **Datasets:** {len(data)} loaded
        """)

# Page: Overview
if page == "🏠 Overview":
    st.markdown("## 📊 City Overview Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_pop = data['city_profile']['Total Population (in thousands)'].sum()
    total_households = data['households']['Total no. of Households'].sum()
    total_crimes = data['crimes']['Total number of crimes recorded'].sum()
    employment_rate = (data['unemployment']['No. of employed persons'].sum() / 
                      data['unemployment']['Total labour force in the city (age 15-59) [Employed + Unemployed Persons)'].sum() * 100)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Population", f"{total_pop/1000:.2f}M", "👥")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Households", f"{total_households:,}", "🏠")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Employment Rate", f"{employment_rate:.1f}%", "💼")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Crimes", f"{total_crimes:,}", "🔒")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏘️ Top 10 Wards by Population")
        top_wards = data['city_profile'].nlargest(10, 'Total Population (in thousands)')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.viridis(np.linspace(0, 1, 10))
        bars = ax.barh(top_wards['Ward Name'], top_wards['Total Population (in thousands)'], 
                      color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Population (thousands)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Ward Name', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 📈 Crime Trend Over Years")
        crimes_df = data['crimes'].sort_values('Year')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(crimes_df['Year'], crimes_df['Total number of crimes recorded'], 
               marker='o', linewidth=3, markersize=10, color='#FF6B6B')
        ax.fill_between(crimes_df['Year'], crimes_df['Total number of crimes recorded'], 
                       alpha=0.3, color='#FF6B6B')
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Crimes', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Page: Demographics
elif page == "👥 Demographics":
    st.markdown("## 👥 Population & Household Analysis")
    
    # Zone-wise statistics
    zone_pop = data['city_profile'].groupby('Zone Name')['Total Population (in thousands)'].sum().reset_index()
    zone_hh = data['households'].groupby('Zone Name')['Total no. of Households'].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗺️ Population by Zone")
        fig, ax = plt.subplots(figsize=(10, 8))
        top_zones = zone_pop.nlargest(8, 'Total Population (in thousands)')
        colors = plt.cm.plasma(np.linspace(0, 1, len(top_zones)))
        wedges, texts, autotexts = ax.pie(top_zones['Total Population (in thousands)'], 
                                           labels=top_zones['Zone Name'],
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90,
                                           textprops={'fontsize': 9, 'fontweight': 'bold'})
        ax.set_title('Top 8 Zones by Population', fontsize=14, fontweight='bold', pad=20)
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 🏘️ Households by Zone (Top 10)")
        zone_hh_sorted = zone_hh.nlargest(10, 'Total no. of Households')
        colors = plt.cm.viridis(np.linspace(0, 1, len(zone_hh_sorted)))
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(zone_hh_sorted['Zone Name'].astype(str), zone_hh_sorted['Total no. of Households'],
               color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Number of Households', fontsize=12, fontweight='bold')
        ax.set_ylabel('Zone', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    st.markdown("---")
    
    # Employment statistics
    st.markdown("### 💼 Employment Statistics")
    col1, col2, col3 = st.columns(3)
    
    employed = data['unemployment']['No. of employed persons'].iloc[0]
    unemployed = data['unemployment']['No. of unemployed persons (seeking or available for work)'].iloc[0]
    total_workforce = data['unemployment']['Total labour force in the city (age 15-59) [Employed + Unemployed Persons)'].iloc[0]
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Employed")
        st.markdown(f"**{employed:,}**")
        st.markdown(f"{(employed/total_workforce*100):.1f}% of workforce")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Unemployed")
        st.markdown(f"**{unemployed:,}**")
        st.markdown(f"{(unemployed/total_workforce*100):.1f}% of workforce")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Total Workforce")
        st.markdown(f"**{total_workforce:,}**")
        st.markdown("Age 15-59")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Employment visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ['Employed', 'Unemployed']
    sizes = [employed, unemployed]
    colors = ['#4ECDC4', '#FF6B6B']
    explode = (0.05, 0.05)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       colors=colors, startangle=90,
                                       textprops={'fontsize': 14, 'fontweight': 'bold'})
    ax.set_title('Employment Distribution', fontsize=16, fontweight='bold', pad=20)
    fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Page: Environment
elif page == "🌍 Environment":
    st.markdown("## 🌍 Environmental Quality Analysis")
    
    env_df = data['environment'].copy()
    env_df = env_df.sort_values('Month -Year')
    
    # Key environmental metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_pm25 = env_df['Monthly mean/average concentration - PM2.5'].mean()
    avg_pm10 = env_df['Monthly mean concentration - PM10'].mean()
    avg_no2 = env_df['Monthly mean concentration - NO2'].mean()
    avg_so2 = env_df['Monthly mean concentration - SO2'].mean()
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg PM2.5", f"{avg_pm25:.1f} μg/m³", "⚠️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg PM10", f"{avg_pm10:.1f} μg/m³", "⚠️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg NO2", f"{avg_no2:.1f} μg/m³", "🌫️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg SO2", f"{avg_so2:.1f} μg/m³", "🌫️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Multi-pollutant trend
    st.markdown("### 📊 Air Quality Trends Over Time")
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = range(len(env_df))
    ax.plot(x, env_df['Monthly mean/average concentration - PM2.5'], 
           label='PM2.5', marker='o', linewidth=2.5, color='#FF6B6B')
    ax.plot(x, env_df['Monthly mean concentration - PM10'], 
           label='PM10', marker='s', linewidth=2.5, color='#4ECDC4')
    ax.plot(x, env_df['Monthly mean concentration - NO2'], 
           label='NO2', marker='^', linewidth=2.5, color='#45B7D1')
    ax.plot(x, env_df['Monthly mean concentration - SO2'], 
           label='SO2', marker='D', linewidth=2.5, color='#FFA07A')
    
    ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
    ax.set_ylabel('Concentration (μg/m³)', fontsize=12, fontweight='bold')
    ax.set_title('Pollutant Concentration Trends', fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(x[::3])
    ax.set_xticklabels(env_df['Month -Year'].iloc[::3], rotation=45, ha='right')
    ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
    fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown("---")
    
    # Pollutant distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 PM2.5 Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        n, bins, patches = ax.hist(env_df['Monthly mean/average concentration - PM2.5'], 
                                   bins=10, edgecolor='black', alpha=0.7)
        for i, patch in enumerate(patches):
            patch.set_facecolor(plt.cm.Reds(i / len(patches)))
        ax.set_xlabel('PM2.5 Concentration (μg/m³)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.axvline(avg_pm25, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_pm25:.1f}')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 📊 PM10 Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        n, bins, patches = ax.hist(env_df['Monthly mean concentration - PM10'], 
                                   bins=10, edgecolor='black', alpha=0.7)
        for i, patch in enumerate(patches):
            patch.set_facecolor(plt.cm.Blues(i / len(patches)))
        ax.set_xlabel('PM10 Concentration (μg/m³)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.axvline(avg_pm10, color='blue', linestyle='--', linewidth=2, label=f'Mean: {avg_pm10:.1f}')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Page: Water & Sanitation
elif page == "💧 Water & Sanitation":
    st.markdown("## 💧 Water & Sanitation Infrastructure")
    
    ws_df = data['water_sanitation']
    
    # Key metrics
    total_hh = ws_df['Total number of households (HH)'].sum()
    sewerage_hh = ws_df['HH part of the city sewerage network'].sum()
    toilet_hh = ws_df['Number of Households with toilets'].sum()
    public_toilets = ws_df['Number of Public Toilet '].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Households", f"{total_hh:,}", "🏠")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Sewerage Coverage", f"{(sewerage_hh/total_hh*100):.1f}%", "🚰")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("HH with Toilets", f"{(toilet_hh/total_hh*100):.1f}%", "🚽")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Public Toilets", f"{public_toilets}", "🚻")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Sanitation Coverage")
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = ['Sewerage\nConnected', 'With Toilets', 'Not Connected']
        values = [sewerage_hh, toilet_hh, total_hh - sewerage_hh]
        colors = ['#4ECDC4', '#45B7D1', '#FF6B6B']
        
        bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_ylabel('Number of Households', fontsize=12, fontweight='bold')
        ax.set_title('Household Sanitation Coverage', fontsize=14, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 🚻 Public Toilet Distribution")
        
        zone_toilets = ws_df.groupby('Zone Name')['Number of Public Toilet '].sum().reset_index()
        zone_toilets = zone_toilets[zone_toilets['Number of Public Toilet '] > 0].sort_values('Number of Public Toilet ', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.viridis(np.linspace(0, 1, len(zone_toilets)))
        bars = ax.barh(zone_toilets['Zone Name'], zone_toilets['Number of Public Toilet '],
                      color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Number of Public Toilets', fontsize=12, fontweight='bold')
        ax.set_ylabel('Zone', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Zones by Public Toilets', fontsize=14, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Page: Traffic
elif page == "🚦 Traffic":
    st.markdown("## 🚦 Traffic Infrastructure Analysis")
    
    int_df = data['intersections']
    
    total_intersections = int_df['No. of intersections / junctions'].sum()
    signalized = int_df['Total number of operational signalized intersections'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Intersections", f"{total_intersections}", "🚦")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Signalized", f"{signalized}", "🚥")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Signalization Rate", f"{(signalized/total_intersections*100):.1f}%", "📊")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗺️ Zone-wise Intersections")
        zone_int = int_df.groupby('Zone Name')[['No. of intersections / junctions', 
                                                 'Total number of operational signalized intersections']].sum().reset_index()
        zone_int = zone_int.sort_values('No. of intersections / junctions', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 7))
        x = np.arange(len(zone_int))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, zone_int['No. of intersections / junctions'], width,
                      label='Total Intersections', color='#4ECDC4', edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, zone_int['Total number of operational signalized intersections'], width,
                      label='Signalized', color='#FF6B6B', edgecolor='black', linewidth=0.5)
        
        ax.set_xlabel('Zone', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Zones by Intersections', fontsize=14, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(zone_int['Zone Name'], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 📊 Signalization Status")
        
        labels = ['Signalized', 'Non-Signalized']
        sizes = [signalized, total_intersections - signalized]
        colors = ['#4ECDC4', '#FF6B6B']
        explode = (0.05, 0.05)
        
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90,
                                           textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Intersection Signalization', fontsize=14, fontweight='bold', pad=20)
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Page: Crime Analysis
elif page == "🔒 Crime Analysis":
    st.markdown("## 🔒 Crime Statistics & Trends")
    
    crimes_df = data['crimes'].sort_values('Year')
    
    latest_year = crimes_df.iloc[-1]
    previous_year = crimes_df.iloc[-2] if len(crimes_df) > 1 else latest_year
    change = latest_year['Total number of crimes recorded'] - previous_year['Total number of crimes recorded']
    pct_change = (change / previous_year['Total number of crimes recorded'] * 100)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Latest Year", latest_year['Year'], "📅")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Crimes", f"{latest_year['Total number of crimes recorded']:,}", 
                 f"{change:+,} ({pct_change:+.1f}%)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_all_years = crimes_df['Total number of crimes recorded'].sum()
        st.metric("All Years Total", f"{total_all_years:,}", "📊")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Crime Trend Analysis")
        fig, ax = plt.subplots(figsize=(12, 7))
        
        ax.plot(crimes_df['Year'], crimes_df['Total number of crimes recorded'],
               marker='o', linewidth=3, markersize=12, color='#FF6B6B', label='Total Crimes')
        ax.fill_between(crimes_df['Year'], crimes_df['Total number of crimes recorded'],
                       alpha=0.3, color='#FF6B6B')
        
        for idx, row in crimes_df.iterrows():
            ax.annotate(f"{row['Total number of crimes recorded']:,}",
                       xy=(row['Year'], row['Total number of crimes recorded']),
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
        
        ax.set_xlabel('Year', fontsize=13, fontweight='bold')
        ax.set_ylabel('Number of Crimes', fontsize=13, fontweight='bold')
        ax.set_title('Crime Rate Over Years', fontsize=15, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.xticks(rotation=45)
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### 📊 Year-wise Distribution")
        fig, ax = plt.subplots(figsize=(8, 7))
        colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(crimes_df)))
        bars = ax.bar(crimes_df['Year'], crimes_df['Total number of crimes recorded'],
                     color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_xlabel('Year', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Crimes', fontsize=11, fontweight='bold')
        ax.set_title('Crime Distribution', fontsize=13, fontweight='bold', pad=15)
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa' if st.session_state.theme == 'light' else '#1e2130')
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Page: Digital Services
elif page == "💻 Digital Services":
    st.markdown("## 💻 Digital Service Availability")
    
    digital_df = data['digital']
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 🌐 E-Governance Services Status")
    st.markdown("Overview of online services available for Indore citizens")
    st.markdown('</div>', unsafe_allow_html=True)
    
    services = {
        'Tax Payment': digital_df['Online Payment of taxes (property / water) [Yes / No]'].iloc[0],
        'Traffic Violations': digital_df['Online Payment against traffic violations (challans, fines, etc.) [Yes / No]'].iloc[0],
        'Service Connections': digital_df['Online request for Service Connections (gas, water supply) [Yes / No]'].iloc[0],
        'Certificates': digital_df['Online request for Certificates / Licenses (marriage, driving, birth & death certificates) [Yes / No]'].iloc[0],
        'Tenders': digital_df['Online display of Tenders (for various works) across various departments/ utilities [Yes / No]'].iloc[0],
        'Grievances': digital_df['Online Grievance management (tracking of complaints) [Yes / No]'].iloc[0],
        'Tickets': digital_df['Online buying of Tickets and passes (e.g. public transport, cultural events) [Yes / No]'].iloc[0],
        'Documents': digital_df['Online request of Disclosure of documents (e.g. budgets, plans, RTI requests) [Yes / No]'].iloc[0]
    }
    
    available = sum(1 for v in services.values() if v.lower() == 'yes')
    total_services = len(services)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📊 Service Availability")
        
        fig, ax = plt.subplots(figsize=(8, 8))
        sizes = [available, total_services - available]
        labels = ['Available', 'Not Available']
        colors = ['#4ECDC4', '#FF6B6B']
        explode = (0.1, 0)
        
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%',
                                           colors=colors, startangle=90,
                                           textprops={'fontsize': 14, 'fontweight': 'bold'})
        ax.set_title(f'{available}/{total_services} Services Online', fontsize=16, fontweight='bold', pad=20)
        fig.patch.set_facecolor('#ffffff' if st.session_state.theme == 'light' else '#0e1117')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### ✅ Service Details")
        
        for service, status in services.items():
            icon = "✅" if status.lower() == 'yes' else "❌"
            color = "green" if status.lower() == 'yes' else "red"
            st.markdown(f"**{icon} {service}** - Status: :{color}[{status}]")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>🏙️ Indore City Data Dashboard | Built with Streamlit, Pandas, NumPy & Matplotlib</p>
        <p>Data Sources: City Profile, Environment, Demographics, Infrastructure & Public Services</p>
    </div>
""", unsafe_allow_html=True)

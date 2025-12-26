# Indore City Analytics Dashboard

A clean, simple data visualization dashboard for Indore city statistics built with Streamlit.

## Features

- **Water & Sanitation**: Household coverage and public facilities
- **Environment**: Air quality monitoring and pollution data
- **Crime Statistics**: Historical crime trends and analysis
- **Infrastructure**: Traffic intersections and signalization
- **Employment**: Labour force and unemployment statistics
- **Data Explorer**: Browse raw datasets

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run main.py
```

3. Open your browser to `http://localhost:8501`

## Project Structure

```
├── main.py              # Main application
├── data_handler.py      # Data loading and processing
├── pages.py            # Dashboard page components
├── requirements.txt    # Dependencies
└── datasets/
    └── unified/        # CSV data files
```

## Data Sources

The dashboard uses CSV datasets in `datasets/unified/`:
- `unified_water_sanitation.csv` - Water and sanitation data
- `unified_environment.csv` - Air quality monitoring
- `unified_crimes.csv` - Crime statistics
- `unified_intersections.csv` - Infrastructure data
- `unified_employment.csv` - Employment statistics

## Usage

Navigate through sections using the sidebar. Each section provides key metrics, visualizations, and data tables. Use the Data Explorer to browse raw datasets.
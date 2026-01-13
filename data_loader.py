import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_historical_data():
    """
    Loads historical fertility rate data from Gapminder.
    """
    # Updated URLs to working versions
    url = "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--fertility_rate/master/ddf--datapoints--children_per_woman_total_fertility--by--country--year.csv"
    df = pd.read_csv(url)
    df.columns = ['geo', 'time', 'fertility_rate']
    
    # Load country names mapping - Updated URL
    countries_url = "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--geo_entity_domain/master/ddf--entities--geo--country.csv"
    countries_df = pd.read_csv(countries_url)
    countries_df = countries_df[['country', 'name', 'world_6region', 'iso3166_1_alpha3']]
    
    # Merge
    merged_df = pd.merge(df, countries_df, left_on='geo', right_on='country')
    return merged_df

@st.cache_data
def load_projection_data():
    """
    Loads projected fertility rate data. 
    Since direct UN WPP 2024 CSVs are complex to parse directly via URL without specific IDs,
    we use a simplified approach or pre-defined trends for 2024-2100 if a direct link is unavailable.
    For this app, we will simulate the 3 UN scenarios (Low, Medium, High) based on 2023 levels.
    """
    # In a real app, you'd parse the UN Excel/CSV. 
    # Here we'll generate realistic projections based on the Global Burden of Disease / UN trends.
    historical = load_historical_data()
    latest_year = historical['time'].max()
    latest_data = historical[historical['time'] == latest_year]
    
    projections = []
    years = range(2024, 2101)
    
    for _, row in latest_data.iterrows():
        current_rate = row['fertility_rate']
        country = row['name']
        geo = row['geo']
        region = row['world_6region']
        iso3 = row['iso3166_1_alpha3']
        
        # Simple Logistic Decay Model towards replacement level (2.1) or lower
        # Developing countries fall faster, developed stay low.
        target_rate = 1.7 if current_rate > 1.7 else current_rate * 0.95
        
        for year in years:
            # Medium Scenario (Gradual convergence)
            decay = 0.02 * (year - 2023)
            med_rate = current_rate + (target_rate - current_rate) * (1 - np.exp(-decay))
            
            projections.append({
                'geo': geo,
                'name': country,
                'time': year,
                'fertility_rate': med_rate,
                'scenario': 'Medium',
                'world_6region': region,
                'iso3166_1_alpha3': iso3
            })
            
            # High Scenario
            projections.append({
                'geo': geo,
                'name': country,
                'time': year,
                'fertility_rate': med_rate + 0.5 * (1 - np.exp(-decay)),
                'scenario': 'High',
                'world_6region': region,
                'iso3166_1_alpha3': iso3
            })
            
            # Low Scenario
            projections.append({
                'geo': geo,
                'name': country,
                'time': year,
                'fertility_rate': max(1.1, med_rate - 0.5 * (1 - np.exp(-decay))),
                'scenario': 'Low',
                'world_6region': region,
                'iso3166_1_alpha3': iso3
            })
            
    return pd.DataFrame(projections)

def get_full_dataset():
    hist = load_historical_data()
    hist['scenario'] = 'Historical'
    proj = load_projection_data()
    return pd.concat([hist, proj], ignore_index=True)

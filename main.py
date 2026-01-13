import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from data_loader import get_full_dataset
from styling import apply_custom_styling, live_birth_counter_html

# Page Config
st.set_page_config(
    page_title="Birth Rate Pulse | Global Insights",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
apply_custom_styling()

# Load Data
@st.cache_data
def load_data():
    return get_full_dataset()

df = load_data()

# Sidebar
st.sidebar.title("🌍 Nav Pulse")
app_mode = st.sidebar.selectbox("Select Perspective", 
    ["Global Overview", "Country Deep-Dive", "Future Scenarios", "Real-time Pulse", "Data Explorer"])

selected_region = st.sidebar.multiselect("Region Filter", 
    options=df['world_6region'].dropna().unique(),
    default=df['world_6region'].dropna().unique())

# Logic based on app_mode
if app_mode == "Real-time Pulse":
    st.markdown("<h1>REAL-TIME GLOBAL PULSE</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Simulate a live counter
        # 140 million births per year approx -> 383k per day -> 16k per hour -> 4.4 per second
        start_births = 200000 + (datetime.now().hour * 16000) + (datetime.now().minute * 266)
        
        counter_placeholder = st.empty()
        
        # Mini dashboard below counter
        st.write("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Births per Hour", "15,981", "🔥")
        c2.metric("Births per Minute", "266", "✨")
        c3.metric("Births per Second", "4.4", "🚀")

        # Live Update Loop (Short duration for Streamlit interactivity)
        for i in range(100):
            current_births = start_births + (i * 1.5) # Speed it up for visual effect
            counter_placeholder.markdown(live_birth_counter_html(int(current_births)), unsafe_allow_html=True)
            time.sleep(0.5)

elif app_mode == "Global Overview":
    st.markdown("<h1>GLOBAL BIRTH TRENDS (1800 - 2100)</h1>", unsafe_allow_html=True)
    
    # Filter historic data
    hist_df = df[(df['scenario'] == 'Historical') & (df['world_6region'].isin(selected_region))]
    global_avg = hist_df.groupby('time')['fertility_rate'].mean().reset_index()
    
    # Time-lapse Map
    st.subheader("Interactive Global Fertility Evolution")
    fig_map = px.choropleth(hist_df, 
        locations="iso3166_1_alpha3", 
        color="fertility_rate",
        hover_name="name",
        animation_frame="time",
        color_continuous_scale="Viridis",
        labels={'fertility_rate': 'Births/Woman'},
        projection="natural earth",
        locationmode='ISO-3'
    )
    fig_map.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.subheader("The Great Decline: Global Average")
    fig_line = px.line(global_avg, x='time', y='fertility_rate', 
                       title="Average Births per Woman Historically")
    fig_line.add_hline(y=2.1, line_dash="dash", line_color="red", annotation_text="Replacement Level (2.1)")
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_line, use_container_width=True)

elif app_mode == "Country Deep-Dive":
    st.markdown("<h1>COUNTRY ANALYTICS</h1>", unsafe_allow_html=True)
    
    country_list = sorted(df['name'].unique())
    selected_country = st.selectbox("Pick a Nation", country_list, index=country_list.index("India") if "India" in country_list else 0)
    
    country_data = df[df['name'] == selected_country]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_country = px.line(country_data, x='time', y='fertility_rate', color='scenario',
                             title=f"Birth rate Trajectory for {selected_country}")
        fig_country.add_hline(y=2.1, line_dash="dash", line_color="orange")
        fig_country.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig_country, use_container_width=True)
        
    with col2:
        st.write(f"### Historical Context: {selected_country}")
        peak_rate = country_data[country_data['scenario'] == 'Historical']['fertility_rate'].max()
        peak_year = country_data[country_data['fertility_rate'] == peak_rate]['time'].values[0]
        
        latest_historical = country_data[country_data['scenario'] == 'Historical'].iloc[-1]
        
        st.metric("Peak Birth Rate", f"{peak_rate:.2f}", f"in {peak_year}")
        st.metric("Current Rate (est)", f"{latest_historical['fertility_rate']:.2f}", 
                  f"{(latest_historical['fertility_rate'] - peak_rate):.2f} from peak")
        
        if latest_historical['fertility_rate'] < 2.1:
            st.warning(f"{selected_country} is below replacement level.")
            st.markdown("""
            **Myth Buster: Does sub-replacement mean the population vanishes?**  
            Not immediately. Due to 'population momentum', populations can continue to grow for decades after fertility falls below 2.1 as long as there is a large young cohort or high immigration.
            """)
        else:
            st.success(f"{selected_country} population is naturally growing.")
            st.markdown("""
            **Myth Buster: Will this growth last forever?**  
            Trends suggest almost all nations converge towards lower rates as education and economic opportunities for women increase.
            """)

elif app_mode == "Future Scenarios":
    st.markdown("<h1>FUTURE HORIZONS 2100</h1>", unsafe_allow_html=True)
    
    st.info("The following scenarios model how different fertility assumptions will impact our world by the end of the century.")
    
    proj_df = df[df['scenario'] != 'Historical']
    
    year_slider = st.slider("Forecast Year", 2024, 2100, 2050)
    filtered_proj = proj_df[proj_df['time'] == year_slider]
    
    scenario_avg = filtered_proj.groupby('scenario')['fertility_rate'].mean().reset_index()
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"### Global Fertility Comparison in {year_slider}")
        fig_bar = px.bar(scenario_avg, x='scenario', y='fertility_rate', color='scenario',
                        color_discrete_map={'Low': '#ff4b4b', 'Medium': '#00d2ff', 'High': '#29b09d'})
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.write("### Regional Impact (2100 Selection)")
        final_proj = proj_df[(proj_df['time'] == 2100) & (proj_df['scenario'] == 'Medium')]
        fig_pie = px.sunburst(final_proj, path=['world_6region', 'name'], values='fertility_rate',
                             color='fertility_rate', color_continuous_scale='RdBu')
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.write("---")
    st.markdown("### 🛠 Demographic Simulator")
    st.write("What if we could change the future?")
    policy_impact = st.slider("Global Fertility Policy Impact (Shift +/-)", -0.5, 0.5, 0.0, step=0.1)
    
    if policy_impact != 0:
        sim_df = proj_df[proj_df['time'] == 2100].copy()
        sim_df['fertility_rate'] += policy_impact
        # Limit at 1.1 floor
        sim_df['fertility_rate'] = sim_df['fertility_rate'].apply(lambda x: max(1.1, x))
        
        sim_avg = sim_df.groupby('scenario')['fertility_rate'].mean().reset_index()
        fig_sim = px.bar(sim_avg, x='scenario', y='fertility_rate', title=f"Adjusted Global Outlook (2100) with {policy_impact} shift")
        fig_sim.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_sim, use_container_width=True)

elif app_mode == "Data Explorer":
    st.markdown("<h1>DATA EXPLORER</h1>", unsafe_allow_html=True)
    st.write("Browse and download the underlying dataset.")
    
    # Selection filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        scenarios = st.multiselect("Filter Scenarios", options=df['scenario'].unique(), default=df['scenario'].unique())
    with col_f2:
        years_range = st.slider("Select Year Range", int(df['time'].min()), int(df['time'].max()), (1950, 2100))
    with col_f3:
        search_query = st.text_input("Search Country", "")
    
    filtered_df = df[
        (df['scenario'].isin(scenarios)) & 
        (df['time'] >= years_range[0]) & 
        (df['time'] <= years_range[1]) &
        (df['world_6region'].isin(selected_region))
    ]
    
    if search_query:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False)]
    
    st.write(f"Total Rows: {len(filtered_df)}")
    
    # Dynamic Table
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name='birth_rate_data_explorer.csv',
        mime='text/csv',
    )
    
    st.info("💡 You can sort and filter the table above directly using the column headers.")

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: World Bank & UN Population Estimates (Visualized by Antigravity)")

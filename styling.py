import streamlit as st

def apply_custom_styling():
    st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Glassmorphism Containers */
    div.stMetric, div.stAlert, .stMarkdownContainer {
        # background: rgba(255, 255, 255, 0.05);
        # backdrop-filter: blur(10px);
        # border-radius: 15px;
        # border: 1px solid rgba(255, 255, 255, 0.1);
        # padding: 10px;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
    }
    
    h2, h3 {
        color: #00d2ff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 12, 41, 0.8);
        border-right: 1px solid rgba(0, 210, 255, 0.2);
    }
    
    /* Metric Enhancement */
    [data-testid="stMetricValue"] {
        color: #00d2ff;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #ffffff;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 210, 255, 0.2) !important;
        border-bottom: 2px solid #00d2ff !important;
    }

    /* Live Counter Styling */
    .live-counter {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #ff007f;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.5);
        margin: 20px 0;
    }
    
    /* Hide Streamlit components for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

def live_birth_counter_html(count):
    return f"""
    <div class="live-counter">
        {count:,}
    </div>
    <div style="text-align: center; font-size: 0.8rem; color: #aaa;">ESTIMATED BIRTHS TODAY WORLDWIDE</div>
    """

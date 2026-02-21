import streamlit as st 


import streamlit as st


def css_styling():
    st.markdown("""
    <style>

    html, body, [class*="css"]  {
        font-family: "Georgia", "Times New Roman", serif;
    }

    .stApp {
        background: linear-gradient(
            180deg,
            #141414 0%,
            #101010 100%
        );
        color: #E8E6E3;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1250px;
    }

    .main_title {
        font-size: 58px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #E8E6E3;
        margin-bottom: 0;
    }

    .subtitle {
        color: #A6A6A6;
        font-size: 20px;
        margin-bottom: 25px;
        max-width: 850px;
        line-height: 1.6;
    }

    .section-header {
        font-size: 30px;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 18px;
        color: #E8E6E3;
        letter-spacing: -0.3px;
    }

    .card {
        background-color: #1C1C1C;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #343434;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    /* subtle warm glow */
    .card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at top left,
            rgba(198,161,91,0.08),
            transparent 40%
        );
        opacity: 0;
        transition: opacity 0.25s;
    }

    .card:hover::before {
        opacity: 1;
    }

    .card:hover {
        transform: translateY(-8px);
        border-color: #C6A15B;
    }


    .metric-label {
        color: #A6A6A6;
        margin: 0;
        font-size: 14px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    .metric-value {
        font-size: 40px;
        font-weight: 800;
        margin-top: 8px;
        color: #E8E6E3;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6em 1.2em;
        background-color: #222222;
        color: #E8E6E3;
        border: 1px solid #343434;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #C6A15B;
        color: #C6A15B;
    }

    section[data-testid="stSidebar"] {
        background: #111111;
        border-right: 1px solid #2A2A2A;
    }


    .stAlert {
        border-radius: 12px;
        background-color: #1C1C1C;
        border: 1px solid #343434;
        color: #E8E6E3;
    }


    </style>
    """, unsafe_allow_html=True)



def metric_card(label, value):
    st.markdown(f"""
        <div class="card">
            <p class="metric-label">{label}</p>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

    

def metric_card(label, value):
    st.markdown(f"""
        <div class="card">
            <p class="metric-label">{label}</p>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)
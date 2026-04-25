# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import simulation as sim
import content

st.set_page_config(page_title="Monte Carlo Simulation", layout="wide")

# Initialize Session State
if 'sim_count' not in st.session_state:
    st.session_state.sim_count = 0

# App Title with Emojis
st.title("🎲 Monte Carlo Simulation Dashboard 🪙")

# Definitions from our static file
with st.expander("📚 Key Definitions"):
    st.markdown(content.get_definitions())

# Sidebar
with st.sidebar:
    st.info(content.get_sidebar_info())
    mode = st.selectbox("Type", ["Coin Toss", "Dice Roll"])
    n_trials = st.number_input("Trials", value=10000)
    n_repeats = st.number_input("Repeats", value=1000)
    run_btn = st.button("Run Simulation")

if run_btn:
    st.session_state.sim_count += 1
    results = sim.run_monte_carlo(mode, n_trials, n_repeats)
    t_mean, t_sd = sim.calculate_theory(mode, n_trials)
    
    st.header(f"Simulation #{st.session_state.sim_count}")
    
    # Visualization & Stats
    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots()
        ax.hist(results, bins=50, color='skyblue', edgecolor='black')
        st.pyplot(fig)
        
    with col2:
        sigmas = [1, 1.5, 2, 2.5, 3, 6]
        df = pd.DataFrame({
            "Sigma": [f"{s}σ" for s in sigmas],
            "Lower": [t_mean - (s * t_sd) for s in sigmas],
            "Upper": [t_mean + (s * t_sd) for s in sigmas]
        })
        st.table(df)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Monte Carlo Simulator", layout="wide")

# --- Constants & Limits ---
# Total elements limit (Trials * Repeats) set to 10 Million for stability
MAX_TOTAL_ELEMENTS = 10_000_000 

def run_simulation(mode, trials, repeats):
    if mode == "Coin Toss":
        # Using uint8 to save 8x memory compared to default int64
        data = np.random.randint(0, 2, size=(repeats, trials), dtype=np.uint8)
        results = data.sum(axis=1)
        label = "Number of Heads"
    else:
        # Dice roll
        data = np.random.randint(1, 7, size=(repeats, trials), dtype=np.uint8)
        results = data.mean(axis=1)
        label = "Average Dice Value"
    return results, label

st.title("🎲 Safe Monte Carlo Simulator")

with st.sidebar:
    st.header("Configuration")
    sim_mode = st.selectbox("Select Simulation", ["Coin Toss", "Dice Roll"])
    
    n_trials = st.number_input("Trials per repeat", min_value=1, max_value=1_000_000, value=10_000)
    n_repeats = st.number_input("Number of repeats", min_value=1, max_value=100_000, value=1_000)
    
    total_requested = n_trials * n_repeats
    
    # Safety Check Logic
    if total_requested > MAX_TOTAL_ELEMENTS:
        st.error(f"⚠️ Calculation too large! {total_requested:,} exceeds limit of {MAX_TOTAL_ELEMENTS:,}.")
        run_btn = st.button("Run Simulation", disabled=True)
    else:
        st.success(f"✅ Simulation size safe: {total_requested:,} points.")
        run_btn = st.button("Run Simulation")

if run_btn:
    results, axis_label = run_simulation(sim_mode, n_trials, n_repeats)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Frequency Histogram")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Using your logic for frequency plotting
        # We cap bins at 100 to keep rendering fast
        num_bins = min(len(np.unique(results)), 100)
        ax.hist(results, bins=num_bins, color='#2ec4b6', edgecolor='black', alpha=0.8)
        
        ax.set_xlabel(axis_label)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col2:
        st.subheader("Stats")
        stats_data = {
            "Mean": [np.mean(results)],
            "Std Dev": [np.std(results)],
            "Range": [f"{np.min(results)} - {np.max(results)}"]
        }
        st.table(pd.DataFrame(stats_data).T)
else:
    st.info("Adjust the settings in the sidebar and click 'Run Simulation' to see the results.")
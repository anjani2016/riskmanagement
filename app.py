import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

# Set page configuration
st.set_page_config(page_title="Advanced Monte Carlo Simulator", layout="wide")

# --- Session State Initialization ---
# This resets when the tab is closed or the page is refreshed
if 'sim_count' not in st.session_state:
    st.session_state.sim_count = 0

# --- Constants ---
MAX_TOTAL_ELEMENTS = 10_000_000 

def get_theoretical_stats(mode, trials):
    """Calculates theoretical values based on probability theory."""
    if mode == "Coin Toss":
        # For a Binomial Distribution (n=trials, p=0.5)
        theo_mean = trials * 0.5
        theo_sd = np.sqrt(trials * 0.5 * 0.5)
    else:
        # For a Dice Roll (discrete uniform 1-6)
        # Mean of one die is 3.5. Mean of 'trials' dice is still 3.5.
        theo_mean = 3.5
        # SD of one die is sqrt(((6-1+1)^2 - 1) / 12) approx 1.707
        # SD of the MEAN of 'trials' dice is (SD of one) / sqrt(trials)
        theo_sd = np.sqrt((6**2 - 1) / 12) / np.sqrt(trials)
    
    return theo_mean, theo_sd

def run_simulation(mode, trials, repeats):
    """Execution logic matching your notebook's requirements."""
    if mode == "Coin Toss":
        data = np.random.randint(0, 2, size=(repeats, trials), dtype=np.uint8)
        results = data.sum(axis=1)
    else:
        data = np.random.randint(1, 7, size=(repeats, trials), dtype=np.uint8)
        results = data.mean(axis=1)
    return results

# --- UI Setup ---
st.title("🎲 Advanced Monte Carlo Simulator")

# Definitions Section (Static Text)
with st.expander("📚 Key Definitions & Concepts"):
    st.markdown("""
    - **Mean (μ):** The average value. In a simulation, it represents the "center" of your results.
    - **Standard Deviation (σ):** A measure of how spread out the numbers are. A low SD means results are clustered closely around the mean.
    - **Theoretical Stats:** What *should* happen in a perfect world according to mathematical probability.
    - **Noise:** Random fluctuations or 'jitter' in data. In Monte Carlo, noise is represented by the variation between individual repeats.
    - **6-Sigma (6σ):** A statistical term referring to data points that are extremely far from the mean (only happens ~3.4 times per million in a normal distribution).
    """)

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    sim_mode = st.selectbox("Simulation Type", ["Coin Toss", "Dice Roll"])
    n_trials = st.number_input("Trials per repeat", min_value=1, value=10000)
    n_repeats = st.number_input("Number of repeats", min_value=1, value=1000)
    
    total_points = n_trials * n_repeats
    if total_points > MAX_TOTAL_ELEMENTS:
        st.error(f"Size too large ({total_points:,}). Limit is {MAX_TOTAL_ELEMENTS:,}.")
        run_btn = st.button("Run Simulation", disabled=True)
    else:
        run_btn = st.button("Run Simulation")

if run_btn:
    st.session_state.sim_count += 1
    results = run_simulation(sim_mode, n_trials, n_repeats)
    t_mean, t_sd = get_theoretical_stats(sim_mode, n_trials)
    
    st.header(f"Simulation #{st.session_state.sim_count} Results")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Frequency Histogram & Noise")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(results, bins=50, color='skyblue', edgecolor='black', alpha=0.7, label='Observed Data')
        
        # Add Noise Visualization (Scatter of individual results on a separate axis)
        st.pyplot(fig)
        
        # Simulation vs Theoretical Analysis
        sim_mean = np.mean(results)
        diff = sim_mean - t_mean
        range_in_sd = (np.max(results) - np.min(results)) / t_sd
        
        st.metric("Mean Deviation (Sim - Theo)", f"{diff:.4f}")
        st.metric("Results Range (in Theoretical SDs)", f"{range_in_sd:.2f}σ")

    with col2:
        st.subheader("Theoretical Sigma Table")
        # Sigma thresholds requested: 1, 1.5, 2, 2.5, 3, and 6
        sigmas = [1, 1.5, 2, 2.5, 3, 6]
        sigma_data = {
            "Sigma Level": [f"{s}σ" for s in sigmas],
            "Lower Bound": [t_mean - (s * t_sd) for s in sigmas],
            "Upper Bound": [t_mean + (s * t_sd) for s in sigmas]
        }
        st.table(pd.DataFrame(sigma_data))

        st.subheader("General Summary")
        st.write(f"**Theoretical Mean:** {t_mean:.4f}")
        st.write(f"**Theoretical SD:** {t_sd:.4f}")
        st.write(f"**Simulation Mean:** {sim_mean:.4f}")
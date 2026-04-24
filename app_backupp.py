import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Monte Carlo Simulator", layout="wide")

def run_simulation(mode, trials, repeats):
    """
    Runs the Monte Carlo simulation.
    mode: "Coin Toss" or "Dice Roll"
    trials: Number of events per simulation
    repeats: Number of times to repeat the simulation
    """
    if mode == "Coin Toss":
        # 0 = Tails, 1 = Heads. Summing gives the count of Heads.
        data = np.random.randint(0, 2, size=(repeats, trials))
        results = data.sum(axis=1)
        label = "Heads Count"
    else:
        # Dice roll 1-6.
        data = np.random.randint(1, 7, size=(repeats, trials))
        results = data.mean(axis=1)
        label = "Average Roll Value"
    
    return results, label

# --- UI Setup ---
st.title("🎲 Monte Carlo Simulation Dashboard")
st.markdown("Compare simulation outcomes side-by-side.")

# Sidebar for inputs
with st.sidebar:
    st.header("Simulation Settings")
    sim_type = st.selectbox("Select Simulation", ["Coin Toss", "Dice Roll"])
    num_trials = st.number_input("Number of Trials (per repeat)", min_value=1, value=1000, step=1000)
    num_repeats = st.number_input("Number of Repeats", min_value=1, value=100, step=100)
    run_btn = st.button("Run Simulation")

if run_btn:
    # Run the logic
    results, label = run_simulation(sim_type, num_trials, num_repeats)

    # Create side-by-side columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribution Plot")
        fig, ax = plt.subplots()
        ax.hist(results, bins=30, color='#0077b6', edgecolor='white')
        ax.set_xlabel(label)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col2:
        st.subheader("📈 Summary Statistics")
        stats = {
            "Mean Outcome": np.mean(results),
            "Standard Deviation": np.std(results),
            "Max Value": np.max(results),
            "Min Value": np.min(results)
        }
        st.table(pd.DataFrame(stats, index=["Value"]))
        
        st.write(f"**Total Data Points Processed:** {num_trials * num_repeats:,}")
else:
    st.info("Adjust the settings in the sidebar and click 'Run Simulation' to see the results.")
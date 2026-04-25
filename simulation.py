# simulation.py
import numpy as np

def run_monte_carlo(mode, trials, repeats):
    if mode == "Coin Toss":
        data = np.random.randint(0, 2, size=(repeats, trials), dtype=np.uint8)
        results = data.sum(axis=1)
    else:
        data = np.random.randint(1, 7, size=(repeats, trials), dtype=np.uint8)
        results = data.mean(axis=1)
    return results

def calculate_theory(mode, trials):
    if mode == "Coin Toss":
        t_mean = trials * 0.5
        t_sd = np.sqrt(trials * 0.5 * 0.5)
    else:
        t_mean = 3.5
        t_sd = np.sqrt((6**2 - 1) / 12) / np.sqrt(trials)
    return t_mean, t_sd
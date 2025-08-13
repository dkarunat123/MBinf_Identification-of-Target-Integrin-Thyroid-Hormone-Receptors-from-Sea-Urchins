# calculate_kd_from_dg.py

import math

# Constants
R = 0.001987  # kcal·mol^-1·K^-1
T = 298.15    # Kelvin (25°C)

# Ask user for ΔG
dg_input = input("Enter ΔG in kcal/mol: ").strip()
try:
    dg = float(dg_input)
except ValueError:
    print("Error: Please enter a valid number for ΔG.")
    exit(1)

# Calculate Kd
RT = R * T
kd_molar = math.exp(dg / RT)  # M
kd_micromolar = kd_molar * 1e6  # μM

# Output
print(f"\nΔG = {dg:.2f} kcal/mol")
print(f"Kd  = {kd_molar:.3e} M")
print(f"Kd  = {kd_micromolar:.3f} μM")

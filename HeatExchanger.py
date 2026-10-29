
import math

# Given process data
Q = 250800.0            # Heat duty, W
dt1 = 40.0              # Terminal temperature difference, K
dt2 = 30.0              # Terminal temperature difference, K
F = 0.95                # Illustrative LMTD correction factor

# Tube dimensions
do = 0.01905            # Outside diameter, m
di = 0.01575            # Inside diameter, m
L = 4.0                 # Tube length, m
kw = 16.0               # Illustrative tube-wall conductivity, W/m.K

# Illustrative fouling resistances, m2.K/W
Rfo = 0.0002
Rfi = 0.0002

# Replace these with calculated values from your design.
# hs must be calculated using the Bell-Delaware method.
hs = 1000.0             # Illustrative corrected shell-side h, W/m2.K
hi = 3000.0             # Illustrative tube-side h, W/m2.K

# LMTD
lmtd = (dt1 - dt2) / math.log(dt1 / dt2)
dtm = F * lmtd

# Overall coefficient, based on outside tube area
resistance = (
    1.0 / hs
    + Rfo
    + do * math.log(do / di) / (2.0 * kw)
    + (do / di) * (1.0 / hi + Rfi)
)
U_calculated = 1.0 / resistance

# Fixed-point iteration with relaxation
U_guess = float(input("Enter assumed overall heat transfer coefficient U (W/m²·K): "))
tolerance = 0.001
relaxation = 0.5
max_iterations = 100

print(f"LMTD = {lmtd:.3f} K")
print(f"Corrected mean temperature difference = {dtm:.3f} K")
print()
print("Iter | U assumed | U calculated | Area (m2) | Error (%)")

for iteration in range(1, max_iterations + 1):
    area = Q / (U_guess * dtm)
    error = abs(U_calculated - U_guess) / U_calculated * 100

    print(
        f"{iteration:4d} | {U_guess:9.2f} | "
        f"{U_calculated:12.2f} | {area:9.3f} | "
        f"{error:8.3f}"
    )

    if error < tolerance:
        break

    U_guess = (
        relaxation * U_calculated
        + (1.0 - relaxation) * U_guess
    )

print("\nFinal converged overall coefficient:",
      round(U_guess, 2), "W/m2.K")

print("Required area:",
      round(Q / (U_guess * dtm), 3), "m2")

print("Approximate tube count:",
      math.ceil(Q / (U_guess * dtm) / (math.pi * do * L)))

import numpy as np

print("This problem uses Particle Swarm Optimization to find")
print("the values of R1, R5, R8, and V3 that satisfy the condition:")
print("Power delivered by V1 = 10% of power delivered by V3")
print("--------------------------------------------------------------")

num_variables = 4
lower_bounds = np.zeros(4)  # Lower bounds
upper_bounds = np.array([50, 150, 250, 18]) # Upper bounds
num_particles = 40
max_iterations = 100

# PSO Parameters
inertia_weight = 0.7
cognitive_coeff = 1.5
social_coeff = 1.5

def objective_function(params):
    R1, R5, R8, V3 = params
    R2, R3, R4 = 100, 47, 32
    R6, R7 = 22, 132
    V1, V2 = 8, 12

    resistance_matrix = np.array([
        [R1 + R2 + R3, -R2, 0],
        [-R2, R2 + R4 + R5 + R6, -R6],
        [0, -R6, R6 + R7 + R8]
    ])
    voltage_vector = np.array([V1, -V2, -V3])
    currents = np.linalg.solve(resistance_matrix, voltage_vector)

    power_V1 = V1 * currents[0]
    power_V3 = V3 * currents[2]
    error = abs(power_V1 - 0.1 * power_V3)
    return error, currents, power_V1, power_V3

positions = np.random.rand(num_particles, num_variables) * (upper_bounds - lower_bounds) + lower_bounds
velocities = np.zeros((num_particles, num_variables))
personal_best_positions = positions.copy()
personal_best_costs = np.array([objective_function(p)[0] for p in positions])
global_best_index = np.argmin(personal_best_costs)
global_best_position = personal_best_positions[global_best_index].copy()
global_best_cost = personal_best_costs[global_best_index]

# PSO Main Loop
for iteration in range(max_iterations):
    for i in range(num_particles):
        r1 = np.random.rand(num_variables)
        r2 = np.random.rand(num_variables)

        # Velocity and position update
        velocities[i] = (
            inertia_weight * velocities[i]
            + cognitive_coeff * r1 * (personal_best_positions[i] - positions[i])
            + social_coeff * r2 * (global_best_position - positions[i])
        )
        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], lower_bounds, upper_bounds)

        # Evaluate new position
        cost, *_ = objective_function(positions[i])
        if cost < personal_best_costs[i]:
            personal_best_costs[i] = cost
            personal_best_positions[i] = positions[i]
            if cost < global_best_cost:
                global_best_cost = cost
                global_best_position = positions[i]

    print(f"Iteration {iteration+1}: Best Cost = {global_best_cost:.6f}")

R1, R5, R8, V3 = global_best_position
_, mesh_currents, power_V1, power_V3 = objective_function(global_best_position)

print("\n--- Optimized Circuit Values ---")
print(f"R1 = {R1:.2f} ohms")
print(f"R5 = {R5:.2f} ohms")
print(f"R8 = {R8:.2f} ohms")
print(f"V3 = {V3:.2f} volts")

print("\n--- Mesh Currents ---")
for i, current in enumerate(mesh_currents, start=1):
    print(f"I{i} = {current:.4f} A")

print("\n--- Power ---")
print(f"Power from V1 = {power_V1:.4f} W")
print(f"Power from V3 = {power_V3:.4f} W")
print(f"Objective Function Value = {global_best_cost:.6f}")

input("Press Enter to exit...")

import numpy as np
#Some functions

num_variables = 40
lower_bounds = np.array([36, 36, 60, 80, 47, 68, 110, 135, 135, 130, 94, 94, 125, 125, 125, 125, 220, 220, 242, 242, 254, 254, 254, 254, 254, 254, 10, 10, 10, 47, 60, 60, 60, 90, 90, 90, 25, 25, 25, 242])  # Lower bounds
upper_bounds = np.array([114, 114, 120, 190, 97, 140, 300, 300, 300, 300, 375, 375, 500, 500, 500, 500, 500, 500, 550, 550, 550, 550, 550, 550, 550, 550, 150, 150, 150, 97, 190, 190, 190, 200, 200, 200, 110, 110, 110, 550])# Upper bounds
num_particles = 500
max_iterations = 100
power_demand = 10490
system_tolerance = 0.000001 * power_demand
accepted_cost = 1_50_000

#Quantum Mechanical Constants
h = 6.62607015e-34  # Planck's constant
h_bar = h / (2 * np.pi)  # Reduced Planck's constant
c_mps = 299792458  # Speed of light in m/s
qt_beta = 1.5 #Decay constant for quantum tunneling
qt_lambda = 0.75 #Wavelength for quantum tunneling
qt_L = 20 #Maximum tunneling range

# Objective coefficients
a = np.array([0.00690, 0.00690, 0.02028, 0.00942, 0.01140, 0.01142, 0.00357, 0.00492, 0.00573, 0.00605, 0.00515, 0.00569, 0.00421, 0.00752, 0.00752, 0.00752, 0.00313, 0.00313, 0.00313, 0.00313, 0.00298, 0.00298, 0.00284, 0.00284, 0.00277, 0.00277, 0.52124, 0.52124, 0.52124, 0.01140, 0.00160, 0.00160, 0.00160, 0.00010, 0.00010, 0.00010, 0.01610, 0.01610, 0.01610, 0.00313])
b = np.array([6.73, 6.73, 7.07, 8.18, 5.35, 8.05, 8.03, 6.99, 6.60, 12.9, 12.9, 12.8, 12.5, 8.84, 8.84, 8.84, 7.97, 7.95, 7.97, 7.97, 6.63, 6.63, 6.66, 6.66, 7.10, 7.10, 3.33, 3.33, 3.33, 5.35, 6.43, 6.43, 6.43, 8.95, 8.62, 8.62, 5.88, 5.88, 5.88, 7.97])
c = np.array([94.705, 94.705, 309.54, 369.03, 148.89, 222.33, 287.71, 391.98, 455.76, 722.82, 635.20, 654.69, 913.40, 1760.4, 1760.4, 1760.4, 647.85, 649.69, 647.83, 647.81, 785.96, 785.96, 794.53, 794.53, 801.32, 801.32, 1055.1, 1055.1, 1055.1, 148.89, 222.92, 222.92, 222.92, 107.87, 116.58, 116.58, 307.45, 307.45, 307.45, 647.83])
e = np.array([100, 100, 100, 150, 120, 100, 200, 200, 200, 200, 200, 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 120, 120, 120, 120, 150, 150, 150, 200, 200, 200, 80, 80, 80, 300])
f = np.array([0.084, 0.084, 0.084, 0.063, 0.077, 0.084, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.077, 0.077, 0.077, 0.077, 0.063, 0.063, 0.063, 0.042, 0.042, 0.042, 0.098, 0.098, 0.098, 0.035])
g = np.array([abs(e[i]*np.sin(f[i]*(lower_bounds[i]-upper_bounds[i]))) for i in range(num_variables)])    

get_cognitive_coeff = lambda social_coeff: np.sqrt(1 - social_coeff)    

def objective_function(params):
    cost_list = a * params**2 + b * params + c + g
    total_cost = sum(cost_list)
    error = sum(params) - power_demand
    penalty = abs(error) * 1e5 if abs(error) > system_tolerance else 0
    return total_cost, error, penalty

def get_coefficients(i):
        social_coeff, cognitive_coeff = coefficients[i]
        distance_to_global_best = np.linalg.norm((positions[i] - positions[global_best_index]) + mean_position)
        social_coeff = min(1, 1 / (distance_to_global_best + 1e-9))
        cognitive_coeff = get_cognitive_coeff(social_coeff)
        coefficients[i] = np.array([social_coeff, cognitive_coeff])
        return social_coeff, cognitive_coeff

# PSO Parameters
inertia_weight = 0.8
social_coeff = 1 / np.sqrt(2)
cognitive_coeff = get_cognitive_coeff(social_coeff)
velocity_cap = upper_bounds - lower_bounds

positions = np.random.rand(num_particles, num_variables) * (upper_bounds - lower_bounds) + lower_bounds
velocities = np.zeros((num_particles, num_variables))
coefficients = np.ones([num_particles, 2]) * np.array([social_coeff, cognitive_coeff])

personal_best_positions = positions.copy()
personal_best_costs = []
personal_best_errors = []

for p in positions:
    cost, error, penalty = objective_function(p)
    personal_best_costs.append(cost + penalty)
    personal_best_errors.append(error)

global_best_index = np.argmin(personal_best_costs)
global_best_error_index = np.argmin(personal_best_errors)

global_best_position = personal_best_positions[global_best_index].copy()
global_best_cost = personal_best_costs[global_best_index].copy()
global_best_error = personal_best_errors[global_best_error_index].copy()
sf = False #Solution Found Flag

print("Initial cost:", global_best_cost , "Initial error:", global_best_error ,'\n')

# PSO Main Loop
run_count = 1
while not sf:
    print(f"\nStarting PSO. Run {run_count}\n")
    for iteration in range(max_iterations):
        for i in range(num_particles):
            r1 = np.random.rand(num_variables)
            r2 = np.random.rand(num_variables)
            sign = np.random.choice([-1, 1]) 
            u = np.clip(np.random.uniform(0, 1), 1e-10, 1 - 1e-10)
            mean_position = np.mean(positions, axis=0)
            social_coeff, cognitive_coeff = get_coefficients(i)

            # Velocity and position update
            velocities[i] = (
                inertia_weight * velocities[i]
                + cognitive_coeff * r1 * (personal_best_positions[i] - positions[i])
                + social_coeff * r2 * (global_best_position - positions[i])
                + (mean_position - positions[i]) * -np.log(u)
            )

            # Update position
            positions[i] += np.clip(velocities[i], -velocity_cap, velocity_cap) 

            #Tunneling effect
            if abs(personal_best_errors[i]) > 3 * system_tolerance and abs(personal_best_errors[i]) < 9 * system_tolerance:
                qt_q = sign * qt_L * -np.log(u)
                positions[i] += qt_lambda + qt_q * r1 * np.exp(-qt_beta) * (global_best_position - positions[i])
            positions[i] = np.clip(positions[i], lower_bounds, upper_bounds)

            cost, error, penalty = objective_function(positions[i])
            true_cost = cost + penalty
            
            # Update personal best
            if true_cost < personal_best_costs[i] or (true_cost == personal_best_costs[i] and error < personal_best_errors[i]):
                personal_best_positions[i] = positions[i].copy()
                personal_best_costs[i] = true_cost
                personal_best_errors[i] = error
                if true_cost < global_best_cost or (true_cost == global_best_cost and error < global_best_error):
                    global_best_position = positions[i].copy()
                    global_best_cost = true_cost
                    global_best_index = i
                    if error < system_tolerance and global_best_cost < accepted_cost:
                        global_best_error = error
                        global_best_error_index = i
                        print(f"\nSolution found at iteration {iteration+1} of run {run_count} with error {error:.6f}")
                        sf = True
                        break         
        if sf == True:
            break
        else:
            print(f"Iteration {iteration+1}: Cost = {true_cost:.6f} Error = {error:.6f}")
    run_count += 1
    if run_count > 10:
        print("Maximum run count reached without finding a solution.")
        break

print(f"Final Position: \n{positions[global_best_index]}")
print((f"Final Error: {personal_best_errors[global_best_index]:.6f}"))
print(f'Final power delivery: {sum(positions[global_best_index]):.6f}')
print(f"Final Cost: {personal_best_costs[global_best_index]:.6f}")
if sf == True:
    print("Final Best Position Found!\n")
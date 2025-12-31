# Overview
This python program implements Particle Swarm Optimization (PSO) algorithm to
solve for optimal component values in an electric circuit, given the following conditions:  
- Some component values are predetermined
- Some set behavior is expected from the circuit

In an update, a slightly modified PSO is used to tackle the problem of Economic Dipatch in a 40 unit 
system.

# Terminology
particle(s) = List of _num_variable_ elements  
best (historical) position = Position resulting in the least error from _objective_function_  
num_variable = Number of variables in the circuit to be solved  
num_particles = Number of _particles_ in the sample space  
max_iterations = Number of iterations PSO will update for  
positions = List of all _particles_ in space  
velocities = Velocity of each _particle_ in positions  
personal_best_positions = List of the _best historical position_ for each _particle_ in _positions_  
personal_best_costs = List of the least error computed by _objective_function_ for each _particle_ in _positions_ in any iteration  
global_best_index = Index of the least value in _personal_best_costs_  
global_best_position = _Particle_ in _positions_ that resulted in the least value in _personal_best_costs_  
global_best_cost = Least error value stored in _personal_best_costs_

# Program Flow (Genereal Outline)
The program initializes a random space of n _particles_ (n = _num_particles_), each
consisting of _num_variables_ elements, representing possible optimal solutions to our
problem, and creates a list of velocities for all _particles_, initially zero. 
Given the initialized random space, the _personal_best_costs_ list is populated with the current error value
computed by feeding each _particle_ into _objective_function_, and the _global_best_position_ is
found by taking the minimum error value computed using any _particle_ in the random space.

The _objective_function_ takes a list of variables, namely [R1, R5, R8, V3] provided by
the main PSO loop, calculates currents formed in the circuit and returns a list of values,
namely [error, currents, power_V1, power_V3], where error is the difference in _power_V1_
and 0.1 * _power_V3_.

The PSO algorithm loops for _max_iterations_ for each _particle_ in _positions_, updating
_velocities_ and _positions_ which defines the _particle_'s updated position in the sample space. For any _particle_, if the 
error computed in the ongoing iteration is less than the least error computed in any previous iteration, 
the index corresponding to that particle is updated with the computed error in _personal_best_costs_. 
If the computed error is also less than the _global_best_cost_, _global_best_cost_ is updated to the current error
value and _global_best_position_ is updated to the current _particle_. The iteration number and
best cost computed in each iteration are printed on the screen.

After _max_iterations_, the most optimal values are printed out by evaluating
_objective_function_ over the _global_best_position_.

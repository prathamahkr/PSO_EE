% Solving for optimal circuit component values using manual PSO
% --------------------------------------------------------------

clear; clc; close all; format compact;

disp('This problem uses Particle Swarm Optimization to find')
disp('the values of R1, R5, R8, and V3 that satisfy the condition:')
disp('Power delivered by V1 = 10% of power delivered by V3')
disp('--------------------------------------------------------------')

% Problem Setup
nVar = 4;                          % [R1, R5, R8, V3]
lb = [10, 90, 160, 12];            % Lower bounds
ub = [50, 150, 250, 18];           % Upper bounds
nParticles = 30;                  
maxIters = 100;                   

% PSO Parameters
w = 0.7; c1 = 1.5; c2 = 1.5;

% Initialize Particles
pos = rand(nParticles, nVar) .* (ub - lb) + lb;
vel = zeros(nParticles, nVar);
best_pos = pos;
best_cost = arrayfun(@(i) objective(pos(i,:)), 1:nParticles)';
[global_best_cost, idx] = min(best_cost);
global_best_pos = best_pos(idx, :);

% PSO Loop
for iter = 1:maxIters
    for i = 1:nParticles
        vel(i,:) = w * vel(i,:) ...
                 + c1 * rand(1,nVar) .* (best_pos(i,:) - pos(i,:)) ...
                 + c2 * rand(1,nVar) .* (global_best_pos - pos(i,:));
        pos(i,:) = pos(i,:) + vel(i,:);
        pos(i,:) = max(min(pos(i,:), ub), lb);

        cost = objective(pos(i,:));
        if cost < best_cost(i)
            best_cost(i) = cost;
            best_pos(i,:) = pos(i,:);
            if cost < global_best_cost
                global_best_cost = cost;
                global_best_pos = pos(i,:);
            end
        end
    end
    fprintf('Iteration %d: Best Cost = %.6f\n', iter, global_best_cost);
end

% Final Output
[R1, R5, R8, V3] = deal(global_best_pos(1), global_best_pos(2), global_best_pos(3), global_best_pos(4));
[~, I, PV1, PV3] = objective(global_best_pos);

disp(' ')
disp('--- Optimized Circuit Values ---')
fprintf('R1 = %.2f ohms\n', R1);
fprintf('R5 = %.2f ohms\n', R5);
fprintf('R8 = %.2f ohms\n', R8);
fprintf('V3 = %.2f volts\n', V3);

disp(' ')
disp('--- Mesh Currents ---')
fprintf('I1 = %.4f A\n', I(1));
fprintf('I2 = %.4f A\n', I(2));
fprintf('I3 = %.4f A\n', I(3));

disp(' ')
disp('--- Power ---')
fprintf('PV1 = %.4f W\n', PV1);
fprintf('PV3 = %.4f W\n', PV3);
fprintf('Objective Value = %.6f\n', global_best_cost);

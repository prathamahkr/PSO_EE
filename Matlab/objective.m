function [error, I, PV1, PV3] = objective(x)
    R2 = 100; R3 = 47; R4 = 32;
    R6 = 22; R7 = 132;
    V1 = 8; V2 = 12;

    R1 = x(1); R5 = x(2); R8 = x(3); V3 = x(4);

    A = [R1+R3+R2, -R2,        0;
        -R2, R2+R4+R5+R6, -R6;
         0, -R6, R6+R7+R8];

    B = [V1; -V2; -V3];
    I = A \ B;
    PV1 = V1 * I(1);
    PV3 = V3 * I(3);
    error = abs(PV1 - 0.1 * PV3);
end

clc; clear; close all

% Initial conditions, constants, and variables
dt = 0.01;          % Time step (s)
x0 = 0;             % Initial position on the X-axis (m)
z0 = 0;             % Initial height from the ground (m)
h_i = 978;          % Launch point altitude (m)
phi0 = 85;          % Initial flight path angle (degrees)
m_i = 22.3;         % Initial mass of the rocket (kg)
fuel_i = 4.12;      % Initial mass of the fuel (kg)
isp = 189.4;        % Specific impulse (s)
d = 0.144;          % Diameter of the rocket (m)
area = pi*d^2/4;    % Cross-sectional area of the rocket (m^2)
v0 = 1;             % Initial composite velocity value (m/s)
g = 9.801;          % Gravitational acceleration (m/s^2)

% Import thrust data vs time data and interpolate 
thrustData = readtable('thrustTime.csv');
finalThrustTime = max(thrustData.Time);     % Final time value of the thrust [s]
thrustDataCount = finalThrustTime/dt;       % Number of data points for interpolation
interp_time = linspace(0, finalThrustTime, thrustDataCount);
interp_thrust = interp1(thrustData.Time, thrustData.Thrust, interp_time, 'linear');
m_dot = interp_thrust / (isp * g);          % Mass flow rate (kg/s)

% Import drag coefficient vs mach number data and fit it.
cdMach = readtable('cdMach.csv');
cdFit = cdMach.CD;
machFit = cdMach.Mach;
[fitresult, gof] = createFit(machFit, cdFit);

% Assign initial values to variables
x = x0;
z = z0;
vx = v0 * cosd(phi0);
vz = v0 * sind(phi0);
h = h_i + z;
phi = phi0;

% Predefine storage lists 
list_x = [x];
list_z = [z];
list_vx = [vx];
list_vz = [vz];
list_phi = [phi];
list_pdx = [0];
mach_list = [0];

s = 1; % Loop counter
% Run the loop until apogee (vertical speed equals zero)
while vz > 0 
    h = h_i + z;

    % Thrust conditions
    if s <= thrustDataCount
        thrust = interp_thrust(s);
    else
        thrust = 0;
    end

    % Compute changes in fuel and mass
    if s <= thrustDataCount
        fuel_i = fuel_i - (m_dot(s) * dt);
        m = m_i - (m_dot(s) * dt);
    end

    % Calculate temperature, air density, and speed of sound using a predefined function
    [temperature, rho, a] = atmosphere_conditions(h);  

    % Compute resultant velocity and corresponding Mach number
    v = sqrt(vx^2 + vz^2);
    mach = v / a;
    
    % Compute drag coefficient based on fitted data
    Cd = fitresult(mach);

    % Compute aerodynamic forces
    p_dyn = 0.5 * rho * v^2;                % Dynamic pressure [Pa]
    F_drag = p_dyn * Cd * area;             % Drag force [N]
    F_X = (thrust - F_drag) * cosd(phi);    % Net force along the X-axis [N]
    F_Z = (thrust - F_drag) * sind(phi);    % Net force along the Z-axis [N]

    % Update velocity and position values
    vx = vx + (F_X / m) * dt;
    x = x + vx * dt;
    vz = vz - g * dt + (F_Z / m) * dt;
    z = z + vz * dt;
    phi = atand(vz / vx);

    % Update lists
    list_x(end + 1) = x;
    list_z(end + 1) = z;
    list_vx(end + 1) = vx;
    list_vz(end + 1) = vz;
    mach_list(end + 1) = mach;
    list_pdx(end + 1) = p_dyn * cosd(phi);
    list_phi(end + 1) = phi;

    % Increment loop counter
    s = s + 1;
end

% Simulation results
max_mach = max(mach_list);
range = list_x(end);
altitude = list_z(end);
final_velocity = sqrt(list_vx(end)^2 + list_vz(end)^2);
final_mach = mach_list(end);
apogee_time = s * dt;

% Create time series for graphing up to apogee
total_time = linspace(0, apogee_time, s-1); 

% Plot results using subplots
figure;
set(0, 'DefaultLineLineWidth', 2)

subplot(3, 2, 1);
plot(list_x, list_z);
xlabel('Range [m]');
ylabel('Altitude [m]');
grid on;
title('Range vs Altitude');

subplot(3, 2, 2);
plot(total_time, list_phi(1:s-1));
xlabel('Time [s]');
ylabel('Flight Angle [°]');
grid on;
title('Time vs Flight Angle');

subplot(3, 2, 3);
plot(total_time, mach_list(1:s-1));
xlabel('Time [s]');
ylabel('Mach Number');
grid on;
title('Time vs Mach Number');

subplot(3, 2, 4);
plot(total_time, list_pdx(1:s-1));
xlabel('Time [s]');
ylabel('Dynamic Pressure [Pa]');
grid on;
title('Time vs Dynamic Pressure');

subplot(3, 2, 5);
plot(total_time, list_vz(1:s-1));
xlabel('Time [s]');
ylabel('Vertical Climb Speed [m/s]');
grid on;
title('Time vs Vertical Climb Speed');

% Plot fit with data
subplot(3, 2, 6)
h = plot(fitresult, machFit, cdFit);
legend(h, 'cd vs. mach', 'Fitted Curve', 'Location', 'NorthEast', 'Interpreter', 'none');
xlabel('mach', 'Interpreter', 'none');
ylabel('cd', 'Interpreter', 'none');
grid on

% Function to define atmospheric conditions
function [temperature, rho, a] = atmosphere_conditions(h)
    % Formulas for atmospheric conditions
    temperature = 15.04 - 0.00649 * h;                         % Air temperature (C)
    pressure = ((temperature + 273.1) / 288.08)^5.256 * 101.29;% Air pressure (Pa)
    rho = pressure / (0.2869 * (temperature + 273.1));         % Air density (kg/m^3)
    a = (1.4 * 287.05 * (temperature + 273.15))^0.5;           % Speed of sound (m/s)
end

% Perform curve fitting for Cd vs Mach data
function [fitresult, gof] = createFit(machFit, cdFit)
%CREATEFIT(MACHFIT,CDFIT)
%  Create a fit.
%  Data for 'cdMachFit' fit:
%      X Input: machFit
%      Y Output: cdFit
%  Output:
%      fitresult : a fit object representing the fit.
%      gof : structure with goodness-of-fit info.

% Prepare data for fitting
[xData, yData] = prepareCurveData(machFit, cdFit);

% Set up fit type and options
ft = fittype('fourier8');
opts = fitoptions('Method', 'NonlinearLeastSquares');
opts.Display = 'Off';
opts.StartPoint = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2.10845144536228];

% Fit model to data
[fitresult, gof] = fit(xData, yData, ft, opts);
end

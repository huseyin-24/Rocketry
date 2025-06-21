## Objective 
Trajectory of any rocket is determined by external forces and its initial conditions. Assuming that the atmosphere is modelled mathematiclly and 
all other factors (thrust, gravity, mass change and drag coefficient with respect to time) are known, the trajectory can be estimated using basic mechanics laws. This simulation
enables to estimate the altitude, horizontal distance, flight angle, speed dynamic pressure during the fligth. 

<p align="center"><img src="https://github.com/user-attachments/assets/7423f8c5-592f-4028-8cbb-71497759e51d" /></p>
<p align="center">Free Body Diagram Used in Simulation (including velocity).</p><p align="center">Ref: http://www.braeunig.us/space/aerodyn_wip.htm </p>

Flight is simulated assuming angle of attack (angle represented as alpha in the figure above) is always zero. The python script for the simulation animates the fligth visually in addition to calculation of variables of each time step from at the very beginning of the flight to the apogee.  
After calculating all simulation variables, the animation is generated using the animation classes of matplotlib: 


https://github.com/user-attachments/assets/047c5e69-ac5e-45d0-be34-f5981eb35ea9


Other simulation results are as follows: 

<p align="center"><img src="https://github.com/user-attachments/assets/7b9d64a1-a3ea-432d-965c-25eb44f36bd7" /></p>


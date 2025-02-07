## Structural Analysis  
The rocket is exposed to largest forces when the maximum acceleration occurs. At that moment, inertia force is maximum, and external forces are thrust and aerodynamic forces. Considering aerodynamic forces are proportional to the second power of speed and maximum acceleration instant does not overlap large speed instances, the analysis is run with thrust, gravity and inertial forces.  
To model the case explained above, static structural analysis within Ansys Mechanical is used.  
- Geometric Modifications: Since the CAD model contains each detail about the rocket, unnecessary parts, such as elastic bands, servo motor, eyebolts and electronic hardware, are removed in FEA analysis. Also, bolts are excluded for the reason explained in ‘’contacts part’’ below.  
- Mesh: Due to the node/element limit of 125K of Ansys Mechanical Student Version, 116K nodes and 54K elements are assigned to solid bodies. Note that average element size is 30mm. Also, aluminum alloy, carbon fiber and fiber glass materials are assigned to flexible bodies accordingly.
- Boundary Conditions: External force is thrust of 2300N, and inertial relief is activated for static equilibrium of the assembly. Since a dynamic case is structurally analyzed using static analysis, balancing the external thrust force with inertial relief is the proper way of running the simulation, instead of constraining the assembly with fixed/displacement contacts. Additionally, gravity is included.
Since eyebolts, parachute assembly, payload, servomotor and hardware are excluded from simulation, their inertial effects are simulated by defining point masses of corresponding masses to their locations. 
- Contacts: All contacts are assumed as bonded contacts, including bolt connections. Since bolts are cold forged steel components, they are unlikely to yield. Also, the overall stress magnitudes are supposed to be observed. This simplified method is reasonable especially considering node/element limit.
- Solution Method and Options: Nonlinearities, inertial relief, weak springs and large deflections are activated while other details of the solver are held at their default options.
- Results and Discussion: As one can see in Figure 1., maximum von-Mises equivalent stress turns out to be 10.4 MPa throughout the whole assembly. Considering the yield limits of materials used in the rocket are in 3 orders of magnitude, these stress values are significantly below critical values. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/64e3a5e9-e902-4357-be5f-c7f99b17f52c" width="402" /></p>
<p align="center">Figure 1. Equivalent von-Mises Stress Response of the Rocket</p>


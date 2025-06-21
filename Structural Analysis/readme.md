# Structural Analysis  
## Bolt Selection
Instead of more, four bolts per centering ring/bulkhead are used to join them with rocket body because each
bolt increases total drag coefficient of the rocket. Bolt diameters and grade are determined with the help of both
Ansys simulations and hand calculations. After calculations and simulations for a couple of grade&diameter
combinations, final bolts are chosen as grade 8.8 M5. Since the bolts joining motor bulkhead and rocket body are
exposed to the highest forces, the analysis is based on motor bulkhead as follows:
The bolts joining motor bulkhead and body are the ones transferring total thrust from the motor to the rocket.
They transmit thrust of 2440N at the instance of maximum thrust; hence, each bolt is carrying 610N to rocket
body.
### Numerical Analysis
Ansys simulation is prepared with bolts, a portion of body and dummy centering ring (though motor bulkhead
is bulky at the center, ring geometry represents it well for analysis purposes) as shown in Fig. 11 Here are some
key features in the simulation:
- Total thrust of 2440N is applied over the cross section of body. 
- Centering ring is fixed using 3-2-1 method to prevent over constrained model. 
- Internal surface of the ring is exposed to cylindrical support since no deformation is expected in that
direction. 
- Threaded portion of the ring and bolts are bonded since they behave like bonded connection when the
bolts are tightened. 
- Pretension of 1000N is applied for each bolt to simulate the effect of preload. 
- Frictional contacts are defined properly between bolt shanks&heads and related surfaces of the rocket
body. 
- Mesh is refined at contact points for contacts to work properly and to capture stress distribution well. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/bae32aa3-5f2f-4e82-bf8a-c40ded91ca45" width="500" /></p>
<p align="center">Figure 1. Boundary Conditions of Analysis</p>

Maximum equivalent von-Mises stress results are 112, 17.1 and 67.3 MPa for bolts, rocket body and centering
rings, respectively. Considering yield strength of each part, bolts (640 MPa yield strength of grade 8.8 bolts), body
(no available yield strength information; however, 2000 MPa ultimate tensile strength) and centering (276 MPa
yield strength) turn out to have 5.71, 117, 4.11 factors of safety. Additionally, sticking regions in contact results
also indicate that the pretension definitions of bolts work properly.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f38f37b2-b25f-402e-9c89-50472270ef6c" width="500" /></p>
<p align="center">Figure 2. Equivalent Stress Response for Body, Centering Ring, Bolt and Overall Model</p>

### Analytical Analysis
In addition to numerical simulation, equivalent von-Mises stress is investigated by hand calculation with
analytical formulas. For each bolt force of 𝐹 =
𝐹𝑡𝑜𝑡𝑎𝑙/4
= 610𝑁 and fixed boundary condition over threads can be
seen in Fig. 3

<p align="center">
  <img src="https://github.com/user-attachments/assets/371deced-fb5a-4f04-9bc2-7236ea05b981" width="500" /></p>
<p align="center">Figure 3. Boundary Conditions of Analytical Calculation</p>

The stress state of a cylindrical bar with a cross-sectional area of 19.6𝑚𝑚2
(cylindrical crosssectional area of M5 bolt shank) is analyzed under a bending moment of 𝑀 = 𝐹 ∗ 𝑑 = 610𝑁𝑚𝑚 (since the force
is assumed to be uniform and can be idealized as concentrated point force at where 𝑑=1 mm away), a transverse shear
force of 𝐹𝑠 = 𝐹 = 610𝑁, and an axial pretension load of 𝐹𝑝𝑡 = 1000𝑁. The second moment of area was calculated
as, yielding approximately 𝐼 = 30.7𝑚𝑚⁴
. The bending normal stress was found using the formula 𝜎<sub>𝑏</sub> =
𝑀 ∗ 𝑐 / 𝐼
= 49.7𝑀𝑃𝑎, where 𝑐 = 2.5𝑚𝑚 is the distance from the neutral axis, leading to. The shear stress due to
transverse loading was calculated by 𝜏𝑠 =
F<sub>s</sub>/𝐴
= 31.1𝑀𝑃𝑎. Similarly, the axial stress due to pretension was
calculated by 𝜎<sub>pt</sub> =
F<sub>pt</sub>/A 
= 50.9𝑀𝑃𝑎. The total normal stress then became the sum of bending and axial stresses,
calculated as 𝜎<sub>a</sub> = 𝜎<sub>𝑏</sub> + 𝜎<sub>pt</sub> = 100.6𝑀𝑃𝑎. The von Mises stress under combined normal and shear stresses was
calculated using
𝜎<sub>eqv</sub> formula
resulting in a final von Mises stress of approximately 114.1 MPa.
Nevertheless, despite the minute discrepancy of about 2 MPa between numerical and analytical results, both
methods result in reliable factors of safety values and bolts are determined as M5 with proper thread and shank
lengths.

## Overall Structural Analysis

The rocket is exposed to largest forces when the maximum acceleration occurs. At that moment, inertia force
is maximum, and the external forces are thrust and aerodynamic forces. Considering aerodynamic forces are
proportional to second power of speed of the rocket and maximum acceleration instant does not overlap large
speed instances, the analysis is run with only thrust and inertial forces.  
To model the case explained above, static structural analysis within Ansys Mechanical is used.  
- Geometric Modifications: Since the CAD model contains each detail about the rocket, unnecessary parts, such
as elastic bands, servo motor, eyebolts and electronic hardware, are removed in FEA analysis. Also, bolts are
excluded for the reason explained in ‘’contacts part’’ below.
- Mesh & Materials: 985K nodes and 541K elements are assigned to solid bodies. Also, aluminum alloy, carbon
fiber and fiber glass materials are assigned to flexible bodies accordingly.
- Boundary Conditions: External force is thrust of 2440N, and inertial relief is activated for static equilibrium
of the assembly. Since a dynamic case is structurally analyzed using static analysis, balancing the external thrust
force with inertial relief is the proper way of running the simulation, instead of constraining the assembly with
fixed/displacement contacts. Additionally, gravity is included. An overview of boundary conditions is visualized
in Figure 4.

<p align="center">
  <img src="https://github.com/user-attachments/assets/40be3787-aa3d-4aa9-b95a-bca0171a8264" width="500" /></p>
<p align="center">Figure 4. Boundary conditions and mass replacements inside rocket at maximum thrust instance.</p>

Since eyebolts, parachute assembly, payload, servomotor and hardware are excluded from simulation, their
inertial effects are simulated by defining distributed masses to their locations.  
- Contacts: All contacts are assumed as bonded contacts, including bolt connections. Since bolts are examined
in another section to design bolted connections with proper contact and pretension definitions, this analysis
excludes concentrated stress distribution near contacts. This simplified method is reasonable to see stress general
stress response of each part separately.
- Solution Method and Options: Nonlinearities, inertial relief and weak springs are activated while other details
of the solver are held at their default options.
Results and Discussion: As one can see in Figure 21, maximum von-Mises equivalent stress for the whole
assembly turns out to be 10.1 MPa at motor bulkhead ex expected. Maximum observed equivalent stress values
for motor bulkhead, lower body, upper body, nose cone, coupler are 10.1, 1.64, 3.92, 0.177 and 1.83 MPa,
respectively. Considering the yield limits of materials used in the rocket are in 3 orders of magnitude, these stress
values are significantly below yield limits and correspond to at least two orders of magnitude of safety factors.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5e8e256e-22f8-455f-90d0-6e9f401ae180" width="500" /></p>
<p align="center">Figure 5. Stress distribution of a) motor bulkhead, b) lower body, c) nose cone and d) upper body.</p>






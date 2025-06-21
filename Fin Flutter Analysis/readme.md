## Objective
Since the fins of a rocket is excited by the surrounding air during its flight, they are dynamiclly loaded by the air modelues. This dynamic loading requires the fins to be 
designed according to its flutter speed, which is the speed resulting in natural frequency excititaion. Therefore, it is a must to analyze and compare the fin flutter speed 
and expected rocket speed during its flight. 

### Here is the fin flutter analysis part submitted for IREC2025 competition:
#### Analytical Approach 
According to Ref. [1], fin flutter speed is governed by an equation where geometric dimension of fins, atmospheric pressure, speed of sound and shear modulus of fin material appear. Since geometric dimensions and shear modulus of the fins are not varying during the whole flight, remaining parameters, namely atmospheric pressure and speed of sound is carefully examined so that fin flutter speed can be revealed for the whole flight up to apogee. 
Atmospheric pressure and temperature for each altitude are modelled using the Ref. [2] provided by NASA. Depending on the temperature, speed of sound is determined by equation  ![Formula](https://latex.codecogs.com/svg.latex?\\color{white}c_{air}=\sqrt{kR_*T}), where the only variable is temperature. Flutter speed is, then accordingly, calculated with respect to altitude as shown in Figure 1. The same figure monitors the expected speed of the rocket with respect to altitude to compare them. Obviously, the fins flutter speed is significantly higher than expected rocket speed, which indicates that fins are not concerned to be exposed to flutter.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/f0c5cac5-0257-4437-bd7a-55824016c3b4" width="500" /></p>
<p align="center">Figure 1. Fin Flutter Speed and Speed of Rocket vs. Altitude </p>

 
Figure 1 also shows that minimum fin flutter speed, which is 405 m/s, is 59% higher than the maximum expected rocket velocity, which is 255 m/s. These numerical values agree with the requirement 8.2.2 in Design, Test, & Evaluation Guide (Revision: 2025 V1.1.4).  

#### Numerical and Experimental Approach 
To verify the results of analytical calculations provided in Apogee Newsletter 615, numerical analysis is run in Ansys FEA software. After defining custom carbon fiber material with mechanical properties. Fig. 2 monitors first 4 natural frequencies and their corresponding mode shapes are 633, 1500, 3001 and 3757 Hz, respectively. One can recognize that the first (fundamental) natural frequency and its mode shape is bending mode as expected due to long and thin topology of the fin. 


<p align="center">
  <img src="https://github.com/user-attachments/assets/3be474cf-cb49-469a-8e0e-7a0fdd46680a" width="500" /></p>
<p align="center">Figure 2. The first 4 mode shapes of fins. </p>


Frequency Response Function (FRF) analysis of the fin between 0-10 kHz can be found in Fig. 3. Using result of modal analysis and defining a damping ratio of 1% [4], harmonic analysis response of pressure variations along fin surfaces reveals that maximum displacement of 1.88*10^(-5)  mm at fundamental frequency. Though the rocket is designed such that its maximum speed is lower than flutter speed, this small displacement value does not cause any structural integrity problem in case of any flutter issue. From FRF analysis, note that the dominant, resulting in the highest displacement response, mode is fundamental mode; hence, the flutter speed corresponds to 633 Hz.


<p align="center">
  <img src="https://github.com/user-attachments/assets/50995f7d-d6e7-4169-aa88-0aea876eb37d" width="500" /></p>
<p align="center">Figure 3. Frequency Response Function (FRF) of Fins. Note that amplitude is the displacement defined as normal to fin surface. </p>

To relate that frequency with rocket’s speed, dimensionless number Strouhal number (St) in fluid mechanics is used. It is the number relating vortex shedding frequency (f) and free stream velocity (U) as follows:
![Formula](https://latex.codecogs.com/svg.latex?\\color{white}St=\{fL}/{U}),
where L denotes a characteristic length of the fin. Determining characteristic length is based on experiment setup from which the St data is obtained. For example, Rostami et al. [4] defined L as the thickness of the thin plate and found a Strouhal number of 0.01 for a 5-degree angle of attack. Therefore, L is taken as 4mm, and St is assumed to be 0.005 for 0-degree angle of attack, considering the St trend with respect to angle of attack values of 5, 10 and 15-degrees.
The first (fundamental) natural frequency with characteristics length of 0.004m and St of 0.005 yields free stream velocity of 
U=530 m/s.
This numerically& experimentally calculated velocity value is in the same order of magnitude as the analytical result, which is 442 m/s, found in the previous section. The discrepancy can be attributed to lack of exact value of experimentally determined St and fixed boundary condition defined in modal analysis since rocket will vibrate as well, which makes fin joint impossible to be fixed.
Finally, it is expected to have a flutter speed of 530 m/s and 442 m/s for numerical & experimental and analytical results. They, respectively, correspond to 96.3% and 63.7% higher velocities compared to maximum rocket speed of 270 m/s. 




- [1] https://apogeerockets.com/education/downloads/Newsletter291.pdf
- [2] https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
- [3] Mondal, Subhajit & Chakraborty, Sushanta. (2018). Estimation of Viscous Damping Parameters of Fibre Reinforced Plastic Plates using Finite Element Model Updating. The International Journal of Acoustics and Vibration. 23. 10.20855/ijav.2018.23.11064.
- [4] Rostami, A.B., Mobasheramini, M. & Fernandes, A.C. Strouhal number of flat and flapped plates at moderate Reynolds number and different angles of attack: experimental data. Acta Mech 230, 333–349 (2019). https://doi.org/10.1007/s00707-018-2292-2 


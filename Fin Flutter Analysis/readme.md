## Objective
Since the fins of a rocket is excited by the surrounding air during its flight, they are dynamiclly loaded by the air modelues. This dynamic loading requires the fins to be 
designed according to its flutter speed, which is the speed resulting in natural frequency excititaion. Therefore, it is a must to analyze and compare the fin flutter speed 
and expected rocket speed during its flight. 

### Here is the fin flutter analysis plot submitted for IREC2025 competition:
According to Ref. [1], fin flutter speed is governed by an equation where geometric dimension of fins, atmospheric pressure, speed of sound and shear modulus of fin material appear. Since geometric dimensions and shear modulus of the fins are not varying during the whole flight, remaining parameters, namely atmospheric pressure and speed of sound is carefully examined so that fin flutter speed can be revealed for the whole flight up to apogee. 
Atmospheric pressure and temperature for each altitude are modelled using the Ref. [2] provided by NASA. Depending on the temperature, speed of sound is determined by equation c_air=√(kR_* T), where the only variable is temperature. Flutter speed is, then accordingly, calculated with respect to altitude as shown in Figure 1. The same figure monitors the expected speed of the rocket with respect to altitude to compare them. Obviously, the fins flutter speed is significantly higher than expected rocket speed, which indicates that fins are not concerned to be exposed to flutter.  

![speedComparison](https://github.com/user-attachments/assets/f0c5cac5-0257-4437-bd7a-55824016c3b4)

Figure 1. Fin Flutter Speed and Speed of Rocket vs. Altitude  
Figure 1 also shows that minimum fin flutter speed, which is 405 m/s, is 59% higher than the maximum expected rocket velocity, which is 255 m/s. These numerical values agree with the requirement 8.2.2 in Design, Test, & Evaluation Guide (Revision: 2025 V1.1.4).  
The Python script used for calculations can be referred to for further calculation details.   
References  
- [1] https://apogeerockets.com/education/downloads/Newsletter291.pdf
- [2] https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html


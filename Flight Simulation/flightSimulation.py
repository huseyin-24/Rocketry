import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from flightAnimation import Animator
import matplotlib.image as mpimg
import matplotlib.animation as animation

# Initial Conditions and Constants
dt = 0.01      # Time step
x0, z0 = 0, 0  # Initial positions
h_i = 978      # Launch height (m)
phi0 = 85      # Initial flight path angle (degrees)
m_i = 22.3     # Initial mass (kg)
fuel_i = 4.12  # Initial fuel mass (kg)
isp = 189.4    # Specific impulse (s)
d = 0.144      # Rocket diameter (m)
area = np.pi * d**2 / 4  # Cross-sectional area (m^2)
v0 = 1         # Initial velocity (m/s)
g = 9.801      # Gravititaional acceleration (m/s^2)

# Read thrust data
thrust_data = pd.read_csv("thrustTime.csv")
final_thrust_time = thrust_data['Time'].max()   # Final thrust time
thrust_data_count = int(final_thrust_time / dt)
interp_time = np.linspace(0, final_thrust_time, thrust_data_count)
interp_thrust = np.interp(interp_time, thrust_data['Time'], thrust_data['Thrust'])
m_dot = interp_thrust / (isp * g)               # Mass flow rate (kg/s)

# Read drag coefficient data
cdMach = pd.read_csv('cdMach.csv')
mach_data = cdMach['Mach']
cd_data = cdMach['CD']

# Define 8th order Fourier fit function
def fourier8(x, *coeffs):
    result = coeffs[0]  # a0
    for n in range(1, 9):
        result += coeffs[2 * n - 1] * np.cos(n * x) + coeffs[2 * n] * np.sin(n * x)
    return result

# Fit Fourier curve to drag coefficient vs Mach data
initial_guess = [0] * 17
params, _ = curve_fit(fourier8, mach_data, cd_data, p0=initial_guess)

# Function to get Cd from Mach
def get_cd(mach):
    return fourier8(mach, *params)

# Initialize variables
x, z = x0, z0
vx = v0 * np.cos(np.radians(phi0))
vz = v0 * np.sin(np.radians(phi0))
h = h_i + z
phi = phi0

# Predefine storage lists
list_x, list_z = [x], [z]
list_vx, list_vz = [vx], [vz]
list_phi, list_pdx, mach_list = [phi], [0], [0]

s = 0  # Loop counter
# Loop up to apogee where vertical velocity is zero
while vz > 0:
    h = h_i + z

    # Thrust conditions
    if s < thrust_data_count:
        thrust = interp_thrust[s]
        fuel_i -= m_dot[s] * dt
        m = m_i - m_dot[s] * dt
    else:
        thrust = 0

    # Atmospheric conditions
    temperature = 15.04 - 0.00649 * h
    pressure = ((temperature + 273.1) / 288.08) ** 5.256 * 101.29
    rho = pressure / (0.2869 * (temperature + 273.15))  # Air density (kg/m^3)
    a = np.sqrt(1.4 * 287.05 * (temperature + 273.15))  # Speed of sound (m/s)

    # Aerodynamic conditions
    v = np.sqrt(vx**2 + vz**2)
    mach = v / a
    Cd = get_cd(mach)

    # Calculate aerodynamic forces
    p_dyn = 0.5 * rho * v**2
    F_drag = p_dyn * Cd * area
    F_X = (thrust - F_drag) * np.cos(np.radians(phi))
    F_Z = (thrust - F_drag) * np.sin(np.radians(phi))

    # Update velocities and positions
    vx += (F_X / m) * dt
    x += vx * dt
    vz += (-g + F_Z / m) * dt
    z += vz * dt
    phi = np.degrees(np.arctan2(vz, vx)) if vx != 0 else 90

    # Update lists
    list_x.append(x)
    list_z.append(z)
    list_vx.append(vx)
    list_vz.append(vz)
    mach_list.append(mach)
    list_pdx.append(p_dyn * np.cos(np.radians(phi)))
    list_phi.append(phi)

    s += 1

# Results
max_mach = max(mach_list)
range_value = list_x[-1]
altitude = list_z[-1]
final_velocity = np.sqrt(list_vx[-1]**2 + list_vz[-1]**2)
final_mach = mach_list[-1]
apogee_time = s * dt
total_time = np.linspace(0, apogee_time, s)

'''
# Plot results using subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 10))

axs[0, 0].plot(list_x, list_z)
axs[0, 0].set_xlabel('Range [m]')
axs[0, 0].set_ylabel('Altitude [m]')
axs[0, 0].grid(True)
axs[0, 0].set_title('Range vs Altitude')

axs[0, 1].plot(total_time, list_phi[:-1])
axs[0, 1].set_xlabel('Time [s]')
axs[0, 1].set_ylabel('Flight Angle [°]')
axs[0, 1].grid(True)
axs[0, 1].set_title('Time vs Flight Angle')

axs[1, 0].plot(total_time, mach_list[:-1])
axs[1, 0].set_xlabel('Time [s]')
axs[1, 0].set_ylabel('Mach Number')
axs[1, 0].grid(True)
axs[1, 0].set_title('Time vs Mach Number')

axs[1, 1].plot(total_time, list_pdx[:-1])
axs[1, 1].set_xlabel('Time [s]')
axs[1, 1].set_ylabel('Dynamic Pressure [Pa]')
axs[1, 1].grid(True)
axs[1, 1].set_title('Time vs Dynamic Pressure')

axs[2, 0].plot(total_time, list_vz[:-1])
axs[2, 0].set_xlabel('Time [s]')
axs[2, 0].set_ylabel('Vertical Climb Speed [m/s]')
axs[2, 0].grid(True)
axs[2, 0].set_title('Time vs Vertical Climb Speed')

axs[2, 1].plot(mach_data, fourier8(mach_data, *params), label="8th Order Fourier Fit")
axs[2, 1].scatter(mach_data, cd_data, color='red',label="Mach vs Cd Data", s=2)
axs[2, 1].set_xlabel('Mach')
axs[2, 1].set_ylabel('Cd')
axs[2, 1].grid(True)
axs[2, 1].set_title('Mach vs Cd')

plt.legend()
plt.tight_layout()
plt.show()'''

# ANIMATE THE FLIGHT
image =  mpimg.imread("rocket.png")
background = mpimg.imread("background.png")
imageWidth, imageHeight = image.shape[1], image.shape[0]
centerOffset = (imageWidth/2, imageHeight/2)
scale = 1 
seconds = apogee_time
print(f'Apogee time (s): {seconds:.02f}')
fps = 24

downsamplingRate = 10
points  = list(zip(list_x, list_z))
points = points[::downsamplingRate]

rotationAngles = list_phi
rotationAngles = rotationAngles[::downsamplingRate]

speeds = list(np.sqrt(np.array(list_vx)**2 + np.array(list_vz)**2))
speeds = speeds[::downsamplingRate]

myAnimator = Animator(points, rotationAngles, speeds, centerOffset, scale, image, background, seconds=seconds, fps=fps)
myAnimator.animate()

Writer = animation.writers['ffmpeg']
writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=-1)
myAnimator.anim.save('im.mp4', writer=writer)

print('finished!')
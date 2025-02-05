import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
import numpy as np
import matplotlib.animation as animation
from matplotlib.artist import Artist

class Animator:
    def __init__(self, points: list, rotationAngles: list, speeds: list, centerOffset: tuple, scale: float, image: np.ndarray, fps=24):
        self.centers = points
        self.rotationAngles = rotationAngles
        self.speeds = speeds
        self.centerOffset = centerOffset
        self.image = image
        self.scaleWidth = scale
        self.scaleHeight = self.image.shape[0] / self.image.shape[1] * self.scaleWidth
        self.fps = fps

        x_values, y_values = zip(*self.centers)
        self.centersX = list(x_values)
        self.centersY = list(y_values)

    def transformer(self, rotation:float, pointCenter:tuple):
        transform = (
            Affine2D()
            .translate(-self.centerOffset[0], -self.centerOffset[1])      # Center image
            .scale(self.scaleWidth, -self.scaleHeight)                   # Scale image
            .rotate_deg(rotation)                         # Rotate image
            .translate(pointCenter[0], pointCenter[1])  # Position image on the plot
        )
        return transform

    def animate_func(self, i):
        try: Artist.remove(self.textArtist)
        except:None
        pointCenter = self.centers[i]
        rotation = self.rotationAngles[i] # Increment rotation based on speed
        transform = self.transformer(rotation, pointCenter)
        self.im.set_transform(transform + self.ax.transData)  # Set transformation
        self.ax.plot(self.centersX[:i+1], self.centersY[:i+1], color = 'blue', linestyle='--', label='Trajectory', linewidth=1)
        
        text = f'Speed (m/s): {self.speeds[i]:.0f} \nRotation\nangle(degree): {self.rotationAngles[i]:.0f}'
        textX, textY = 0.5, 0.45
        self.textArtist = self.fig.text(textX, textY, text, fontsize = 8)

        return [self.im]

    def animate(self):
        self.xLim = max(point[0] for point in self.centers) * 1.5
        self.yLim = max(point[1] for point in self.centers) * 1.2

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.xLim)
        self.ax.set_ylim(0, self.yLim)

        self.im = self.ax.imshow(self.image, origin='upper')  # Initialize the image plot

        self.anim = animation.FuncAnimation(
            self.fig,
            self.animate_func,
            frames=len(self.centers),
            interval=1000/self.fps, #in ms
        )
        plt.title("Rocket on its trajectory")
        plt.xlabel("Range (m)")
        plt.ylabel("Altitude (m)")
        #plt.grid(True)
        plt.show()

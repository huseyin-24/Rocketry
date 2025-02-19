import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
import numpy as np
import matplotlib.animation as animation
from matplotlib.artist import Artist

class Animator:
    def __init__(self, points: list, rotationAngles: list, speeds: list, centerOffset: tuple, scale: float, image: np.ndarray, background,seconds= 20, fps=24):
        self.centers = points
        print(f'Length of initial dataset: {len(self.centers)}')
        self.rotationAngles = rotationAngles
        self.speeds = speeds
        self.centerOffset = centerOffset
        self.image = image
        self.background = background
        self.scaleWidth = scale
        self.scaleHeight = self.image.shape[0] / self.image.shape[1] * self.scaleWidth
        self.fps = fps
        self.seconds = seconds
        self.speedAdjustmenResolution = 0.01

        x_values, y_values = zip(*self.centers)
        self.centersX = list(x_values)
        self.centersY = list(y_values)

        self.finalSpeeds, self.finalXCenters, self.finalYCenters, self.finalRotationAngles = self.adjustTime1()
        self.finalCenters = list(zip(self.finalXCenters, self.finalYCenters))
        print(f'Length of final dataset: {len(self.finalCenters)}')


    def adjustTime1(self):
        numOfFrames = int(self.seconds * self.fps)
        
        # Vectorized interpolation of speeds
        interp_xdata = np.linspace(0, len(self.speeds) - 1, numOfFrames)
        speedsAdjusted = np.interp(interp_xdata, np.arange(len(self.speeds)), self.speeds)

        numOfSpeedSections = int(self.seconds * self.fps * self.speedAdjustmenResolution)
        InitNumOfFramesInOneSection = int(numOfFrames/numOfSpeedSections)

        # Vectorized section-wise speed adjustment
        section_indices = np.arange(numOfSpeedSections) * InitNumOfFramesInOneSection
        avgSpeedsInSections = speedsAdjusted[section_indices + InitNumOfFramesInOneSection // 2]

        # Compute frame count per section
        k = numOfFrames / np.sum(1 / avgSpeedsInSections)
        numOfFramesInSections = np.round(k / avgSpeedsInSections).astype(int)

        # Generate final speeds using efficient interpolation
        finalSpeeds = np.concatenate([
            np.interp(
                np.linspace(start, end, numFrames),
                np.arange(start, end),
                speedsAdjusted[start:end]
            )
            for start, end, numFrames in zip(section_indices, section_indices + InitNumOfFramesInOneSection, numOfFramesInSections)
        ])
        
        # Interpolate centers and angles
        expandedIndices = np.linspace(0, len(self.centersX) - 1, len(finalSpeeds))
        adjustedCentersX = np.interp(expandedIndices, np.arange(len(self.centersX)), self.centersX)
        adjustedCentersY = np.interp(expandedIndices, np.arange(len(self.centersY)), self.centersY)
        adjustedAngles = np.interp(expandedIndices, np.arange(len(self.rotationAngles)), self.rotationAngles)

        # Use vectorized 'takeClosest' approach
        adjustedCentersX = np.array([self.takeClosest(x, self.centersX) for x in adjustedCentersX])
        adjustedCentersY = np.array([self.takeClosest(y, self.centersY) for y in adjustedCentersY])
        adjustedAngles = np.array([self.takeClosest(a, self.rotationAngles) for a in adjustedAngles])

        return finalSpeeds, adjustedCentersX, adjustedCentersY, adjustedAngles

    def adjustTime(self): 
        numOfFrames = int(self.seconds * self.fps)
        
        interp_xdata = np.linspace(min(self.speeds), max(self.speeds), numOfFrames)
        speedsAdjusted = np.interp(interp_xdata, np.array(range(len(self.speeds))), self.speeds)
        speedsAdjusted = list(speedsAdjusted)
        
        numOfSpeedSections = int(self.seconds * self.fps * self.speedAdjustmenResolution)
        InitNumOfFramesInOneSection = int(numOfFrames/numOfSpeedSections)

        tot = 0 
        avgSpeedsInSections, numOfFramesInSections, finalSpeeds = [], [], []
        for i in range(numOfSpeedSections):
            rangeStart = i*InitNumOfFramesInOneSection
            rangeEnd = (i+1)*InitNumOfFramesInOneSection
            speedRange = speedsAdjusted[rangeStart:rangeEnd]
            avgSpeedInRange = speedRange[int(InitNumOfFramesInOneSection/2)]
            avgSpeedsInSections.append(avgSpeedInRange)
            tot += 1/avgSpeedInRange
        
        k = numOfFrames / tot
        
        for i in range(numOfSpeedSections):
            frameInOneSection = round(k/avgSpeedsInSections[i])
            numOfFramesInSections.append(frameInOneSection)

        for i in range(numOfSpeedSections):
            rangeStart = i*InitNumOfFramesInOneSection
            rangeEnd = (i+1)*InitNumOfFramesInOneSection
            speedRange = speedsAdjusted[rangeStart:rangeEnd]

            interp_xdata = np.linspace(rangeStart, rangeEnd, numOfFramesInSections[i])
            FinalSpeedsInOneSection = np.interp(interp_xdata, list(range(rangeStart,rangeEnd)), speedRange)
            
            for speed in FinalSpeedsInOneSection:
                finalSpeeds.append(speed)
        
        adjustedCentersX, adjustedCentersY, adjustedAngles =  [], [], []
        
        expandedXDataPoints = np.linspace(0, len(self.centersX), len(finalSpeeds))
        expandedYDataPoints = np.linspace(0, len(self.centersY), len(finalSpeeds))
        expandedAngleDataPoints = np.linspace(0, len(self.rotationAngles), len(finalSpeeds))

        InterpolatedXCenters = np.interp(expandedXDataPoints, list(range(len(self.centersX))), self.centersX)
        InterpolatedYCenters = np.interp(expandedYDataPoints, list(range(len(self.centersY))), self.centersY)
        InterpolatedAngles = np.interp(expandedAngleDataPoints, list(range(len(self.rotationAngles))), self.rotationAngles)
        
        for i in range(len(finalSpeeds)): 
            closestX = self.takeClosest(InterpolatedXCenters[i], self.centersX)
            closestY = self.takeClosest(InterpolatedYCenters[i], self.centersY)
            closestAngle = self.takeClosest(InterpolatedAngles[i], self.rotationAngles)        
            adjustedCentersX.append(closestX)
            adjustedCentersY.append(closestY)
            adjustedAngles.append(closestAngle)

        return finalSpeeds, adjustedCentersX, adjustedCentersY, adjustedAngles
      
    def takeClosest(self, num, collection):
        return min(collection,key=lambda x:abs(x-num))
    
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
        # Update text
        if self.textArtist:
            self.textArtist.set_text(
                f'Speed (m/s): {self.finalSpeeds[i]:.0f}\n'
                f'Rotation angle (°): {self.finalRotationAngles[i]:.0f}\n'
                f'Time (s): {i / self.fps:.0f}\n'
                f'Instance: {i}'
            )

        # Fetch frequently used values once
        pointCenter = self.finalCenters[i]
        rotation = self.finalRotationAngles[i]

        # Apply transformation
        transform = self.transformer(rotation, pointCenter)
        self.im.set_transform(transform + self.ax.transData)
        
        return [self.im, self.textArtist]

    def animate(self):
        # Set limits dynamically with NumPy
        self.xLim = np.max(self.finalXCenters) * 1.5
        self.yLim = np.max(self.finalYCenters) * 1.2

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.xLim)
        self.ax.set_ylim(0, self.yLim)

        self.ax.imshow(self.background, extent=[0, self.xLim, 0, self.yLim])
        self.im = self.ax.imshow(self.image, origin='upper')  

        # Initialize text artist (only once)
        self.textArtist = self.fig.text(
            0.45, 0.30, 
            "",  # Start with empty text
            fontsize=8
        )

        self.anim = animation.FuncAnimation(
            self.fig,
            self.animate_func1,
            frames=len(self.finalCenters),
            interval=1000 / self.fps,  # in ms
        )

        plt.title("Rocket on its trajectory")
        plt.xlabel("Range (m)")
        plt.ylabel("Altitude (m)")
        plt.show()

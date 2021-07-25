import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from import_c3d import MarkerSet

marker = MarkerSet('jumping_jacks.c3d')
print(marker.markerLabels)

# 3d projection
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i in range(2,marker.endFrame, 10):
    print(marker.frameRate)
    data = marker.getMarkerList(marker.markerLabels[:],i)
    for j, points in enumerate(data):
        ax.scatter(points[0], points[1], points[2])
    plt.pause(0.000001)
    ax.cla()

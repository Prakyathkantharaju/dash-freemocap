import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from import_c3d import MarkerSet

marker = MarkerSet('hips.c3d')
print(marker.markerLabels)
data = marker.getMarkerList(marker.markerLabels[:],20)

# 3d projection
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i, points in enumerate(data):
    print(i)
    ax.scatter(points[0], points[1], points[2])

plt.show()

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 20:37:34 2018

@author: ankhek

an example script for calcuating NDVI and ENDVI of plants to 
estimate the amount of photosynthesis

see http://www.maxmax.com/endvi.htm 
for how these indices are defined.
and https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index


for python 3.6 and opencv 3.4


"""

import cv2
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm



img = cv2.imread('NoirCamwBlueFilter.jpg')

cv2.imshow("img",img)
cv2.waitKey(1)

fromCenter = False
r = cv2.selectROI("img",img, fromCenter)

## Crop image
imCrop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
cv2.imshow("ImageCropped", imCrop)
cv2.waitKey(1)


R= imCrop[:,:,2].astype(np.float32)#red channel
G= imCrop[:,:,1].astype(np.float32)#green channel
B= imCrop[:,:,0].astype(np.float32)#blue channel  

"""check if divide by zero happens"""
ind = np.where(np.logical_and(R==0,B==0))
if ind[0].size>0:
    R[ind[0],ind[1]] = 1

"""NDVI using blue channel as red visible light"""
    
ndvi = (R-B)/(R+B)

"""ENDVI Enhanced Normalized Difference Vegetation Index """
endvi = (R+G-2*B)/(R+G+2*B)


fig, ax = plt.subplots()

cax = ax.imshow(ndvi, interpolation='nearest', cmap=cm.viridis)
ax.set_title('NDVI estimate')

cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
cbar.ax.set_yticklabels(['-1', '0', '1'])  # vertically oriented colorbar

fig2,ax2 = plt.subplots()
cax2 = ax2.imshow(endvi,cmap = cm.jet)
ax2.set_title('ENDVI estimate')
cbar2 = fig2.colorbar(cax2,ticks= [-1,0,1])
cbar2.ax.set_yticklabels(['-1','0','1'])

cv2.destroyAllWindows()
#

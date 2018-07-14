import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import time
from nibabel.testing import data_path
import matplotlib.animation as animation

example_filename = os.path.join(data_path, 'anatomical.nii')
img = nib.load(example_filename)
data = img.get_fdata()
fig = plt.figure()
i=0
im = plt.imshow(data[0], animated=True)
def updatefig(*args):
    global i
    if (i+1<len(data)):
        i += 1
    else:
        i=0
    im.set_array(data[i])
    return im,
ani = animation.FuncAnimation(fig, updatefig,  blit=True)
plt.show()

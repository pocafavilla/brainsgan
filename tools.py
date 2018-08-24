from __future__ import print_function, division
from PIL import Image
from scipy import ndimage

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#import sys
#from nibabel.testing import data_path

data_path = '/data/Team_Caspers/Leona_Maehler/Data/'
violin = True


def violin(errors):
        #l = ["1"]
        #for i in range(2, len(errors)+1):        #for i in range(1, len(errors)):
                #l.append(str(i))
        #print(np.random.randint(low=0, high=10, size=(1, len(l))))
        data = pd.DataFrame(np.asarray(errors).T, columns=["data", "model"])
        sns.set(style="whitegrid")
        #ax = sns.violinplot(x=errors_brains_GAN)
        ax = sns.violinplot(x = "model", y = "data", data = errors, palette = "muted")
        print(data)
        return ax.get_figure()

def save(px = None, name = None):

	px = (px * 255 / np.max(px)).astype('uint8')
	p = np.stack((px,)*3, -1)
	new_image = Image.fromarray(p, 'RGB')

	#im = plt.imshow(data, cmap = 'binary')
	#im = plt.imshow(new_image)
	#plt.show()

	# Use PIL to create an image from the new array of pixels
	new_image.save(name + '.png')


                                                                                #on first run:
#os.makedirs("./RAISE HR")
#os.makedirs("./../../../../data/Team_Caspers/Leona_Maehler/slices_HR")


def resize(path = None, filename = None):
	im1 = Image.open(path+filename)
	im2 = im1.resize((int(im1.width/2), int(im1.height/2)), Image.NEAREST)
	im2.save("/data/Team_Caspers/Leona_Maehler/slices_LR/"+filename)

def split(name = None):
	#do slicing:

	#example_filename = os.path.join(data_path, './anatomical.nii')
	#os.chdir("./RAISE HR")
	example_filename = os.path.join(data_path, name)
	img = nib.load(example_filename)
	data = img.get_fdata()
	
	os.chdir("/data/Team_Caspers/Leona_Maehler/slices_HR")

	#horizontallly [up to down]                                                             axial
	for y in range(50, len(data)-50):#160,  80-3=77       77|3|4|76  = 
               #for y in range(50, len(data)-50)              127|128            
		save(px = data[y][:][1:], name = name[:2]+"_left_to_right_"+str(y))
	#im2 = im1.resize((width, height), Image.NEAREST)

	'''
	#vertically [left to right]                                                             sagital

	arr = ([None])
	for z in range(0, len(data[0])):
		ar = ([data[0][0].tolist()])
		arr[0] = ar
		for y in range(1, len(data)):
			ar.append(data[y][z])
		save(px = ar, name = "up_to_down_"+str(z))
		arr.append(ar)

	#vertically [back to front]                                                             coronal
	brr = ([None])
	for x in range(0, len(data[0][0])):
		br = [None] * len(data)
		#print(brr[0])
		for y in range(0, len(data)):
		        r = [None] * len(data[0])
		        for z in range(0, len(data[0])):
		                r[z] = data[y][z][x]
		        br[y] = r
		save(px = br, name = "back_to_front_"+str(x))
		brr.append(br)	'''


def split_dir():
	print('commencing...')
	dir_files = os.listdir(data_path)
	for i in range(102, 170):#	for i in range(53, 110):
		filename=dir_files[i]
		if(filename.endswith("e.nii.gz")):
			print(filename+" "+str(i))
			split(name = filename)

def resize_dir():
	for filename in os.listdir("/data/Team_Caspers/Leona_Maehler/slices_HR"):
		resize("/data/Team_Caspers/Leona_Maehler/slices_HR/",filename)






def get_original(filename):
        img = Image.open("/data/Team_Caspers/Leona_Maehler/BrainsGAN/1/data/test_HR/"+filename)
        data = img.getdata()
        return(data)



def evaluate(ar1, ar2):
        error = float(0)
        for x in range(len(ar1)):
               for y in range(len(ar1[0])):
                      #ar1[x][y] -= ar2[x][y]
                      error += (ar1[x][y] - ar2[x][y])*(ar1[x][y] - ar2[x][y])
        return(error)


def evaluate_all_imgs(path):
        dir = os.listdir(path)
        if(not violin):
                error = float(0)
                for filename in dir:
                        img = Image.open(path+filename)
                        data = img.getdata()
                        error += evaluate(get_original(filename), data)
                return error
        else:
                error = [None] * len(dir)
                i = 0
                for filename in dir:
                        img = Image.open(path+filename)
                        data = img.getdata()
                        error[i] = evaluate(get_original(filename), data)
                        i+=1
                return error
        
def spline(path):
        for filename in os.listdir(path):
                img = Image.open(path+filename)
                p = img.resize([img.width*2,img.height*2], resample = Image.BICUBIC)
                p.save("/data/Team_Caspers/Leona_Maehler/spline/"+filename)
                #print("done")



def linear(path):
        for filename in os.listdir(path):
                img = Image.open(path+filename)
                p = img.resize([img.width*2,img.height*2], resample = Image.BILINEAR)
                p.save("/data/Team_Caspers/Leona_Maehler/linear/"+filename)
                #print("done")
        
def write_eval_report():
        

#split_dir()
#resize_dir()
#evaluate_all_methods()

linear = evaluate_all_imgs("/data/Team_Caspers/Leona_Maehler/linear/")
spline = evaluate_all_imgs("/data/Team_Caspers/Leona_Maehler/spline/")
brainsGAN = evaluate_all_imgs("/data/Team_Caspers/Leona_Maehler/BrainsGAN/1/result/images/")
l = [[None] * 42*3, [None] * 42*3]
for j in range(0, 3):
        for i in range(0, 42):
                if(j == 0):
                        l[0][i + j*42] = linear[i]
                        l[1][i + j*42] = "linear"
                elif(j == 1):
                        l[0][i + j*42] = spline[i]
                        l[1][i + j*42] = "spline"
                else:
                        l[0][i + j*42] = brainsGAN[i]
                        l[1][i + j*42] = "brainsGAN"

        
d = {"error": l[0], "model": l[1]}          
            
df = pd.DataFrame(data=d)

print (df)

tips = sns.load_dataset("tips")
print (tips)

data = pd.DataFrame(df, columns=["error", "model"])
#print(data)
sns.set(style="whitegrid")
#ax = sns.violinplot(x=errors_brains_GAN)
ax = sns.violinplot(x = "model", y = "error", data = df, palette = "muted")
#print(data)
ax.get_figure().savefig("res.png")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        










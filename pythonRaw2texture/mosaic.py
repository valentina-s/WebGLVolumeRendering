"""
This function creates a 2D texture mosaic from a 3d volume.
It first pads the image to equal dimensions.
Then downscales it to 256x256x256. This is stored by default to
Then creates a .png mosaic of all the slices: (16*256)x(16*256) = 4096x4096.

Source:

It is a modification of the code in

http://www3.cs.stonybrook.edu/~igutenko/volrender/extractslice.py
- adjusted to work with Python 3
- adjusted to work with nrrd files
- adjusted the output names

Usage:

    python mosaic.py input_image.nrrd input_image_mosaic256.png input_image_paddedCube256.nrrd

#TODO

- test to see whether I can tile directly in numpy without creating and storing files
- make it work for number different than 256
- make to work for non-equal dimensions
- modify it to read and output tif images

"""


import numpy as np
from PIL import Image
from scipy import misc
import nrrd
import sys
import math
import matplotlib.pyplot as plt
from scipy import ndimage




width = 256
height = 256
depth = 256
n = 256.

slicesX = 16
slicesY = 16

ext = '.png'

# set the input filename by hand:
# infile = '../../volumeJS/data/eye.nrrd'
# infile = 'eye_downscaled.nrrd'

#original = numpy.fromfile(infile, dtype=numpy.uint8)
#original = numpy.reshape(original, (width, height, depth))

# read the input filename (it is expected to be .nrrd file)
infile = sys.argv[1]

# read the file
original = np.array(nrrd.read(infile)[0],dtype = 'uint8')

# padding the
dim1, dim2, dim3 = original.shape
m = max((dim1,dim2,dim3))
pad1 = ((m - dim1)/2)
pad2 = ((m - dim2)/2)
pad3 = ((m - dim3)/2)
print(pad1,pad2,pad3)
original_padded = np.pad(original,[(math.ceil(pad1),math.floor(pad1)),(math.ceil(pad2),math.floor(pad2)),(math.ceil(pad3),math.floor(pad3))],mode = 'edge')
# original_padded = np.pad(original,[(math.ceil(pad1),math.floor(pad1)),(math.ceil(pad2),math.floor(pad2)),(math.ceil(pad3),math.floor(pad3))],mode = 'constant',constant_values = [(0,0),(0,0),(0,0)])
print(original_padded.shape)

# downscale
zooming_factor = n/original_padded.shape[0]
original_resized = ndimage.zoom(original_padded,zooming_factor)
# original_padded.resize((256,256,256))
print(original_resized.shape)

# I can rearrange the axes if needed
# original = np.rollaxis(original_resized,2,0).copy()
original = original_resized.copy()

# saving resized image as an .nrrd volume
if len(sys.argv)<3:
    infile_paddedCube = infile[:-5] + '_cube' + str(n) + '.nrrd'
else:
    infile_paddedCube = sys.argv[3]

if len(sys.argv)<2:
    mosaic_file = infile[:-5]+'_mosaic' + str(n) + ext
else:
    mosaic_file = sys.argv[2]

nrrd.write(infile_paddedCube,original)
print(original.shape)
for i in range(0,n):
    slice = original[i]
    misc.imsave(dataset + '/img'+ str(i-0+1) + ext, slice)

resultImg = Image.new('L', (width*slicesX, height*slicesY))
# read files 1 by 1 from dir
for tileIdx in range(0,n):
    tileName = dataset + '/img'+ str(tileIdx+1) +ext
    print(tileName)
    tileImg = Image.open(tileName)
    tileIdxX = tileIdx % slicesX
    tileIdxY = tileIdx // slicesY

    for tileX in range(0, width):
        for tileY in range(0, height):
            imgX = width * tileIdxX + tileX
            imgY = height * tileIdxY + tileY
            print(imgX)
            print(imgY)
            pixel = tileImg.getpixel((tileX, tileY))

            resultImg.putpixel((imgX, imgY), pixel)


resultName = mosaic_file[-4]


resultImg.save(mosaic_file)

# I have not tested the iterpolated textures, not sure if the dimensions are right
newWidth = 2048
newHeight = 2048

resultImgNearest 	=  resultImg.resize((newWidth, newHeight), Image.NEAREST)
resultImgBilinear 	=  resultImg.resize((newWidth, newHeight), Image.BILINEAR)
resultImgBicubic 	=  resultImg.resize((newWidth, newHeight), Image.BICUBIC)
resultImgAntialias 	=  resultImg.resize((newWidth, newHeight), Image.ANTIALIAS)

resultImgNearest.save(resultName + 'Nearest' + ext)
resultImgBilinear.save(resultName + 'Bilinear' + ext)
resultImgBicubic.save(resultName + 'Bicubic' + ext)
resultImgAntialias.save(resultName + 'Antialias' + ext)

resultImg = np.asarray(resultImg)

# creating an image with 4 channels (otherwise webgl cannot display it)
# (I think the fourth channel is transparency: maybe I can modify that to obtain desirable visualization effects, at this point the image is tiled to fill the 4th channel)
resultImg = np.tile(resultImg.reshape(resultImg.shape[0],resultImg.shape[1],1),(1,1,4))
misc.imsave(mosaic_file, resultImg)

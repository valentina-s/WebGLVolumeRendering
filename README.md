WebGL Volume Rendering
====================

This repository is an adaptation of the code at 

https://github.com/lebarba/WebGLVolumeRendering

to display cornea images. The approach uses 2D textures.That requires building a 2d mosaic image out of the 3d image. To efficiently process textures it is best if the image dimensions are of power of 2. Cornea images do not satisfy this condition. For now we pad the images to the maximal dimension (to have equal dimensions), and then downsample to an image of size 256x256x256. This needs to be optimized.


![Screenshot1](https://raw.githubusercontent.com/valentina-s/WebGLVolumeRendering/master/img/slices.png)    
![Screenshot2](https://raw.githubusercontent.com/valentina-s/WebGLVolumeRendering/master/img/3dvis_controls.png)     

To add the display the segmentation in THREE.js we need to convert the .swc files to a format readable by the library. There are several options to display surfaces:

* vtk - I can convert .swc file to an unstructured grid .vtk format, but the three.js example for a vtk-loader seems to work on only with the polydata format.
* stl - 
* obj - I can convert .swc to the .obj format in Fiji and align it correctly with the volume (in Vaa3d the bounding box changes and the alignment with the volume is lost). Need to find a command-line/python tool to do the conversion.



## LICENSE

The MIT License (MIT)
Copyright (c) 2017 Valentina Staneva

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


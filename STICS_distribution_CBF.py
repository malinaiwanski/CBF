# @Float(label="width and height of square ROI (pixels)", value=15) width_sub
# @Float(label="over-estimate the duration of one ciliary beat cycle or enter duration of entire movie (frames)", value=50) max_cycle_length
# @Dataset dataset

#NB: do not currently use input max cycle length

import os
import csv

from net.imagej.axis import Axes
from ij.plugin.frame import RoiManager
from ij.plugin import ZProjector, ZAxisProfiler, ImageCalculator
from ij.gui import Roi, GenericDialog, PlotMaker, PlotWindow
from ij import IJ, WindowManager, ImagePlus, process, ImageStack

RoiManager.getRoiManager()
rm = RoiManager.getInstance()
if len(rm.getRoisAsArray()) > 0:
	print("Warning: all other ROIs about to be deleted")
	rm.runCommand("Deselect")
	rm.runCommand("Delete")

filename = dataset.getName()
parent_folder = dataset.getSource().replace(filename, "")
save_folder = parent_folder + "/STICS data"
try:
	if not os.path.exists(save_folder):
		os.makedirs(save_folder)
except OSError:
	print("Could not create directory to save files")
coords_path = os.path.join(save_folder, os.path.splitext(filename)[0]) # + "_STICS_map" + ".tif")

imp = IJ.getImage()
IJ.run("32-bit")

name = imp.getTitle()
width = imp.width
height = imp.height
num_slices = imp.getNSlices()
num_channels = imp.getNChannels()
num_frames = imp.getNFrames()

max_cycle_length = int(max_cycle_length)

assert width_sub < width and width_sub < height, "Size of square must be less than dimensions of movie"
assert num_channels == 1, "Image can only have one channel"

#imp = process.ImageConverter.convertToGray32(original_imp)

avg_img = ZProjector.run(imp,"avg");
avg_img.show()
imp2 = ImageCalculator().run("Subtract create stack", imp, avg_img)
imp2.show()
#WindowManager.getImage("AVG_Pos0")

num_window_x = int(round(width/width_sub)) #int(width-width_sub+1)
num_window_y = int(round(height/width_sub)) #int(height-width_sub+1)

center_px = int(round(width_sub/2))

new_rois = []
for i in range(0,num_window_x):
	for j in range(0,num_window_y):
		new_roi = Roi(i*width_sub, j*width_sub, width_sub, width_sub)
		new_rois.append(new_roi)
		
for new_roi in new_rois:
	rm.addRoi(new_roi)

#new_img = IJ.createHyperStack("Time Correlation",width,height,1,1,num_frames, 32)
result_stack = ImageStack.create(width,height, max_cycle_length, 32)

#empty = imp2.getProcessor().createProcessor(width, height)

#for i in range(max_cycle_length):
	#result_stack.addSlice("",empty)

for i, roi in enumerate(rm.getRoisAsArray()):
	assert roi.getTypeAsString() == 'Rectangle', "ROI needs to be a rectangle"
	x_pos = roi.getPolygon().xpoints[0] + int(round(width_sub/2))
	y_pos = roi.getPolygon().ypoints[0] + int(round(width_sub/2))
	imp3 = imp2.duplicate()
	imp3.show()
	#imp3 = IJ.getImage()
	imp3.setRoi(roi)
	IJ.run(imp3, "Crop", "")
	IJ.run("2D STICS (space, time)", "max=50 calculation=[FFT cross-correlation (fast)]")
	#WindowManager.setCurrentWindow("Result of Pos0_2D_STICS")
	img = IJ.getImage()
	#print(img.getTitle())
	img.setRoi(center_px, center_px, 1, 1)
	plot = ZAxisProfiler.getPlot(img)
  	#plot.show();
  	x_val = plot.getXValues();
  	y_val = plot.getYValues();
  	#plot2 = new Plot("Z Axis Plot", "X", "Y", xval, yval);
  	#plot2.show();
	for j in range(len(y_val)):
		result_stack.setVoxel(x_pos,y_pos,j,y_val[j])
	imp3.changes = False
	imp3.close()
	img.changes = False
	img.close()

	print("STICS completed for ROI " + str(i+1) + " of " + str(num_window_x*num_window_y))

IJ.log("2D STICS completed")
IJ.log("Window size: " + str(width_sub) + " pixels")
IJ.log("Maximum time lag analyzed: " + str(max_cycle_length) + " frames")

#savepath = IJ.getDirectory("")
#imp = IJ.getImage()
#ssize = imp.getStackSize()
#titleext = imp.getTitle()
title = os.path.splitext(filename)[0] + "_STICS_map" #os.path.splitext(titleext)[0]

save_imp = ImagePlus(title, result_stack)
save_imp.show()

dimA = save_imp.getDimensions()
for c in range(dimA[2]):
	for z in range(dimA[3]):
		for t in range(dimA[4]):
			save_imp.setPosition(c+1, z+1, t+1)
			#print c, z, t
			numberedtitle = \
			title + "_c" + IJ.pad(c, 2) + \
			"_z" + IJ.pad(z, 4) + \
			"_t" + IJ.pad(t, 4) + ".tif"
			stackindex = save_imp.getStackIndex(c + 1, z + 1, t + 1)
			aframe = ImagePlus(numberedtitle, save_imp.getStack().getProcessor(stackindex))
			IJ.saveAs(aframe, "TIFF", coords_path + numberedtitle)
			#IJ.log("saved:" + numberedtitle)

#IJ.saveAs(result_stack, "TIFF", coords_path)
IJ.log("Saved " + str(dimA[3]) + " files at: " + coords_path)
  	
print("Done")

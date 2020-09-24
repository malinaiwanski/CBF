
run("Z Project...", "projection=[Standard Deviation]");
//setTool("line");
makeLine(17, 13, 40, 43);
roiManager("Add");
run("Measure");

selectWindow("Pos0");
run("Rotate... ", "angle=-52.52 grid=1 interpolation=Bilinear stack");

//setTool("rectangle");
makeRectangle(4, 15, 52, 29);
roiManager("Add");
run("Duplicate...", "duplicate");

run("Volume Viewer");
selectWindow("Volume_Viewer_1");
//setTool("rectangle");
makeRectangle(299, 0, 50, 660);
roiManager("Add");
run("Duplicate...", " ");


run("FFT");
selectWindow("PS of Volume_Viewer_1-1");
selectWindow("Complex of Volume_Viewer_1-1");
selectWindow("FFT of Volume_Viewer_1-1");
//setTool("line");
makeLine(512, 0, 512, 1024);
roiManager("Add");
run("Plot Profile");
run("Script...");

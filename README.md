# COVID

Codes to process data for the COVID project.
This set of files currently allows you to:

1. obtain a frame time histogram and mean frame time from metadata saved with MicroManager.
2. perform (spatio)temporal image correlation spectroscopy (STICS) in ROIs tiled across your image and safe the resulting correlation profiles.
3. fit the correlation profiles in each ROI to estimate the beat period/frequency and create a map of the beat frequencies across the image.
4. compile the ciliary beat frequency (CBF) information for different conditions into violin plots for comparison.

To do so, use the codes as follows:

In Jupyter lab, run metadata-extract-timestamps and record the average frame time in msec provided. This code is based on the MicroManager metadata file output when you save movies as separate image files. The histogram produced by the code will show if there are any outliers in frame time that you should be careful about. If the exact frame time of your movie is known, this code can be ignored and you can just input the known frame time in the following code instead. If you need such a code, but this version does not work with your metadata, I am happy to help you figure it out.

Run STICS_distribution_CBF through Fiji scripts on the movie of choice. Note that currently, 2D STICS will be performed using a delay of 50 regardless of input. You are able to change the width of the square ROI used in producing this map (in pixels; I always use an odd number for this so the 'center' pixel is well defined). Running this code requires the Correlescence v0.0.4 plugin --> 2D STICS from Eugene Katrukha. Contact me for more information.

In Jupyter lab, run STICS_CBF. Ensure you input the appropriate frame time in msec, as well as the size of the movie in pixels in x and y. While running this code, select the 'STICS data' folder created by running the previous code. You can toggle between displaying/saving images and files. Note that saving files is required to proceed with the subsequent step. This code will provide you with a map of the ciliary beat frequencies across one field of view.

In Jupyter lab, run STICS_CBF_all_frequencies. This will provide you with a distribution of the ciliary beat frequencies across all movies analyzed. While running this code, select the parent folder in which all the folders/movies with 'STICS data/Results' folders are located. Here you will have to input category names depending on how you organize your files and which categories you want to plot (e.g. + and - treatment or WT and mutant, etc.). The category names must be typed as they are in the file names for the code to find them. Note that if a file contains the names of two categories, it will also be counted in both categories, so this should be avoided.

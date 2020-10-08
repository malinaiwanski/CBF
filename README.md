# COVID

Codes to process data for the COVID project.
Currently allows you to obtain frame time histogram and mean frame time from metadata saved with micro manager and outlines the steps to estimate the CBF.

Run STICS_distribution_CBF through Fiji scripts on the movie of choice. Note that currently, 2D STICS will be performed using a delay of 50 regardless of input. Note that doing so requires the Correlescence v0.0.4 plugin --> 2D STICS from Eugene Katrukha. Contact me for more information.

In Jupyter lab, run metadata-extract-timestamps and record the average frame time in msec provided. The histogram will show if there are any outliers in frame time. If the exact frame time of your movie is known, this can be used in the following code instead.

In Jupyter lab, run STICS_CBF. Ensure you input the appropriate frame time in msec, as well as the size of the movie in pixels in x and y. You can toggle between displaying/saving images and files. Note that saving files is required to the subsequent step. This code will provide you with a map of the ciliary beat freuquencies across one field of view.

In Jupyter lab, run STICS_CBF_all_frequencies. This will provide you with a distribution of the ciliary beat frequencies across all movies analyzed.

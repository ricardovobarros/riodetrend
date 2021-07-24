"""In this module you will see all the necessary packages to run the code.
The Address of the directories for raster and shape files are defined here.
Additionally, you can set up what kinds of plots you want too show.
"""
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import logging

    from gdal import ogr
    import geopandas

    from osgeo import gdal
    import os
    import glob
    import sys
    from time import perf_counter
    from pathlib import Path

except ImportError:
    print("One of the python packages could not be opened")

# EXAMPLE SET UP

# Save address of directories of shape files (Thalweg points),
# raster files (digital elevation models) of the example
# and detrended raster(s)
directory_shape_files = Path(os.path.abspath(os.getcwd()) + "/geodata_example/shapefiles/")
directory_raster_files = Path(os.path.abspath(os.getcwd()) + "/geodata_example/rasters/")
detrended_raster_path = Path("geodata_example/detrended_rasters")

# Define the band fo the raster(s) file(s) to be extracted.
band_num = 1

# Limit to be considered detrended
detrend_limit = 10 ** -2

# Set True to show the plots of the respective elements.
# plot_detrender = True
plot_detrender = True

# Delete log file to avoid errors
try:
    os.remove("logfile.log")
except:
    pass

# SET UP WITH INPUT FROM TERMINAL
plots_path = None
if len(sys.argv) > 1:
    try:
        directory_raster_files = Path(sys.argv[1])
        directory_shape_files = Path(sys.argv[2])
        if len(sys.argv) > 3:
            plot_detrender = bool(int(sys.argv[3]))
            if len(sys.argv) > 4:
                band_num = int(sys.argv[4])
                if len(sys.argv) > 5:
                    detrend_limit = float(sys.argv[5])
        try:
            plots_path = Path(str(directory_raster_files)
                              .strip(str(directory_raster_files)
                                     .split(str(Path("/")))[-1]) + "detrender_plotter")

            os.mkdir(plots_path)
            print("Successfully created the directory with plots at {} ".format(plots_path))
        except OSError:
            pass
        try:
            detrended_raster_path = Path(str(directory_raster_files)
                                         .strip(str(directory_raster_files)
                                                .split(str(Path("/")))[-1]) + "detrended_rasters")
            os.mkdir(detrended_raster_path)
            print("Successfully created the directory with detrended rasters at {} ".format(detrended_raster_path))
        except OSError:
            pass

    except:
        print("Input invalid. Example was ran instead.")

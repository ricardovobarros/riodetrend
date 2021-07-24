""" Main script of detrender

This stand alone script contains the logical step-by-step process to detrended a raster file.
It needs the module functions and the classes Thalweg and Raster to run.

Functions:
----
* find_files: returns a list with the raw name of all file inside a
given directory

* detrender: contains all the necessary steps to get a shapefile (thalweg points)
and raster file (DEM) and saves the detrended raster file inside a chosen folder.

* main : runs the function detrender as many times as the number of raster
files given as input.

"""
from config import *
from fun_plot import *
from fun_support import *
from raster import Raster
from thalweg import Thalweg


def find_files(directory=None):
    """It finds all the .tif or .shp files inside a folder and
     create list of strings with their raw names

    :param directory: string of directory's address
    :return: list of strings from addresses of all files inside the directory
    """
    # Set up variables
    is_raster = False
    is_shape = False
    # raster_folder, shape_folder = verify_folders(directory)

    # terminate the code if there is no directory address
    if directory is None:
        print("Any directory was given")
        sys.exit()

    # Append / or / in director name if it does not have
    if not str(directory).endswith("/") and not str(directory).endswith("\\"):
        directory = Path(str(directory) + "/")

    # Find out if there is shape or raster file inside the folder
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.tif'):
                is_raster = True
                break
            if file_name.endswith('.shp'):
                is_shape = True
                break
    except:
        print("Input directory {} was not found".format(directory))

    # Create a list of shape files or raster files names
    if is_shape:
        file_list = glob.glob(str(directory) + "/*.shp")
    elif is_raster:
        file_list = glob.glob(str(directory) + "/*.tif")
    else:
        print("There is no valid file inside the folder {}".format(directory))
        exit()
    return file_list


@chronometer
def detrender(raster_add, shapefile_add):
    """ It instantiates one object from the class Raster
    and one object from class Thalweg.
    It performs all the necessary computations to create
    a detrended array.
    Finally, it creates a .tif of the detrended array and
    saves it inside the folder "detrended_rasters".

    :param raster_add: string of raster's address
    :param shapefile_add: string of shape's address
    :return: None
    """
    # Instantiate a Raster class and create a data frame with xy(coordinates) and z(band1).
    raster = Raster(raster_address=raster_add, driver="Gtiff", band=band_num)
    band_array, band_array_flat = raster.get_band_array()
    raster_coord_df = raster.coord_dataframe(array=band_array_flat)

    # Instantiate a Thalweg class and create a data frame of the points layer.
    thal_points = Thalweg(shapefile_add)
    thal_df = thal_points.shape2dataframe
    thal_points.slope = thal_points.compute_slope(thal_df)
    logging.info("Dem {} trend = {}%".format(raster.name,
                                             thal_points * 100))  # Use magic method __mul__

    # Compute a normal vector and a point of the DEM's Trend Plane.
    plane_normal, plane_point = compute_normal(thal_df)

    # Compute a dataframe with the x,y and z position of the DEM's Trend Plane.
    plane_df = compute_plane(raster_coord_df["x"],
                             raster_coord_df["y"],
                             plane_normal,
                             plane_point)

    # Compute a normalized array for the z values of the Trend Plane.
    plane_normalized = normalize_plane(band_array,
                                       plane_df['z'])

    # Compute detrended array.
    detrended_array = np.asarray(band_array
                                 - plane_normalized)

    # Find thalweg z coordinates for the Detrended DEM for validation.
    thalweg_new_z_vector = thal_points.find_thal_new_z(thal_df,
                                                       detrended_array,
                                                       raster)
    thal_points.slope = thal_points.compute_slope(thal_df, thalweg_new_z_vector, type="detrend")
    logging.info("Detredend dem {} trend = {}%".format(raster.name,
                                                       thal_points * 100))  # Use magic method __mul__

    # Check if the new Trend is flat enough
    thal_points.check_detrend(raster_object=raster)

    # Create detrended raster file.
    raster.burn(detrended_array)

    # Plot the elements marked as True in config.py
    plotter(thal_df, plane_df, raster_coord_df, thalweg_new_z_vector, raster.name, thal_points.name)


@log_actions
@chronometer
def main():
    """It loops through a list of names of raster and shapes
    and uses each combination of them to call the function detrender.
    :return: None
    """
    for i, file_raster in enumerate(file_list_raster):
        detrender(file_raster, file_list_shape[i])


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # Create two lists with all addresses of: raster files (DEMs); shape files (thalweg points).
    file_list_raster = find_files(directory=directory_raster_files)
    file_list_shape = find_files(directory=directory_shape_files)

    print("\nThe detrend of your raster(s) have the following results: \n")

    # Call main function
    main()

"""This module contains support functions for detrender
 that perform mathematical operations or wrap functions.

Math Functions
____
    * compute_plane: creates a dataframe with (x,y,z) given
    a domain, a point on the plane and a normal vector

    * compute_normal: computes a normal vector and finds a point on the
    Trend Plane, which is the best plane to represent a given set od 3d points.

    * normalize plain: normalizes a Trend Plane such that it can be subtracted by
    the altitudes of the raster array.

    * verify_inputs: verifies if there are .shp files and .tif files in the
    given folder and if they are equal in number.

Wrapper Functions
____
    * log_actions: sets the logging configuration and shut it down.
    * start_logging: (not wrapper) log_actions's helper.
    * chronometer: takes track of the run time and print it.
"""

from detrender import *


def compute_plane(x, y, normal, point):
    """Computes the z values of the DEM's Trend Plane and
    organizes it in a dataframe

    :param x: Vector with X coordinates of all pixels of DEM (Domain)
    :param y: Vector with Y coordinates of all pixels of DEM (Domain)
    :param normal: A normal vector of the Trend Plane
    :param point: A defined point on the Trend Plane
    :return: Data frame with coordinates (x,y,z) of all points on the plane
    """
    # Store and compute plane equation constants (Ax+By+Cz=D).
    A = normal[0]
    B = normal[1]
    C = normal[2]
    D = A * point[0] + B * point[1] + C * point[2]

    # Compute z value of the plane for all Dem's pixels.
    z = 1 / C * (-1 * A * x
                 + (-1) * B * y
                 + D)

    array = np.array([x, y, z]).transpose()
    return pd.DataFrame(array, columns=["x", "y", "z"])


def compute_normal(df):
    """Computes a normal vector to the Trend Plane, given as input a
    data frame with columns (x,y,z) representing the coordinates of the points
    of thalweg.

    :param df: Data frame with (x,y,z) of thalweg's points
    :return: A normal vector to the plane and a point on the plane
    """
    # Compute the coefficients of the regression lines of thalweg points:
    # X vs.Y (Center Line);
    # and DistanceDownstream vs. Z (DEM's Trend).
    line_coefs_xy = np.polyfit(df["x"], df["y"], 1)
    line_coefs_dz = np.polyfit(df["distance"], df["z"], 1)

    # Find X and Y coordinates of the first and last point in the "Center Line".
    x_first = df["x"][0]
    x_last = df["x"].iloc[-1]
    y_first = line_coefs_xy[0] * x_first + line_coefs_xy[1]
    y_last = line_coefs_xy[0] * x_last + line_coefs_xy[1]

    # Find the z coordinate of the Last Point and the First Point of "Center Line".
    z_last = df["z"].iloc[-1]
    points_distance = np.sqrt((x_first - x_last) ** 2
                              + (y_first - y_last) ** 2)
    z_first = z_last + abs(line_coefs_dz[0]) * points_distance

    # Define two points of the Trend plane.
    point_last = np.array([x_last, y_last, z_last])
    point_first = np.array([x_first, y_first, z_first])

    # Compute a vector on the Trend plane.
    plane_vector = point_last - point_first

    # Compute a normal vector to the plane
    x_normal = 1
    y_normal = x_normal * line_coefs_xy[0]
    z_normal = -(1 / plane_vector[2]) * (plane_vector[0] * x_normal + plane_vector[1] * y_normal)

    plane_normal = np.array([x_normal, y_normal, z_normal])
    return plane_normal, point_last


def normalize_plane(band, plane):
    """ Normalize the Trend Plane such that it can be subtracted by
    the altitudes of the raster's band array.

    :param band: array with altitude of DEM's pixels
    :param plane: array of z values of the Trend Plane
    :return: Array with normalized values of the Trend Plane
    """
    num_rows, num_cols = band.shape
    plane_floor = (plane.median()) * np.ones((num_rows, num_cols))
    normalized_plane = np.asarray(plane).reshape(num_rows, num_cols) - plane_floor
    return normalized_plane


def log_actions(fun):
    """Wrapper function initiate and close logging actions

    :param fun: Wrapped function
    :return: wrapper
    """

    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()

    return wrapper


def start_logging():
    """Configurations of logging and action to display the
    logging actions on terminal

    :return:None
    """
    logging.basicConfig(filename="logfile.log",
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        filemode="w",
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())


def chronometer(fun):
    """Wrapper function that track the run time of another function

    :param fun:Wrapped function
    :return: Wrapper
    """

    def wrapper(*args, **kwargs):
        name = fun.__name__
        t0 = perf_counter()
        fun(*args, **kwargs)
        t1 = perf_counter()
        print("function {0} had a time elapsed of {1:.3f}: ".format(name, (t1 - t0)))
        print("\n")

    return wrapper


def verify_inputs(args=None):
    """verifies if there are .shp files and .tif files in the
    given folder and if they are equal in number.

    :param args: List of string with directories names
    :return: None
    """
    if args is None:
        return
    have_raster = False
    have_shape = False
    shape_num = 0
    raster_num = 0
    try:
        for file_name in os.listdir(args[-2]):
            if file_name.endswith('.tif'):
                have_raster = True
                raster_num += 1
        for file_name in os.listdir(args[-1]):
            if file_name.endswith('.shp'):
                have_shape = True
                shape_num += 1
    except:
        print("Input not valid")
    if raster_num != shape_num:
        print("The number of shape files and raster files must be equal")
        sys.exit()
    if not have_raster:
        print("Any raster file was found")
        sys.exit()
    if not have_shape:
        print("Any raster file was found")
        sys.exit()

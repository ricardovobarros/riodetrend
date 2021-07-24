"""
 Module designated to Thalweg (Child class of Shape)
 Author: Ricardo Barros
 """
from shape import *


class Thalweg(Shape):

    def __init__(self, shape_address="", driver="ESRI Shapefile"):
        """A class used to represent a shape file of points
        that represents the thalweg line of a DEM. This class
        is child of the class Shape.

        Attributes
        ----
        _slope: Float values os the slope of the regression line from
        the  thalwegs' points (Elevation, Distance Downstream)

        Methods:
        ----
        slope: (Setter) Sets the property slope to follow the detrend process
        __mul__: Magic method to transforms the attribute slope in percentage
        __gt__: Magic method to check if the slope of the detrended DEM is lower
        enough to be considered flat (detrended)
        find_thal_new_z: Finds the elevation values of the detrended DEM that
        corresponds to coordinates of the thalwegs' points
        compute_slope: Compute the slope of a regression line of a 2d scatter
        check_detrend: Checks if the DEM respects a limit to be considered detrended

        Parameters:
        ____
        :param shape_address: String of the local address of a shape file
        :param driver: Type of driver to open a shape file. DEFAULT:"ESRI Shapefile"
        """
        super().__init__(shape_address, driver)
        self._slope = np.nan

    @property
    def slope(self):
        """Sets property slope to me changed.

        :return: self.slope
        """
        return self._slope

    @slope.setter
    def slope(self, value):
        """Sets slope of the Thalweg object to a new value.

        :param value: New value od slope
        :return: None
        """
        self._slope = float(value)

    def __mul__(self, multiplier):
        """Multiples the slope by 100 to get the value in percentage.

        :param multiplier: int 100
        :return: Slope in percentage
        """
        self.slope *= multiplier
        return self.slope

    def __gt__(self, limit):
        """Compares if the new slope of the thalweg of the detrended is small enough
        to be considered flat.

        :param limit: Threshold
        :return: Boolean True if the slope is grater than the limit
        """
        return abs(self.slope) > limit

    @staticmethod
    def find_thal_new_z(thalweg_df, detrended_array, raster):
        """Uses the coordinates of the Thalweg points to extract its corresponding
        altitudes of the detrended array.

        :param thalweg_df: Geo data frame with coordinates, altitude
         and distance between points of thalweg
        :param detrended_array: Array with elevation values of detrended DEM
        :param raster: Object from class Raster
        :return: Vector with detrended corresponding altitudes of the thalweg's points
        """
        # Find number of columns and rows of the raster dataset.
        cols = raster.dataset.RasterXSize
        rows = raster.dataset.RasterYSize

        # Find coordinates of reference pixel (first pixel) and pixels dimensions.
        x_origin = raster.transform[0]
        y_origin = raster.transform[3]
        pixel_width = raster.transform[1]
        pixel_height = -raster.transform[5]

        # Create a list with the coordinates of all pixels.
        points = thalweg_df[thalweg_df.columns[[5, 6]]].to_records(index=False)
        points_list = list(points)
        thalweg_new_z_array = np.array([])

        # Find a corresponding z value in detrended dem array for all point of thalweg.
        for point in points_list:
            col = int((point[0] - x_origin) / pixel_width)
            row = int((y_origin - point[1]) / pixel_height)
            thalweg_new_z_array = np.append(thalweg_new_z_array,
                                            detrended_array[row][col])

        return thalweg_new_z_array

    @staticmethod
    def compute_slope(df, vector_z=np.nan, type="trend"):
        """Computes the slope of a regression from 2d points,
        which are generated from the combination of two vectors.

        :param df: Geo data frame with coordinates, altitude
         and distance between points of thalweg
        :param vector_z: vector with altitudes of thalweg's points
        :param type: Type line.
        :return: Integer that represents the slope of the regression line
        """
        if type == "trend":
            return np.polyfit(df["distance"], df["z"], 1)[0]
        else:
            return np.polyfit(df["distance"], vector_z, 1)[0]

    # @staticmethod
    def check_detrend(self, raster_object):
        """ Checks if the DEM respects a limit to be considered detrended.

        :param raster_object: Raster object
        :return: None
        """
        if self > detrend_limit:  # Use magic method __gt__
            logging.warning("Detrended dem {} may not be sufficiently flat".format(raster_object.name))
        else:
            print("Dem {} was detrended successfully".format(raster_object.name))

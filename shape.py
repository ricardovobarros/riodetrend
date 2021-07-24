""" Module designated to Shape class

Author: Renan Vasconcelos
"""

from detrender import *


class Shape:
    def __init__(self, shape_address="", driver="ESRI Shapefile"):
        """Class that represents a shape file

        Attributes
        ----
        address: String of the files' address
        name: String of the files' name
        driver: Object Driver from Gdal
        dataset:Object Dataset from Gdal
        layer: Object Layer from Gdal

        Methods:
        ----
        shape2dataframe: Creates a geo data frame and
        adds two new columns (xy coordinates) to it

        Parameters:
        ____

        :param shape_address: String local address of shape file
        :param driver: Type of driver to open the shape file
        """
        try:
            self.address = shape_address
            self.name = self.address.split(str(Path("/")))[-1].strip(".shp")
            self.driver = ogr.GetDriverByName(driver)
            self.dataset = self.driver.Open(shape_address)
            self.layer = self.dataset.GetLayer()
            logging.info("Shape: {} was read successfully".format(self.name))
        except Exception:
            logging.error("Shape file could not be read")

    @property
    def shape2dataframe(self):
        """Creates a Geo data frame from the instantiated object
        and add two new columns with the xy coordinates respectively.
        This xy tuples are extracted from a columns of the Geopandas
        named ["geometry"].

        :return: Data frame with x y new columns
        """
        try:
            df_shape = geopandas.read_file(self.address)
            df_shape["x"] = df_shape["geometry"].x
            df_shape["y"] = df_shape["geometry"].y
        except Exception:
            print("Geopandas could not be created")
            sys.exit()
        return df_shape




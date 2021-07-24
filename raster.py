"""Module designated to Raster class

Author : Ricardo Barros
"""

from detrender import *


class Raster:

    def __init__(self, raster_address="", driver="Gtiff", band=band_num):
        """A class used to represent a raster file (.tif)

        Attributes
        ----
        name: String of the files' name
        driver: Object Driver from Gdal
        dataset:Object Dataset from Gdal
        transform: Tuple with pixels information
        projection: String of DEMs' projection
        band: Object Band from Gdal

        Methods:
        ----
        get_band_array: creates a array with a given band and substitutes
        the values -9999 for np.nan
        coord_dataframe: creates a data frame with XYZ coordinates of pixels
        burn: burns a array into a raster (.tif)

        Parameters:
        ____
        :param raster_address: String local address of raster file
        :param driver: Type of driver to open the raster file
        :param band: Integer number of the raster's band
        """
        try:
            self.name = raster_address.split(str(Path("/")))[-1].strip(".tif")
            self.driver = gdal.GetDriverByName(driver)
            self.dataset = gdal.Open(raster_address)
            self.transform = self.dataset.GetGeoTransform()
            self.projection = self.dataset.GetProjection()
            self.band = self.dataset.GetRasterBand(band)
            logging.info("Raster: {} with projection {} was read successfully".format(self.name, self.projection.strip(
                "PROJCS[]").split(",")[0]))
        except:
            logging.error("Raster file could not be read")
            pass

    def get_band_array(self):
        """Creates a array with a given band and substitutes
        the values -9999 for np.nan

        :return: Array of bands' float values
        :return: Vector (flat array of bands' float values)
        """
        band_array = self.band.ReadAsArray()
        band_array[band_array == -9999] = np.nan
        band_array_flat = band_array.reshape(band_array.size, 1)
        return band_array, band_array_flat

    def coord_dataframe(self, array):
        """Creates a data frame with XYZ coordinates of pixels

        :param array: flat array of bands' float values
        :return: data frame with columns [x,y,z]
        """
        table_xyz = gdal.Translate("dem.xyz", self.dataset)
        table_xyz = None
        df = pd.read_csv("dem.xyz", sep=" ", header=None)
        os.remove("dem.xyz")
        df.columns = ["x", "y", "z"]
        df[["z"]] = array
        return df

    def burn(self, array):
        """Creates a (.tif) file from a array and saves it with
        the same projection and transform information of the
        instantiated object.

        :param array: Array nxm of Floats/Int
        :return:None
        """
        try:
            array = np.ma.masked_invalid(array)
            self.driver.Register()
            output_raster = self.driver.Create(
                str(detrended_raster_path) + str(Path("/detrended_raster_")) + str(self.name.split("_")[-1] + ".tif"),
                xsize=array.shape[1],
                ysize=array.shape[0],
                bands=1, eType=gdal.GDT_Float32)
            output_raster.SetGeoTransform(self.transform)
            output_raster.SetProjection(self.projection)
            output_raster_band = output_raster.GetRasterBand(1)

            output_raster_band.WriteArray(array)

            # output_raster_band.SetNoDataValue(np.nan)
            output_raster_band.FlushCache()

            output_raster_band = None
            output_raster = None
        except Exception:
            print("Raster file could not be created")

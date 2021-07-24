# Detrender Tool - Python Solution to Detrend a river Digital Elevation Model (DEM)


## 1. About the Code
### - Purpose
Detrend a piecewise Digital Elevation Model (DEM) of a river.
### - Motivation 
The Detrended DEM is a valuable information for a variety of analyses in River Engineering
such as flood simulations, sediments transports and river modelling. 
After a careful research, we could not find an open source algorithm to detrend a DEM, therefore we decided to develop 
this open source project.
### - Goal
Remove the overall valley slope (loss of elevation) of a given DEM (Digital Elevation Model).
### - Data Flow Diagram
<img src="https://media.github.tik.uni-stuttgart.de/user/2363/files/537af300-751d-11eb-87ba-455bd7ca31ec" width = "800" />

### - Code Diagram (UML)
<img src="https://media.github.tik.uni-stuttgart.de/user/2363/files/877f1280-7608-11eb-9680-db2907106bc6" width = "800" />

## 2. Run the code
___

### - Clone the repository
    $ git clone https://github.tik.uni-stuttgart.de/st166353/detrender.git
### - Prerequisites
Python 3.0\
QGIS 
### - Used Packages 
- `matplotlib.pyplot`
- `numpy`   
- `pandas`
- `geopandas`
- `gdal`
- `os`
- `glob`
- `sys`
- `time`
- `logging`
### - Input Instructions 
To run Detrender Toll, the User has to provide on terminal the local address of two folders
which contains respectively Raster file(s) and Shape file(s), in that oder 
.Alternatively the user can run the example within the code, just running `detrender.py`.
The number of files has to be the same for both folders so that each raster file corresponds to a shape fil 

To ensure the correspond order, it is recommended that the file's names end with number, example: "raster_1" and "thalweg_points_2".


#### 1.Input Raster

 - DEM of the river should not have tributaries. It must have only on main path of the river.
 - Clip your DEM in a **optimized**  way. That means, this toll won't be able to detrend the DEM
 if the clipped raster files are curved. Please see examples in the folder `geodata_example`.
 
#### 2. Input Shape 
Follow the step-by-step below to create a desirable shape file input to run Detrender Tool.

__The shapefiles do not contain the information of the elevation (z).__ 
Then it will be necessary to obtain this data from the DEM and relate them to the corresponding coordinates (X,Y)
from the shapefile. This process can be done using the **Field Calculator**, 
as shown in following steps:

1. Open a piecewise DEM in (QGIS).
1. Create a Shape Line with the same projection of DEM.
1. Use the tool from SAGA `Gradient Vector from Surface` to create a gradient vector field on the DEM.
1. Use the  provided `DEM_style` to paint the DEM. In raster file go to: _properties>>style>>load style_ and choose `DEM_style`
1. Still in properties, inside Band Rendering, change the max and min values to better fit the style on the DEM. Press ok. 
1. With the help of the style and the gradient vector filed draw a Shape Line representing the Thalweg of the DEM.
1. Use the Tool `Points Along Geometry` and choose the previous created line as Input Layer. Define the distance as the larger pixel size of the DEM
1. To save the elevation of the pixels immediately below the Shape points do the following: 
    1. Select the created Shape Points  and open ![Captura de Tela 2021-02-23 às 19 15 04](https://media.github.tik.uni-stuttgart.de/user/2363/files/afbc4080-760b-11eb-8d1b-e16be50c6df0) **Field Caculator** (Upper part, on the right of "ToolBox" button)
    1. Inside **Field Caculator** create a new field, as shown in the Figure 1, with the following properties:
        1. Choose the function _"Expression" >> "Rasters" >> "raster_value"_  
            1. raster_value(DEM name, DEM band number, XY value of Shape Points)  
        1. Output field name = "z" (it must be letter 'z' in lower case)
        1. Output field type = Decimal number (real)




![Captura de Tela 2021-02-23 às 19 35 24](https://media.github.tik.uni-stuttgart.de/user/2363/files/68837f00-760e-11eb-8b39-7c53e029cc8d) \
**Figure 1.** Creating Field named 'z' which saves \
the elevation values of DEM's pixels located at  
the exact Shape Point


----
### Execution
#### - From the Terminal



`python detrender.py [(rasters'_file),
                        (shapes'_file),
                        (print_boolean = 1)
                        (band = 1),
                        (detended_limit=10**(-3))]`
+ *rasters' file*: (STRING) path-like of the folder in the system that contains all 
raster files (.tif) to be detrended
+ *shapes' file*: (STRING) path-like string of the folder in the system that contains all 
shape files (.shp)
+ *print_boolean*: (Optional INT, default=1) choose 1 to plot all figures related to the de
trend process. Choose 0 to not plot it.
+ *band*: (Optional INT, default=1) band of the raster, in which is locates the elations of the pixels.
+ *detrended_limit*: (Optional FLOAT, default=10**-3) limit used to validate a detrended raster is flat enough 
to be considered detrended.
  
One folder named *detrend_rasters* will be automatic created at the save location of the 
folder containing the raster files.\
If `print_boolan = 1`, one folder named *detrender_plotter* will be automatic created at the save location fo the 
folder containing the raster files.\
The path to the folders should not have space on it.

  
#### - Run Example "geodata_example"
To run the example contained inside the folder "geodata_example", one can just run `detrender.py`. The setup 
for running the example is defined in `config.py`. The output will be safed inside the folders "detrended_rasters"
and "plots". 

### Modules and their functions
#### `detrender.py`
This stand alone script contains the logical step-by-step process to detrended a raster file.
It needs the module functions and the classes Thalweg and Raster to run.

**find_files**(directory=None):\
It finds all the .tif or .shp files inside a folder and create list of strings with their raw names

    :param directory: string of directory's address
    :return: list of strings from addresses of all files inside the directory

**detrender**(raster_add, shapefile_add):\
It instantiates one object from the class Raster and one object from class Thalweg. 
It performs all the necessary computations to create a detrended array.
Finally, it creates a .tif of the detrended array and saves it inside the folder "detrended_rasters".

    :param raster_add: string of raster's address
    :param shapefile_add: string of shape's address
    :return: None
    
---
#### `raster.py`
This class is used to represent a raster file (.tif) and its respective attributes. 
Moreover this class also contains the following methods:

**get_band_array**(self):\
Creates a array with a given band and substitutes the values -9999 for np.nan

    :return: Array of bands' float values
    :return: Vector (flat array of bands' float values)

**coord_dataframe**(self, array):\
Creates a data frame with XYZ coordinates of pixels

    :param array: flat array of bands' float values
    :return: data frame with columns [x,y,z]

**burn**(self, array):\
Creates a (.tif) file from an array and saves it with
the same projection and transform information of the 
instantiated object.

    :param array: Array nxm of Floats/Int
    :return:None
        
---

#### `shape.py`
This class is used to represent a shape file and its respective attributes. 
Moreover this class also contains the following methods:

**shape2dataframe**(self):\
Creates a Geo data frame from the instantiated object
and add two new columns with the xy coordinates respectively. 
This xy tuples are extracted from a columns of the Geopandas
named ["geometry"].

    :return: Data frame with x y new columns
    
---- 
#### `thalweg.py`
A class used to represent a shape file of points 
that represents the thalweg line of a DEM. 
This class is child of the class Shape.

@property\
**slope**(self):\
Sets property slope to me changed.

    :return: self.slope

@slope.setter\
**slope**(self, value):\
Sets slope of the Thalweg object to a new value.

    :param value: New value od slope
    :return: None


__ **mul**__'(self, multiplier):\
Magic method to transforms the attribute slope in percentage

    :param multiplier: int 100
    :return: Slope in percentage

__ **gt** __(self, limit):\
Magic method to check if the slope of the detrended DEM is 
lower enough to be considered flat (detrended).

    :param limit: Threshold
    :return: Boolean True if the slope is grater than the limit

@staticmethod\
**find_thal_new_z**(thalweg_df, detrended_array, raster):
Uses the coordinates of the Thalweg points to extract its corresponding 
altitudes of the detrended array.

    :param thalweg_df: Geo data frame with coordinates, altitude
        and distance between points of thalweg
    :param detrended_array: Array with elevation values of detrended DEM
    :param raster: Object from class Raster
    :return: Vector with detrended corresponding altitudes of the thalweg's points

@staticmethod\
**compute_slope**(df, vector_z=np.nan, type="trend"):\
Computes the slope of a regression from 2d points, 
which are generated from the combination of two vectors.

    :param df: Geo data frame with coordinates, altitude
            and distance between points of thalweg
    :param vector_z: vector with altitudes of thalweg's points
    :param type: Type line.
    :return: Integer that represents the slope of the regression line

**check_detrend**(self, raster_object):\
Checks if the DEM respects a limit to be considered detrended.

    :param raster_object: Raster object
    :return: None


----

#### `fun_plot.py`
This module contains all the supplementary functions to run `detrender.py`

**plot_thalweg**(x, y, type_=None, title=None):\
    Plots the a scatter plot with of the vector x and y.\
    It also performs a linear regression from the points and plot the line. \
    Choose type="trend" or "detrend" to plot Altitude vs. Distance of the
    thalweg point and type="plane_view" to plot XY coordinates of the points.
    Also in the type="Plane_view" the regression line is assumed to be
    the "center line" of the DEM.

    :param x: Vector with values of the x-axis
    :param y: Vector with values of the y-axis
    :param type_: String used as condition to set up the plot
     (trend, detrend or plane_view)
    :param title: (Optional) String for the title of the plots
    :return: None

**plot_3d**(df_plane, df_raster, type_=None, title=None):\
    Plots the DEM's Trend Plane if type="trend_plane".\
    it plots the DEM as scatter and Trend Plane if type="trend_plane_and_raster".

    :param df_plane: Data frame containing columns (x,y,z) with values of Trend Plane
    :param df_raster: Data frame containing columns (x,y,z) with values of raster pixels
    :param type_: String used as a condition to set up the plot
    :param title: (Optional) String for the title of the plots
    :return:None

**plotter**(thalweg_df, plane_df, raster_coord_df,
            thalweg_new_z_vector,
            raster_name, thalweg_name):\
Plot all the steps of the detrend process to visualize what is happening with the raster(s).

    :param thalweg_df: Data frame with columns (x,y,z) )
    :param plane_df: Data frame with (x,y,z) values of Trend Plane
    :param raster_coord_df: Data frame with (x,y,z) values of raster
    :param thalweg_new_z_vector: Vector with detrended corresponding
    altitudes of the thalweg's points
    :param raster_name: String with name of raster object
    :param thalweg_name: String with name of raster object
    :return: None
 ----   
#### `fun_support.py`
This module contains support functions for detrender that perform mathematical operations and wrap functions.


**compute_plane**(x, y, normal, point):\
  Computes the z values of the DEM's Trend Plane and organizes it in a dataframe
  
    :param x: Vector with X coordinates of all pixels of DEM (Domain)
    :param y: Vector with Y coordinates of all pixels of DEM (Domain)
    :param: normal A normal vector of the Trend Plane
    :param: point A defined point on the Trend Plane
    :return: Data frame with coordinates (x,y,z) of all points on the plane

**compute_normal**(df):\
    Computes a normal vector to the Trend Plane, given as input a
    data frame with columns (x,y,z) representing the coordinates of the points
    of thalweg.

    :param df: Data frame with (x,y,z) of thalweg's points
    :return: A normal vector to the plane and a point on the plane

**normalize_plane**(band, plane):\
Normalize the Trend Plane such that it can be subtracted by the altitudes of the raster's band array.

    :param band: array with altitude of DEM's pixels
    :param plane: array of z values of the Trend Plane
    :return: Array with normalized values of the Trend Plane

**verify_inputs**(args=None):\
verifies if there are .shp files and .tif files in the given folder and if they are equal in number.

    :param args: List of string with directories names
    :return: None

**log_actions**(fun):\
Wrapper function initiate and close logging actions

    :param fun: Wrapped function
    :return: wrapper

**start_logging**():\
Configurations of logging and action to display the logging actions on terminal

    :return:None

**chronometer**(fun):\
Wrapper function that track the run time of another function

    :param fun:Wrapped function
    :return: Wrapper






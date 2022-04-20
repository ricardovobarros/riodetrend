# Riodetrend - Python Solution to Detrend Digital Elevation Model (DEM)


## 1. About Riodetrend

###  Purpose
Detrend a piecewise Digital Elevation Model (DEM) of a river.
### Motivation 
Detrended DEM is a valuable information for a variety of analyses in River Engineering
such as flood simulations, sediments transports and river modelling. 

However, most known software that remove the trend of DEMs require license. 

Riodetrend is a open source tool that efficiently removes the trend of DEMs with approximately linear Thalweg. However, the tool is not 
limited to DEMs with approximately linear Thalwegs, since a DEM can be clipped into smaller pieces that have the desired linear
overall shape.   
    

### Data Flow Diagram
In general terms, the algorithm first reads a raster (DEM) and a point shapefile (Thalweg) as a arrays. It fits a plane
using the cardinal direction and elevation of Thalweg points. As a second step, DEM array and the plane are subtracted resulting in a 
detrended DEM array. Finally, the detrended array is converted back into a raster (see workflow below).  
  
<img src="https://media.github.tik.uni-stuttgart.de/user/2363/files/537af300-751d-11eb-87ba-455bd7ca31ec" width = "800" />


## 2. Run Riodetrend
___

### - Clone the repository
    $ git clone https://github.tik.uni-stuttgart.de/st166353/detrender.git

### - Requiried packages Packages 
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






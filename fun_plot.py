""" The module contains all the supplementary functions to run detrender

It has to import config.py to run.

Functions
----
    * plot_thalweg: plots the points (x,y) or (z,distance downstream)
    as scatter plot and fit a line on it.

    * plot_3d: plots the trend only Trend plane or with DEM.

    * plotter: plots step-by-step of the detrend process, which
    were previous define by the user in config.py.
"""


from detrender import *


def plot_thalweg(x, y, type_=None, title=None):
    """Plots the a scatter plot with of the vector x and y.
    It also performs a linear regression from the points and plot the line.
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
    """
    fig = plt.figure(figsize=(6.18, 3.82), dpi=150, facecolor="w", edgecolor="gray")
    axes = fig.add_subplot(1, 1, 1)

    # Set up plot according to type.
    if type_ == "trend" or type_ == "detrended_validation":
        colormap = plt.cm.get_cmap("coolwarm")
        label = "Z value of thalweg points"
        ax = axes.scatter(x, y, marker="x", c=y, cmap=colormap, label=label)
        axes.set_xlabel("Distance Downstream [m]", labelpad=10)
        axes.set_ylabel(label, labelpad=10)
        plt.title("{} {} Line".format(title, type_))
    if type_ == "plane_view":
        label = "Thalweg points"
        ax = axes.scatter(x, y, marker="x", color="blue", label=label)
        axes.set_xlabel("X coordinates", labelpad=10)
        axes.set_ylabel("Y coordinates", labelpad=10)
        plt.title('{} "Center Line"'.format(title))

    # Fit a line on the scatter and plot.
    coef = np.polyfit(x, y, 1)
    p = np.poly1d(coef)
    plt.tight_layout()
    ax = axes.plot(x, p(x), linestyle="-", color="red", label="Trend line with slope = " + str(coef[0] * 100) + "%")

    axes.legend(loc="upper right", facecolor="y", edgecolor="k", framealpha=0.5, fontsize=6)
    plt.tight_layout()

    if plots_path is None:
        plt.savefig(str(Path("geodata_example/plots/{} from {}")).format(type_, title))
    else:
        plt.savefig(str(Path("{}/{} from {}")).format(plots_path, type_, title))


def plot_3d(df_plane, df_raster, type_=None, title=None):
    """Plots the DEM's Trend Plane if type="trend_plane".
    it plots the DEM as scatter and Trend Plane if type="trend_plane_and_raster".

    :param df_plane: Data frame containing columns (x,y,z) with values of Trend Plane
    :param df_raster: Data frame containing columns (x,y,z) with values of raster pixels
    :param type_: String used as a condition to set up the plot
    :param title: (Optional) String for the title of the plots
    :return:None
    """
    fig = plt.figure(figsize=(8, 5), dpi=150, facecolor="w", edgecolor='gray')
    ax = fig.add_subplot(111, projection="3d")

    # Set up plot according to type.
    if type_ == "trend_plane":
        ax.scatter(df_plane["x"], df_plane["y"], df_plane["z"], color='r', s=10, marker="o", label="DEM trend plane")
    if type_ == "trend_plane_and_raster":
        ax.scatter(df_raster["x"], df_raster["y"], df_raster["z"], color='b', s=0.005, marker='o',
                   label="DEM pixel elevation")
        ax.plot(df_plane["x"], df_plane["y"], df_plane["z"], color="r", label="DEM trend plane")

    # Set up labels
    ax.set_xlabel("X Coordinate [m]", labelpad=10)
    ax.set_ylabel("Y Coordinate [m]", labelpad=10)
    ax.set_zlabel("Z Elevation [m]", labelpad=10)
    ax.text2D(0.05, 0.95, title, transform=ax.transAxes)
    ax.legend()

    plt.tight_layout()

    if plots_path is None:
        plt.savefig(str(Path("geodata_example/plots/{} from {}")).format(type_, title))
    else:
        plt.savefig(str(Path("{}/{} from {}")).format(plots_path, type_, title))




def plotter(thalweg_df, plane_df, raster_coord_df,
            thalweg_new_z_vector,
            raster_name, thalweg_name):
    """  Plot all the steps of the detrend process to visualize what is happening
    with the raster(s).

    :param thalweg_df: Data frame with columns (x,y,z) )
    :param plane_df: Data frame with (x,y,z) values of Trend Plane
    :param raster_coord_df: Data frame with (x,y,z) values of raster
    :param thalweg_new_z_vector: Vector with detrended corresponding
    altitudes of the thalweg's points
    :param raster_name: String with name of raster object
    :param thalweg_name: String with name of raster object
    :return: None
    """
    if plot_detrender:
        plot_thalweg(thalweg_df["distance"], thalweg_df["z"], "trend", thalweg_name)
        plot_thalweg(thalweg_df["x"], thalweg_df["y"], "plane_view", thalweg_name)
        plot_3d(plane_df, raster_coord_df, "trend_plane", raster_name)
        plot_3d(plane_df, raster_coord_df, "trend_plane_and_raster", raster_name)
        plot_thalweg(thalweg_df["distance"], thalweg_new_z_vector, "detrended_validation", thalweg_name)

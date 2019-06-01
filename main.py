from files import organized
from SQL import sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal
from mpl_toolkits.mplot3d.axes3d import Axes3D
import sys
from pathlib import Path
file = Path(Path.cwd()) / Path('gmted_small.tif')
def raster(src_ds):
    print("[ RASTER BAND COUNT ]: ", src_ds.RasterCount)
    for band in range( src_ds.RasterCount ):
        band += 1
        print("[ GETTING BAND ]: ", band)
        srcband = src_ds.GetRasterBand(band)
        if srcband is None:
            continue
    
        stats = srcband.GetStatistics( True, True )
        if stats is None:
            continue
    
        print("[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
                    stats[0], stats[1], stats[2], stats[3] ))

def my_graph():
    dem = gdal.Open(str(file))
    if dem == None:
        print('Unable to open .tiff file')
    raster(dem)
    print(dem.GetMetadata())
    gt = dem.GetGeoTransform()
    dem = dem.ReadAsArray()
    fig, ax = plt.subplots(figsize=(16, 8), subplot_kw={'projection': '3d'})
    
    xres = gt[1]
    yres = gt[5]
    
    print(xres)
    print(yres)
    
    X = np.arange(gt[0], gt[0] + dem.shape[1]*xres, xres)
    Y = np.arange(gt[3], gt[3] + dem.shape[0]*yres, yres)
    
    print(X)
    print(Y)

    X, Y = np.meshgrid(X, Y)

    print(X)
    print(Y)
    
    surf = ax.plot_surface(X,Y, dem, rstride=1, cstride=1, cmap=plt.cm.RdYlBu_r, vmin=0, vmax = 400)
    
    ax.set_zlim(0, 60000)
    ax.view_init(60, -105)
    
    fig.colorbar(surf, shrink=0.4, aspect=20)

    
    plt.show()

if __name__ == '__main__':
    my_graph()
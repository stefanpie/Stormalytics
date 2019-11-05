import os
import matplotlib.pyplot as plt
import netCDF4
import numpy as np

from cartopy import config
import cartopy.crs as ccrs


# get the path of the file. It can be found in the repo data directory.
fname = "../../data/hursat_mw/raw_data_extracted/HURSAT-mw_v05_1992230N11325_ANDREW/1992230N11325.ANDREW.1992.08.24.1447.17.F10.101.hursat-mw.v05.nc"

dataset = netCDF4.Dataset(fname)
dataset.set_auto_scale(True)
dataset.set_auto_mask(False)
print(dataset)

lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]


data_layer_h = dataset.variables['T85H'][:,:]
data_layer_v = dataset.variables['T85V'][:,:]



data_layer_h = np.where(data_layer_h==-1, 0, data_layer_h)
data_layer_v = np.where(data_layer_v==-1, 0, data_layer_v)

pct = (1.7*data_layer_v) - (0.7*data_layer_h)
pct = np.where(pct==0, np.nan, pct)

print(pct)

# print(data_layer)
# plt.imshow(data_layer)
# plt.show()

# where_are_NaNs = np.isnan(data_layer)
# data_layer[where_are_NaNs] = 0
# print(data_layer)


ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ps = plt.pcolormesh(lons, lats, pct, transform=ccrs.PlateCarree())
plt.colorbar(ps)


plt.show()

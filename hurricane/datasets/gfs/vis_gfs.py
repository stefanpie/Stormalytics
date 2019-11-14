import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from skimage import measure



import netCDF4

from cartopy import config
import cartopy.crs as ccrs


# get the path of the file. It can be found in the repo data directory.
fname = "../../data/gfs/netcdf_data/gfsanl_3_20170904_0600_000.nc"

dataset = netCDF4.Dataset(fname)
dataset.set_auto_scale(True)
dataset.set_auto_mask(False)
# print(dataset)

lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]


X = dataset.variables['Cloud_mixing_ratio_isobaric'][0, :, :, :]

X = np.moveaxis(X, 0, -1)
slices = X.shape[-1]
print(slices)
print(np.min(X))
print(np.max(X))

ax = plt.axes(projection=ccrs.PlateCarree())
plt.contourf(lons, lats, X[:,:,15], transform=ccrs.PlateCarree())
ax.coastlines()
plt.show()

# print("running marching cubes")
# verts, faces, _, _ = measure.marching_cubes_lewiner(X, 0.0002)

# print("plotting")

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_trisurf(verts[:, 0], verts[:,1], faces, verts[:, 2], cmap='Spectral', lw=1)
# plt.show()
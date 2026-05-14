dp = "data/topaz4_arctic_velocity_2004_2025.nc"

# lazy load the data
import xarray as xr
ds = xr.open_dataset(dp)
# Dataset info:
''' Time: 2004-01-01 to 2025-12-01, 264 monthly steps
Lat: 50-90N (321 points), Lon: -180 to 180 (2880 points), Depth: 0-4000m (40 levels)

Variables:
- vxo, vyo       eastward/northward velocity (m/s), 4D, 39GB each
- thetao         potential temperature (degrees_C), 4D, 39GB
- so             salinity (PSU), 4D, 39GB
- mlotst         mixed layer depth (m), 3D, 976MB
- zos            sea surface height (m), 3D, 976MB
- model_depth    bathymetry (m), 2D, 4MB

Velocity is already rotated to geographic east/north by CMEMS at download -- no further rotation needed.
'''

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import imageio
from io import BytesIO

dp = "data/topaz4_arctic_velocity_2004_2025.nc"
ds = xr.open_dataset(dp)

frames = []

for t in range(60):  # 5 years = 60 months
    vxo_surf = ds['vxo'].isel(time=t, depth=0)
    vyo_surf = ds['vyo'].isel(time=t, depth=0)

    lon = vxo_surf.longitude.values
    lat = vxo_surf.latitude.values
    lon2d, lat2d = np.meshgrid(lon, lat)

    stride = 20

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": ccrs.NorthPolarStereo()})
    ax.set_extent([-180, 180, 50, 90], ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    ax.quiver(lon2d[::stride, ::stride], lat2d[::stride, ::stride],
              vxo_surf.values[::stride, ::stride], vyo_surf.values[::stride, ::stride],
              transform=ccrs.PlateCarree(), scale=5)

    timestamp = str(ds.time.values[t])[:7]
    ax.set_title(f'Surface Velocity (m/s) - {timestamp}')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    frames.append(imageio.imread(buf))
    print(f"Frame {t+1}/60 done")

imageio.mimsave('surface_velocity_2004_2008.gif', frames, fps=4)
print("Saved: surface_velocity_2004_2008.gif")
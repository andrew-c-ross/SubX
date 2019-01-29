import numpy as np
import os
import xarray

mod = 'GEFS'

# var = 'tas'
# level = '2m'

# var = 'uas'
# level = 'None'

var = 'vas'
level = 'None'

inpath = '/Volumes/Data/subx/hindcast/{}/{}/{}/daily/anom/1999-01-07.2015-12-30.daily_anomalies.nc'.format(mod, var, level)
outpath = '/Volumes/Data/subx/hindcast/{}/{}/{}/daily/standarddeviation/1999-01-07.2015-12-30.standarddeviation.nc'.format(mod, var, level)

anom = xarray.open_dataarray(inpath)

print('Calculating standard deviation')
stdev = anom.groupby('S.dayofyear').std(['M', 'S'])

print('Filling')
x = np.empty((366, len(stdev.L), len(stdev.Y), len(stdev.X)))
x.fill(np.nan)
_da = xarray.DataArray(
    x,
    coords=[
        np.linspace(1, 366, num=366, dtype=np.int64),
        stdev.L,
        stdev.Y,
        stdev.X
    ],
    dims = stdev.dims
)
filled = stdev.combine_first(_da)

print('Smoothing')
smooth = filled.copy()
for i in range(2):
    smooth = xarray.concat([smooth[-15:], smooth, smooth[:15]], 'dayofyear')
    smooth = (
        smooth
        .pipe(np.power, 2)
        .rolling(dayofyear=31, center=True, min_periods=1)
        .mean()
        .pipe(np.sqrt)
        .isel(dayofyear=slice(15, -15))
    )

final = smooth.sel(dayofyear=filled.dayofyear)

print('Writing')
if not os.path.isdir(os.path.dirname(outpath)):
    os.makedirs(os.path.dirname(outpath))

final.to_netcdf(outpath)
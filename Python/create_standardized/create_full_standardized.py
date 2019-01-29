import numpy as np
import os
import xarray


mod = 'GEFS'

# var = 'tas'
# level = '2m'

var = 'vas'
level = 'None'

# var = 'vas'
# level = 'None'

anoms_file = '/Volumes/Data/subx/hindcast/{}/{}/{}/daily/anom/1999-01-07.2015-12-30.daily_anomalies.nc'.format(mod, var, level)
std_file = '/Volumes/Data/subx/hindcast/{}/{}/{}/daily/standarddeviation/1999-01-07.2015-12-30.standarddeviation.nc'.format(mod, var, level)
outpath = '/Volumes/Data/subx/hindcast/{}/{}/{}/daily/standardized/1999-01-07.2015-12-30.standardized.nc'.format(mod, var, level)

print('Opening')
anom = xarray.open_dataarray(anoms_file, chunks={'S': 100})
std = xarray.open_dataarray(std_file, chunks={'dayofyear': 100})

print('Dividing')
standardized = anom.groupby('S.dayofyear') / std

print('Writing')
if not os.path.isdir(os.path.dirname(outpath)):
    os.makedirs(os.path.dirname(outpath))

standardized.to_netcdf(outpath)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 18:32:20 2022

@author: jeremybenik
"""

# %% importing libraries
print("importing libraries")
import pandas as pd
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import wrf
import statistics as st
import glob
# %% Reading in the files
fuels_14 = nc.Dataset('14_namelist_fire/wrfout_d01_0001-01-01_00:00:00')

fuels_40 = nc.Dataset('40_Scott_Burgen/wrfout_d01_0001-01-01_00:00:00')

# %% Reading in the ROS and fire ground heat flux
print('Reading in ROS from file 14')
ROS_14 = wrf.getvar(fuels_14, "ROS", timeidx = None)
print('Reading in ROS from file 40')
ROS_40 = wrf.getvar(fuels_40, "ROS", timeidx = None)

# Fire ground heat flux
print('Reading in FGRNHFX from file 14')
aaa = wrf.getvar(fuels_14, 'FGRNHFX', None)
print('Reading in FGRNHFX from file 40')
bbb = wrf.getvar(fuels_40, 'FGRNHFX', None)

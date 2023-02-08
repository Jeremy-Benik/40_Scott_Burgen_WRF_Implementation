#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:35:54 2023

@author: jeremybenik
"""

# %% Importing necessary Libraries
# Reading in necessary libraries
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import wrf
import glob
# %% Going through one file to see what is inside of it, then will probably iteratre through all files

# Setting the path to my files
path1 = r'/Users/jeremybenik/Research_Files/40_Scott_Burgen_WRF_Implementation/simulations/Albini/'
path2 = r'/Users/jeremybenik/Research_Files/40_Scott_Burgen_WRF_Implementation/simulations/Scott_Burgan/'

# Setting the path and saying I want to iterate through my .csv files
filenames_Albini = glob.glob(path1 + "fuel_*/wrfout_*") 
filenames_Scott_Burgan = glob.glob(path2 + "fuel_*/wrfout_*")


label_scott = ['GR7', 'GR2', 'GR8', 'SH5', 'SH7', 'SH4', 'SH4', 'TL3', 'TL9', 
               'TU5', 'SB1', 'SB2', 'SB2']
label_albini = np.arange(1, 14)
# %% Looping through the files and plotting them.

for i in range(0, 13):   

    #  Reading in the files
    print('Reading in the file')

    Albini = nc.Dataset(filenames_Albini[i])
    
    Scott_Burgan = nc.Dataset(filenames_Scott_Burgan[i])
    
    # Reading in variables (fire winds first)
    
    # fire_albini = wrf.getvar(Albini, 'AVG_FUEL_FRAC', None)
    
    fire_albini = wrf.getvar(Albini, 'FIRE_AREA', None)
    
    fire_scott_burgan = wrf.getvar(Scott_Burgan, 'FIRE_AREA', None)
    
    # fire_scott_burgan = wrf.getvar(Scott_Burgan, 'AVG_FUEL_FRAC', None)
    
    
    fgrnhfx_Albini = wrf.getvar(Albini, "FGRNHFX", None)
    
    fgrnhfx_Scott_Burgan = wrf.getvar(Scott_Burgan, "FGRNHFX", None)   
     
    lat_albini = wrf.getvar(Albini, "XLAT", None)[0, :, 0]
    lon_albini = wrf.getvar(Albini, "XLONG", None)[0, 0, :]
    
    lat_Scott_Burgan = wrf.getvar(Scott_Burgan, "XLAT", None)[0, :, 0]
    lon_Scott_Burgan = wrf.getvar(Scott_Burgan, "XLONG", None)[0, 0, :]
    
    fxlat_albini = wrf.getvar(Albini, "FXLAT", None)[0, :, 0]
    fxlon_albini = wrf.getvar(Albini, "FXLONG", None)[0, 0, :]
    
    fxlat_Scott_Burgan = wrf.getvar(Scott_Burgan, "FXLAT", None)[0, :, 0]
    fxlon_Scott_Burgan = wrf.getvar(Scott_Burgan, "FXLONG", None)[0, 0, :]
    
    u = wrf.getvar(Albini, "ua", timeidx = 0, units = "m/s")[0, :, :]
    
    v = wrf.getvar(Albini, "va", timeidx = 0, units = "m/s")[0, :, :]
    
    ws = np.sqrt((u ** 2) + (v ** 2))
    u_ = wrf.getvar(Scott_Burgan, "ua", units = "m/s")[0, :, :]
    
    v_ = wrf.getvar(Scott_Burgan, "va", units = "m/s")[0, :, :]
    
    ws_ = np.sqrt((u_ ** 2) + (v_ ** 2))
    #  Plotting the fire areas from the coupled and uncoupled simulations
    print('Creating the plot')
    # Change step if you want fewer vectors on the plot. I find 8 for a 5m resolution
    # Simulation is perfect
    if fgrnhfx_Albini.max() > fgrnhfx_Scott_Burgan.max():
        aaa = fgrnhfx_Albini.max()
    else:
        aaa = fgrnhfx_Scott_Burgan.max()
        
    levels = np.linspace(0, aaa, 501)
    m = 5
    fig, ax = plt.subplots(2, 2, figsize=(14, 12), dpi=200)
    
    ax[0, 0].contour(fxlat_albini[:], fxlon_albini[:], fire_albini[-1, :, :], colors="blue")
    ax[0, 0].contour(fxlat_albini[:], fxlon_albini[:], fire_albini[60, :, :], colors="red")
    ax[0, 0].contour(fxlat_albini[:], fxlon_albini[:], fire_albini[120, :, :], colors="green")
    
    im = ax[0, 0].quiver(lat_albini[::m], lon_albini[::m], u[::m, ::m], v[::m, ::m], ws[::m, ::m], cmap = 'hsv', clim = [9, 9.5])
    ax[0, 1].quiver(lat_albini[::m], lon_albini[::m], u[::m, ::m], v[::m, ::m], ws[::m, ::m], cmap = 'hsv', clim = [9, 9.5])
    
    
    
    ip = ax[0, 1].contour(fxlat_albini[:], fxlon_albini[:], fgrnhfx_Albini[-1, :, :], levels, cmap = 'gist_ncar')
    ax[0, 1].contour(fxlat_albini[:], fxlon_albini[:], fgrnhfx_Albini[60, :, :], levels, cmap = 'gist_ncar')
    ax[0, 1].contour(fxlat_albini[:], fxlon_albini[:], fgrnhfx_Albini[120, :, :], levels, cmap = 'gist_ncar')
    
    ax[1, 0].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fire_scott_burgan[-1, :, :], colors="blue")
    ax[1, 0].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fire_scott_burgan[60, :, :], colors="red")
    ax[1, 0].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fire_scott_burgan[120, :, :], colors="green")
    
    
    ax[1, 1].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fgrnhfx_Scott_Burgan[-1, :, :], levels, cmap = 'gist_ncar')
    ax[1, 1].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fgrnhfx_Scott_Burgan[60, :, :], levels, cmap = 'gist_ncar')
    ax[1, 1].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:], fgrnhfx_Scott_Burgan[120, :, :], levels, cmap = 'gist_ncar')
    
    ax[1, 0].quiver(lat_albini[::m], lon_albini[::m], u_[::m, ::m], v_[::m, ::m], ws_[::m, ::m], cmap = 'hsv', clim = [9, 9.5])
    ax[1, 1].quiver(lat_albini[::m], lon_albini[::m], u_[::m, ::m], v_[::m, ::m], ws_[::m, ::m], cmap = 'hsv', clim = [9, 9.5])
    
    
    ax[1, 0].set_xlabel('Meters From Origin', fontsize = 15, fontweight = 'bold')
    ax[1, 1].set_xlabel('Meters From Origin', fontsize = 15, fontweight = 'bold')
    
    ax[0, 0].set_ylabel('Meters From Origin', fontsize = 15, fontweight = 'bold')
    ax[1, 0].set_ylabel('Meters From Origin', fontsize = 15, fontweight = 'bold')

    ax[0, 0].set_title(f"Fire Area From Fuel Type {label_albini[i]}", fontsize = 15, fontweight = 'bold')
    
    ax[0, 1].set_title(f"Fire Ground Heat Flux From Fuel Type {label_albini[i]}", fontsize = 15, fontweight = 'bold')
    
    ax[1, 1].set_title(f"Fire Ground Heat Flux From {label_scott[i]}", fontsize = 15, fontweight = 'bold')
    
    ax[1, 0].set_title(f"Fire Area From {label_scott[i]}", fontsize = 15, fontweight = 'bold')
    
    plt.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.82, 0.15, 0.04, 0.7])
    pg = plt.colorbar(ip, cax=cbar_ax)
    pg.set_label('Fire Ground Heat Flux (W/m^2)', fontsize = 15, fontweight = 'bold')
    
    
    plt.subplots_adjust(bottom=0.2)
    cmar_ax = fig.add_axes([0.1, 0.1, 0.7, 0.04])
    pl = plt.colorbar(im, cax=cmar_ax, orientation = "horizontal")
    pl.set_label('Wind Speed (m/s)', fontsize = 15, fontweight = 'bold')
    ax[0, 0].grid()
    ax[0, 1].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    plt.show()
    plt.close(fig)

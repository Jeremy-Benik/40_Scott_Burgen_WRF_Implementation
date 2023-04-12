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
from matplotlib import cm
from matplotlib.colors import ListedColormap
import seaborn as sns
import pandas as pd
# %% Going through one file to see what is inside of it, then will probably iteratre through all files

# Setting the path to my files

path1 = r'../Simulations/Albini_fuels/fuel_*'
path2 = r'../Simulations/Scott_Burgan/fuel_*'

# Setting the path and saying I want to iterate through my .csv files
filenames_Albini = glob.glob(path1 + "fuel_*/wrfout_*")
filenames_Scott_Burgan = glob.glob(path2 + "fuel_*/wrfout_*")

# Setting the labels for use with titles
label_scott = ['GR7', 'GR2', 'GR8', 'SH5', 'SH7', 'SH4', 'SH4', 'TL3', 'TL9',
               'TU5', 'SB1', 'SB2', 'SB2']
# %% So it turns out that plotting them in a for loop doesn't work so I will just do them individually
#  Reading in the files
print('Reading in the file')
path_al = '../Simulations/Scott_Burgan/fire_atms_0/fuel_3/wrfout_d01_0001-01-01_00:00:00'
Albini = nc.Dataset(path_al)

Scott_Burgan = nc.Dataset('../Simulations/Albini_fuels/fire_atms_0/fuel_3/wrfout_d01_0001-01-01_00:00:00')
# m = -33
# n = -31
m = -32
n = -31
# Reading in variables (fire winds first)

# Reading in the fire area for plotting the fire contours
print('I am reading in the fire area for the Albini file')
fire_albini = wrf.getvar(Albini, 'FIRE_AREA', timeidx = 180)

print('I am reading in the fire area for the S&B file')
fire_scott_burgan = wrf.getvar(Scott_Burgan, 'FIRE_AREA', timeidx = 180)



print(fire_albini.sum()*36/4046.86)
print(fire_scott_burgan.sum()* 36/4046.86)
# %%

'''
1 = 
albini = 150.90204775
Scott and Burgan = 75.20719768

2 = 
Albini = 57.88255914
Scott and Burgan = 46.96434589

3 = 
157.78510994
119.03506669

4 = 
172.72935259
173.33200733

5 = 
137.58338834
88.44428342

6 = 
107.47243889
36.21022036

7 = 
107.49380963
42.03624558

8 = 
3.92828218
4.5856207

9=
13.11480669
15.84221533

10=
19.43905999
22.91151349

11=
10.35967257
9.68472436

12=
20.99880877
17.42675764

13=
20.99880877
19.42101648
'''
# Albini_fire_area = [150.90204775, 57.88255914, 157.78510994, 172.72935259, 137.58338834, 107.47243889, 
#           107.49380963, 3.92828218, 13.11480669, 19.43905999, 10.35967257, 20.99880877, 20.99880877]

# Scott_Burgan_fire_area = [75.20719768, 46.96434589, 119.03506669, 173.33200733, 88.44428342, 36.21022036,
#                           42.03624558, 4.5856207, 15.84221533, 22.91151349, 9.68472436, 17.42675764, 19.42101648]


Albini_fire_area = [80.49225008710457, 58.66166579, 105.34234992, 60.58427186, 72.31483802, 37.55157065, 
          42.82212397, 4.58651766, 15.89401548, 22.79925198, 9.79211014, 17.9085157, 19.91801205 ]

Scott_Burgan_fire_area = [98.27847045301789, 63.34904127, 98.19899043, 71.38930274, 73.59021485, 78.57042154, 
                          78.58086366, 3.92831258, 13.21413609, 19.52490345, 10.37633696, 21.00451415, 21.00451415]


# %% Plotting the scale
names = np.arange(1, 14)

fig = plt.figure(figsize = (10, 8))
plt.bar(names + 0.2, Albini_fire_area, 0.4, label = "Albini")
plt.bar(names - 0.2, Scott_Burgan_fire_area, 0.4, label = "Scott and Burgan")

plt.ylabel("Acres Burned", fontsize = 12, fontweight = 'bold')
plt.xlabel("Fuel Type", fontsize = 12, fontweight = 'bold')
plt.xticks(names)
plt.grid()
plt.legend()
fig.set_dpi(500)
plt.tight_layout()
plt.show()
# Now we are plotting the scale
scale = []
for i in range(len(names)):
    scale.append(Albini_fire_area[i] / Scott_Burgan_fire_area[i])
    
fig = plt.figure(figsize = (10, 8))
plt.bar(names, scale, color = 'blue')
plt.xticks(names, fontsize = 12)
plt.yticks(fontsize = 12)
plt.ylabel("Scale", fontsize = 12, fontweight = 'bold')
plt.xlabel('Fuel Category', fontsize =12, fontweight = 'bold')
plt.title("Fire Area Scale From Albini and Scott And Burgan Fuels (Albini / S&B) FIRE_ATMS_1", fontsize = 15, fontweight = 'bold')
plt.grid()
fig.set_dpi(500)
plt.tight_layout()
plt.show()
# %%
print('Reading in latitude and longitude')
fgrnhfx_Albini = wrf.getvar(Albini, "FGRNHFX", timeidx = 180) / 1000

fgrnhfx_Scott_Burgan = wrf.getvar(Scott_Burgan, "FGRNHFX", timeidx = 180) / 1000

lat_albini = wrf.getvar(Albini, "XLAT", timeidx = 180)[:, 0]
lon_albini = wrf.getvar(Albini, "XLONG", timeidx = 180)[0, :]

lat_Scott_Burgan = wrf.getvar(Scott_Burgan, "XLAT", timeidx = 180)[:, 0]
lon_Scott_Burgan = wrf.getvar(Scott_Burgan, "XLONG", timeidx = 180)[0, :]

fxlat_albini = wrf.getvar(Albini, "FXLAT", timeidx = 180)[:, 0]
fxlon_albini = wrf.getvar(Albini, "FXLONG", timeidx = 180)[0, :]

fxlat_Scott_Burgan = wrf.getvar(Scott_Burgan, "FXLAT", timeidx = 180)[:, 0]
fxlon_Scott_Burgan = wrf.getvar(Scott_Burgan, "FXLONG", timeidx = 180)[ 0, :]

print('I am reading in U from the Albini simulation')
u = wrf.getvar(Albini, "ua", timeidx = 180, units="m/s")[0, :, :]
print('I am reading in V from the Albini simulation')
v = wrf.getvar(Albini, "va", timeidx = 180, units="m/s")[0, :, :]
print('Calculating the Horizontal Wind Speed')
ws = np.sqrt((u ** 2) + (v ** 2))

print(' I am reading in U from the S&B simulation')
u_ = wrf.getvar(Scott_Burgan, "ua", timeidx = 180, units="m/s")[0, :, :]

print(' I am reading in V from the S&B simulation')
v_ = wrf.getvar(Scott_Burgan, "va", timeidx = 180, units="m/s")[0, :, :]
print('I am calculating the hotizontal wind speed')
ws_ = np.sqrt((u_ ** 2) + (v_ ** 2))
#  Plotting the fire areas from the coupled and uncoupled simulations

print('Creating the plot')
# Change step if you want fewer vectors on the plot. I find 8 for a 5m resolution
# Simulation is perfect
# %%
if fgrnhfx_Albini.max() > fgrnhfx_Scott_Burgan.max():
    aaa = fgrnhfx_Albini.max()
else:
    aaa = fgrnhfx_Scott_Burgan.max()

viridis = cm.get_cmap('Reds', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([256/256, 256/256, 256/256, 1])
newcolors[:2, :] = white
newcmp = ListedColormap(newcolors)

# %%
k = 3

levels = np.linspace(0, 18, 91)

fig, ax = plt.subplots(2, 2, figsize=(9, 7))

ip = ax[0, 1].contourf(fxlat_albini[:], fxlon_albini[:],
                       fgrnhfx_Albini[:, :], levels, cmap=newcmp)

ax[1, 1].contourf(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:],
                  fgrnhfx_Scott_Burgan[:, :], levels, cmap=newcmp)

im = ax[0, 0].quiver(lat_albini[::k], lon_albini[::k], u[::k, ::k],
                     v[::k, ::k], ws[::k, ::k], cmap='turbo', clim=[5, 15])

# ax[0, 1].quiver(lat_albini[::k], lon_albini[::k], u[::k, ::k],
# v[::k, ::k], ws[::k, ::k], cmap='nipy_spectral', clim=[5, 15])

ax[1, 0].quiver(lat_albini[::k], lon_albini[::k], u_[::k, ::k], v_[
    ::k, ::k], ws_[::k, ::k], cmap='turbo', clim=[5, 15])
# ax[1, 1].quiver(lat_albini[::k], lon_albini[::k], u_[::k, ::k], v_[
# ::k, ::k], ws_[::k, ::k], cmap='nipy_spectral', clim=[5, 15])

ax[0, 0].contour(fxlat_albini[:], fxlon_albini[:],
                 fire_albini[:, :], colors="blue")


ax[1, 0].contour(fxlat_Scott_Burgan[:], fxlon_Scott_Burgan[:],
                 fire_scott_burgan[:, :], colors="blue")


ax[1, 0].set_xlabel('Meters From Origin', fontsize=12, fontweight='bold')
ax[1, 1].set_xlabel('Meters From Origin', fontsize=12, fontweight='bold')

ax[0, 0].set_ylabel('Meters From Origin', fontsize=12, fontweight='bold')
ax[1, 0].set_ylabel('Meters From Origin', fontsize=12, fontweight='bold')

ax[0, 0].set_title(f"Fire Area From Fuel Type {int(path_al[m:n])}",
                   fontsize=12, fontweight='bold')

ax[0, 1].set_title(f"Fire Ground Heat Flux From Fuel Type {int(path_al[m:n])}",
                   fontsize=12, fontweight='bold')

ax[1, 1].set_title(f"Fire Ground Heat Flux From {label_scott[int(path_al[m:n]) - 1]}",
                   fontsize=12, fontweight='bold')

ax[1, 0].set_title(
    f"Fire Area From {label_scott[int(path_al[m:n]) - 1]}", fontsize=12, fontweight='bold')

plt.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.83, 0.15, 0.04, 0.7])
pg = plt.colorbar(ip, cax=cbar_ax)
pg.set_label('Fire Ground Heat Flux (KW/m^2)', fontsize=12, fontweight='bold')
pg.ax.tick_params(labelsize=12)
pg.update_ticks()
plt.subplots_adjust(bottom=0.2)
cmar_ax = fig.add_axes([0.1, 0.07, 0.7, 0.04])
pl = plt.colorbar(im, cax=cmar_ax, orientation="horizontal")
pl.set_label('Wind Speed (m/s)', fontsize=12, fontweight='bold')
pl.ax.tick_params(labelsize=12)

ax[0, 0].grid()
ax[0, 1].grid()
ax[1, 0].grid()
ax[1, 1].grid()
ax[0, 0].set_xticklabels([])
ax[0, 1].set_yticklabels([])
ax[0, 1].set_xticklabels([])
ax[1, 1].set_yticklabels([])

fig.set_dpi(500.0)
# plt.savefig(f'images/fire_area_fuel_{int(path_al[m:n])}.png')
plt.show()
plt.close(fig)

# %% creating a bar plot
areas = {'Fuel Category (Albini)': [], 'Scott and Burgan': [],'Albini': []}

areas['Fuel Category (Albini)'].append(1)
areas['Scott and Burgan'].append((wrf.to_np(fire_scott_burgan).sum()*6 * 6)/4046.86)
# areas['Balbi'].append(ds2['FIRE_AREA'][-1].sum()*fdx*fdy/4046.86)
areas['Albini'].append((wrf.to_np(fire_albini).sum()*6*6)/4046.86)


fig,ax = plt.subplots(2,1,sharex=True, figsize = (10, 8))
df = pd.DataFrame(areas).set_index('Fuel Category (Albini)')
df.plot.bar(ax=ax[0],color=['r','b'])
df['Scale'] = df['Scott and Burgan']/df['Albini']
color = ['g' if s <= 1. else 'r' for s in df['Scale']]
df.plot.bar(ax=ax[1],color=['g'],y='Scale',legend=False)
# df.plot.bar(ax=ax[1],color=['b','g'],y=['Scale_Balbi','Scale_Behave'],legend=False)
ax[0].set_ylabel('Fire Area (acres)', fontsize = 12, fontweight = 'bold')
ax[1].set_xlabel('Fuel Category', fontsize = 12, fontweight = 'bold')
ax[1].set_title('Scaling Factor For The Area Burnt in S&B Compared to Albini (S&B / Albini)', fontsize = 15, fontweight = 'bold')
ax[0].set_title('Total Area Burnt (Acres)', fontsize = 15, fontweight = 'bold')
ax[1].set_ylabel('Scale', fontsize = 12, fontweight = 'bold')
ax[1].grid()
ax[0].grid()
ax[1].set_ylim(0.8, 1.05)
plt.suptitle(f'Comparison of Total Acres Burnt From {label_scott[int(path_al[m:n]) - 1]} and Fuel Type {int(path_al[m:n])}', fontsize = 18, fontweight = 'bold')
fig.set_dpi(500)
plt.tight_layout()
# plt.savefig(f'images/bar_plots/bar_plot_fuel_{int(path_al[m:n])}.png')

plt.show()



# %% creating a violin plot

columns = np.array(['Scott and Burgan', 'Albini'])

Scott_WS = np.transpose(wrf.to_np(ws_))
Albini_WS = np.transpose(wrf.to_np(ws))
Wind_Speeds = np.vstack((Scott_WS, Albini_WS)).flatten()

name_1 = []
name_2 = []
for i in range(3362):
    if i <= 1680:
        name_1.append(columns[0])
    else:
        name_2.append(columns[1])
Fuel_Name = np.vstack((name_1, name_2)).flatten()

d = {'Fuel Category': Fuel_Name, 'Wind Speed (m/s)': Wind_Speeds}
df = pd.DataFrame(data=d)

# %% Plotting violin plot
fig, ax = plt.subplots(figsize=(10, 8))
sns.boxplot(data=df, x='Fuel Category', y='Wind Speed (m/s)')

ax.set_xlabel(ax.get_xlabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.set_ylabel(ax.get_ylabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.grid()
ax.tick_params(axis='x', labelsize=12)
ax.set_title(
    f'Horizontal Wind Speed Distribution for {label_scott[int(path_al[m:n]) - 1]} and Fuel Type {int(path_al[m:n])}', fontsize=18, fontweight='bold')
fig.set_dpi(500)
plt.tight_layout()
# plt.savefig(
    # f'images/violin_plots/violin_plot_fuel_{int(path_al[m:n])}.png')
plt.show()

# %% plotting box and whisker plot

Scott_fire = np.transpose(wrf.to_np(fgrnhfx_Scott_Burgan))
Albini_fire = np.transpose(wrf.to_np(fgrnhfx_Albini))
name_1_fire = []
name_2_fire = []
for i in range((fire_albini.shape[1] ** 2) * 2):
    if i <= 176399:
        name_1_fire.append(columns[0])
    else:
        name_2_fire.append(columns[1])
Fire_name = np.vstack((name_1_fire, name_2_fire)).flatten()

Fire = np.vstack((Scott_fire, Albini_fire)).flatten()
data = Scott_fire
data1 = data[data != 0]

e = {'Fuel Category': Fire_name, "Fire Ground Heat Flux (KW/m^2)": Fire}
df_2 = pd.DataFrame(data=e)


fig, ax = plt.subplots(figsize=(10, 8))
sns.boxplot(data=df_2, x='Fuel Category', y='Fire Ground Heat Flux (KW/m^2)')

ax.set_xlabel(ax.get_xlabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.set_ylabel(ax.get_ylabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.grid()
ax.tick_params(axis='x', labelsize=12)
ax.set_title(
    f'Fire Ground Heat Flux Distribution for {label_scott[int(path_al[m:n]) - 1]} and Fuel Type {int(path_al[m:n])}', fontsize=18, fontweight='bold')
fig.set_dpi(500)
plt.tight_layout()
# plt.savefig(
    # f'images/box_whisker_plots/box_whisker_plot_fuel_{int(path_al[m:n])}.png')
plt.show()

# %%
Scott_fire_1 = np.transpose(wrf.to_np(fgrnhfx_Scott_Burgan)).flatten()
Scott_fire = Scott_fire_1[Scott_fire_1 >= 1]
Albini_fire_1 = np.transpose(wrf.to_np(fgrnhfx_Albini)).flatten()
Albini_fire = Albini_fire_1[Albini_fire_1 >= 1]

df_1 = pd.DataFrame({'Fuel Category' : 'Scott and Burgan', 'Fire Ground Heat Flux (KW/m^2)' : Scott_fire})

df_2 = pd.DataFrame({'Fuel Category' : 'Albini', 'Fire Ground Heat Flux (KW/m^2)' : Albini_fire})

df = pd.concat((df_1, df_2))

fig, ax = plt.subplots(figsize=(10, 8))
sns.violinplot(data=df, x='Fuel Category', y='Fire Ground Heat Flux (KW/m^2)')

ax.set_xlabel(ax.get_xlabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.set_ylabel(ax.get_ylabel(), fontdict={'size': 15, 'weight': 'bold'})
ax.grid()
ax.tick_params(axis='x', labelsize=12)
ax.set_ylim(0, 1000)
ax.set_title(
    f'Fire Ground Heat Flux Distribution for {label_scott[int(path_al[m:n]) - 1]} and Fuel Type {int(path_al[m:n])}', fontsize=18, fontweight='bold')
fig.set_dpi(500)
plt.tight_layout()
# plt.savefig(
    # f'images/box_whisker_plots/box_whisker_plot_fuel_{int(path_al[m:n])}.png')
plt.show()

# %%












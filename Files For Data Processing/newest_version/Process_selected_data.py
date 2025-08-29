# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:09:28 2024
Last modified on Mar 21 10:48 2024

@author: Marti
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import warnings
from tkinter import Tk
from tkinter.filedialog import askdirectory
Folder = askdirectory(title='Select Folder') # shows dialog box and return the path
Wd = (Folder)  
import os
os.chdir(Wd)

root = tk.Tk()
root.withdraw()  # Hide the main window
# Select a file
filename = filedialog.askopenfilename(
    title='Select a file',
    filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
# Close the Tkinter root window
root.destroy()
# Extract the directory and file name
folder = os.path.dirname(filename)
name = os.path.basename(filename)
filename = folder + '/' + name


#read in data from .txt file
data = pd.read_csv(filename, sep='\s+')
data.columns = ['Time(s)', 'Distance_m','Force(N)']
t = data['Time(s)'].values
F = data['Force(N)'].values
D = data['Distance_m'].values

def moving_average(data, window_size):
    """
    Calculates the moving average of a 1-dimensional array using a specified
    window size. The window is centered around each index, and decreases at
    the ends of the input array.

    Parameters
    ----------
    data : The input 1-dimensional array.
    window_size : int
        The window size. This should be an odd number. If it is even it will
        be increased by 1 to have a symmetric window around each element.
    """
    if window_size % 2 == 0:
        warnings.warn(f"Got an even sized {window_size=}. Increasing it by 1")
        window_size += 1
    wh = window_size // 2  # Half window: Number of samples before/after current
    result = np.empty_like(data)  # Return values as a numpy array, not a list
    length = len(data)
    for i in range(length):
        if i < wh:  # Average over smaller interval at beginning
            result[i] = sum(data[:2 * i + 1]) / (2 * i + 1)
        elif length - i <= wh:    # Average over smaller interval at end
            l = 2 * i - length + 1
            # print(f"{i=},  {l=}")
            result[i] = sum(data[l:]) / (length - l)
        else:
            result[i] = sum(data[i - wh:i + wh + 1]) / window_size
    return result


#window_size=len(df)
window_size=9

Favg = moving_average(F, window_size)
print(Favg)
Davg = moving_average(D, window_size)
tavg = moving_average(t, window_size)

name = name.replace("_second_selected_dat.txt", "")

############ Here we calculate the velocity as a derivative of displacement and time######
def derivative_central(y, t):
    """
    Computes dy/dt based on central difference.

    Parameters:
    y : array-like
        The dependent variable.
    t : array-like
        The independent variable.

    Returns:
    der : array-like
        The derivative of y with respect to t.
    """
    der = np.empty_like(y)
    der[1:-1] = (y[2:] - y[:-2]) / (t[2:] - t[:-2])
    # Assume same derivative value for first and last element as the
    # second, second last element, respectively
    der[[0, -1]] = der[[1, -2]]
    return der


vel = -derivative_central(Davg,t )
avg_vel=moving_average(vel, window_size)

#print(avg_vel)
####################################################

#################Here we apply the calibration factors based on three ranges###################

FOV_LOW = 2.0e3
FOV_HIGH = 2.001e3

# Calibration as listed in Table 1
cal = {
    'low': {'f/v': 1.8e3,'m': 2.4755, 'b': -1112.3},
    'high': {'f/v':2.2e3,'m': 3.0935, 'b': -1687.1}
}


def eta(force, vel):
    """Calculate viscosity from calibration regions and interpolate in
    transition interval.
    Parameters
    ----------
    force
    vel
    """
    visc = np.empty_like(force)
    fov = force / vel
    clu, cll = cal['high'], cal['low']
    # upper calibration range:
    idx = fov >= clu['f/v']
    if np.any(idx):
        visc[idx] = clu['m'] * fov[idx] + clu['b']
    # lower calibration range
    idx = fov <= cll['f/v']
    if np.any(idx):
        visc[idx] = cll['m'] * fov[idx] + cll['b']
    # linear interpolation in transition range
    idx = np.logical_and(fov < clu['f/v'], fov > cll['f/v'])
    if np.any(idx):
        fovup, fovlow = clu['f/v'], cll['f/v']
        mup, mlow = clu['m'], cll['m']
        bup, blow = clu['b'], cll['b']
        m = (mup - mlow) / (fovup - fovlow) * (fov[idx] - fovlow) + mlow
        b = (bup - blow) / (fovup - fovlow) * (fov[idx] - fovlow) + blow
        visc[idx] = m * fov[idx] + b
    return visc


cal_visc= eta(Favg, vel) #####this is now the raw calibrated viscosity 

Vmavgcal =moving_average(cal_visc, window_size)#########we smooth the calibrated viscosity here

dstart = 3
# Initialize depth array with the same length as velocity array
depth = np.empty_like(vel)
# Compute depth as integral of the velocity over time
# Here done by the trapezoidal rule 
depth[:dstart] = 0.  # Set initial values before dstart to 0
depth[dstart] = 0.5 * (vel[dstart] + vel[dstart - 1]) * (t[dstart] - t[dstart - 1])  # Initial value at dstart
for i in range(dstart + 1, len(vel)):
    depth[i] = depth[i - 1] + 0.5 * (vel[i] + vel[i - 1]) * (t[i] - t[i - 1])  # Compute depth using trapezoidal rule



plt.plot(depth, cal_visc, 'o-', color='red', mfc='none', mec='k', label='vcal vs. depth')
plt.plot(depth, Vmavgcal, 'o-', color='black', mfc='none', mec='k', label='vmavgcal vs. depth')



plt.legend(loc="upper left")
plt.ylabel('Viscosity Pas')
plt.xlabel('lenght (m)')
plt.show()
###export data into .txt files 
np.savetxt(name+" _processed_dat.txt", np.c_[cal_visc, Vmavgcal, depth])
data_out = np.c_[cal_visc, Vmavgcal, depth, avg_vel]
df = pd.DataFrame(data_out, columns=['Calibrated Viscosity', 'Smoothed Calibrated Viscosity', 'Depth', 'Average Velocity'])
df.to_csv(name + '_processed_dat.csv', index=False)



data_out = np.c_[cal_visc, Vmavgcal, depth, avg_vel]
df = pd.DataFrame(data_out, columns=['Calibrated Viscosity', 'Smoothed Calibrated Viscosity', 'Depth', 'Average Velocity'])
df.to_csv(name + '_processed_dat.csv', index=False)





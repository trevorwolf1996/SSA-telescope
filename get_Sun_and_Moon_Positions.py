# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:15:42 2018

This function will calculate the position of the Moon and Earth in the ECIF mean 
of date coordinate system for an input epoch. The function uses the SPK SPICE JPL 
Ephemerides library. The Emphemeride set used for this particular function is the DE430
data set. To access this file, one can download it from ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp.
One also needs to install the spiceypy python module or equivalent SPK Spice python implimentation. 
An associated leapsecond kernel will also need to be downloaded and refereced in the same meta-kernel
that references the DE430 emphemeris kernel. It is strongly recommended that the user takes some time 
to understand the basics of the the SPK framework before using or modifying this funtion. 

Inputs:
    
    epoch_UTC: string in format 'mm-dd-yyyy hh:mm:ss.sss'
    ttt: terrestrial time
    
Outputs:
    
    rECIF_Moon: ECIF 3x1 position vector of the Moon in mean-of-date coordinate frame
    rECIF_Sun: ECIF 3x1 position vector of the Sun in mean-of-date coordinate frame

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""


import numpy as np
import spiceypy as spice



# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.
#   https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/a_old_versions/naif0009.tls
#   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc

spice.furnsh("./Get_Sun_Moon/metaGetSunMoon.txt") #load above kernels into workspace-- note one should do this globally
# before this function because of the size of the files

epoch_UTC = epoch_UTC+' TDB'

# get et value
et = spice.str2et(epoch_UTC) # converts to a numeric vector -- this is seconds since J2000 in tbd -- barycentric dynamical time

#Run spkpos as a vectorized function
rECIF_Moon_J2000, _ = spice.spkpos('Moon', et, 'J2000', 'NONE', 'Earth')
rECIF_Sun_J2000, _ = spice.spkpos('Sun', et, 'J200', 'NONE', 'Earth')

rECIF_Moon_J2000 = np.array(rECIF_Moon_J2000) # Convert from list in np array
rECIF_Sun_J2000 = np.array(rECIF_Sun_J2000) 

# Clean up the kernels
#spice.kclear()







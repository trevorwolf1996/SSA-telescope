# -*- coding: utf-8 -*-
"""
This function will calculate the position of the Moon and Earth in the ECIF mean 
of date coordinate system for an input epoch. The function uses the SPK SPICE JPL 
Ephemerides library. The Emphemeride set used for this particular function is the DE430
data set. To access this file, one can download it from ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp.
One also needs to install the spiceypy python module or equivalent SPK Spice python implimentation. 
An associated leapsecond kernel will also need to be downloaded and refereced in the same meta-kernel
that references the DE430 emphemeris kernel. It is strongly recommended that the user takes some time 
to understand the basics of the the SPK framework before using or modifying this funtion. 

Inputs:
    yr: Year of interest
    mon: Month of interest
    day: Day of interest
    hr: Hour of interest
    mi: Minute of interest
    sec: Second of interest
    
    epoch_UTC: string in format 'mm-dd-yyyy hh:mm:ss.sss'
    ttt: terrestrial time
    
Outputs:
    
    rECIF_Moon: ECIF 3x1 position vector of the Moon in mean-of-date coordinate frame
    rECIF_Sun: ECIF 3x1 position vector of the Sun in mean-of-date coordinate frame

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""


import numpy as np
import spiceypy as spice

def get_Sun_and_Moon_Positions(yr, mon, day, hr, mi, sec):
    #
    # Convert the given UTC inputs into the necessary string format
    #
    yr_string = str(yr);
    #
    if mon < 10:
        mon_string = '0' + str(mon);
    else:
        mon_string = str(mon);
    #
    if day < 10:
        day_string = '0' + str(day);
    else:
        day_string = str(day)
    #
    if hr < 10:
        hr_string = '0' + str(hr);
    else:
        hr_string = str(hr);
    #
    if mi < 10:
        mi_string = '0' + str(mi);
    else:
        mi_string = str(mi);
    #
    if sec < 10:
        sec_string = '0' + str(sec);
    else:
        sec_string = str(sec);
#
# Create the total string needed for the epoch of interest
#
    epoch_UTC = mon_string + '-' + day_string + '-' + yr_string + ' ' + hr_string +\
            ':' + mi_string + ':' + sec_string;
#

    epoch_UTC = epoch_UTC+' TDB'

    # get et value
    et = spice.str2et(epoch_UTC) # converts to a numeric vector -- this is seconds since J2000 in tbd -- barycentric dynamical time

    #Run spkpos as a vectorized function
    rECIF_Moon_J2000, vECIF_Moon_J2000 = spice.spkpos('Moon', et, 'J2000', 'NONE', 'Earth')
    rECIF_Sun_J2000, vECIF_Sun_J2000 = spice.spkpos('Sun', et, 'J200', 'NONE', 'Earth')

    rECIF_Moon_J2000 = np.array(rECIF_Moon_J2000); # Convert from list in np array
    rECIF_Sun_J2000 = np.array(rECIF_Sun_J2000); 
    #
    vECIF_Moon_J2000 = np.array(vECIF_Moon_J2000);
    vECIF_Sun_J2000 = np.array(vECIF_Sun_J2000);

    return rECIF_Moon_J2000, rECIF_Sun_J2000, vECIF_Moon_J2000, vECIF_Sun_J2000









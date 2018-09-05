# -*- coding: utf-8 -*-
"""
This function is meant to validate the acceleration perturbation models created
thus far. These include the spherical harmonic gravity perturbation effects, 
atmospheric drag, third body perturbation effects, and solar radiation effects.
The results of these models will be compared to GMAT.

Copyright (c) Trevor Wolf 2018. All Rights Reserved 
"""
import numpy as np
from spherical_harmonic_arrays import spherical_harmonic_arrays
from spherical_harmonic_acceleration import spherical_harmonic_acceleration
from rECIF2RADEC import rECIF2RADEC
from rECEF2LATLONG import rECEF2LATLONG
from jday import jday
#from pull_NOAA_K_p import pull_NOAA_K_p ##NEEDS WORK
#from pull_NOAA_F_10p7 import pull_NOAA_F_10p7 ##NEEDS WORK
from third_body_accelerations import third_body_accelerations
#from get_Sun_and_Moon_Positions import get_Sun_and_Moon_Positions ##NEEDS WORK
from solar_radiation_pressure import solar_radiation_pressure
from jacchia_71_gill_tabulated_SD_values import jacchia_71_gill_tabulated_SD_values
from jacchia_71_gill_density import jacchia_71_gill_density
from jacchia_71_gill_tabulated_helium_values import jacchia_71_gill_tabulated_helium_values
#
import spiceypy as spice


#
# First, load in states generated previously in GMAT 
#

# manually select directory to where the file is found

ephemeris_file = open('C:/Users/Trevor/Documents/GMAT/AMC_8_Jan1_2018/Spherical_Harmonic_Perturbation_Report_AMC_8_jan_1_2018.txt');
#
count = 0;
#
while True:
    #
    current_line = ephemeris_file.readline()
    #
    if not current_line:
        break 
    #
    if count == 2:
        #
        new_j_date = float(current_line[27:50])
        julian_date = np.array(new_j_date)
        #
        new_x_ECEF = float(current_line[131:155]);
        x_ECEF = np.array(new_x_ECEF);
        #
        new_y_ECEF = float(current_line[157:180]);
        y_ECEF = np.float(new_y_ECEF);
        #
        new_z_ECEF = float(current_line[183:208]);
        z_ECEF = np.array(new_z_ECEF);
        #
        new_vx_ECEF = float(current_line[53:78]);
        vx_ECEF = np.array(new_vx_ECEF);
        #
        new_vy_ECEF = float(current_line[79:105]);
        vy_ECEF = np.float(new_vy_ECEF);
        #
        new_vz_ECEF = float(current_line[105:131]);
        vz_ECEF = np.array(new_vz_ECEF);
        #
        new_ax_ECEF_GMAT = float(current_line[365:395]);
        ax_ECEF_GMAT = np.array(new_ax_ECEF_GMAT);
        #
        new_ay_ECEF_GMAT = float(current_line[409:440]);
        ay_ECEF_GMAT = np.array(new_ay_ECEF_GMAT);
        #
        new_az_ECEF_GMAT = float(current_line[453:485]);
        az_ECEF_GMAT = np.array(new_az_ECEF_GMAT);
        #
    elif count > 2:
        new_j_date = float(current_line[27:50])
        julian_date = np.vstack((julian_date, new_j_date))
        #
        new_x_ECEF = float(current_line[131:155]);
        x_ECEF = np.vstack((x_ECEF, new_x_ECEF));
        #
        new_y_ECEF = float(current_line[157:180]);
        y_ECEF = np.vstack((y_ECEF, new_y_ECEF));
        #
        new_z_ECEF = float(current_line[183:208]);
        z_ECEF = np.vstack((z_ECEF, new_z_ECEF));
        #
        new_vx_ECEF = float(current_line[53:78]);
        vx_ECEF = np.vstack((vx_ECEF, new_vx_ECEF));
        #
        new_vy_ECEF = float(current_line[79:105]);
        vy_ECEF = np.vstack((vy_ECEF, new_vy_ECEF));
        #
        new_vz_ECEF = float(current_line[105:131]);
        vz_ECEF = np.vstack((vz_ECEF, new_vz_ECEF));
        #
        new_ax_ECEF_GMAT = float(current_line[365:395]);
        ax_ECEF_GMAT = np.vstack((ax_ECEF_GMAT, new_ax_ECEF_GMAT));
        #
        new_ay_ECEF_GMAT = float(current_line[409:440]);
        ay_ECEF_GMAT = np.vstack((ay_ECEF_GMAT, new_ay_ECEF_GMAT));
        #
        new_az_ECEF_GMAT = float(current_line[453:485]);
        az_ECEF_GMAT = np.vstack((az_ECEF_GMAT, new_az_ECEF_GMAT));
        #
        
    #
    count = count + 1;
#
# Call the spherical harmonic array file
#
zonal_coeff_array, sectorial_coeff_array, tesseral_coeff_array =\
spherical_harmonic_arrays()
#
# Call the jacchia 71 model array files
#
c_ij_array = jacchia_71_gill_tabulated_SD_values()
h_ij_array = jacchia_71_gill_tabulated_helium_values()
#
# 

        
    
    
    
    














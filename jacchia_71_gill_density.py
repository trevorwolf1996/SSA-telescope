# -*- coding: utf-8 -*-
"""
This program will calculate the atmospheric density using the a tabulated version
of the Jacchia 71 atmospheric model described by Gill (1996). The process can be 
decomposed into two main steps. First, the atmospheric temperature is calculated
using an empirical formula. The formula first considers the F_10.7 cm solar flux
to calculate a baseline temperature. Next, the geographic latitude and declination 
of the sun are then considered to calculate a value T_1. Corrections to this baseline
are then added to account for the geomagnetic activity. 

Using this value of temperature and the altitude of the satellite, a polynomial 
is interpolated to find the standard density value. The coefficients for this polynomial
are tabulated in Gill (1996). If the altitude of the satellite is below 350 km, 
a geomagnetic correcting term is then added to the density value. I addition,
a terms is added to account for the the apparent migration of Helium concentration 
at the winter pole. 

The resulting density calculation will be used to calculate the atmospheric drag 
for the that the satllite will experienc in LEO.   

Inputs:
    RA_sat: Right-Ascension of the satellite
    RA_sun: Right-Ascension of the Sun 
    Z: The altitude of the spacecraft according the an ellipsoid Earth model
    declination_sun: Declination of the Sun
    latitude_sat: Geographic latitude of the satellite
    jday: Julian day of time of interest
    F_10p7_current: Current f_10.7 solar flux value 
    F_10p7_bar: 3-Solar cylce average of the f_10.7 solar flux value
    K_p: Geomagnetic index taken at 6.7 hours prior to current time of interest
    c_ij_array: Array containing the tabulated standard density values of the 
    atmosphere according to Gill (1996)
    h_ij_array: Array containing the tabulated partial volume of Helium, tabulated 
    by Gill (1996)
    
Outputs:
    log_density: log-density of the atmosphere 



Copyright (c) 2018 Trevor Wolf. All Rights Reserved.
"""
import numpy as np
# Comment to test project commit

def jacchia_71_gill_density(RA_sat, RA_sun, Z, declination_sun, latitude_sat,\
                            jday, F_10p7_current, F_10p7_bar, K_p, c_ij_array,\
                            h_ij_array):
    #
    # Calculate the Hour Angle
    #
    hour_angle = RA_sat - RA_sun;
    #
    # Calculate the Modified Julian Day
    #
    MJD = jday - 2400000.5; 
    #
    # Call function to find the obliquity of the ecliptic
    #
    obliquity_ecliptic  = 23.439291; #degrees -- taken as the mean at J2000
    #
    # Calculate value of T_c
    #
    T_c = 379.0 + 3.24*F_10p7_bar + 1.3*(F_10p7_current - F_10p7_bar); #degrees K
    #
    # Calculate the value of T_1
    #
    #
    # First, find the parameters tau, theta and eta
    #
    tau = hour_angle - 37.0 + 6.0*(hour_angle + 43.0); #degrees
    theta = 0.5*(latitude_sat + declination_sun); #degrees
    eta = 0.5*(latitude_sat - declination_sun); #degrees
    #
    two_theta = 2*theta;
    two_eta = 2*eta;
    #
    sin_p2p2_abs_theta = (0.5*(1.0 - np.cos(np.deg2rad(two_theta))))**1.1; #CHECK THESE
    cos_p2p2_abs_eta = (0.5*(1.0 + np.cos(np.deg2rad(two_eta))))**1.1;
    cos_p3p0_tau_over_two = np.cos(np.deg2rad(tau/2))**3;
    #
    T_1 = T_c*(1.0 + 0.3*(sin_p2p2_abs_theta + (cos_p2p2_abs_eta - sin_p2p2_abs_theta))*\
          cos_p3p0_tau_over_two); #CHECK THIS
    #
    
    # Add corrective terms for the geomagnetic effect
    #
    exp_K_p = np.exp(K_p);
    #
    delta_T_inf_H = 28.0*K_p + 0.03*exp_K_p; # for Z > 350 km
    delta_T_inf_L = 14.0*K_p + 0.02*exp_K_p; # for Z < 350 km
    #
    # Calculate smoothing function f
    #
    f = 0.5*(np.arctanh(0.04*(Z - 350.0)) + 1.0);
    one_minus_f = 1-f;
    #
    # Calculate delta_T_inf
    #
    delta_T_inf = f*delta_T_inf_H + one_minus_f*delta_T_inf_L;
    #
    # Finally, find T_inf
    # 
    T_inf = T_1 + delta_T_inf;
    #          
               
    # Use values of Z and T_inf to find the standard atmospheric density
    
    # Decide which c_ij matrix subset is appropriate
    if T_inf < 850:
        if Z < 1000:
            if Z < 500:
                if Z < 180:
                    c_ij = c_ij_array.T_less_than_850_and_Z_less_than_180
                else:
                    c_ij = c_ij_array.T_less_than_850_and_Z_less_than_500_greater_than_180
            else:
                c_ij  = c_ij_array.T_less_than_850_and_Z_less_than_1000_greater_than_500
        else:
            c_ij = c_ij_array.T_less_than_850_and_Z_greater_than_1000
    else:
        if Z < 1000:
            if Z < 500:
                if Z < 180:
                    c_ij = c_ij_array.T_greater_than_850_and_Z_less_than_180
                else:
                    c_ij = c_ij_array.T_greater_than_850_and_Z_less_than_500_greater_than_180
            else:
                c_ij = c_ij_array.T_greater_than_850_and_Z_less_than_1000_greater_than_500
        else:
             c_ij = c_ij_array.T_greater_than_850_and_Z_greater_than_1000
             
    
    Z_over_1000_km = Z / 1000; # normalize Z by 1000 km
    T_inf_over_1000_K = T_inf/1000; # normalize temperature by 1000 k
    #
    Z_over_1000_pi_array = np.zeros(6);
    T_over_1000_pj_array = np.zeros(5);
    #
    log_density_standard = 0;
    #
    for i in range(0, 6):
        #
        if i == 0:
            Z_over_1000_pi_array[i] = 1.0;
        else:
            Z_over_1000_pi_array[i] = Z_over_1000_pi_array[i - 1]*Z_over_1000_km;
        #
        for j in range(0, 5):
            #
            if i == 0:
                #
                if j == 0:
                    T_over_1000_pj_array[j] = 1.0;
                else:
                    T_over_1000_pj_array[j] = T_over_1000_pj_array[j - 1]*T_inf_over_1000_K;
                    #
                #    
            log_density_standard = log_density_standard + c_ij[i, j]*Z_over_1000_pi_array[i]*\
                                    T_over_1000_pj_array[j];
                                    
    ##
    # Add corrective density terms not expressed in standard atmospheric model
    
    # if Z is less than 350 km-- add a geomagnetic density corrective term 
    if Z < 350:
        delta_log_density_GM = (0.012*K_p + 1.2e-5*exp_K_p)*one_minus_f;
    else:
        delta_log_density_GM = 0; 
            
    
    # Add corrective term for the semi-annual variation in thermosphere and lower
    # atmosphere
        
    phi  = (MJD - 36204.0)/365.2422;
    two_pi_times_phi = 2.0*np.pi*phi;
    #
    tau_sa = phi + 0.09544*((0.5 + 0.5*np.sin(two_pi_times_phi + 6.035)**1.65) -\
             0.5);
    two_pi_times_tau_sa = 2*np.pi*tau_sa;
    four_pi_times_tau_sa = 2*two_pi_times_tau_sa;
    #
    f_of_Z = (5.876e-7*Z**2.331 + 0.06328)*np.exp(-0.002868*Z);
    g_of_t = 0.02835 + (0.3817 + 0.17829*np.sin(two_pi_times_tau_sa + 4.137))*\
    np.sin(four_pi_times_tau_sa + 4.259);
    #
    delta_log_density_sa = f_of_Z*g_of_t;
    # 
    # Add corrective term for seasonal-latitudinal density dependence
    #
    delta_Z_90 = Z - 90; # deviation from 90 km
    if latitude_sat < 0:
        sign_sin_p2_lat = -np.sin(np.deg2rad(latitude_sat))**2;
    else:
        sign_sin_p2_lat = np.sin(np.deg2rad(latitude_sat))**2;
    #
    delta_log_density_sl = 0.014*delta_Z_90*np.exp(-0.0013*delta_Z_90**2)*\
    np.sin(two_pi_times_phi + 1.72)*sign_sin_p2_lat;
    #
    # Add density corrective term for the seasonal variation of He over the winter pole
    #
    abs_decli_sun_over_obli_eclip = abs(declination_sun / obliquity_ecliptic); #unitless
    decli_sun_over_abs_decli_sun = declination_sun / abs(declination_sun); #unitless
    pi_over_four = np.pi/4;
    sat_lat_over_two = latitude_sat / 2;
    #
    delta_log_num_He = 0.65*abs_decli_sun_over_obli_eclip*(np.sin(pi_over_four - \
    sat_lat_over_two*decli_sun_over_abs_decli_sun)**3.0 - 0.35355); # this is the correction for the amount of helium that changes semiannually 
    #
    # Create array for storing the Z_pi and T_pj 
    #
    thousand_power_array = np.zeros(6);
    #
    for iterate in range(0, 6):
        if iterate == 0:
            thousand_power_array[iterate] = 1;
        else:
            thousand_power_array[iterate] = thousand_power_array[iterate - 1]*1000;
            
        
    Z_pi_array = Z_over_1000_pi_array*thousand_power_array;
    T_pj_array = T_over_1000_pj_array*thousand_power_array[0:5];
    
    # Choose which set of arrays to use 
    if Z < 2500:
        if Z < 1000:
            if Z < 500:
                h_ij = h_ij_array.Z_less_than_500_greater_than_90
            else:
                h_ij = h_ij_array.Z_less_than_1000_greater_than_500
        else:
             h_ij = h_ij_array.Z_less_than_2500_greater_than_1000
    #
    # interpolate the find log_n_He using Gill's tabulations
    #
    log_num_He = 0;
    #
    for i in range(0, 6):
        for j in range(0, 5):
            #
            log_num_He = h_ij[i, j]*Z_pi_array[i]*T_pj_array;
            #
        #    
    #
    # Find the density correction for the Helium migration
    #
    molar_mass_He = 4.0026; #grams per mole
    A_v = 6.022140857e23; # avagadro's number 
    #
    delta_log_density_He = 10**log_num_He*(molar_mass_He / A_v)*\
    (10**delta_log_num_He - 1);
    
    #
    # Add the density of the standard atmosphere and the corrections to find the density at the 
    # given time and location
    #
    
    log_density  = log_density_standard + delta_log_density_GM + \
    delta_log_density_sa + delta_log_density_sl + delta_log_density_He;
    #
    return log_density



                                                           
                                                    
    




    
                                
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           

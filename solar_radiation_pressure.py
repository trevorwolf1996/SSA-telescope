# -*- coding: utf-8 -*-
"""
This function calculates the solar radiation pressure that the spacecraft of 
interest is experiencing at any given time. This function considers occulation
effects from the Earth and the Moon. The occulations can be total, partial or 
none. One must know the parameters of the spacecraft of interest to use this 
function. In an orbit determination routine, these parameters could be estimated
through the measurement function. These parameters are the reflectivity coefficient
epsilon, the orientation vector n, the mass mass_sat, and the area of the effective
surface experiencing radiation pressure area_sat.

Input:
    r_sunECEF: Position of the Sun in the ITRF reference system (m)
    r_moonECEF: Position of the Moon in the ITRF reference system (m)
    rECEF: Postion of the satellite in the ITRF reference system (m) 
    n: Orientation unit vector w.r.t epsilon sun unit vector
    epsilon: Solar reflectivity constant 
    area_sat: Area of the satellite (m^2)
    mass_sat: Mass of the satellite (kg)
    
Output:
    accel_solar_radiation: Solar radiation pressure experienced by satellite in 
    the ITRF reference frame 

Copyright (c) Trevor Wolf 2018. All Rights Reserved.
"""
import numpy as np

def solar_radiation_pressure(rECEF, r_sunECEF, r_moonECEF, n, epsilon, area_sat,\
                             mass_sat):
    #
    # Initialize constants 
    #
    R_sun = 6.957e8; # Radius of the Sun - meters
    R_moon = 1.737e6; #Radius of the Moon - meters
    R_earth = 6.371e6; # Radius of the Earth - meters
    AU = 1.496e11; # Astronimical Unit - meters
    P_sun = 4.56e-6;
    #
    # Initialize nu as one
    #
    nu = 1.0;
    #
    # Find the parameters a, b and c
    #
    r_sun_minus_r_sat = r_sunECEF - rECEF;
    abs_r_sun_minus_r_sat = abs(r_sun_minus_r_sat);
    #
    # First find the parameters a that does not vary per body
    #
    a_earth = np.arcsin(R_sun/abs_r_sun_minus_r_sat);
    a_moon = a_earth;
    #
    # Find the b and c paremters for the Earth
    #
    s_vec_earth = rECEF;
    abs_s_vec_earth = abs(s_vec_earth);
    #
    b_earth = np.arcsin(R_earth / abs_s_vec_earth);
    #
    c_earth = np.arccos(np.dot(-s_vec_earth, r_sun_minus_r_sat)/(abs_s_vec_earth*\
                        abs_r_sun_minus_r_sat));                   
    #
    # Check conditions for occulation effects for the Earth
    #
    if c_earth < abs(a_earth - b_earth):
        nu = 0.0; # total occulation from Earth
    #
    elif a_earth + b_earth <= c_earth:
        #
        s_vec_moon = rECEF - r_moonECEF;
        abs_s_vec_moon = abs(s_vec_moon);
        #
        b_moon = np.arcsin(R_moon/abs_s_vec_moon);
        #
        c_moon = np.arccos(np.dot(-s_vec_moon, r_sun_minus_r_sat)/(abs_s_vec_moon*\
                         abs_r_sun_minus_r_sat));
        #
        if c_moon < abs(a_moon - b_moon):
            nu = 0.0;
           #
        elif a_moon + b_moon <= c_moon:
            pass
           #
        else:
            a_moon_squared = a_moon**2.0;
            b_moon_squared = b_moon**2.0;
            # Calculate the parameters x and y
            x_moon = (c_moon**2.0 + a_moon_squared - b_moon_squared) / (2.0*c_moon);
            y_moon = np.sqrt(a_moon_squared - x_moon**2.0);
            #
            occulated_area_moon = a_moon_squared*np.arccos(x_moon / a_moon) + \
            b_moon_squared*np.arccos((c_moon - x_moon) / b_moon) - c_moon*y_moon;
            #
            nu  = nu - occulated_area_moon/(np.pi*a_moon_squared);
    else:
        a_earth_squared = a_earth**2.0;
        b_earth_squared = b_earth**2.0;
        # Calculate the parameters x and y
        x_earth = (c_earth**2.0 + a_earth_squared - b_earth_squared) / (2.0*c_earth);
        y_earth = np.sqrt(a_earth_squared - x_earth**2.0);
        #
        occulated_area_earth = a_earth_squared*np.arccos(x_earth / a_earth) + \
        b_earth_squared*np.arccos((c_earth - x_earth) / b_earth) - c_earth*y_earth;
        #
        nu  = nu - occulated_area_earth/(np.pi*a_earth_squared);
        #
        # Find the parameters b and c for the Moon 
        #
        s_vec_moon = rECEF - r_moonECEF;
        abs_s_vec_moon = abs(s_vec_moon);
        #
        b_moon = np.arcsin(R_moon/abs_s_vec_moon);
        #
        c_moon = np.arccos(np.dot(-s_vec_moon, r_sun_minus_r_sat)/(abs_s_vec_moon*\
                        abs_r_sun_minus_r_sat));
        #
        # Check conditions for occulation from the Moon
        #
        if c_moon < abs(a_moon - b_moon):
            nu = 0.0;
            #
        elif a_moon + b_moon <= c_moon:
            pass
            #
        else:
            a_moon_squared = a_moon**2.0;
            b_moon_squared = b_moon**2.0;
            # Calculate the parameters x and y
            x_moon = (c_moon**2.0 + a_moon_squared - b_moon_squared) / (2.0*c_moon);
            y_moon = np.sqrt(a_moon_squared - x_moon**2.0);
            #
            occulated_area_moon = a_moon_squared*np.arccos(x_moon / a_moon) + \
            b_moon_squared*np.arccos((c_moon - x_moon) / b_moon) - c_moon*y_moon;
            #
            nu  = nu - occulated_area_moon/(np.pi*a_moon_squared);
        #
    #
        
    if nu == 0.0:
        accel_solar_radiation = 0.0;
    else:
        #
        # Calculate remaining parameters needed to find the solar radiation pressure
        #
        norm_r_sunECEF = np.linalg.norm(r_sunECEF);
        e_sun = r_sunECEF/norm_r_sunECEF; # Unit vector pointing from the sun to S.C
        cos_theta = np.dot(n, e_sun); # Cosine of angle between orientation of S.C. and Sun
        #
        accel_solar_radiation = -nu*P_sun*(AU**2/norm_r_sunECEF)*area_sat/mass_sat*\
        cos_theta*((1 - epsilon)*e_sun + 2.0*epsilon*cos_theta*n);
    #
    return accel_solar_radiation

    



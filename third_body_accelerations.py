# -*- coding: utf-8 -*-
"""
This function will calculate the third body perturbation effects on the satellite
of interest. Currently as is, the function only considers the perturbing effects
from the Sun and Moon, which are the two dominant perturbing bodies for Earth 
orbiting satellites. 

Inputs:
    rECEF: Position of satellite in ITRF reference system
    r_sunECEF: Position of Sun in the ITRF reference system
    r_moonECEF: Position of the Moon in the ITRF reference system 
Output:
    accel_third_body: Acceleration in ECEF frame caused by third body perturbations

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""
import numpy as np

def third_body_accelerations(rECEF, r_sunECEF, r_moonECEF):
    #
    # Define gravitational constant parameters
    #
    mu_sun = 1.32712440018e20;
    mu_earth = 3.986004418e14;
    mu_moon = 4.9048695e12;
    #
    # Find vectors between sat_Sun and sat_Moon
    #
    r_sat_sunECEF = r_sunECEF - rECEF;
    r_sat_moonECEF = r_moonECEF - rECEF;
    #
    # Compute the norms of each of these vectors
    #
    norm_rECEF = np.linalg.norm(rECEF);
    #
    norm_r_sunECEF = np.linalg.norm(r_sunECEF);
    norm_r_moonECEF = np.linalg.norm(r_moonECEF);
    #
    norm_sat_sunECEF = np.linalg.norm(r_sat_sunECEF);
    norm_sat_moonECEF = np.linalg.norm(r_sat_moonECEF);
    #
    # Compute the arguement of the Legendre polynomial for the sun and the moon
    #
    legendre_arg_sun = -(norm_sat_sunECEF**2.0 - norm_rECEF**2.0 - norm_r_sunECEF**2.0)/\
    (2.0*norm_rECEF*norm_r_sunECEF);
    #
    legendre_arg_moon = -(norm_sat_moonECEF**2.0 - norm_rECEF**2.0 - norm_r_moonECEF**2.0)/\
    (2.0*norm_rECEF*norm_r_moonECEF);
    #
    # Compute the parameter h for the sun and the moon
    #
    h_sun = norm_rECEF/norm_r_sunECEF;
    h_moon = norm_rECEF/norm_r_moonECEF;
    #
    # Compute the legendre polynomial factors
    #
    P_sun = np.zeros(6);
    P_moon = np.zeros(6);
    #
    P_sun[0] = 1;
    P_moon[0] = 1;
    #
    P_sun[1] = legendre_arg_sun;
    P_moon[1] = legendre_arg_moon;
    #
    
    for l in range(2, 6):
        P_sun[l] = ((2*l - 1)*legendre_arg_sun*P_sun[l-1] - (l-1)*P_sun[l-2])/l;
        P_moon[l] = ((2*l - 1)*legendre_arg_moon*P_sun[l-1] - (l-1)*P_moon[l-2])/l;
        #
    #
    # Compute the parameter B
    #
    B_sun = 0;
    B_moon = 0;
    #
    for j in range(1, 6): 
        B_sun = P_sun[j]*h_sun**j;
        B_moon = P_moon[j]*h_moon**j;
    #
    # Compute the parameter beta
    #
    beta_sun = 3.0*B_sun + 3.0*B_sun**2.0 + B_sun**3.0;
    beta_moon = 3.0*B_moon + 3.0*B_moon**2.0 + B_moon**3.0;
    #
    accel_sun = -mu_sun/(norm_r_sunECEF**3.0)*(rECEF - beta_sun*r_sat_sunECEF);
    accel_moon = -mu_moon/(norm_r_moonECEF**3.0)*(rECEF - beta_moon*r_sat_moonECEF);
    #
    accel_third_body = accel_sun + accel_moon;
    #
    return accel_third_body





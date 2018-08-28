# -*- coding: utf-8 -*-
"""
This function will find the geocentric latitude, longitude and altitude of the 
satellite. The function is adapted from David Vallado's book "Fundamentals
of Astromechanics" 

Inputs: 
    rECEF: Position of body in Earth Centered Fixed coordinates
Outputs:
    phi_gd: Geodetic latitude eof the body -- need to convert to geocentric for spherical harmonic calcs
    longitude: Longtude of the body
    h_ellp: Altitude of the spacecraft considering an ellitical Earth model

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""
import numpy as np

def rECEF2LATLONG(rECEF):
    
    r_delta_sat = np.sqrt(rECEF[0]**2.0 + rECEF[1]**2.0);
    a = 6378.1363; # Equatorial radius of the Earth
    b = 6356.751*np.sign(rECEF[2]);
    #
    E = (b*rECEF[2] - (a**2 - b**2))/(a*r_delta_sat);
    #
    longitude = np.atan2(rECEF[1]/rECEF[0]);
    #
    F = (b*rECEF[2] + (a**2.0 + b**2.0))/(a*r_delta_sat);
    P = (4.0*(E*F + 1.0))/3.0;
    Q = 2.0*(E**2.0 - F**2.0);
    D = P**3.0 + Q**2.0;
    if D > 0.0:
        nu = (np.sqrt(D) - Q)**(1/3) - (np.sqrt(D) + Q)**(1/3);
    else:
        sqrt_negative_P = np.sqrt(-P);
        nu = 2.0*sqrt_negative_P*np.cos(1/3*np.arccos(Q/(P*sqrt_negative_P)));
    #
    G = 0.5*(np.sqrt(E + nu) + E);
    t = np.sqrt(G**2.0 + (F-nu*G)/(2*G - E)) - G;
    #
    phi_gd = np.atan2(a*(1.0 - t**2.0)/(2.0*b*t));
    h_ellp = (r_delta_sat - a*t)*np.cos(phi_gd) + (rECEF[2] - b)*np.sin(phi_gd);
    #
    return phi_gd, longitude, h_ellp

    


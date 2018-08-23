# -*- coding: utf-8 -*-
"""
This function is an adaptation of David Vallado's algorithm for transforming a given 
geocentric state in an intertial coordinate system into the right ascention and 
declination. 

Input: 
    r_ECIF: Position of body in Earth centered inertial coordinate frame (GCRF)
    v_ECIF: Velocity of body in Earth centered inertial coordinate frame (GCRF)

Output: 
    ra: Right ascension of the body of interest
    decl: Declination of the body of interest

Copyright (c) Trevor Wolf 2018. All Rights Reserved .
"""
import numpy as np

def rECIF2RADEC(rECIF, vECIF):
    r_mag = np.linalg.norm(rECIF);
    #
    sin_decl = rECIF[2]/r_mag;
    decl = np.arcsin(sin_decl); 
    #
    # A check for singularities must be added for the Right Ascension 
    #
    temp = np.sqrt(rECIF[0]**2.0 + rECIF[1]**2.0);
    tolerance = 10e-8;
    #
    if temp > tolerance:
        ra = np.atan2(rECIF[1], rECIF[0]);
    else:
        ra = np.atan2(vECIF[1], vECIF[0]);
    #
    return ra, decl
    
    
    
    


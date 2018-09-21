# -*- coding: utf-8 -*-
"""
This function will compute acceleration contribution caused by the spherical 
harmonic mass model of the Earth. It considers zonal, sectorial and tesseral 
effects. The number of terms used should be input. The current implimentation 
considers a tableua of up 25 terms along the zonal axis, and a 5x5 tableuas
with respect to the sectorial and and tesseral axes. The accelerations are 
computed in the body fixed ITRF coordinate frame. This will be transformed 
into either a MOD or TOD coordinate frame for integrating. 

Copyright (c) 2018 Trevor Wolf. All rights reserved. 

Inputs: 
    
    zonal_coeff_array: numpy array containing the terms that describe the mass distribution
    of the Earth with respect to latitude 
    
    sectorial_coeff_array: numpy array containing the terms that describe the mass 
    distribution of the Earth with respect to longitude 
    
    tesseral_coeff_array: numpy array containt the terms that describe the mass 
    distrition of the Earth for a teseral pattern 

Outputs:
        
    accel_spherical_harmonic_ITRF: Accelation caused be the spherical harmonic 
    Earth gravitational model in the ITRF reference frame 
"""



import numpy as np
import math as math

def spherical_harmonic_acceleration(zonal_coeff_array, sectorial_coeff_array,\
                                    tesseral_coeff_array, r_ITRF, order_zonal,\
                                    order_tesseral):
    
    # Call function for computing phi_gc_sat and lambda
    #
    phi_gc = 1;
    lambda_sat = 1;
    r_earth = 1;
    mu_earth = 1;
    r_ITRF_mag = 1;
    #
    # Create array of the evaluate legendre polynomials through recursion
    # 
    P = np.zeros((order_zonal + 1, order_tesseral + 1));
    #
    # Define the first l<2 lenendre evaluated functions
    #
    sin_phi_gc = math.sin(phi_gc);
    cos_phi_gc = math.cos(phi_gc);
    #
    tan_phi_gc = sin_phi_gc / cos_phi_gc;
    #
    P[0, 0] = 1;
    #
    P[1, 0] = sin_phi_gc;
    P[1, 1] = cos_phi_gc;
    
    # recursively fill array 
    
    for l in range(2, order_zonal):
        #
        two_l_minus_one = 2*l-1;
        l_minus_one = l-1;
        #
        P[l, 0] = (two_l_minus_one*sin_phi_gc*P[l-1, 0] - l_minus_one*P[l-2, 0])/l;
        #
        if l > order_tesseral:
            continue
        
        for m in range(1, l): 
            #
            P[l, m] = P[l-2, m] + two_l_minus_one*cos_phi_gc*P[l-1, m-1];
            # 
            if m == l:
                #
                P[l, m] = two_l_minus_one*cos_phi_gc*P[l-1, l-1];
    
    #
    # Initialize array of cos(m*lambda) and sin(m*lambda) and other variables
    #
    cos_m_times_lambda_array = np.zeros(order_tesseral + 1);
    sin_m_times_lambda_array = np.zeros(order_tesseral + 1);
    #
    cos_m_times_lambda_array[1] = math.cos(lambda_sat);
    sin_m_times_lambda_array[1] = math.sin(lambda_sat);
    #  
    r_ITRF_mag = np.linalg.norm(r_ITRF);
    r_earth_over_rmag = r_earth / r_ITRF_mag;
    r_earth_over_rmag_p_l_array = np.power(r_earth_over_rmag, np.array(range(order_zonal)));
    #      
    # Compute partial derivatives of w.r.t r, phi_gc and lambda_sat
    #
    # First compute w.r.t r
    #
    sum_zonal_terms = 0;
    sum_tesseral_terms = 0;
    #
    for l in range(2, order_zonal):
        #
        r_earth_over_rmag_p_l_times_l_minus1 = r_earth_over_rmag_p_l_array[l]*(l+1);
        #
        outside_factor_zonal = r_earth_over_rmag_p_l_times_l_minus1*P[l, 0];
        # 
        sum_zonal_terms = sum_zonal_terms + outside_factor_zonal*zonal_coeff_array[l]
        #
        if l > order_tesseral:
            continue
        #
        cos_m_times_lambda_array[l] = math.cos(l*lambda_sat);
        sin_m_times_lambda_array[l] = math.sin(l*lambda_sat);
        #
        for m in range(1, l):
            #
            outside_factor_tesseral = r_earth_over_rmag_p_l_times_l_minus1*P[l, m]
            #
            sum_tesseral_terms = sum_tesseral_terms + outside_factor_tesseral*\
            (sectorial_coeff_array[l, m]*cos_m_times_lambda_array[m] +\
             tesseral_coeff_array[l, m]*sin_m_times_lambda_array[m]);
        #
    #
    # Compute the partial derivative
    #
    d_potential_d_rmag = (-mu_earth/r_ITRF_mag**2)*(sum_zonal_terms + sum_tesseral_terms);
    #
    # Next, compute w.r.t phi_gc
    #
    sum_zonal_terms = 0;
    sum_tesseral_terms = 0;
    #
    for l in range(2, order_zonal):
        #
        r_earth_over_rmag_p_l = r_earth_over_rmag_p_l_array[l];
        #
        outside_factor_zonal = r_earth_over_rmag_p_l*P[l, 1]; # check this line
        #
        sum_zonal_terms = sum_zonal_terms + outside_factor_zonal*zonal_coeff_array[l]
        #
        if l> order_tesseral:
            continue
        #
        for m in range(1, l):
            #
            outside_factor_tesseral = r_earth_over_rmag_p_l*(P[l, m+1] - m*tan_phi_gc*P[l, m]);
            # 
            sum_tesseral_terms = sum_tesseral_terms + outside_factor_tesseral*\
            (sectorial_coeff_array[l, m]*cos_m_times_lambda_array[m] +\
             tesseral_coeff_array[l, m]*sin_m_times_lambda_array[m]);
        #
    #
    # Compute the partial derivative
    #
    d_potential_d_phi_gc = (mu_earth/r_ITRF_mag)*(sum_zonal_terms + sum_tesseral_terms);
    #
    # Next, compute w.r.t lambda_sat
    #
    sum_tesseral_terms = 0;
    #
    for l in range(2, order_tesseral):
        #
        r_earth_over_rmag_p_l = r_earth_over_rmag_p_l_array[l];
        #
        for m in range(1, order_tesseral):
            #
            outside_factor_tesseral = r_earth_over_rmag_p_l*m*P[l, m];
            #
            sum_tesseral_terms = sum_tesseral_terms + outside_factor_tesseral*\
            (tesseral_coeff_array[l, m]*cos_m_times_lambda_array[m] - \
             sectorial_coeff_array[l, m]*sin_m_times_lambda_array[m]);
        #
    #
    # Compute the partial derivative
    #
    d_potential_d_lambda_sat = (mu_earth/r_ITRF_mag)*sum_tesseral_terms;
    #
    # Compute the necessary arguements for finding the accelerations
    #
    ri_p2_plus_rj_p2 = r_ITRF[0]**2 + r_ITRF[1]**2;
    one_over_ri_p2_plus_rj_p2 = 1/ri_p2_plus_rj_p2;
    sqrt_ri_p2_plus_rj_p2 = np.sqrt(ri_p2_plus_rj_p2);
    one_over_sqrt_ri_p2_plus_rj_p2 = 1/sqrt_ri_p2_plus_rj_p2;
    #
    one_over_r_mag = 1/r_ITRF_mag;
    #
    r_mag_squared = r_ITRF_mag**2;
    one_over_r_mag_squared = 1/r_mag_squared;
    #
    rk_over_rmag_p2_times_sqrt_ri_p2_plus_rj_p2 = r_ITRF[2]*one_over_r_mag_squared*\
    one_over_sqrt_ri_p2_plus_rj_p2
    #
    # Initialize array for storing acceleration values
    #
    accel_spherical_harmonic_ITRF = np.zeros(3);
    #
    # Compute accelerations in ITRF
    accel_spherical_harmonic_ITRF[0] = (one_over_r_mag*d_potential_d_rmag -\
    rk_over_rmag_p2_times_sqrt_ri_p2_plus_rj_p2*d_potential_d_phi_gc)*r_ITRF[0] -\
    (one_over_ri_p2_plus_rj_p2*d_potential_d_lambda_sat)*r_ITRF[1];
    #
    accel_spherical_harmonic_ITRF[1] = (one_over_r_mag*d_potential_d_rmag -\
    rk_over_rmag_p2_times_sqrt_ri_p2_plus_rj_p2*d_potential_d_phi_gc)*r_ITRF[1] +\
    (one_over_ri_p2_plus_rj_p2*d_potential_d_lambda_sat)*r_ITRF[0];
    #
    accel_spherical_harmonic_ITRF[2] = one_over_r_mag*d_potential_d_rmag*r_ITRF[2]+\
    sqrt_ri_p2_plus_rj_p2/r_mag_squared*d_potential_d_phi_gc;
    
    return accel_spherical_harmonic_ITRF
    

#accel = spherical_harmonic_acceleration(zonal_coeff_array, sectorial_coeff_array,\
 #                                   tesseral_coeff_array, r_ITRF, order_zonal,\
  #                                  order_tesseral)
                             
                                 
    
    
    
    
    
    
    
    
                                                
            
      
            
            
        
        
            
        
                    
        
    
    
    

    


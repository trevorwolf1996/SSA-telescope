# -*- coding: utf-8 -*-
"""
This script will contain the arrays that store the zonal, and secular and tesseral
coefficients for the spherical harmonci Earth gravity model. The 
coefficients given here are listed in appendix d of David Vallado's book 
"Fundamentals of Astrodynamcis". The coefficients define the EMG - 96 
gravity model. This model was chosen instead of the common WGS-76/84 for its high
precision 

Copyright (c) 2018 Trevor Wolf. All rights reserved. 
"""

import numpy as np

# zonal harmonics- selective terms of J2 - J70

def spherical_harmonic_arrays():
    #
    zonal_coeff_array = np.zeros(71);
    #
    zonal_coeff_array[2] =  -1.08262668355e-03 #J2
    zonal_coeff_array[3] =   2.53265648533e-06 #J3
    zonal_coeff_array[4] =   1.61962159137e-06 #J4
    zonal_coeff_array[5] =   2.27296082869e-07 #J5
    zonal_coeff_array[6] =  -5.40681239107e-07 #J6
    zonal_coeff_array[7] =   3.52359908418e-07 #J7
    zonal_coeff_array[8] =   2.04799466985e-07 #J8
    zonal_coeff_array[9] =   1.20616967365e-07 #J9
    zonal_coeff_array[10] =  2.41145438626e-07 #J10
    zonal_coeff_array[11] = -2.44402148325e-07 #J11
    zonal_coeff_array[12] =  1.88626318279e-07 #J12
    zonal_coeff_array[13] =  2.19788001661e-07 #J13
    zonal_coeff_array[14] = -1.30744533118e-07 #J14
    zonal_coeff_array[15] =  8.23528409456e-09 #J15
    zonal_coeff_array[16] = -1.81139265112e-08 #J16
    zonal_coeff_array[17] =  1.16904733834e-07 #J17
    zonal_coeff_array[18] =  3.09424678746e-08 #J18
    zonal_coeff_array[19] = -2.03450147680e-08 #J19
    zonal_coeff_array[20] =  1.42395629049e-07 #J20
    zonal_coeff_array[21] =  3.85459516960e-08 #J21
    zonal_coeff_array[22] = -7.62958407818e-08 #J22
    zonal_coeff_array[23] = -1.55075644100e-07 #J23
    zonal_coeff_array[24] =  5.34560170488e-09 #J24
    #
    zonal_coeff_array[66] = -2.83793303822e-09 #J66
    zonal_coeff_array[67] = -1.12773634901e-09 #J67
    zonal_coeff_array[68] =  5.41092788511e-09 #J68
    zonal_coeff_array[69] =  1.13653140244e-08 #J69
    zonal_coeff_array[70] = -2.03624641391e-08 #J70
    
    # seculorial harmonic terms 
    sectorial_coeff_array = np.zeros((6, 6)); # more terms may be added if deemed necessary
    
    sectorial_coeff_array[2, 1] = -2.41400000000e-10
    sectorial_coeff_array[2, 2] =  1.57446037456e-06
    #
    sectorial_coeff_array[3, 1] =  2.19263852917e-06
    sectorial_coeff_array[3, 2] =  3.08989206881e-07
    sectorial_coeff_array[3, 3] =  1.00548778064e-07
    #
    sectorial_coeff_array[4, 1] = -5.08799360404e-07
    sectorial_coeff_array[4, 2] =  7.84175859844e-08
    sectorial_coeff_array[4, 3] =  5.92099402629e-08
    sectorial_coeff_array[4, 4] = -3.98407411766e-09
    #
    sectorial_coeff_array[5, 1] = -5.31803015008e-08
    sectorial_coeff_array[5, 2] =  1.05587168391e-07
    sectorial_coeff_array[5, 3] = -1.49300637492e-08
    sectorial_coeff_array[5, 4] = -2.29930029013e-09
    sectorial_coeff_array[5, 5] =  4.30822462052e-10
    
    # tesseral harmonic effects 
    tesseral_coeff_array = np.zeros((6, 6))
    #
    tesseral_coeff_array[2, 1] =  1.54310000000e-09
    tesseral_coeff_array[2, 2] = -9.03803806639e-07
    #
    tesseral_coeff_array[3, 1] =  2.68424890297e-07
    tesseral_coeff_array[3, 2] = -2.11437612437e-07
    tesseral_coeff_array[3, 3] =  1.97222559006e-07
    #
    tesseral_coeff_array[4, 1] = -4.49144872839e-07
    tesseral_coeff_array[4, 2] =  1.48177868296e-07
    tesseral_coeff_array[4, 3] = -1.20077667634e-08
    tesseral_coeff_array[4, 4] =  6.52571425370e-09
    #
    tesseral_coeff_array[5, 1] = -8.08586947661e-08
    tesseral_coeff_array[5, 2] = -5.23291936216e-08
    tesseral_coeff_array[5, 3] = -7.09734236890e-09
    tesseral_coeff_array[5, 4] =  3.86712335851e-10
    tesseral_coeff_array[5, 5] = -1.64818262628e-09
    #
    return zonal_coeff_array, sectorial_coeff_array, tesseral_coeff_array






















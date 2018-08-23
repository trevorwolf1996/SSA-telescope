# -*- coding: utf-8 -*-
"""
This function contains the tabulated polynomial coefficients describing the ammount
of Hemium in the atmosphere. This amount is transient and is caused by the 
seasonal migration at the winter pole. This effect was first described in the 
Jacchia 71 atmospheric model and later tabulated by Gill (1996).

Outputs: 
    h_ij_array: Tabulated helium partial volume amounts according to Gill (1996)

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""
import numpy as np

# Create class for storing arrays

class h_ij_array_class():
    pass

def jacchia_71_tabulated_helium_vales():
    
    # 
    h_ij_array = h_ij_array_class();
    #
    h_ij_array.Z_less_than_500_greater_than_90 = np.array(\
     [[ 1.831549e+01,  5.887556e03,  -4.813257e-06,  1.701738e-09, -2.128374e-13],
      [-7.374008e-02, -1.251077e-04,  1.039269e-07, -3.679280e-11,  4.555258e-15],
      [ 4.384164e-04,  8.657027e-07, -7.216946e-10,  2.481534e-13, -2.859074e-17],
      [-1.411195e-06, -2.483834e-09,  2.004107e-12, -6.244985e-16,  5.561004e-20],
      [ 2.153639e-09,  3.421944e-12, -2.628961e-15,  7.085655e-19, -3.279804e-23],
      [-1.255139e-12, -1.827253e-15,  1.321581e-18, -2.887398e-22, -7.827178e-27]]);
    #
    h_ij_array.Z_less_than_1000_greater_than_500 = np.array(\
     [[ 1.627089e01,  -1.786816e-02,  3.079079e-05, -2.043431e-08,  4.643419e-12],
      [-1.958297e-02,  1.386126e-04, -2.532463e-07,  1.714183e-10, -3.934230e-14],
      [ 2.514251e-05, -3.806339e-07,  7.692376e-10, -5.394766e-13,  1.260304e-16],
      [-2.983314e-08,  5.855851e-10, -1.210663e-12,  8.561632e-16, -2.009030e-19],
      [ 1.802028e-11, -4.382878e-13,  9.201530e-16, -6.543935e-19,  1.540220e-22],
      [-4.243067e-15,  1.268830e-16, -2.695807e-19,  1.925469e-22, -4.542329e-26]]);
    #
    h_ij_array.Z_less_than_2500_greater_than_1000 = np.array(\
     [[ 1.873346e01,   2.285683e-02, -6.860776e-05,  5.379623e-08, -1.327559e-11]
      [-2.362530e-02, -6.907613e-05,  2.251680e-07, -1.795937e-10,  4.463659e-14]
      [ 1.893899e-05,  1.145960e-07, -3.183259e-10,  2.461076e-13, -6.040423e-17]
      [-1.132198e-08, -7.438326e-11,  2.040288e-13, -1.573191e-16,  3.857032e-20]
      [ 3.465014e-12,  2.308943e-14,  6.320466e-17,  4.871419e-20, -1.194139e-23]
      [-4.156710e-16, -2.791930e-18,  7.632792e-21, -5.881112e-24,  1.441455e-27]]);
    
    return h_ij_array
        



    
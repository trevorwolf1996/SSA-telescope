# -*- coding: utf-8 -*-
"""
This function is meant to validate the acceleration perturbation models created
thus far. These include the spherical harmonic gravity perturbation effects, 
atmospheric drag, third body perturbation effects, and solar radiation effects.
The results of these models will be compared to GMAT.

Copyright (c) Trevor Wolf 2018. All Rights Reserved 
"""
import numpy as np
from spherical_harmonic_arrays.py import spherical_harmonic_arrays
from spherical_harmonic_acceleration.py import spherical_harmonic_acceleration
from rECIF2RADEC.py import rECIF2RADEC
from rECEF2LATLONG import rECEF2LATLONG
from jday.py import jday
from pull_NOAA_K_p.py import pull_NOAA_K_p
from pull_NOAA_F_10p7.py import pull_NOAA_F_10p7
from third_body_accelerations.py import third_body_accelerations
from get_Sun_and_Moon_Positions.py import get_Sun_and_Moon_Positions
from solar_radiation_pressure.py import solar_radiation_pressure
from jacchia_71_gill_tabulated_SD_values.py import jacchia_71_gill_tabulated_SD_values
from jacchia_71_gill_density.py import jacchia_71_gill_density
from jacchia_71_gill_tabulated_helium_values import jacchia_71_gill_tabulated_helium_values
import spiceypy as spice
#
















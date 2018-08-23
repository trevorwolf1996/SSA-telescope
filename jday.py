# -*- coding: utf-8 -*-
"""
This function find the Julian Day given a time. This time can be in UTC or UTC_1

Input: 
    yr: year of date of interest
    mon: month of interest
    day: day of interest
    hr: hour of interest
    mi: minute of interest
    sec: second of interest
    
Copyright (c) Trevor Wolf 2018. All Rights Reserved
"""
import numpy as np

def jday(yr, mon, day, hr, mi, sec):
    jd = 367.0 * yr - \
    np.floor( (7.0 * (yr + np.floor( (mon + 9.0) / 12.0) ) ) * 0.25 ) + \
    np.floor( 275 * mon / 9.0 )+ day + 1721013.5;   
    jdfrac = (sec + mi * 60.0 + hr *3600.0) / 86400.0;
    
    # check jdfrac
    if jdfrac > 1.0: 
        jd = jd + np.floor(jdfrac);
        jdfrac = jdfrac - np.floor(jdfrac);
    #
    return jd, jdfrac
    
        

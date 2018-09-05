# -*- coding: utf-8 -*-
"""
This Function will pull the current F_10.7 and F_10.7_bar values as well as the 
current K_p value from the NOAA ftp site. These values will be used in 
calculating the current atmospheric density that the spacecraft of interest is
experiencing. Note that this data is limited to current satellite propagations, 
therefore, the user should not use this function if he or she is attempting to 
propagate past states of the satellite. Future work should include generalizations
to this constraint.

Inputs:
    yr: Year of interest
    mo: Month of interest
    day: Day of interest
    hr: Hour of interst
    mi: Minute of interest

Output:
    F_10p7: Current F_10.7 solar flux value


Copyright (c) Trevor Wolf 2018. All Rights Reserved.
"""

import urllib.request
yr = 2018;
mon = 8;
day = 30;
hr = 0;
mi = 0;

def pull_NOAA_F_10p7(yr, mon, day, hr, mi):
    
    mon_vec = [b'Jan', b'Feb', b'Mar', b'Apr', b'May', b'Jun', b'Jul', b'Aug', \
               b'Sep', b'Oct', b'Nov', b'Dec']
    #
    # Pull the current F_10.7 solar flux value
    #
    
    F_10p7 = [];
    mon_index = mon - 1;
    mon_string = mon_vec[int(mon_index)];
    #
    response = urllib.request.urlopen('ftp://ftp.swpc.noaa.gov/pub/weekly/27DO.txt')
    #
    for i in range(0, 38):
        line = response.readline()
        if i >=  11:
            if float(line[0:4]) == yr:
                if line[5:8] == mon_string:
                    if float(line[9:11]) == day:
                        F_10p7 = float(line[17:19])
                    #
                #
    
    if not F_10p7:
        raise ValueError('No valid F_10.7 flux value could be found');
    
                    






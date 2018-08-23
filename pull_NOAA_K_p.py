# -*- coding: utf-8 -*-
"""
This function will pull the current K_p values from the NOAA ftp site for use
in the Jacchia 71' atmospheric model. Note that these values will only work for 
current satellite propagations due to the fact that they are updated on a 27-day 
basis. The user should also have a valid internet connection to use this function.

Input:
    yr: Year of interest
    mon: Month of interest
    day: Day of interest
    hr: Hour of interst
    mi: Minute of interest

Copyright (c) Trevor Wolf 2018. All Rights Reserved.
"""
import urllib.request

#
# Pull the current K_p value - This value is pulled at 6.7 hours prior to the current state
#
psuedo_hr = hr + mi / 60.0;
hr_interst = psuedo_hr - 6.7;
#
if hr_interest < 0:
    hr_interest = hr_interest + 24.0;
    day_interest = day - 1;
    #
    if day_interest < 0:
        previous_month_flag = 1;
        #
        if mon == 1:
            previous_year_flag = 1;
            #
        else:
            previous_year_flag = 0;
        #
    else:
        previous_month_flag = 0;
    #
else:
    day_interest = day;
#
K_p = [];
#
response = urllib.request.urlopen('http://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt');
#
for j in range(0, 42):
    line = response.readline()
    if j >= 12:
        if float(line[0:4]) == yr:
            if float(line[5:7]) == mon:
                if float(line[8:10]) == day:
                    


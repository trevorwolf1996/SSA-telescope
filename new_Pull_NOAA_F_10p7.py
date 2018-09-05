# -*- coding: utf-8 -*-
"""
This is an updated version of the pull_NOAA_F_10p7.py. This file will draw all
of the values from a set of files updated a various time intervals by NOAA to
find the values of F_10.7 and F_10.7_bar. This progam's purpose is to fill in the 
gaps for each of the data sets in order to create one that spans the entire time 
domain from any time in the past, until present. Because of the nature of how NOAA
updates this flux value, there is not one data set that contains all the information 
needed to do this. The two data sets needed are yyyy.vm and quar_dsd.txt. Numeric values
of these files will then be converted to a numpy array to which the values will be 
easily accessible for analysis. 

Inputs:
    yr: Year of interest 
    mon: Month of interest

Outputs:
    F_10p7_obs_array: 

Copyright (c) Trevor Wolf 2018. All Rights Reserved. 
"""
import numpy as np
import urllib.request

def pull_NOAA_F_10p7(yr, mon):
    #
    # Pull historical information from the current and previous two quarters
    # Note: I am assuming that the ftp site only keeps four quarters up at any 
    # given time. For that reason, the follows if statements are structured this 
    # way. If this turns out not to be the case, then the file will need to be 
    # changed to accomadate. 
    #
    # ftp site
    #
    ftp_site = 'ftp://ftp.swpc.noaa.gov/pub/indices/old_indices/'
    #
    if mon < 4:
        #
        first_file = ftp_site + str(yr) + 'Q1_DSD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q2_DSD.txt';
        third_file = ftp_site + str(yr - 1) + 'Q3_DSD.txt';
        second_file = ftp_site + str(yr - 1) + 'Q4_DSD.txt';
        #
    elif mon < 7:
        #
        second_file = ftp_site + str(yr) + 'Q1_DSD.txt';
        first_file = ftp_site + str(yr) + 'Q2_DSD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q3_DSD.txt';
        third_file = ftp_site + str(yr - 1) + 'Q4_DSD.txt';
        #
    elif mon < 10:
        #
        third_file = ftp_site + str(yr) + 'Q1_DSD.txt';
        second_file = ftp_site + str(yr) + 'Q2_DSD.txt';
        first_file = ftp_site + str(yr) + 'Q3_DSD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q4_DSD.txt';
        
    else:
        #
        fourth_file = ftp_site + str(yr) + 'Q1_DSD.txt';
        third_file = ftp_site + str(yr) + 'Q2_DSD.txt';
        second_file = ftp_site + str(yr) + 'Q3_DSD.txt';
        first_file = ftp_site + str(yr) + 'Q4_DSD.txt';
            
#
# Extract the values contained in these files into an arrays starting from the 
# closest to date and moving backwards
#
    response = urllib.request.urlopen(first_file);
    #
    first_entry_flag = 1;
    #
    for line in reversed(list(response.readlines())):
        #
        if line.decode('utf-8')[0] == '#':
            break
        #
        yr_line = float(line[0:4]);
        mo_line = float(line[5:7]);
        day_line = float(line[8:10]);
        #
        F_10p7_value = float(line[13:15]);
        #
        if first_entry_flag == 1:
            #
            F_10p7_obs_array = np.array([yr_line, mo_line, day_line, F_10p7_value]);
            first_entry_flag = 0;
            #
        else:
            F_10p7_obs_array = np.vstack((F_10p7_obs_array, [yr_line, mo_line,\
                               day_line, F_10p7_value]));
            #
#
# Repeat the above for the next files in order from closest to-date to latest
#
    response = urllib.request.urlopen(second_file);
    #
    for line in reversed(list(response.readlines())):
        #
        if line.decode('utf-8')[0] == '#':
            break
        #
        yr_line = float(line[0:4]);
        mo_line = float(line[5:7]);
        day_line = float(line[8:10]);
        #
        F_10p7_value = float(line[13:15]);
        #
        F_10p7_obs_array = np.vstack((F_10p7_obs_array, [yr_line, mo_line,\
                               day_line, F_10p7_value]));
    #
    response = urllib.request.urlopen(third_file);
    #
    for line in reversed(list(response.readlines())):
        #
        if line.decode('utf-8')[0] == '#':
            break
        #
        yr_line = float(line[0:4]);
        mo_line = float(line[5:7]);
        day_line = float(line[8:10]);
        #
        F_10p7_value = float(line[13:15]);
        #
        F_10p7_obs_array = np.vstack((F_10p7_obs_array, [yr_line, mo_line,\
                               day_line, F_10p7_value]));
    #
    response = urllib.request.urlopen(fourth_file);
    #
    for line in reversed(list(response.readlines())):
        #
        if line.decode('utf-8')[0] == '#':
            break
        #
        yr_line = float(line[0:4]);
        mo_line = float(line[5:7]);
        day_line = float(line[8:10]);
        #
        F_10p7_value = float(line[13:15]);
        #
        F_10p7_obs_array = np.vstack((F_10p7_obs_array, [yr_line, mo_line,\
                               day_line, F_10p7_value]));
        #
    #
    return F_10p7_obs_array

yr = 2018;
mon = 9;

F_10p7_obs_array = pull_NOAA_F_10p7(yr, mon)
        
        
    
    
    
    
    
    

#
# Find the historical F_10.7 values contained in the data set yyyy.vm and save 
#



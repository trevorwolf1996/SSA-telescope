# -*- coding: utf-8 -*-
"""
This function will pull time-stamped K_p values from the NOAA ftp site for use
in the Jacchia 71' atmospheric model.

Input:
    yr: Year of interest
    mon: Month of interest
Output: 
    K_p_array: Array containing the K_p and the yr, month, day and hr that the 
               The observation was taken at 
    
Copyright (c) Trevor Wolf 2018. All Rights Reserved.
"""
import urllib.request
import numpy as np

def pull_NOAA_K_p(yr, mon):
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
        first_file = ftp_site + str(yr) + 'Q1_DGD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q2_DGD.txt';
        third_file = ftp_site + str(yr - 1) + 'Q3_DGD.txt';
        second_file = ftp_site + str(yr - 1) + 'Q4_DGD.txt';
        #
    elif mon < 7:
        #
        second_file = ftp_site + str(yr) + 'Q1_DGD.txt';
        first_file = ftp_site + str(yr) + 'Q2_DGD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q3_DGD.txt';
        third_file = ftp_site + str(yr - 1) + 'Q4_DGD.txt';
        #
    elif mon < 10:
        #
        third_file = ftp_site + str(yr) + 'Q1_DGD.txt';
        second_file = ftp_site + str(yr) + 'Q2_DGD.txt';
        first_file = ftp_site + str(yr) + 'Q3_DGD.txt';
        fourth_file = ftp_site + str(yr - 1) + 'Q4_DGD.txt';
        
    else:
        #
        fourth_file = ftp_site + str(yr) + 'Q1_DGD.txt';
        third_file = ftp_site + str(yr) + 'Q2_DGD.txt';
        second_file = ftp_site + str(yr) + 'Q3_DGD.txt';
        first_file = ftp_site + str(yr) + 'Q4_DGD.txt';
            
#
# Extract the values contained in these files into an arrays starting from the 
# closest to date and moving backwards
#
    response = urllib.request.urlopen(first_file);
    #
    first_entry_flag = 1;
    #
    hr_vec = [21, 18, 15, 12, 9, 6, 3, 0]; # This assumes that the average over three hours
    # is the value given at the epoch three hours prior
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
        # Find the values that are updated in 3-hr intervals
        for i in range(0, 8):
            #
            hr_line = hr_vec[i];
            #
            if i == 0:
                K_p_value = float(line[77:79]);
            elif i == 1:
                K_p_value = float(line[75:77]);
            elif i == 2:
                K_p_value = float(line[73:75]);
            elif i == 3:
                K_p_value = float(line[71:73]);
            elif i == 4:
                K_p_value = float(line[69:71]);
            elif i == 5:
                K_p_value = float(line[67:69]);
            elif i == 7:
                K_p_value = float(line[65:67]);
            #
            if first_entry_flag == 1:
                #
                K_p_array = np.array([yr_line, mo_line, day_line, hr_line,\
                                             K_p_value]);
                first_entry_flag = 0;
                #
            else:
                K_p_array = np.vstack((K_p_array, [yr_line, mo_line,\
                               day_line, hr_line, K_p_value]));
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
        # Find the values that are updated in 3-hr intervals
        for i in range(0, 8):
            #
            hr_line = hr_vec[i];
            #
            if i == 0:
                K_p_value = float(line[77:79]);
            elif i == 1:
                K_p_value = float(line[75:77]);
            elif i == 2:
                K_p_value = float(line[73:75]);
            elif i == 3:
                K_p_value = float(line[71:73]);
            elif i == 4:
                K_p_value = float(line[69:71]);
            elif i == 5:
                K_p_value = float(line[67:69]);
            elif i == 7:
                K_p_value = float(line[65:67]);
            #
            K_p_array = np.vstack((K_p_array, [yr_line, mo_line,\
                               day_line, hr_line, K_p_value]));
            #
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
        # Find the values that are updated in 3-hr intervals
        for i in range(0, 8):
            #
            hr_line = hr_vec[i];
            #
            if i == 0:
                K_p_value = float(line[77:79]);
            elif i == 1:
                K_p_value = float(line[75:77]);
            elif i == 2:
                K_p_value = float(line[73:75]);
            elif i == 3:
                K_p_value = float(line[71:73]);
            elif i == 4:
                K_p_value = float(line[69:71]);
            elif i == 5:
                K_p_value = float(line[67:69]);
            elif i == 7:
                K_p_value = float(line[65:67]);
            #
            K_p_array = np.vstack((K_p_array, [yr_line, mo_line,\
                               day_line, hr_line, K_p_value]));
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
        # Find the values that are updated in 3-hr intervals
        for i in range(0, 8):
            #
            hr_line = hr_vec[i];
            #
            if i == 0:
                K_p_value = float(line[77:79]);
            elif i == 1:
                K_p_value = float(line[75:77]);
            elif i == 2:
                K_p_value = float(line[73:75]);
            elif i == 3:
                K_p_value = float(line[71:73]);
            elif i == 4:
                K_p_value = float(line[69:71]);
            elif i == 5:
                K_p_value = float(line[67:69]);
            elif i == 7:
                K_p_value = float(line[65:67]);
            #
            K_p_array = np.vstack((K_p_array, [yr_line, mo_line,\
                               day_line, hr_line, K_p_value]));
        #
    #
    return K_p_array

#
# Test function
#
yr = 2018;
mon = 9;


K_p_array = pull_NOAA_K_p(yr, mon)





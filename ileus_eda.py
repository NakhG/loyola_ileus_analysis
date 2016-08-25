# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:24:21 2016

@author: gnakhleh
"""

#Loyola research on spine ileus

'''Questions: 
Does having an ileus predispose patients 
to longer stays, heart attacks, 
blood clots in lungs, deep vein thrombosis, 
sepsis or death?
'''

#Read in the data

import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

import os

os.chdir("C:\\Users\\gnakhleh\\Documents\\Loyola")

ileus_df = pd.read_stata("Spine Ileus\\SPINE_ILEUS_CA.dta")

ileus_df.shape #big: 198k rows, 237 columns

#we probably don't need all those columns...

#lets take a sample and inspect it visually
sample_ileus_df = ileus_df.sample(200, random_state = 902)
sample_ileus_df.to_csv("Spine Ileus\\spine_ileus_sample.csv")

#what do we see inspecting visually...
#Variables about comorbidities

#Look at column names where 'ileus' shows up
col_names = list(ileus_df.columns.values)
ileus_colnames = [s for s in col_names if 'ileus' in s.lower()]
ileus_colnames #we now have the ileus columns

'''
Looking at the .do file that goes with this ... 
It looks like the variables we are interested in are all of these ileus columns except ileus_NPOA
'''

#what about the other things we're interested in
#longer stays, heart attacks, pulmonary embolism, deep vein thromb., sepsis, death

comorbid_colnames = []
comorbid_strings = ['mi_', 'dvt_', 'sepsis', 'pe_']
for name in col_names:
    if any(string in name.lower() for string in comorbid_strings):
        comorbid_colnames.append(name)
        
comorbid_colnames #got em

#How could we test if any of those comorbidities are present
ileus_df[(ileus_df[comorbid_colnames] == 1).any(1)].shape
ileus_df[(ileus_df[comorbid_colnames] == 0).all(1)].shape
#those two things should add up to the length of the dataframe
len(ileus_df[(ileus_df[comorbid_colnames] == 1).any(1)].index) + len(ileus_df[(ileus_df[comorbid_colnames] == 0).all(1)].index)

#By this syntax, we should be able to get ileus diag's with...
ileus_diag_df = ileus_df[(ileus_df[ileus_colnames] == 1).any(1)]
100. * ileus_diag_df['DIED'].value_counts() / len(ileus_diag_df.index)
ileus_nodiag_df = ileus_df[(ileus_df[ileus_colnames] == 0).all(1)]
100. * ileus_nodiag_df['DIED'].value_counts() / len(ileus_nodiag_df.index)

#based on this, it looks like there's very little diff. at a high level between mortality rate of ileus diags and non diags
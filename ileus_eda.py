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
import matplotlib.pyplot as plt

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

#let's look at some of the comorbidities
100. * ileus_diag_df['MI_POA'].value_counts() / len(ileus_diag_df.index)
100. * ileus_nodiag_df['MI_POA'].value_counts() / len(ileus_nodiag_df.index)
100. * ileus_diag_df['MI_NPOA'].value_counts() / len(ileus_diag_df.index)
100. * ileus_nodiag_df['MI_NPOA'].value_counts() / len(ileus_nodiag_df.index)
#small diff's in myocardial infarction


100. * ileus_diag_df['Sepsis_NPOA'].value_counts() / len(ileus_diag_df.index)
100. * ileus_nodiag_df['Sepsis_NPOA'].value_counts() / len(ileus_nodiag_df.index)
#2% higher rate of sepsis npoa for ileus, less than 1% diff for poa

100. * ileus_diag_df['PE_POA'].value_counts() / len(ileus_diag_df.index)
100. * ileus_nodiag_df['PE_POA'].value_counts() / len(ileus_nodiag_df.index)
ileus_df['PE_NPOA'].value_counts()
ileus_df['PE_POA'].value_counts()
#No one in the dataset has pulmonary embolism

100. * ileus_diag_df['DVT_NPOA'].value_counts() / len(ileus_diag_df.index)
100. * ileus_nodiag_df['DVT_NPOA'].value_counts() / len(ileus_nodiag_df.index)
#1% diff. in deep vein thrombosis npoa, less for poa

#do that, but way faster
for colname in comorbid_colnames:
    diag_col_summary = 100. * ileus_diag_df[colname].value_counts() / len(ileus_diag_df.index)
    nodiag_col_summary = 100. * ileus_nodiag_df[colname].value_counts() / len(ileus_nodiag_df.index)
    print("Breakdown of {} for those with ileuses".format(colname))
    print(diag_col_summary)
    print("Breakdown of {} for those without ileuses".format(colname))
    print(nodiag_col_summary)
    print("\n")
    
def summary_comparer(colname_list, df_1, df_2, str_1, str_2):
    for colname in colname_list:
        df_1_summary = 100. * df_1[colname].value_counts() / len(df_1.index)
        df_2_summary = 100. * df_2[colname].value_counts() / len(df_2.index)
        print("Breakdown of {} for {}".format(colname, str_1))
        print(df_1_summary)
        print("Breakdown of {} for {}".format(colname, str_2))
        print(df_2_summary)
        print("\n")

#back to it: what about length of stay?
ileus_diag_df['LOS'].describe()
ileus_nodiag_df['LOS'].describe()

ileus_diag_df['LOS'].plot.box()
ileus_nodiag_df['LOS'].plot.box()


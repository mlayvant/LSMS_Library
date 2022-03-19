#!/usr/bin/env python

"""Pull region identifier from other_features and use as markets;
   concatenate other material in other features with
   household_characteristics.
"""

import pandas as pd
from cfe.df_utils import use_indices

DFs = ['food_expenditures','household_characteristics','food_quantities']

dir = '../var/%s.parquet'

oc = pd.read_parquet(dir % 'other_features')

def m_regions(df,oc):

    df = df.reset_index('m')
    oc = oc.reset_index('m')
    df['m'] = use_indices(oc,['m'])
    df = df.set_index(['j','t','m'])

    df = pd.concat([df,oc],axis=1)

    return df

for fn in DFs:
    df = pd.read_parquet(dir % fn)
    m_regions(df,oc).to_parquet(dir % fn)

    


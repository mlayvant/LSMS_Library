#!/usr/bin/env python

#2019
import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
from tanzania import age_sex_composition

myvars = dict(fn='../Data/HH_SEC_B.dta',
              HHID='sdd_hhid',
              sex='hh_b02',
              age='hh_b04')

df = age_sex_composition(**myvars)

df = df.filter(regex='ales ')

df['log HSize'] = np.log(df.sum(axis=1))

# Drop any obs with infinities...
df = df.loc[np.isfinite(df.min(axis=1)),:]

#reformat
df = df.reset_index()
df.insert(1, 't', '2019-20')
df.set_index(['j','t'], inplace = True)

df.to_parquet('household_characteristics.parquet')

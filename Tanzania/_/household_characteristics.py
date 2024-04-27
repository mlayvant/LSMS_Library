#!/usr/bin/env python
"""
Concatenate data on household characteristics across rounds.
"""

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
from tanzania import Waves, id_match
import dvc.api
from lsms import from_dta

y={}
for t in Waves.keys():
    y[t] = pd.read_parquet('../'+t+'/_/household_characteristics.parquet')
    #z[t] = id_match(z[t],t,Waves)

z = pd.concat(y.values())

z = z.reset_index().set_index(['j','t'])

# Get hh ids into nice string representation
ids = list(set(z.index.get_level_values('j')))
f2s = {k:str(k).split('.')[0] for k in ids}
z = z.rename(index=f2s,level='j')

try:
    of = pd.read_parquet('../var/other_features.parquet')
    z = z.join(of.reset_index('m')[['m']],on=['j','t'])
    z = z.reset_index().set_index(['j','t','m'])
except FileNotFoundError:
    warnings.warn('No other_features.parquet found.')
    z['m'] = 'Tanzania'
    z = z.reset_index().set_index(['j','t','m'])

z.columns.name = 'k'

z.to_parquet('../var/household_characteristics.parquet')

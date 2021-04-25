#!/usr/bin/env python
"""
Concatenate data on household characteristics across rounds.
"""

import pandas as pd

z={}
for t in ['2008-09','2010-11','2012-13','2014-15']:
    z[t] = pd.read_parquet('../'+t+'/_/household_characteristics.parquet')
    z[t] = z[t].stack('k')
    z[t] = z[t].reset_index().set_index(['j','k']).squeeze()

z = pd.DataFrame(z)
z = z.stack().unstack('k')
z.index.names=['j','t']

z.to_parquet('household_characteristics.parquet')

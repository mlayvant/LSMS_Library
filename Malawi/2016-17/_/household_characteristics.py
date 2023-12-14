#!/usr/bin/env python

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
import json
import dvc.api
from lsms import from_dta
from lsms.tools import get_household_roster
from malawi import age_sex_composition, sex_conv

with dvc.api.open('../Data/hh_mod_b.dta', mode='rb') as dta:
    df = from_dta(dta, convert_categoricals=True)

final = age_sex_composition(df, sex='hh_b03', sex_converter=sex_conv,
                           age='hh_b05a', age_converter=None, hhid='case_id')

final = final.reset_index()

final['t'] = '2016-17'
final = final.set_index(['j','t'])
final.columns.name = 'k'

final.to_parquet('household_characteristics.parquet')

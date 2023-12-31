#!/usr/bin/env python

import pandas as pd
import numpy as np
import json
import dvc.api
from lsms import from_dta
from lsms.tools import get_household_roster

def age_sex_composition(df, sex, sex_converter, age, age_converter, hhid):
    Age_ints = ((0,4),(4,9),(9,14),(14,19),(19,31),(31,51),(51,100))
    df = get_household_roster(df, sex=sex,  sex_converter=sex_converter,
                                  age=age, age_converter=age_converter, HHID= hhid,
                                  convert_categoricals=True,Age_ints=Age_ints,fn_type=None)
    df['log HSize'] = np.log(df[['girls', 'boys', 'men', 'women']].sum(axis=1))
    df.index.name = 'j'
    return df

def sex_conv(x):
    if str.lower(x) == 'female':
        return 'f'
    elif str.lower(x) == 'male':
        return 'm'

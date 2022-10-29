#!/usr/bin/env python
import sys
sys.path.append('../../_')
from uganda import nonfood_expenditures
import dvc.api
from lsms import from_dta

myvars = dict(fn='../Data/gsec15c.dta',
              item='itmcd',
              HHID='hhid',
              purchased='h15cq5',
              away=None,
              produced='h15cq7',
              given='h15cq9')

x = nonfood_expenditures(**myvars)

# "Wrong" hhid variable; get correct one from gsec1
with dvc.api.open('../Data/gsec1.dta',mode='rb') as f:
    ids = from_dta(f)[['HHID','hh']]

ids = ids.set_index('hh').squeeze().to_dict()

x = x.replace({'hhid':ids})

x.to_parquet('nonfood_expenditures.parquet')

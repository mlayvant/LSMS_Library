#!/usr/bin/env python
import sys
from lsms.tools import from_dta
import numpy as np
import dvc.api
import pandas as pd
sys.path.append('../../../_/')
from local_tools import df_from_orgfile

t = '2016-17'

selector_pur = {'hhid': 'j',
                'freqcd': 'i'}

#categorical mapping
labels = df_from_orgfile('./categorical_mapping.org',name='harmonize_food',encoding='ISO-8859-1')
labelsd = {}
for column in ['Code_9b', 'Code_8h']:
    labelsd[column] = labels[['Preferred Label', column]].set_index(column).to_dict('dict')
#units = df_from_orgfile('./categorical_mapping.org',name='s8hq9',encoding='ISO-8859-1')
#unitsd = units.set_index('Code').to_dict('dict')

#food expenditure
with dvc.api.open('../Data/g7sec9b_small.dta',mode='rb') as dta:
    df = from_dta(dta, convert_categoricals=False)
    #harmonize food labels
    df['freqcd'] = df['freqcd'].replace(labelsd['Code_9b']['Preferred Label'])

df['hhid'] = (df.apply(lambda x:f"{int(x['clust']):d}/{int(x['nh']):02d}",axis=1))
#df['clust'].astype(int).astype("string")+'/'+df['nh'].astype(int).astype("string")


#create purchased column labels for each visit -- from the 2nd to 11th visit
selector_pur.update({f's9bq{i}a':f'purchased_value_v{i}' for i in range(1,7)})
selector_pur.update({f's9bq{i}b':f'purchased_quantity_v{i}' for i in range(1,7)})
selector_pur.update({f's9bq{i}c':f'purchased_unit_v{i}' for i in range(1,7)})

x = df.rename(columns=selector_pur)[[*selector_pur.values()]]
x = x.replace({r'':np.nan, 0 : np.nan})
x = x.groupby(['j','i']).sum() # Deal with some cases with multiple records for purchases
x = pd.wide_to_long(x.reset_index(),['purchased_value','purchased_quantity','purchased_unit'],['j','i'],'visit',sep='_v')
x = x.replace(0,np.nan).dropna(how='all')

# Only select food expenditures,since section9b also recorded non-food expenditures.
x = x.loc[x.index.isin(labelsd['Code_9b']['Preferred Label'].values(),level='i')]

# Add null unit index
x = x.rename(columns={'purchased_unit':'u'})
x = x.reset_index().set_index(['j','i','u','visit'])

# Home produced amounts
with dvc.api.open('../Data/g7sec8h.dta',mode='rb') as dta:
    prod = from_dta(dta, convert_categoricals=False)
    #harmonize food labels and map unit labels:
    #prod['foodcd'] = prod['foodcd'].replace(labelsd['Code_8h']['Preferred Label'])
    #prod['s8hq13'] = prod['s8hq13'].replace(unitsd['Label'])

prod = prod[prod['s8hq1'] == 1] #select only if hh consumed any own produced food in the past 12 months
#create produced column labels for each visit -- 3-day recall starting from the 2nd to 7th visit

prod['hhid'] = (prod.apply(lambda x:f"{int(x['clust']):d}/{int(x['nh']):02d}",axis=1))

selector_pro = {'hhid': 'j',
                'foodcd': 'i'}

selector_pro.update({f's8hq{i}q':f'produced_quantity_v{i}' for i in range(3,9)})
selector_pro.update({f's8hq{i}u':f'produced_unit_v{i}' for i in range(3,9)})
selector_pro.update({f's8hq{i}p':f'produced_price_v{i}' for i in range(3,9)})

y = prod.rename(columns=selector_pro)[[*selector_pro.values()]]
#unit code 1.7498005798264095e+100 has no categorical mapping
y.index = y.index.map(str)

#unstack by visits
y = y.replace({r'':np.nan, 0 : np.nan})
y = y.dropna(how='all')
y = pd.wide_to_long(y.reset_index(),['produced_quantity','produced_unit','produced_price'],['j','i'],'visit',sep='_v')
y = y.rename(labelsd['Code_8h']['Preferred Label'],level='i')

y = y.join(x,how='outer')

y['t'] = t
y = y.reset_index().set_index(['j','t','i','u','visit'])

fa = y.groupby(['j','t','i','u']).sum()
fa = fa.replace(0,np.nan).dropna(how='all')

# Deal with non-string values in units
fa.index = fa.index.set_levels(fa.index.levels[3].astype(str),level='u')
fa.to_parquet('food_acquired.parquet')

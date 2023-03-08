#!/usr/bin/env python
import sys
sys.path.append('../../_/')
from ethiopia import food_acquired

fn='../Data/sect5a_hh_w2.dta'

myvars = dict(item='hh_s5aq00',                  # Code label uniquely identifying food
              HHID='household_id2',                # Unique household id
              quantity = 'hh_s5aq02_a',           # Quantity of food consumed
              units = 'hh_s5aq02_b',              # Units for food consumed
              value_purchased  = 'hh_s5aq04',     # Total value of food purchased
              quantity_purchased = 'hh_s5aq03_a', # Quantity of food purchased
              units_purchased = 'hh_s5aq03_b')

df = food_acquired(fn,myvars)

df.to_parquet('food_acquired.parquet')

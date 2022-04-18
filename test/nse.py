# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 00:01:20 2021

@author: Saprative Jana
"""

from datetime import date
from nsepy import get_history
sbin = get_history(symbol='SBIN',
                   start=date(2022,1,1),
                   end=date(2022,1,10))

print(sbin)
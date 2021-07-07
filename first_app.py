# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from math import sqrt, atan, log, exp, sin, cos, tan

from scipy.integrate import odeint
from scipy.optimize import *

#from one_zone_model_v1test import *
import one_zone_model_v1test

pd.options.display.max_columns = 999

st.write("""
         # My first app test
         Hello *world!*
         """)
         
data=None

fl=st.file_uploader("Drop data here (excel file)")
if fl is not None:
    data=fl.getvalue()
    dataname=fl.name

if data is not None:
    data_zone=pd.read_excel(data,sheet_name="zone")

st.write(data_zone)

data_zone=data_zone.set_index('parameters')
data_zone = data_zone.T   #transpose, so indices becomes column names
st.write(data_zone)
UA_opaqi=data_zone['UA_opaqi'].values[0]
UA_opaqe=data_zone['UA_opaqe'].values[0]
UA_walli=data_zone['UA_walli'].values[0]
UA_windows=data_zone['UA_windows'].values[0]
Hv=data_zone['Hv'].values[0]
frad=data_zone['frad'].values[0]
Cwalli=data_zone['Cwalli'].values[0]
Copaq=data_zone['Copaq'].values[0]
Cem=data_zone['Cem'].values[0]
mdot_em=data_zone['mdot_em'].values[0]
Afl=data_zone['Afl'].values[0]
Vi=data_zone['Vi'].values[0]
Rfl=data_zone['Rfl'].values[0]

Ti_zone,Qdot_zone,Ti= one_zone_model_v1test.zone_model(UA_opaqi,UA_opaqe,UA_walli,UA_windows,Hv,frad,Cwalli,Copaq,Cem,mdot_em,Afl,Vi,Rfl)
st.write(Ti_zone)
Ti_zone=Ti_zone.set_index('time')
st.write(Ti_zone)
st.line_chart(Ti_zone)
#plt.figure
#plt.plot(Ti_zone['time'],Ti_zone['Tair'], color= 'C1', label="Tair")
#st.pyplot()
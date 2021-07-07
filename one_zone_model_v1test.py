import pandas as pd                 # Data tables
import os                           # Returns current directory, create files
import numpy as np                  # Arrays
import matplotlib.pyplot as plt	    # Graphs

from math import sqrt, atan, log

from scipy.integrate import odeint

def zone_model(UA_opaqi,UA_opaqe,UA_walli,UA_windows,Hv,frad,Cwalli,Copaq,Cem,mdot_em,Afl,Vi,Rfl):
    v_air=0.8401 # [m^3/kg] "specific volume of humid air per kg of dry air"
    cp_air=1020 # [J/kg-K] "specific heat capacity of humid air per kg of dry air"
    c_water = 4187  #[J/kgK]
    Tinit=20
    # Time in s
    # Create an array of evenly-spaced values
    t_initial = 0
    t_final=48*3600
    delta_t = 10*60
    t = np.arange(t_initial,t_final+1,delta_t)
    
    Te=-8  #in te lezen!!!!!!!!!!!!!!
    Cair= 5*Vi*cp_air/v_air
  
    Ti0= [Tinit]
    Ti0.extend([Tinit])
    Ti0.extend([Tinit])
    Ti0.extend([Tinit])
    
    def RC_model(Ti,t):
        Tair = Ti[0]
        Topaq = Ti[1]
        Twalli = Ti[2]
        Tem = Ti[3]
        Top = 0.5*Tair+0.25*Topaq+0.25*Twalli
        
        #Pemitter
        Tin= 30
        eff_em=0.9
        Pemitter = 10.8*Afl*(Tem-Top) #10.8W/m²K

        #emitter node
        #Qdot_water_em = mdot_em*c_water*eff_em*(Tin-Tem)
        Qdot_water_em = mdot_em*c_water*(Tin-Tem)/(Rfl*c_water*mdot_em+0.5)
        #nog toe te voegen: zonnewinsten, interne winsten
        Iem= -Pemitter+ Qdot_water_em
        dTem =  Iem/Cem    
        
        Qdot_air_walli = UA_walli*(Twalli-Tair)
        Qdot_air_opaq = UA_opaqi*(Topaq-Tair)
        
        #air node
        Qdot_air_wind = UA_windows*(Te-Tair)
        Qdot_vent = Hv*(Te-Tair)   
        Qdot_em_air = (1-frad)*Pemitter
        #nog toe te voegen: zonnewinsten, interne winsten (resp 50% en 80%)
        Iair=Qdot_air_walli+Qdot_air_opaq+Qdot_air_wind+Qdot_vent+Qdot_em_air
        dTair = Iair/Cair
        
        #external wall node
        Qdot_opaq_ext = UA_opaqe*(Te-Topaq)
        Qdot_em_opaq = 0.1*frad*Pemitter
        #nog toe te voegen: zonnewinsten, interne winsten (resp 50% en 80%)
        Iopaq = -Qdot_air_opaq+Qdot_opaq_ext+Qdot_em_opaq
        dTopaq =  Iopaq/Copaq     
        
        #internal wall node
        Qdot_em_walli = 0.9*frad*Pemitter
        #nog toe te voegen: zonnewinsten, interne winsten (resp 40% en 10%) of aan te passen want deel nr vloer(node emitter)
        Iwalli = Qdot_em_walli -Qdot_air_walli
        dTwalli =  Iwalli/Cwalli      
        
        
        dTi=[dTair]
        dTi.extend([dTopaq])
        dTi.extend([dTwalli])
        dTi.extend([dTem])
        
        return (dTi,Pemitter,Qdot_water_em)
   
    def afgeleide(Ti,t):
        ret = RC_model(Ti,t) # only dTi_T is returned for ordinary differential integral
        return ret[0]
   
    Ti = odeint(afgeleide , Ti0, t)    
    
    Pemitter = np.asarray([RC_model(Ti[tt],t[tt])[1] for tt in range(len(t))])
    Qdot_water_em= np.asarray([RC_model(Ti[tt],t[tt])[2] for tt in range(len(t))])
    
    Ti_zone=pd.DataFrame({'Tair':Ti[:,0],'Topaq':Ti[:,1],'Twalli':Ti[:,2],'Tem':Ti[:,3]})
    Ti_zone['time']=t
    Ti_zone['Tair'] = round(Ti_zone['Tair'],2)
    Ti_zone['Topaq'] = round(Ti_zone['Topaq'],2)
    Ti_zone['Twalli'] = round(Ti_zone['Twalli'],2)
    Ti_zone['Tem'] = round(Ti_zone['Tem'],2)
    
    Qdot_zone=pd.DataFrame()
    Qdot_zone['time']=t
    Qdot_zone['Pemitter']=Pemitter
    Qdot_zone['Pemitter'] = round(Qdot_zone['Pemitter'],0)
    Qdot_zone['Qdot_em']=Qdot_water_em
    Qdot_zone['Qdot_em'] = round(Qdot_zone['Qdot_em'],0)   
    
    return Ti_zone,Qdot_zone,Ti
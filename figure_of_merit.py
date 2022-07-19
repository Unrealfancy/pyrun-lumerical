# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:14:49 2022

@author: zhouziji
"""

def figure_of_merit(x,sim):
    import numpy as np    
    um=1e-6
    Size_x=np.array([3 , 3 , 3])*um
    Size_D=np.array([0.2 , x[0] , x[1]])*um
    S_materials=["Ag (Silver) - CRC","Al2O3 - Palik","Ag (Silver) - CRC"]        
    S_wavelenth=[0.2*um,1*um,501]
    S_Periodic=0.5*um
    sim.build2d(Size_x,Size_D,S_materials,S_wavelenth,S_Periodic)
    sim.run()
    RAT=sim.RAT()
    fom_range=[0.5*um,0.55*um]

    step=(S_wavelenth[1]-S_wavelenth[0])/S_wavelenth[2]
    point1=int((fom_range[0]-S_wavelenth[0])/step)
    point2=int((fom_range[1]-S_wavelenth[0])/step)
    y=1-np.mean(RAT[1][point1:point2])
    return y,RAT


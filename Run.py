# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 15:57:59 2022

@author: zhouziji
"""

import numpy as np
from Sim_fdtd import *
from PSA import *
# file_path="D:\simulation\MCT\python\MCT3.fsp"
file_path="D:\simulation\python\SiNpdms-20220615_20nmSiN-PDMS_Total4.5um.fsp"

txt_path="D:\simulation\python\R.txt"
data = np.loadtxt(txt_path) 

a=Sim_fdtd(file_path)
b=a.modify('uni_par_distr','r max', 0.01*10**-6)
# b=a.build3d(Size_x,Size_z,Size_D,S_materials,S_wavelenth,S_Periodic,S_Efield,olap)
# c=a.build2d(Size_x,Size_D,S_materials,S_wavelenth,S_Periodic)
d=a.run()
f,e=a.RAT()
# e=a.Efield(0)
# a.close()

opti=PSA(2,3,[[1,0.05,2],[2,0.2,3]],a)
returndata=opti.run();


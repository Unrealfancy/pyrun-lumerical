# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 11:02:39 2022

@author: dell
"""
import numpy as np
import build_structure
from scipy import constants
import importlib.util
import sys, os
sys.path.append(r'C:\Program Files\Lumerical\v202\api\python'+'\\') #Default windows lumapi path
sys.path.append(os.path.dirname(__file__)) #Current directory
os.add_dll_directory(r'C:\Program Files\Lumerical\v202\api\python'+'\\')
path = importlib.util.spec_from_file_location('lumapi', r"C:\Program Files\Lumerical\v202\api\python\lumapi.py")
#Functions that perform the actual loading
lumapi = importlib.util.module_from_spec(path)
path.loader.exec_module(lumapi)
import lumapi

um = 1e-6
file_name="D:\simulation\MCT\python\MCT.fsp"
fdtd = lumapi.FDTD(file_name)
S_type="3d"
Size_x=np.array([3 , 3 , 0.1])*um
Size_z=np.array([3 , 3 , 1.5])*um
Size_D=np.array([0.1 , 0.1 , 0.01])*um
S_materials=["Ag (Silver) - CRC","Al2O3 - Palik","Ag (Silver) - CRC"]
S_wavelenth=[0.5*um,2*um,501]
S_Periodic=0.5*um
S_Efield=[-1]

build_structure.build(fdtd,S_type,Size_x,Size_z,Size_D,S_materials,S_wavelenth,S_Periodic,S_Efield)
fdtd.run()
wavelength=constants.c/fdtd.getdata("R","f")
R=fdtd.transmission('R')
T=-fdtd.transmission('T')
# time.sleep(15)
fdtd.close()
    
cc=build_structure.aa
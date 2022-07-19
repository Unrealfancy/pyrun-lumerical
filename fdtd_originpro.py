import sys, os
import numpy as np

import matplotlib.pyplot as plt
import originpro as op
import os
import importlib.util
from mpl_toolkits.mplot3d import Axes3D
import time
sys.path.append("C:\\Program Files\\Lumerical\\v202\\api\\python\\") #Default windows lumapi path
sys.path.append(os.path.dirname(__file__)) #Current directory
os.add_dll_directory("C:\\Program Files\\Lumerical\\v202\\api\\python\\")
#The default paths for windows and linux
path = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py')
#Functions that perform the actual loading
lumapi = importlib.util.module_from_spec(path) #windows
path.loader.exec_module(lumapi)
import lumapi

###############
um=1e-6
file_name="D:\simulation\MCT\python\MCT.fsp"
S_type="3d"
Size_x=np.array([3 , 3 , 0.1])*um
Size_z=np.array([3 , 3 , 1.5])*um
Size_D=np.array([0.1 , 0.1 , 0.01])*um
S_materials=["Ag (Silver) - CRC","Al2O3 - Palik","Ag (Silver) - CRC"]
S_wavelenth=[0.5*um,2*um,501]
S_Periodic=0.5*um
S_Efield=[-1]
fdtd=lumapi.FDTD(file_name)
##############
def bulid_structure(S_type,Size_x,Size_z,Size_D,S_materials,S_wavelenth,S_Periodic,S_Efield):
    status=fdtd.layoutmode()
    print(status)
    if (status==0): 
        fdtd.switchtolayout()
    fdtd.deleteall()
    n=len(S_materials)
    Y=list(range(n+1))
    Y[0]=0
    Y[1]=Size_D[0]
    
    for i in range(0, n):
        Y[i+1]=Y[i]+Size_D[i]
        fdtd.addrect(name="layer"+str(i),x=0,z=0,x_span=Size_x[i],z_span=Size_z[i],y_min=Y[i],y_max=Y[i+1],material=S_materials[i])
    
    fdtd.addfdtd(dimension=S_type,x=0,z=0,x_span=S_Periodic,z_span=S_Periodic,y_min=0,y_max=Y[n]+2*S_Periodic,force_symmetric_x_mesh=1,force_symmetric_z_mesh=1,
                  allow_symmetry_on_all_boundaries=1, x_min_bc='Anti-Symmetric',x_max_bc='Anti-Symmetric',Mesh_accuracy=2,PML_layers=32)
    if S_type=="3d":
        fdtd.set("z min bc",'Symmetric')
        fdtd.set("z max bc",'Symmetric')
        
    fdtd.addplane(injection_axis='y', direction='backward', x=0, z=0, x_span=S_Periodic, z_span=S_Periodic,
                  y=Y[n]+S_Periodic, wavelength_start=S_wavelenth[0], wavelength_stop=S_wavelenth[1])
    if S_type=="3d":
        fdtd.set("polarization angle",90)
     
    fdtd.setglobalmonitor("frequency points",S_wavelenth[2]);
    fdtd.setglobalmonitor('use wavelength spacing',1);
    if (0 in S_Efield):        
        fdtd.addprofile(name='XY_Field',override_global_monitor_settings=1,use_wavelength_spacing=1,monitor_type=7,
                    x=0,z=0,x_span=S_Periodic,y_min=0,y_max=Y[n])
    elif (-1 in S_Efield):        
        pass
    else:
        fdtd.addprofile(name='XY_Field',override_global_monitor_settings=1,use_wavelength_spacing=1,monitor_type=7,
                        x=0,z=0,x_span=S_Periodic,y_min=Y[min(S_Efield)-1],y_max=Y[max(S_Efield)])
        
    fdtd.addpower(name='R',override_global_monitor_settings=1,use_wavelength_spacing=1,monitor_type=6,
                    x=0,z=0,x_span=S_Periodic,z_span=S_Periodic,y=Y[n]+1.5*S_Periodic)
    
    fdtd.addpower(name='T',override_global_monitor_settings=1,use_wavelength_spacing=1,monitor_type=6,
                    x=0,z=0,x_span=S_Periodic,y=0)
   
#######################
bulid_structure(S_type,Size_x,Size_z,Size_D,S_materials,S_wavelenth,S_Periodic,S_Efield)
fdtd.run()
wavelength=constants.c/fdtd.getdata("R","f")
R=fdtd.transmission('R')
T=-fdtd.transmission('T')
plt.plot(wavelength,R,wavelength,T)
# time.sleep(15)
# fdtd.close()


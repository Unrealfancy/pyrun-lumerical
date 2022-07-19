# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:19:00 2022

@author: zhouziji
"""


class Sim_fdtd(object):
    def __init__(self, file_path):
        import importlib.util
        import sys
        import os
        # Default windows lumapi path
        sys.path.append(r'C:\Program Files\Lumerical\v202\api\python'+'\\')
        sys.path.append(os.path.dirname(__file__))  # Current directory
        os.add_dll_directory(
            r'C:\Program Files\Lumerical\v202\api\python'+'\\')
        path = importlib.util.spec_from_file_location(
            'lumapi', r"C:\Program Files\Lumerical\v202\api\python\lumapi.py")
        #Functions that perform the actual loading
        lumapi = importlib.util.module_from_spec(path)
        path.loader.exec_module(lumapi)
        self.path = file_path
        import lumapi
        if (os.access(file_path, os.F_OK)):
            self.fdtd = lumapi.FDTD(self.path)
        else:
            self.fdtd = lumapi.FDTD()
            self.fdtd.save(file_path)
            self.fdtd.select('FDTD')
            self.fdtd.setview('extent')

    def build3d(self, Size_x, Size_z, Size_D, S_materials, S_wavelenth, S_Periodic, S_Efield=-1, ovlap=((0, 0), (2, 2))):
        status = self.fdtd.layoutmode()
        if (status == 0):
            self.fdtd.switchtolayout()
        self.fdtd.deleteall()
        n = len(S_materials)
        Y = list(range(n+1))
        Y[0] = 0
        order = 0
        if (isinstance(ovlap[0], (int, float))):
            ol = [int(ovlap[0])]
            mesh = [int(ovlap[1])]
        else:
            ol = list(map(int, ovlap[0]))
            mesh = list(map(int, ovlap[1]))
        for i in range(0, n):
            if (i+1 in ol):
                Y[i+1] = Y[i-1]+Size_D[i]
                self.fdtd.addrect(name="layer"+str(i), x=0, z=0, x_span=Size_x[i], z_span=Size_z[i], y_min=Y[i-1], y_max=Y[i+1],
                                  material=S_materials[i], override_mesh_order_from_material_database=1, mesh_order=mesh[order])
                order += 1
            else:
                Y[i+1] = Y[i]+Size_D[i]
                self.fdtd.addrect(name="layer"+str(i), x=0, z=0,
                                  x_span=Size_x[i], z_span=Size_z[i], y_min=Y[i], y_max=Y[i+1], material=S_materials[i])

        self.fdtd.addfdtd(dimension='3d', x=0, z=0, x_span=S_Periodic, z_span=S_Periodic, y_min=0, y_max=Y[n]+2*S_Periodic, force_symmetric_x_mesh=1, force_symmetric_z_mesh=1,
                          allow_symmetry_on_all_boundaries=1, x_min_bc='Anti-Symmetric', x_max_bc='Anti-Symmetric', z_min_bc='Symmetric', z_max_bc='Symmetric',
                          Mesh_accuracy=2, PML_layers=32)

        self.fdtd.addplane(injection_axis='y', direction='backward', x=0, z=0, x_span=S_Periodic, z_span=S_Periodic,
                           y=Y[n]+S_Periodic, wavelength_start=S_wavelenth[0], wavelength_stop=S_wavelenth[1], polarization_angle=90)

        self.fdtd.setglobalmonitor("frequency points", S_wavelenth[2])
        self.fdtd.setglobalmonitor('use wavelength spacing', 1)
        if (isinstance(S_Efield, (int, float))):
            S_Efield = [int(S_Efield)]
            ##change int to list
        else:
            S_Efield = list(S_Efield)
            ##for matlab import as np.array
            S_Efield = list(map(int, S_Efield))
        if (0 in S_Efield):
            self.fdtd.addprofile(name='E', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=7,
                                 x=0, z=0, x_span=S_Periodic, y_min=0, y_max=Y[n])
        elif (min(S_Efield) > 1 and max(S_Efield) <= n):
            self.fdtd.addprofile(name='E', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=7,
                                 x=0, z=0, x_span=S_Periodic, y_min=Y[min(S_Efield)-1], y_max=Y[max(S_Efield)])

        elif (-1 in S_Efield):
            pass
        else:
            print("Efield out of range,please set between 0-max_layer")
        self.fdtd.addpower(name='R', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=6,
                           x=0, z=0, x_span=S_Periodic, z_span=S_Periodic, y=Y[n]+1.5*S_Periodic)

        self.fdtd.addpower(name='T', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=6,
                           x=0, z=0, x_span=S_Periodic, y=0)
        self.fdtd.selectpartial('layer')
        self.fdtd.setview('extent')

    def build2d(self, Size_x, Size_D, S_materials, S_wavelenth, S_Periodic, S_Efield=-1, ovlap=(0, 2)):
        status = self.fdtd.layoutmode()
        if (status == 0):
            self.fdtd.switchtolayout()
        self.fdtd.deleteall()
        n = len(S_materials)
        Y = list(range(n+1))
        Y[0] = 0
        order = 0
        # ovlap=list(ovlap)
        # print(ovlap)
        if (isinstance(ovlap[0], (int, float))):
            ol = [int(ovlap[0])]
            mesh = [int(ovlap[1])]
        else:
            ol = list(map(int, ovlap[0]))
            mesh = list(map(int, ovlap[1]))
        for i in range(0, n):
            if (i+1 in ol):
                Y[i+1] = Y[i-1]+Size_D[i]
                self.fdtd.addrect(name="layer"+str(i), x=0, z=0, x_span=Size_x[i], z_span=Size_x[i], y_min=Y[i-1], y_max=Y[i+1],
                                  material=S_materials[i], override_mesh_order_from_material_database=1, mesh_order=mesh[order])
                order += 1
            else:
                Y[i+1] = Y[i]+Size_D[i]
                self.fdtd.addrect(name="layer"+str(i), x=0, z=0,
                                  x_span=Size_x[i], z_span=Size_x[i], y_min=Y[i], y_max=Y[i+1], material=S_materials[i])

        self.fdtd.addfdtd(dimension="2d", x=0, z=0, x_span=S_Periodic, y_min=0, y_max=Y[n]+2*S_Periodic, force_symmetric_x_mesh=1,
                          allow_symmetry_on_all_boundaries=1, x_min_bc='Anti-Symmetric', x_max_bc='Anti-Symmetric', Mesh_accuracy=2, PML_layers=32)

        self.fdtd.addplane(injection_axis='y', direction='backward', x=0, z=0, x_span=S_Periodic, z_span=S_Periodic,
                           y=Y[n]+S_Periodic, wavelength_start=S_wavelenth[0], wavelength_stop=S_wavelenth[1])

        self.fdtd.setglobalmonitor("frequency points", S_wavelenth[2])
        self.fdtd.setglobalmonitor('use wavelength spacing', 1)
        if (isinstance(S_Efield, (int, float))):
            S_Efield = [int(S_Efield)]
            ##change int to list
        else:
            S_Efield = list(S_Efield)
            ##for matlab import as np.array
            S_Efield = list(map(int, S_Efield))
        if (0 in S_Efield):
            self.fdtd.addprofile(name='E', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=7,
                                 x=0, z=0, x_span=S_Periodic, y_min=0, y_max=Y[n])
        elif (min(S_Efield) > 1 and max(S_Efield) <= n):
            self.fdtd.addprofile(name='E', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=7,
                                 x=0, z=0, x_span=S_Periodic, y_min=Y[min(S_Efield)-1], y_max=Y[max(S_Efield)])
        elif (-1 in S_Efield):
            pass
        else:
            print("Efield out of range,please set between 0-max_layer")
        self.fdtd.addpower(name='R', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=6,
                           x=0, z=0, x_span=S_Periodic, z_span=S_Periodic, y=Y[n]+1.5*S_Periodic)

        self.fdtd.addpower(name='T', override_global_monitor_settings=1, use_wavelength_spacing=1, monitor_type=6,
                           x=0, z=0, x_span=S_Periodic, z_span=S_Periodic, y=0)
        self.fdtd.selectpartial('layer')
        self.fdtd.setview('extent')

    def modify(self, pname, setname, setdata):
        status = self.fdtd.layoutmode()
        if (status == 0):
            self.fdtd.switchtolayout()
        self.fdtd.select(pname)
        self.fdtd.set(setname, setdata)

    def run(self):
        self.fdtd.run()

    def close(self):
        self.fdtd.close()

    def RAT(self):
        wl = 3*10**8/self.fdtd.getdata("R", "f")
        R = self.fdtd.transmission('R')
        T = -self.fdtd.transmission('T')
        self.A = 1-R-T
        return wl, R, T, self.A

    def Efield(self, point='max'):
        chek = self.fdtd.getdata('E')
        if chek == 0:
            print('Efield doesnt exist!')
        else:
            import numpy as np
            wl = 3*10**8/self.fdtd.getdata("R", "f")
            x = self.fdtd.getdata('E', 'x')
            y = self.fdtd.getdata('E', 'y')
            # z=self.fdtd.getdata('E','z')
            E = np.sqrt(self.fdtd.getelectric('E'))
            if (point == 'max'):
                idx = np.argmax(self.A)
            elif (point == 'min'):
                idx = np.argmin(self.A)
            else:
                idx = point
            E = E[:, :, 0, idx]
            wlidx = wl[idx]
            return x, y, E, wlidx

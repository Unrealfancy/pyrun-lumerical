
% %%%%%  Run when first used   %%%%%%
% pyversion('D:\Anaconda\python.exe')
% 
% %%%%   Reload Python module(Run when change py module)  %%%%%
clear classes
obj = py.importlib.import_module('Sim_fdtd');
py.importlib.reload(obj);

clear;clc;
file_path='D:\simulation\MCT\python\MCT.fsp'
Sim=py.Sim_fdtd.Sim_fdtd(file_path);

%%%%%%%%%% parameter input %%%%%%%%%%%%%%
um=1e-6;
X=[1,1,0.17]*um;
Z=[3,3,1,1]*um;
D=[0.2,0.10,0.04]*um;
Materials={"Au (Gold) - CRC","Si (Silicon) - Palik","Au (Gold) - CRC"};
Wavelenth=[0.5*um,3*um,501];
Periodic=0.34*um;
Efield=[0];
olap={0,0};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:1
%     D=[0.2,0.09,0.01*i]*um;
    Sim.build2d(X,D,Materials,Wavelenth,Periodic,Efield,olap);
%     Sim.build3d(X,Z,D,Materials,Wavelenth,Periodic,Efield,olap);
    Sim.run();
    Plot_RAT(Sim);
end

Plot_RAT(Sim);
Plot_E(Sim,'max',10);
Sim.close()



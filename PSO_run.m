% %%%%%  Run when first used   %%%%%%
% pyversion('D:\Anaconda\python.exe')
% 
% %%%%   Reload Python module(Run when change py module)  %%%%%
clear;clc;
clear classes
obj1 = py.importlib.import_module('PSA');
py.importlib.reload(obj1);
obj2 = py.importlib.import_module('Sim_fdtd');
py.importlib.reload(obj2);
obj3 = py.importlib.import_module('figure_of_merit');
py.importlib.reload(obj3);


file_path='D:\simulation\MCT\python\MCT.fsp'
Sim=py.Sim_fdtd.Sim_fdtd(file_path);
pop_range={[0.1,0.01],[0.3,0.02]};
% speed_range={[-0.2,-0.02,-0.2],[0.2,0.02,0.2]};
opti=py.PSA.PSA(4,6,pop_range,Sim);
returndata=opti.run();
Sim.close()
plot_PSA(returndata)

plot(1:10,1:10,'color',[1,0,0])
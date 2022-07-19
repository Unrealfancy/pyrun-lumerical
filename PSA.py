# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:49:08 2022
@author: zhouziji
"""


import numpy as np
import matplotlib.pyplot as plt
class PSA(object):
    def __init__(self,itimes,pop_size,pop_range,sim=None,speed_range=None):       
        self.itimes=int(itimes)
        self.pop_size=int(pop_size)
        self.pop_range=[np.array(pop_range[0]),np.array(pop_range[1])]
        self.learnf=(2,2)
        if speed_range==None:
            speed=0.1*(self.pop_range[1]-self.pop_range[0])
            self.speed_range=[-1.0*speed,speed]
        else:    
            self.speed_range=[np.array(speed_range)[0],np.array(speed_range)[1]]
        self.Pnum=len(pop_range[0])
        self.sim=sim

    def fom(self,x):
        import figure_of_merit as F_O_M 
        y,self.R=F_O_M.figure_of_merit(x,self.sim)  
        return y


    def inipop (self,pop_size):
        pop = np.zeros((pop_size, self.Pnum))
        v = np.zeros((pop_size, self.Pnum))
        fitness = np.zeros(pop_size)
        R=[]
        for i in range(pop_size):
            pop[i] = np.random.random(self.Pnum)*(self.pop_range[1]-self.pop_range[0])+self.pop_range[0]
            v[i] = np.random.random(self.Pnum)*(self.speed_range[1]-self.speed_range[0])+self.speed_range[0]
            fitness[i] = self.fom(pop[i])
            R.append(self.R[1])
        wl=self.R[0]
        return pop, v, fitness,wl,R


    def getbest(self,fitness,pop):
        Gbestpop=pop[fitness.argmax()].copy()
        Gbestfitness=fitness.max()
        Pbestpop=pop.copy()
        Pbestfitness=fitness.copy()
        return Gbestpop,Gbestfitness,Pbestpop,Pbestfitness


    def run(self):
        pop,V,fitness,wl,R=self.inipop(self.pop_size)      
        Gbestpop,Gbestfitness,Pbestpop,Pbestfitness=self.getbest(fitness, pop) 
        result=[Gbestfitness]
        resultpop=[list(Gbestpop)]
        Reflection=[R]
        fig,axes=plt.subplots(self.itimes+1,self.pop_size,sharex=True,sharey=True,dpi=100)
        for k in range(self.pop_size):
            axes[0,k].set(title='itimes0,number'+str(k+1)+'\n'+str(pop[k].astype('float16')))
            axes[0,k].plot(wl,R[k])
        for i in range(self.itimes):
            R=[]
            for j in range(self.pop_size): 
                V[j] = (0.5*(100-i)/100+0.4) * V[j] + self.learnf[0] * \
                    np.random.rand() * (Pbestpop[j] - pop[j]) + \
                    self.learnf[1] * np.random.rand() * (Gbestpop - pop[j])
                V[j] = np.maximum(V[j] , self.speed_range[0])
                V[j] = np.minimum(V[j] , self.speed_range[1])
                # updata speed,where the first term denote inertia factor (form 0.9-0.4）


            for j in range (self.pop_size):
                pop[j]=V[j]+pop[j]
                pop[j] = np.maximum(pop[j] , self.pop_range[0])
                pop[j] = np.minimum(pop[j] , self.pop_range[1])


            for j in range(self.pop_size):
                fitness[j]=self.fom(pop[j])            
                R.append(self.R[1])
                axes[i+1,j].set(title='itimes'+str(i+1)+',number'+str(j+1)+'\n'+str((pop[j].astype('float16'))))
                axes[i+1,j].plot(wl,R[j])
                if fitness[j]>Pbestfitness[j]:
                    Pbestfitness[j]=fitness[j]
                    Pbestpop[j]=pop[j].copy()


            if Pbestfitness.max()>Gbestfitness:
                Gbestfitness=Pbestfitness.max()
                Gbestpop=pop[Pbestfitness.argmax()].copy()
            fig.tight_layout()
            print('Optimal result parameters: '+str(Gbestpop))
            print('Optimal result: '+str(Gbestfitness))
            Reflection.append(R)
            result.append(Gbestfitness)
            resultpop.append(list(Gbestpop))
        return result,resultpop,wl,Reflection




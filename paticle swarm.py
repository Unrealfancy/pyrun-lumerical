# -*- coding: utf-8 -*-
"""
Created on Tue May 25 19:53:47 2021

@author: dell
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

class PSO(object):
    def __init__(self):
        self.iter=300 #迭代次数
#         self.w=1 #惯性权重
        self.lr = (2, 2)  #粒子群个体和社会的学习因子，即加速常数
        self.sizepop=20 #种群规模
        self.rangepop=(-2,2) #粒子的位置的范围限制,x、y方向的限制相同
        self.rangespeed=(-0.5,0.5) #速度限制
        self.px=[]  #当前全局最优解
        self.py=[]


    def func(self, x):
        # x输入粒子位置
        # y 粒子适应度值
        if (x[0] == 0) & (x[1] == 0):
            y = np.exp((np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1])) / 2) - 2.71289
        else:
            y = np.sin(np.sqrt(x[0] ** 2 + x[1] ** 2)) / np.sqrt(x[0] ** 2 + x[1] ** 2) + np.exp(
                (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1])) / 2) - 2.71289
        return y


    def initpopvfit(self, sizepop):
        pop = np.zeros((sizepop, 2))
        v = np.zeros((sizepop, 2))
        fitness = np.zeros(sizepop)
        for i in range(sizepop):
            pop[i] = [(np.random.rand() - 0.5) * self.rangepop[0] * 2, (np.random.rand() - 0.5) * self.rangepop[1] * 2]
            v[i] = [(np.random.rand() - 0.5) * self.rangepop[0] * 2, (np.random.rand() - 0.5) * self.rangepop[1] * 2]
            fitness[i] = self.func(pop[i])
        return pop, v, fitness


    def getinitbest(self, fitness, pop):
        # 群体最优的粒子位置及其适应度值
        gbestpop, gbestfitness = pop[fitness.argmax()].copy(), fitness.max()
        # 个体最优的粒子位置及其适应度值,使用copy()使得对pop的改变不影响pbestpop，pbestfitness类似
        pbestpop, pbestfitness = pop.copy(), fitness.copy()
        return gbestpop, gbestfitness, pbestpop, pbestfitness
 
    
    def run(self):
        """
        通过循环迭代，不断的更新粒子的位置和速度，根据新粒子的适应度值更新个体和群体的极值
        :return:
        """
        pop, v, fitness = self.initpopvfit(self.sizepop)
        gbestpop, gbestfitness, pbestpop, pbestfitness = self.getinitbest(fitness, pop)

        result = np.zeros(self.iter)
        for i in range(self.iter):
            # 速度更新
            for j in range(self.sizepop):
                v[j] = (0.5*(100-i)/100+0.4) * v[j] + self.lr[0] * \
                    np.random.rand() * (pbestpop[j] - pop[j])
                + self.lr[1] * np.random.rand() * (gbestpop - pop[j])
            v[v < self.rangespeed[0]] = self.rangespeed[0]
            v[v > self.rangespeed[1]] = self.rangespeed[1]

            # 粒子位置更新
            for j in range(self.sizepop):
                pop[j] += v[j]
            pop[pop < self.rangepop[0]] = self.rangepop[0]
            pop[pop > self.rangepop[1]] = self.rangepop[1]
 
            # 适应度更新
            for j in range(self.sizepop):
                fitness[j] = self.func(pop[j])
 
            for j in range(self.sizepop):
                if fitness[j] > pbestfitness[j]:
                    pbestfitness[j] = fitness[j]
                    pbestpop[j] = pop[j].copy()
 
            if pbestfitness.max() > gbestfitness:
                gbestfitness = pbestfitness.max()
                gbestpop = pop[pbestfitness.argmax()].copy()
 
            result[i] = gbestfitness
            self.px.append(gbestpop[0])
            self.py.append(gbestpop[1])
        return result, self.px, self.py
 
    def drawPaht(self,X, Y, Z, px, py, pz):
        """
        绘图
        """
        fig = plt.figure()
        ax = Axes3D(fig)
        plt.title("PSO")
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='b', )
        ax.set_xlabel('x label', color='r')
        ax.set_ylabel('y label', color='g')
        ax.set_zlabel('z label', color='b')
        ax.plot(px, py, pz, 'r.')  # 绘点x
        plt.show()
        

def f(X, Y):
    return np.sin(np.sqrt(X ** 2 + Y ** 2)) / np.sqrt(X ** 2 + Y ** 2) + np.exp(
        (np.cos(2 * np.pi * X) + np.cos(2 * np.pi * Y)) / 2) - 2.71289
a=0
b=0
for i in range(1000):
    pso = PSO()
    result, px, py = pso.run()
    print(max(result), result.argmax())
    if max(result)>1:
        a+=1
    else :
        b+=1
print(a,b)


plt.plot(result)

X = np.arange(-2, 2, 0.05)
Y = np.arange(-2, 2, 0.05)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)
pso.drawPaht(X, Y, Z, px, py, f(np.array(px), np.array(py)))
plt.show()

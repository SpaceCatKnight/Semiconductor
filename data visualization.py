# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:22:41 2017

@author: mrsom
"""

'''Der Peak von T und der von V liegen ca. 5s auseinander.
T hat gegenueber V den Vorteil, dass das Maximum nur einmal erreicht wird, statt 20mal
'''


import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize


data1 = np.loadtxt(fname='Full R data.txt', skiprows=7)

V = data1[:,0]
R = data1[:,1]
T = data1[:,2]
t = data1[:,3]

#data2 = np.loadtxt(fname='Full PID data.txt', skiprows=6)


#Ausreisser ausglätten
Vmin = np.min(V)
Vmax = np.max(V)
for i in range(len(V)):
    if V[i] == Vmin:
        V[i] = V[i-1]
#    if V[i] == Vmax:
#        print('Vmax at t = ', t[i])
    
#Cool- und Heat-Teil voneinander trennen
Tmax = np.max(T)
for i in range(len(T)):
    if T[i] == Tmax:
#        print('Tmax at t = ', t[i])
        V_heat = V[:i]
        V_cool = V[i:]
        R_heat = R[:i]
        R_cool = R[i:]       
        T_heat = T[:i]
        T_cool = T[i:]
        t_heat = t[:i]
        t_cool = t[i:]

'''
plt.subplot(221)
plt.plot(T_heat,R_heat,'r')

plt.subplot(222)
plt.plot(V_heat,R_heat,'b')

plt.subplot(223)
plt.plot(T_cool,R_cool,'g')

plt.subplot(224)
plt.plot(V_cool,R_cool,'y')

plt.figure()
plt.plot(t,T,'r')
plt.figure()
plt.plot(t,V,'g')
'''
plt.figure()
plt.plot(V,R)
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:29:36 2017

@author: mrsom
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

data = np.loadtxt('data_test.txt')

eV = 1.6021766208*10**(-19)
k_B = 1.38064852*10**(-23)

#print(np.exp(1.107*eV/(2*k_B*300))/10000)

V = data[:,0]
R = data[:,1]
T = data[:,2]
t = data[:,3]

A_B_guess = [1/10000,1.107*eV/(2*k_B)]

def func(T,A,B):
    return A*np.exp(B/T)

param = scipy.optimize.curve_fit(func,T,R,A_B_guess)[0]

A_new = float(param[0])
B_new = float(param[1])


plt.figure()
plt.plot(T,R)
plt.plot(T,func(T,A_new,B_new))
plt.show()

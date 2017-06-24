# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:29:36 2017

@author: mrsom
"""

'''
- in eigenen Worten zeigen, dass wir 4-Punktmessung und PID-Regler verstanden haben
- erklären, wieso man Vakuum braucht
- Fehler qualitativ nennen (nicht ganz intrinsisch, Raumtemperatur geraten, übliches)
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

#Tabellenfunktion
a = 24.3124079487
b = 1.05876485886
def tabelle(V,a,b):
    return a*V + b
    
    
#Konstanten
eV = 1.6021766208*10**(-19)
k_B = 1.38064852*10**(-23)


#Daten auslesen
data = np.loadtxt('data_test.txt')
V_0 = data[:,0] #V
R = data[:,1] #Ohm
T_C = data[:,2] #C
t = data[:,3] #s

V = 10**3*np.array(V_0) #mV
T = 273.15+np.array(T_C) #K


#Temperatur aus Spannung bestimmen
T_0 = 26
T_1 = tabelle(V,a,b)

def Uth(V, T_0,a,b):
    uv = (T_0-b)/a
    return V + uv

T_korr = tabelle(Uth(V,T_0,a,b),a,b)
T_korr = 273.15+np.array(T_korr)


#exponentielle Fitfunktion
A_B_guess = [100,1.107*eV/(2*k_B)]

def func(T,A,B):
    return A*T**(-3/2)*np.exp(B/T)

param = scipy.optimize.curve_fit(func,T,R,A_B_guess)[0]
A_new = float(param[0])
B_new = float(param[1])
print(A_new)
print(B_new)
'''
plt.figure()
plt.plot(T,R,'r')
#plt.plot(T,func(T,*A_B_guess),'g')
plt.plot(T,func(T,A_new,B_new))
plt.show()
'''


#lineare Fitfunktion
def linearfit(x,a,b):
    return a*x + b

guess = [1.107*eV/(2*k_B),1]
Tfit= T_korr[400:1200]
Rfit=R[400:1200]
a,b = scipy.optimize.curve_fit(linearfit,1/Tfit,np.log(Rfit),guess)[0]

plt.plot(1/T_korr,np.log(R))
plt.plot(1/Tfit, linearfit(1/Tfit,a,b))

print(a*2*k_B/eV)
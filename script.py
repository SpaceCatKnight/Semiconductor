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
data = np.loadtxt(fname='Full R data.txt', skiprows=7)

V_0 = data[:,0] #V
R = data[:,1] #Ohm
T_C = data[:,2] #°C
t = data[:,3] #s

V = 10**3*np.array(V_0) #mV
T = 273.15+np.array(T_C) #K


#Ausreisser ausglätten
Vmin = np.min(V)
Vmax = np.max(V)
for i in range(len(V)):
    if V[i] == Vmin:
        V[i] = V[i-1]
#    if V[i] == Vmax:
#        print('Vmax at t = ', t[i])
        

#Temperatur aus Spannung bestimmen
T_0 = 26
T_1 = tabelle(V,a,b)

def Uth(V, T_0,a,b):
    uv = (T_0-b)/a
    return V + uv

T_korr = tabelle(Uth(V,T_0,a,b),a,b)
T_korr = 273.15+np.array(T_korr)


#Cool- und Heat-Teil voneinander trennen
Vmax = np.max(V)
for i in range(len(V)):
    if V[i] == Vmax:
#        print('Vmax at t = ', t[i])
        T_korr_heat = T_korr[:i]
        T_korr_cool = T_korr[i:]
        R_heat = R[:i]
        R_cool = R[i:]       
        T_heat = T[:i]
        T_cool = T[i:]
        t_heat = t[:i]
        t_cool = t[i:]

        
#lineare Fitfunktion
def linearfunc(x,a,b):
    return a*x + b

def LogRange(R,a,b,accuracy): #gibt Start- und End-Indizes eines ausgewaehlten Log-Bereichs aus
    A = 0
    B = 0
    for i in range(len(R)):
        if np.log(R[i]) >= a-accuracy and np.log(R[i]) <= a+accuracy:
            A = i
        if np.log(R[i]) >= b-accuracy and np.log(R[i]) <= b+accuracy:
            B = i
    return A,B

def linearfit(T,R,Log_R_range,guess,title):
    A,B = LogRange(R,*Log_R_range)
    if A > B:
        A,B = B,A
    Tfit= T[A:B]
    Rfit= R[A:B]
    a,b = scipy.optimize.curve_fit(linearfunc,1/Tfit,np.log(Rfit),guess)[0]
    sigma = np.sqrt(np.diag(scipy.optimize.curve_fit(linearfunc,1/Tfit,np.log(Rfit),guess)[1]))
    
    plt.figure()
    plt.semilogy(1/T*1000,R,'b',label='Messung')
    plt.semilogy(1/Tfit*1000,Rfit,'r',label='linearer Bereich')
    plt.semilogy(1/T*1000, np.exp(linearfunc(1/T,a,b)),'g--',label='linearer Fit')
    plt.xlabel(r'$T^{-1}$ [$10^{-3} \cdot $K$^{-1}$]')
    plt.ylabel(r'$R$ [$\Omega$]')
    plt.title(title)
    plt.legend(loc=2)
    print('a: ',a,'\n b: ',np.exp(b))
    print('Sigma von a : ',sigma[0],'\n Sigma von b: ',np.exp(sigma[1]))
    print('Band gap energy in eV: ',a*2*k_B/eV)
    print('Sigma von E_g: ',sigma[0]*2*k_B/eV)
    

guess = [1.107*eV/(2*k_B),1]


#Plot R/T

#print('\n','Reglertemperatur beim Aufheizen:')
#linearfit(T_heat,R_heat,[6.25,10,1e-2],guess,'Aufheizen')
#plt.savefig('reglertemp_heat.png',dpi=250)
#plt.show()

print('\n','korrigierte Temperatur beim Aufheizen:')
linearfit(T_korr_heat,R_heat,[3.09,11.9,1e-1],guess,'Aufheizen')
plt.savefig('temp_heat.png',dpi=250)
#plt.show()

#print('\n','Reglertemperatur beim Abkuehlen:')
#linearfit(T_cool,R_cool,[3.5,12,1e-3],guess,'Abkühlen')
#plt.savefig('reglertemp_heat.png',dpi=250)
#plt.show()

print('\n','korrigierte Temperatur beim Abkuehlen:')
linearfit(T_korr_cool,R_cool,[3.22,12,1e-3],guess,'Abkühlen')
plt.savefig('temp_cool.png',dpi=250)
#plt.show()




#Plot T/t
"""
plt.figure()
plt.plot(t[:5000],T[:5000],label='Reglertemperatur')
plt.plot(t[:5000],T_korr[:5000],label='Probentemperatur')
plt.xlabel('$t$ [s]')
plt.ylabel('$T$ [K]')
plt.legend(loc=4)
plt.savefig('temp_time.png',dpi=250)
"""

#Plot R/T

plt.figure()
plt.plot(T_korr_heat,R_heat/1000,label='Aufwärmprozess')
plt.plot(T_korr_cool,R_cool/1000,label='Abkühlprozess')
plt.xlabel('$T$ [K]')
plt.ylabel('$R$ [$k\Omega$]')
plt.legend(loc=1)
plt.xlim(300,450)
plt.savefig('res_temp.png',dpi=250)



'''
#exponentielle Fitfunktion
A_B_guess = [100,1.107*eV/(2*k_B)]

def func(T,A,B):
    return A*T**(-3/2)*np.exp(B/T)

param = scipy.optimize.curve_fit(func,T,R,A_B_guess)[0]
A_new = float(param[0])
B_new = float(param[1])
print(A_new)
print(B_new)

plt.figure()
plt.plot(T,R,'r')
#plt.plot(T,func(T,*A_B_guess),'g')
plt.plot(T,func(T,A_new,B_new))
plt.show()
'''

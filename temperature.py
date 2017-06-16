import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

T = np.array([   0,   5,  10,  15,  20,   25,   30,   35,   40,   45,   50,   60,   70,   75,   80,   90,   95,  100,  120,  140,  150,  160,  180,  200,  220,  240,   250,   260,   280,   300,   325,   350,   375,   400,   450,   500,   550])
V = np.array([.000,.198,.397,.597,.798,1.000,1.203,1.407,1.611,1.817,2.022,2.436,2.850,3.058,3.266,3.681,3.888,4.095,4.919,5.733,6.137,6.539,7.338,8.137,8.938,9.745,10.151,10.560,11.381,12.207,13.247,14.292,15.342,16.395,18.513,20.640,22.772])


def func(V,a,b):
    return a*V + b
    
print(func(V,a_new,b_new))

fit = scipy.optimize.curve_fit(func,V,T)[0]

a_new, b_new = fit
print(a_new)
print(b_new)

plt.figure()
plt.plot(V,T)
plt.plot(V,func(V,a_new,b_new))
plt.show()

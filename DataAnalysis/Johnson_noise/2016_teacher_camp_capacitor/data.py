from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

'''
R = 1 Mohm
'''
def fit_model(params, x):
    A = params['A'].value
    B = params['B'].value
    output = A*np.exp(-B*x)
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)/err

v_rms = np.array([5.58,
                  4.26,
                  3.36,
                  2.65,
                  2.11,
                  1.754,
                  1.388,
                  1.126,
                  0.925,
                  0.758,
                  0.624,
                  0.516,
                  0.429,
                  0.361,
                  0.304,
                  0.257,
                  0.220,
                  0.189,
                  0.1615,
                  0.1399,
                  0.1227,
                  0.1075,
                  0.0949,
                  0.0841,
                0.0750,
                0.0675,
                0.0609,
                0.0552,
                0.0504,
                0.0460,
                0.0422,
                0.0388,
                0.0360,
                0.0334
                  ])

time = np.array([10,
                 20,
                 30,
                 40,
                 50,
                 60,
                 70,
                 80,
                 90,
                 100,
                 110,
                 120,
                 130,
                 140,
                 150,
                 160,
                 170,
                 180,
                 190,
                 200,
                 210,
                 220,
                 230,
                 240,
                250,
                260,
                270,
                280,
                290,
                300,
                310,
                320,
                330,
                340
                 ])

x = time
y = v_rms
yerr = y*0.02

params = lmfit.Parameters()
 
params.add('A', value = 9.0)
params.add('B', value = 0.65)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),200)

figure = pyplot.figure(0)

#print x_plot
#print fit_model(result.params,x_plot)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)

#pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.show()
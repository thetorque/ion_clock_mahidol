from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
'''
R = 3.02Mohm
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

v_rms = np.array([8.13,
                  7.21,
                  6.46,
                  5.84,
                  5.28,
                  4.78,
                  4.33,
                  3.94,
                  3.59,
                  3.27,
                  2.98,
                  2.73,
                  2.49,
                  2.27,
                  2.08,
                  1.91,
                  1.75,
                  1.61,
                  1.48,
                  1.36,
                  1.26,
                  1.16,
                  1.07,
                  0.98,
                  0.91,
                  0.84
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
                260
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
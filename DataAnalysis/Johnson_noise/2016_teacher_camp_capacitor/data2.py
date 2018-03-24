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

v_rms = np.array([8.40,
                  7.52,
                  6.75,
                  6.09,
                  5.48,
                  4.94,
                  4.48,
                  4.04,
                  3.65,
                  3.29
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
                 100
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

R_m = 10.0e6
R_c = 3.02e6

print "R effective is ", R_m*R_c/(R_m+R_c)

print "C is ", 1/(result.params['B'].value*(R_m*R_c/(R_m+R_c)))
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)

#pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.show()
from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
from scipy.interpolate import interp1d




def fit_johnson_model(params, x):
    A = params['Af'].value
    C = params['Cf'].value
    #print "x is " + str(x)
    #print "new_R is " + str(new_R)
    output = A*(x+C)
    #print x
    return output
'''
define how to compare data to the function
'''
def fit_johnson_fit(params , x, data, err):
    model = fit_johnson_model(params, x)
    return (model - data)



bg_noise = 0.00149

v_rms = 0.001*np.array([2.677,4.254,6.200, 4.987,6.058])
t_c = np.array([67.5,33.0,13.25, 26.25,15.25])
res = np.array([1904.0,7000.0,17160.0, 9510.0,15770.0])

y = v_rms**2 - bg_noise**2

y = y/res
y = y*1e9

x = t_c

yerr = 0.03*y


params = lmfit.Parameters()
 
params.add('Af', value = 8.2224e-3, vary = True)
params.add('Cf', value = 269.15, vary = True)
 
result = lmfit.minimize(fit_johnson_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(-300,x.max(),1000)


figure = pyplot.figure(0)

#print x

pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot),linewidth = 3.0)


#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   
pyplot.xlabel('T (Celcius)')
pyplot.ylabel('$V^2/R$ (x $10^{-9}$ mV$^2$/$\Omega$)')
#pyplot.ylim([0.00000005,0.001])

pyplot.ylim([0.0,3.0])
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9]) 

pyplot.show()
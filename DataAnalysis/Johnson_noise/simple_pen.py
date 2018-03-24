from __future__ import division
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

### define fitting function

def fit_model(params, x):
    L_0 = params['L_0'].value
    g = params['g'].value
    output = 4*np.pi**2*(x+L_0)/g
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)/err

### define raw data

period_1 = np.array([36.58, 34.32, 31.88, 29.16, 26.44, 23.03, 19.35])
period_2 = np.array([36.54,34.16,31.94,29.10,26.47,23.09,19.38])
period_3 = np.array([36.41,34.25,31.81,29.12,26.32,23.16,19.31])

period = ((period_1+period_2+period_3)/3.0/20)**2

period_err = 2*np.sqrt(period)*0.4/np.array([20,20,20,20,20,20,20])
D = 0.01*np.array([80,70,60,50,40,30,20])


### define what to fit

x = D
y = period
yerr = period_err

### fit

params = lmfit.Parameters()

params.add('g', value = 11, vary = True)
params.add('L_0', value = 0.034, vary = True)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

print "chi_sq is ", result.redchi

## plot

x_plot = np.linspace(0.0,x.max(),4000)

figure = pyplot.figure(0)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)
#pyplot.plot(x_plot,fit_model(params,x_plot),linewidth = 3.0)

#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.xlabel('Length $L$ (cm)')
pyplot.ylabel('$T^2$ (s$^2$)')

#pyplot.ylim([0.0,3.5])
#pyplot.xlim([0.0,0.9])

pyplot.show()
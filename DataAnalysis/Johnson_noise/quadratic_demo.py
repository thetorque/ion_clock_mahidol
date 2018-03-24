from __future__ import division
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

### define fitting function

def fit_model(params, x):
    a_0 = params['a_0'].value
    a_1 = params['a_1'].value
    a_2 = params['a_2'].value
    output = a_0 + a_1*x + a_2*x**2
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

period = ((period_1+period_2+period_3)/3.0/20)#**2

period_err = 2*np.sqrt(period)*0.4/np.array([20,20,20,20,20,20,20])
D = 0.01*np.array([80,70,60,50,40,30,20])

print period
print period_err 

### define what to fit

x = D
y = period
yerr = period_err

### fit

params = lmfit.Parameters()

params.add('a_0', value = 0.713, vary = True)
params.add('a_1', value = 1.4399, vary = True)
params.add('a_2', value = 0.00, vary = True)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

print "chi_sq is ", result.redchi**2

## plot

x_plot = np.linspace(x.min(),x.max(),4000)

figure = pyplot.figure(0)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 2.0)
#pyplot.plot(x_plot,fit_model(params,x_plot),linewidth = 2.0)

#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.xlabel('x data')
pyplot.ylabel('y data')

#pyplot.ylim([0.0,3.5])
#pyplot.xlim([0.0,0.9])

pyplot.show()
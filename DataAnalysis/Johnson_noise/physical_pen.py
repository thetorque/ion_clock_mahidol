from __future__ import division
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

### define fitting function

def fit_model(params, x):
    k = params['k'].value
    g = params['g'].value
    x_cm = params['x_cm'].value
    D = x - x_cm
    output = 2*np.pi*np.sqrt((k**2+D**2)/(np.absolute(g*D)))
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)/err

### define raw data

period_1 = np.array([1.65,1.61, 1.58, 1.55, 1.53, 1.54, 1.58, 1.65, 1.93, 2.60])
period_err_1 = 0.4/np.array([20,20,20,20,20,20,15,10,10,5])
D_1 = np.array([50.5, 45.5, 40.5, 35.5, 30.5, 25.5, 20.5, 15.5, 10.5, 5.5])
period_2 = np.array([2.71, 1.97, 1.71, 1.61, 1.55, 1.53, 1.55, 1.58, 1.61])
period_err_2 = 0.4/np.array([5,5,10,15,20,20,20,20,20])
D_2 = np.array([4.5, 9.5, 14.5, 19.5, 24.5, 29.5, 34.5, 39.5, 44.5])

period = np.append(period_1,period_2)
D = np.append(D_1+49.5,49.5-D_2)
period_err = np.append(period_err_1,period_err_2)

### define what to fit

x = D
y = period
yerr = period_err

### fit

params = lmfit.Parameters()

params.add('g', value = 988, vary = True)
params.add('k', value = 28, vary = True)
params.add('x_cm',value = 50, vary = True)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

print "chi_sq is ", result.redchi**2

## plot

x_plot = np.linspace(x.min(),x.max(),4000)

figure = pyplot.figure(0)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)


pyplot.xlabel('Distance $D$ (cm)')
pyplot.ylabel('Period $T$ (s)')


#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   


pyplot.ylim([1.4,3.0])

pyplot.show()
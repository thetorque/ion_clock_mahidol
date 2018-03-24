from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit


def fit_model(params, x):
    A = params['A'].value
    B = params['B'].value
    output = A*x**B
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)/err

bg_noise = 0.001043

#v_rms = 0.001*np.array([4.543, 5.205, 5.471, 6.950, 8.737, 12.111, 23.22, 33.08, 46.37, 50.2, 57.54, 58.96, 59.59])

v_rms = 0.001*np.array([
13.7,
10,
4.8,
3.4,
1.83,
1.5,
1.17])

#res = np.array([
#47.19,
#149.99,
#200.9,
#511,
#1003.5,
#2204,
#10012,
#20040,
#68320,
#101750, 
#223140,
#476300,
#1014300])

res = np.array([
100000,
46000,
10000,
4600,
1000,
470,
100])

x = res
y = np.sqrt(v_rms**2 - bg_noise**2)
yerr = y*0.05

params = lmfit.Parameters()
 
params.add('A', value = 0.0008)
params.add('B', value = 0.5, vary = False)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),2000)

figure = pyplot.figure(0)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)

pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.show()
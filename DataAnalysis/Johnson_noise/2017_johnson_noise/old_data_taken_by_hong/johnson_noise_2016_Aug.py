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

bg_noise = 0.007

v_rms = np.array([0.0081,
0.0092,
0.0128,
0.028,
0.088,
0.164,
0.406,
0.9993,
1.3787,
#1.423,
2.614])

res = np.array([100,
200,
422,
1500,
4900,
9968,
26905,
67700,
94530,
#120100,
219000])

x = res
y = np.sqrt(v_rms**2 - bg_noise**2)
yerr = y*0.10

params = lmfit.Parameters()
 
params.add('A', value = 0.0008)
params.add('B', value = 0.5)
 
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
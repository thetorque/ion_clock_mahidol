'''
We observe photon scattered from the Cs cell with quarter wave-plate rotated.
'''
from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
from scipy.interpolate import interp1d

# 0 degrees is 220.0 #
angle = np.arange(0,360.0,10.0)

print angle

volt = np.array([51.72,
    52.05,
    53.20,
    54.20,
    54.96,
    55.10,
    54.52,
    53.41,
    52.35,
    51.95,
    52.00,
    52.70,
    53.50,
    54.05,
    54.10,
    53.50,
    52.34,
    51.33,
    51.00,
    51.62,
    52.65,
    53.77,
    54.38,
    54.40,
    53.72,
    52.46,
    51.60,
    51.40,
    51.74,
    52.66,
    53.46,
    54.03,
    53.87,
    53.10,
    51.85,
    50.70])

x = angle
y = volt
yerr = volt*0.001

### fit johnson noise


def fit_sine_model(params, x):
    A = params['Af'].value
    B = params['Bf'].value
    C = params['Cf'].value
    D = params['Df'].value
    E = params['Ef'].value

    output = A*(np.sin(B*x+C))-D*x+E
    #print x
    return output
'''
define how to compare data to the function
'''
def fit_sine_fit(params , x, data, err):
    model = fit_sine_model(params, x)
    return (model - data)/err


params = lmfit.Parameters()
 
params.add('Af', value = 2, vary = True)
params.add('Bf', value = 2*np.pi/90.0, vary = True)
params.add('Cf', value = 0.0, vary = True)
params.add('Df', value = 0.0, vary = True)
params.add('Ef', value = 52.0, vary = True)
 
result = lmfit.minimize(fit_sine_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),1000)

print result.redchi

figure = pyplot.figure(0)

#print x
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_sine_model(result.params,x_plot),linewidth = 2.0, color = 'green')

#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   
pyplot.xlabel('angle (degrees)')
pyplot.ylabel('$V$ (mV)')
#pyplot.ylim([0.00000005,0.001])



'''
k = np.array([0.6087,0.9604, 1.191, 1.269, 1.33, 1.37, 1.405])
R = np.array([])
'''


pyplot.show()
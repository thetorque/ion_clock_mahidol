from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit


def fit_model(params, x):
    #A = params['A'].value
    #B = params['B'].value
    #output = A*x**B
    #k = params['k'].value
    #g = params['g'].value
    #x_cm = params['x_cm'].value
    emf = params['emf'].value
    r_in = params['r_in'].value
    #D = x - x_cm
    output = (emf**2)*x/((x+r_in)**2)
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)/err



volt = np.array([2.85,5.79,4.18,6.37,5.25,6.75,7.08,2.41,3.29,1.83])
res = np.array([82,300,150,382,232,450,532,64.4,100,45.1])

volt = np.array([x for (y,x) in sorted(zip(res,volt))])
res = np.sort(res)


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


# x = res
# y = np.sqrt(v_rms**2 - bg_noise**2)
# yerr = y*0.05

power = volt**2/res

x = res
y = power
yerr = y*0.01


params = lmfit.Parameters()
 
#params.add('A', value = 0.0008)
#params.add('B', value = 0.5, vary = False)

params.add('r_in', value = 500, vary = True)
params.add('emf', value = 6, vary = True)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),2000)

#x_plot = np.linspace(0,x.max(),2000)

figure = pyplot.figure(0)
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)

#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

# 9.8 pm 0.1, 29.1 pm 0.3
# 9.5 pm 0.1 , 28.4 pm 0.3

#pyplot.ylim([1.4,3.0])

pyplot.show()
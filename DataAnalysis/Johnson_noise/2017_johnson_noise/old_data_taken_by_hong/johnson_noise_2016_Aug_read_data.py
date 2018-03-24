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

bg_noise = 0.0043

v_rms = np.array([0.005,
0.0058,
0.007,
0.009,
0.0105,
0.018,
0.024,
0.033,
0.0455,
#0.061,
#0.073
])

res = np.array([120,
250,
500,
980,
1500,
5000,
10000,
20400,
47660,
#120000,
#216000
])


# data_list = [#["scope_1.csv",5],
#              ["scope_2.csv",5],
#              ["scope_3.csv",5],
#              ["scope_4.csv",5],
#              ["scope_5.csv",5],
#              ["scope_6.csv",5],
#              ["scope_7.csv",5],
#              ["scope_8.csv",5],
#              ["scope_9.csv",5],
#              ["scope_10.csv",5],
#              #["scope_11.csv",5],
#              ["scope_12.csv",5],
#              ]
# 
# v_rms = np.array([])
# 
# for i in range(int(np.size(data_list)/2)):
#     data_1 = np.loadtxt(data_list[i][0], skiprows=data_list[i][1],delimiter = ",") 
#     rms = np.sqrt(np.sum((data_1[:,1] - np.average(data_1[:,1]))**2/np.size(data_1[:,1])))
#     print rms
#     v_rms = np.append(v_rms,rms)

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
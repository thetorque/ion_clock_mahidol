from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

def fit_freq_model(params, x):
    A = params['A'].value ### low pass frequency
    B = params['B'].value ### high pass frequency
    C = params['C'].value ### gain
    D = params['D'].value ### offset
    f_l = x/A
    f_h = x/B
    output = C**2*(f_h**2/(1+(f_h**2)))*(1/(1+f_l**2))-D
    return output
'''
define how to compare data to the function
'''
def fit_freq_fit(params , x, data, err):
    model = fit_freq_model(params, x)
    return (model - data)#/err

v_in = 0.000396

v_out = np.array([1.12,
1.28,
1.36,
1.44,
1.60,
1.68,
1.84,
1.92,
2.08,
2.16,
2.24,
2.40,
2.48,
2.64,
2.72,
2.80,
2.96,
3.04,
3.12,
3.28,
3.36,
3.52,
3.68,
3.76,
3.84,
4.00,
4.16,
4.40,
4.56,
4.72,
4.88,
4.96,
5.04,
5.12,
5.20,
5.28,
5.36,
5.44,
5.52,
5.44,
5.36,
5.28,
5.20,
5.04,
4.96,
4.88,
4.80,
4.72,
4.64,
4.56,
4.48,
4.32,
3.68,
3.28,
2.72,
2.56,
2.40,
2.24,
1.60,
1.20,
1.08,
1.00,
0.76])

freq = np.array([85.20,
90.03,
97.80,
100.80,
108.80,
113.80,
124.80,
130.70,
141.10,
148.20,
153.10,
160.40,
170.00,
180.60,
187.50,
195.10,
206.80,
213.30,
221.70,
237.40,
241.80,
258.00,
277.20,
292.60,
300.70,
321.30,
345.90,
385.20,
413.20,
478.50,
514.14,
564.50,
602.30,
667.80,
732.20,
872.50,
973.20,
1090.00,
1670.00,
4860.00,
5660.00,
6490.00,
7420.00,
8600.00,
9290.00,
9910.00,
10620.00,
11090.00,
11670.00,
12130.00,
12900.00,
13750.00,
18000.00,
21960.00,
26330.00,
28150.00,
30860.00,
32400.00,
42510.00,
52520.00,
56300.00,
58600.00,
69800.00])

x = freq
y = (v_out/v_in)**2
yerr = y*0.10
 
params = lmfit.Parameters()
  
params.add('A', value = 320.8, vary = True)
params.add('B', value = 18277.3994, vary = True)
params.add('C', value = 5.5/v_in, vary = True)
params.add('D', value = 10.0, vary = True)
  
result = lmfit.minimize(fit_freq_fit, params, args = (x, y, yerr))
  
fit_values  = y + result.residual
  
lmfit.report_errors(result.params)
 
x_plot = np.linspace(66.2,70000.0,10000)
y_plot = fit_freq_model(result.params,x_plot)

gain_x = x_plot
gain_y = y_plot

interval = x_plot[1]-x_plot[0]
area = np.sum(y_plot*interval)



### fit johnson noise


def fit_johnson_model(params, x, gain_x, gain_y):
    A = params['Af'].value
    B = params['Bf'].value
    C = params['Cf'].value
    new_R = np.ones_like(x)
    for i in range(len(x)):
        new_gain_y = gain_y/(1+(2*np.pi*gain_x*x[i]*C)**2)
        new_R[i] = np.sum(new_gain_y*interval)/area
    #print "x is " + str(x)
    #print "new_R is " + str(new_R)
    output = A*(x*new_R)**B
    #print x
    return output
'''
define how to compare data to the function
'''
def fit_johnson_fit(params , x, gain_x, gain_y, data, err):
    model = fit_johnson_model(params, x, gain_x, gain_y)
    return (model - data)/err

bg_noise = 0.004263

v_rms = 0.001*np.array([4.543, 5.205, 5.471, 6.950, 8.737, 12.111, 23.22, 33.08, 46.37, 50.2, 57.54, 58.96, 59.59])

res = np.array([
47.19,
149.99,
200.9,
511,
1003.5,
2204,
10012,
20040,
68320,
101750, 
223140,
476300,
1014300])

#res = res[:-1]
#v_rms = v_rms[:-1]

x = res
y = v_rms**2 - bg_noise**2
yerr = (v_rms**2)*0.04

params = lmfit.Parameters()
 
params.add('Af', value = 6.3623e-08, vary = True)
params.add('Bf', value = 1.0, vary = False)
params.add('Cf', value = 1.0e-11, vary = True)
 
result = lmfit.minimize(fit_johnson_fit, params, args = (x, gain_x, gain_y, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),1000)

print "k is " + str(result.params['Af']/(3.74658348542e+12*4*297))

print result.redchi

figure = pyplot.figure(0)

#print x
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot, gain_x, gain_y),linewidth = 3.0)

pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.show()
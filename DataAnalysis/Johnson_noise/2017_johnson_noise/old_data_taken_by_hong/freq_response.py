from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit


def fit_model(params, x):
    A = params['A'].value ### low pass frequency
    B = params['B'].value ### high pass frequency
    C = params['C'].value ### gain
    D = params['D'].value ### offset
    f_l = x/A
    f_h = x/B
    output = C*(f_h**2/(1+(f_h**2)))*(1/(1+f_l**2)) + D
    return output
'''
define how to compare data to the function
'''
def fit_fit(params , x, data, err):
    model = fit_model(params, x)
    return (model - data)#/err

v_in = 0.0000396

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
  
params.add('A', value = 305, vary = True)
params.add('B', value = 14808, vary = True)
params.add('C', value = 4.8400e13, vary = True)
params.add('D', value = 100, vary = True)
 
result = lmfit.minimize(fit_fit, params, args = (x, y, yerr))
  
fit_values  = y + result.residual
  
lmfit.report_errors(result.params)
 
x_plot = np.linspace(x.min(),x.max(),2000)

figure = pyplot.figure(0)
  
pyplot.plot(x,y, 'o-')
pyplot.plot(x_plot,fit_model(result.params,x_plot),linewidth = 3.0)

pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

pyplot.show()
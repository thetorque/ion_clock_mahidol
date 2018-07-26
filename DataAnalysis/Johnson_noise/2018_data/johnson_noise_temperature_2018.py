from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
from scipy.interpolate import interp1d
from NTC_CURVE_2018 import T_from_R

def fit_johnson_model(params, temp, res, gain_x, gain_y):
    A = params['Af'].value
    B = params['T0'].value
    C = params['Cf'].value
    new_R = np.ones_like(temp)
    for i in range(len(temp)):
        new_gain_y = gain_y/(1+(2*np.pi*gain_x*res[i]*C)**2)
        new_R[i] = np.sum(new_gain_y*interval)/area
    #print "x is " + str(x)
    #print "new_R is " + str(new_R)
    output = A*(res*new_R*(temp-B))
    #print x
    return output
'''
define how to compare data to the function
'''
def fit_johnson_fit(params , temp, res, gain_x, gain_y, data, err):
    model = fit_johnson_model(params , temp, res, gain_x, gain_y)
    return (model - data)#/err

def fit_linear_model(params, x):
    A = params['Af'].value
    B = params['T0'].value
    output = A*(x-B)
    return output
'''
define how to compare data to the function
'''
def fit_linear_fit(params , x, data, err):
    model = fit_linear_model(params , x)
    return (model - data)#/err


v_in = 0.001690

v_out = np.array([0.2659,
0.3902,
0.5251,
0.6731,
0.821,
0.9685,
1.1122,
2.3416,
3.1409,
3.616,
3.9085,
4.0965,
4.2222,
4.309,
4.37,
4.415,
4.537,
4.5126,
4.4509,
4.3707,
4.277,
4.1718,
4.0601,
3.945,
3.825,
3.226,
2.895,
2.693,
2.252,
1.8181,
1.536,
1.349,
1.1534,
0.99,
0.855,
0.742,
0.568,
0.4438,
0.355,
0.2895,
0.1486,
0.074])

freq = np.array([40.0,
50,
60,
70,
80,
90,
100,
200,
300,
400,
500,
600,
700,
800,
900,
1000,
2000,
3000,
4000,
5000,
6000,
7000,
8000,
9000,
10000,
15000,
18000,
20000,
25000,
31000,
36000,
40000,
45000,
50000,
55000,
60000,
70000,
80000,
90000,
100000,
140000,
200000])

x = freq
y = (v_out/v_in)**2
v_out_err = np.array([0.0003,
0.0003,
0.0003,
0.0002,
0.0002,
0.0005,
0.001,
0.002,
0.003,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.001,
0.0005,
0.0005,
0.0005,
0.0005,
0.0005,
0.0005,
0.0005,
0.001])

yerr = 2*v_out_err*y

print np.sqrt(y)

# params = lmfit.Parameters()
  
# params.add('A', value = 320.8, vary = True)
# params.add('B', value = 18277.3994, vary = True)
# params.add('C', value = 5.5/v_in, vary = True)
# params.add('D', value = 10.0, vary = False)
  
# result = lmfit.minimize(fit_freq_fit, params, args = (x, y, yerr))
  
# fit_values  = y + result.residual
  
# lmfit.report_errors(result.params)

f2 = interp1d(x,y, kind = 'cubic')
 
x_plot = np.linspace(freq.min(),freq.max(),10000)
y_plot = f2(x_plot)
#y_plot = fit_freq_model(result.params,x_plot)

gain_x = x_plot
gain_y = y_plot

interval = x_plot[1]-x_plot[0]
area = np.sum(y_plot*interval)

####


bg_noise = 0.00149


### data set 2 taken 7/20/2018 1:50PM

v_rms = 0.001*np.array([2.608, 2.736, 2.924, 3.126, 3.655, 3.801, 4.109, 4.584, 5.034, 5.491, 5.915, 6.74, 7.853, 9.2,  10.650, 10.386, 7.237])#, 10.541])#, 10.671])#, 9.2, 10.5])
#t_c = np.array([91.3, 87.0, 80.0, 74.5, 62.7, 59.8, 54.8, 47.2, 41.7, 36.1, 31.7, 24.7, 16.0, 7.4, 1.5, 0.8, 0.5, 1.3])#, 0.8,0.6])#, 7.4, 0.5])

res = np.array([1750.0, 2000.0, 2500.0, 3000.0, 4500.0, 5000.0, 6000.0, 8000.0, 10000.0, 12500.0, 15000.0, 20200.0, 30000.0, 45000.0,  62700.0, 56850.0, 23400.0])

res = res*10000000.0/(res+10000000.0)
t_c = T_from_R(res/2.0)
#print t_c


y = v_rms**2 - bg_noise**2

y = y*1e9

x = t_c

yerr = 0.01*y


# params = lmfit.Parameters()
 
# params.add('Af', value = area*1.3806e-23*4*1e9, vary = True)
# params.add('T0', value = 269.15, vary = True)
# params.add('Cf', value = 4.1435e-11, vary = False)
 
# result = lmfit.minimize(fit_johnson_fit, params, args = (x, res, gain_x, gain_y, y, res))
 
# fit_values  = y + result.residual
 
# lmfit.report_errors(result.params)

# print result.redchi

# C_fitted = result.params['Cf'].value
C_fitted = 4.1e-11

new_res = np.ones_like(res)
for i in range(len(res)):
    new_gain_y = gain_y/(1+(2*np.pi*gain_x*res[i]*C_fitted)**2)
    new_res[i] = np.sum(new_gain_y*interval)/area

new_res = new_res*res

y = y/new_res


yerr = 0.02*y

params = lmfit.Parameters()
 
params.add('Af', value = 0.00754036, vary = True)
params.add('T0', value = -262, vary = True)
 
result = lmfit.minimize(fit_linear_fit, params, args = (x, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

print result.redchi

x_plot = np.linspace(-300,x.max(),1000)


figure = pyplot.figure(0)

#print x

pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_linear_model(result.params,x_plot),linewidth = 2.0)


#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   
pyplot.xlabel('T (degrees Celcius)')
pyplot.ylabel('$V^2/R$ (x $10^{-15}$ V$^2$/$\Omega$)')
pyplot.ylim([0,3.0])

#pyplot.ylim([0.0,3.0])
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9]) 

pyplot.show()
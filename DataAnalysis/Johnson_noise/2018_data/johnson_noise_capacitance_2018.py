from __future__ import division
#import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit
from scipy.interpolate import interp1d

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

bg_noise = 0.00149

v_rms = 0.001*np.array([1.53,
1.57,
1.65,
1.824,
2.14,
2.721,
3.628,
4.98,
7.06,
10.02,
13.7,
17.8,
21.1,
22.9])

## with BNC measured C = 90 pF added 1m of BNC ##
v_rms_2 = 0.001*np.array([1.528,
1.560,
1.659,
1.836,
2.133,
2.710,
3.612,
4.950,
6.830,
9.065,
11.3,
13.00,
13.800,
14.092])

res = np.array([47.0,
100,
220,
470,
1000,
2200,
4700,
10000,
22000,
47000,
100000,
220000,
470000,
1000000])

res = res*10000000.0/(res+10000000.0)

#res = res[:-1]
#v_rms = v_rms[:-1]

x = res
y = v_rms**2 - bg_noise**2
yerr = 0.001*np.array([0.008,
0.005,
0.005,
0.003,
0.01,
0.01,
0.02,
0.02,
0.03,
0.03,
0.05,
0.1,
0.1,
0.1]) 
yerr = yerr + 0.001*0.008*np.ones_like(yerr)

yerr = 2*yerr*v_rms

y2 = v_rms_2**2 - bg_noise**2

params = lmfit.Parameters()
 
params.add('Af', value = 2.2476e-9, vary = True)
params.add('Bf', value = 1.0, vary = False)
params.add('Cf', value = 4.22e-11, vary = True)
 
result = lmfit.minimize(fit_johnson_fit, params, args = (x, gain_x, gain_y, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),1000)

print "k is " + str(result.params['Af']/(area*4*(23.8+273.15)))

print result.redchi

figure = pyplot.figure(0)

#print x
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot, gain_x, gain_y),linewidth = 3.0)


## data set 2 ##

params = lmfit.Parameters()
 
params.add('Af', value = 2.2476e-9, vary = True)
params.add('Bf', value = 1.0, vary = False)
params.add('Cf', value = 4.22e-11, vary = True)
 
result = lmfit.minimize(fit_johnson_fit, params, args = (x, gain_x, gain_y, y2, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),1000)

print "k is " + str(result.params['Af']/(area*4*(23.8+273.15)))

print result.redchi

figure = pyplot.figure(0)

#print x
  
pyplot.errorbar(x,y2,yerr, linestyle='None',markersize = 4.0,fmt='o',color='blue')
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot, gain_x, gain_y),linewidth = 3.0)
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot, gain_x, gain_y),linewidth = 3.0)

pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   
pyplot.xlabel('Resistance ($\Omega$)')
pyplot.ylabel('$V^2$ (mV$^2$)')
pyplot.ylim([0.00000005,0.001])

figure = pyplot.figure(1)
pyplot.plot(gain_x,gain_y/1000000)
pyplot.errorbar(freq,(v_out/v_in)**2.0/1000000,linestyle='None',markersize = 4.0,fmt='o',color='black')
#pyplot.xscale('log')
#pyplot.xlabel('Frequency (Hz)')
pyplot.ylabel('Gain$^2$ ($10^6$)')
#pyplot.ylim([1.4,3.0])
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9]) 

pyplot.show()
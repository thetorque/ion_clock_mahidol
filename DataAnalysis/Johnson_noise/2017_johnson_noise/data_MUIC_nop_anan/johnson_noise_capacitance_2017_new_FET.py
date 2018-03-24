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
    output = C**2*(f_h**2/(1+(f_h**2)))*(1/(1+f_l**2)) + D**2*(f_h**4/(1+(f_h**4)))*(1/(1+f_l**4))
    return output
'''
define how to compare data to the function
'''
def fit_freq_fit(params , x, data, err):
    model = fit_freq_model(params, x)
    return (model - data)#/err

v_in = (0.30125/2.0)*(0.03939/7.076)/np.sqrt(2)

v_out = np.array([
    0.04544,
    0.11818,
    0.20688,
    0.34777,
    0.7500,
    1.1932,
    1.4217,
    1.4785,
    1.5170,
    1.5435,
    1.5258,
    1.4606,
    1.3707,
    1.1870,
    1.0000,
    0.8312,
    0.6883,
    0.5701,
    0.4766,
    0.4033,
    0.3432,
    0.2545,
    0.194,
    0.0988,
    0.059,
    0.023])

freq = np.array([
    30,
    50,
    70,
    100,
    200,
    400,
    700,
    900,
    1200,
    2000,
    4000,
    7000,
    10000,
    15000,
    20000,
    25000,
    30000,
    35000,
    40000,
    45000,
    50000,
    60000,
    70000,
    100000,
    130000,
    200000])

x = freq
y = (v_out/v_in)**2

print np.sqrt(y.max())

yerr = y*0.01+500
 
# params = lmfit.Parameters()
  
# params.add('A', value = 320.8, vary = True)
# params.add('B', value = 18277.3994, vary = True)
# params.add('C', value = 5.5/v_in, vary = True)
# params.add('D', value = 10.0, vary = True)
  
# result = lmfit.minimize(fit_freq_fit, params, args = (x, y, yerr))
  
# fit_values  = y + result.residual
  
# lmfit.report_errors(result.params)
 
x_plot = np.linspace(x.min(),x.max(),10000)
#y_plot = fit_freq_model(result.params,x_plot)

f = interp1d(x,y,kind = 'cubic')
y_plot = f(x_plot)

gain_x = x_plot
gain_y = y_plot

interval = x_plot[1]-x_plot[0]
area = np.sum(y_plot*interval)

print area

figure = pyplot.figure(0)

pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
#pyplot.plot(x_plot,fit_freq_model(result.params,x_plot),linewidth = 3.0)
pyplot.plot(x_plot,y_plot,linewidth = 3.0)

pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   


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
    output = A*(x*new_R)+B
    #print x
    return output
'''
define how to compare data to the function
'''
def fit_johnson_fit(params , x, gain_x, gain_y, data, err):
    model = fit_johnson_model(params, x, gain_x, gain_y)
    return (model - data)/err

bg_noise = 0.00107

v_rms = 0.001*np.array([1.10,
    1.10,
    1.13,
    1.18,
    1.23,
    1.28,
    1.29,
    1.34,
    1.397,
    1.51,
    1.661,
    1.865,
    2.416,
    2.981,
    3.526,
    4.045,
    4.896,
    6.826,
    10.344,
    10.778,
    12.198,
    14.450,
    19.55,
    21.69,
    24.38,
    26.26,
    27.51])

res_raw = np.array([10,
    20,
    47.3,
    98.6,
    150,
    197,
    220,
    270,
    330,
    470,
    671,
    975,
    1965,
    3242,
    4600,
    6580,
    9900,
    19600,
    46000,
    51200,
    67000,
    99000,
    215000,
    304000,
    470000,
    684000,
    991000])


v_rms_shot = 0.001*np.array([
    24.65,
    22.36,
    17.76,
    11.08,
    7.70,
    7.5435,
    4.92,
    3.61,
    2.25,
    1.870,
    1.529,
    1.216])

v_batt = 8.56

res_shot = np.array([
    991000,
    684000,
    304000,
    99000,
    51200,
    46000,
    19600,
    9900,
    3242,
    1965,
    975,
    270])

current = 8.56/res_shot

# res_raw = np.append(res_raw,res_shot/2)
# v_rms = np.append(v_rms,v_rms_shot)
#res = res_raw
res = res_raw*10000000/(res_raw+10000000)

#print res

#res = res[:-1]
#v_rms = v_rms[:-1]

x = res
y = v_rms**2# - bg_noise**2
yerr = (v_rms**2)*0.02

params = lmfit.Parameters()
 
params.add('Af', value = 6.3623e-08, vary = True)
params.add('Bf', value = 1.0, vary = True)
params.add('Cf', value = 1.0e-11, vary = True)
 
result = lmfit.minimize(fit_johnson_fit, params, args = (x, gain_x, gain_y, y, yerr))
 
fit_values  = y + result.residual
 
lmfit.report_errors(result.params)

x_plot = np.linspace(x.min(),x.max(),50000)

print "k is " + str(result.params['Af']/(area*4*293))

print result.redchi

figure = pyplot.figure(1)

#print x
  
pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,fit_johnson_model(result.params,x_plot, gain_x, gain_y),linewidth = 3.0)

pyplot.xscale('log')
pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

### plot shot noise
#pyplot.errorbar(res_shot/2.0,v_rms_shot**2-bg_noise**2,v_rms_shot**2*0.02, linestyle='None',markersize = 4.0,fmt='o',color='blue')

pyplot.show()
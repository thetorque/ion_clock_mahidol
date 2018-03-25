from __future__ import division
import labrad
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit

def allan_model(params, x):
    A = params['A'].value
    B = params['B'].value
    output = A/np.power(x,B)
    #output = A/(x**B)
    return output
'''
define how to compare data to the function
'''
def allan_fit(params , x, data, err):
    model = allan_model(params, x)
    return (model - data)/err


data = np.loadtxt("scope_58.csv", delimiter=",", skiprows=2)
volt = data[:,1]
volt = volt - np.average(volt)
v_fft = np.absolute(np.fft.rfft(volt))

time = data[:,0]

time_step = time[1]-time[0]
print time_step
frequency_array = np.linspace(0.0,1/(2.0*time_step), np.size(volt)/2.0+1)

# print "data points is ", np.size(volt)
# 
# average_volt = np.average(volt)
# print "average volt is ", average_volt
# volt = volt - average_volt
# print volt
# average_rms = np.sqrt(np.average(volt**2.0))
# print "rms volt is ", average_rms
# 
# 
# #volt = np.sin(10000.0*2.0*np.pi*time)
# 
# v_fft = np.absolute(np.fft.rfft(volt))
# print v_fft
# print np.size(v_fft)     
#pyplot.plot(time,volt,'o')
pyplot.plot(frequency_array[1:], v_fft[1:]) ##skip over the first point
#pyplot.plot(v_fft) ##skip over the first point
 
 
##############################################

#pyplot.plot(x_plot,allan_model(params,x_plot),linewidth = 2.0)
   
#pyplot.xscale('log',basex = 10)
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])
     
# ytick = [0.05,0.1,0.2,0.3]
# pyplot.yticks(ytick,ytick)
#xtick = [0,50,100,150,200,250]
#pyplot.xticks(xtick,xtick)
 
pyplot.show()

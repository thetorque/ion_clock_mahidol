from __future__ import division
import numpy as np
from matplotlib import pyplot
import matplotlib
import lmfit



x_plot = np.linspace(0.001,7,1000)
j = np.floor(x_plot)
y_plot = 2*j*(j+1)/x_plot-(2*j+1)

figure = pyplot.figure(0)
  
#pyplot.errorbar(x,y,yerr, linestyle='None',markersize = 4.0,fmt='o',color='black')
pyplot.plot(x_plot,y_plot,linewidth = 2.0)
#pyplot.plot(x_plot,fit_model(params,x_plot),linewidth = 3.0)

#pyplot.xscale('log')
#pyplot.yscale('log',basey = 10,subsy=[2, 3, 4, 5, 6, 7, 8, 9])   

#pyplot.xlabel('$nu$')
#pyplot.ylabel('$T^2$ (s$^2$)')

#pyplot.ylim([0.0,3.5])
#pyplot.xlim([0.0,0.9])

pyplot.show()
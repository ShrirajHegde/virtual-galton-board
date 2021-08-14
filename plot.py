#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from numba import jit


#width of the plot or height of the galton board
width=30

#total number of beads to release at the top
number_of_beads=40000

#=============================================================================================
#array to hold the data where the bead lands
data=[0]*(width+1)  

#setting x axis range accordingly if width is even or odd
lrange=-int(width/2) 
if width%2: #for even
    urange=-lrange+2
else:
    urange=-lrange+1

#array for plotting
x_axis= [i for i in range(lrange,urange)] 
#array for spline plotting
x_spline = xnew = np.linspace(min(x_axis), max(x_axis), 300)

#use numba for seedup
@jit(nopython=True)
def update():
    coordinate=0
    for j_th_level in range(width):
        if random.randint(0,1): #if random output between 0 and 1 gives 1(True)
            coordinate+=1 #increase the coordinate (bead goes to the right)
    return coordinate

#main simulation loop
for i_th_bead in range(1,number_of_beads+1):
    plt.clf() #clear the plot
    coordinate=update()

    """ 
    NOTE:Bead never travels left ,This does not affect result, 
    but shifts the data, this is taken care of while plotting 
    """

    #Count is incremented in the corresponding place where the bead "lands"
    data[coordinate]+=1

    print('bead number =',i_th_bead,end='\r')
    #update plot in intervals of 250 beads
    if i_th_bead%250==0:
        Spline =  make_interp_spline(x_axis, data, k=3)
        y_spline = Spline(x_spline)
        plt.title("Number of 'Virtual Beads'={}".format(i_th_bead))
        plt.bar(x_axis,data,color='black')
        #Hide xtics
        plt.xticks([])
        plt.plot(x_spline,y_spline,color='red')
        plt.pause(0.00001)
        # plt.savefig("frames/{}.png".format(int(i_th_bead)),dpi=200)
        ## uncomment line above to save the individual frames to create animation if needed

print('\n complete,close the window to exit')
plt.bar(x_axis,data,color='black')
plt.plot(x_spline,y_spline,color='red')
plt.show()
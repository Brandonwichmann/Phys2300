import numpy as np
import math as m
import matplotlib.pyplot as plt
"""
Make sure you make this module as modular as you can.
That is add as many functions as you can.
1) Have a main function
2) A function to capture user input, this could be inside your "main" function
3) A function to calculate the projectile motion
4) A function to display the graph

Make sure you use docstring to document your module and all
your functions.

Make sure your python module works in dual-mode: by itself or import to other module
"""
# NOTE: You may need to run: $ pip install matplotlib

# Function to calculate projectile motion
def po(comp, vel, time, accel):  # This is what order each variable goes into this function
    """
    This will find the position of your projectile motion
    Using the equation to find it
    """
    return comp + vel* time + 0.5* accel*(time*time)   # equation to calculate amount
# Function to plot data
def plot_data(x, y, Title):
    """
    param: x is the x component
    param: y is the y component
    param: Title is the name of the line
    """
    return plt.plot(x, y, label= Title )

# "Main" Function
def main():
    pass

gravity = -9.8
x0 = 1.0
vx0 = 70.0         # TODO: capture input

y0 = 0.0
vy0 = 80.0          # TODO: capture input

ax = 0.0
ay = gravity           # connects the constant to the acceleration in the y direction

deltat = 0.1 #how much time passes inbetween each point
t = 0.0  #set the time to be 0

x = []
y = []

interval = 170 

for i in range(interval):  #start the loop
    x.append(po(x0,vx0,t,ax))  # Change the x value
    y.append(po(y0,vy0,t,ay))  #Change the y value
    t = t + deltat  # changes the value of t to the next interval

    if y[i] < 0.0:  #This is what pulls it out of the loop if the projectile has crossed the x plane
        break

plt.xlabel('Horizontal Distance')  #label the x-axis
plt.ylabel('Vertical Distance')  # Label the y-axis
plot_data(x, y, "Travel Path") #stores the values and then labels the projectile path
plt.legend()  # Creates a legend for the graph
plt.show() #plots the values
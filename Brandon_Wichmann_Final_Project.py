import argparse
import numpy as np
import pandas as pd
import sys
from vpython import *

G = -6.674e-11
sun_mass = 1.988e30
c = 2.99792458e8
dt = 6.3e4

def main():

    Data = {}
    inputparameters(Data)
    Schwarchild_radius(Data)
    au_to_m(Data)
    Data['x'] = Data['mx']
    Data['y'] = Data['my']
    force(Data)
    accel(Data)
    vel(Data)
    x_y(Data)
    


    print(Data)

def accel(Data):
    Accelerationx = Data['GFx'] / Data['PM']
    Accelerationy = Data['GFy'] / Data['PM']
    Data['Accelx'] = Accelerationx
    Data['Accely'] = Accelerationy

    return(Data)


def x_y(Data):
    x = Data['x'] + dt * Data['Vel']
    Data['x'] = x

    return(Data)



def au_to_m(Data):
    mx = 1.49597870700e11 * Data['x0']
    my = 1.49597870700e11 * Data['y0']
    Data['mx'] = mx
    Data['my'] = my

    return(Data)



def m_to_au(Data):
    aux = Data['x0']
    auy = Data['xy']
    Data['aux'] = aux
    Data['auy'] = auy

    return(Data)



def vel(Data):
    Vel = Data['V'] + dt * Data['Accel'] 
    Data['Vel'] = Vel

    return(Data)



def force(Data):
    Gravitational_Forcex = ((G * Data['BHM'] * Data['PM']) / Data['x'])
    Gravitational_Forcey = ((G * Data['BHM'] * Data['PM']) / Data['y'])
    Data['GFx'] = Gravitational_Forcex
    Data['GFy'] = Gravitational_Forcey

    return(Data)


def inputparameters(Data):
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--Semi_Major", "-SM", action = "store", dest = "SM", default = 1, help = "This is an inputed value for the semi-major axis")
    parser.add_argument("--Velocity", "-v", action = "store", dest = "Velocity", default = 29.783e6, help = "This is an inputed value for the starting Velocity")
    parser.add_argument("--Hole_mass", "-BHM", action = "store", dest = "hole_Mass", default = 1, help = "This is an inputed value for the Mass of the black hole(solar masses)")
    parser.add_argument("--planet_mass", "-PM", action = "store", dest = "planet_Mass", default = 5.9722e24, help = "This is an inputed value for the Mass of a planet(kg)")
    args = parser.parse_args()
    Data['SM'] = args.SM
    Data['x0'] = args.SM
    Data['y0'] = 0.000001
    Data['V'] = args.Velocity
    Data['BHM'] = args.hole_Mass * sun_mass
    Data['PM'] = args.planet_Mass

    return Data

def Schwarchild_radius(Data):
    black_hole_radius = ((2 * G * Data['BHM']) / c**2)
    Data['BHR'] = black_hole_radius

    return Data


if __name__ == '__main__':

    main()
    exit(0)
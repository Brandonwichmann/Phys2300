from math import sqrt
from numpy import empty, array, arange, copy, float64
from matplotlib import pyplot as plt  
from vpython import *
import argparse

def inputparameters():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--Semi_Major", "-SM", action = "store", dest = "SM", default = 1, help = "This is an inputed value for the semi-major axis(AU)")
    parser.add_argument("--Velocity", "-v", action = "store", dest = "Velocityy", default = 29.783e6, help = "This is an inputed value for the starting Velocity(m / sec)")
    parser.add_argument("--Hole_mass", "-BHM", action = "store", dest = "hole_Mass", default = 1, help = "This is an inputed value for the Mass of the black hole(solar masses)")
    parser.add_argument("--planet_mass", "-PM", action = "store", dest = "planet_Mass", default = 5.9722e24, help = "This is an inputed value for the Mass of a planet(kg)")
    args = parser.parse_args()
    SM= args.SM
    x0 = args.SM * 1.49597870700e11
    y0 = 0.000001
    Vy = args.Velocityy
    Vx = .00001
    BHM= args.hole_Mass * sun_mass
    PM = args.planet_Mass

    return (x0, y0, Vy, Vx, BHM, PM)


def Schwarchild_radius(M):
    black_hole_radius = ((2 * G * M) / c**2)
    BHR = black_hole_radius

    return (BHR)
# Constants
G = 6.6738e-11          # Newton's Gravitational Contant 
M = 1.9891e30           # Mass of the Sun (kg)   
m = 5.9722e24
sun_mass = 2e30           # Earth's mass
year = 31557600         # One year in seconds
week = 7*24*3600        # One week in seconds
day = 24 * 3600
delta = 1000/year
c = 2.99792458e8
# x0 = 1.5210e11
# y0 = 0.0
# vx0 = 0.0
# vy0 = 3e4
a = 0.0
b = year
H = day / 2


def main():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--Semi_Major", "-SM", type = float,action = "store", dest = "SM", default = 8, help = "This is an inputed value for the semi-major axis(AU)")
    parser.add_argument("--Velocity", "-v",type = float, action = "store", dest = "Velocityy", default = 2.32e6, help = "This is an inputed value for the starting Velocity(m / sec). If this velocity is too low it will get caught in a loop when finding the error bars and won't display the animation. Starting value is 30,000 m/s")
    parser.add_argument("--Hole_mass", "-BHM",type = float, action = "store", dest = "hole_Mass", default = 70000, help = "This is an inputed value for the Mass of the black hole(solar masses) starting value is one solar mass. If you change this mass you need to also change the velocity. If it is more increase velocity. If it is less decrease velocity.")
    parser.add_argument("--planet_mass", "-PM",type = float, action = "store", dest = "planet_Mass", default = 5.9722e26, help = "This is an inputed value for the Mass of a planet(kg)")
    parser.add_help


    args = parser.parse_args()
    SM= args.SM
    x0 = args.SM * 1.49597870700e11
    y0 = 0.000001
    Vy = args.Velocityy
    Vx = .00001
    BHM= args.hole_Mass * M
    PM = args.planet_Mass
    BHScale = 5e4   #The Black hole radius is extremely small because of the extreme density of it
    Scale = 1e2   #Have to use a smaller scale to allow for the black hole to scale to the same size
    Time_dilation_scale = 1
    xpoints = []
    ypoints = []
    TD = []
    Planetr = ((3 * PM)/ (4 * 5510)) ** (1/3)  #Finds the radius of the planet using density and mass
    BHR = ((2 * G * BHM) / c**2)   #Use the Schwarchild equation to find the radius of the black hole
    # print(BHR, Planetr)
    # Do the "Big Steps" of size H
    r = array([x0, y0, Vx, Vy], float)
    Black_hole = sphere(pos = vector(0, 0, 0), radius = BHR * Scale, make_trail = True)
    Earth = sphere(pos = vector(r[0], r[1], 0), radius = Planetr * Scale  , make_trail = True )
    for t in arange(a, b, H):
        rate(100)
        xpoints.append(r[0])
        ypoints.append(r[1])
        Time_dilation = ((1 - ((2 * G * BHM) / ((sqrt(r[0]**2 + r[1]**2) - BHR) * c **2)))** (.5) * (1 - ((sqrt(r[2]**2 + r[3]**2)) / c **2))** (.5)) * Time_dilation_scale
        # print(Time_dilation)
        TD.append(Time_dilation)
        # Do the leapfrog step to get things started
        counter = 1   # couter
        step = H
        r1 = copy(r)
        r2 = r1 + 0.5*step*fun(r1, BHM)
        r1 += step*fun(r2, BHM)
        
        R1 = empty([1,4], float)
        R2 = empty([1,4], float)
        R1[0] = r1   #save array in position 1
        
        # print("n value:", counter)
        # print("r1", r1)
        # print(m)
        #
        # return # DEBUG
        Earth.pos = vector(r[0], r[1], 0)
        # Now increase n and extrapolate
        error = 2*H*delta
        # print("t step", t, "error ", error, "Delta*H", delta*H)
        n = 0
        while abs(error) > H*delta:
        # while n < 5:   # TODO: debug
            counter += 1
            step = H/counter   #resetting step
            # Leap frog method
            r1 = copy(r)
            r2 = r1 + 0.5*step*fun(r1 , BHM)
            for i in range (counter):
                r1 += step*fun(r2, BHM)
                r2 += step*fun(r1, BHM)
            # TODO: You need R1 values
            # Calculate extrapolation estimates
            # print(n, r1)
            R2 =   R1  # TODO Use the copy method to copy the np.array
            R1 = empty([counter,4], float)
            R1[0] = r1
            for ncounter in range (1, counter):
                # print("R1[ncounter]:", R1[ncounter - 1],"R2[ncounter-1]", R2[ncounter - 1])
                epsilon = (R1[ncounter-1] - R2[ncounter-1])/((counter/(counter-1))**(2*ncounter) - 1)
                R1[ncounter] = R1[ncounter-1] + epsilon
                error = sqrt(epsilon[0]**2 + epsilon[1]**2)
                # print("epsilon is :", epsilon)
                # print("R1[ncounter]", R1[ncounter])
            
            # print("error is:", error, "Delta ", delta*H)
            n += 1
        # Set r equal to the most accurate estimate
        r = R1[counter-1]
        # print("r is :", r)
        
     

    print(TD)
    # Plot the results
    plt.plot(arange(a, b, H), TD)
    plt.title("Time dilation per second vs. position in orbit in respect to time in simulation")
    # print(xpoints, ypoints)
    plt.show()


# Function fun(r)
def fun(r, M):
    x = r[0]
    y = r[1]
    vx = r[2]
    vy = r[3]
    fx = vx
    fy = vy
    
    fvx = -G*M*x/sqrt(x*x + y*y)**3
    fvy = -G*M*y/sqrt(x*x + y*y)**3
    return array([fx, fy, fvx, fvy], float)




if __name__ == '__main__':

    main()
    exit(0)
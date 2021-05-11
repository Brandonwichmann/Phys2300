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

# Constants
G = 6.6738e-11          # Newton's Gravitational Contant 
M = 1.9891e30           # Mass of the Sun (kg)   
m = 5.9722e24
sun_mass = 2e30           # Earth's mass
year = 31557600         # One year in seconds
week = 7*24*3600        # One week in seconds
delta = 1000/year
# x0 = 1.5210e11
# y0 = 0.0
# vx0 = 0.0
# vy0 = 3e4
a = 0.0
b = year
H = week


def main():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--Semi_Major", "-SM", action = "store", dest = "SM", default = 1, help = "This is an inputed value for the semi-major axis(AU)")
    parser.add_argument("--Velocity", "-v", action = "store", dest = "Velocityy", default = 2.783e4, help = "This is an inputed value for the starting Velocity(m / sec)")
    parser.add_argument("--Hole_mass", "-BHM", action = "store", dest = "hole_Mass", default = 1, help = "This is an inputed value for the Mass of the black hole(solar masses)")
    parser.add_argument("--planet_mass", "-PM", action = "store", dest = "planet_Mass", default = 5.9722e24, help = "This is an inputed value for the Mass of a planet(kg)")
    
    args = parser.parse_args()
    SM= args.SM
    x0 = args.SM * 1.49597870700e11
    y0 = 0.000001
    Vy = args.Velocityy
    Vx = .00001
    BHM= args.hole_Mass * M
    PM = args.planet_Mass
    xpoints = []
    ypoints = []
    # Do the "Big Steps" of size H
    r = array([x0, y0, Vx, Vy], float)
    Sun = sphere(pos = vector(0, 0, 0), radius = 10e10, make_trail = True)
    Earth = sphere(pos = vector(r[0], r[1], 0), radius = 10e9, make_trail = True )
    for t in arange(a, b, H):
        rate(100)
        xpoints.append(r[0])
        ypoints.append(r[1])
        # Do the leapfrog step to get things started
        counter = 1   # couter
        step = H
        r1 = copy(r)
        r2 = r1 + 0.5*step*fun(r1)
        r1 += step*fun(r2)
        
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
        print("t step", t, "error ", error, "Delta*H", delta*H)
        n = 0
        while abs(error) > H*delta:
        # while n < 5:   # TODO: debug
            counter += 1
            step = H/counter   #resetting step
            # Leap frog method
            r1 = copy(r)
            r2 = r1 + 0.5*step*fun(r1)
            for i in range (counter):
                r1 += step*fun(r2)
                r2 += step*fun(r1)
            # TODO: You need R1 values
            # Calculate extrapolation estimates
            # print(n, r1)
            R2 =   R1  # TODO Use the copy method to copy the np.array
            R1 = empty([counter,4], float)
            R1[0] = r1
            for ncounter in range (1, counter):
                print("R1[ncounter]:", R1[ncounter - 1],"R2[ncounter-1]", R2[ncounter - 1])
                epsilon = (R1[ncounter-1] - R2[ncounter-1])/((counter/(counter-1))**(2*ncounter) - 1)
                R1[ncounter] = R1[ncounter-1] + epsilon
                error = sqrt(epsilon[0]**2 + epsilon[1]**2)
                # print("epsilon is :", epsilon)
                # print("R1[ncounter]", R1[ncounter])
            
            print("error is:", error, "Delta ", delta*H)
            n += 1
        # Set r equal to the most accurate estimate
        r = R1[counter-1]
        print("r is :", r)
        
     


    # Plot the results
    # plt.plot(xpoints, ypoints)
    # print(xpoints, ypoints)
    # plt.show()


# Function fun(r)
def fun(r, ):
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
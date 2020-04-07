from graphics import *
import time
import math
import random
import sys
import os
import numpy as np
from mpi4py import MPI


#TODO STATIC FRICTION, MULTIWAY COLLISIONS
WIDTH = 400
HEIGHT = 400
timestep = .03

# *********
# ALTERABLE VARIABLES
RADIUS = 5 #RADIUS OF BALLS
duration = 10 # DURATION OF PROGRAM
num_particles = 12 # NUMBER OF PARTICLES
G_CONST = 1 #Gravitational Constant
co_frict = .1#COEFFECIENT OF FRICTION
# *********

g_acel = 9.8

class Particle:
    rad = 0
    velx = 0
    vely = 0
    cir = 0
    mass = 0
    posx = 0
    posy = 0
    color = 0

    def __init__(self, radius, velocityx, velocityy, posx, posy, color, m):
        self.rad = radius
        self.velx = velocityx
        self.vely = velocityy
       # self.cir = Circle(pt, self.rad)
      #  self.cir.setFill(color)
        self.posx = posx
        self.posy = posy
        self.mass = m
        self.color = color

    def get_Posx(self):
       return self.posx

    def get_Posy(self):
        return self.posy


def get_distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))


def collision(x1, x2, y1, y2, rad1, rad2,sig):
    distance = get_distance(x1,x2,y1,y2)

    if distance <= rad1 + rad2 +sig:
        return True
    else:
        return False


def rotate(velx,vely,angle):
    rotate_vel = [velx*math.cos(angle)-vely*math.sin(angle),
                  velx*math.sin(angle)+vely*math.cos(angle)]
    return rotate_vel


def update_positions(valid_pos, particles, i, j):
    for k in range(num_particles):
        if k != i and k!=j:
            if get_distance(particles[i].velx, particles[k].velx, particles[i].vely, particles[k].vely) < particles[i].rad + particles[k].rad  - .5:

                valid_pos[k] = 0
            elif get_distance(particles[j].velx, particles[k].velx, particles[j].vely, particles[k].vely) < particles[j].rad + particles[k].rad  - .5:
                valid_pos[k] = 0

    return valid_pos


def check_positions(valid_pos):
    for i in range(len(valid_pos)):
        if valid_pos[i] == 0:
            return False

    return True


def find_index(valid_pos):
    for i in range(len(valid_pos)):
        if valid_pos[i] == 0:
            return i

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        if os.path.exists("output.txt"):
            os.remove('output.txt')

   # fh = MPI.File.Open(comm,'output.txt', MPI.MODE_WRONLY|MPI.MODE_CREATE)
    if rank ==0:    
        fh = open('output.txt', 'w')
     
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'white', 'orange', 'brown', 'purple', 'pink', 'teal', 'maroon', 'magenta', 'tan', 'gold', 'grey', 'cyan']
    num_timesteps = duration / timestep
    counter = 0
    particles = []

    #RANK 0 DOES ALL WRITING


    num_timesteps = duration / timestep
    if rank == 0:
        fh.write(str(WIDTH) + '\n')
        fh.write(str(HEIGHT) + '\n')
        j = 0
        future_col = False

        #string = str(num_particles)
        fh.write(str(num_particles)+'\n')
        fh.write(str(num_timesteps)+'\n')
        #fh.Write(str(num_particles)+'\n')
        #fh.Write(str(num_timesteps)+'\n')
        fh.write('\n')
        collision_array = [[] for l in range(num_particles)]
        # print(collision_array, file=orig_stdout)

        for i in range(num_particles):

            x = random.randint(RADIUS, WIDTH - RADIUS)
            y = random.randint(RADIUS, HEIGHT - RADIUS)
            rad = RADIUS
            k = 0

            while (k < len(particles)):
                if get_distance(particles[k].get_Posx(), x, particles[k].get_Posy(), y) <= particles[k].rad + rad:
                    x = random.randint(RADIUS, WIDTH - RADIUS)
                    y = random.randint(RADIUS, HEIGHT - RADIUS)
                    k = 0
                else:
                    k += 1
           # print(j, len(colors))
            particles.append(Particle(RADIUS, random.randint(-10, 10), random.randint(-10, 10),
                                      x, y,
                                      colors[j],
                                      1))

            while particles[i].velx == 0 and particles[i].vely == 0:
                particles[i].velx = random.randint(-10, 10)

                particles[i].vely = random.randint(-10, 10)

            fh.write(str(particles[i].rad) + " " + str(particles[i].get_Posx()) + " " + str(particles[i].get_Posy()) + " " + colors[j] + '\n')
            j += 1

            if j == len(colors):
                j = 0

            # radius, posx, posy, color, mass


        fh.write('\n')
    # END OF INITIALIZING STUFF

    blocksize = num_particles//size
    startInd= rank*blocksize

    for j in range(int(num_timesteps)):


        particles = comm.bcast(particles,root=0)

        sub_particles = [0] * blocksize
        tmp = startInd

        for i in range(blocksize):
            sub_particles[i] = particles[tmp]
            tmp += 1 #Index variable used above

        for i in range(blocksize):
            y1 = sub_particles[i].get_Posy()
            x1 = sub_particles[i].get_Posx()
            if x1 >= WIDTH - sub_particles[i].rad:
                if sub_particles[i].velx > 0:
                    sub_particles[i].velx *= -1

            if x1 <= sub_particles[i].rad:
                if sub_particles[i].velx < 0:
                    sub_particles[i].velx *= -1

            if y1 >= HEIGHT - sub_particles[i].rad:
                if sub_particles[i].vely < 0:
                    sub_particles[i].vely *= -1

            if y1 <= sub_particles[i].rad:
                if sub_particles[i].vely > 0:
                    sub_particles[i].vely *= -1


            vel1 = math.sqrt((sub_particles[i].velx * sub_particles[i].velx) + (sub_particles[i].vely * sub_particles[i].vely))

            if sub_particles[i].velx < 0:  # apparently don't need for y since we use it to find the angle?
                dir1x = -1
            elif sub_particles[i].velx > 0:
                dir1x = 1
            else:
                dir1x = 0

            new_vel = vel1 - co_frict * g_acel * (timestep)

            if new_vel <= 0:
                sub_particles[i].velx = 0
                sub_particles[i].vely = 0
            else:
                ang1 = math.asin(sub_particles[i].vely / vel1)
                sub_particles[i].velx = math.cos(ang1) * new_vel * dir1x
                sub_particles[i].vely = math.sin(ang1) * new_vel

            #End Of Wall Collision and Friction
            """ #TO DO COLLISION STUFF HERE
            curInd = startInd
            for k in range(num_particles):
                if k == curInd and k < startInd+blocksize:
                    curInd+=1
                    continue
                else:
                    test= 0
            """

            sub_particles[i].posx += sub_particles[i].velx
            sub_particles[i].posy += -(sub_particles[i].vely)


        #LEFTOVERS DONE ON ROOT
        if rank == 0:
            leftoverInd = blocksize * size
            for i in range(leftoverInd, num_particles):
                y1 = particles[i].get_Posy()
                x1 = particles[i].get_Posx()
                if x1 >= WIDTH - particles[i].rad:
                    if particles[i].velx > 0:
                        particles[i].velx *= -1

                if x1 <= particles[i].rad:
                    if particles[i].velx < 0:
                        particles[i].velx *= -1

                if y1 >= HEIGHT - particles[i].rad:
                    if particles[i].vely < 0:
                        particles[i].vely *= -1

                if y1 <= particles[i].rad:
                    if particles[i].vely > 0:
                        particles[i].vely *= -1

                vel1 = math.sqrt((particles[i].velx * particles[i].velx) + (particles[i].vely * particles[i].vely))

                if particles[i].velx < 0:  # apparently don't need for y since we use it to find the angle?
                    dir1x = -1
                elif particles[i].velx > 0:
                    dir1x = 1
                else:
                    dir1x = 0

                new_vel = vel1 - co_frict * g_acel * (timestep)

                if new_vel <= 0:
                    particles[i].velx = 0
                    particles[i].vely = 0
                else:
                    ang1 = math.asin(particles[i].vely / vel1)
                    particles[i].velx = math.cos(ang1) * new_vel * dir1x
                    particles[i].vely = math.sin(ang1) * new_vel


                """ 
                #TO DO COLLISION STUFF HERE
                curInd = startInd
                for k in range(num_particles):
                    if k == curInd and k < startInd + blocksize:
                        curInd += 1
                        continue
                """


                particles[i].posx += particles[i].velx
                particles[i].posy += -(particles[i].vely)








        new_particles= comm.gather(sub_particles,root=0)



        if rank == 0:
            rowInd = 0
            colInd = 0
            leftoverInd = blocksize*size
            for i in range(blocksize*size):
               # print(i)
                particles[i] = new_particles[rowInd][colInd]
                colInd +=1
                if colInd >= blocksize:
                    colInd = 0
                    rowInd += 1
              #  print(particles[i].velx)
                fh.write(str(particles[i].posx) + " " + str(particles[i].posy) + '\n')

            for i in range(leftoverInd,num_particles):
                fh.write(str(particles[i].posx) + " " + str(particles[i].posy) + '\n')

        #comm.Barrier()
        """
        blocksize=comm.bcast(blocksize,root=0)
        print(blocksize)
        subarray = np.empty(blocksize,dtype='i')
        """


     # comm.scatter(particles, root= 0)


    if rank == 0:
        fh.close()


main()








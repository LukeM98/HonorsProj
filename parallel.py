from graphics import *
import time
import math
import random
import sys
import os
import copy
import numpy as np
from mpi4py import MPI

# COLLISION WORKS FOR EVENLY DISTRIBUTED  BLOCKSIZES

#TODO STATIC FRICTION, MULTIWAY COLLISIONS

timestep = .03
timestep_rat = 1

# *********
# ALTERABLE VARIABLES
WIDTH = 500  #WIDTH AND HEIGHT PF DISPLAYING WINDOW, THESE TWO MUST BE
HEIGHT = 500 # BIG ENOUGH TO FIT ALL THE BALLS OR ERROR WILL OCCUR
RADIUS = 10 #RADIUS OF BALLS
duration = 20 # DURATION OF PROGRAM
num_particles = 4 # NUMBER OF PARTICLES
G_CONST = 1 #Gravitational Constant
co_frict = 0#COEFFECIENT OF FRICTION
# *********

g_acel = 9.8
#make timestep relative to highest velocity. Multiple all velocoties by this new timestep.
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

    def vel(self):
        return math.sqrt((self.velx * self.velx) + (self.vely * self.vely))





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

#ERROR OF BALLS SLOWING SIG WHEN GETTING HIT W OTHER BALLS IN THeIR BLOCK
def main():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    global  timestep
    if rank == 0:
        if os.path.exists("output.txt"):
            os.remove('output.txt')

    if rank ==0:
        fh = open('output.txt', 'w')
     
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'white', 'orange', 'brown', 'purple', 'pink', 'teal', 'maroon', 'magenta', 'tan', 'gold', 'grey', 'cyan']
    num_timesteps = duration / timestep
    counter = 0
    particles = []

    #RANK 0 DOES ALL WRITING


    num_timesteps = duration / .03

    if rank == 0:
        fh.write(str(WIDTH) + '\n')
        fh.write(str(HEIGHT) + '\n')
        j = 0


        fh.write(str(num_particles)+'\n')
        fh.write(str(num_timesteps)+'\n')
        fh.write('\n')

        # for i in range(num_particles):
        #
        #     x = random.randint(RADIUS, WIDTH - RADIUS)
        #     y = random.randint(RADIUS, HEIGHT - RADIUS)
        #     rad = RADIUS
        #     k = 0
        #
        #     while (k < len(particles)):
        #         if get_distance(particles[k].get_Posx(), x, particles[k].get_Posy(), y) <= particles[k].rad + rad:
        #             x = random.randint(RADIUS, WIDTH - RADIUS)
        #             y = random.randint(RADIUS, HEIGHT - RADIUS)
        #             k = 0
        #         else:
        #             k += 1
        #    # print(j, len(colors))
        #     particles.append(Particle(RADIUS, random.randint(-10, 10), random.randint(-10, 10),
        #                               x, y,
        #                               colors[j],
        #                               1))
        #    # if j == 0:
        #     #    particles[0].velx = 0;
        #      #   particles[0].vely = 0;
        #
        #     while particles[i].velx == 0 and particles[i].vely == 0:
        #         particles[i].velx = random.randint(-10, 10)
        #
        #         particles[i].vely = random.randint(-10, 10)
        #
        #     fh.write(str(particles[i].rad) + " " + str(particles[i].get_Posx()) + " " + str(particles[i].get_Posy()) + " " + colors[j] + '\n')
        #     j += 1
        #
        #     if j == len(colors):
        #         j = 0

            # radius, posx, posy, color, mass



        particles.append(Particle(RADIUS, 0, 0,
                                 350, 363,
                                 colors[0],
                                 1))




        particles.append(Particle(RADIUS, 0, 0,
                                 250, 450,
                                 colors[1],
                                 1))

        particles.append(Particle(100, 0, 0,
                                  110, 120,
                                  colors[2],
                                  100000))


        particles.append(Particle(RADIUS, 0, 0,
                                 300, 250,
                                 colors[3],
                                 1))
        fh.write(str(particles[0].rad) + " " + str(particles[0].get_Posx()) + " " + str(particles[0].get_Posy()) + " " +
                 colors[0] + '\n')
        fh.write(str(particles[1].rad) + " " + str(particles[1].get_Posx()) + " " + str(particles[1].get_Posy()) + " " +
                 colors[1] + '\n')
        fh.write(str(particles[2].rad) + " " + str(particles[2].get_Posx()) + " " + str(particles[2].get_Posy()) + " " +
                  colors[2] + '\n')
        fh.write(str(particles[3].rad) + " " + str(particles[3].get_Posx()) + " " + str(particles[3].get_Posy()) + " " +
                 colors[3] + '\n')

        fh.write('\n')
    # END OF INITIALIZING STUFF

    blocksize = num_particles//size
    startInd= rank*blocksize

    for j in range(int(num_timesteps)):


        particles = comm.bcast(particles,root=0)

        sub_particles = [0] * blocksize
        tmp = startInd
        max_vel = 0
        for i in range(blocksize):
            sub_particles[i] = copy.deepcopy(particles[tmp])
            if sub_particles[i].vel() > max_vel:
                max_vel = sub_particles[i].vel()
            tmp += 1 #Index variable used above

        # max_vels = comm.gather(max_vel, root=0)
        # global timestep_rat
        # if rank == 0:
        #     maximum = max(max_vels)
        #   #  print(maximum)
        #     if maximum > 10:
        #
        #         timestep_rat= 10 / maximum
        #        # print(round(timestep *timestep_rat,2))
        #
        # timestep_rat = comm.bcast(timestep_rat,root=0)

       # print("RANK = ", rank, timestep_rat)

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





            vel1 = sub_particles[i].vel()

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

            for k in range(num_particles):
                if k == startInd + i:
                    continue
               # elif i > k and i >= startInd and i <= (startInd+blocksize-1):
                #    continue
                else:
                    x1 = sub_particles[i].get_Posx()
                    y1 = sub_particles[i].get_Posy()
                    x2 = particles[k].get_Posx()
                    y2 = particles[k].get_Posy()

                    if collision(x1, x2, y1, y2, sub_particles[i].rad, particles[k].rad,1):
                        xveldif = sub_particles[i].velx - particles[k].velx
                        yveldif = sub_particles[i].vely - particles[k].vely

                        xdistance = x2 - x1
                        ydistance = y2 - y1
                        if xveldif * xdistance + yveldif * (-ydistance) >= 0:
                            if (sub_particles[i].vely == 0 and particles[k].vely == 0):
                                mass1 = sub_particles[i].mass
                                mass2 = particles[k].mass
                                vel1x = sub_particles[i].velx * (mass1 - mass2) / (mass1 + mass2) + particles[
                                    k].velx * 2 * mass2 / (mass1 + mass2)
                                vel2x = particles[k].velx * (mass2 - mass1) / (mass1 + mass2) + sub_particles[
                                    i].velx * 2 * mass2 / (mass1 + mass2)
                                sub_particles[i].velx = vel1x
                                particles[k].velx = vel2x
                                sub_particles[i].vely = 0
                                particles[k].vely = 0
                            else:
                                angle = math.atan2(ydistance, xdistance)  # gets angle between the two particles
                                mass1 = sub_particles[i].mass
                                mass2 = particles[k].mass

                                u1 = rotate(sub_particles[i].velx, sub_particles[i].vely, angle)
                                u2 = rotate(particles[k].velx, particles[k].vely, angle)

                                vel1x = u1[0] * (mass1 - mass2) / (mass1 + mass2) + u2[0] * 2 * mass2 / (
                                            mass1 + mass2)
                                vel2x = u2[0] * (mass2 - mass1) / (mass1 + mass2) + u1[0] * 2 * mass1 / (
                                            mass1 + mass2)
                                vel1y = u1[1]
                                vel2y = u2[1]

                                vFinal = rotate(vel1x, vel1y, -angle)
                                vFinal2 = rotate(vel2x, vel2y, -angle)

                                sub_particles[i].velx = vFinal[0]
                                sub_particles[i].vely = vFinal[1]

                                particles[k].velx = vFinal2[0]
                                particles[k].vely = vFinal2[1]
                                print("COLOR ", particles[k].color, "AFTER COLLISION ", particles[k].vel())


                #GRAVITY STARTS HERE
                c_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                x_dist = math.sqrt(c_sq - ((y1 - y2) * (y1 - y2)))
                y_dist = math.sqrt(c_sq - ((x1 - x2) * (x1 - x2)))

                distance = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
                force_grav = (G_CONST * sub_particles[i].mass * particles[k].mass) / (distance * distance)

                p1_acel = force_grav / sub_particles[i].mass
                p2_acel = force_grav / particles[k].mass

                p1_acelx = 0
                p2_acely = 0
                p1_acely = 0
                p2_acelx = 0

                if x1 > x2 and y1 < y2:  # REPEAT THIS FOR OTHER 3 SCENARIOS                    #p1_acel = - p1_acel

                    deg1 = math.acos(y_dist / distance)
                    deg2 = math.acos(x_dist / distance)

                    p1_acelx = (math.sin(deg1)) * p1_acel
                    p1_acely = (math.cos(deg1)) * p1_acel

                    p2_acelx = (math.cos(deg2)) * p2_acel
                    p2_acely = (math.sin(deg2)) * p2_acel

                    p1_acelx = -p1_acelx
                    p1_acely = -p1_acely

                elif x1 < x2 and y1 < y2:

                    # p2_acel = -p2_acel

                    deg1 = math.acos(y_dist / distance)
                    deg2 = math.acos(x_dist / distance)

                    p1_acelx = (math.sin(deg1)) * p1_acel
                    p1_acely = (math.cos(deg1)) * p1_acel

                    p2_acelx = (math.cos(deg2)) * p2_acel
                    p2_acely = (math.sin(deg2)) * p2_acel

                    p2_acelx = -p2_acelx
                    p1_acely = -p1_acely
                # print("here2",file=orig_stdout)
                elif x1 > x2 and y1 > y2:
                    deg1 = math.asin(y_dist / distance)
                    deg2 = math.asin(x_dist / distance)

                    p1_acely = (math.sin(deg1)) * p1_acel
                    p1_acelx = (math.cos(deg1)) * p1_acel

                    p2_acely = (math.cos(deg2)) * p2_acel
                    p2_acelx = (math.sin(deg2)) * p2_acel
                    # print("here", file=orig_stdout)

                    p2_acely = -p2_acely
                    p1_acelx = - p1_acelx

                elif x1 < x2 and y1 > y2:
                    deg1 = math.asin(y_dist / distance)
                    deg2 = math.asin(x_dist / distance)

                    p1_acely = (math.sin(deg1)) * p1_acel
                    p1_acelx = (math.cos(deg1)) * p1_acel

                    p2_acely = (math.cos(deg2)) * p2_acel
                    p2_acelx = (math.sin(deg2)) * p2_acel

                    p2_acelx = -p2_acelx
                    p2_acely = -p2_acely
                elif x1 == x2 and y1 > y2:
                    p1_acelx = 0
                    p2_acelx = 0
                    p2_acely = -p2_acel
                    p1_acely = p1_acel
                elif x1 == x2 and y1 < y2:
                    p1_acelx = 0
                    p2_acelx = 0
                    p2_acely = p2_acel
                    p1_acely = -p1_acel
                elif x1 > x2 and y1 == y2:
                    p1_acelx = -p1_acel
                    p2_acelx = p2_acel
                    p1_acely = 0
                    p2_acely = 0
                elif x1 < x2 and y1 == y2:
                    p1_acelx = p1_acel
                    p2_acelx = -p2_acel
                    p1_acely = 0
                    p2_acely = 0

                sub_particles[i].velx = sub_particles[i].velx + (p1_acelx * timestep)
                #particles[k].velx = particles[k].velx + (p2_acelx * timestep)

                sub_particles[i].vely = sub_particles[i].vely + (p1_acely * timestep)
                #particles[k].vely = particles[k].vely + (p2_acely * timestep)
                #GRAVITY ENDS HERE
                """ #TO DO COLLISION STUFF HERE
            curInd = startInd
            for k in range(num_particles):
                if k == curInd and k < startInd+blocksize:
                    curInd+=1
                    continue
                else:
                    test= 0
            """
            future_collisionx = []
            future_collisiony = []
            valid_pos = [1] * blocksize


            for l in range(num_particles):

                if l != startInd + i:

                # if valid_pos[i] == 0 and valid_pos[j] == 0:
                # print(particles[i].velx, particles[i].vely, particles[j].velx, particles[j].vely,file=orig_stdout)
                    y2 = particles[l].get_Posy()
                    x2 = particles[l].get_Posx()
                    if collision(x2 + particles[l].velx, x1 + sub_particles[i].velx, y2 + (-particles[l].vely),
                                 y1 + (-sub_particles[i].vely), particles[l].rad, sub_particles[i].rad, 1) and (
                            sub_particles[i].velx != 0 or sub_particles[i].vely != 0 or particles[l].velx != 0 or
                            particles[l].vely != 0):
                        #print("FUTURE COLLISION BETWEEN ", particles[l].color, sub_particles[i].color)
                        # IN HERE ADJUST THE TWO BALLS AND CHECK THEM WITH EVERY OTHER BALL. IF THERE IS NO OVERLAP, THEN IT IS IN VALID SPOT.
                        # IF THERE IS OVERLAP WITH OTHER BALLS, ADJUST BALL THAT IS NEWLY IN INVALID SPOT

                        future_collisionx.append(sub_particles[
                                                        i].velx)  # puts velocity in that partciles velocity array, used to determine old velocity of particle after its collision
                        future_collisiony.append(sub_particles[i].vely)

                        # if j >= startInd and j <= startInd + blocksize:
                        #     future_collisionx[j].append(particles[j].velx)
                        #     future_collisiony[j].append(particles[j].vely)
                        #
                        #
                        sigma = 0
                        iteration = 0  # prevents infinite loops

                        # THIS, FOR MOST PART CHECKS FUTURE DETECTION, RARE MULTIWAY COLLISIONS WILL RESULT IN SOME OVERLAPPING
                        while (get_distance(x2 + particles[l].velx, x1 + sub_particles[i].velx, y2 + (-particles[l].vely),
                                            y1 + (-sub_particles[i].vely)) < (
                                       sub_particles[i].rad + particles[l].rad)) and (iteration < 10):

                            iteration += 1

                            overlap = (sub_particles[i].rad + particles[l].rad) - get_distance(x1 + sub_particles[i].velx,
                                                                                           x2 + particles[l].velx,
                                                                                           y1 + (-sub_particles[i].vely),
                                                                                           y2 + (-particles[l].vely))
                            vel1 = math.sqrt(
                                (sub_particles[i].velx * sub_particles[i].velx) + (sub_particles[i].vely * sub_particles[i].vely))

                            vel2 = math.sqrt((particles[l].velx * particles[l].velx) + (particles[l].vely * particles[l].vely))

                            totalvel = vel1 + vel2

                            if (totalvel != 0):
                                vel1_rat = vel1 / totalvel
                                vel2_rat = vel2 / totalvel
                            else:
                                vel1_rat = 0
                                vel2_rat = 0


                            if sub_particles[i].velx < 0:  # apparently don't need for y since we use it to find the angle?
                                dir1x = -1
                            elif sub_particles[i].velx > 0:
                                dir1x = 1
                            else:
                                dir1x = 0

                            if particles[l].velx < 0:
                                dir2x = -1
                            elif particles[l].velx > 0:
                                dir2x = 1
                            else:
                                dir2x = 0
                            #
                            vel1_ov = vel1 - (vel1_rat * overlap)
                            vel2_ov = vel2 - (vel2_rat * overlap)

                            # TODO: The other scenarios in this conditional (including vely=0 and velx=0).
                            # TODO: ISSUE WHERE NO COLLISION DETECTED IF BALL IS GOING SO FAST THAT IS SKIPS OVER THE OTHER BALL
                            # NEW IDEA: FIND COLLISION WITH SMALLEST TIME STEP, MAKE THAT THE NEW TIME STEP,
                            if (vel1 != 0):
                                ang1 = math.asin(sub_particles[i].vely / vel1)
                                sub_particles[i].velx = dir1x * vel1_ov * math.cos(ang1)
                                sub_particles[i].vely = vel1_ov * math.sin(ang1)

                            if (vel2 != 0):
                                ang2 = math.asin(particles[l].vely / vel2)
                                particles[l].velx = dir2x * vel2_ov * math.cos(ang2)

                                particles[l].vely = vel2_ov * math.sin(ang2)

                           # print("MEMORY OF INDEX PARTICLE 2", hex(id(particles[2])), "MEMORY OF SUB_PARTICLE AT 2 ", hex(id(sub_particles[2])), "\n\n")
                            # iteration += 1

                            # print("FUTURE COLLISION BETWEEN ", particles[i].color, particles[j].color,
                            #       "CURRENT X VELOCITY: ",
                            #       particles[j].velx, particles[i].velx,
                            #       "CURRENT Y VELOCITY", particles[i].vely, particles[j].vely, "FUTURE DISTANCE: ",
                            #       get_distance(x2 + particles[j].velx, x1 + particles[i].velx,
                            #                    y2 + (-particles[j].vely),
                            #                    y1 + (-particles[i].vely)), "CURRENT DISTANCE: ",
                            #       get_distance(x2, x1, y2, y1), file=orig_stdout)
                            sigma += .1

                            future_collisionx.append(sub_particles[i].velx)
                            future_collisiony.append(sub_particles[i].vely)

                            #future_collisionx[j].append(particles[j].velx)
                           # future_collisiony[j].append(particles[j].vely)
                        #  valid_pos[j] = 1
                        # valid_pos = update_positions(valid_pos,particles,i,j)

                        # valid_pos[i] = 1

                        # update_position(valid_pos, particles)
            # if rank == 0:
            #     print("0")
            # elif rank == 1:
            #     print("1")
            # elif rank ==2:
            #     print("2")

            if(future_collisionx):
                sub_particles[i].velx = min(future_collisionx, key=abs)
                sub_particles[i].vely = min(future_collisiony, key=abs)



            sub_particles[i].posx += sub_particles[i].velx
            sub_particles[i].posy += -(sub_particles[i].vely)

            if(future_collisionx):
                sub_particles[i].velx = future_collisionx[0]
                sub_particles[i].vely = future_collisiony[0]

        #LEFTOVERS DONE ON ROOT
        # if rank == 0:
        #     leftoverInd = blocksize * size
        #     for i in range(leftoverInd, num_particles):
        #         y1 = particles[i].get_Posy()
        #         x1 = particles[i].get_Posx()
        #         if x1 >= WIDTH - particles[i].rad:
        #             if particles[i].velx > 0:
        #                 particles[i].velx *= -1
        #
        #         if x1 <= particles[i].rad:
        #             if particles[i].velx < 0:
        #                 particles[i].velx *= -1
        #
        #         if y1 >= HEIGHT - particles[i].rad:
        #             if particles[i].vely < 0:
        #                 particles[i].vely *= -1
        #
        #         if y1 <= particles[i].rad:
        #             if particles[i].vely > 0:
        #                 particles[i].vely *= -1
        #
        #         vel1 = math.sqrt((particles[i].velx * particles[i].velx) + (particles[i].vely * particles[i].vely))
        #
        #         if particles[i].velx < 0:  # apparently don't need for y since we use it to find the angle?
        #             dir1x = -1
        #         elif particles[i].velx > 0:
        #             dir1x = 1
        #         else:
        #             dir1x = 0
        #
        #         new_vel = vel1 - co_frict * g_acel * (timestep)
        #
        #         if new_vel <= 0:
        #             particles[i].velx = 0
        #             particles[i].vely = 0
        #         else:
        #             ang1 = math.asin(particles[i].vely / vel1)
        #             particles[i].velx = math.cos(ang1) * new_vel * dir1x
        #             particles[i].vely = math.sin(ang1) * new_vel
        #         #END COLLISION STUFF
        #
        #
        #         for k in range(num_particles):
        #             if k == startInd + i:
        #                 continue
        #             # elif i > k and i >= startInd and i <= (startInd+blocksize-1):
        #             #    continue
        #             else:
        #                 x1 = particles[i].get_Posx()
        #                 y1 = particles[i].get_Posy()
        #                 x2 = particles[k].get_Posx()
        #                 y2 = particles[k].get_Posy()
        #
        #                 if collision(x1, x2, y1, y2, particles[i].rad, particles[k].rad, 1):
        #                     xveldif = particles[i].velx - particles[k].velx
        #                     yveldif = particles[i].vely - particles[k].vely
        #
        #                     xdistance = x2 - x1
        #                     ydistance = y2 - y1
        #                     if xveldif * xdistance + yveldif * (-ydistance) >= 0:
        #                         if (particles[i].vely == 0 and particles[k].vely == 0):
        #                             mass1 = particles[i].mass
        #                             mass2 = particles[k].mass
        #                             vel1x = particles[i].velx * (mass1 - mass2) / (mass1 + mass2) + particles[
        #                                 k].velx * 2 * mass2 / (mass1 + mass2)
        #                             vel2x = particles[k].velx * (mass2 - mass1) / (mass1 + mass2) + sub_particles[
        #                                 i].velx * 2 * mass2 / (mass1 + mass2)
        #                             particles[i].velx = vel1x
        #                             particles[k].velx = vel2x
        #                             particles[i].vely = 0
        #                             particles[k].vely = 0
        #                         else:
        #                             angle = math.atan2(ydistance, xdistance)  # gets angle between the two particles
        #                             mass1 = particles[i].mass
        #                             mass2 = particles[k].mass
        #
        #                             u1 = rotate(particles[i].velx, particles[i].vely, angle)
        #                             u2 = rotate(particles[k].velx, particles[k].vely, angle)
        #
        #                             vel1x = u1[0] * (mass1 - mass2) / (mass1 + mass2) + u2[0] * 2 * mass2 / (
        #                                     mass1 + mass2)
        #                             vel2x = u2[0] * (mass2 - mass1) / (mass1 + mass2) + u1[0] * 2 * mass2 / (
        #                                     mass1 + mass2)
        #                             vel1y = u1[1]
        #                             vel2y = u2[1]
        #
        #                             vFinal = rotate(vel1x, vel1y, -angle)
        #                             vFinal2 = rotate(vel2x, vel2y, -angle)
        #
        #                             particles[i].velx = vFinal[0]
        #                             particles[i].vely = vFinal[1]
        #
        #                             particles[k].velx = vFinal2[0]
        #                             particles[k].vely = vFinal2[1]
        #
        #
        #             # Start of Gravity
        #             c_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        #             x_dist = math.sqrt(c_sq - ((y1 - y2) * (y1 - y2)))
        #             y_dist = math.sqrt(c_sq - ((x1 - x2) * (x1 - x2)))
        #
        #             distance = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
        #             force_grav = (G_CONST * particles[i].mass * particles[k].mass) / (distance * distance)
        #
        #             p1_acel = force_grav / particles[i].mass
        #             p2_acel = force_grav / particles[k].mass
        #
        #             p1_acelx = 0
        #             p2_acely = 0
        #             p1_acely = 0
        #             p2_acelx = 0
        #
        #             if x1 > x2 and y1 < y2:  # REPEAT THIS FOR OTHER 3 SCENARIOS                    #p1_acel = - p1_acel
        #
        #                 deg1 = math.acos(y_dist / distance)
        #                 deg2 = math.acos(x_dist / distance)
        #
        #                 p1_acelx = (math.sin(deg1)) * p1_acel
        #                 p1_acely = (math.cos(deg1)) * p1_acel
        #
        #                 p2_acelx = (math.cos(deg2)) * p2_acel
        #                 p2_acely = (math.sin(deg2)) * p2_acel
        #
        #                 p1_acelx = -p1_acelx
        #                 p1_acely = -p1_acely
        #
        #             elif x1 < x2 and y1 < y2:
        #
        #                 # p2_acel = -p2_acel
        #
        #                 deg1 = math.acos(y_dist / distance)
        #                 deg2 = math.acos(x_dist / distance)
        #
        #                 p1_acelx = (math.sin(deg1)) * p1_acel
        #                 p1_acely = (math.cos(deg1)) * p1_acel
        #
        #                 p2_acelx = (math.cos(deg2)) * p2_acel
        #                 p2_acely = (math.sin(deg2)) * p2_acel
        #
        #                 p2_acelx = -p2_acelx
        #                 p1_acely = -p1_acely
        #             # print("here2",file=orig_stdout)
        #             elif x1 > x2 and y1 > y2:
        #                 deg1 = math.asin(y_dist / distance)
        #                 deg2 = math.asin(x_dist / distance)
        #
        #                 p1_acely = (math.sin(deg1)) * p1_acel
        #                 p1_acelx = (math.cos(deg1)) * p1_acel
        #
        #                 p2_acely = (math.cos(deg2)) * p2_acel
        #                 p2_acelx = (math.sin(deg2)) * p2_acel
        #                 # print("here", file=orig_stdout)
        #
        #                 p2_acely = -p2_acely
        #                 p1_acelx = - p1_acelx
        #
        #             elif x1 < x2 and y1 > y2:
        #                 deg1 = math.asin(y_dist / distance)
        #                 deg2 = math.asin(x_dist / distance)
        #
        #                 p1_acely = (math.sin(deg1)) * p1_acel
        #                 p1_acelx = (math.cos(deg1)) * p1_acel
        #
        #                 p2_acely = (math.cos(deg2)) * p2_acel
        #                 p2_acelx = (math.sin(deg2)) * p2_acel
        #
        #                 p2_acelx = -p2_acelx
        #                 p2_acely = -p2_acely
        #             elif x1 == x2 and y1 > y2:
        #                 p1_acelx = 0
        #                 p2_acelx = 0
        #                 p2_acely = -p2_acel
        #                 p1_acely = p1_acel
        #             elif x1 == x2 and y1 < y2:
        #                 p1_acelx = 0
        #                 p2_acelx = 0
        #                 p2_acely = p2_acel
        #                 p1_acely = -p1_acel
        #             elif x1 > x2 and y1 == y2:
        #                 p1_acelx = -p1_acel
        #                 p2_acelx = p2_acel
        #                 p1_acely = 0
        #                 p2_acely = 0
        #             elif x1 < x2 and y1 == y2:
        #                 p1_acelx = p1_acel
        #                 p2_acelx = -p2_acel
        #                 p1_acely = 0
        #                 p2_acely = 0
        #
        #
        #
        #             particles[i].velx = particles[i].velx + (p1_acelx * timestep)
        #             # particles[k].velx = particles[k].velx + (p2_acelx * timestep)
        #
        #             particles[i].vely = particles[i].vely + (p1_acely * timestep)
        #             # particles[k].vely = particles[k].vely + (p2_acely * timestep)
        #
        #         future_collisionx = []
        #         future_collisiony = []
        #         valid_pos = [1] * blocksize
        #
        #
        #         for l in range(num_particles):
        #
        #             if l != i:
        #
        #                 # if valid_pos[i] == 0 and valid_pos[j] == 0:
        #                 # print(particles[i].velx, particles[i].vely, particles[j].velx, particles[j].vely,file=orig_stdout)
        #                 y2 = particles[l].get_Posy()
        #                 x2 = particles[l].get_Posx()
        #                 if collision(x2 + particles[l].velx, x1 + particles[i].velx, y2 + (-particles[l].vely),
        #                              y1 + (-particles[i].vely), particles[l].rad, particles[i].rad, 1) and (
        #                         particles[i].velx != 0 or particles[i].vely != 0 or particles[l].velx != 0 or
        #                         particles[l].vely != 0):
        #                     # print("FUTURE COLLISION BETWEEN ", particles[l].color, sub_particles[i].color)
        #                     # IN HERE ADJUST THE TWO BALLS AND CHECK THEM WITH EVERY OTHER BALL. IF THERE IS NO OVERLAP, THEN IT IS IN VALID SPOT.
        #                     # IF THERE IS OVERLAP WITH OTHER BALLS, ADJUST BALL THAT IS NEWLY IN INVALID SPOT
        #
        #                     future_collisionx.append(particles[
        #                                                  i].velx)  # puts velocity in that partciles velocity array, used to determine old velocity of particle after its collision
        #                     future_collisiony.append(particles[i].vely)
        #
        #                     # if j >= startInd and j <= startInd + blocksize:
        #                     #     future_collisionx[j].append(particles[j].velx)
        #                     #     future_collisiony[j].append(particles[j].vely)
        #                     #
        #                     #
        #                     sigma = 0
        #                     iteration = 0  # prevents infinite loops
        #
        #                     # THIS, FOR MOST PART CHECKS FUTURE DETECTION, RARE MULTIWAY COLLISIONS WILL RESULT IN SOME OVERLAPPING
        #                     while (get_distance(x2 + particles[l].velx, x1 + particles[i].velx,
        #                                         y2 + (-particles[l].vely),
        #                                         y1 + (-particles[i].vely)) < (
        #                                    particles[i].rad + particles[l].rad)) and (iteration < 10):
        #
        #                         iteration += 1
        #
        #                         overlap = (particles[i].rad + particles[l].rad) - get_distance(
        #                             x1 + particles[i].velx,
        #                             x2 + particles[l].velx,
        #                             y1 + (-particles[i].vely),
        #                             y2 + (-particles[l].vely))
        #                         vel1 = math.sqrt(
        #                             (particles[i].velx * particles[i].velx) + (
        #                                         particles[i].vely * particles[i].vely))
        #
        #                         vel2 = math.sqrt(
        #                             (particles[l].velx * particles[l].velx) + (particles[l].vely * particles[l].vely))
        #
        #                         totalvel = vel1 + vel2
        #
        #                         if (totalvel != 0):
        #                             vel1_rat = vel1 / totalvel
        #                             vel2_rat = vel2 / totalvel
        #                         else:
        #                             vel1_rat = 0
        #                             vel2_rat = 0
        #
        #                         if particles[
        #                             i].velx < 0:  # apparently don't need for y since we use it to find the angle?
        #                             dir1x = -1
        #                         elif particles[i].velx > 0:
        #                             dir1x = 1
        #                         else:
        #                             dir1x = 0
        #
        #                         if particles[l].velx < 0:
        #                             dir2x = -1
        #                         elif particles[l].velx > 0:
        #                             dir2x = 1
        #                         else:
        #                             dir2x = 0
        #                         #
        #                         vel1_ov = vel1 - (vel1_rat * overlap)
        #                         vel2_ov = vel2 - (vel2_rat * overlap)
        #
        #                         # TODO: The other scenarios in this conditional (including vely=0 and velx=0).
        #                         # TODO: ISSUE WHERE NO COLLISION DETECTED IF BALL IS GOING SO FAST THAT IS SKIPS OVER THE OTHER BALL
        #                         # NEW IDEA: FIND COLLISION WITH SMALLEST TIME STEP, MAKE THAT THE NEW TIME STEP,
        #                         if (vel1 != 0):
        #                             ang1 = math.asin(particles[i].vely / vel1)
        #                             particles[i].velx = dir1x * vel1_ov * math.cos(ang1)
        #                             particles[i].vely = vel1_ov * math.sin(ang1)
        #
        #                         if (vel2 != 0):
        #                             ang2 = math.asin(particles[l].vely / vel2)
        #                             particles[l].velx = dir2x * vel2_ov * math.cos(ang2)
        #
        #                             particles[l].vely = vel2_ov * math.sin(ang2)
        #
        #                         # print("MEMORY OF INDEX PARTICLE 2", hex(id(particles[2])), "MEMORY OF SUB_PARTICLE AT 2 ", hex(id(sub_particles[2])), "\n\n")
        #                         # iteration += 1
        #
        #                         # print("FUTURE COLLISION BETWEEN ", particles[i].color, particles[j].color,
        #                         #       "CURRENT X VELOCITY: ",
        #                         #       particles[j].velx, particles[i].velx,
        #                         #       "CURRENT Y VELOCITY", particles[i].vely, particles[j].vely, "FUTURE DISTANCE: ",
        #                         #       get_distance(x2 + particles[j].velx, x1 + particles[i].velx,
        #                         #                    y2 + (-particles[j].vely),
        #                         #                    y1 + (-particles[i].vely)), "CURRENT DISTANCE: ",
        #                         #       get_distance(x2, x1, y2, y1), file=orig_stdout)
        #                         sigma += .1
        #
        #                         future_collisionx.append(particles[i].velx)
        #                         future_collisiony.append(particles[i].vely)
        #
        #                         # future_collisionx[j].append(particles[j].velx)
        #                     # future_collisiony[j].append(particles[j].vely)
        #
        #
        #         if (future_collisionx):
        #             particles[i].velx = min(future_collisionx, key=abs)
        #             particles[i].vely = min(future_collisiony, key=abs)
        #
        #         particles[i].posx += particles[i].velx * timestep
        #         particles[i].posy += -(particles[i].vely) * timestep
        #
        #         if (future_collisionx):
        #             particles[i].velx = future_collisionx[0]
        #             particles[i].vely = future_collisiony[0]
                # STOP

                #UPDATE POSITION THEN CHANGE VELOCITIES BACK








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








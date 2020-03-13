from graphics import *
import time
import math
import random
import sys
#TODO STATIC FRICTION, MULTIWAY COLLISIONS
WIDTH = 500
HEIGHT = 500
RADIUS = 20

num_particles = 40
timestep = .03
duration = 200

G_CONST = 0 #Gravitational Constant

sig = 0
g_acel = 9.8
co_frict = .1 #ice = .02 #COEFFECIENT OF FRICTION



class Particle:
    rad = 0
    velx = 0
    vely = 0
    cir = 0
    mass = 0
    color = 0

    def __init__(self, radius, velocityx, velocityy, pt, color, win, m):
        self.rad = radius
        self.velx = velocityx
        self.vely = velocityy
        self.cir = Circle(pt, self.rad)
        self.cir.setFill(color)
        self.cir.draw(win)
        self.mass = m
        self.color = color

    def get_Posx(self):
        return self.cir.getCenter().getX()

    def get_Posy(self):
        return self.cir.getCenter().getY()


def get_distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))


def collision(x1, x2, y1, y2, rad1, rad2,option):
    distance = get_distance(x1,x2,y1,y2)

    if distance <= rad1 + rad2 +sig:
        return True
    else:
        return False


def rotate(velx,vely,angle):
    rotate_vel = [velx*math.cos(angle)-vely*math.sin(angle),
                  velx*math.sin(angle)+vely*math.cos(angle)]
    return rotate_vel

def main():
    orig_stdout = sys.stdout

    sys.stdout = open('output.txt', 'w')

    win = GraphWin("MyWindow", WIDTH, HEIGHT)

    colors = ['red', 'green', 'blue', 'yellow', 'black', 'white', 'orange', 'brown', 'purple', 'pink', 'teal', 'maroon', 'magenta', 'tan', 'gold', 'grey', 'cyan']
    old_velsx = []
    old_velsy = []
    ind_arr = []
    particles = []
    n = 0
    j = 0
    future_col=False
    num_timesteps = duration/timestep
    counter = 0
    print(num_particles)
    print(num_timesteps)
    print()
    time_counter = 0
    collision_array = [[] for j in range(num_particles)]
    #print(collision_array, file=orig_stdout)

    for i in range(num_particles):

        x = random.randint(RADIUS, WIDTH - RADIUS)
        y = random.randint(RADIUS, HEIGHT - RADIUS)
        rad = RADIUS
        k=0

        while( k < len(particles)):
            if get_distance(particles[k].get_Posx(),x,particles[k].get_Posy(),y) <= particles[k].rad + rad:
                x = random.randint(RADIUS, WIDTH - RADIUS)
                y = random.randint(RADIUS, HEIGHT - RADIUS)
                k = 0
            else:
                k+=1


        particles.append(Particle(RADIUS, random.randint(-10, 10), random.randint(-10, 10),
                                  Point(x, y),
                                  colors[j], win, 1))

        while particles[i].velx != 0 and particles[i].vely != 0:
            particles[i].velx = random.randint(-10, 10)

            particles[i].vely = random.randint(-10,10)

        print(particles[i].rad, particles[i].get_Posx(), particles[i].get_Posy(), colors[j])

        # radius, posx, posy, color, mass

        j += 1

        if j >= len(colors):
            j = 0


    #
    # particles.append(Particle(RADIUS, -10, 0,
    #                           Point(20, 100), colors[0],
    #                           win, 1))
    # particles.append(Particle(RADIUS, -10, 0,
    #                           Point(190, 100), colors[1],
    #                           win, 1))
    # particles.append(Particle(RADIUS, 8, 0,
    #                           Point(150, 100), colors[2],
    #                           win, 1))
    #
    # particles.append(Particle(RADIUS, 5, 0,
    #                           Point(220, 100), colors[3],
    #                           win, 1))
    #
    # particles.append(Particle(RADIUS, -4, 0,
    #                           Point(60, 100), colors[4],
    #                           win, 1))
    #
    # particles.append(Particle(RADIUS, 2, 0,
    #                           Point(100, 100), colors[5],
    #                           win, 1))
    #

    #
    print(particles[0].rad, particles[0].get_Posx(), particles[0].get_Posy(),colors[0])
    print(particles[1].rad, particles[1].get_Posx(), particles[1].get_Posy(),colors[1])
    print(particles[2].rad, particles[2].get_Posx(), particles[2].get_Posy(),colors[2])
    print(particles[3].rad, particles[3].get_Posx(), particles[3].get_Posy(),colors[3])
    print(particles[4].rad, particles[4].get_Posx(), particles[4].get_Posy(),colors[4])
    print(particles[5].rad, particles[5].get_Posx(), particles[5].get_Posy(),colors[5])
    # print(particles[0].rad, particles[0].get_Posx(), particles[0].get_Posy(), colors[6])
    #print(particles[1].rad, particles[1].get_Posx(), particles[1].get_Posy(), colors[7])


    print()

    sleeper = .001

    for k in range(int(num_timesteps)):
        old_velsx[:] = []
        old_velsy[:] = []
        ind_arr[:] = []
        for l in range(num_particles):
            collision_array[l][:] = []
        for i in range(num_particles):  # collision detection with wall
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
            #END OF WALL BOUNCING CHECKS/FRICTION


        for i in range(num_particles):
            for j in range(i+1,num_particles,1):
                x1 = particles[i].get_Posx()
                y1 = particles[i].get_Posy()
                x2 = particles[j].get_Posx()
                y2 = particles[j].get_Posy()
                if collision(x1, x2, y1, y2, particles[i].rad, particles[j].rad, 0):
                    collision_array[i].append(j)

       # print(collision_array, file=orig_stdout)

        for i in range(num_particles):
            for j in range(len(collision_array[i])):

                for k in range(j,len(collision_array[i])):
                    index = collision_array[i][j]
                    vel1 = math.sqrt((particles[index].velx * particles[index].velx) + (
                                particles[index].vely * particles[index].vely))

                    index2 = collision_array[i][k]
                    vel2 = math.sqrt((particles[index2].velx*particles[index2].velx)+(particles[index2].vely*particles[index2].vely))
                    if vel2 > vel1:
                        tmp = collision_array[i][j]
                        collision_array[i][j] = collision_array[i][k]
                        collision_array[i][k] = tmp

        #print(collision_array, file=orig_stdout)

        for m in range(num_particles):
            i = m
            normal_vector = []
            x1 = particles[i].get_Posx()
            y1 = particles[i].get_Posy()
            for n in range(len(collision_array[i])):
                j = collision_array[m][n]
                # x2 = particles[j].get_Posx()
                # y2 = particles[j].get_Posy()
                #
                # normal_vector =[x2-x1, y2-y1]
                #
                # dist = get_distance(x2,x1,y2,y1)
                #
                # unit_vector = [normal_vector[0]*(1/dist),normal_vector[1]*(1/dist)]
                #
                # unit_tangent = [-unit_vector[1],unit_vector[0]]
                #
                # v1n = particles[i].velx * unit_vector[0] + particles[i].vely * unit_vector[1]
                # v1t = particles[i].velx * unit_tangent[0] + particles[i].vely * unit_tangent[1]
                #
                # v2n = particles[j].velx * unit_vector[0] + particles[j].vely * unit_vector[1]
                # v2t = particles[j].velx * unit_tangent[0] + particles[j].vely * unit_tangent[1]
                #
                # v1nTag = (v1n*(particles[i].mass - particles[j].mass)+(2*particles[j].mass*v2n))/(particles[i].mass+particles[j].mass)
                # v2nTag = (v2n *(particles[j].mass - particles[i].mass)+(2*particles[i].mass*v1n))/(particles[i].mass+particles[j].mass)
                #
                # v1nTag2 = [v1nTag*unit_vector[0],v1nTag*unit_vector[1]]
                # v1tTag = [unit_tangent[0]*v1t,unit_tangent[1]*v1t]
                #
                # v2nTag2 = [v2nTag*unit_vector[0],v2nTag*unit_vector[1]]
                # v2tTag = [unit_tangent[0]*v2t,unit_tangent[1]*v2t]
                #
                # particles[i].velx = v1nTag2[0] + v1tTag[0]
                # particles[i].vely = v1nTag2[1] + v1tTag[1]
                #
                # particles[j].velx = v2nTag2[0] + v2tTag[0]
                # particles[j].vely = v2nTag2[1] + v2tTag[1]





                # cir_oldvelx = particles[i].velx
                # cir2_oldvelx = particles[j].velx
                # particles[j].velx = (
                #                             particles[i].mass * cir_oldvelx + particles[
                #                         j].mass * cir2_oldvelx - cir2_oldvelx * particles[i].mass + cir_oldvelx *
                #                             particles[i].mass) / (
                #                             particles[i].mass + particles[j].mass)
                #
                # particles[i].velx = particles[j].velx + cir2_oldvelx - cir_oldvelx
                # # particles[i].velx = (particles[i].mass*cir_oldvelx+particles[j].mass*cir2_oldvelx-particles[j].mass*particles[j].velx)/particles[i].mass
                #
                # cir_oldvely = particles[i].vely
                # cir2_oldvely = particles[j].vely
                # particles[j].vely = (
                #                             particles[i].mass * cir_oldvely + particles[
                #                         j].mass * cir2_oldvely - cir2_oldvely * particles[i].mass + cir_oldvely *
                #                             particles[i].mass) / (
                #                             particles[i].mass + particles[j].mass)
                # particles[i].vely = (particles[i].mass * cir_oldvely + particles[j].mass * cir2_oldvely - particles[
                #     j].mass * particles[j].vely) / particles[i].mass
                # print("BOOM BETWEEN", particles[i].color, particles[j].color, "\nVelocities for ",
                #       particles[i].color, ": ", particles[i].velx, particles[i].vely, "\nVelocities for ",
                #       particles[j].color, ": ", particles[j].velx, particles[j].vely, file=orig_stdout)

        for i in range(num_particles):
            for j in range(i+1, num_particles, 1):

                x1 = particles[i].get_Posx()
                y1 = particles[i].get_Posy()
                x2 = particles[j].get_Posx()
                y2 = particles[j].get_Posy()
                col2 =False

                if collision(x1, x2, y1, y2, particles[i].rad, particles[j].rad,0):
             #       print("BOOM BETWEEN", particles[i].color,particles[j].color, "DISTANCE APART IS: ", get_distance(x1,x2,y1,y2),"\n",file=orig_stdout)
                    xveldif = particles[i].velx - particles[j].velx
                    yveldif = particles[i].vely - particles[j].vely

                    xdistance = x2 - x1
                    ydistance = y2-y1
                    if xveldif * xdistance + yveldif * (-ydistance) >= 0:  # prevent accidental overlaps
                   # print("IN HERE WITH ", particles[i].color, particles[j].color,file=orig_stdout)
                        if(particles[i].vely == 0 and particles[j].vely == 0):
                            mass1 = particles[i].mass
                            mass2 = particles[j].mass
                            vel1x = particles[i].velx * (mass1 - mass2) / (mass1 + mass2) + particles[j].velx * 2 * mass2 / (mass1 + mass2)
                            vel2x = particles[j].velx * (mass2 - mass1) / (mass1 + mass2) + particles[i].velx * 2 * mass2 / (mass1 + mass2)
                            particles[i].velx = vel1x
                            particles[j].velx = vel2x
                            particles[i].vely = 0
                            particles[j].vely = 0
                        else:
                            angle = math.atan2(ydistance, xdistance)  # gets angle between the two particles
                            mass1 = particles[i].mass
                            mass2 = particles[j].mass

                            u1 = rotate(particles[i].velx, particles[i].vely, angle)
                            u2 = rotate(particles[j].velx, particles[j].vely, angle)

                            vel1x = u1[0] * (mass1 - mass2) / (mass1 + mass2) + u2[0] * 2 * mass2 / (mass1 + mass2)
                            vel2x = u2[0]*(mass2-mass1)/(mass1+mass2) + u1[0] * 2 * mass2 / (mass1 + mass2)
                            vel1y = u1[1]
                            vel2y = u2[1]

                            vFinal = rotate(vel1x, vel1y, -angle)
                            vFinal2 = rotate(vel2x, vel2y, -angle)

                            particles[i].velx = vFinal[0]
                            particles[i].vely = vFinal[1]

                            particles[j].velx = vFinal2[0]
                            particles[j].vely = vFinal2[1]
                         #   print("IN HERE WITH ", particles[i].color, particles[j].color, "FINAL X VELOCITIES: ", particles[i].velx,particles[j].velx,"FINAL Y VELOCITIES: ", particles[i].vely,particles[j].vely, file=orig_stdout)

                #     counter+=1
                #     col2=True
                #
                #     cir_oldvelx = particles[i].velx
                #     cir2_oldvelx = particles[j].velx
                #     particles[j].velx = (
                #                          particles[i].mass * cir_oldvelx + particles[j].mass * cir2_oldvelx - cir2_oldvelx * particles[i].mass + cir_oldvelx * particles[i].mass) / (
                #                         particles[i].mass + particles[j].mass)
                #
                #     particles[i].velx = particles[j].velx + cir2_oldvelx - cir_oldvelx
                #     #particles[i].velx = (particles[i].mass*cir_oldvelx+particles[j].mass*cir2_oldvelx-particles[j].mass*particles[j].velx)/particles[i].mass
                #
                #     cir_oldvely = particles[i].vely
                #     cir2_oldvely = particles[j].vely
                #     particles[j].vely = (
                #                          particles[i].mass * cir_oldvely + particles[j].mass * cir2_oldvely - cir2_oldvely * particles[i].mass + cir_oldvely * particles[i].mass) / (
                #                         particles[i].mass + particles[j].mass)
                #     particles[i].vely = (particles[i].mass*cir_oldvely+particles[j].mass*cir2_oldvely-particles[j].mass*particles[j].vely)/particles[i].mass
                #     print("BOOM BETWEEN", particles[i].color, particles[j].color, "\nVelocities for ",
                #           particles[i].color, ": ", particles[i].velx, particles[i].vely, "\nVelocities for ",
                #           particles[j].color, ": ", particles[j].velx, particles[j].vely, file=orig_stdout)
                #
                #
                # # print("OLD VELX: ", cir_oldvelx, "OLD VELY: ", cir_oldvelx, file=orig_stdout)
                #     #print("NEW VELX: ", particles[0].velx, "NEW VELY: ", particles[0].vely, file=orig_stdout)
                #     #print("",file= orig_stdout)


                    # normal_vector = [x1 - x2, y1 - y2]
                    #
                    # dist = get_distance(x2, x1, y2, y1)
                    #
                    # unit_vector = [normal_vector[0] * (1 / dist), normal_vector[1] * (1 / dist)]
                    #
                    # unit_tangent = [-unit_vector[1], unit_vector[0]]
                    #
                    # v1n = particles[i].velx * unit_vector[0] + particles[i].vely * unit_vector[1]
                    # v1t = particles[i].velx * unit_tangent[0] + particles[i].vely * unit_tangent[1]
                    #
                    # v2n = particles[j].velx * unit_vector[0] + particles[j].vely * unit_vector[1]
                    # v2t = particles[j].velx * unit_tangent[0] + particles[j].vely * unit_tangent[1]
                    #
                    # v1nTag = (v1n * (particles[i].mass - particles[j].mass) + (2 * particles[j].mass * v2n)) / (
                    #             particles[i].mass + particles[j].mass)
                    # v2nTag = (v2n * (particles[j].mass - particles[i].mass) + (2 * particles[i].mass * v1n)) / (
                    #             particles[i].mass + particles[j].mass)
                    #
                    # v1nTag2 = [v1nTag * unit_vector[0], v1nTag * unit_vector[1]]
                    # v1tTag = [unit_tangent[0] * v1t, unit_tangent[1] * v1t]
                    #
                    # v2nTag2 = [v2nTag * unit_vector[0], v2nTag * unit_vector[1]]
                    # v2tTag = [unit_tangent[0] * v2t, unit_tangent[1] * v2t]
                    #
                    # particles[i].velx = v1nTag2[0] + v1tTag[0]
                    # particles[i].vely = v1nTag2[1] + v1tTag[1]
                    #
                    # particles[j].velx = v2nTag2[0] + v2tTag[0]
                    # particles[j].vely = v2nTag2[1] + v2tTag[1]

                else:
                    col2= False
                    #print("no boom: ", get_distance(x1,x2,y1,y2), file=orig_stdout)

                c_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                x_dist = math.sqrt(c_sq - ((y1 - y2) * (y1 - y2)))
                y_dist = math.sqrt(c_sq - ((x1 - x2) * (x1 - x2)))

                distance = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
                force_grav = (G_CONST * particles[i].mass * particles[j].mass) / (distance * distance)

                p1_acel = force_grav / particles[i].mass
                p2_acel = force_grav / particles[j].mass

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

               # print("VELX: ", particles[j].velx, " VELY: ", particles[j].vely, file=orig_stdout)
               # print("ACCELX: ", p2_acelx, " ACCELY: ", p2_acely, file=orig_stdout)
                #print("",file=orig_stdout)



                particles[i].velx = particles[i].velx + (p1_acelx * timestep)
                particles[j].velx = particles[j].velx + (p2_acelx * timestep)

                particles[i].vely = particles[i].vely + (p1_acely * timestep)
                particles[j].vely = particles[j].vely + (p2_acely * timestep)


        # End of collision and gravity stuff
       # print(file=orig_stdout)

        for i in range(num_particles):
            y1 = particles[i].get_Posy()
            x1 = particles[i].get_Posx()
            for j in range(i + 1, num_particles,1):
                #print(particles[i].velx, particles[i].vely, particles[j].velx, particles[j].vely,file=orig_stdout)
                y2 = particles[j].get_Posy()
                x2 = particles[j].get_Posx()
                if collision(x2 + particles[j].velx, x1 + particles[i].velx, y2 + (-particles[j].vely),
                             y1 + (-particles[i].vely), particles[j].rad, particles[i].rad, 1) and (particles[i].velx!=0 or particles[i].vely!=0 or particles[j].velx!=0 or particles[j].vely!=0):
                    iteration = 0
                   #
                   #
                   # # ISSUE OCCURED WHEN PARTICLE WAS GOING SO FAST IT ENDED UP ON THE OTHER SIDE OF THE PARTICLE IT WOULD COLLIDE WITH. THIS WOULD THROW OFF THE DISTANCE FORMULA, MAKING THEM STILL INTERSECT OUTSIDE THEIR BORDERS
                   #  while (get_distance(x2 + particles[j].velx, x1 + particles[i].velx, y2 + (-particles[j].vely),
                   #  #                    y1 + (-particles[i].vely)) < (particles[i].rad + particles[j].rad) - sig):
                   #
            #         if (iteration == 0):
            #             old_velsx.append(particles[i].velx)
            #             old_velsy.append(particles[i].vely)
            #             ind_arr.append(i)
            #
            #             old_velsx.append(particles[j].velx)
            #             old_velsy.append(particles[j].vely)
            #             ind_arr.append(j)
            #
            #
            #         overlap = (particles[i].rad + particles[j].rad) - get_distance(x1 + particles[i].velx,
            #                                                                        x2 + particles[j].velx,
            #                                                                        y1 + (-particles[i].vely),
            #                                                                        y2 + (-particles[j].vely))
            #         vel1 = math.sqrt(
            #             (particles[i].velx * particles[i].velx) + (particles[i].vely * particles[i].vely))
            #         vel2 = math.sqrt(
            #             (particles[j].velx * particles[j].velx) + (particles[j].vely * particles[j].vely))
            #
            #         totalvel = vel1 + vel2
            #
            #         if(totalvel != 0):
            #             vel1_rat = vel1 / totalvel
            #             vel2_rat = vel2 / totalvel
            #         else:
            #             vel1_rat = 0
            #             vel2_rat = 0
            #
            #         if particles[i].velx < 0:  # apparently don't need for y since we use it to find the angle?
            #             dir1x = -1
            #         elif particles[i].velx > 0:
            #             dir1x = 1
            #         else:
            #             dir1x = 0
            #
            #         if particles[j].velx < 0:
            #             dir2x = -1
            #         elif particles[j].velx > 0:
            #             dir2x = 1
            #         else:
            #             dir2x = 0
            #
            #         vel1_ov = vel1 - (vel1_rat * overlap)
            #         vel2_ov = vel2 - (vel2_rat * overlap)
            #
            #         # TODO: The other scenarios in this conditional (including vely=0 and velx=0).
            #         # TODO: ISSUE WHERE NO COLLISION DETECTED IF BALL IS GOING SO FAST THAT IS SKIPS OVER THE OTHER BALL
            #
            #         if(vel1!=0):
            #             ang1 = math.asin(particles[i].vely / vel1)
            #             particles[i].velx = dir1x * vel1_ov * math.cos(ang1)
            #             particles[i].vely = vel1_ov * math.sin(ang1)
            #
            #         if(vel2!=0):
            #             ang2 = math.asin(particles[j].vely / vel2)
            #             particles[j].velx = dir2x * vel2_ov * math.cos(ang2)
            #             particles[j].vely = vel2_ov * math.sin(ang2)
            #         iteration += 1
            #
            #         print("FUTURE COLLISION BETWEEN ", particles[i].color, particles[j].color, "CURRENT X VELOCITY: ",
            #              particles[j].velx, particles[i].velx,
            #              "CURRENT Y VELOCITY", particles[i].vely, particles[j].vely, "FUTURE DISTANCE: ",
            #              get_distance(x2 + particles[j].velx, x1 + particles[i].velx, y2 + (-particles[j].vely),
            #                          y1 + (-particles[i].vely)), "CURRENT DISTANCE: ",
            #              get_distance(x2, x1, y2, y1), file=orig_stdout)
            #         test= 9
            # # End of future collision loops

        for i in range(num_particles):
            print(particles[i].get_Posx(), particles[i].get_Posy())
            #print("Particle: ", i, "velocity x and y", particles[i].velx, particles[i].vely, "\n", file=orig_stdout)
            particles[i].cir.move(particles[i].velx, -particles[i].vely)

        for q in range(len(ind_arr)):
            #print("particles", particles[ind_arr[q]].color, "slower velocity x and y: ", particles[ind_arr[q]].velx, particles[ind_arr[q]].vely, file=orig_stdout)
            #print("particles", particles[ind_arr[q]].color, "new, faster velocity x and y: ", old_velsx[q],
             #     old_velsy[q], "\n", file=orig_stdout)
            particles[ind_arr[q]].velx = old_velsx[q]
            particles[ind_arr[q]].vely = old_velsy[q]

        time_counter += 1
        #time.sleep(.03)

    sys.stdout.close()
    win.close()

main()
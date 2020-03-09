from graphics import *
import time
import math
import random
import sys

WIDTH = 500
HEIGHT = 500
RADIUS = 5

num_particles = 2
timestep = .03
duration = 20

G_CONST = 1

sig = .00001

class Particle:
    rad = 0
    velx = 0
    vely = 0
    cir = 0
    mass = 0

    def __init__(self, radius, velocityx, velocityy, pt, color, win, m):
        self.rad = radius
        self.velx = velocityx
        self.vely = velocityy
        self.cir = Circle(pt, self.rad)
        self.cir.setFill(color)
        self.cir.draw(win)
        self.mass = m

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
    """
    for i in range(num_particles):

        particles.append(Particle(RADIUS, random.randint(-11, 11), random.randint(-11, 11),
                                  Point(random.randint(0, WIDTH - RADIUS), random.randint(0, HEIGHT - RADIUS)),
                                  colors[j], win, 1))

        while particles[i].velx == 0 and particles[i].vely == 0:
            particles[i].velx = random.randint(-11, 11)

            particles[i].vely = random.randint(-11, 11)
          
        print(particles[i].rad, particles[i].get_Posx(), particles[i].get_Posy(), colors[j])

        # radius, posx, posy, color, mass

        j += 1

        if j >= len(colors):
            j = 0
    """




    particles.append(Particle(50,4, 0,
                              Point(190, 200), colors[0],
                              win, 300))

    particles.append(Particle(RADIUS, 10, 0,
                              Point(100, 200), colors[1],
                              win, 1))

    #particles.append(Particle(RADIUS, 0, 0,
     #                         Point(60, 60), colors[0],
      #                        win, 300000))

    #particles.append(Particle(5, 0, 0,
       #                       Point(450, 469), colors[1],
        #                      win, 1))






    print(particles[0].rad, particles[0].get_Posx(), particles[0].get_Posy(), colors[0])
    print(particles[1].rad, particles[1].get_Posx(), particles[1].get_Posy(), colors[5])


    print()

    sleeper = .001

    for k in range(int(num_timesteps)):
        old_velsx[:] = []
        old_velsy[:] = []
        ind_arr[:] = []
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

        for i in range(num_particles):
            for j in range(i+1, num_particles, 1):

                x1 = particles[i].get_Posx()
                y1 = particles[i].get_Posy()
                x2 = particles[j].get_Posx()
                y2 = particles[j].get_Posy()
                col2 =False

                if collision(x1, x2, y1, y2, particles[i].rad, particles[j].rad,0):
                    print("BOOM DISTANCE APART IS: ", get_distance(x1,x2,y1,y2),"\n",file=orig_stdout)
                    counter+=1
                    col2=True

                    cir_oldvelx = particles[i].velx
                    cir2_oldvelx = particles[j].velx
                    particles[j].velx = (
                                         particles[i].mass * cir_oldvelx + particles[j].mass * cir2_oldvelx - cir2_oldvelx * particles[i].mass + cir_oldvelx * particles[i].mass) / (
                                        particles[i].mass + particles[j].mass)

                  #  particles[i].velx = particles[j].velx + cir2_oldvelx - cir_oldvelx
                    particles[i].velx = (particles[i].mass*cir_oldvelx+particles[j].mass*cir2_oldvelx-particles[j].mass*particles[j].velx)/particles[i].mass

                    cir_oldvely = particles[i].vely
                    cir2_oldvely = particles[j].vely
                    particles[j].vely = (
                                         particles[i].mass * cir_oldvely + particles[j].mass * cir2_oldvely - cir2_oldvely * particles[i].mass + cir_oldvely * particles[i].mass) / (
                                        particles[i].mass + particles[j].mass)
                    particles[i].vely = (particles[i].mass*cir_oldvely+particles[j].mass*cir2_oldvely-particles[j].mass*particles[j].vely)/particles[i].mass


                   # print("OLD VELX: ", cir_oldvelx, "OLD VELY: ", cir_oldvelx, file=orig_stdout)
                    #print("NEW VELX: ", particles[0].velx, "NEW VELY: ", particles[0].vely, file=orig_stdout)
                    #print("",file= orig_stdout)
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



                particles[i].velx = particles[i].velx + p1_acelx * timestep
                particles[j].velx = particles[j].velx + p2_acelx * timestep

                particles[i].vely = particles[i].vely + p1_acely * timestep
                particles[j].vely = particles[j].vely + p2_acely * timestep



                #if(col2==True):
                   # print("i=",i,file=orig_stdout)
                    #print("VELX AFTER ACCELERATION: ", particles[0].velx, "VELY: ", particles[0].vely, file=orig_stdout)
                #Problem with timestep, i think it is due to the accelration outweighing the velocity

                #print(x1+particles[i].velx, x2+particles[j].velx, y1+(-particles[i].vely), y2+(-particles[j].vely), file=orig_stdout)

                if collision(x2+particles[j].velx, x1+particles[i].velx, y2+(-particles[j].vely), y1+(-particles[i].vely), particles[j].rad, particles[i].rad, 1):
                    iteration = 0
                    # ISSUE OCCURED WHEN PARTICLE WAS GOING SO FAST IT ENDED UP ON THE OTHER SIDE OF THE PARTICLE IT WOULD COLLIDE WITH. THIS WOULD THROW OFF THE DISTANCE FORMULA, MAKING THEM STILL INTERSECT OUTSIDE THEIR BORDERS
                    while(get_distance(x2+particles[j].velx, x1+particles[i].velx, y2+(-particles[j].vely), y1+(-particles[i].vely)) < particles[i].rad + particles[j].rad):
                        print("FUTURE COLLISION, CURRENT X VELOCITY: ", particles[j].velx, particles[i].velx, "CURRENT Y VELOCITY", particles[i].vely,particles[j].vely, "FUTURE DISTANCE: ", get_distance(x2+particles[j].velx, x1+particles[i].velx, y2+(-particles[j].vely), y1+(-particles[i].vely)) , "CURRENT DISTANCE: ", get_distance(x2, x1, y2, y1),file=orig_stdout)

                        future_col = True
                        if(iteration == 0):
                            old_velsx.append(particles[i].velx)
                            old_velsy.append(particles[i].vely)
                            ind_arr.append(i)

                            old_velsx.append(particles[j].velx)
                            old_velsy.append(particles[j].vely)
                            ind_arr.append(j)

                        overlap = (particles[i].rad+particles[j].rad) - get_distance(x1+particles[i].velx, x2+particles[j].velx, y1+(-particles[i].vely), y2+(-particles[j].vely))
                        vel1 = math.sqrt((particles[i].velx*particles[i].velx)+(particles[i].vely * particles[i].vely))
                        vel2 = math.sqrt((particles[j].velx*particles[j].velx)+(particles[j].vely * particles[j].vely))

                        totalvel = vel1+vel2

                        vel1_rat = vel1/totalvel
                        vel2_rat = vel2/totalvel

                        print("overlap = ", overlap, file=orig_stdout)
                        print("ratios = ", vel1_rat, vel2_rat, file=orig_stdout)
                        #print("TOTAL VEL: ", totalvel, file=orig_stdout)
                        #print("VEL1_RAT: ", vel1_rat, file=orig_stdout)

                        if particles[i].velx < 0: #apparently don't need for y since we use it to find the angle?
                            dir1x = -1
                        elif particles[i].velx > 0:
                            dir1x = 1
                        else:
                            dir1x = 0

                        if particles[j].velx < 0:
                            dir2x = -1
                        elif particles[j].velx > 0:
                            dir2x = 1
                        else:
                            dir2x = 0

                        if particles[i].vely < 0: #apparently don't need for y since we use it to find the angle?
                            dir1y = -1
                            #print("vel2_ov: ",  file=orig_stdout)
                        elif particles[i].vely > 0:
                            dir1y = 1
                        else:
                            dir1y = 0

                        if particles[j].vely < 0:
                            dir2y = -1
                            #print("vel2_ov: ", file=orig_stdout)
                        elif particles[j].vely > 0:
                            dir2y = 1
                        else:
                            dir2y = 0
                        """"
                     # TODO TEST FOR Y VALUES, WHAT TO DO WHEN X AND Y ARE INVOLVED. EX: XS ARE BOTH POSITIVE BUT Y VELOCITIES ARE OPPOSITES
                        if (dir1x == 1 and dir2x == 1) or (dir1x == -1 and dir2x == -1):
                            if vel1 > vel2:
                                vel1_ov = vel1 - overlap
                                vel2_ov = vel2
                            else:
                                vel2_ov = vel2 - overlap
                                vel1_ov = vel1
                        elif (dir1y == 1 and dir2y == 1) or (dir2y == -1 and dir2y == -1):
                            if vel1 > vel2:
                                vel1_ov = vel1 - overlap
                                vel2_ov = vel2
                            else:
                                #print("vel2_ov: ",  file=orig_stdout)
                                vel2_ov = vel2 - overlap
                                vel1_ov = vel1
                        else:"""
                        vel1_ov = vel1 - (vel1_rat * overlap)
                        vel2_ov = vel2  - (vel2_rat * overlap)

                        #print("Old velocity: ", vel1, file=orig_stdout)
                        #print("New velocity: ", vel2_ov, file=orig_stdout)

                    #TODO: The other scenarios in this conditional (including vely=0 and velx=0).
                    #TODO: ISSUE WHERE NO COLLISION DETECTED IF BALL IS GOING SO FAST THAT IS SKIPS OVER THE OTHER BALL



                       # if vel1 != abs(particles[i].velx) and vel1 != abs(particles[i].vely):
                        ang1 = math.asin(particles[i].vely/vel1)
                        particles[i].velx = dir1x * vel1_ov * math.cos(ang1)
                        particles[i].vely = vel1_ov * math.sin(ang1)

             #           elif vel1 == abs(particles[i].velx):

                        #particles[i].velx = vel1_ov * dir1x
                       # elif vel1 == abs(particles[i].vely):
                        #particles[i].vely = vel1_ov *dir1y


                        #if vel2 != abs(particles[j].velx) and vel2 != abs(particles[j].vely):

                        ang2 = math.asin(particles[j].vely / vel2)
                        particles[j].velx = dir2x * vel2_ov * math.cos(ang2)
                        particles[j].vely = vel2_ov * math.sin(ang2)
                        #elif vel2 == abs(particles[j].velx):

                        #particles[j].velx = vel2_ov * dir2x
                       # elif vel2 == abs(particles[j].vely):

                        #    particles[j].vely = vel2_ov * dir2y


                        print("x1: ", particles[i].get_Posx(), "y2: ", particles[i].get_Posy(), "vel2 here: ",
                              particles[i].vely, file=orig_stdout)

                        print("x2: ", particles[j].get_Posx(), "y2: ", particles[j].get_Posy(), "vel2 here: ", particles[j].vely, file=orig_stdout)
                        print("NEW FUTURE DISTANCE = ", get_distance(x1+particles[i].velx, x2+particles[j].velx, y1+(-particles[i].vely), y2+(-particles[j].vely)), file=orig_stdout)
                        iteration += 1




                    """
                    d = get_distance(x1+particles[i].velx, x2+particles[j].velx, y1+(-particles[i].vely), y2+(-particles[j].vely))
                    x_dist = abs((x1+particles[i].velx) - (x2+particles[j].velx))
                    y_dist = abs((y1+(-particles[i].vely)) - (y2+(-particles[j].vely)))
                    print("Upcoming Overlap = ", overlap,  file=orig_stdout)
                    print("distance = ", d, file=orig_stdout)
                    print("x_dist = ", x_dist, file = orig_stdout)
                    print("y_dist = ", y_dist, file=orig_stdout)
                    ang1 = math.acos(y_dist/d)
                    ang2 = math.acos(x_dist/d)

                    particles[i].velx= -(vel1_ov*math.cos(ang2))
                    particles[i].vely= -(vel1_ov*math.sin(ang2))

                    particles[j].velx = vel2_ov*math.sin(ang1)
                    particles[j].vely = vel2_ov*math.cos(ang1)
                    """


                    #old_ind[0] = i
                    #old_ind[1] = j
                   # print("",file=orig_stdout)
                else:
                    future_col = False
                   # print("VELX: ", particles[i].velx, file=orig_stdout)
                    #print("VELY: ", particles[i].vely, file=orig_stdout)
                    #print("",file=orig_stdout)


        for i in range(num_particles):
            print(particles[i].get_Posx(), particles[i].get_Posy())
            #if(i==0):
                #print("velx: ", particles[i].velx, "vely: ", particles[i].vely, file = orig_stdout)
            particles[i].cir.move(particles[i].velx, -particles[i].vely)



       # print(old_velsx, file=orig_stdout)
        for q in range(len(ind_arr)):
           # print("HERE", file=orig_stdout)
           # print("Ind_arr[l] = ", q, file=orig_stdout)
            particles[ind_arr[q]].velx = old_velsx[q]
            particles[ind_arr[q]].vely = old_velsy[q]

            #print("old velx: ", old_vels[0], file=orig_stdout)
            #print("old vely: ", old_vels[1], file=orig_stdout)


           # particles[old_ind[1]].velx = old_vels[2]
           # particles[old_ind[1]].vely = old_vels[3]
            future_col = False

        if counter == 4:
            sleeper = 1
        time.sleep(.03)

    sys.stdout.close()
    win.close()

main()
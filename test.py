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

sig = .000001

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
    old_vels = [0,0,0,0]
    old_ind = [0,0]
    # error with velocity 4 and 13
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


    particles.append(Particle(40, 0, 0,
                              Point(450, 450), colors[5],
                              win, 1))

    particles.append(Particle(40, 0, 0,
                              Point(44, 47), colors[0],
                              win, 300000))



    print(particles[0].rad, particles[0].get_Posx(), particles[0].get_Posy(), colors[0])
    print(particles[1].rad, particles[1].get_Posx(), particles[1].get_Posy(), colors[5])


    print()

    sleeper = .001

    for k in range(int(num_timesteps)):
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
                    print("BOOM", file=orig_stdout)
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
                    print("no boom: ", get_distance(x1,x2,y1,y2), file=orig_stdout)

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
                    print("FUTURE COLLISION, CURRENT X VELOCITY: ", particles[i].velx, "CURRENT Y VELOCITY", particles[i].vely, "FUTURE DISTANCE: ", get_distance(x2+particles[j].velx, x1+particles[i].velx, y2+(-particles[j].vely), y1+(-particles[i].vely)) , "CURRENT DISTANCE: ", get_distance(x2, x1, y2, y1),file=orig_stdout)

                    future_col = True
                    """
                    vel1= math.sqrt((particles[i].velx*particles[i].velx)+(particles[i].vely*particles[i].vely))
                    vel2= math.sqrt((particles[j].velx*particles[j].velx)+(particles[j].vely*particles[j].vely))

                    num1 = (particles[i].rad + particles[j].rad+particles[j].get_Posx()-particles[i].get_Posx())/(particles[i].velx-particles[j].velx)
                    num2 = (particles[i].rad + particles[j].rad+particles[j].get_Posy()-particles[i].get_Posy())/(particles[i].vely-particles[j].vely)
                    den1 = (particles[j].get_Posx()-particles[i].get_Posx())/(particles[i].velx-particles[j].velx)
                    den2 = (particles[j].get_Posy()-particles[i].get_Posy())/(particles[i].vely-particles[j].vely)

                    multiplier= abs(num1/den1)
                    multiplier2= abs(num2/den2)

                    print(multiplier, " ", multiplier2, file=orig_stdout)
                    old_vels[0] = particles[i].velx
                    old_vels[1] = particles[i].vely
                    old_vels[2] = particles[j].velx
                    old_vels[3] = particles[j].vely

                    old_ind[0] = i
                    old_ind[1] = j
                    particles[i].velx *= multiplier
                    particles[j].velx *= multiplier
                    particles[j].vely *= multiplier2
                    particles[j].vely *= multiplier2
                
                    """
                    old_vels[0] = particles[i].velx
                    old_vels[1] = particles[i].vely

                    old_vels[2] = particles[j].velx
                    old_vels[3] = particles[j].vely

                    overlap = (particles[i].rad+particles[j].rad) - get_distance(x1+particles[i].velx, x2+particles[j].velx, y1+(-particles[i].vely), y2+(-particles[j].vely))
                    vel1 = math.sqrt((particles[i].velx*particles[i].velx)+(particles[i].vely * particles[i].vely))
                    vel2 = math.sqrt((particles[j].velx*particles[j].velx)+(particles[j].vely * particles[j].vely))

                    totalvel = vel1+vel2
                    vel1_rat = vel1/totalvel
                    vel2_rat = vel2/totalvel
                    print("TOTAL VEL: ", totalvel, file=orig_stdout)
                    print("VEL1_RAT: ", vel1_rat, file=orig_stdout)

                    vel1_ov = vel1 - (vel1_rat*overlap)
                    vel2_ov = vel2 - (vel2_rat*overlap)

                    #print("Old velocity: ", vel1, file=orig_stdout)
                    #print("New velocity: ", vel2_ov, file=orig_stdout)

                    #TODO: The other scenarios in this conditional (including vely=0 and velx=0). Also need to do everything for particles 1
                    #TODO: Multiple particles, take the smallest timestep and do this operation on it

                    if particles[i].velx < 0 and particles[i].vely > 0:
                        ang1 = math.asin(particles[i].vely/vel1)
                        particles[i].velx = -(vel1_ov * math.cos(ang1))
                        particles[i].vely = (vel1_ov * math.sin(ang1))
                        #print("new x velocity: ", particles[i].velx, file=orig_stdout)
                        #print("new y velocity: ", particles[i].vely, file=orig_stdout)



                    if particles[j].vely < 0 and particles[j].velx > 0:
                        ang2 = math.acos(particles[j].vely/vel2)
                        particles[j].velx = vel2_ov * math.sin(ang2)
                        particles[j].vely = vel2_ov * math.cos(ang2)
                    elif particles[j].vely > 0 and particles[j].velx < 0:
                        ang2 = math.asin(particles[j].vely/vel2)
                        particles[j].velx = -(vel2_ov * math.cos(ang2))
                        particles[j].vely = vel2_ov * math.sin(ang2)




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


                    old_ind[0] = i
                    old_ind[1] = j
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


        if future_col:
            particles[old_ind[0]].velx = old_vels[0]
            particles[old_ind[0]].vely = old_vels[1]

            #print("old velx: ", old_vels[0], file=orig_stdout)
            #print("old vely: ", old_vels[1], file=orig_stdout)


            particles[old_ind[1]].velx = old_vels[2]
            particles[old_ind[1]].vely = old_vels[3]
            future_col = False

        if counter == 4:
            sleeper = 1
        #time.sleep(.01)

    sys.stdout.close()
    win.close()

main()
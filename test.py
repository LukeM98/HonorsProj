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


def collision(x1, x2, y1, y2, rad1, rad2):
    distance = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    if distance <= rad1 + rad2:
        return True
    else:
        return False


def main():
    orig_stdout = sys.stdout
    sys.stdout = open('output.txt', 'w')

    win = GraphWin("MyWindow", WIDTH, HEIGHT)

    colors = ['red', 'green', 'blue', 'yellow', 'black', 'white', 'orange', 'brown', 'purple', 'pink', 'teal', 'maroon', 'magenta', 'tan', 'gold', 'grey', 'cyan']
    # error with velocity 4 and 13
    particles = []
    n = 0
    j = 0

    num_timesteps = duration/timestep

    print(num_particles)
    print(num_timesteps)
    print()

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



    print()

   # particles.append(Particle(20, 0, 0,
       #                       Point(random.randint(0, WIDTH - RADIUS), random.randint(0, HEIGHT - RADIUS)), colors[j],
      #                        win, 4000))
   # particles.append(Particle(RADIUS, 0, 0,
    #                          Point(random.randint(0, WIDTH - RADIUS), random.randint(0, HEIGHT - RADIUS)), colors[j],
     #                         win, 1))

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

                if collision(x1, x2, y1, y2, particles[i].rad, particles[j].rad):
                    cir_oldvelx = particles[i].velx
                    cir2_oldvelx = particles[j].velx
                    particles[j].velx = ((
                                         particles[i].mass * cir_oldvelx + particles[j].mass * cir2_oldvelx) - cir2_oldvelx * particles[i].mass + cir_oldvelx * particles[i].mass) / (
                                        particles[i].mass + particles[j].mass)
                    particles[i].velx = particles[j].velx + cir2_oldvelx - cir_oldvelx
                    cir_oldvely = particles[i].vely
                    cir2_oldvely = particles[j].vely
                    particles[j].vely = ((
                                         particles[i].mass * cir_oldvely + particles[j].mass * cir2_oldvely) - cir2_oldvely * particles[i].mass + cir_oldvely * particles[i].mass) / (
                                        particles[i].mass + particles[j].mass)
                    particles[i].vely = particles[j].vely + cir2_oldvely - cir_oldvely

                c_sq = (x1-x2)*(x1-x2) + (y1-y2) * (y1-y2)
                x_dist = math.sqrt(c_sq - ((y1-y2)*(y1-y2)))
                y_dist = math.sqrt(c_sq - ((x1-x2)*(x1-x2)))

                distance = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

                force_grav = (G_CONST * particles[i].mass * particles[j].mass) / (distance*distance)

                p1_acel = force_grav/particles[i].mass
                p2_acel = force_grav/particles[j].mass

                p1_acelx = 0
                p2_acely = 0
                p1_acely = 0
                p2_acelx = 0

                if x1 > x2 and y1 < y2: # REPEAT THIS FOR OTHER 3 SCENARIOS
                    #p1_acel = - p1_acel

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
                elif x1 > x2 and y1 > y2:
                    deg1 = math.asin(y_dist / distance)
                    deg2 = math.asin(x_dist / distance)

                    p1_acely = (math.sin(deg1)) * p1_acel
                    p1_acelx = (math.cos(deg1)) * p1_acel

                    p2_acely = (math.cos(deg2)) * p2_acel
                    p2_acelx = (math.sin(deg2)) * p2_acel

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





                particles[i].velx = particles[i].velx + p1_acelx*timestep
                particles[j].velx = particles[j].velx + p2_acelx*timestep

                particles[i].vely = particles[i].vely + p1_acely * timestep
                particles[j].vely = particles[j].vely + p2_acely * timestep

        for i in range(num_particles):
            print(particles[i].get_Posx(), particles[i].get_Posy())
            particles[i].cir.move(particles[i].velx, -particles[i].vely)



        time.sleep(timestep)

    sys.stdout.close()
    win.close()

main()
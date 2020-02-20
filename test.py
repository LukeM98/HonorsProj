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
    """
    for i in range(num_particles):

        particles.append(Particle(RADIUS, random.randint(-11, 11), random.randint(-11, 11), Point(random.randint(0, WIDTH-RADIUS), random.randint(0, HEIGHT-RADIUS)), colors[j], win, 1))

        while particles[i].velx == 0 and particles[i].vely == 0:
            particles[i].velx = random.randint(-11, 11)
            particles[i].vely = random.randint(-11, 11)

        print(particles[i].rad, particles[i].get_Posx(), particles[i].get_Posy(), colors[j])

        #radius, posx, posy, color, mass
        j += 1
        if j >= len(colors):
            j = 0
"""
    particles.append(Particle(20, 0, 0,
                              Point(250, 250), colors[j],
                              win, 4000))
    particles.append(Particle(RADIUS, 0, 0,
                              Point(400, 400), colors[j],
                              win, 1))
    print()
    #cir = Particle(RADIUS, 5, 10, Point(250, 300), 'black', win, 1)
    #cir2 = Particle(RADIUS, 6, -8, Point(350, 200), 'red', win, 1)

    t_end = time.time() + duration
    x1_bool = False
    x1_bool2 = False
    x2_bool = False
    x2_bool2 = False
    counter = 0
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


       # print(cir.get_Posx())

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
                force_gravx = (G_CONST * particles[i].mass * particles[j].mass)/((x1-x2)*(x1-x2))
                force_gravy = (G_CONST * particles[i].mass * particles[j].mass)/((y1-y2)*(y1-y2))

                p1_acelx = force_gravx/particles[i].mass
                p2_acelx = force_gravx/particles[j].mass

                p1_acely = force_gravy / particles[i].mass
                p2_acely = force_gravy / particles[j].mass

                if x1 > x2 and y1 < y2:
                    p1_acelx = -p1_acelx
                    p1_acely = -p1_acely
                elif x1 < x2 and y1 < y2:
                    p2_acelx = -p2_acelx
                    p1_acely = -p1_acely
                elif x1 > x2 and y1 > y2:
                    p1_acelx = -p1_acelx
                    p2_acely = -p2_acely
                elif x1 < x2 and y1 > y2:
                    p2_acely = -p2_acely
                    p2_acelx = -p2_acelx
                    print("true", file=orig_stdout)
                # need scenarios where x and y = 0




                #print("x1: ", x1, file=orig_stdout)
                #print("y1: ", y1, file=orig_stdout)
                #print("x2: ", x2, file=orig_stdout)
                #print("y2: ", y2, file=orig_stdout)
                #print()
                particles[i].velx = particles[i].velx + p1_acelx*timestep
                particles[j].velx = particles[j].velx + p2_acelx*timestep

                particles[i].vely = particles[i].vely + p1_acely * timestep
                particles[j].vely = particles[j].vely + p2_acely * timestep

    #            print(particles[j].velx, "\n", file=orig_stdout)
     #           print(particles[j].velx, "\n", file=orig_stdout)



        for i in range(num_particles):
            print(particles[i].get_Posx(), particles[i].get_Posy())
            particles[i].cir.move(particles[i].velx, -particles[i].vely)


        counter += 1

        time.sleep(timestep)

    #win.getMouse()
    sys.stdout.close()
    win.close()

main()
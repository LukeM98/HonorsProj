from graphics import *
import time

WIDTH = 500
HEIGHT = 500


class Particle:
    rad = 0
    cir = 0

    def __init__(self, radius, pt, color, win):
        self.rad = radius
        self.cir = Circle(pt, self.rad)
        self.cir.setFill(color)
        self.cir.draw(win)

    def get_Posx(self):
        return self.cir.getCenter().getX()

    def get_Posy(self):
        return self.cir.getCenter().getY()


def main():
    f = open("output.txt", "r")
    f1 = f.readlines()
    win = GraphWin("MyWindow", WIDTH, HEIGHT)

    num_particles = int(f1[0])
    num_timesteps = float(f1[1])
    particles = []

    for i in range(num_particles):
        string = f1[i+3]
        str1 = string.split(' ')
        str2 = str1[3].split('\n')

        particles.append(Particle(int(str1[0]), Point(float(str1[1]), float(str1[2])), str2[0], win))


    counter = 4+num_particles
    for step in range(int(num_timesteps)):
        for i in range(num_particles):

            cords = f1[counter]
            counter += 1

            cords = cords.split(' ')
            posx = float(cords[0])

            cordsy = cords[1].split('\n')
            posy = float(cordsy[0])
            #print("X = ", posx)
            #print("Y = ", posy)
            difx = posx - particles[i].get_Posx()
            dify = posy - particles[i].get_Posy()
            particles[i].cir.move(difx, dify)

        time.sleep(.03)

    f.close()

    win.close()



main()
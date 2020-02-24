from graphics import *
import time
import keyboard


WIDTH = 500
HEIGHT = 500
rest = 0
speed = .03


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


def pause():
    global rest
    if rest:
        rest = False
    else:
        rest = True


def adjust_speed(number):
    global speed
    speed = number

def main():

    keyboard.add_hotkey(' ', lambda: pause())
    keyboard.add_hotkey('1', lambda: adjust_speed(1))
    keyboard.add_hotkey('2', lambda: adjust_speed(.5))
    keyboard.add_hotkey('3', lambda: adjust_speed(.03))
    print("HOTKEYS:\n SPACEBAR to pause\n 1 to make speed slowest\n 2 to make speed slow\n 3 to make speed  normal")
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

    counter = 4 + num_particles

    for step in range(int(num_timesteps)):
        if rest:
            while rest:
                time.sleep(.05)

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

        time.sleep(speed)

    f.close()

    win.close()



main()
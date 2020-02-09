from graphics import *
import time
import math
import random

WIDTH = 500
HEIGHT = 500
RADIUS = 40


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


def collision(x1, x2, y1, y2):
    distance = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    if distance <= RADIUS + RADIUS:
        return True
    else:
        return False


def main():

    win = GraphWin("MyWindow", WIDTH, HEIGHT)

    # error with velocity 4 and 13
    cir = Particle(RADIUS, 5, 10, Point(250, 300), 'black', win, 1)
    cir2 = Particle(RADIUS, 6, -8, Point(350, 200), 'red', win, 1)
    print("start")
    t_end = time.time() + 150
    x1_bool = False
    x1_bool2 = False
    x2_bool = False
    x2_bool2 = False
    while time.time() < t_end:
        y1 = cir.get_Posy()
        y2 = cir2.get_Posy()

        x1 = cir.get_Posx()
        x2 = cir2.get_Posx()

        if x1 >= WIDTH - cir.rad:
            if not x1_bool:
                cir.velx *= -1
                x1_bool = True
        else:
            x1_bool = False

        if x1 <= cir.rad:
            if not x1_bool2:
                cir.velx *= -1
                x1_bool2 = True
        else:
            x1_bool2 = False

        if y1 >= HEIGHT - cir.rad:
            cir.vely *= -1

        if y1 <= cir.rad:
            cir.vely *= -1

        if x2 >= WIDTH - cir2.rad:
            if not x2_bool:
                cir2.velx *= -1
                x2_bool = True
        else:
            x2_bool = False;

        if x2 <= cir2.rad:
            if not x2_bool2:
                cir2.velx *= -1
                x2_bool2 = True
        else:
            x2_bool2 = False

        if y2 >= HEIGHT - cir2.rad:
            cir2.vely *= -1

        if y2 <= cir2.rad:
            cir2.vely *= -1

       # print(cir.get_Posx())
        if collision(x1, x2, y1, y2):
            if cir.vely == 0 and cir2.vely == 0:
                cir_oldvelx = cir.velx
                cir2_oldvelx = cir2.velx
                cir2.velx = ((cir.mass*cir_oldvelx + cir2.mass*cir2_oldvelx) - cir2_oldvelx*cir.mass + cir_oldvelx*cir.mass)/(cir.mass + cir2.mass)
                cir.velx = cir2.velx+cir2_oldvelx-cir_oldvelx
                #print("new cir velx = ", cir.velx)
               # print("new cir vely = ", cir.vely)
               # print("new cir2 velx = ", cir2.velx)
                #print("new cir2 vely", cir2.vely)
               # print("")
            elif cir.velx == 0 and cir2.velx == 0:
                cir_oldvely = cir.vely
                cir2_oldvely = cir2.vely
                cir2.vely = ((cir.mass * cir_oldvely + cir2.mass * cir2_oldvely) - cir2_oldvely * cir.mass + cir_oldvely * cir.mass) / (
                                        cir.mass + cir2.mass)
                cir.vely = cir2.vely + cir2_oldvely - cir_oldvely

            else:
                cir_oldvelx = cir.velx
                cir2_oldvelx = cir2.velx
                cir2.velx = ((
                                         cir.mass * cir_oldvelx + cir2.mass * cir2_oldvelx) - cir2_oldvelx * cir.mass + cir_oldvelx * cir.mass) / (
                                        cir.mass + cir2.mass)
                cir.velx = cir2.velx + cir2_oldvelx - cir_oldvelx
                cir_oldvely = cir.vely
                cir2_oldvely = cir2.vely
                cir2.vely = ((
                                         cir.mass * cir_oldvely + cir2.mass * cir2_oldvely) - cir2_oldvely * cir.mass + cir_oldvely * cir.mass) / (
                                    cir.mass + cir2.mass)
                cir.vely = cir2.vely + cir2_oldvely - cir_oldvely
                """
                print("cirx = ", cir.get_Posx())
                print("ciry = ", cir.get_Posy())
                print("cir2x = ", cir2.get_Posx())
                print("cir2y = ", cir2.get_Posy())
                print("cir velx = ", cir.velx)
                print("cir vely = ", cir.vely)
                print("cir2 velx = ", cir2.velx)
                print("cir2 vely = ", cir2.vely)

                #radius = pow((cir.get_Posx() - cir2.get_Posx()), 2) + pow((cir.get_Posy()-cir2.get_Posy()), 2)
                radius = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
                vr = ((cir.velx-cir2.velx) * (cir.get_Posx() - cir2.get_Posx())) + ((cir.vely - cir2.vely) * (cir.get_Posy() - cir2.get_Posy()))
                print("vr = ", vr)
                impulse = (2*cir.mass*cir2.mass * vr)/(radius*(cir.mass+cir2.mass))
                print("impulse = ", impulse)
                impx = (impulse * (cir.get_Posx() - cir2.get_Posx()))/radius
                print("impx = ", impx)
                impy = (impulse * (cir.get_Posy() - cir2.get_Posy()))/radius
                print("impy = ", impy)
                oldvelx = cir.velx
                oldvely = cir.vely
                oldvelx2 = cir2.velx
                oldvely2 = cir2.vely

                cir.velx = oldvelx + impx/cir.mass
                cir.vely = oldvely + impy/cir.mass
                cir2.velx = oldvelx2 - impx/cir2.mass
                cir2.vely = oldvely2 - impy/cir2.mass
"""
                print("new cir velx = ", cir.velx)
                print("new cir vely = ", cir.vely)
                print("new cir2 velx = ", cir2.velx)
                print("new cir2 vely", cir2.vely)
                print("")

        cir.cir.move(cir.velx, -cir.vely)
        cir2.cir.move(cir2.velx, -cir2.vely)

        time.sleep(.1)

    #win.getMouse()
    win.close()

main()
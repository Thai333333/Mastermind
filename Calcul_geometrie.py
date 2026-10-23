from math import sqrt, pi

class Geometrie:
    def aire_carre (c):
        return c**2

    def aire_retangle(l,h):
        return l*h

    def aire_losange(d1,d2):
        return d1*d2

    def aire_triangle(b,h):
        return h*b

    def aire_disque(r):
        return pi*r**2

    def distance_entre_deux_points(xa,ya,xb,yb):
        return sqrt((xa-xb)**2+(ya-yb)**2)

    def norme(x,y):
        return sqrt(x**2+y**2)

    def pythagore(l_x, l_y):
        return sqrt(l_x**2 + l_y ** 2) 
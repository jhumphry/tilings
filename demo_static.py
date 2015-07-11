import os

from periodic_tiling2 import triangular_tiling, hexagonal_tiling
from periodic_tiling3 import cubic_tiling3, tetra_octa_tiling3
from matrix3 import rotate_x, rotate_y
from vector3 import Vector3
from restrict32 import restrict32
from tiling2_matplotlib import plot_matplotlib



def draw_cubic1_eps():

    def facecol((a, (r,g,b))):
        return (0.6 + (r%2)*0.2, 0.6 + (g%2)*0.2, 0.6 + (b%2)*0.2)

    m = rotate_x(0.75) * rotate_y(0.55)
    v = Vector3(0,0,-0.1)
    l3 = cubic_tiling3(((-6,6),(-6,6),(-6,6))).deform(m).translate(v)
    l2 = restrict32(l3).clip(-5,5,-5,5)
    with open("demos/cubic1.eps", "w") as f:
        l2.write_eps(f, (20,220,520,720), (-5,5,-5,5), facecol=facecol)

    
def draw_cubic2_eps():

    def edgecol(((i,), t)):
        if i==1:
            return (0.3, 0.0, 0.0)
        elif i==2:
            return (0.0, 0.3, 0.0)
        elif i==3:
            return (0.0, 0.0, 0.3)
        else:
            raise ValueError("The edge should lie in some direction")

    l3 = cubic_tiling3(((-2,2),(-2,2),(-2,2))).translate(Vector3(0,0,3))
    with open("demos/cubic2.eps", "w") as f:
        l3.write_eps(f, (0,0,500,500), (-1.5,5.7,-2.7,4.5),
                     whiterange=6, subdivs=25, edgecol=edgecol)


def draw_cubic1_matplotlib():

    m = rotate_x(0.75) * rotate_y(0.55)
    v = Vector3(0,0,-0.1)
    l3 = cubic_tiling3(((-6,6),(-6,6),(-6,6))).deform(m).translate(v)
    l2 = restrict32(l3)
    plot_matplotlib(l2).savefig("demos/cubic1.png")


def draw_tetra_octa_eps():

    def edgecol((s,t)):
        if s == "T1":
            return (1.0, 0.0, 0.0)
        elif s == "T2":
            return (0.0, 1.0, 0.0)
        elif s == "T3":
            return (0.0, 0.0, 1.0)
        elif s == "F1":
            return (0.0, 0.5, 0.5)
        elif s == "F2":
            return (0.5, 0.0, 0.5)
        elif s == "F3":
            return (0.5, 0.5, 0.0)
        else:
            raise ValueError("Should get one of those edge colours.")
        
    l3 = tetra_octa_tiling3(((-3,3),(-3,3),(-3,3))).clip(-3,3,-3,3,-3,3).scale(0.66).translate(Vector3(0,0,3))
    with open("demos/tetra_octa1.eps", "w") as f:
        l3.write_eps(f, (0,0,500,500), (-1.5,5.7,-2.7,4.5),
                     whiterange=6, subdivs=25, edgecol=edgecol)


def draw_triangular():

    def facecol((a,v)):
        if a:
            return (1.0,0.4,0.4)
        else:
            return (0.4,0.4,1.0)
    t = triangular_tiling(((-10,10),(-10,10))).clip(-8,8,-8,8)
    with open("demos/triangular.eps", "w") as f:
        t.write_eps(f,(0,0,500,500),(-8,8,-8,8),facecol=facecol)


def draw_hexagonal():

    def facecol((a,(i,j))):
        n = (i-j)%3
        if n==0:
            return (1.0,0.4,0.4)
        elif n==1:
            return (0.4,1.0,0.4)
        elif n==2:
            return (0.4,0.4,1.0)
    t = hexagonal_tiling(((-10,10),(-10,10))).clip(-8,8,-8,8)
    with open("demos/hexagonal.eps", "w") as f:
        t.write_eps(f,(0,0,500,500),(-8,8,-8,8),facecol=facecol)

        
        
if __name__=="__main__":

    if not os.path.exists("demos/"):
        os.makedirs("demos/")
    
    print "draw_cubic1_eps"
    draw_cubic1_eps()

    print "draw_cubic2_eps"
    draw_cubic2_eps()

    print "draw_cubic1_matplotlib"
    draw_cubic1_matplotlib()

    print "draw_tetra_octa_eps"
    draw_tetra_octa_eps()

    print "draw_triangular"
    draw_triangular()

    print "draw_hexagonal"
    draw_hexagonal()
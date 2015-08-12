from math import floor, ceil

from common import cycle
from vector2 import Vector2


class Tiling2():
    """
    Base class for a 2D tiling.
    """

    def __init__(self, v=None, e=None, f=None):
        if v is None:
            self.vertices = {}
        else:
            self.vertices = dict(v)
        if e is None:
            self.edges = {}
        else:
            self.edges = dict(e)
        if f is None:
            self.faces = {}
        else:
            self.faces = dict(f)

    def __repr__(self):
        return "Tiling2(%r, %r, %r)"%(self.vertices, self.edges, self.faces)

    def minx(self):
        return min(v.x for v in self.vertices)

    def maxx(self):
        return max(v.x for v in self.vertices)

    def miny(self):
        return min(v.y for v in self.vertices)

    def maxy(self):
        return max(v.y for v in self.vertices)

    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,(h(a),x))
                 for (a,x) in self.vertices.iteritems())
        e = dict((a,(frozenset(v[i][0] for i in a),x))
                 for (a,x) in self.edges.iteritems())
        f = dict((a,(frozenset(e[i][0] for i in a),x))
                 for (a,x) in self.faces.iteritems())
        return Tiling2(v.itervalues(),e.itervalues(),f.itervalues())

    def translate(self, offset):
        return self.deform(lambda x: x+offset)

    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def transform(self, matrix):
        return self.deform(matrix) # matrix action is overloaded function call

    def clip(self, minx, maxx, miny, maxy):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.iteritems() if minx <= v.x <= maxx and miny <= v.y <= maxy)
        newe = dict((e,x) for (e,x) in self.edges.iteritems() if any(v in newv for v in e))
        newf = dict((f,x) for (f,x) in self.faces.iteritems() if any(e in newe for e in f))
        return Tiling2(newv, newe, newf)

    def write_eps(self, f, psbox, geobox, facecol=lambda x:(1.0,1.0,1.0)):
        """
        Draw a picture in EPS format.

        Arguments:
         - f is a file object
         - psbox is the coordinates of the box in the output
           PostScript
         - geobox is the coordinates of the corresponding box in the
           Tiling2
         - facecol takes the label of a face, and returns the desired
           colour (in RGB format, between 0.0 and 1.0).

        Note that the order of the coordinates for psbox and geobox is
        different!
        """
        (gminx, gmaxx, gminy, gmaxy) = geobox
        (pminx, pminy, pmaxx, pmaxy) = psbox
        def coords(v):
            x = (v.x-gminx)*(pmaxx-pminx)/(gmaxx-gminx) + pminx
            y = (v.y-gminy)*(pmaxy-pminy)/(gmaxy-gminy) + pminy
            return "%f %f"%(x,y)
        f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        f.write("%%%%BoundingBox: %d %d %d %d\n"%psbox)
        for (face,x) in self.faces.iteritems():
            f.write("gsave %f %f %f setrgbcolor "%(facecol(x)))
            for (i,v) in enumerate(cycle(face)):
                f.write(coords(v))
                if i == 0:
                    f.write(" moveto ")
                else:
                    f.write(" lineto ")
            f.write("closepath fill grestore\n")
        for (v1,v2) in self.edges:
            f.write("newpath " + coords(v1) + " moveto " + coords(v2) + " lineto stroke\n")

    def face_count_information(self):
        polygon_count = {}
        for face in self.faces.keys():
            n = len(face)
            if n not in polygon_count.keys() :
                polygon_count[n] = 1
            else:
                polygon_count[n] += 1
        return polygon_count

    def face_count_information_print(self):
        for (k,v) in polygon_count(self).iteritems():
            print 'Number of %s_gons : %s.'%(k,v)

from vector3 import Vector3
from restrict32 import restrict32
from common import cycle

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
import numpy as np
import os

default_intersection_colours = ['lime', 'red', 'blue','aqua', 'orange', 'magenta','green','yellow',
                               'pink','purple','lightgreen','lightblue', 'gold', 'pink']

def tiling3_s_3d_subplot(tiling3_s, figure = False, number_of_rows = 1,number_of_columns = 1,position = 1,
                         colours = default_intersection_colours,
                      plane_z0_on = False, restrict32_intersection_on = False, tiling3_edges_on = True,
                      tiling3_faces_on = True,tiling3_edge_colours = ['black'],
                      axis_limit = False, elevation = 30, azimuth = 30,
                      save_name = 'tiling3_image', folder = 'demos/tiling3', save_on = True,
                      plane_z0_alpha = 0.2, restrict32_alpha = 0.8, tiling3_faces_alpha = 0.8, tiling3_edges_alpha = 0.8):
    '''
    This function is used to create 3D subplots for tiling3 objects.

        This function creates a 3D subplot that is able to produce images of :
    - a Tiling3 instance's edges and/or faces,
    - a Tiling2 instance's edges and faces on the plane z = 0,
    - the plane z = 0.

    Number of rows and number of columns determines how the figure is subdivided into equal areas
    and the position code decides which area the subplot is plotted in.

    To plot in the area in the i^{th} row and j^{th} the position code should be
    j + (i-1)*j .

    For example to plot in the top right quarter of a picture we use
    number_of_rows = 2, number_of_columns = 2, position_code = 1.
    '''


    if figure == False :
        figure = plt.figure()
    axis = plt.subplot(number_of_rows,number_of_columns,position, projection = '3d', aspect = 'equal')
    if axis_limit == False:
        bound = 0
        for tiling_3 in tiling3_s:
            if tiling_3.vertices:
                contender = max([abs(tiling_3.maxx()), abs(tiling_3.minx()),
                abs(tiling_3.miny()), abs(tiling_3.maxy()),
                abs(tiling_3.minz()), abs(tiling_3.maxz())])
                if contender > bound:
                    bound = contender
        axis_limit = [[-bound-1,bound+1]]*3
    polygon_tiles = []
    axis.grid(False)
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_zticks([])
    axis.set_axis_off()
    axis.set_xlim(axis_limit[0])
    axis.set_ylim(axis_limit[1])
    axis.set_zlim(axis_limit[2])
    axis.view_init(elevation,azimuth)
    lines = []
    x_s = []
    y_s = []
    z_s = []
    for (k,tiling3) in enumerate(tiling3_s):
        print k, tiling3_edge_colours[k%len(tiling3_edge_colours)]
        if tiling3_edges_on == True:
            for (j,face) in enumerate(tiling3.faces):
                for edge in list(face):
                    lines.append(axis.plot([],[],[],'',color = tiling3_edge_colours[k%len(tiling3_edge_colours)],
                                           alpha = tiling3_edges_alpha)[0])
                    vertex_1 = [list(edge)[0][1],list(edge)[0][2],list(edge)[0][3]]
                    vertex_2 = [list(edge)[1][1],list(edge)[1][2],list(edge)[1][3]]
                    x_s += [[vertex_1[0],vertex_2[0]]]
                    y_s += [[vertex_1[1],vertex_2[1]]]
                    z_s += [[vertex_1[2],vertex_2[2]]]
            for (j,line) in enumerate(lines):
                line.set_data(x_s[j],y_s[j])
                line.set_3d_properties(z_s[j])
        if tiling3_faces_on == True:
            for (j,face) in enumerate((tiling3).faces):
                polygon_tiles .append(axis.add_collection3d(Poly3DCollection([[(v.x,v.y,v.z) for v in cycle(face)]],
                facecolor = colours[(len(face)-3)%len(colours)],
                edgecolor  = tiling3_edge_colours[k%len(tiling3_edge_colours)],
                alpha = tiling3_faces_alpha)))
        if restrict32_intersection_on == True:
            for (j,face) in enumerate(restrict32(tiling3).faces):
                polygon_tiles .append(axis.add_collection3d(Poly3DCollection([[(v.x,v.y,0) for v in cycle(face)]],
                facecolor = colours[(len(face)-3)%len(colours)],
                edgecolor  = tiling3_edge_colours[k%len(tiling3_edge_colours)],alpha = restrict32_alpha)))
    if plane_z0_on == True:
        axis.add_collection3d(Poly3DCollection([[(axis_limit[0][0],axis_limit[1][0],0),(axis_limit[0][0],axis_limit[1][1],0),\
                                                 (axis_limit[0][1],axis_limit[0][1],0),(axis_limit[0][1],axis_limit[1][0],0)]],\
                                               facecolor = 'white',\
                                               edgecolor = 'black',alpha = plane_z0_alpha))
    if save_on:
        folder_name = os.path.join(folder)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        figure.savefig(folder+'/'+str(save_name)+'.png')
    return axis

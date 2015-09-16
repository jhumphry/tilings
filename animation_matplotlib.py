import os
import matplotlib.pyplot as plt

from polygon_count import *
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling2_matplotlib import tiling2_s_flattened_subplot
from data_line_matplotlib import line_plot_2d
from simultaneous_plot import simultaneous_plot
from restrict32 import restrict32
from progress import progressenumerate


def restriction_full_animation(list_of_tiling3_s, face_count_tiling='tiling3',
             common_colours=default_intersection_colours,
             save_name='tiling_image', folder='demos/tiling', save_on=True, figure_size=(20,10),

             tiling3_s_on=True, tiling3_s_number_of_rows=2, tiling3_s_number_of_columns=2, tiling3_s_position_code=1,
             plane_z0_on=False, restrict32_intersection_on=False, tiling3_edges_on=True,
             tiling3_faces_on=True, tiling3_edge_colours=['black'],
             tiling3_axis_limit=[[-2,2]]*3, elevation=40, azimuth=30,
             plane_z0_alpha=0.2, restrict32_alpha=0.8, tiling3_faces_alpha=0.8, tiling3_edges_alpha=0.8,

             tiling2_s_on=True, tiling2_s_number_of_rows=2, tiling2_s_number_of_columns=2, tiling2_s_position_code=2,
             tiling2_edge_colours=['black'], tiling2_limits=False, tiling2_alpha=0.8,
             data_lines_on=True, x_s=False,
             data_number_of_rows=2, data_number_of_columns=1, data_position_code=2,
             legend_on=True, marker_style='polygon',
             data_lines_x_label='Iteration',
             index_start=False, index_end=False):
    '''
    This function will take in list_of_tiling3_s and will make a
    simultaneous plot for each tiling3 with the tiling2 being the
    retrict32(tiling3) and the data_lines either being the number of
    faces on the tiling3 or the restrict32(tiling3) (determined by
    assigning the variable face_count_tiling='tiling2' or
    face_count_tiling='tiling3'.

    list_of_tiling3_s should be a list such that the i^{th} element is
    a single tiling3 object that you wish to display on the i^{th}
    frame.

    This function should be used to make animations that contain
    tiling3 objects as well as data lines and restrict32 projections.

    For animations that just require a tiling3 image it is recommended
    that the user uses tiling3_s_animation function instead.
    '''
    list_of_tiling2_s = [0]*len(list_of_tiling3_s)

    if tiling2_s_on or face_count_tiling == 'tiling2':
        list_of_tiling2_s = []
        for tiling3 in list_of_tiling3_s:
            list_of_tiling2_s.append(restrict32(tiling3))

    dictionary_of_dictionary_of_y_s = dict([(i,0) for i in range(len(list_of_tiling3_s))])
    for i in range(len(list_of_tiling3_s)):
        if data_lines_on:
            if face_count_tiling == 'tiling2':
                dictionary_of_dictionary_of_y_s[i] = list_of_dictionary_of_y_s_creater(list_of_tiling2_s)
                data_lines_y_label = 'Polyhedron 2D Cross-Section Polygon Count'
            elif face_count_tiling == 'tiling3':
                dictionary_of_dictionary_of_y_s[i] = list_of_dictionary_of_y_s_creater(list_of_tiling3_s)
                data_lines_y_label = 'Polyhedron Face Count'
        simultaneous_plot([list_of_tiling3_s[i]], [list_of_tiling2_s[i]], dictionary_of_dictionary_of_y_s[i], common_colours,
             "img%06d.png"%(i+1,), folder=folder, save_on=save_on, figure_size=figure_size,

             tiling3_s_on=tiling3_s_on,
             tiling3_s_number_of_rows=tiling3_s_number_of_rows, tiling3_s_number_of_columns=tiling3_s_number_of_columns, tiling3_s_position_code=tiling3_s_position_code,
             plane_z0_on=plane_z0_on, restrict32_intersection_on=restrict32_intersection_on, tiling3_edges_on=tiling3_edges_on,
             tiling3_faces_on=tiling3_faces_on, tiling3_edge_colours=tiling3_edge_colours,
             tiling3_axis_limit=tiling3_axis_limit, elevation=elevation, azimuth=azimuth,
             plane_z0_alpha=plane_z0_alpha, restrict32_alpha=restrict32_alpha, tiling3_faces_alpha=tiling3_faces_alpha, tiling3_edges_alpha=tiling3_edges_alpha,

             tiling2_s_on=tiling2_s_on,
             tiling2_s_number_of_rows=tiling2_s_number_of_rows, tiling2_s_number_of_columns=tiling2_s_number_of_columns, tiling2_s_position_code=tiling2_s_position_code,
             tiling2_edge_colours=tiling2_edge_colours, tiling2_limits=tiling2_limits, tiling2_alpha=tiling2_alpha,

             data_lines_on=data_lines_on, x_s=x_s,
             data_number_of_rows=data_number_of_rows, data_number_of_columns=data_number_of_columns, data_position_code=data_position_code,
             legend_on=legend_on, marker_style=marker_style,
             data_lines_x_label=data_lines_x_label, data_lines_y_label=data_lines_y_label,
             index_start=0, index_end=i+1)
    return None


def tiling3_s_animation(list_of_tiling3_s, figure=False,
                        tiling3_s_number_of_rows=2, tiling3_s_number_of_columns=2, tiling3_s_position_code=1,
                        colours=default_intersection_colours,
                        plane_z0_on=False, restrict32_intersection_on=False, tiling3_edges_on=True,
                        tiling3_faces_on=True, tiling3_edge_colours=['black'],
                        axis_limit=False, elevation=30, azimuth=30,
                        save_name='tiling3_image', folder='demos/tiling3animation', save_on=True,
                        plane_z0_alpha=0.2, restrict32_alpha=0.8, tiling3_faces_alpha=0.8, tiling3_edges_alpha=0.8,
                        print_progress=True):
    '''
    This function takes a list of lists of tiling3 objects,
    list_of_tiling3_s, and creates a tiling3_s_3d_subplot for each
    tiling3_s.

    This can be used to make quick animations of tiling3 objects.
    '''
    for (j, tiling3_s) in progressenumerate(list_of_tiling3_s, name=save_name, visible=print_progress):
        tiling3_s_3d_subplot(tiling3_s, figure,
                            tiling3_s_number_of_rows, tiling3_s_number_of_columns, tiling3_s_position_code,
                            colours, plane_z0_on, restrict32_intersection_on, tiling3_edges_on,
                            tiling3_faces_on, tiling3_edge_colours,
                            axis_limit, elevation, azimuth,
                            "img%06d.png"%(j+1,), folder, save_on,
                            plane_z0_alpha, restrict32_alpha, tiling3_faces_alpha, tiling3_edges_alpha)
    return None

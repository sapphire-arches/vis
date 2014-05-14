from numpy import cos, sin

def make_square(x, y, w, h, color):
    verts = []
    colors = [color] * 6
    verts += (x    , y    , 0)
    verts += (x + w, y    , 0)
    verts += (x    , y + h, 0)
    verts += (x + w, y    , 0)
    verts += (x + w, y + h, 0)
    verts += (x    , y + h, 0)
    return verts, colors

def _make_circle_point(theta, radius):
    return (cos(theta) * radius, sin(theta) * radius, 0)

def make_circle_segment(theta, dtheta, inner_radius, outer_radius, start_color, end_color):
    verts = []
    colors = []
    verts += _make_circle_point(theta         , inner_radius); colors += [start_color]
    verts += _make_circle_point(theta         , outer_radius); colors += [start_color]
    verts += _make_circle_point(theta + dtheta, inner_radius); colors += [end_color]
    verts += _make_circle_point(theta         , outer_radius); colors += [start_color]
    verts += _make_circle_point(theta + dtheta, inner_radius); colors += [end_color]
    verts += _make_circle_point(theta + dtheta, outer_radius); colors += [end_color]
    return verts, colors

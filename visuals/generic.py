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


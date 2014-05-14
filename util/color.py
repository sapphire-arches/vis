# Color management magics

# (hue, saturation, value)
def hsv_to_rgb(*color):
    # tuple/list support
    if len(color) == 1:
        color = color[0]
    # c = v * s
    c = color[2] * color[1]
    # h = h / 60
    h = (color[0] % 360) / 60.0
    # x = c(1 - abs(h mod 2 - 1))
    x = c * (1 - abs(h % 2 - 1))

    r = g = b = 0
    if 0 <= h < 1:
        r = c
        g = x
    elif 1 <= h < 2:
        r = x
        g = c
    elif 2 <= h < 3:
        g = c
        b = x
    elif 3 <= h < 4:
        g = x
        b = c
    elif 4 <= h < 5:
        r = x
        b = c
    else:
        r = c
        b = x
    # m = v - c
    m = color[1] - c
    r += m
    g += m
    b += m
    return (r, g, b)

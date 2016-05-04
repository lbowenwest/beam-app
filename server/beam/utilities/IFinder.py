from numpy import pi


def rectangle(width, height):
    return (width * height ** 3) / 12


def circle(radius):
    return (pi * radius ** 4) / 4


def i_beam(total_width, total_height, bar_width, bar_height):
    return rectangle(total_width, total_height) - rectangle(total_width - bar_width, total_height - 2 * bar_height)


def t_beam(total_width, total_height, bar_width, bar_height):
    a1 = total_width * bar_height
    a2 = bar_width * (total_height - bar_height)

    y_bar = ((a1 * (total_height - bar_height / 2)) + (a2 * (total_height - bar_height) / 2)) / (a1 + a2)

    I1 = rectangle(total_width, bar_height)
    I2 = rectangle(bar_width, (total_height - bar_height))

    # Parallel axis theorem
    I1 += a1 * ((total_height - bar_height / 2) - y_bar) ** 2
    I2 += a2 * ((total_height - bar_height) / 2 - y_bar) ** 2

    return I1 + I2


def c_beam(total_width, total_height, bar_width, bar_height):
    return rectangle(total_width, total_height) - rectangle(total_width - bar_width, total_height - 2 * bar_height)

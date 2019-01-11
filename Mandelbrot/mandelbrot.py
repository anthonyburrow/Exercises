import numpy as np
from multiprocessing import Pool
import itertools
from math import floor

from plotly.offline import plot
import plotly.graph_objs as go

from mypytools.math.complex import Complex


def CheckMandelbrot(re, im):
    z = Complex(re, im)

    # Not counting what is in the main cardioid or P-2 bulb
    # for memory management; only the boundaries are plotted
    if Cardioid(z):
        return False
    if P2Bulb(z):
        return False

    return EscapeTime(z)


def Cardioid(z):
    x = z.re
    y = z.im
    q = (x - 0.25)**2 + y**2
    # Should be <= but I am keeping the boundary
    P = q * (q + (x - 0.25)) < 0.25 * y**2

    return P


def P2Bulb(z):
    x = z.re
    y = z.im
    # p = np.sqrt((x - 0.25)**2 + y**2)

    # Should be <= but I am keeping the boundary
    P = (x + 1)**2 + y**2 < 0.0625

    return P


def EscapeTime(c, max_iter=500):
    iterate = 0
    z = Complex(0, 0)
    while iterate < max_iter:
        z = z**2 + c
        # if abs(z.re) > 2 or abs(z.im) > 2:
        if z.re**2 + z.im**2 > 4:
            return False
        iterate += 1

    return True


def CheckRow(rPoints, im):
    row = []
    prev = None
    for re in rPoints:
        z = (re, im)
        is_mandelbrot = CheckMandelbrot(*z)
        if prev is None:
            if is_mandelbrot:
                row.append(z)
            prev = (z, is_mandelbrot)
            continue
        if prev[1] == is_mandelbrot:
            continue

        if is_mandelbrot:
            row.append(z)
        else:
            row.append(prev[0])
        prev = (z, is_mandelbrot)

    return row


def main():
    print('Setting up domain to check...')

    # Image
    image_dim = (1920, 1080)
    axis_imag = (-1.25, 1.25)
    axis_real_upper = 0.8
    axis_real = (axis_real_upper - (image_dim[0] / image_dim[1]) *
                 (axis_imag[1] - axis_imag[0]), axis_real_upper)

    iRange = (0, axis_imag[1])
    rRange = axis_real

    scale = 1
    rPoints = np.linspace(*rRange, image_dim[0] * scale, endpoint=False)
    iPoints = np.linspace(*iRange, floor(image_dim[1] * scale / 2),
                          endpoint=False)

    print('Checking domain for Mandelbrot points...')

    with Pool(processes=6) as pool:
        mandelbrot_set = pool.starmap(CheckRow, zip(itertools.repeat(rPoints),
                                                    iPoints))

    # Plotting
    print('Plotting data...')

    x = [x[0] for rw in mandelbrot_set for x in rw]
    y = [x[1] for rw in mandelbrot_set for x in rw]

    trace1 = go.Scattergl(mode='markers', x=x, y=y,
                          marker=dict(color='#3a3a3a', size=1),
                          showlegend=False)

    y = [-x[1] for rw in mandelbrot_set for x in rw]

    trace2 = go.Scattergl(mode='markers', x=x, y=y,
                          marker=dict(color='#3a3a3a', size=1),
                          showlegend=False)

    data = [trace1, trace2]
    layout = go.Layout(
        xaxis=dict(
            range=axis_real,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            range=axis_imag,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename='mandelbrot.html')


if __name__ == '__main__':
    main()

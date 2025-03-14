import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def plot_polynomial_growth(n, max_x):
    data = [i for i in poly_values(max_x)]
    x = [i[0] for i in data]
    y1 = [i[1] for i in data]
    y2 = [i[2] for i in data]
    y3 = [i[3] for i in data]

    fig, axes = plt.subplots(1, 3, figsize=(15,5))
    fig.suptitle("Polynomical Growth Comparison")
    axes[0].plot(x, y1)
    axes[0].set_title("x^2")

    axes[1].plot(x, y2)
    axes[1].set_title("x^3")

    axes[2].plot(x, y3)
    axes[2].set_title("x^4")

    vline = [None, None, None]
    for i in range(3):
        axes[i].set_xlabel("x")
        axes[i].set_ylabel("y")
        axes[i].set_yscale('log')
        axes[i].grid(True)
        vline[i] = axes[i].axvline(n, color='r', linestyle="--")

    # Slider
    plt.subplots_adjust(bottom=0.25) # Make room for slider
    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03]) # left bottom width height
    slider = Slider(ax=slider_ax, label="x-value", valmin=0, valmax=max_x, valinit=n)

    def update(val):
        for i in range(3):
            vline[i].set_xdata([val, val]) # move vertical line
        fig.canvas.draw_idle() # Redraw

    slider.on_changed(update)
    

    plt.show()

         



def poly_values(max_x):
    """Generator to yield 100 x values and their coresponding polynomial values (x**2, x**3, x**4) from 0 up to max_x."""
    x = 0
    while x <= max_x:
        yield (x, x**2, x**3, x**4)
        x += max_x / 100








plot_polynomial_growth(3, 10)

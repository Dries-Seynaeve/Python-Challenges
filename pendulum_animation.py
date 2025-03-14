import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import numpy as np

def plot_pendulum_motion(max_t, length, gravity, initial_angle):
    global x, y, ani, period

    period = 2*np.pi*np.sqrt(length/gravity)
    data = list(pendulum_motion(max_t, length, gravity, initial_angle))
    t = [i[0] for i in data]
    x = [i[1] for i in data]
    y = [i[2] for i in data]


    fig, ax = plt.subplots(figsize=(8,8))
    
    plt.scatter([0], [0], color="blue", s=100)
    pendulum = plt.scatter([x[0]], [y[0]], color="red", s=200)
    line, = plt.plot([0, x[0]], [0, y[0]], linestyle="-", color="red")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3.3, 0)
    ax.set_aspect('equal')
    ax.grid(True)


    # Add the animation
    def update_animation(frame):
        ax.set_title(f"Pendulum: t = {t[frame]:.2f}, period = {period:.1f}")
        pendulum.set_offsets(np.c_[x[frame], y[frame]])
        line.set_xdata([0, x[frame]])
        line.set_ydata([0, y[frame]])
        return pendulum, line

    ani = FuncAnimation(fig, update_animation, frames=range(len(x)), interval=50)

    # Add the Slider
    plt.subplots_adjust(bottom=.25)
    l_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    g_slider_ax = plt.axes([0.2, 0.125, 0.6, 0.03])
    a_slider_ax = plt.axes([0.2, 0.2, 0.6, 0.03])

    l_slider = Slider(ax=l_slider_ax, label="length", valmin=1, valmax=3, valinit=length)
    g_slider = Slider(ax=g_slider_ax, label="gravity", valmin=5, valmax=15, valinit=gravity)
    a_slider = Slider(ax=a_slider_ax, label="initial angle", valmin=-1, valmax=1, valinit=initial_angle)

    def update_slider(val):
        global t, x, y, ani, period
        period = 2*np.pi*np.sqrt(l_slider.val/g_slider.val)
        data = list(pendulum_motion(max_t, l_slider.val, g_slider.val, a_slider.val))
        t = [i[0] for i in data]
        x = [i[1] for i in data]
        y = [i[2] for i in data]

        ani.event_source.stop()
        ani = FuncAnimation(fig, update_animation, frames=range(len(x)), interval=50)
        fig.canvas.draw_idle()

    l_slider.on_changed(update_slider)
    g_slider.on_changed(update_slider)
    a_slider.on_changed(update_slider)



    plt.show()



def pendulum_motion(max_t, length, gravity, initial_angle):
    """Generate the position of the pendulum as a function of time"""
    t = 0
    dt = 0.05
    
    theta = initial_angle  # angle of the pendulum
    omega = 0              # angular velocitiy
    while t <= max_t:
        x = length * np.sin(theta)
        y = - length * np.cos(theta)
        yield t, x, y, theta

        omega += - gravity * np.sin(theta) * dt / length
        theta += omega * dt
        t += dt




if __name__ == "__main__":
    plot_pendulum_motion(10, 1.0, 9.8, 0.5)

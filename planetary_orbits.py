import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


def plot_planetary_orbits(max_t, mass_planet, mass_star, distance, eccentricity):
    data = list(get_planet_positions(max_t, mass_planet, mass_star, distance, eccentricity))
    global x, y, ani, period
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    t = [i[2] for i in data]
    period = 2*np.pi*np.sqrt(distance**3 / mass_star)


    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')
    ax.grid(True)

    plt.scatter([0], [0], color="yellow", label="Star", s=200)
    planet = ax.scatter([x[0]], [y[0]], s=50, c="blue", label="Planet")


    def update_animation(frame):
        ax.set_title(f"Planet around Star: t = {t[frame]:.2f}, period: {period:.1f}")
        planet.set_offsets(np.c_[x[frame], y[frame]])
        return planet,

    ani = FuncAnimation(fig, update_animation, frames=range(len(x)), interval=50)

    # Add the sliders
    plt.subplots_adjust(bottom=0.25)
    d_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    e_slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    m_slider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])

    d_slider = Slider(ax=d_slider_ax, label="initial distance", valmin=5, valmax=15, valinit=distance)
    e_slider = Slider(ax=e_slider_ax, label="eccentricity", valmin=0, valmax=0.99, valinit=eccentricity)
    m_slider = Slider(ax=m_slider_ax, label="Star Mass", valmin=500, valmax=1500, valinit=mass_star)


    def update_slider(val):
        global ani, data, x, y, period # Reset animation
        period = 2*np.pi*np.sqrt(d_slider.val**3 / m_slider.val) 
        data = list(get_planet_positions(max_t, mass_planet, m_slider.val, d_slider.val, e_slider.val))
        
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        ani.event_source.stop()
        ani = FuncAnimation(fig, update_animation, frames=range(len(x)))
        fig.canvas.draw_idle()



    e_slider.on_changed(update_slider)
    d_slider.on_changed(update_slider)
    m_slider.on_changed(update_slider)
    ax.legend()
    plt.show()
        




def get_planet_positions(max_t, mass_planet, mass_star, distance, eccentricity):
    """"Generate the star position, we assume during the orbit the position of the
    star remains the same ea. the mass_star >>>> mass_planet."""
    
    t = 0
    dt = 0.1

    x = distance
    y = 0

    vx = 0
    vy = np.sqrt(mass_star*(1-eccentricity)/distance)

    while t <= max_t:
        yield x, y, t

        # Update the acceleration based on the new position
        r = np.sqrt(x**2+y**2)

        ax = - mass_star * x / (r**3)
        ay = - mass_star * y / (r**3)

        # Update the position and velocity for the next timestep
        vx += ax*dt
        vy += ay*dt

        x += vx*dt
        y += vy*dt

        t += dt



if __name__ == "__main__":
    plot_planetary_orbits(20, 1.0, 1000, 10, 0)


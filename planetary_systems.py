import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import itertools

class PlanetarySystem:
    def __init__(self, planets_data, star_mass=1000):
        self.planets = [{'mass': m, 'distance': d} for m, d in planets_data]
        self.n = len(planets_data)
        self.Ms = star_mass
        self.G = 1.0
        self.base_dt = 0.1
        self.time_scale = 1.0
        self.t = 0
        self.thetas = np.zeros(self.n)  # Initial angles
        self.xs = []
        self.ys = []

    def orbit_generator(self):
        # Yield list of [x, y] positions forever
        while True:
            x, y = np.array([(p["distance"] * np.cos(t), p["distance"] * np.sin(t)) for p, t in zip(self.planets, self.thetas)]).T
            if len(self.xs) == 50:
                self.xs.pop(0)
                self.ys.pop(0)
                
            self.xs.append(x)
            self.ys.append(y)

            yield x, y
            dt = self.base_dt * self.time_scale
            distance = np.array([p['distance'] for p in self.planets])

            self.thetas += np.sqrt(self.G * self.Ms) * distance**-1.5 * dt
            self.t += dt

    def reset(self):
        self.xs = []
        self.ys = []
        self.thetas = np.zeros(self.n)
        self.t = 0


def plot_planetary_system(max_t, planets_data):
    global planets
    system = PlanetarySystem(planets_data)
    planets = system.orbit_generator()
    fig, ax = plt.subplots(figsize=(8,8))
    
    # Initialize star and planet scatters
    [x, y] = next(planets)
    colors = list(itertools.islice(["red", "blue", "green"], len(planets_data)))
    xs = np.array(system.xs).T
    ys = np.array(system.ys).T
    trails = []

    ax.set_title(f"Planetary System: t={system.t}, Planets = {system.n}")
    ax.scatter([0], [0], s=500, color="yellow", label="Star")
    scatter_planet = ax.scatter(x, y, s=[50*p[0] for p in planets_data], color=colors)
    for c, (x, y) in zip(colors, zip(xs, ys)):
        trails.append(plt.plot(x, y, color=c, alpha=0.2)[0])

    
    def update(frame):
        # Consume generator, update scatters
        x, y = next(planets)
        xs = np.array(system.xs).T
        ys = np.array(system.ys).T
        ax.set_title(f"Planetary System: t={system.t:.2f}, Planets = {system.n}")
        scatter_planet.set_offsets(np.c_[x, y])
        for i, (x, y) in enumerate(zip(xs, ys)):
            trails[i].set_data(x, y)
        if system.t > max_t:
            system.reset()
        return scatter_planet


    ani = FuncAnimation(fig, update, frames=10000)
    
    # Add sliders for Ms and time_scale
    plt.subplots_adjust(bottom=0.25)
    ms_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    ts_slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])

    ms_slider = Slider(ax=ms_slider_ax, valmin=500, valmax=1500, valinit=system.Ms, label="Stellar Mass")
    ts_slider = Slider(ax=ts_slider_ax, valmin=0.1, valmax=2., valinit=system.time_scale, label="Time Scale")

    def update_slider(val):
        system.Ms = ms_slider.val
        system.time_scale = ts_slider.val
        

    ms_slider.on_changed(update_slider)
    ts_slider.on_changed(update_slider)

    
    # Set limits, labels, show
    ax.set_xlabel("Distance (units)")
    ax.set_ylabel("Distance (units)")
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.grid(True)
    plt.show()



if __name__ == "__main__":
    plot_planetary_system(50, [(1, 5), (2, 10), (3, 15)])


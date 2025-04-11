import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import itertools


class EvolvingSystem():
    def __init__(self, planets_data):
        self.planets = [GrowingPlanet(m, d) if t == "grow" else
                        ShrinkingPlanet(m,d) if t == "shrink" else
                        Planet(m,d) for (t,m,d) in planets_data]
        self.dt = 0.1
        self.time_scale = 1
        self.time = 0
        self.paths = [[] for p in self.planets]
        self.Ms = 1000


    def reset(self):
        # Reset the system to how it started
        self.time = 0
        self.paths = [[] for p in self.planets]
        for planet in self.planets:
            planet.reset()


    def update_system(self):
        # Get generator that generates the positions of the planets for every timestep
        while True:

            self.time += self.time_scale * self.dt
            positions = [planet.update(self.time_scale * self.dt, self.Ms) for planet in self.planets]

            # Add the positons to the paths
            for path, pos in zip(self.paths, positions):
                path.append(pos)


            if len(self.paths[0]) > 50:
                (path.pop(0) for path in self.paths)

            # Yield the positons
            yield np.array(positions)

    def get_planet_masses(self):
        return np.array([planet.mass for planet in self.planets])

    def set_star_mass(self, Ms):
        self.Ms = Ms
            
    def set_time_scale(self, ts):
        self.time_scale = ts

    def get_paths(self):
        return self.paths

        

    




class Planet():
    def __init__(self, mass, distance):
        # Constructor of the Planet class
        self.mass = mass
        self.distance = distance
        self.theta = 0
        self.G = 1

    def update(self, dt, Ms):
        """Get the positions of the planet"""
        x = self.distance * np.cos(self.theta)
        y = self.distance * np.sin(self.theta)

        self.theta += np.sqrt(self.G * Ms / self.distance**3) * dt
        return np.array([x, y])

    def reset(self):
        self.theta = 0



class GrowingPlanet(Planet):
    def __init__(self, mass, distance):
        self.m_init = mass
        super().__init__(mass, distance)

    def update(self, dt, Ms):
        # Update changes the mass 
        self.mass += 0.01*dt
        return super().update(dt, Ms)

    def reset(self):
        # Reset should also reset the mass
        self.mass = self.m_init
        super().reset()
            

class ShrinkingPlanet(Planet):
    def __init__(self, mass, distance):
        self.d_init = distance
        super().__init__(mass, distance)

    def update(self, dt, Ms):
        # Update changes the distance
        self.distance -= 0.1*dt
        return super().update(dt, Ms)

    def reset(self):
        # Reset also resets the distance
        self.distance = self.d_init
        super().reset()




def plot_evolving_system(max_t, planets_data):
    system = EvolvingSystem(planets_data)
    positions = system.update_system()
    masses = system.get_planet_masses()
    colors = list(itertools.islice(["red", "blue", "green"], len(planets_data)))


    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter([0], [0], s=500, color="yellow") # Sun 
    
    ax.set_title(f"Planetary System: t = {system.time:.2f}, Planets = {len(planets_data)}")
    current_positions = next(positions) # Positions of the planets
    [x, y] = current_positions.transpose()

    planet_scatter = ax.scatter(x, y, s=50*masses, color=colors)
    planet_paths = []

    paths = system.get_paths()

    for color, path in zip(colors, paths):
        [x, y] = np.array(path).transpose()
        planet_paths.append(ax.plot(x, y, color=color, alpha=0.2)[0])


    def update_frame(frame):
        current_positions = next(positions)  # Position of the planets
        masses = system.get_planet_masses()
        [x, y] = current_positions.transpose()
        planet_scatter.set_offsets(np.c_[x, y])
        planet_scatter.set_sizes(50*masses)

        ax.set_title(f"Planetary System: t = {system.time:.1f}, Planets = {len(planets_data)}")

        paths = system.get_paths()

        for planet_path, path in zip(planet_paths, paths):
            [x,y] = np.array(path).transpose()
            planet_path.set_data(x, y)

        if system.time >= max_t:
            system.reset()

        return [planet_scatter] + planet_paths

    
    ani = FuncAnimation(fig, update_frame, frames=range(int(max_t/(system.dt * system.time_scale))), interval=50, blit=False)

    plt.subplots_adjust(bottom=0.2)
    m_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    t_slider_ax = plt.axes([0.2, 0.12, 0.6, 0.03])

    m_slider = Slider(ax=m_slider_ax, valmin=500, valmax=1500, valinit=1000 ,label="Star Mass")
    t_slider = Slider(ax=t_slider_ax, valmin=0.1, valmax=2, valinit=1 ,label="Time Scale")

    def update_slider(val):
        system.set_star_mass(m_slider.val)
        system.set_time_scale(t_slider.val)


    m_slider.on_changed(update_slider)
    t_slider.on_changed(update_slider)


    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xlabel("Distance (units)")
    ax.set_ylabel("Distance (units)")

    plt.show()


if __name__ == "__main__":
    plot_evolving_system(50, [("grow", 1, 5), ("shrink", 2, 10)])

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

G = 1



class Planet():
    def __init__(self, mass_star, distance, eccentricity):

        self.d = distance
        self.e = eccentricity
        self.s_mass = mass_star

        self.t = 0
        self.theta = 0

        

    def update(self):
        self.t += 0.1
        self.theta += np.sqrt(G* self.s_mass / self.d**3)*0.1

    def reset(self):
        self.t = 0
        self.theta = 0
        

    def get_positions(self):
        return self.d*np.cos(self.theta), self.d*np.sqrt(1 - self.e**2)*np.sin(self.theta), 0

    def get_orbit(self):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.d * np.cos(theta)
        y = self.d * np.sqrt(1 - self.e**2) * np.sin(theta)
        z = np.zeros_like(theta)
        return x, y, z

    




def plot_3d_orbit(max_t, mass_star, distance, eccentricity):
    global x_path, y_path, z_path, planet_scatter
    planet = Planet(mass_star, distance, eccentricity)

    fig = plt.figure()
    ax  = fig.add_subplot(projection='3d')
    
    ax.scatter(0, 0, 0, color="yellow", s=500)
    x, y, z = planet.get_positions()
    x_orbit, y_orbit, z_orbit = planet.get_orbit()

    planet_scatter = ax.scatter(x, y, z, color="blue")
    path_traveld, = ax.plot(x_orbit, y_orbit, z_orbit, color="blue", alpha=0.3)


    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)
    ax.set_xlabel("Distance (units)")
    ax.set_ylabel("Distance (units)")
    ax.set_zlabel("Distance (units)")
    ax.set_title(f"Orbit t: {planet.t:.1f}, period: {(2 * np.pi * np.sqrt(planet.d**3) / (G*mass_star)):.2f}")
    ax.set_box_aspect([1,1,1])

    # Add the animation
    def update_animation(frame):
        global planet_scatter
        if planet.t >= max_t:
            planet.reset()
        else:
            planet.update()

        planet_scatter.remove()
        x, y, z = planet.get_positions()
        planet_scatter = ax.scatter(x, y, z, color="blue")

        ax.set_title(f"Orbit t: {planet.t:.1f}, period: {(2 * np.pi * np.sqrt(planet.d**3) / (G*planet.s_mass)):.2f}")
        return planet_scatter

    
    ani = FuncAnimation(fig, update_animation, frames=int(max_t/0.1))

    # Add the sliders
    plt.subplots_adjust(bottom=0.25)
    m_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    m_slider = Slider(ax=m_slider_ax, valmin=500, valmax=1500, valinit=mass_star, label="Star Mass")
    d_slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    d_slider = Slider(ax=d_slider_ax, valmin=5, valmax=15, valinit=distance, label="Distance")
    e_slider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])
    e_slider = Slider(ax=e_slider_ax, valmin=0, valmax=0.9, valinit=eccentricity, label="eccentricity")

    def update_slider(val):
        global planet_scatter
        planet.d = d_slider.val
        planet.e = e_slider.val
        planet.s_mass = m_slider.val
        planet.update()

        x_orbit, y_orbit, z_orbit = planet.get_orbit()
        path_traveld.set_data_3d(x_orbit, y_orbit, z_orbit)

        planet_scatter.remove()
        x, y, z = planet.get_positions()
        planet_scatter = ax.scatter(x, y, z, color="blue")

    d_slider.on_changed(update_slider)
    e_slider.on_changed(update_slider)
    m_slider.on_changed(update_slider)
    


    plt.show()



if __name__ == "__main__":
    plot_3d_orbit(20, 1000, 10, 0.5)

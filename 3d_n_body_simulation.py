import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

epsilon = 0.1


class NbodySystem():
    def __init__(self, n_bodies, masses, positions, velocities):
        self.masses = np.array(masses, dtype="float64")
        self.n = n_bodies

        self.time = 0
        self.G = 1.0
        self.base_dt = 0.01
        self.time_scale = 1.0

        self.positions = [np.array(positions, dtype="float64")]
        self.init_p = np.array(positions, dtype="float64").copy()
        self.velocities = np.array(velocities, dtype="float64")
        self.init_v = np.array(velocities, dtype="float64").copy()






    def get_acceleration(self, positions):
        """Returns the acceleration that all particles feel"""
        pos = np.array(positions[-1])
        acc = np.zeros_like(pos)

        for idx in range(self.n):
            r = pos - pos[idx]  # Shape: (n, 3)
            r_norm = np.linalg.norm(r, axis=1) + epsilon
            mask = r_norm != epsilon # Avoid self-interaction
            r_unit = r / r_norm[:, np.newaxis]**3 # Shape: (n, 3)

            acc[idx] = np.sum(self.G * self.masses[:, np.newaxis] * r_unit * mask[:, np.newaxis], axis=0)

        return acc








    def get_energy(self):
        """Compute total energy (kinetic + potential)"""
        kinnetic = 0.5*np.sum(self.masses * np.sum(self.velocities**2, axis=1))

        pos = self.positions[-1]

        # Vectorize potential
        idx = np.triu_indices(self.n, k=1)
        r = pos[idx[0]] - pos[idx[1]] # Pairwise differences
        r_norm = np.linalg.norm(r, axis=1) + epsilon

        potential = -self.G * np.sum(self.masses[idx[0]] * self.masses[idx[1]] / r_norm)
        return kinnetic + potential 
        




    def reset(self):
        """Reset simulation"""
        self.velocities = self.init_v.copy()
        self.positions = [self.init_p.copy()]
        self.time = 0
        

    def update(self):
        """Update the state of the N bodies"""
        dt = self.base_dt * self.time_scale
        self.time += dt
        
        # Update velocities
        self.velocities +=  self.get_acceleration(self.positions)*dt

        # Update positions
        pos = self.positions[-1] + self.velocities * dt
        self.positions.append(pos)
        if len(self.positions) > 50:
            self.positions.pop(0)

def plot_3d_nbody(max_t, n_bodies, masses, positions, velocities):
    system = NbodySystem(n_bodies, masses, positions, velocities)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection='3d')
    colors = ["red", "blue", "green"]

    # Plot the bodies
    x, y, z = system.positions[-1].T
    scatters = []
    trails = []
    
    for i in range(n_bodies):
        scatters.append(ax.scatter(x[i], y[i], z[i], s=masses[i]*50, color=colors[i % len(colors)]))
        trails.append(ax.plot(x[i], y[i], z[i], color=colors[i % len(colors)], alpha=0.2)[0])

    # Let's define the animation
    def update_animation(frame):
        system.update()
        x, y, z = system.positions[-1].transpose()
        xs = np.array([p[:, 0] for p in system.positions]).transpose()
        ys = np.array([p[:, 1] for p in system.positions]).transpose()
        zs = np.array([p[:, 2] for p in system.positions]).transpose()


        for i in range(n_bodies):
            scatters[i].remove()
            scatters[i] = ax.scatter(x[i], y[i], z[i], s=masses[i]*50, color=colors[i % len(colors)])
            trails[i].set_data_3d(xs[i], ys[i], zs[i])

        ax.set_title(f"N-Body: t = {system.time:.2f}, Energy = {system.get_energy():.2f}")
        if system.time > max_t:
            system.reset()
        return scatters + trails,

    ani = FuncAnimation(fig, update_animation, frames=range(5000), blit=False)

    # Add the Slider
    plt.subplots_adjust(bottom=0.25)
    g_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    t_slider_ax = plt.axes([0.2, 0.10, 0.6, 0.03])

    g_slider = Slider(ax=g_slider_ax, valmin=0.5, valmax=2., valinit=1., label="Gravity Strength")
    t_slider = Slider(ax=t_slider_ax, valmin=0.1, valmax=2.0, valinit=1, label="Time scale")

    def update_slider(val):
        system.G = g_slider.val
        system.time_scale = t_slider.val

    t_slider.on_changed(update_slider)
    g_slider.on_changed(update_slider)

    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)

    ax.set_xlabel("Distance (units)")
    ax.set_ylabel("Distance (units)")
    ax.set_zlabel("Distance (units)")
    plt.show()


if __name__ == "__main__":
    plot_3d_nbody(50, 3, [5, 3, 2], [[0, 0, 0], [5, 0, 0], [0, 5, 0]], [[0, 0, 0], [0, 1, 0], [-1, 0, 0]])




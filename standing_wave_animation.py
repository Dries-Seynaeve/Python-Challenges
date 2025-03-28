import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider



class Wave():
    def __init__(self, max_t, tension, density, amplitude):
        if max_t <= 0:
            raise ValueError("max_t should be strictly positive")
        else:
            self.max_t = max_t
        if tension < 50 or tension > 150:
            raise ValueError("tension should be between 50N and 150N.")
        else:
            self.tension = tension
        if 0.1 > density or 0.5 < density:
            raise ValueError("density should be between 0.1kg/m and 0.5kg/m")
        else:
            self.density = density
        if 0.5 > amplitude or 2 < amplitude:
            raise ValueError("amplitude should be between 0.5m and 2m")
        else:
            self.amplitude = amplitude
        self.t = 0
        self.dt = 0.1
        self.x = np.arange(0, 20.1, 0.1)
        self.k = 2 * np.pi / 10
        self.update_wave()


    def update_wave(self):
        c = self.get_speed()
        omega = self.k * c
        self.y = self.amplitude * np.sin(self.k * self.x - omega * self.t)
        self.speed = c

    def increase_time(self):
        self.t += self.dt

    def get_speed(self):
        return np.sqrt(self.tension / self.density)

    def set_tension(self, tension):
        self.tension = tension

    def set_density(self, density):
        self.density = density

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude
        






def plot_wave_propagation(max_t, tension, density, amplitude):
    wave = Wave(max_t, tension, density, amplitude)

    # Get an inition plot
    fig, ax = plt.subplots()
    wave_figure, = ax.plot(wave.x, wave.y, 'b-')

    # Set up the animation
    def update_animation(frame):
        wave.increase_time()
        wave.update_wave()
        speed = wave.get_speed()
        ax.set_title(f"Wave: t = {wave.t:.1f} s, Speed = {speed:.2f}")
        wave_figure.set_ydata(wave.y)
        return wave_figure, 

    ani = FuncAnimation(fig, update_animation, frames=range(1000), interval=50)
    
    # Add the sliders
    plt.subplots_adjust(bottom=0.25)
    t_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    t_slider    = Slider(ax=t_slider_ax, valmin=50, valmax=150, valinit=tension, label="tension")
    d_slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    d_slider    = Slider(ax=d_slider_ax, valmin=0.1, valmax=0.5, valinit=density, label="density")
    a_slider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])
    a_slider    = Slider(ax=a_slider_ax, valmin=0.5, valmax=2, valinit=amplitude, label="amplitude")

    def update_slider(val):
        wave.set_amplitude(a_slider.val)
        wave.set_density(d_slider.val)
        wave.set_tension(t_slider.val)
        wave.update_wave()

    t_slider.on_changed(update_slider)
    d_slider.on_changed(update_slider)
    a_slider.on_changed(update_slider)


    # Finish setting up the figure
    ax.set_ylim(-2, 2)
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Displacement (m)")
    ax.set_title(f"Wave: t = {0} s, Speed = {wave.get_speed()}")
    ax.grid(True)
    plt.show()






if __name__ == "__main__":
    plot_wave_propagation(10, 100, 0.2, 1.0)

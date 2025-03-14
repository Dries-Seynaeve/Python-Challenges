import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import exp, cos, sin, pi



def plot_harmonic_oscillator(max_t, amplitude, frequency, damping):

    if max_t <= 0:
        raise ValueError("max_t should be > 0")
    if amplitude < 0 or amplitude > 2:
        raise ValueError(f"Amplitude should be between 0 and 2, {amplitude} given")
    if frequency < 0 or frequency > 4*pi:
        raise ValueError(f"Frequency should be between 0 and {4*pi}, {frequency} given")
    if damping < 0 or damping > 0.5:
       raise ValueError(f"Damping should be between 0 and 0.5, {damping} given") 


    data = list(oscillator(max_t, amplitude, frequency, damping))
    fig, axes = plt.subplots(3,1, sharex=True)

    x = [i[0] for i in data]
    y = [i[1] for i in data]
    v = [i[2] for i in data]
    e = [i[3] for i in data]

    dline, = axes[0].plot(x, y, color="b")
    axes[0].set_title("Displacement x(t)")
    axes[0].set_ylim([-2, 2])
    axes[0].set_ylabel("y")
    axes[0].grid(True)

    vline, = axes[1].plot(x, v, color="r")
    axes[1].set_title("Velocity v(t)")
    axes[1].set_ylim([-4*pi, 4*pi])
    axes[1].set_ylabel("v")
    axes[1].grid(True)
    
    eline, = axes[2].plot(x, e, color="g")
    axes[2].set_title("Energy e(t)")
    axes[2].set_ylim([0.01, 16*pi**2])
    axes[2].set_yscale("log")
    axes[2].set_ylabel("e")
    axes[2].set_xlabel("Time [s]")
    axes[2].grid(True)


    # Slider
    plt.subplots_adjust(bottom=0.25)
    aslider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
    fslider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
    dslider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])

    aslider = Slider(ax=aslider_ax, label="Amplitude", valmin=0, valmax=2, valinit = amplitude)
    fslider = Slider(ax=fslider_ax, label="frequency", valmin=0, valmax=4*pi, valinit=frequency)
    dslider = Slider(ax=dslider_ax, label="damping", valmin=0, valmax=0.5, valinit=damping)

    def update(val):
        data = list(oscillator(max_t, aslider.val, fslider.val, dslider.val))

        y = [i[1] for i in data]
        v = [i[2] for i in data]
        e = [i[3] for i in data]

        dline.set_ydata(y)
        vline.set_ydata(v)
        eline.set_ydata(e)

        fig.canvas.draw_idle()
    


    aslider.on_changed(update)
    fslider.on_changed(update)
    dslider.on_changed(update)
    
    fig.legend(handles=[dline, vline, eline], labels=["displacement", "velocity", "energy"], loc="upper right")
    fig.suptitle("Harmonic Oscillator", fontsize=20)
    plt.show()
    

    




def oscillator(max_t, amplitude, frequency, damping):
    t = 0
    while t <= max_t:
        displacement = amplitude*exp(-damping*t)*cos(frequency*t)
        velocity = -amplitude*damping*exp(-damping*t)*cos(frequency*t)-amplitude*frequency*exp(-damping*t)*sin(frequency*t)
        energy = 0.5*velocity**2 + 0.5*(frequency * displacement)**2
        yield  t, displacement, velocity, energy
        t += max_t / 100




plot_harmonic_oscillator(10, 1, 2*pi, 0.1)

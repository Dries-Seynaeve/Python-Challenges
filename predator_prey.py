import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider
import numpy as np


def plot_predator_prey(max_t, prey_growth, pred_growth, prey_loss, pred_loss):

    data = list(predator_prey(max_t, prey_growth, prey_loss, pred_growth, pred_loss))

    time = [d[0] for d in data]
    prey = [d[1] for d in data]
    pred = [d[2] for d in data]

    fig = plt.figure()
    gs = GridSpec(2,2)

    # Create the subplots
    ax1 = fig.add_subplot(gs[0,:])
    ax2 = fig.add_subplot(gs[1,0])
    ax3 = fig.add_subplot(gs[1,1])

    # Plot the figure
    preyline, = ax1.plot(time, prey, color="red", label="Prey")
    predline, = ax1.plot(time, pred, color="blue", label="Predator")
    ax1.set_title("Prey and predator versus time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population")
    ax1.legend()
    ax1.grid(True)

    phase_line = ax2.scatter(pred, prey, color="green")
    ax2.set_title("Prey and predator phase plot")
    ax2.set_xlabel("Predator")
    ax2.set_ylabel("Prey")
    ax2.grid(True)

    total_line = ax3.plot(time, [x+y for x,y in zip(prey,pred)], color="black")
    ax3.set_title("Total population")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Population")
    ax3.grid(True)

    # Set up the sliders
    plt.subplots_adjust(bottom=0.35)
    aaxis = plt.axes([0.2, 0.05, 0.6, 0.03])
    baxis = plt.axes([0.2, 0.10, 0.6, 0.03])
    daxis = plt.axes([0.2, 0.15, 0.6, 0.03])
    gaxis = plt.axes([0.2, 0.2, 0.6, 0.03])

    aslider = Slider(ax=aaxis, label="alpha", valmin=0, valmax=0.2, valinit=prey_growth)
    bslider = Slider(ax=baxis, label="beta", valmin=0, valmax=0.02, valinit=prey_loss)
    dslider = Slider(ax=daxis, label="delta", valmin=0, valmax=0.02, valinit=pred_growth)
    gslider = Slider(ax=gaxis, label="gamma", valmin=0, valmax=0.2, valinit=pred_loss)

    
    fig.suptitle(f"Prey Predator: alpha: {aslider.val}, beta: {bslider.val}, delta: {dslider.val}, gamma: {gslider.val}")
    def update(val):
        data = list(predator_prey(max_t, aslider.val, bslider.val, dslider.val, gslider.val))

        prey = [d[1] for d in data]
        pred = [d[2] for d in data]

        preyline.set_ydata(prey)
        predline.set_ydata(pred)
        
        phase_line.set_offsets(np.c_[pred, prey])
        
        total_line[0].set_ydata([x+y for x, y in zip(prey, pred)])
        fig.suptitle(f"Prey Predator: alpha: {aslider.val}, beta: {bslider.val}, delta: {dslider.val}, gamma: {gslider.val}")

        fig.canvas.draw_idle()
    
    aslider.on_changed(update)
    bslider.on_changed(update)
    dslider.on_changed(update)
    gslider.on_changed(update)
    plt.show()    



def predator_prey(max_t, alpha, beta, delta, gamma):
    """Yield the predator/preys for every time from 0 to max_t"""
    if max_t <= 0:
        raise ValueError("max_t is smaller or equal to 0, value should be positive.")
    t = 0
    prey = 40
    pred = 9
    while t <= max_t:
        yield (t, prey, pred)

        prey += 0.1*(alpha*prey - beta*prey*pred)
        pred += 0.1*(delta*prey*pred - gamma*pred)
        t += 0.1




if __name__ == "__main__":
    plot_predator_prey(50, 0.1, 0.01, 0.01, 0.1)



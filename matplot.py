import matplotlib.pyplot as plt

def fibonacci_limit(n):
    if n < 0:
        return

    a = 0
    b = 1
    while n >= a:
        yield a
        dummy = a + b
        a = b
        b = dummy


def plot_fibonacci_limit(n):
    """Plots Fibonacci numbers up to n with indices."""

    
    x, y = zip(*enumerate(fibonacci_limit(n)))

    plt.plot(x, y, 'bo-', label="Fibonacci")
    plt.xlabel("Index of each Fibonacci number")
    plt.ylabel("Fibonacci Values")
    plt.title("Fibonacci Numbers")
    plt.grid(True)
    plt.legend()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np
def plot_population_growth(max_time, growth_rate, initial_pop):
    """Models and visualizes exponential population growth with saturation"""

    # Check that initial_pop is positive
    if initial_pop <= 0:
        raise ValueError("initial_pop must be positive")
    if max_time <= 0:
        raise ValueError("max_time must be positive")
    
    K = 1000.   # Carrying capacity (max population)

    t = np.linspace(0, max_time, 100)
    y = K / (1 + ((K - initial_pop) / initial_pop)*np.exp(-growth_rate * t))

    t0 = max_time/2
    y0 = K / (1 + ((K - initial_pop) / initial_pop)*np.exp(-growth_rate * t0))

    plt.plot(t, y, label="Logistic Growth", color="red")
    plt.axhline(K, label="Carrying Capacity", color="blue", linestyle="--")
    plt.annotate("t_max / 2", (t0, y0), xytext=(t0-10, y0+60), arrowprops=dict(facecolor='black', arrowstyle='->')) 
    plt.xlabel("time")
    plt.ylabel("population")
    plt.legend()
    plt.show()

    

    

if __name__ == "__main__":
    # plot_fibonacci_limit(100000)
    plot_population_growth(50, 0.1, 10)

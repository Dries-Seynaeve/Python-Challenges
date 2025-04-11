import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def estimate_pi(n_darts=1000, plot=True):
    if n_darts < 0:
        raise ValueError(f"n_darts should be a positive")
    if (not isinstance(n_darts, (int, float))) or (not isinstance(plot, bool)):
        if isinstance(n_darts, (int, float)):
            raise TypeError("plot should be boolean")
        else:
           raise TypeError("n_darts should be number")
       
    square = 2*np.random.rand(int(n_darts), 2)-1
    mask = np.array(np.sum(square**2, axis=1) <= 1)
    circle   = square[mask]
    rest      = square[np.invert(mask)]

    pi_estimate_evolution = [4*np.mean(mask[:i]) for i in range(500, n_darts, 500)]
    pi_estimate = 4*np.mean(mask)
    unique_points = len({(x,y) for [x, y] in square})




    if plot:
        fig, ax = plt.subplots(2)
        
        if n_darts >= 5000:
            indices = np.random.choice(np.arange(n_darts), size=5000, replace=False)
            square = square[indices]
            mask = np.array(np.sum(square**2, axis=1) <= 1)
            circle = square[mask]
            rest = square[np.invert(mask)]
            
        [x_r, y_r] = rest.transpose()
        [x_c, y_c] = circle.transpose()

        ax[0].scatter(x_r, y_r, color="red", label="outside the circle", s=1)
        ax[0].scatter(x_c, y_c, color="blue", label="inside the circle", s=1)
        circle = Circle((0,0), 1, fill=False, color="black")
        ax[0].add_patch(circle)
        ax[0].set_aspect('equal')
        ax[0].legend()

        ax[1].scatter(range(500, n_darts, 500), pi_estimate_evolution, color="blue")
        ax[1].hlines(np.pi,500, n_darts, color="red")
        
        plt.show()
    return pi_estimate, unique_points
    
    

    



if __name__ == "__main__":
    print(estimate_pi(n_darts=5000000))

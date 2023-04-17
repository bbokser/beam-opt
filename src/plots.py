import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'no-latex'])
plt.rcParams['lines.linewidth'] = 2
import matplotlib.ticker as plticker

plt.rcParams['font.size'] = 16


def plot_gen(x, y, mat_name, x_label, y_label):
    for k in range(np.shape(x)[0]):
        plt.plot(x[k, :], y[k, :], label=mat_name[k])        
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


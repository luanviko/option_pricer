from option_pricer.vanilla import VanillaOptionBS
from option_pricer.vanilla import VanillaOptionMC
from option_pricer.average import ArithmeticOptionMC
import numpy as np
import matplotlib.pyplot as plt


def test_average_put_call():

    option = ArithmeticOptionMC(
        K=100,
        S=np.linspace(95, 105, 100), 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=1000
    )

    call = option.call()
    put  = option.put()
    S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(projection='3d')
    ax1.set_title('Arithmetic Call Option')
    ax1.plot_surface(S_grid, T_grid, call, cmap='jet')
    ax1.set_xlabel('Stock Price')
    ax1.set_ylabel('Time to Expiry')
    ax1.set_zlabel('Value')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(projection='3d')
    ax2.set_title('Arithmetic Put Option')
    ax2.plot_surface(S_grid, T_grid, put, cmap='jet')
    ax2.set_xlabel('Stock Price')
    ax2.set_ylabel('Time to Expiry')
    ax2.set_zlabel('Value')

    plt.show()
    plt.close()

    assert isinstance(call, np.ndarray) or isinstance(call, float) or isinstance(put, np.ndarray) or isinstance(put, float)


def test_average_greeks():

    option = ArithmeticOptionMC(
        K=100,
        S=np.linspace(95, 105, 100), 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=1000
    )

    delta = option.delta()
    theta = option.theta()

    S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(projection='3d')
    ax3.set_title('Arithmetic Option Delta')
    ax3.plot_surface(S_grid, T_grid, delta, cmap='jet')
    ax3.set_xlabel('Stock Price')
    ax3.set_ylabel('Time to Expiry')
    ax3.set_zlabel('Value')

    fig4 = plt.figure()
    ax4 = fig4.add_subplot(projection='3d')
    ax4.set_title('Arithmetic Theta')
    ax4.plot_surface(S_grid, T_grid, theta, cmap='jet')
    ax4.set_xlabel('Stock Price')
    ax4.set_ylabel('Time to Expiry')
    ax4.set_zlabel('Value')

    plt.show()
    plt.close()

    assert isinstance(theta, np.ndarray) or isinstance(theta, float)

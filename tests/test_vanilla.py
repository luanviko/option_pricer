import numpy as np
import matplotlib.pyplot as plt
from option_pricer.vanilla import VanillaOptionBS, VanillaOptionMC

def test_call_option():
    fig, ax = plt.subplots()
    option = VanillaOptionBS(
        K=100,
        S=[97.5, 100, 102.5], 
        sigma=0.2, 
        r=0.05,
        t=1
    )
    price = option.call()
    
    ax.plot(option.ts, price)
    ax.set_title("Call Option Price vs Time")
    plt.show(block=False)
    
    assert isinstance(price, np.ndarray) or isinstance(price, float)

def test_put_option():
    fig, ax = plt.subplots()
    option = VanillaOptionBS(
        K=100,
        S=100, 
        sigma=0.2, 
        r=0.05,
        t=1
    )
    price = option.put()
    
    ax.plot(option.ts, price)
    ax.set_title("Put Option Price vs Time")
    plt.show(block=False)  
    
    assert isinstance(price, np.ndarray) or isinstance(price, float)

def test_parity():
    fig, ax = plt.subplots()
    option = VanillaOptionBS(
        K=100,
        S=100, 
        sigma=0.2, 
        r=0.05,
        t=1
    )
    price_call = option.call()
    price_put  = option.put()

    ax.plot(option.ts, price_call - price_put, label='Call - Put')
    ax.plot(option.ts, option.Ss - option.K * np.exp(-option.r * option.ts), label=r'$S - Ke^{(-rt)}$')
    ax.set_title("Put-Call Parity Check")
    ax.legend()
    plt.show(block=False)
    
    assert np.isclose(price_call - price_put, option.Ss - option.K * np.exp(-option.r * option.ts), atol=1e-6).all()

def test_stock_price_range():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    option = VanillaOptionBS(
        K=100,
        S=np.linspace(50, 150, 100), 
        sigma=0.2, 
        r=0.05,
        t=1
    )
    price_call = option.call()
    price_put  = option.put()
    payoff_call = option.call_payoff()
    payoff_put  = option.put_payoff()

    # Call Subplot
    ax1.plot(option.Ss[0], price_call[0], label='Call Option Price')
    ax1.plot(option.Ss[0], payoff_call[0], label='Call Option Payoff', linestyle='--')
    ax1.set_xlabel('Stock Price')
    ax1.set_ylabel('Option Price')
    ax1.set_title('Call Prices vs Stock Price')
    ax1.legend()

    # Put Subplot
    ax2.plot(option.Ss[0], price_put[0], label='Put Option Price')
    ax2.plot(option.Ss[0], payoff_put[0], label='Put Option Payoff', linestyle='--')
    ax2.set_xlabel('Stock Price')
    ax2.set_ylabel('Option Price')
    ax2.set_title('Put Prices vs Stock Price')
    ax2.legend()
    
    plt.show(block=False)

def test_greeks():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    option = VanillaOptionBS(
        K=100,
        S=np.linspace(50, 150, 100), 
        sigma=0.2, 
        r=0.05,
        t=1
    )

    delta_call, _ = option.delta()
    ax.plot_surface(option.Ss, option.ts, delta_call, cmap='viridis')
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Time to Expiry')
    ax.set_zlabel('Delta')
    ax.set_title('Delta Surface')
    plt.show(block=False)

def test_MC_paths():
    fig, ax = plt.subplots()
    option = VanillaOptionMC(
        K=100,
        S=[100, 150], 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=5
    )
    stock_paths = option._generate_paths()
    
    for i in range(0, len(option.S)):
        ax.plot(stock_paths[i, :, :])
        
    ax.set_title("Monte Carlo Paths")
    plt.show(block=False)
    assert isinstance(stock_paths, np.ndarray) or isinstance(stock_paths, float)

def test_MC_call_t():
    fig, ax = plt.subplots()
    option = VanillaOptionMC(
        K=100,
        S=[97.5, 100, 102.5], 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=10000
    )
    call = option.call()
    
    for i in range(0, len(option.S)):
        ax.plot(option.time_space, call[i,:])
        
    ax.set_title("MC Call Price Over Time")
    plt.show(block=False)
    assert isinstance(call, np.ndarray) or isinstance(call, float)

def test_MC_call_S():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    option = VanillaOptionMC(
        K=100,
        S=np.linspace(95, 105, 100), 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=1000
    )
    call = option.call()
    
    S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')
    ax.plot_surface(S_grid, T_grid, call, cmap='viridis')
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Time to Expiry')
    ax.set_title('MC Call Price Surface')
    plt.show(block=False)
    assert isinstance(call, np.ndarray) or isinstance(call, float)

def test_MC_delta():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    option = VanillaOptionMC(
        K=100,
        S=np.linspace(95, 105, 100), 
        sigma=0.2, 
        r=0.05,
        t=1,
        M=1000
    )
    delta = option.delta()
    
    S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')
    ax.plot_surface(S_grid, T_grid, delta, cmap='viridis')
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Time to Expiry')
    ax.set_title('MC Delta Surface')
    plt.show()
    assert isinstance(delta, np.ndarray) or isinstance(delta, float)
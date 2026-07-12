from option_pricer.vanilla import VanillaOptionBS
from option_pricer.vanilla import VanillaOptionMC
import numpy as np
import matplotlib.pyplot as plt

# def test_call_option():
#     option = VanillaOptionBS(
#         K=100,
#         S=[97.5, 100, 102.5], 
#         sigma=0.2, 
#         r=0.05,
#         t=1
#     )
#     price = option.call()
#     plt.plot(option.ts, price)
#     print(price)
#     plt.show()  
#     assert isinstance(price, np.ndarray) or isinstance(price, float)

# def test_put_option():
#     option = VanillaOption(
#         K=100,
#         S=100, 
#         sigma=0.2, 
#         r=0.05,
#         t=1
#     )
#     price = option.put()
#     plt.plot(option.ts, price)
#     print(price)
#     plt.show()  
#     assert isinstance(price, np.ndarray) or isinstance(price, float)

# def test_parity():
#     option = VanillaOption(
#         K=100,
#         S=100, 
#         sigma=0.2, 
#         r=0.05,
#         t=1
#     )
#     price_call = option.call()
#     price_put  = option.put()

#     plt.plot(option.ts, price_call - price_put, label='Call - Put')
#     plt.plot(option.ts, option.Ss - option.K * np.exp(-option.r *option.ts), label=r'$S - Ke^{(-rt)}$')
#     plt.legend()
#     plt.show()
#     assert np.isclose(price_call - price_put, option.Ss - option.K * np.exp(-option.r * option.ts), atol=1e-6).all()  # Note the .all() to evaluate the entire boolean grid matrix

# def test_stock_price_range():
#     option = VanillaOption(
#         K=100,
#         S=np.linspace(50, 150, 100), 
#         sigma=0.2, 
#         r=0.05,
#         t=1
#     )
#     price_call = option.call()
#     price_put  = option.put()
#     payoff_call = option.call_payoff()
#     payoff_put  = option.put_payoff()

#     plt.plot(option.Ss[0], price_call[0], label='Call Option Price')
#     plt.plot(option.Ss[0], payoff_call[0], label='Call Option Payoff', linestyle='--')
#     plt.xlabel('Stock Price')
#     plt.ylabel('Option Price')
#     plt.title('Option Prices vs Stock Price')
#     plt.legend()
#     plt.show()
#     plt.close()

#     plt.plot(option.Ss[0], price_put[0], label='Put Option Price')
#     plt.plot(option.Ss[0], payoff_put[0], label='Put Option Payoff', linestyle='--')
#     plt.xlabel('Stock Price')
#     plt.ylabel('Option Price')
#     plt.title('Option Prices vs Stock Price')
#     plt.legend()
#     plt.show()
#     plt.close()

def test_greeks():
    option = VanillaOptionBS(
        K=100,
        S=np.linspace(50, 150, 100), 
        sigma=0.2, 
        r=0.05,
        t=1
    )

    delta_call, delta_put = option.delta()
    # theta_call, theta_put = option.theta()
    rho_call, rho_put     = option.rho()
    vega  = option.vega()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(option.Ss, option.ts, delta_call, cmap='viridis')
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Time to Expiry')
    ax.set_zlabel('Delta')
    ax.set_title('Delta Surface')
    print(delta_call.shape)
    plt.show()

# def test_MC_paths():

#     option = VanillaOptionMC(
#         K=100,
#         S=[100, 150], 
#         sigma=0.2, 
#         r=0.05,
#         t=1,
#         M=5
#     )
#     stock_paths = option._generate_paths()
#     print(stock_paths.shape)
#     for i in range(0, len(option.S)):
#         plt.plot(stock_paths[i, :, :])
#     plt.show()
#     assert isinstance(stock_paths, np.ndarray) or isinstance(stock_paths, float)

def test_MC_call_t():

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
        plt.plot(option.time_space, call[i,:])
    plt.show()
    assert isinstance(call, np.ndarray) or isinstance(call, float)

# def test_MC_call_S():

#     option = VanillaOptionMC(
#         K=100,
#         S=np.linspace(95, 105, 100), 
#         sigma=0.2, 
#         r=0.05,
#         t=1,
#         M=1000
#     )
#     call = option.call()
#     # plt.plot(option.S, call[:,0])
#     # plt.show()
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')
#     ax.plot_surface(S_grid, T_grid, call, cmap='viridis')
#     ax.set_xlabel('Stock Price')
#     ax.set_ylabel('Time to Expiry')
#     # ax.set_zlabel('Delta')
#     # ax.set_title('Delta Surface')
#     plt.show()
#     assert isinstance(call, np.ndarray) or isinstance(call, float)

# def test_MC_delta():

#     option = VanillaOptionMC(
#         K=100,
#         S=np.linspace(95, 105, 100), 
#         sigma=0.2, 
#         r=0.05,
#         t=1,
#         M=1000
#     )
#     delta = option.delta()
#     # plt.plot(option.S, call[:,0])
#     # plt.show()
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')
#     ax.plot_surface(S_grid, T_grid, delta, cmap='viridis')
#     ax.set_xlabel('Stock Price')
#     ax.set_ylabel('Time to Expiry')
#     # ax.set_zlabel('Delta')
#     # ax.set_title('Delta Surface')
#     plt.show()
#     assert isinstance(delta, np.ndarray) or isinstance(delta, float)

# def test_MC_theta():

#     option = VanillaOptionMC(
#         K=100,
#         S=np.linspace(95, 105, 100), 
#         sigma=0.2, 
#         r=0.05,
#         t=1,
#         M=1000
#     )
#     theta = option.theta()
#     rho = option.rho()
#     # plt.plot(option.S, call[:,0])
#     # plt.show()
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     S_grid, T_grid = np.meshgrid(option.S, option.time_space, indexing='ij')
#     ax.plot_surface(S_grid, T_grid, rho, cmap='viridis')
#     ax.set_xlabel('Stock Price')
#     ax.set_ylabel('Time to Expiry')
#     # ax.set_zlabel('Delta')
#     # ax.set_title('Delta Surface')
#     plt.show()
#     assert isinstance(theta, np.ndarray) or isinstance(theta, float)

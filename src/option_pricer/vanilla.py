import numpy as np
from scipy.stats import norm
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class VanillaOptionBS:
    S: np.ndarray
    K: float
    r: float
    sigma: float
    t: np.ndarray
    N: ClassVar[np.ufunc] = norm.cdf
    t_steps: int = 1000
    tol: float = 1e-6
    t0: float = 0.0

    def __post_init__(self):
        time_space = np.linspace(self.t, self.t0+self.tol, self.t_steps)
        self.Ss, self.ts = np.meshgrid(self.S, time_space)
        self.d1 = np.array([])
        self.d2 = np.array([])

    def _d1(self) -> np.ndarray:
        self.d1 = (np.log(self.Ss/self.K) + (self.r + (self.sigma**2)*0.5)*self.ts)/self.sigma/np.sqrt(self.ts)
        return self.d1

    def _d2(self) -> np.ndarray:
        self.d2 = self.d1 - self.sigma*np.sqrt(self.ts)
        return self.d2

    def call(self) -> np.ndarray:
            if self.d1.size == 0: self._d1()
            if self.d2.size == 0: self._d2()
            self.C = self.Ss * self.N(self.d1) - self.K * np.exp(-1. * self.r * self.ts) * self.N(self.d2)
            return self.C

    def put(self) -> np.ndarray:
        if self.d1.size == 0: self._d1()
        if self.d2.size == 0: self._d2()
        self.P = self.K * np.exp(-1. * self.r * self.ts) * self.N(-self.d2) - self.Ss * self.N(-self.d1)
        return self.P
    
    def call_payoff(self) -> np.ndarray:
        self.payoff_call = np.maximum(self.Ss - self.K, 0)
        return self.payoff_call

    def put_payoff(self) -> np.ndarray:
        self.payoff_put = np.maximum(self.K - self.Ss, 0)
        return self.payoff_put

    def delta(self) -> np.ndarray:
        if self.d1.size == 0: self._d1()
        delta_call = self.N(self.d1)
        delta_put = delta_call - 1
        return delta_call, delta_put
    
    def vega(self) -> np.ndarray:
        if self.d1.size == 0: self._d1()
        vega = self.Ss * norm.pdf(self.d1) * np.sqrt(self.ts)
        return vega
    
    def theta(self) -> np.ndarray:
        if self.d1.size == 0: self._d1()
        if self.d2.size == 0: self._d2()
        pdf_d1 = norm.pdf(self.d1)
        vol_term = - (self.Ss * self.sigma * pdf_d1) / (2.0 * np.sqrt(self.ts))
        theta_call = vol_term - self.r * self.K * np.exp(-self.r * self.ts) * self.N(self.d2)
        theta_put  = vol_term + self.r * self.K * np.exp(-self.r * self.ts) * self.N(-self.d2)
        return theta_call, theta_put
    
    def rho(self) -> np.ndarray:
        if self.d2.size == 0: self._d2()
        rho_call = self.ts * self.K * np.exp(-self.r * self.ts) * self.N(self.d2)
        rho_put  = -1.*self.ts * self.K * np.exp(-self.r * self.ts) * self.N(-1.*self.d2)
        return rho_call, rho_put
    

@dataclass
class VanillaOptionMC:
    S: np.ndarray
    K: float
    r: float
    sigma: float
    t: np.ndarray
    Z: ClassVar[np.ufunc] = norm.cdf
    M: int
    t_steps: int = 1000
    tol: float = 1e-6
    t0: float = 0.0
    seed:int = 42

    def __post_init__(self):
        self.S = np.atleast_1d(self.S)
        self.dt = (self.t-self.t0)/self.t_steps
        self.time_space = np.linspace(self.t0, self.t, self.t_steps+1)
        self.paths = self._generate_paths()

    def _generate_paths(self):
        np.random.seed(self.seed)
        noise = np.random.normal(size = (self.t_steps, self.M))
        drift = (self.r - 0.5 * self.sigma**2) * self.dt
        log_returns = np.cumsum(drift + self.sigma * np.sqrt(self.dt) * noise, axis=0)
        log_returns = np.insert(log_returns, 0, 0, axis=0)
        self.S_grid = np.atleast_1d(self.S)[:, np.newaxis, np.newaxis]
        self.stock_path = self.S_grid*np.exp(log_returns[np.newaxis, :, :])
        return self.stock_path
    
    def call_payoff(self):
        return np.maximum(self.paths - self.K, 0)
    
    def call(self):
        self.paths = self._generate_paths()
        payoffs = np.maximum(self.paths - self.K, 0)
        expected_payoffs = np.mean(payoffs, axis=2)
        remaining_times = self.t - self.time_space
        remaining_times = np.maximum(remaining_times, self.tol)
        discount_factors = np.exp(-self.r * remaining_times)
        return expected_payoffs * discount_factors[np.newaxis, :]
    
    def delta(self):
        
        # Set up step size for central derivative 
        h = 1.e-5

        # Back up original S array
        original_S = np.copy(self.S)
        
        # Create forward samples
        self.S = original_S + 0.5*h 
        call_forward = self.call() 

        # Create backward samples
        self.S = original_S - 0.5*h 
        call_backward = self.call() 

        # Restore original array
        self.S = original_S 

        # Return the difference between forward and backwared
        return (call_forward - call_backward) / h
    
    def theta(self) -> np.ndarray:
        '''Repeating the same steps for delta, but changing S to time_space.'''
        h = 1.e-5
        original_time_space = np.copy(self.time_space)
        self.time_space = original_time_space + 0.5 * h
        call_forward = self.call()
        self.time_space = original_time_space - 0.5 * h
        call_backward = self.call()
        self.time_space = original_time_space
        return (call_forward - call_backward) / h
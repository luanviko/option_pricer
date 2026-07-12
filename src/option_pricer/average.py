import numpy as np
from scipy.stats import norm
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class ArithmeticOptionMC:
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

    def call(self):
            self.paths = self._generate_paths()
            n_assets, n_times, _ = self.paths.shape
            call_prices_grid = np.zeros((n_assets, n_times))
            for t in range(n_times):
                current_averages = np.mean(self.paths[:, :t+1, :], axis=1)
                payoffs = np.maximum(current_averages - self.K, 0)
                call_prices_grid[:, t] = np.mean(payoffs, axis=1)
            remaining_times = self.t - self.time_space
            remaining_times = np.maximum(remaining_times, self.tol)
            discount_factors = np.exp(-self.r * remaining_times)
            return call_prices_grid * discount_factors[np.newaxis, :]

    def put(self):
        self.paths = self._generate_paths()
        n_assets, n_times, _ = self.paths.shape
        call_prices_grid = np.zeros((n_assets, n_times))
        for t in range(n_times):
            current_averages = np.mean(self.paths[:, :t+1, :], axis=1)
            payoffs = np.maximum(self.K - current_averages, 0)
            call_prices_grid[:, t] = np.mean(payoffs, axis=1)
        remaining_times = self.t - self.time_space
        remaining_times = np.maximum(remaining_times, self.tol)
        discount_factors = np.exp(-self.r * remaining_times)
        return call_prices_grid * discount_factors[np.newaxis, :]
    
    def delta(self):
        h = 1.e-5
        original_S = np.copy(self.S)
        self.S = original_S + 0.5*h 
        call_forward = self.call() 
        self.S = original_S - 0.5*h 
        call_backward = self.call() 
        self.S = original_S 
        return (call_forward - call_backward) / h
    
    def theta(self) -> np.ndarray:
        h = 1.e-5
        original_time_space = np.copy(self.time_space)
        self.time_space = original_time_space + 0.5 * h
        call_forward = self.call()
        self.time_space = original_time_space - 0.5 * h
        call_backward = self.call()
        self.time_space = original_time_space
        return (call_forward - call_backward) / h
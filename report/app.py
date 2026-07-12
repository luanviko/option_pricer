import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os, sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
    
src_path = os.path.join(root_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from helpers import *
from option_pricer.vanilla import VanillaOptionBS
from option_pricer.vanilla import VanillaOptionMC
from option_pricer.average import ArithmeticOptionMC

# --- Page Configuration
st.set_page_config(
    page_title="Development of Quantitative Pricers for Vanilla and Average-Value Options",
    page_icon="📄",
    layout="centered", # Centered forces an academic, document-like margins
    initial_sidebar_state="collapsed"
)

# --- Apply style from latex_like.css
current_dir = os.path.dirname(os.path.abspath(__file__))
style_css = os.path.join(current_dir, "latex_like.css")
with open(style_css, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- INTERACTIVE SIMULATION SIDEBAR INPUTS ---
t_steps = 1000
st.sidebar.header("Parameters")
S_in = st.sidebar.slider("Spot Price ($S$)", 50.0, 150.0, 100.0)
K_in = st.sidebar.slider("Strike ($K$)", 50.0, 150.0, 100.0)
sigma_in = st.sidebar.slider("Volatility ($\sigma$)", 0.05, 1.2, 0.20)
r_in = st.sidebar.slider("Risk-Free Rate ($r$)", 0.0, 0.12, 0.05)

sigma_geo_in = sigma_in/np.sqrt(3)
r_geo_in = 0.5 * (r_in + (sigma_in**2 / 6.0))

S_range_in = st.sidebar.slider(
    "Spot Price Range (S)",
    25.0, 250.0,
    (75.0, 125.0)   # tuple default -> renders as a two-handle range slider
)

t_step_in = st.sidebar.slider("t Step", 0, t_steps-1, int(t_steps//2))


# --- INITIALIZE PRICERS WITH CORRECT ATTRIBUTES ---

### NUMBER OF SIMULATIONS
n_sim = 500
### WARNING: CHOOSE THIS NUMBER CAREFULLY. TOO HIGH A NUMBER WILL CRASH
### THE APP. FOR MORE ACCURATE SIMULATIONS, RUN THE PRICERS ON A PYTHON 
### SCRIPT, NOT A WEB-BASED STREAMLIT APP. 

vanilla_option = VanillaOptionBS(
        K=K_in,
        S=[S_in-0.25*S_in, S_in, S_in+0.25*S_in],
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps
    )

vanilla_option_greeks = VanillaOptionBS(
        K=K_in,
        S=np.linspace(S_range_in[0], S_range_in[1], 100),
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps
    )

geometric_option = VanillaOptionBS(
        K=K_in,
        S=[S_in-0.25*S_in, S_in, S_in+0.25*S_in],
        sigma=sigma_geo_in, 
        r=r_geo_in,
        t=1,
        t_steps=t_steps
    )

geometric_option_greeks = VanillaOptionBS(
        K=K_in,
        S=np.linspace(S_range_in[0], S_range_in[1], 100),
        sigma=sigma_geo_in, 
        r=r_geo_in,
        t=1,
        t_steps=t_steps
    )

vanilla_option_MC = VanillaOptionMC(
        K=K_in,
        S=[S_in-0.25*S_in, S_in, S_in+0.25*S_in], 
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps,
        M=n_sim
    )

vanilla_option_MC_greeks = VanillaOptionMC(
        K=K_in,
        S=np.linspace(S_range_in[0], S_range_in[1], 100), 
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps,
        M=n_sim
    )

arithmetic_option_MC = ArithmeticOptionMC(
        K=K_in,
        S=[S_in-0.25*S_in, S_in, S_in+0.25*S_in], 
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps,
        M=n_sim
    )

arithmetic_option_MC_greeks = ArithmeticOptionMC(
        K=K_in,
        S=np.linspace(S_range_in[0], S_range_in[1], 100), 
        sigma=sigma_in, 
        r=r_in,
        t=1,
        t_steps=t_steps,
        M=n_sim
    )


# --- HEADER SECTION ---
st.markdown("<h1>Development of Quantitative Pricers for Vanilla and Average-Value Options</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="author-block">
    <strong>Luan Koerich</strong><br>
    Erdős Institute Quant Finance Bootcamp<br>
    <span style="font-size: 0.95rem; color: #777777;">July 10, 2026</span>
</div>
""", unsafe_allow_html=True)

# --- ABSTRACT ---
st.markdown("""
<div class="abstract-box">
    <div class="abstract-heading">Abstract</div>
    This project explores the development of quantitative pricers for vanilla (European) \
    and average-value (Asian) options. Though geometrically averaged options have a closed-form  \
    solution under a Black-Scholes-Merton model, arithmetically averaged options require \
    numerical solutions based on Monte Carlo methods. With this in mind, \
    a Black-Scholes-Merton pricer was developed for vanilla options, 
    then adapted to geometrically averaged options. \
    This same model is used to validate a Monte Carlo pricer for vanilla options, which is then \
    expanded for arithmetically averaged options.
</div>
""", unsafe_allow_html=True)



# --- SECTION 1 ---
st.markdown("<h2>1. Options </h2>", unsafe_allow_html=True)
st.markdown(
    r"""

    An **option** is a derivative contract between two parties that gives its buyer the option, not the obligation,
    to buy or to sell an underlying asset before or at a predetermined date and at a defined price.

    The defined price is called **strike price** ($K$) and is a fixed value written in the contract. 
    The predetermined date is, in turn, called **maturity date** ($T$) and is the basic deadline for 
    exercising the contract. 

    Usually an option can be split into two categories: **call options** or put **options**.
    A call is the right to buy an underlying asset, while a put is the right to sell it. 
    """
    )
    
# --- SECTION 1.1 ---
st.markdown("<h3>1.1 Vanilla Options </h3>", unsafe_allow_html=True)

st.markdown(
    r"""
    For **European options** (also referred to as **vanilla options**), 
    the contract can only be exercised at the maturity date, and not before. 

    At the date of maturity, the holder who exercises the option will receive a payoff 
    equal to the difference between the price of the underlying asset at the time of maturity ($S_T$) 
    and the strike price ($K$). 
    
    Before subtracting any premiums (the operational cost to hold such a contract), 
    the payoff of a **vanilla call option** is defined as:
    """
)

st.latex(r"C_T = \max(S_T - K, 0)")

st.markdown(r"where $S_T$ is the price of the underlying asset at $T$.")

st.markdown("For a **vanilla put option**, the payoff is defined as:")

st.latex(r"P_T = \max(K - S_T, 0)")

st.markdown(
    r"""
    Notice how a max operator is used, as the holder of the option will 
    only exercise it if it is favourable—*i.e.*, for a net positive difference. 
    Otherwise, the payoff is simply zero.
    """
)

S_range = np.linspace(S_range_in[0], S_range_in[1], 1000)
call_payoffs = np.maximum(S_range - K_in, 0)
put_payoffs  = np.maximum(K_in - S_range, 0)
fig_call = build_payoffs(S_range, call_payoffs, title = "Call Payoff")
fig_put  = build_payoffs(S_range, put_payoffs,  title = "Put Payoff")
st.plotly_chart(fig_call, use_container_width=True)
st.plotly_chart(fig_put, use_container_width=True)

# --- SECTION 1.2 ---
st.markdown("<h3>1.2 Average Value Options </h3>", unsafe_allow_html=True)

st.markdown(
    r"""
    A vanilla option payoff uses $S_T$, the price of the underlying exactly at time $T$, 
    meaning that the call or put option pricing is directly susceptible to the volatility 
    of the underlying asset. 
    
    For asset classes that are notoriously volatile, therefore, vanilla options can be too risky. 

    To mitigate such a risk, **Asian options** (also known as **average-value options**) 
    consider the partial or entire history of asset values to determine the payoff by considering 
    an average of the asset values. This neutralizes any spikes and sudden drops in the value of the 
    asset at the maturity date.

    The call and put payoffs for an average-value option are defined as:
    """
)

st.latex(r"C_T = \max(\langle S \rangle - K, 0)")

st.markdown("and")

st.latex(r"P_T = \max( K - \langle S \rangle, 0)")

st.markdown(
    r"""
    where $\langle S \rangle$ is the underlying asset's average value.

    In turn, there are two principal ways of calculating such an average:

    * **Geometrically averaged options:** $\langle S \rangle = \sqrt[n]{S_1 \cdot S_2 \cdot \ldots \cdot S_n}$
    * **Arithmetically averaged options:** $\langle S \rangle = \frac{1}{N}\sum_{i=1}^{N} S_i$, where $S_N = S_T$

    While the call and put payoffs for geometrically averaged options have a closed-form solution in a no-arbitrage 
    Black-Scholes-Merton (BSM) scenario, arithmetically averaged options only have approximate analytical solutions, 
    often requiring numerical simulations based on a Monte Carlo (MC) approach. 

    In the next sections, I will present a BSM pricer for vanilla and geometrically averaged option payoffs, 
    then use this same model to validate an MC pricer for vanilla options. Based on this MC pricer, 
    I will numerically determine the pricing of arithmetically averaged option payoffs.
    """
)

# --- SECTION 2 ---
st.markdown("<h2>2. Black-Scholes-Merton Option Pricer</h2>", unsafe_allow_html=True)

st.markdown(
    r"""
    The illustration below shows a single MC simulation of an asset path (blue line)
    together with its running geometric average. 
    A vanilla option depends only on the asset value at maturity,
    taking its real value at the $T$, while the geometrically averaged 
    option will consider an average of the asset value history (black line).
    """
)

sample_optionMC = VanillaOptionMC(
    S=S_in,
    K=K_in,
    r=r_in,
    sigma=sigma_in,
    t=1.0,
    M=1,
    t_steps=100,
    seed=42
)

fig_MC_sample = build_mc_paths_plot(sample_optionMC)
st.plotly_chart(fig_MC_sample, use_container_width=True)

st.markdown(
    r"""
    In this section I will introduce an implementation of the vanilla BSM pricer 
    and then use it to describe a geometrically averaged options, comparing it to the original.
    """
)

# --- SECTION 2.1 ---
st.markdown("<h3>2.1 Vanilla Options</h2>", unsafe_allow_html=True)

st.markdown(
    r"""
    For the BSM pricer, I am using the same notation and equations introduced by Thomas during classes. 

    In a no-arbitrage BSM scenario where the risk-free interest rate is given by $r$, consider two 
    moments in time, $t' > t$, and the time interval $dt = t' - t$. Let the call price be defined as:
    """
)

st.latex(r"C_t = e^{-r dt} \mathbb{E}[\max(S_{t'} - K, 0) ]")

st.markdown("and the put price as:")

st.latex(r"P_t = e^{-r dt} \mathbb{E}[\max(K - S_{t'}, 0) ]")

st.markdown(
    r"""
    Considering $\varphi$ and $\Phi$ to be the probability density function (PDF) and cumulative 
    distribution function (CDF) of the standard normal distribution, respectively, let:
    """
)

st.latex(
    r"\varphi(x) = \dfrac{e^{-x^2/2}}{\sqrt{2\pi}}  \qquad\text{and}\qquad \Phi(y) = \int_{-\infty}^y\varphi(x)\,dx"
)

st.markdown(
    r"""
    so that, if the underlying asset prices at a given time $t$ ($S_t$) are 
    determined by a Geometric Brownian Motion (GBM), such as:
    """
)

st.latex(r"dS_t = r S_t dt + \sigma S_t dW_t")

st.markdown(
    r"""
    where $\sigma$ is the volatility of the underlying asset and $dW_t$ 
    is the random component of the GBM, then the call and put option values become:
    """
)

st.latex(r"C_t = S_t \Phi (d_1) - K e^{-rdt} \Phi(d_2)")

st.markdown("and")

st.latex(r"P_t = K e^{-rdt}\Phi(-d_2) - S_t \Phi(-d_1)")

st.markdown("with:")

st.latex(
    r"d_1 = \dfrac{\ln\left(\frac{S_{t}}{K}\right) + \left(r + \frac{\sigma^2}{2}\right)dt}{\sigma \sqrt{dt}} \qquad\text{and}\qquad d_2 = d_1 - \sigma\sqrt{dt}"
)

st.markdown(
    r"""
    The **Call and Put Price** curves can be seen below. 
    As time to maturity decreases, the option values decay toward the baseline payoff. 
    """
)

fig_vanilla_call = build_price_by_time(vanilla_option, vanilla_option.call(), title = "Call", y_label="Call Price")
st.plotly_chart(fig_vanilla_call, use_container_width=True)

fig_vanilla_put = build_price_by_time(vanilla_option, vanilla_option.put(), title = "Put", y_label="Put Price")
st.plotly_chart(fig_vanilla_put, use_container_width=True)

st.markdown(
    r"""
    The **Delta ($\Delta$)** curve shows the rate at which the call option value changes
    with the spot price $S$.  

    As $S$ moves to $S \gg K$, $\Delta$ asymptotically approaches $1.0$ for the call option; 
    the call starts matching the underlying asset one-to-one. 
    
    On the other hand, when $S \ll K$, the $\Delta$ asymptotically approaches $0.0$.

    As time approaches maturity, it is noticeable that the curve becomes less smooth
    and steeper, to the point where, at $t=T$, the curve collapses into a step function,
    """
)

st.latex(
    r"""
    \Delta = \begin{cases} 0 & \text{if } S < K \quad \text{(Out-of-the-Money)} \\ 1 & \text{if } S > K \quad \text{(In-the-Money)} \end{cases}
    """
)

st.markdown(
    r"""
    This means that, as time to maturity approaches, keeping your portfolio $\Delta$ neutral
    becomes increasingly less nuanced, as at $t=T$ you need to either hold 100% of your assets
    or none of it. 
    """
)

fig_vanilla_delta = build_delta(vanilla_option_greeks, title = "Delta")
st.plotly_chart(fig_vanilla_delta, use_container_width=True)

st.markdown(
    r"""
    The **Theta ($\Theta$)**, in turn, is the derivative of the call option value in relation to time, 
    that is, the plot below tracks the rate of change of the call option over time. 

    **By changing the values of $S$ and $K$ in the left panel, you can move the call option to
    in-the-money or out-of-the-money positions and see how $\Theta$ changes closer to time of maturity.**
    Notice how, for a call option, $\Theta$ is strictly negative as expected.  
    """
)

fig_vanilla_theta = build_theta(vanilla_option, title = "Theta")
st.plotly_chart(fig_vanilla_theta, use_container_width=True, key="van_theta")

# --- SECTION 2.2 ---
st.markdown("<h3>2.2 Geometrically Averaged Options</h2>", unsafe_allow_html=True)

st.text(
  """
  When considering the geometric average of the underlying asset, 
  the volatility $\sigma$ is replaced with an effective volatility
  """)
st.latex(r"\sigma_a = \dfrac{\sigma}{\sqrt{3}} \sim 0.577 \sigma,")
st.markdown(
  """
  meaning a considerable reduction in the volatility of the call option pricing.
  In turn, the risk-free rate $r$ is replaced by $r-q_a$, where this synthetic discount factor is
  defined as
  """)
st.latex(r"q_a = \dfrac{1}{2}\left(r + \frac{\sigma^2}{6}\right).")

st.markdown(
  """

  In the figure below, the vanilla and geometrically averaged call options are compared. 
  
  **Please select different values of $\sigma$ in the left panel.**

  It is noticeable that the geometric average is always cheaper than the 
  vanilla option, especially when the volatility is high. 
  When setting $\sigma \sim 0.2$, the difference between the options is around 1. 
  However, when setting $\sigma \sim 0.8$, the geometrically averaged option is $\sim 10$.

  """
)
fig_comp_geo_call_t, fig_comp_geo_put_t = build_geo_comp_t(vanilla_option, geometric_option)
st.plotly_chart(fig_comp_geo_call_t, use_container_width=True, key="com_geo_call_t")
st.markdown(
  """

  When it comes to put options, the geometric options are valued higher 
  than vanilla options for lower $\sigma$, but there is a complete 
  inversion of the pricings for higher $\sigma$. 
  At the highest volatility, the geometric option is significantly cheaper than the vanilla.

  """
)
st.plotly_chart(fig_comp_geo_put_t, use_container_width=True, key="com_geo_put_t")

st.markdown(
  """

 A similar pattern, including an inversion in the put option pricing, is observed when plotting 
 the call and put prices over the spot price. 
  """
)

fig_comp_geo_call_S, fig_comp_geo_put_S = build_geo_comp_S(vanilla_option_greeks, geometric_option_greeks, t_step=t_step_in)
st.plotly_chart(fig_comp_geo_call_S, use_container_width=True, key="com_geo_call_S")
st.plotly_chart(fig_comp_geo_put_S, use_container_width=True, key="com_geo_put_S")

fig_comp_geo_delta, fig_comp_geo_theta = build_geo_greeks(vanilla_option_greeks, geometric_option_greeks, t_step=t_step_in)

st.markdown(
  """
The Delta plot highlights how the geometric option's sensitivity changes depending
on the asset price. For $S < K$, the geometric Delta decreases a lot faster than the vanilla Delta.
On the other hand, $S > K$ shows a steeper geometric Delta. We notice that the difference 
between the geometric and vanilla Deltas is larger for $S < K$, which means a lower rate of
change in the geometric call option when $S$ becomes considerably smaller than $K$.
  """
)
st.plotly_chart(fig_comp_geo_delta, use_container_width=True, key="com_geo_delta")

st.markdown(
  """
  In turn, the comparison between the geometric and vanilla Thetas 
  show that, for higher volatilities and at times closer to maturity, 
  the geometric call options are less susceptible to changes in time.
  """
)

st.plotly_chart(fig_comp_geo_theta, use_container_width=True, key="com_geo_theta")


# --- SECTION 3 ---
st.markdown("<h2>3. Monte Carlo Option Pricer </h2>", unsafe_allow_html=True)

st.markdown(
  """
  The illustration below shows the simulation of several asset value paths
  following a GBM, which are repeated at least 1000 times to determine 
  the call and put option prices for vanilla and arithmetically averaged options. 
  """
)

sample_optionMC = VanillaOptionMC(
    S=S_in,
    K=K_in,
    r=r_in,
    sigma=sigma_in,
    t=1.0,
    M=10,
    t_steps=100,
    seed=42
)

fig_MC_sample = build_mc_paths_plot(sample_optionMC, average_type = 'arithmetic')
st.plotly_chart(fig_MC_sample, use_container_width=True)


st.markdown(
  """
  In this section I will introduce a MC-based pricer for vanilla options
  and adapt it for arithmetically averaged options. 
  """
)

# --- SECTION 3.1 ---
st.markdown("<h3>3.1 Vanilla Options </h2>", unsafe_allow_html=True)

st.markdown(
  """
  As an alternative approach to `VanillaOptionBS`, which uses the closed-form analytical solutions
  to describe the prices of call and put options, I implemented a class called 
  `VanillaOption MC`, which uses a random number generator to simulate the path of an asset value. 

  I start using the same definition of a vanilla option, 
  """
)

st.latex(r"V_t = e^{-r(T-t)} \mathbb{E} \left[ \max(S_T - K, 0) \right]")

st.markdown(
  r"""
  approximating the expected value $\mathbb{E} \left[ \max(S_T - K, 0) \right]$
  by averaging over `M` assets paths with `np.mean()`.

  The class attributes are the spot price `S`, the strike price `K`,
  the interest rate `r`, the volatility `sigma` and the time to maturity `t_0`. 

  Internally, `T = 0` is the maturity time by default, but it can be adjusted. 
  The time is discretized by `n_steps`, following `dt = (T - t_0)/n_steps` or, 
  equivalently, 
  """
)

st.latex(r"dt = \dfrac{T - t_0}{N_\text{steps}}")

st.markdown(
  """
  The simulation follows the same underlying mechanics for the BSM model, 
  that is, I assume that the underlying asset price follows a BGM of the form
  """
)

st.latex("dS_t = rS_t dt + \sigma S_t dW_t")

st.markdown(
  """
  which leads to 
  """
)

st.latex(r"S_{t+\Delta t} = S_t \exp\left[ \left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z \right], \quad Z \sim \mathcal{N}(0,1)")

st.markdown(
  """
  where $N(0, 1)$ is the normal distribution.

  To maximize efficiency and vectorization of the code, $Z$ is implemented as 
  `np.random.normal(size = self.t_steps, self.M)`. In turn the paths are
  calculated in the same fashion as we developed in class, using the cumulative
  log returns with `np.cumsum(..., axis = 0)`.
  Finally, in order to broadcast the expected values over a range of $S$ and time space,
  `np.newaxis` was added to match multidimensional multiplication when needed and 
  maintain the code completely vectorized and efficient. 

  In turn, the payoff was calculated at maturity and every point in space before
  that using the usual formula, 
  """
)

st.latex(r"\text{Payoff}(S_t) = \max(S_t - K, 0)")

st.markdown(
  r"""
  After that, the expected value of the payoffs was calculated using `np.mean(... axis = 2)`, 
  to collapse the multi-path dimension, defined by `M`, into a single expected value for all
  the asset value paths. Note that the discount factor was calculated for every step 
  $\tau = T - t$ using $e^{-r\tau}$, and applied to each path's step before the average was calculated. 

  The image below shows the call option price for three different spot prices over time. 
  It compares the BSM pricer developed above with the MC pricer, showing that MC-based 
  pricer behaves closely to the analytical BSM model.
  """
)

fig_vanilla_call_MC_t = build_price_by_time_MC(vanilla_option_MC, vanilla_option, y_label="Call Price")
st.plotly_chart(fig_vanilla_call_MC_t, use_container_width=True)

st.markdown(
  r"""
  Below, the image compares the call option price for a range of spot prices. 
  
  **Please adjust the time (t Step) in the left panel.**
  
  MC and BSM show similar behaviour, including the collapse into the payoff formula 
  at time of maturity (t Step set to 0).
  """
)

fig_vanilla_call_MC_S = build_price_by_S_MC(vanilla_option_MC_greeks, vanilla_option_greeks, t_step = t_step_in)
st.plotly_chart(fig_vanilla_call_MC_S, use_container_width=True)


st.markdown(
  r"""
  In turn, calculating the greeks requires numerical differentiation methods,
  namely the Finite Difference Method (FDM) with central difference scheme. 
  For efficiency and vectorization, we recalculate paths by bumping the paths 
  up or down by a factor $h/2$ over $S$ or $dt$, then calculate the difference.
  Here, $h$ is a small number. 

  The derivative of $V$ over $S$, called Delta ($\Delta$), is then defined as 
  """
)

st.latex(r"\Delta = \frac{\partial V}{\partial S} \approx \frac{V(S + \frac{1}{2}h) - V(S - \frac{1}{2}h)}{h}")

st.markdown(
  r"""
  while Theta ($\Theta$), the derivative of $V$ over time, is defined by 
  """
)

st.latex(r"\Theta = \frac{\partial V}{\partial t} \approx \frac{V(t + \frac{1}{2}h) - V(t - \frac{1}{2}h)}{h}")

st.markdown(
  """
  As an illustration, the image below shows the $\Delta$ comparison for the BSM and MC
  pricers, showing qualitatively similar curves for both models.
  """
)
fig_vanilla_delta_MC = build_delta_MC(vanilla_option_MC_greeks, vanilla_option_greeks, t_step = t_step_in)
st.plotly_chart(fig_vanilla_delta_MC, use_container_width=True)


# --- SECTION 3.1 ---
st.markdown("<h3>3.2 Arithmetically Averaged Options </h2>", unsafe_allow_html=True)

st.markdown(
  """
  For arithmetically averaged options, the call options of lognormal paths 
  do not have a closed form, requiring the use of MC methods.
  I am now going to apply the method developed above for vanilla options 
  for this case. 

  The arithmetically averaged option call follows
  """
)

st.latex(r"A_t = e^{-r(T-t)} \mathbb{E} \left[ \text{Payoff}(\langle S \rangle) \right]")

st.markdown(
  """
  where the average value of the underlying asset is defined as
  """
)

st.latex(r"\langle S \rangle = \frac{1}{N_{\text{steps}} + 1} \sum_{i=0}^{N_{\text{steps}}} S_{t_i}")

st.markdown(
  """
  implemented in the code as `np.mean(self.paths, axis=1)`. 

  The call payoff is defined as 
  """
)

st.latex(r"\text{Payoff}(S_t) = \max( \langle S \rangle - K, 0)")

st.markdown(
  """
  and implemented using `np.maximum()` after calculating the average of each path.
  Then the collapse of the $M$ paths to determine the expected value of the call option
  follows the same implementation as for the vanilla MC implementation.

  The plot below compares the vanilla and arithmetically averaged call options
  using the MC pricer. They show a similar behaviour as to the BSM implementation,
  where the average-value call option is valued cheaper than the vanilla option.
  """
)

fig_call_aritmetic_MC = build_call_MC_arith(arithmetic_option_MC_greeks, vanilla_option_MC_greeks, t_step = t_step_in)
st.plotly_chart(fig_call_aritmetic_MC, use_container_width=True)

st.markdown(
  """
  The implementations of $\Delta$ and $\Theta$ follow the same numerical method,
  a FDM with a central difference scheme vectorized by bumping the paths up 
  or down by a small number $h$. 

  It is possible to see from the $\Delta$ comparison below 
  that the vanilla and arithmetically averaged options show 
  a $\Delta$ behaviour similar to that seen for the BSM pricer and geometrically
  averaged options. 
  """
)

fig_vanilla_delta_MC_arith = build_delta_MC_arith(arithmetic_option_MC_greeks, vanilla_option_MC_greeks, t_step = t_step_in)
st.plotly_chart(fig_vanilla_delta_MC_arith, use_container_width=True)

# --- CONCLUSIONS ---
st.markdown("<h2>Conclusions </h2>", unsafe_allow_html=True)

st.markdown(
  """
  In this project, I have explored the development of quantitative pricers
  for vanilla (European) and average-value (Asian) options. 

  Starting by developing a BSM-based pricer for vanilla options, 
  I used it to also price geometrically averaged options,
  whose call option values have a closed-form solution in the BSM scenario.
  
  After that, I implemented a MC-based pricer for vanilla options.
  This MC model was, to a certain extent, validated it against the BSM pricer,
  and then adapted for arithmetically averaged options.
  These options do not have closed-form analytical solutions under a BSM-like scenario,
  and therefore require numerical solutions based on methods such as MC. 

  Preliminary comparisons between vanilla and arithmetically average options with the MC
  method show behaviour similar to that observed for vanilla and average-value options in the BSM model. 

  Further validation of the MC method and application of these options
  for risk mitigation in portfolios containing exotic options are the next steps.
  """
)

st.markdown("<h2>References </h2>", unsafe_allow_html=True)

st.markdown(
    """
    1. Hull, J. C. (2022). *Options, Futures, and Other Derivatives* (11th ed.). Pearson.

    2. Kemna, A. G. Z., & Vorst, A. C. F. (1990). A pricing method for options based on average asset values. *Journal of Banking & Finance, 14*(1), 113–129. [https://www.sciencedirect.com/science/article/abs/pii/0378426690900395](https://www.sciencedirect.com/science/article/abs/pii/0378426690900395)

    3. Glasserman, P. (2004). *Monte Carlo Methods in Financial Engineering*. Springer. [PDF](https://www.bauer.uh.edu/spirrong/Monte_Carlo_Methods_In_Financial_Enginee.pdf)

    4. Wikipedia contributors. Black–Scholes model. *Wikipedia*. [https://en.wikipedia.org/wiki/Black–Scholes_model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)

    5. SoFi Learn. Black-Scholes Model Explained: Definition and Formula. [https://www.sofi.com/learn/content/what-is-the-black-scholes-model/](https://www.sofi.com/learn/content/what-is-the-black-scholes-model/)
    """
)
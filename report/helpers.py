import streamlit as st
import plotly.graph_objects as go
import numpy as np
from option_pricer.vanilla import VanillaOptionBS
from option_pricer.vanilla import VanillaOptionMC
from option_pricer.average import ArithmeticOptionMC 


def build_payoffs(x, y, title, x_label="Spot Price", y_label = "Value"):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = x, y = y ,
        mode='lines',
        opacity=0.5
    ))
    fig.update_layout(
        xaxis_title = x_label,
        yaxis_title = y_label,
        title = title, 
        # legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.01)
    )

    return fig


def build_price_by_time(option, price, title = "", y_label = ""):

    fig = go.Figure()
    for i in range(0, price.shape[1]):
        fig.add_trace(go.Scatter(
            x=option.ts[:, i], y=price[:, i],
            mode='lines',
            name=f"S={option.Ss[0, i]:.1f}",
            opacity=0.5
        ))
    fig.update_layout(
        xaxis_title="Time to Expiry",
        yaxis_title=y_label,
        title = title
    )
    return fig


def build_price_by_S(option, price, title = "", y_label = ""):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=option.Ss[0, :], y=price[0, :],
        mode='lines',
        # name=f"S={option.Ss[0, i]:.1f}",
        opacity=0.5
    ))
    fig.update_layout(
        xaxis_title="Spot Option",
        yaxis_title=y_label,
        title = title
    )
    return fig


def build_delta(option, title = "", y_label = ""):

    delta = np.array(option.delta())
    # st.warning(f"{np.array(delta).shape}, {option.Ss.shape}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=option.Ss[0,:], y=delta[0, 0, :],
        mode='lines',
        name=f"t = 0",
        opacity=0.5
    ))

    N = int(len(option.ts)//1.05)
    fig.add_trace(go.Scatter(
        x=option.Ss[N,:], y=delta[0, N, :],
        mode='lines',
        name=f"t = {option.ts[N, -1]:3.2f}",
        opacity=0.5
    ))
    fig.add_trace(go.Scatter(
        x=option.Ss[-1,:], y=delta[0, -1, :],
        mode='lines',
        name=f"t = {option.ts[0, -1]}",
        opacity=0.5
    ))
    fig.update_layout(
        xaxis_title="Spot Price (S)",
        yaxis_title=r"Delta",
        title = title
    )
    return fig


def build_theta(option, title = "", y_label = ""):

    theta = np.array(option.theta())
    # st.warning(f"{theta.shape}, {option.ts.shape}")
    fig = go.Figure()
    for i in range(option.ts.shape[1]):
        fig.add_trace(go.Scatter(
            x=option.ts[:, i], y=theta[0, :, i],
            mode='lines',
            name=f"S = {option.Ss[0, i]:.2f}",
            opacity=0.5
        ))

    fig.update_layout(
        xaxis_title="Time to Expiry",
        yaxis_title="Theta",
        title = title
    )
    return fig


def build_geo_comp_t(vanilla_option, geometric_option):

    ts = vanilla_option.ts

    fig_t_call = go.Figure()
    fig_t_call.add_trace(go.Scatter(
        x=ts[:, 0], y=vanilla_option.call()[:, 0],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_t_call.add_trace(go.Scatter(
        x=ts[:, 0], y=geometric_option.call()[:, 0],
        mode='lines',
        name=f"Geometric Average",
        opacity=0.5
    ))
    fig_t_call.update_layout(
        xaxis_title="Time to Expiry",
        yaxis_title="Call"
    )

    fig_t_put = go.Figure()
    fig_t_put.add_trace(go.Scatter(
        x=ts[:, 0], y=vanilla_option.put()[:, 0],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_t_put.add_trace(go.Scatter(
        x=ts[:, 0], y=geometric_option.put()[:, 0],
        mode='lines',
        name=f"Geometric Average",
        opacity=0.5
    ))
    fig_t_put.update_layout(
        xaxis_title="Time to Expiry",
        yaxis_title="Put"
    )

    return fig_t_call, fig_t_put


def build_geo_comp_S(vanilla_option, geometric_option, t_step=0):

    Ss = vanilla_option.Ss
    # st.warning(f"{Ss.shape}")

    fig_t_call = go.Figure()
    fig_t_call.add_trace(go.Scatter(
        x=Ss[t_step, :], y=vanilla_option.call()[t_step, :],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_t_call.add_trace(go.Scatter(
        x=Ss[t_step, :], y=geometric_option.call()[t_step, :],
        mode='lines',
        name=f"Geometric Average",
        opacity=0.5
    ))
    fig_t_call.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Call"
    )

    fig_t_put = go.Figure()
    fig_t_put.add_trace(go.Scatter(
        x=Ss[t_step, :], y=vanilla_option.put()[t_step, :],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_t_put.add_trace(go.Scatter(
        x=Ss[t_step, :], y=geometric_option.put()[t_step, :],
        mode='lines',
        name=f"Geometric Average",
        opacity=0.5
    ))
    fig_t_put.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Put"
    )

    return fig_t_call, fig_t_put


def build_geo_greeks(vanilla_option, geometric_option, t_step=0):

    fig_delta = go.Figure()
    fig_delta.add_trace(go.Scatter(
        x=vanilla_option.Ss[t_step,:], y=np.array(vanilla_option.delta())[0, t_step, :],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_delta.add_trace(go.Scatter(
        x=vanilla_option.Ss[t_step,:], y=np.array(geometric_option.delta())[0, t_step, :],
        mode='lines',
        name=f"Geometric",
        opacity=0.5
    ))
    fig_delta.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Delta"
    )

    # x=option.ts[:, i], y=theta[0, :, i],

    fig_theta = go.Figure()
    fig_theta.add_trace(go.Scatter(
        x=vanilla_option.ts[:, 0], y=np.array(vanilla_option.theta())[0, :, 0],
        mode='lines',
        name=f"Vanilla",
        opacity=0.5
    ))
    fig_theta.add_trace(go.Scatter(
        x=geometric_option.ts[:, 0], y=np.array(geometric_option.theta())[0, :, 0],
        mode='lines',
        name=f"Geometric",
        opacity=0.5
    ))
    fig_theta.update_layout(
        xaxis_title="Time to Maturity",
        yaxis_title="Theta"
    )

    return fig_delta, fig_theta


def build_mc_paths_plot(sample_optionMC, average_type = None):

    time_axis = sample_optionMC.time_space
    n_steps = sample_optionMC.t_steps
    
    S_start = sample_optionMC.paths[0, 0, 0]
    num_paths_available = sample_optionMC.paths.shape[2]
    paths_to_plot = min(5, num_paths_available)

    if average_type == 'geometric':
        running_geo_avg = np.zeros(n_steps + 1)
        running_geo_avg[0] = S_start
        primary_path = sample_optionMC.paths[0, :, 0]
        
        for t in range(1, n_steps + 1):
            historical_segment = primary_path[1:t+1]
            running_geo_avg[t] = np.exp(np.mean(np.log(historical_segment)))

        running_avg = running_geo_avg
    
    else:
        running_avg = np.zeros(n_steps + 1)
        running_avg[0] = S_start
        for t in range(1, n_steps + 1):
            running_avg[t] = np.mean(sample_optionMC.paths[0, 1:t+1, 0])
        

    fig = go.Figure()

    for i in range(paths_to_plot):
        fig.add_trace(go.Scatter(
            x=time_axis, 
            y=sample_optionMC.paths[0, :, i], 
            mode='lines', 
            name=f"Path {i+1}", 
            opacity=0.4, 
            line=dict(width=1.5)
        ))

    fig.add_trace(go.Scatter(
        x=time_axis, 
        y=running_avg, 
        mode='lines', 
        name="Running Average (Path 1)", 
        line=dict(color='black', width=2.5, dash='dash')
    ))

    fig.update_layout(
        xaxis_title="Time to Maturity",
        yaxis_title="Asset Value",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Crimson Pro', size=16),
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#eaeaea')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#eaeaea')

    return fig


def build_price_by_time_MC(option_MC, option_BS, y_label):

    price = option_MC.call()
    # st.warning(f"{option_MC.time_space.shape}, {option_MC.S.shape} {np.array(option_MC.call()).shape}")
    fig = go.Figure()
    for i in range(np.array(option_MC.call()).shape[0]):
        fig.add_trace(go.Scatter(
            x=option_MC.time_space[:], y=price[i, :],
            mode='lines',
            name=f"S={option_MC.S[i]:.1f} (MC)",
            opacity=0.5
        ))

    price = option_BS.call()
    for i in range(0, price.shape[1]):
        fig.add_trace(go.Scatter(
            x=option_BS.ts[:, i], y=price[:, i],
            mode='lines',
            name=f"S={option_BS.Ss[0, i]:.1f} (BSM)",
            opacity=0.5
        ))
    fig.update_layout(
        xaxis_title="Time to Expiry",
        yaxis_title=y_label
    )
    return fig


def build_price_by_S_MC(option_MC, option_BS, y_label=None, t_step = 0):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=option_MC.S, y=option_MC.call()[:,t_step],
        mode='lines',
        name=f"MC",
        opacity=0.5
    ))

    mc_step = (option_BS.t_steps-1) - t_step
    price = option_BS.call()
    fig.add_trace(go.Scatter(
        x=option_BS.Ss[0, :], y=price[mc_step, :],
        mode='lines',
        name=f"BSM",
        opacity=0.5
    ))
    fig.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Value"
    )
    return fig


def build_delta_MC(option_MC, option_BS, t_step = 0):

    delta = np.array(option_BS.delta())
    # st.warning(f"{np.array(delta).shape}, {option.Ss.shape}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=option_BS.Ss[t_step,:], y=delta[0, t_step, :],
        mode='lines',
        name=f"BSM",
        opacity=0.5
    ))

    mc_step = (option_BS.t_steps-1) - t_step
    # st.warning(f"{mc_step}, {t_step}")
    fig.add_trace(go.Scatter(
        x=option_MC.S, y=option_MC.delta()[:,mc_step],
        mode='lines',
        name=f"MC",
        opacity=0.5
    ))

    fig.update_layout(
        xaxis_title="Spot Price (S)",
        yaxis_title=r"Delta"
    )

    return fig


def build_delta_MC_arith(option_MC, option_MC2, t_step = 0):

    mc_step = (option_MC.t_steps-1) - t_step

    fig = go.Figure()

    # st.warning(f"{mc_step}, {t_step}")
    fig.add_trace(go.Scatter(
        x=option_MC.S, y=option_MC.delta()[:,mc_step],
        mode='lines',
        name=f"Arithmetically Averaged (MC)",
        opacity=0.5
    ))

    fig.add_trace(go.Scatter(
        x=option_MC2.S, y=option_MC2.delta()[:,mc_step],
        mode='lines',
        name=f"Vanilla (MC)",
        opacity=0.5
    ))

    fig.update_layout(
        xaxis_title="Spot Price (S)",
        yaxis_title=r"Delta"
    )

    return fig


def build_call_MC_arith(option_MC, option_MC2, t_step = 0):

    mc_step = (option_MC.t_steps-1) - t_step

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=option_MC2.S, y=option_MC2.call()[:,mc_step],
        mode='lines',
        name=f"Vanilla (MC)",
        opacity=0.5
    ))


    # st.warning(f"{mc_step}, {t_step}")
    fig.add_trace(go.Scatter(
        x=option_MC.S, y=option_MC.call()[:,mc_step],
        mode='lines',
        name=f"Arithmetically Averaged (MC)",
        opacity=0.5
    ))

    fig.update_layout(
        xaxis_title="Spot Price (S)",
        yaxis_title=r"Call"
    )

    return fig
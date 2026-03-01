import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

st.title("Damped Oscillator")

fixed_x, fixed_y= 0,5

col1, col2 = st.columns(2)

pendulum_placeholder = col1.empty()
graph_placeholder = col2.empty()

gamma = st.number_input("Enter the value of gamma: ", min_value=0.00, max_value=50.00, value=0.15)
angle = st.number_input("Enter the release angle (degrees): ", min_value=-90.0, max_value=90.0, value=-15.0)
length = 5
g = 9.78
dt = 0.05

theta = np.pi*angle / 180
omega = 0
current_time = 0

time_vals = []
theta_vals = []

for _ in range(500):

    alpha = (-g / length) * np.sin(theta) - (gamma * omega)
    omega += alpha * dt
    theta += omega * dt

    # ---- Pendulum Plot (Plotly) ----
    x = fixed_x+length * np.sin(theta)
    y = fixed_y-length * np.cos(theta)

    

    fig_pendulum = go.Figure()
    
    fig_pendulum.add_trace(go.Scatter(
        x=[fixed_x, x],
        y=[fixed_y, y],
        mode="lines+markers"
    ))
    fig_pendulum.update_layout(
        xaxis=dict(range=[-6,6]),
        yaxis=dict(range=[-6,6], scaleanchor="x"),
        showlegend=False
    )
    fig_pendulum.add_shape(
    type="line",
    x0=0, x1=0,
    y0=-6, y1=6,
    line=dict(color="gray", width=0.8, dash="dash")
    )
    fig_pendulum.add_shape(
        type="line",
        x0=-6, x1=6,
        y0=0, y1=0,
        line=dict(color="gray", width=0.8, dash="dash")
    )

    pendulum_placeholder.plotly_chart(fig_pendulum, use_container_width=True)

    # ---- Oscillation Graph ----
    time_vals.append(current_time)
    theta_vals.append(theta)

    fig2, ax = plt.subplots()
    ax.plot(time_vals, theta_vals)
    ax.axhline(0)
    ax.set_xlabel("Time")
    ax.set_ylabel("Theta")

    graph_placeholder.pyplot(fig2)

    current_time += dt
    time.sleep(dt)

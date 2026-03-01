import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Damped Oscillator")

gamma = st.number_input("Gamma", 0.0, 50.0, 0.15)
angle = st.number_input("Release Angle (degrees)", -90.0, 90.0, -15.0)

length = 5
g = 9.78
dt = 0.05
steps = 300

theta = np.pi * angle / 180
omega = 0

time_vals = []
theta_vals = []
x_vals = []
y_vals = []

for i in range(steps):
    alpha = (-g/length) * np.sin(theta) - gamma * omega
    omega += alpha * dt
    theta += omega * dt
    
    time_vals.append(i*dt)
    theta_vals.append(theta)
    
    x_vals.append(length*np.sin(theta))
    y_vals.append(-length*np.cos(theta))

# ---- Create animation frames ----
frames = []

for i in range(steps):
    frames.append(
        go.Frame(
            data=[
                go.Scatter(x=[0, x_vals[i]], y=[0, y_vals[i]], mode="lines+markers")
            ]
        )
    )

fig = go.Figure(
    data=[go.Scatter(x=[0, x_vals[0]], y=[0, y_vals[0]], mode="lines+markers")],
    layout=go.Layout(
        xaxis=dict(range=[-6,6]),
        yaxis=dict(range=[-6,6], scaleanchor="x"),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])]
        )]
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)

st.line_chart({"theta": theta_vals})

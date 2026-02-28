import plotly.graph_objects as go
import numpy as np
import streamlit as st

# --- Setup ---
st.title("Damped Pendulum")
gamma = st.number_input("Enter the value of gamma: ", min_value=0.0, value=0.1)
angle = st.number_input("Enter the value of the release angle (degrees) : ",min_value=-90.0, max_value=90.0, value=-15.0)

length = 5
fixed_x, fixed_y = 0, 5
g = 9.78
dt = 0.05

if st.button("Simulate"):

    # --- 1. Pre-compute all frames (no rendering here) ---
    theta = np.pi*angle/180
    omega = 0
    frames_x, frames_y = [], []

    for _ in range(1000):
        alpha = (-g / length) * np.sin(theta) - (gamma * omega)
        omega += alpha * dt
        theta += omega * dt

        frames_x.append(fixed_x + length * np.sin(theta))
        frames_y.append(fixed_y - length * np.cos(theta))

        if abs(omega) < 0.01 and abs(theta) < 0.01:
            break

    # --- 2. Build a Plotly figure with all frames baked in ---
    fig_frames = []
    for x, y in zip(frames_x, frames_y):
        fig_frames.append(go.Frame(data=[
            go.Scatter(x=[fixed_x, x], y=[fixed_y, y],
                       mode="lines", line=dict(color="black", width=2)),
            go.Scatter(x=[fixed_x, x], y=[fixed_y, y],
                       mode="markers",
                       marker=dict(color=["black", "red"], size=[12, 18])),
        ]))

    fig = go.Figure(
        data=[
            go.Scatter(x=[fixed_x, frames_x[0]], y=[fixed_y, frames_y[0]],
                       mode="lines", line=dict(color="white", width=2)),
            go.Scatter(x=[fixed_x, frames_x[0]], y=[fixed_y, frames_y[0]],
                       mode="markers",
                       marker=dict(color=["black", "red"], size=[12, 18])),
        ],
        layout=go.Layout(
            xaxis=dict(range=[-6, 6], scaleanchor="y"),
            yaxis=dict(range=[-1, 6]),
            showlegend=False,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(
                    label="Play",
                    method="animate",
                    args=[None, dict(frame=dict(duration=50, redraw=True),
                                    fromcurrent=True)]
                )]
            )]
        ),
        frames=fig_frames,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(f"Simulation complete — {len(frames_x)} frames")

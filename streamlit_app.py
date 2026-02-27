import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import time as t

# --- Setup ---
st.title("Damped Pendulum")
gamma = st.number_input("Enter the value of gamma: ")
length = 5
fixed_x, fixed_y = 0, 5
g = 9.78
dt = 0.05

# Initial State
theta = np.pi/6
omega = 0

# --- Streamlit Placeholder for Animation ---
plot_placeholder = st.empty() 

if st.button('Simulate'):
    # Create the figure once outside the loop
    fig, ax = plt.subplots()
    
    # We use a simple loop; Streamlit runs this until completion
    for _ in range(1000):  # Using a range for a set duration
        # Physics Engine (Euler-Cromer)
        alpha = (-g/length) * np.sin(theta) - (gamma * omega)
        omega += alpha * dt
        theta += omega * dt

        x = fixed_x + length * np.sin(theta)
        y = fixed_y - length * np.cos(theta)

        if abs(omega)<0.01 and abs(theta)<0.01:
            st.write("All done")
            break

        # Rendering
        ax.cla()
        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 6)
        ax.set_aspect('equal')
        
        # Draw Pendulum
        ax.plot([fixed_x, x], [fixed_y, y], color='black', linewidth=2)
        ax.scatter(fixed_x, fixed_y, color='black', zorder=5) # Pivot
        ax.scatter(x, y, color='red', s=100, zorder=5)       # Bob
        
        # Update the placeholder with the current frame
        plot_placeholder.pyplot(fig)
        
        # Control animation speed
        t.sleep(0.02) 

    st.write("Simulation Finished!")

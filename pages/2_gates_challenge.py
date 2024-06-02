import streamlit as st 
from streamlit_multipage import MultiPage
import numpy as np 
import qutip as qt
import plotly.graph_objects as go
from quantum_simulator import run_quantum_simulation



def add_square(pulse_vector, amplitude, start, stop, n_steps, t_final):
    """
    Adds a Square pulse to the pulse vector.
    """
    tlist = np.linspace(0, t_final, n_steps)
    square_pulse = np.where((tlist >= start) & (tlist <= stop), amplitude, 0)
    # Extend pulse_vector to match the length of square_pulse
    if len(pulse_vector) < len(square_pulse):
        pulse_vector = np.pad(pulse_vector, (0, len(square_pulse) - len(pulse_vector)), 'constant')
    return np.clip(pulse_vector + square_pulse, -1, 1)

# _________________________________ (Misc Functions) ___________________________________

def default_params():
    # These are default parameters that do not need to be changed for challenge mode
    omega_q = 5.000 # Default qubit frequency is 5.000 GHz
    omega_d = 5.000 # Default drive frequency is 5.000 
    omega_rabi = 50.000 # Default Rabi frequency is 50.000 MHz
    t_final = 200 # Default total time for each simulation is 200 ns
    T1 = 100000000000 # Default relaxation time constant
    T2 = 200000000000 # Default dephasing time constant from 0 to 1000.0 ns
    detuning = 0
    n_steps = 20*int(t_final) # set the number of steps based on user inputs times 20
    num_shots = 256 # set the number of shots to 256
    # Create a list of time values from 0 to t_final
    time_values = np.linspace(0, t_final, n_steps)

    return omega_q, omega_d, omega_rabi, t_final, T1, T2, detuning, n_steps, num_shots, time_values

def menu_buttons():
    import streamlit as st

    with st.container():
        col1, col2, col3, col4 = st.columns(4)

        # TODO: Add on-click functionalities for these buttons
        with col1:
            st.button("TUTORIAL", type="secondary", use_container_width=True)
        with col2:
            st.button("GATE CHALLENGE", type="secondary", use_container_width=True)
        with col3:
            st.button("PULSE CHALLENGE", type="secondary", use_container_width=True)
        with col4:
            st.button("LEVELS", type="secondary", use_container_width=True)

def gates_buttons():
    import streamlit as st
    
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("X-Gate", type="secondary", use_container_width=True)
        with col2:
            st.button("Y-Gate", type="secondary", use_container_width=True)
        with col3:
            st.button("UNDO", type="secondary", use_container_width=True)

def click_button():
    st.session_state.clicked = True

# _________________________________ (Key Functions) ____________________________________

def tutorial_page_1(time_values, t_final):
    import streamlit as st

    with st.container():
        page_text = 'It is commonly known that most computers are told what to do through “binary.” Transistors in classical computation process a string of 1’s and 0’s. to perform computations. :red[Quantum Computation] uses qubits instead of transistors to read 1’s and 0’s. To do a bit flip, we have to use “:red[gates]” to change the state.'
        st.markdown(page_text, unsafe_allow_html=False) # TODO: Add colour to background of container
        
        _, _, _, col4 = st.columns(4)
        with col4:
            st.button("NEXT", type="secondary", use_container_width=True, on_click=click_button)
        
        bloch_sphere(time_values, t_final)
    


def tutorial_page_2(placeholder):
    import streamlit as st

    with st.container():
        page_text = 'Let’s perform a bit flip! Navigate from 0 to 1 using an X-Gate'
        st.text_area(label="text", value=page_text, label_visibility="hidden", height=20)

def tutorial_page_3():
    import streamlit as st

    with st.container():
        page_text = 'Great Job! An X-Gate flips the state from 0 to 1 by rotating about the x-axis.'
        st.text_area(label="text", value=page_text, label_visibility="hidden", height=20) # TODO: Add colour to background of container

        _, _, _, col4 = st.columns(4)
        with col4:
            st.button("NEXT", type="secondary", use_container_width=True)

def tutorial_page_4():
    import streamlit as st

    with st.container():
        page_text = 'Try navigating from 1 back to 0.'
        st.text_area(label="text", value=page_text, label_visibility="hidden", height=20)

def bloch_sphere(time_values, t_final):
    # Bloch Sphere - Creating a meshgrid for the Bloch Sphere 
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x_sphere = np.cos(u) * np.sin(v)
    y_sphere = np.sin(u) * np.sin(v)
    z_sphere = np.cos(v)

    # Bloch Sphere - Color map for the time evolution
    colors = time_values

    fig_bloch = go.Figure(data=[
        go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.3),
        go.Scatter3d(
        mode='markers',
        marker=dict(
            size=6,
            color=colors,
            opacity=0.8,
            colorscale='inferno',
            colorbar=dict(title='Time', tickvals=[0, t_final], ticktext=[0, t_final])
           )  # Use time-based colors
       )
   ])
    
    # Bloch Sphere - this is the default layout
    fig_bloch.update_layout(
    title='State Vector on the Bloch Sphere',
    scene=dict(
        xaxis_title=dict(text="σ_x"),
        yaxis_title=dict(text="σ_y"),
        zaxis_title=r'σ_z',
        xaxis=dict(range=[-1, 1]),
        yaxis=dict(range=[-1, 1]),
        zaxis=dict(range=[-1, 1]),
        ),
    margin=dict(l=0, r=0, b=0, t=0)
   )

    # Bloch Sphere - this sets the starting point of the Bloch Sphere
               
    fig_bloch.add_trace(go.Scatter3d(
        x=[0, 0], 
        y=[0, 0], 
        z=[1.0, -1.0], 
        mode='text',
        text=["|1⟩", "|0⟩"],
        textposition=["top center","bottom center"],
        textfont=dict(
        color=["white", "white"],
        size=20
        )
       ))
    
     # Display the plot
    st.plotly_chart(fig_bloch)

def x_gate(omega_rabi, omega_q, omega_d, num_shots, T1, T2):
    # Rough Draft of X-Gate Button
    if st.button("X-Gate"):
        st.session_state.sigma_x_vec = np.zeros(n_steps)
        st.session_state.sigma_y_vec = np.zeros(n_steps)
        t_final = 200
        n_steps = 25 * t_final
        tlist = np.linspace(0, t_final, n_steps)
        plot_lw = 3
        # Initialize or retrieve sigma_x_vec and sigma_y_vec

        if 'sigma_x_vec' not in st.session_state:
           st.session_state.sigma_x_vec = 0*tlist
        if 'sigma_y_vec' not in st.session_state:
           st.session_state.sigma_y_vec = 0*tlist
        target_channel = "σ_x"
        amp = 1.0
        start = 0.0
        stop = (1 * 10**9)/(omega_rabi * 10**6) # Half the period of the Rabi oscillation
        
        pulse_vector = st.session_state.sigma_x_vec
        updated_pulse_vector = add_square(pulse_vector, amp, start, stop, n_steps, t_final)
        st.session_state.sigma_x_vec = updated_pulse_vector
        st.session_state.sigma_y_vec = np.pad(st.session_state.sigma_y_vec, (0, len(updated_pulse_vector) - len(st.session_state.sigma_y_vec)), 'constant', constant_values=st.session_state.sigma_y_vec[-1])
       
        params = (omega_q, omega_rabi*1e-3, t_final, n_steps, omega_d, st.session_state.sigma_x_vec, st.session_state.sigma_y_vec, num_shots, T1, T2)
        try:
            exp_values, __, sampled_probabilities = run_quantum_simulation(*params)
        except Exception as e:
            st.warning(f"An error occurred. Please refresh the page and try again: {e}")
        # Time array for transformation
        time_array = np.linspace(0, t_final, n_steps)  # Convert time to microseconds
        # Demodulate the expectation values
        exp_y_rotating = -(exp_values[0] * np.cos(2 * np.pi * omega_d * time_array) + exp_values[1] * np.sin(2 * np.pi * omega_d * time_array))
        exp_x_rotating = exp_values[0] * np.sin(2 * np.pi * omega_d * time_array) - exp_values[1] * np.cos(2 * np.pi * omega_d * time_array)

        # plotting the bloch sphere 
        time_values = np.linspace(0, t_final, n_steps) # create list of time values 
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j] # create a meshgrid of u and v values
        x_sphere = np.cos(u) * np.sin(v) # set x values of the sphere
        y_sphere = np.sin(u) * np.sin(v) # set y values of the sphere
        z_sphere = np.cos(v)
        colors = time_values # set colors to time values
   
        fig_bloch = go.Figure(data=[
          go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.3),
               go.Scatter3d(
                   x=exp_x_rotating,  # ⟨σ_x⟩ values
                   y=exp_y_rotating,  # ⟨σ_y⟩ values
                   z=exp_values[2],  # ⟨σ_z⟩ values
                   mode='markers',
                   marker=dict(
                       size=6,
                       color=colors,
                       opacity=0.8,
                        colorscale='inferno',
                        colorbar=dict(title='Time', tickvals=[0, t_final], ticktext=[0, t_final])
                    )  # Use time-based colors
                )
            ])
                    
        fig_bloch.update_layout(title='State Vector on the Bloch Sphere',
               scene=dict(
                   xaxis_title=dict(text="σ_x"),
                   yaxis_title=dict(text="σ_y"),
                   zaxis_title=r'σ_z',
                   xaxis=dict(range=[-1, 1]),
                   yaxis=dict(range=[-1, 1]),
                   zaxis=dict(range=[-1, 1]),
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )
                    
        fig_bloch.add_trace(go.Scatter3d(
            x=[0, 0], 
            y=[0, 0], 
            z=[1.0, -1.0], 
            mode='text',
            text=["|1⟩", "|0⟩"],
            textposition=["top center","bottom center"],
            textfont=dict(
                color=["white", "white"],
                size=20
                )
        ))
        # Display the plot
        st.plotly_chart(fig_bloch)

def y_gate(omega_rabi, omega_q, omega_d, num_shots, T1, T2):
    # Rough Draft of Y-Gate Button
    if st.button("Y-Gate"):
        st.session_state.sigma_x_vec = np.zeros(n_steps)
        st.session_state.sigma_y_vec = np.zeros(n_steps)
        t_final = 200
        n_steps = 25 * t_final
        tlist = np.linspace(0, t_final, n_steps)
        plot_lw = 3
        # Initialize or retrieve sigma_x_vec and sigma_y_vec
        if 'sigma_x_vec' not in st.session_state:
            st.session_state.sigma_x_vec = 0*tlist
        if 'sigma_y_vec' not in st.session_state:
            st.session_state.sigma_y_vec = 0*tlist

        target_channel = "σ_y"
        amp = 1.0
        start = 0.0
        stop = int((1 * 10**9)/(50 * 10**6)) # Half the period of the Rabi oscillation
        
        pulse_vector = st.session_state.sigma_y_vec
        updated_pulse_vector = add_square(pulse_vector, amp, start, stop, n_steps, t_final)
        st.session_state.sigma_y_vec = updated_pulse_vector
        st.session_state.sigma_x_vec = np.pad(st.session_state.sigma_x_vec, (0, len(updated_pulse_vector) - len(st.session_state.sigma_x_vec)), 'constant', constant_values=st.session_state.sigma_x_vec[-1])

        params = (omega_q, omega_rabi*1e-3, t_final, n_steps, omega_d, st.session_state.sigma_x_vec, st.session_state.sigma_y_vec, num_shots, T1, T2)

        try:
            exp_values, __, sampled_probabilities = run_quantum_simulation(*params)
        except Exception as e:
            st.warning(f"An error occurred. Please refresh the page and try again: {e}")

        # Time array for transformation
        time_array = np.linspace(0, t_final, n_steps)  # Convert time to microseconds

        # Demodulate the expectation values
        exp_y_rotating = -(exp_values[0] * np.cos(2 * np.pi * omega_d * time_array) + exp_values[1] * np.sin(2 * np.pi * omega_d * time_array))
        exp_x_rotating = exp_values[0] * np.sin(2 * np.pi * omega_d * time_array) - exp_values[1] * np.cos(2 * np.pi * omega_d * time_array)


        # plotting the bloch sphere 
        time_values = np.linspace(0, t_final, n_steps) # create list of time values 
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j] # create a meshgrid of u and v values
        x_sphere = np.cos(u) * np.sin(v) # set x values of the sphere
        y_sphere = np.sin(u) * np.sin(v) # set y values of the sphere
        z_sphere = np.cos(v)

        colors = time_values # set colors to time values
    
        fig_bloch = go.Figure(data=[
            go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.3),
                go.Scatter3d(
                    x=exp_x_rotating,  # ⟨σ_x⟩ values
                    y=exp_y_rotating,  # ⟨σ_y⟩ values
                    z=exp_values[2],  # ⟨σ_z⟩ values
                    mode='markers',
                    marker=dict(
                        size=6,
                        color=colors,
                        opacity=0.8,
                        colorscale='inferno',
                        colorbar=dict(title='Time', tickvals=[0, t_final], ticktext=[0, t_final])
                    )  # Use time-based colors
                )
            ])
                    
        fig_bloch.update_layout(title='State Vector on the Bloch Sphere',
                scene=dict(
                    xaxis_title=dict(text="σ_x"),
                    yaxis_title=dict(text="σ_y"),
                    zaxis_title=r'σ_z',
                    xaxis=dict(range=[-1, 1]),
                    yaxis=dict(range=[-1, 1]),
                    zaxis=dict(range=[-1, 1]),
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )
                    
        fig_bloch.add_trace(go.Scatter3d(
            x=[0, 0], 
            y=[0, 0], 
            z=[1.0, -1.0], 
            mode='text',
            text=["|1⟩", "|0⟩"],
            textposition=["top center","bottom center"],
            textfont=dict(
                color=["white", "white"],
                size=20
                )
        ))
        # Display the plot
        st.plotly_chart(fig_bloch)


# _________________________________ (Pages) ____________________________________________

def tutorial_page(time_values, t_final):
    import streamlit as st

    st.subheader("LEVEL 1: PAULI GATES - TUTORIAL")

    placeholder = st.empty()
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    with placeholder.container():
        tutorial_page_1(time_values, t_final)
        
    if st.session_state.clicked:
        placeholder.empty()
        st.session_state.clicked = False
        st.write("Page 2")
    
    



# ________________________________ (Main) _____________________________________________

def main():
    
    st.title("Challenge Mode")

    menu_buttons()

    omega_q, omega_d, omega_rabi, t_final, T1, T2, detuning, n_steps, num_shots, time_values = default_params() # default parameters

    tutorial_page(time_values, t_final) # TODO: At the end order these input params properly
    # ___________________________________________________________
    
    # gates_buttons()

    # ____________________________________________________________

    

if __name__ == "__main__":
    main()
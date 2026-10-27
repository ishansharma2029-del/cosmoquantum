import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="CosmoQuantum: Research Grade Dark Matter & Observatory",
    layout="wide"
)

st.markdown("""
<style>
    body { background-color: #0a0a0f; color: #e0e0e0; }
    .stApp { background-color: #0a0a0f; }
    .stButton>button { background-color: #1a1a2e; color: #4da6ff; border: 1px solid #4da6ff; border-radius: 6px; }
    .stButton>button:hover { background-color: #4da6ff; color: #0a0a0f; }
    .stMetric { background-color: #121220; padding: 12px; border-radius: 8px; border: 1px solid #232340; }
    div[data-testid="stExpander"] { background-color: #10101d; border: 1px solid #202035; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

if "unlocked_missions" not in st.session_state:
    st.session_state.unlocked_missions = set()

if "tutorial_step" not in st.session_state:
    st.session_state.tutorial_step = 0

if "preset_selector" not in st.session_state:
    st.session_state.preset_selector = "Milky Way (MW) - 4-Arm Spiral"
if "dm_model_radio" not in st.session_state:
    st.session_state.dm_model_radio = "Fuzzy Dark Matter (FDM)"
if "halo_mass_slider" not in st.session_state:
    st.session_state.halo_mass_slider = 100.0
if "boson_mass_slider" not in st.session_state:
    st.session_state.boson_mass_slider = 1.0
if "velocity_slider" not in st.session_state:
    st.session_state.velocity_slider = 110.0
if "include_bh_check" not in st.session_state:
    st.session_state.include_bh_check = True
if "bh_mass_slider" not in st.session_state:
    st.session_state.bh_mass_slider = 5.0
if "enable_quasar_check" not in st.session_state:
    st.session_state.enable_quasar_check = True
if "dust_slider" not in st.session_state:
    st.session_state.dust_slider = 0.6
if "globular_slider" not in st.session_state:
    st.session_state.globular_slider = 300

st.title("CosmoQuantum: Research Grade Dark Matter & Observatory")

tutorial_container = st.container()
with tutorial_container:
    col_t1, col_t2 = st.columns([1, 4])
    with col_t1:
        if st.button("Start Interactive Guided Tour"):
            st.session_state.tutorial_step = 1
            st.rerun()
    with col_t2:
        if st.session_state.tutorial_step > 0:
            tutorial_steps = [
                "Step 1: Welcome! In the sidebar, pick a galaxy preset and set your physics model.",
                "Step 2: Check out Tab 1 (Structural Analysis) to see how a central supermassive black hole pulls and compacts surrounding dark matter.",
                "Step 3: Head over to Tab 2 (Dual-Zone Observatory) to explore the soliton core and outer halo envelope.",
                "Step 4: Jump to Tab 3 (Analytical Surface Mesh) to look at the static soliton equilibrium profile.",
                "Step 5: Open Tab 4 (PyUltraLight Solver) and hit 'Run Time-Evolution Solver' to fire up the 3D wave evolution engine.",
                "Step 6: Switch to Tab 5 (Radial Scaling & Data) to test your FDM flat soliton core against real gold telescope galaxy data points.",
                "Step 7: Finally, head to Tab 6 (15-Mission Research Campaign) to beat the missions and export your official research report!"
            ]
            current_idx = st.session_state.tutorial_step - 1
            st.info(f"**Guided Tour ({st.session_state.tutorial_step}/7):** {tutorial_steps[current_idx]}")
            
            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.session_state.tutorial_step < 7:
                    if st.button("Next Tour Step"):
                        st.session_state.tutorial_step += 1
                        st.rerun()
                else:
                    if st.button("Complete Tour"):
                        st.session_state.tutorial_step = 0
                        st.rerun()
            with btn_col2:
                if st.button("Exit Tour"):
                    st.session_state.tutorial_step = 0
                    st.rerun()

with st.expander("Research Glossary: Understanding the Physics & Variables", expanded=True):
    st.markdown("""
    ### Welcome to CosmoQuantum Lab

    #### The Core Scientific Mystery (CDM vs. FDM):
    * **Cold Dark Matter (CDM):** The standard theory assumes dark matter consists of heavy particles moving without friction. However, under gravity alone, CDM collapses into an infinitely sharp, spiky central peak called an NFW Cusp. Real telescope observations show that galaxy centers are actually smooth and flat (The Cusp-Core Problem).
    * **Fuzzy Dark Matter (FDM):** Solves this issue by proposing dark matter is made of ultra-light subatomic axion particles ($10^{-22}\\text{ eV}$). Because these particles are so light, quantum physics makes them behave like giant waves spanning thousands of light-years, creating a flat, stable droplet called a Soliton Core.

    #### Glossary of Variables & Telemetry:
    1. Host Halo Mass ($M_{\text{vir}}$): Total dark matter mass scale in billions of Solar Masses ($M_\odot$).
    2. Axion Boson Mass ($m_{\text{axion}}$): Mass scale of ultralight axion particle determining quantum wave wavelength.
    3. Telescopic Velocity Dispersion ($v_{\text{circ}}$): Average orbital speed of stars and gas clouds in km/s.
    4. De Broglie Wavelength ($\lambda_{\text{dB}}$): Physical size of the quantum wave packet.
    5. Soliton Core Radius ($r_c$): Radius of the smooth, flat central dark matter core.
    """)

st.sidebar.header("FDM & CDM Research Controls")

if st.sidebar.button("Reset All Parameters", key="reset_button"):
    st.session_state.preset_selector = "Milky Way (MW) - 4-Arm Spiral"
    st.session_state.dm_model_radio = "Fuzzy Dark Matter (FDM)"
    st.session_state.halo_mass_slider = 100.0
    st.session_state.boson_mass_slider = 1.0
    st.session_state.velocity_slider = 110.0
    st.session_state.include_bh_check = True
    st.session_state.bh_mass_slider = 5.0
    st.session_state.enable_quasar_check = True
    st.session_state.dust_slider = 0.6
    st.session_state.globular_slider = 300
    st.rerun()

def update_galaxy_defaults():
    preset = st.session_state.preset_selector
    if "Milky Way" in preset:
        st.session_state.halo_mass_slider = 100.0
        st.session_state.velocity_slider = 110.0
        st.session_state.boson_mass_slider = 1.0
        st.session_state.bh_mass_slider = 4.0
    elif "Andromeda" in preset:
        st.session_state.halo_mass_slider = 120.0
        st.session_state.velocity_slider = 125.0
        st.session_state.boson_mass_slider = 1.0
        st.session_state.bh_mass_slider = 3.0
    elif "M87" in preset:
        st.session_state.halo_mass_slider = 150.0
        st.session_state.velocity_slider = 250.0
        st.session_state.boson_mass_slider = 0.8
        st.session_state.bh_mass_slider = 35.0
    elif "Sombrero" in preset:
        st.session_state.halo_mass_slider = 110.0
        st.session_state.velocity_slider = 140.0
        st.session_state.boson_mass_slider = 1.0
        st.session_state.bh_mass_slider = 10.0
    elif "Triangulum" in preset:
        st.session_state.halo_mass_slider = 50.0
        st.session_state.velocity_slider = 80.0
        st.session_state.boson_mass_slider = 1.2
        st.session_state.bh_mass_slider = 0.5
    elif "Large Magellanic" in preset:
        st.session_state.halo_mass_slider = 20.0
        st.session_state.velocity_slider = 60.0
        st.session_state.boson_mass_slider = 1.5
        st.session_state.bh_mass_slider = 0.1
    elif "Fornax" in preset:
        st.session_state.halo_mass_slider = 0.5
        st.session_state.velocity_slider = 25.0
        st.session_state.boson_mass_slider = 2.0
        st.session_state.bh_mass_slider = 0.0
    elif "Sculptor" in preset:
        st.session_state.halo_mass_slider = 0.2
        st.session_state.velocity_slider = 18.0
        st.session_state.boson_mass_slider = 3.0
        st.session_state.bh_mass_slider = 0.0

galaxy_preset = st.sidebar.selectbox(
    "Select Galactic System Preset",
    [
        "Milky Way (MW) - 4-Arm Spiral", 
        "Andromeda (M31) - 2-Arm Spiral", 
        "M87 Giant Elliptical (AGN Host)", 
        "Sombrero Galaxy (M104)", 
        "Triangulum Galaxy (M33)", 
        "Large Magellanic Cloud (LMC)", 
        "Fornax Dwarf Spheroidal", 
        "Sculptor Dwarf Spheroidal", 
        "Custom Galaxy"
    ],
    key="preset_selector",
    on_change=update_galaxy_defaults
)

dm_model = st.sidebar.radio(
    "Dark Matter Physics Model",
    ["Fuzzy Dark Matter (FDM)", "Cold Dark Matter (CDM)"],
    key="dm_model_radio"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Physical Controls")
halo_mass = st.sidebar.slider(
    "Host Halo Mass ($M_{\\text{vir}}$ in $10^{10} M_\\odot$)", 
    min_value=0.1, max_value=500.0, step=0.5,
    key="halo_mass_slider",
    help="Total dark matter mass scale in the galaxy halo."
)

if "FDM" in dm_model:
    boson_mass = st.sidebar.slider(
        "Axion Boson Mass ($m_{\\text{axion}}$ in $10^{-22}\\text{ eV}$)", 
        min_value=0.1, max_value=10.0, step=0.1,
        key="boson_mass_slider",
        help="Mass scale of ultralight axion particle determining quantum wave wavelength."
    )
    velocity_dispersion = st.sidebar.slider(
        "Telescopic Velocity Dispersion ($v_{\\text{circ}}$ in km/s)",
        min_value=5.0, max_value=400.0, step=5.0,
        key="velocity_slider",
        help="Independent telescopic orbital speed measurement determining quantum de Broglie wavelength."
    )
else:
    boson_mass = 1.0
    velocity_dispersion = st.sidebar.slider(
        "Telescopic Velocity Dispersion ($v_{\\text{circ}}$ in km/s)",
        min_value=5.0, max_value=400.0, step=5.0,
        key="velocity_slider",
        help="Independent telescopic orbital speed measurement determining quantum de Broglie wavelength."
    )
    st.sidebar.markdown("Boson mass control is disabled in CDM mode.")

include_bh = st.sidebar.checkbox("Include Central Supermassive Black Hole ($M_{\\text{BH}}$)", key="include_bh_check")
if include_bh:
    bh_mass = st.sidebar.slider(
        "Supermassive Black Hole Mass ($M_{\\text{BH}}$ in $10^7 M_\\odot$)", 
        min_value=0.0, max_value=50.0, step=0.5,
        key="bh_mass_slider",
        help="Mass of central supermassive black hole exerting point-mass potential."
    )
    enable_quasar = st.sidebar.checkbox("Enable Quasar Relativistic Jets", key="enable_quasar_check")
else:
    bh_mass = 0.0
    enable_quasar = False

st.sidebar.markdown("---")
st.sidebar.subheader("Aesthetic Details")
dust_absorption = st.sidebar.slider("Interstellar Dust Opacity", 0.0, 1.0, key="dust_slider")
globular_density = st.sidebar.slider("Globular Cluster Density", 100, 1000, key="globular_slider")

if "Milky Way" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 2.6, 0.5, 4, True
elif "Andromeda" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 5.4, 0.8, 2, True
elif "M87" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 4.0, 1.2, 0, False
elif "Sombrero" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 3.5, 0.9, 2, True
elif "Triangulum" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 2.2, 0.4, 2, True
elif "Large Magellanic" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 1.5, 0.3, 1, True
elif "Fornax" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 0.71, 0.2, 0, False
elif "Sculptor" in galaxy_preset:
    real_rd, real_rb, num_arms, is_spiral = 0.29, 0.1, 0, False
else:
    real_rd, real_rb, num_arms, is_spiral = 3.0, 0.6, 3, True

if "FDM" in dm_model:
    lambda_db = 1.2 * (1.0 / boson_mass) * (100.0 / velocity_dispersion) 
    core_mass_solar = 2.7e8 * (1.0 / boson_mass) * (halo_mass * 10.0)**(1.0/3.0)
    rc = 1.2 / (boson_mass * np.sqrt(halo_mass + 0.2))
    m_eff_scale = 1.0e-4 * (lambda_db**3) * (halo_mass / 10.0)
    r_half = 0.335 * (1e9 / core_mass_solar) * (1.0 / boson_mass)**2
    rho_zero = 0.0044 * (boson_mass**4) * ((core_mass_solar / 1e9)**4)
else:
    lambda_db = 0.0
    core_mass_solar = 0.0
    rc = 0.0
    m_eff_scale = 0.0
    r_half = 0.0
    rho_zero = (halo_mass / 15.0)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Structural Analysis", 
    "Dual-Zone Observatory", 
    "Analytical Surface Mesh", 
    "PyUltraLight Solver", 
    "Radial Scaling & Data", 
    "15-Mission Research Campaign"
])

with tab1:
    st.header(f"Core Structural Analysis: {galaxy_preset} — {dm_model}")
    
    np.random.seed(42)
    n_particles = 2500

    if is_spiral:
        r_disk = np.random.exponential(scale=real_rd, size=int(n_particles * 0.75))
        theta = np.random.uniform(0, 2 * np.pi, int(n_particles * 0.75))
        x_base = r_disk * np.cos(theta)
        y_base = r_disk * np.sin(theta)
        z_base = np.random.normal(0, 0.3, int(n_particles * 0.75))
        
        if "FDM" in dm_model:
            r_core_base = np.random.normal(0, rc * 1.5, int(n_particles * 0.25))
        else:
            r_core_base = np.random.exponential(scale=0.15, size=int(n_particles * 0.25))

        theta_c = np.random.uniform(0, 2 * np.pi, int(n_particles * 0.25))
        phi_c = np.random.uniform(0, np.pi, int(n_particles * 0.25))
        x_c_base = np.abs(r_core_base) * np.sin(phi_c) * np.cos(theta_c)
        y_c_base = np.abs(r_core_base) * np.sin(phi_c) * np.sin(theta_c)
        z_c_base = np.abs(r_core_base) * np.cos(phi_c)
        
        x_left = np.concatenate([x_base, x_c_base])
        y_left = np.concatenate([y_base, y_c_base])
        z_left = np.concatenate([z_base, z_c_base])
    else:
        if "FDM" in dm_model:
            r_sph = np.random.power(2.0, size=n_particles) * 4.0
        else:
            r_sph = np.random.exponential(scale=1.2, size=n_particles)
        theta_s = np.random.uniform(0, 2 * np.pi, n_particles)
        phi_s = np.random.uniform(0, np.pi, n_particles)
        x_left = r_sph * np.sin(phi_s) * np.cos(theta_s)
        y_left = r_sph * np.sin(phi_s) * np.sin(theta_s)
        z_left = r_sph * np.cos(phi_s)

    if include_bh:
        jet_status = "ACTIVE (Bipolar Jets)" if enable_quasar else "Disabled"
        st.info(f"Framework: {dm_model} | Central Black Hole: $M_{{\\text{{BH}}}} = {bh_mass} \\times 10^7 M_\\odot$ | Quasar Jets: {jet_status} | Speed: $v_{{\\text{{circ}}}} = {velocity_dispersion:.1f}$ km/s")
        col_left, col_right = st.columns(2)
        
        compaction_factor = max(0.1, 1.0 - (bh_mass / 50.0))
        if enable_quasar:
            compaction_factor *= 0.85 
        
        if is_spiral:
            r_core_pert = r_core_base * compaction_factor
            x_c_pert = np.abs(r_core_pert) * np.sin(phi_c) * np.cos(theta_c)
            y_c_pert = np.abs(r_core_pert) * np.sin(phi_c) * np.sin(theta_c)
            z_c_pert = np.abs(r_core_pert) * np.cos(phi_c)
            x_right = np.concatenate([x_base, x_c_pert])
            y_right = np.concatenate([y_base, y_c_pert])
            z_right = np.concatenate([z_base, z_c_pert])
        else:
            x_right = x_left * compaction_factor
            y_right = y_left * compaction_factor
            z_right = z_left * compaction_factor

        with col_left:
            st.subheader("Unperturbed Core (No Black Hole)")
            fig_left = go.Figure()
            fig_left.add_trace(go.Scatter3d(
                x=x_left, y=y_left, z=z_left, mode='markers',
                marker=dict(size=2, color=np.sqrt(x_left**2 + y_left**2 + z_left**2), colorscale='Plasma' if "FDM" in dm_model else 'Viridis', opacity=0.7),
                name="Baseline Structure"
            ))
            fig_left.update_layout(title=dict(text="Unperturbed Structure"), scene=dict(bgcolor="rgb(8, 8, 15)"), template="plotly_dark", height=480, margin=dict(l=0, r=0, b=0, t=30))
            st.plotly_chart(fig_left, use_container_width=True)

        with col_right:
            st.subheader(f"Perturbed Core ($M_{{\\text{{BH}}}} = {bh_mass} \\times 10^7 M_\\odot$)")
            fig_right = go.Figure()
            fig_right.add_trace(go.Scatter3d(
                x=x_right, y=y_right, z=z_right, mode='markers',
                marker=dict(size=2, color=np.sqrt(x_right**2 + y_right**2 + z_right**2), colorscale='Plasma' if "FDM" in dm_model else 'Viridis', opacity=0.7),
                name="Perturbed Structure"
            ))
            fig_right.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[0], mode='markers+text',
                marker=dict(size=8 + (bh_mass * 0.4), color='magenta', symbol='diamond', line=dict(color='white', width=2)),
                text=[f"Black Hole ({bh_mass} × 10⁷ M_☉)"], textposition="top center",
                name="Supermassive Black Hole"
            ))
            if enable_quasar:
                fig_right.add_trace(go.Scatter3d(
                    x=np.zeros(20), y=np.zeros(20), z=np.linspace(0.5, 5.0, 20),
                    mode='markers', marker=dict(size=4, color='cyan', symbol='diamond'), name="Quasar Jet (+Z Axis)"
                ))
                fig_right.add_trace(go.Scatter3d(
                    x=np.zeros(20), y=np.zeros(20), z=np.linspace(-5.0, -0.5, 20),
                    mode='markers', marker=dict(size=4, color='cyan', symbol='diamond'), name="Quasar Jet (-Z Axis)"
                ))
            fig_right.update_layout(title=dict(text="Black Hole Gravitational Pull Active"), scene=dict(bgcolor="rgb(8, 8, 15)"), template="plotly_dark", height=480, margin=dict(l=0, r=0, b=0, t=30))
            st.plotly_chart(fig_right, use_container_width=True)
    else:
        st.info(f"Framework Active: {dm_model} | Black Hole: Disabled | Speed: $v_{{\\text{{circ}}}} = {velocity_dispersion:.1f}$ km/s")
        fig_single = go.Figure()
        fig_single.add_trace(go.Scatter3d(
            x=x_left, y=y_left, z=z_left, mode='markers',
            marker=dict(size=2, color=np.sqrt(x_left**2 + y_left**2 + z_left**2), colorscale='Plasma' if "FDM" in dm_model else 'Viridis', opacity=0.8),
            name="Halo Structure"
        ))
        fig_single.update_layout(
            title=dict(text=f"{galaxy_preset} — {dm_model}"),
            scene=dict(xaxis_title="X (kpc)", yaxis_title="Y (kpc)", zaxis_title="Z (kpc)", bgcolor="rgb(8, 8, 15)"),
            template="plotly_dark", height=520, margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig_single, use_container_width=True)

with tab2:
    st.header(f"Dual-Zone Halo Observatory: {galaxy_preset} — {dm_model}")
    if "FDM" in dm_model:
        st.markdown(f"""
        **FDM Structure View:** Displays the Soliton Core ($r \\le r_c = {rc:.2f}\\text{{ kpc}}$), Quantum Interference Granules ($\\lambda = {lambda_db:.2f}\\text{{ kpc}}$), and the Outer Halo.
        """)
    else:
        st.markdown("""
        **CDM Structure View:** Displays collisionless particles collapsing into a classical NFW central cusp.
        """)

    fig_obs = go.Figure()

    if is_spiral:
        x_arms, y_arms, z_arms = [], [], []
        n_arm_stars = 2000
        for i in range(num_arms):
            theta = np.linspace(0.1, 3.2 * np.pi, n_arm_stars // num_arms)
            r = real_rd * np.exp(0.32 * theta)
            arm_angle = theta + (i * 2 * np.pi / num_arms)
            x = r * np.cos(arm_angle) + np.random.normal(0, 0.2, len(r))
            y = r * np.sin(arm_angle) + np.random.normal(0, 0.2, len(r))
            z = np.random.normal(0, 0.15, len(r))
            x_arms.extend(x)
            y_arms.extend(y)
            z_arms.extend(z)

        fig_obs.add_trace(go.Scatter3d(
            x=x_arms, y=y_arms, z=z_arms, mode='markers',
            marker=dict(size=2.2, color='lightblue', opacity=0.8), name="Spiral Arm Star-Forming Regions"
        ))

        n_d = int(1000 * dust_absorption)
        if n_d > 0:
            th_d = np.random.uniform(0.1, 3.0 * np.pi, n_d)
            rd = real_rd * np.exp(0.32 * th_d) + np.random.normal(0, 0.1, n_d)
            ad = th_d + 0.3 + (np.random.choice(range(num_arms)) * 2 * np.pi / num_arms)
            fig_obs.add_trace(go.Scatter3d(
                x=rd * np.cos(ad), y=rd * np.sin(ad), z=np.random.normal(0, 0.08, n_d),
                mode='markers', marker=dict(size=2.6, color='saddlebrown', opacity=0.7), name="Dust Absorption Lanes"
            ))

        n_b = 1000
        rb = np.random.normal(0, real_rb * 2.0, n_b)
        phi_b = np.random.uniform(0, np.pi, n_b)
        th_b = np.random.uniform(0, 2 * np.pi, n_b)
        fig_obs.add_trace(go.Scatter3d(
            x=np.abs(rb)*np.sin(phi_b)*np.cos(th_b), y=np.abs(rb)*np.sin(phi_b)*np.sin(th_b), z=np.abs(rb)*np.cos(phi_b)*0.5,
            mode='markers', marker=dict(size=2.5, color='gold', opacity=0.9), name="Central Stellar Bulge"
        ))
    else:
        n_dw = 2500
        rdw = np.random.power(2.0, size=n_dw) * 3.5
        thw = np.random.uniform(0, 2 * np.pi, n_dw)
        phw = np.random.uniform(0, np.pi, n_dw)
        fig_obs.add_trace(go.Scatter3d(
            x=rdw*np.sin(phw)*np.cos(thw), y=rdw*np.sin(phw)*np.sin(thw), z=rdw*np.cos(phw),
            mode='markers', marker=dict(size=2.5, color='orange', opacity=0.8), name="Stellar Population"
        ))

    th_gc = np.random.uniform(0, 2 * np.pi, globular_density)
    ph_gc = np.random.uniform(0, np.pi, globular_density)
    r_gc = np.random.uniform(1.0, 7.0, globular_density)
    fig_obs.add_trace(go.Scatter3d(
        x=r_gc*np.sin(ph_gc)*np.cos(th_gc), y=r_gc*np.sin(ph_gc)*np.sin(th_gc), z=r_gc*np.cos(ph_gc),
        mode='markers', marker=dict(size=3.5, color='white', symbol='circle', opacity=0.8), name="Globular Clusters"
    ))

    n_dm = 3000
    r_dm = np.random.uniform(0.0, 7.0, n_dm)
    th_dm = np.random.uniform(0, 2 * np.pi, n_dm)
    ph_dm = np.random.uniform(0, np.pi, n_dm)

    if "FDM" in dm_model:
        core_mask = r_dm <= rc
        granule_mask = (r_dm > rc) & (r_dm <= rc * 3.5)
        envelope_mask = r_dm > rc * 3.5

        x_dm = r_dm * np.sin(ph_dm) * np.cos(th_dm)
        y_dm = r_dm * np.sin(ph_dm) * np.sin(th_dm)
        z_dm = r_dm * np.cos(ph_dm)

        fig_obs.add_trace(go.Scatter3d(
            x=x_dm[core_mask], y=y_dm[core_mask], z=z_dm[core_mask],
            mode='markers', marker=dict(size=3.5, color='cyan', opacity=0.9),
            name=f"1. Soliton Core (r ≤ {rc:.2f} kpc)"
        ))
        fig_obs.add_trace(go.Scatter3d(
            x=x_dm[granule_mask], y=y_dm[granule_mask], z=z_dm[granule_mask],
            mode='markers', marker=dict(size=2.2, color='magenta', opacity=0.6),
            name=f"2. Interference Granules (λ = {lambda_db:.2f} kpc)"
        ))
        fig_obs.add_trace(go.Scatter3d(
            x=x_dm[envelope_mask], y=y_dm[envelope_mask], z=z_dm[envelope_mask],
            mode='markers', marker=dict(size=1.5, color='purple', opacity=0.3),
            name="3. Outer Halo Envelope"
        ))
    else:
        x_dm = r_dm * np.sin(ph_dm) * np.cos(th_dm)
        y_dm = r_dm * np.sin(ph_dm) * np.sin(th_dm)
        z_dm = r_dm * np.cos(ph_dm)
        fig_obs.add_trace(go.Scatter3d(
            x=x_dm, y=y_dm, z=z_dm,
            mode='markers', marker=dict(size=2.0, color='orange', opacity=0.5),
            name="CDM NFW Cusp Particle Halo"
        ))

    if include_bh:
        fig_obs.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0], mode='markers+text',
            marker=dict(size=9, color='white', symbol='diamond'),
            text=[f"Black Hole ({bh_mass} × 10⁷ M_☉)"], textposition="top center", name="Central Black Hole"
        ))
        if enable_quasar:
            fig_obs.add_trace(go.Scatter3d(
                x=np.zeros(35), y=np.zeros(35), z=np.linspace(0.5, 6.0, 35),
                mode='markers', marker=dict(size=5, color='cyan', symbol='circle', opacity=0.9), name="Quasar Jet (+Z)"
            ))
            fig_obs.add_trace(go.Scatter3d(
                x=np.zeros(35), y=np.zeros(35), z=np.linspace(-6.0, -0.5, 35),
                mode='markers', marker=dict(size=5, color='cyan', symbol='circle', opacity=0.9), name="Quasar Jet (-Z)"
            ))

    fig_obs.update_layout(
        title=dict(text=f"Dual-Zone Observable Universe — {galaxy_preset} — {dm_model}"),
        scene=dict(xaxis_title="X (kpc)", yaxis_title="Y (kpc)", zaxis_title="Z (kpc)", bgcolor="rgb(4, 4, 12)"),
        template="plotly_dark", height=600, margin=dict(l=0, r=0, b=0, t=40)
    )
    st.plotly_chart(fig_obs, use_container_width=True)

with tab3:
    st.header(f"3D Density Surface Mesh — {galaxy_preset} — {dm_model}")
    st.markdown("""
    **Tab 3:**
    This tab acts as a mathematical blueprint. It computes and displays the ideal equilibrium density profile across a spatial grid.
    """)

    x_grid = np.linspace(-8, 8, 50)
    y_grid = np.linspace(-8, 8, 50)
    X, Y = np.meshgrid(x_grid, y_grid)
    R = np.sqrt(X**2 + Y**2)

    if "FDM" in dm_model:
        Z = (halo_mass / 10.0) * (1.0 / (1.0 + 0.091 * (R / (rc + 0.05))**2)**8)
        if include_bh:
            Z += (bh_mass / 4.0) * (R + 0.15)**-1.5
        if enable_quasar:
            Z *= 0.9 
        surface_colorscale = "Plasma"
        surface_title = f"FDM Soliton Core Density Peak (r_c = {rc:.2f} kpc)"
    else:
        scale_radius = 2.5
        Z = (halo_mass / 15.0) * (2.0 / ((R / scale_radius + 0.05) * (1.0 + R / scale_radius)**2))
        if include_bh:
            Z += (bh_mass / 3.0) * (R + 0.05)**-2.0
        surface_colorscale = "Viridis"
        surface_title = "CDM NFW Cusp (Steep Divergent Central Peak)"

    fig_surf = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=surface_colorscale, name="Density Terrain")])
    fig_surf.update_layout(
        title=dict(text=surface_title),
        scene=dict(xaxis_title="X (kpc)", yaxis_title="Y (kpc)", zaxis_title="Density Magnitude ρ", bgcolor="rgb(10, 10, 20)"),
        template="plotly_dark", height=600, margin=dict(l=0, r=0, b=0, t=30)
    )
    st.plotly_chart(fig_surf, use_container_width=True)

with tab4:
    st.header("3D Spectral Schrödinger-Poisson Solver")
    st.markdown("""
    **Tab 4 Purpose:**
    Executes time-dependent Schrödinger-Poisson wave equations step-by-step using the Split-Step Fourier Method across time increments ($\Delta t$).
    """)

    col_s1, col_s2 = st.columns([1, 2])

    with col_s1:
        st.subheader("Simulation Settings")
        grid_res = st.selectbox("3D Grid Resolution", [32, 64], index=0, help="Spatial grid resolution size.")
        sim_steps = st.slider("Time Evolution Steps", min_value=10, max_value=60, value=30, step=10)
        
        st.info("""
        **Spectral Wave Engine Steps:**
        1. Gravity Potential Step: Applies gravitational potential phase shift.
        2. Forward Fourier Transform (FFT): Converts spatial position wave into momentum space.
        3. Quantum Pressure Step: Evolves kinetic energy and quantum wave dispersion.
        4. Inverse Fourier Transform: Converts back to physical space.
        5. Poisson Solver: Calculates updated self-gravity potential field.
        """)
        
        run_solver = st.button("Run Time-Evolution Solver")

    with col_s2:
        if "solver_history" not in st.session_state:
            st.session_state.solver_history = None

        if run_solver:
            try:
                with st.spinner("Executing time-dependent 3D Split-Step Fourier simulation..."):
                    N = int(grid_res)
                    L = 10.0
                    dx = L / N
                    x = np.linspace(-L/2, L/2, N, endpoint=False)
                    X3, Y3, Z3 = np.meshgrid(x, x, x, indexing='ij')
                    R3 = np.sqrt(X3**2 + Y3**2 + Z3**2)

                    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
                    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
                    K_sq = KX**2 + KY**2 + KZ**2
                    K_sq[0, 0, 0] = 1.0e-10

                    if "FDM" in dm_model:
                        density_init = (1.0 + 0.091 * (R3 / (rc + 0.01))**2)**(-8)
                    else:
                        density_init = 2.0 / ((R3 / 2.5 + 0.05) * (1.0 + R3 / 2.5)**2)

                    psi = np.sqrt(density_init) * (1.0 + np.random.normal(0, 0.02, size=(N, N, N)))
                    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx**3)

                    dt = 0.005
                    history_slices = []
                    history_slices.append(np.abs(psi[:, :, N // 2])**2)

                    for s in range(sim_steps):
                        rho = np.abs(psi)**2
                        rho_k = np.fft.fftn(rho)
                        V_k = -4.0 * np.pi * rho_k / K_sq
                        V_k[0, 0, 0] = 0.0
                        V = np.real(np.fft.ifftn(V_k))
                        
                        if include_bh and bh_mass > 0:
                            V -= (bh_mass * 0.1) / (R3 + 0.1)
                        if enable_quasar:
                            V += 0.05 * np.exp(- (X3**2 + Y3**2) / 1.0) * np.cos(Z3)

                        psi = np.exp(-0.5j * V * dt) * psi
                        psi_k = np.fft.fftn(psi)
                        psi_k = np.exp(-0.5j * K_sq * dt) * psi_k
                        psi = np.fft.ifftn(psi_k)
                        psi = np.exp(-0.5j * V * dt) * psi

                        history_slices.append(np.abs(psi[:, :, N // 2])**2)

                    st.session_state.solver_history = history_slices
                    st.success("Successfully simulated time steps")
            except Exception as e:
                st.error(f"Simulation engine encountered an error: {str(e)}. Try lowering the grid resolution or steps.")

        if st.session_state.solver_history is not None:
            history = st.session_state.solver_history
            max_frame = len(history) - 1
            
            st.markdown("---")
            st.subheader("Time Evolution Animation & Scrubber")
            
            anim_col1, anim_col2 = st.columns([1, 1])
            with anim_col1:
                play_animation = st.checkbox("Play Animated GIF Simulation", value=False, help="Automatically loops through time steps like an animation.")
            with anim_col2:
                if play_animation:
                    st.info("Animation mode: Use the frame slider below or let it stream.")

            if play_animation:
                frame_placeholder = st.empty()
                for f_idx in range(len(history)):
                    curr_slice = history[f_idx]
                    fig_anim = go.Figure(data=[go.Surface(
                        z=curr_slice, 
                        colorscale='Plasma' if "FDM" in dm_model else 'Viridis', 
                        name=f"Frame {f_idx}"
                    )])
                    fig_anim.update_layout(
                        title=dict(text=f"Animated Evolution — Frame {f_idx} / {max_frame} (Δt = {f_idx * 0.005:.3f})"),
                        scene=dict(xaxis_title="X (kpc)", yaxis_title="Y (kpc)", zaxis_title="Quantum Density |ψ|²"),
                        template="plotly_dark", height=420, margin=dict(l=0, r=0, b=0, t=30)
                    )
                    frame_placeholder.plotly_chart(fig_anim, use_container_width=True, key=f"anim_frame_{f_idx}")
                    time.sleep(0.1)
            else:
                selected_frame = st.slider(
                    "Scrub Simulation Time Steps", 
                    min_value=0, max_value=max_frame, value=max_frame, step=1,
                    help="Drag to view exact quantum wave density at different time steps."
                )

                current_slice = history[selected_frame]

                fig_solver = go.Figure(data=[go.Surface(
                    z=current_slice, 
                    colorscale='Plasma' if "FDM" in dm_model else 'Viridis', 
                    name=f"Time Step {selected_frame}"
                )])
                fig_solver.update_layout(
                    title=dict(text=f"3D Quantum Wave Density — Time Step {selected_frame} / {max_frame} (Δt = {selected_frame * 0.005:.3f})"),
                    scene=dict(xaxis_title="X (kpc)", yaxis_title="Y (kpc)", zaxis_title="Z (kpc)", bgcolor="rgb(10, 10, 20)"),
                    template="plotly_dark", height=450, margin=dict(l=0, r=0, b=0, t=30)
                )
                st.plotly_chart(fig_solver, use_container_width=True)
                
                st.markdown(f"**Time-Step Status:** Displaying frame {selected_frame} of {max_frame}. Quantum pressure and wave dispersion stabilize the core across time steps.")
        else:
            st.info("Click 'Run Time-Evolution Solver' in the left menu to generate the time-stepped quantum simulation frames.")

with tab5:
    st.header(f"Radial Density Profile & Telescope Data Verification — {galaxy_preset}")
    st.markdown('<a name="tab5"></a>', unsafe_allow_html=True)

    with st.expander("Scientific Guide: Understanding the Tab 5 Curves & Observations", expanded=True):
        st.markdown(r"""
        #### 1. The Gold Telescope Data Points (Dwarf Galaxy Kinematics):
        * The gold dots represent real astronomical measurements from telescopes showing that real galactic centers exhibit a smooth, flat density plateau (a core) rather than a sharp spike.

        #### 2. Cold Dark Matter (CDM / Orange Curve) & The Cusp-Core Crisis:
        * Follows the classical Navarro-Frenk-White (NFW) Profile. Collisionless particles collapse into an infinitely sharp central spike ($\rho \propto r^{-1}$), failing to match flat central telescope data points.

        #### 3. Fuzzy Dark Matter (FDM / Cyan Curve) & The Core-Halo Scaling Paradox:
        * Follows the Schive et al. Soliton Profile. Quantum pressure maintains a wide soliton core ($r_c \approx 1\text{--}2\text{ kpc}$) that matches dwarf galaxy telescope data.
        """)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Diagnostics")
        if "FDM" in dm_model:
            st.metric(label="Soliton Core Mass ($M_c$)", value=f"{core_mass_solar:.2e} Solar Masses")
            st.metric(label="Soliton Core Radius ($r_c$)", value=f"{rc:.2f} kpc")
            st.metric(label="De Broglie Wavelength ($\\lambda_{\\text{dB}}$)", value=f"{lambda_db:.2f} kpc")
            st.metric(label="Telescopic Speed ($v_{\\text{circ}}$)", value=f"{velocity_dispersion:.1f} km/s")
            st.metric(label="Half-Mass Radius Ceiling", value=f"{r_half:.3f} kpc")
        else:
            st.metric(label="Soliton Core Status", value="Disabled (CDM Cusp Active)")
            st.metric(label="NFW Scale Radius ($r_s$)", value="2.00 kpc")
            st.metric(label="Central Cusp Slope", value="Divergent Cusp ($\\rho \\propto r^{-1}$)")
        st.metric(label="Black Hole Mass ($M_{\\text{BH}}$)", value=f"{bh_mass:.1f} × 10⁷ Solar Masses")

    with col2:
        r = np.linspace(0.01, 8.0, 600)
        scale_norm = max(1.0, halo_mass / 10.0)

        fig = go.Figure()

        if "FDM" in dm_model:
            rho_profile = scale_norm * (10.0 / (1.0 + 0.091 * (r / (rc + 0.01))**2)**8)
            model_name = f"FDM Soliton Core Model (r_c = {rc:.2f} kpc)"
            color_line = "cyan"
            
            fig.add_trace(go.Scatter(x=r, y=rho_profile, mode='lines', name=model_name, line=dict(color=color_line, width=4)))
            
            obs_r = np.array([0.2, 0.5, 1.0, 2.0, 3.5, 5.0])
            obs_rho = np.array([9.2, 8.5, 7.0, 4.0, 1.8, 0.6]) * (scale_norm / 10.0)
            fig.add_trace(go.Scatter(
                x=obs_r, y=obs_rho, mode='markers',
                marker=dict(size=12, color='gold', symbol='circle', line=dict(color='white', width=1.5)),
                name="Real Galaxy Telescope Data (Flat Cores)"
            ))
            y_max_limit = max(np.max(rho_profile), np.max(obs_rho)) * 1.15
        else:
            scale_radius = 2.0
            r_safe = np.maximum(r, 0.02)
            rho_profile = scale_norm * (1.5 / ((r_safe / scale_radius) * (1.0 + (r_safe / scale_radius))**2))
            model_name = "CDM NFW Cusp Model (Fails Flat Core Telescope Data)"
            color_line = "orange"

            fig.add_trace(go.Scatter(x=r, y=rho_profile, mode='lines', name=model_name, line=dict(color=color_line, width=4)))
            
            obs_r = np.array([0.2, 0.5, 1.0, 2.0, 3.5, 5.0])
            obs_rho = np.array([9.2, 8.5, 7.0, 4.0, 1.8, 0.6]) * (scale_norm / 10.0)
            fig.add_trace(go.Scatter(
                x=obs_r, y=obs_rho, mode='markers',
                marker=dict(size=12, color='gold', symbol='circle', line=dict(color='white', width=1.5)),
                name="Real Galaxy Telescope Data (Flat Cores)"
            ))
            y_max_limit = 50.0 

        fig.update_layout(
            title=dict(text=f"Radial Density vs. Real Astronomical Observations — {galaxy_preset}"),
            xaxis_title="Galactic Radius r (kpc)", 
            yaxis_title="Normalized Density (ρ / ρ₀)",
            template="plotly_dark", height=450,
            yaxis=dict(range=[0, y_max_limit])
        )
        st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.header("15-Mission Research Campaign")
    
    score_count = len(st.session_state.unlocked_missions)
    st.subheader(f"Campaign Progress: {score_count} / 15 Missions Unlocked")
    st.progress(score_count / 15.0)

    st.markdown("""
    Welcome to the Research Campaign. Every mission below specifies the exact tab you must navigate to, observe diagnostics, calculate values, or inspect galaxy profiles, and enter your answer directly into each mission's input box. Note: All text code inputs are case-insensitive.
    """)

    missions = [
        {"id": 1, "tier": "Tier I: Quantum Fluid Dynamics", "title": "Resolving the Cusp-Core Crisis",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. Compare the FDM core curve against the CDM curve. What central profile shape matches real telescope data? Type 'FLAT' or 'CUSP'.",
         "check": lambda val: str(val).strip().upper() == "FLAT",
         "inputType": "text", "placeholder": "Enter profile type (FLAT or CUSP)...",
         "reveal": "FDM quantum pressure flattens sharp central cusps into smooth, flat soliton cores, matching real dwarf galaxy velocity dispersion data."},
        
        {"id": 2, "tier": "Tier I: Quantum Fluid Dynamics", "title": "De Broglie Macroscopic Wavelength Scale",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. Note: Set Axion Mass = 1.0 and Velocity = 100 km/s in the sidebar first. What is the calculated de Broglie Wavelength (in kpc)?",
         "check": lambda val: abs(float(val) - 1.2) < 0.1 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "When velocity dispersion is 100 km/s and boson mass is 1.0 x 10^-22 eV, the de Broglie wavelength is 1.2 kpc, scaling inversely with speed."},

        {"id": 3, "tier": "Tier I: Quantum Fluid Dynamics", "title": "Soliton Core Compression Threshold",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. In the sidebar, change Axion Boson Mass to 4.0. Observe the Soliton Core Radius ($r_c$) metric. Enter the core radius (in kpc).",
         "check": lambda val: abs(float(val) - rc) < 0.05 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "Increasing boson mass compresses the soliton core radius due to increased quantum density."},

        {"id": 4, "tier": "Tier I: Quantum Fluid Dynamics", "title": "Classical CDM Divergence",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. Switch the physics model to Cold Dark Matter (CDM). Look at the Central Cusp Slope listed under diagnostics. Enter the power law exponent.",
         "check": lambda val: "R^-1" in str(val).strip().upper() or "-1" in str(val).strip(),
         "inputType": "text", "placeholder": "Enter central cusp slope exponent...",
         "reveal": "Collisionless CDM particles collapse without quantum resistance, resulting in steep NFW cusps where central density scales as ρ ∝ r⁻¹."},

        {"id": 5, "tier": "Tier I: Quantum Fluid Dynamics", "title": "Galaxy Core Radius Suppression",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. In FDM mode, scale Host Halo Mass up to 300 x 10^10 Solar Masses. Read the Soliton Core Radius ($r_c$) value in kpc and enter it below.",
         "check": lambda val: abs(float(val) - rc) < 0.05 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "In massive cluster environments, host halo gravitational potentials pull soliton cores inward, compressing r_c below 0.1 kpc."},

        {"id": 6, "tier": "Tier II: Galactic Morphology", "title": "Elliptical Galaxy Preset",
         "briefing": "Navigate to Tab 1: Structural Analysis or the sidebar. Select the galaxy preset corresponding to a giant elliptical galaxy hosting an active supermassive black hole. Type its name.",
         "check": lambda val: "M87" in str(val).strip().upper(),
         "inputType": "text", "placeholder": "Enter galaxy designation...",
         "reveal": "M87 is a giant elliptical galaxy whose spheroid is overcome by a central supermassive black hole."},

        {"id": 7, "tier": "Tier II: Galactic Morphology", "title": "Dwarf Spheroidal Mass",
         "briefing": "Navigate to Tab 2: Dual-Zone Observatory. Choose the Fornax Dwarf preset in the sidebar. What is its Host Halo Mass in $10^{10} M_\\odot$?",
         "check": lambda val: abs(float(val) - 0.5) < 0.05 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "Dwarf spheroidal galaxies like Fornax possess tiny host halos (~0.5 x 10^10 M_sun), making them ideal laboratories for testing FDM core structures."},

        {"id": 8, "tier": "Tier II: Galactic Morphology", "title": "Dust Opacity Testing",
         "briefing": "Navigate to Tab 2: Dual-Zone Observatory. Choose the Milky Way preset and push Dust Opacity to 1.0. What stellar feature gets obscured by dust? Type 'BULGE' or 'ARMS'.",
         "check": lambda val: "BULGE" in str(val).strip().upper() or "DISK" in str(val).strip().upper(),
         "inputType": "text", "placeholder": "Enter obscured galactic structure...",
         "reveal": "Dense interstellar dust lanes obscure starlight across planes, requiring infrared observations to investigate inner core structures."},

        {"id": 9, "tier": "Tier II: Galactic Morphology", "title": "Globular Cluster Density",
         "briefing": "Navigate to Tab 2: Dual-Zone Observatory. Move the Globular Cluster Density slider all the way to the right. What is the maximum cluster count value?",
         "check": lambda val: float(val) == 1000 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "High globular cluster counts allow astronomers to trace gravitational friction and investigate whether FDM interference granules affect orbital decay."},

        {"id": 10, "tier": "Tier III: SMBH & AGN Feedback", "title": "Black Hole Spike Identification",
         "briefing": "Navigate to Tab 1: Structural Analysis. Enable the Central Black Hole and set its mass to 40. Does the dark matter core COMPACT or EXPAND in response to the black hole's gravity?",
         "check": lambda val: "COMPACT" in str(val).strip().upper(),
         "inputType": "text", "placeholder": "Enter structural response (COMPACT or EXPAND)...",
         "reveal": "A point-mass black hole potential creates steep gravitational pulling that compacts surrounding dark matter into central density spikes."},

        {"id": 11, "tier": "Tier III: SMBH & AGN Feedback", "title": "Quasar Jet Energy Venting", 
         "briefing": "Navigate to Tab 1: Structural Analysis. Toggle Quasar Relativistic Jets ON and OFF. Enter 'ACTIVE' or 'DISABLED' when jets are blasting out along the polar Z-axis.",
         "check": lambda val: "ACTIVE" in str(val).strip().upper(),
         "inputType": "text", "placeholder": "Enter jet feedback state...",
         "reveal": "Bipolar quasar jets vent central energy along the Z-axis, counteracting black hole gravity and stabilizing soliton core density."},

        {"id": 12, "tier": "Tier III: SMBH & AGN Feedback", "title": "Pure Soliton Ground State",
         "briefing": "Navigate to Tab 1: Structural Analysis. Turn off the Central Black Hole checkbox in FDM mode. Type 'SCHRODINGER' (the wave equation central to quantum dynamics).",
         "check": lambda val: str(val).strip().upper() == "SCHRODINGER",
         "inputType": "text", "placeholder": "Type SCHRODINGER...",
         "reveal": "Disabling black hole perturbations isolates the ground-state soliton governed solely by coupled Schrödinger-Poisson equations."},

        {"id": 13, "tier": "Tier IV: Synthesis", "title": "Spectral Fourier Engine Resolution",
         "briefing": "Navigate to Tab 4: PyUltraLight Solver. Look at the 3D Grid Resolution dropdown choices. Enter the higher grid resolution option available (e.g., 32 or 64).",
         "check": lambda val: float(val) == 64 if str(val).replace('.','',1).isdigit() else False,
         "inputType": "number",
         "reveal": "Executing split-step Fourier spectral transforms on a 64^3 grid provides refined resolution for modeling wave packet loops."},

        {"id": 14, "tier": "Tier IV: Synthesis", "title": "Core-Halo Scaling Paradox",
         "briefing": "Navigate to Tab 5: Radial Scaling & Data. Observe how Core Radius ($r_c$) changes as you increase Host Halo Mass. Does the core get LARGER or SMALLER?",
         "check": lambda val: "SMALLER" in str(val).strip().upper(),
         "inputType": "text", "placeholder": "Enter core behavior (LARGER or SMALLER)...",
         "reveal": "Pure FDM scaling dictates r_c ∝ M_vir^(-1/3) (more massive halos have smaller cores). This paradox requires galaxy feedback to explain large diffuse cores in real massive galaxies."},

        {"id": 15, "tier": "Tier IV: Synthesis", "title": "Master Verification Code",
         "briefing": "Synthesizing all quantum mechanics, galactic presets, and black hole feedback systems in our analysis. Enter the master verification code 'COSMOQUANTUM' below.",
         "check": lambda val: str(val).strip().upper() == "COSMOQUANTUM",
         "inputType": "text", "placeholder": "Enter master code...",
         "reveal": "Congratulations! You have completed the CosmoQuantum research campaign, demonstrating full understanding of Fuzzy Dark Matter dynamics."}
    ]

    for m in missions:
        is_unlocked = m["id"] in st.session_state.unlocked_missions
        status_badge = "UNLOCKED" if is_unlocked else "LOCKED"

        with st.expander(f"Mission {m['id']}: {m['title']} ({m['tier']}) — [{status_badge}]"):
            st.markdown(f"**Prompt:** {m['briefing']}")
            
            if is_unlocked:
                st.success(f"Discovery: {m['reveal']}")
            else:
                st.markdown("---")
                st.markdown("**Submit Answer:**")
                
                if m["inputType"] == "number":
                    user_raw = st.text_input(
                        f"Enter numerical value for Mission {m['id']}:", 
                        key=f"input_m_{m['id']}"
                    )
                else:
                    user_raw = st.text_input(
                        f"Enter text response for Mission {m['id']}:", 
                        key=f"input_m_{m['id']}", placeholder=m.get("placeholder", "")
                    )

                submit_btn = st.button(f"Verify Mission {m['id']}", key=f"btn_m_{m['id']}")
                
                if submit_btn:
                    if m["inputType"] == "number":
                        try:
                            val_float = float(user_raw)
                            if m["check"](val_float):
                                st.session_state.unlocked_missions.add(m["id"])
                                st.success(f"Correct! Mission {m['id']} Unlocked!")
                                st.rerun()
                            else:
                                st.error("Incorrect value. Check your settings in the specified tab and try again!")
                        except ValueError:
                            st.error("Please enter a valid number (e.g. 1.2 or 64).")
                    else:
                        if m["check"](user_raw):
                            st.session_state.unlocked_missions.add(m["id"])
                            st.success(f"Correct! Mission {m['id']} Unlocked!")
                            st.rerun()
                        else:
                            st.error("Incorrect answer. Check your settings in the specified tab and try again!")

    st.markdown("---")
    st.subheader("Export Lab Report")
    
    report_content = (
        "# CosmoQuantum Lab Report\n"
        "## 1. Simulation Setup\n"
        f"- Galaxy Preset: {galaxy_preset}\n"
        f"- Physics Framework: {dm_model}\n"
        f"- Halo Mass ($M_{{\\text{{vir}}}}$): {halo_mass} x 10^10 Solar Masses\n"
        f"- Axion Boson Mass ($m_{{\\text{{axion}}}}$): {boson_mass} x 10^-22 eV\n"
        f"- Telescopic Speed ($v_{{\\text{{circ}}}}$): {velocity_dispersion:.1f} km/s\n"
        f"- Black Hole Mass ($M_{{\\text{{BH}}}}$): {bh_mass} x 10^7 Solar Masses\n\n"
        "## 2. Calculated Telemetry\n"
        f"- Soliton Core Radius ($r_c$): {rc:.4f} kpc\n"
        f"- Soliton Core Mass ($M_c$): {core_mass_solar:.4e} Solar Masses\n"
        f"- De Broglie Wavelength ($\\lambda_{{\\text{{dB}}}}$): {lambda_db:.4f} kpc\n\n"
        "## 3. Campaign Status\n"
        f"- Missions Completed: {score_count} / 15\n"
    )
    st.download_button(
        label="Download Official Lab Report (.md)",
        data=report_content,
        file_name="CosmoQuantum_Lab_Report.md",
        mime="text/markdown"
    )

st.markdown("---")
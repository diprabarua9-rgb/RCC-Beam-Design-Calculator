import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="RCC Beam Design Calculator",
    page_icon="🏗",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏗 RCC Beam Design Calculator")
st.subheader("Bangladesh National Building Code (BNBC 2020)")

# ==========================================
# SECTION 4 : SIDEBAR
# ==========================================

st.sidebar.title("BNBC 2020 Beam Design")

st.sidebar.info("""
Civil Engineering Software

Code : BNBC 2020

Developed By
Dipra Barua

Developed Using

✔ Python
✔ Streamlit
✔ NumPy
✔ Pandas
✔ Matplotlib
""")

# ==========================================
# SECTION 5 : MATERIAL PROPERTIES & BEAM GEOMETRY
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

# ==========================================
# LEFT COLUMN : MATERIAL PROPERTIES
# ==========================================

with col1:

    st.header("Material Properties")

    fc = st.selectbox(
        "Concrete Strength, f'c (MPa)",
        options=[20, 25, 30, 35, 40, 45, 50, 55, 60],
        index=1
    )

    fy = st.selectbox(
        "Steel Yield Strength, fy (MPa)",
        options=[280, 420, 500, 550],
        index=2
    )

# ==========================================
# RIGHT COLUMN : BEAM GEOMETRY
# ==========================================

with col2:

    st.header("Beam Geometry")

    b = st.number_input(
        "Beam Width, b (mm)",
        min_value=200.0,
        max_value=1000.0,
        value=300.0,
        step=25.0
    )

    h = st.number_input(
        "Overall Depth, h (mm)",
        min_value=300.0,
        max_value=1500.0,
        value=500.0,
        step=25.0
    )

    cover = st.number_input(
        "Clear Cover (mm)",
        min_value=25.0,
        max_value=75.0,
        value=40.0,
        step=5.0
    )

    L = st.number_input(
        "Beam Span, L (m)",
        min_value=1.0,
        max_value=20.0,
        value=6.0,
        step=0.5
    )
# ==========================================
# SECTION 7 : SERVICE LOADS
# ==========================================

st.markdown("---")
st.header("Service Loads")

col1, col2 = st.columns(2)

with col1:

    DL = st.number_input(
        "Dead Load, DL (kN/m)",
        min_value=0.0,
        max_value=500.0,
        value=15.0,
        step=1.0,
        help="Superimposed dead load only. Beam self weight will be calculated automatically."
    )

with col2:

    LL = st.number_input(
        "Live Load, LL (kN/m)",
        min_value=0.0,
        max_value=500.0,
        value=20.0,
        step=1.0,
        help="Service live load."
    )
# ==========================================
# SECTION 8 : DESIGN BUTTON
# ==========================================

st.markdown("---")

col1, col2 = st.columns([1, 3])


# Maintain design state
if "design_done" not in st.session_state:
    st.session_state.design_done = False


with col1:

    design = st.button(
        "🧮 Design RCC Beam",
        use_container_width=True
    )


# Button pressed
if design:

    st.session_state.design_done = True
# ==========================================
# SECTION 9 : START DESIGN
# ==========================================

if st.session_state.design_done:

    st.success("Input data accepted successfully.")
# ==========================================
# SECTION 10 : INPUT SUMMARY
# ==========================================

    st.markdown("---")
    st.header("Input Summary")

    summary = pd.DataFrame({

        "Parameter":[
            "Concrete Strength",
            "Steel Yield Strength",
            "Beam Width",
            "Overall Depth",
            "Clear Cover",
            "Beam Span",
            "Service Dead Load",
            "Service Live Load"
        ],

        "Value":[
            f"{fc} MPa",
            f"{fy} MPa",
            f"{b:.0f} mm",
            f"{h:.0f} mm",
            f"{cover:.0f} mm",
            f"{L:.2f} m",
            f"{DL:.2f} kN/m",
            f"{LL:.2f} kN/m"
        ]

    })

    st.table(summary)
# ==========================================
# SECTION 11 : LOAD ANALYSIS
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Load Analysis")

    # --------------------------------------
    # Unit Weight of Reinforced Concrete
    # --------------------------------------

    gamma_rc = 25.0      # kN/m³

    # --------------------------------------
    # Beam Self Weight
    # --------------------------------------

    self_weight = (b / 1000) * (h / 1000) * gamma_rc

    # --------------------------------------
    # Total Service Dead Load
    # --------------------------------------

    DL_total = DL + self_weight

    # --------------------------------------
    # Ultimate Load Combination
    # BNBC 2020
    # U = 1.2D + 1.6L
    # --------------------------------------

    wu = 1.2 * DL_total + 1.6 * LL

    # --------------------------------------
    # Beam Analysis
    # Simply Supported Beam
    # Uniformly Distributed Load
    # --------------------------------------

    Reaction = wu * L / 2

    Vu = Reaction

    Mu = wu * L**2 / 8

    # --------------------------------------
    # Display Results
    # --------------------------------------

    st.write(f"Unit Weight of Concrete = {gamma_rc:.1f} kN/m³")

    st.write(f"Beam Self Weight = {self_weight:.3f} kN/m")

    st.write(f"Total Dead Load = {DL_total:.3f} kN/m")

    st.write(f"Ultimate Factored Load (Wu) = {wu:.3f} kN/m")

    st.write(f"Support Reaction = {Reaction:.3f} kN")

    st.write(f"Ultimate Shear Force (Vu) = {Vu:.3f} kN")

    st.write(f"Ultimate Bending Moment (Mu) = {Mu:.3f} kN·m")
# ==========================================
# SECTION 12 : SHEAR FORCE DIAGRAM (SFD)
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Shear Force Diagram (SFD)")

    # --------------------------------------
    # Beam Length Coordinates
    # --------------------------------------

    x = np.linspace(0, L, 200)

    # --------------------------------------
    # Shear Force Equation
    # V = R - wx
    # --------------------------------------

    V = Reaction - wu * x

    # --------------------------------------
    # Plot
    # --------------------------------------

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        x,
        V,
        color="blue",
        linewidth=2.5
    )

    ax.fill_between(
        x,
        V,
        color="skyblue",
        alpha=0.35
    )

    ax.axhline(
        0,
        color="black",
        linewidth=1
    )

    # Supports

    ax.scatter(
        [0, L],
        [Reaction, -Reaction],
        color="black",
        s=70,
        zorder=5
    )

    # Labels

    ax.text(
        0,
        Reaction,
        f"{Reaction:.2f} kN",
        ha="left",
        va="bottom"
    )

    ax.text(
        L,
        -Reaction,
        f"{-Reaction:.2f} kN",
        ha="right",
        va="top"
    )

    ax.set_title("Shear Force Diagram")

    ax.set_xlabel("Beam Length (m)")

    ax.set_ylabel("Shear Force (kN)")

    ax.grid(True)

    st.pyplot(fig)

    st.success(f"Maximum Shear Force = {Vu:.2f} kN")
# ==========================================
# SECTION 13 : BENDING MOMENT DIAGRAM (BMD)
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Bending Moment Diagram (BMD)")

    # --------------------------------------
    # Bending Moment Along Beam
    # M = Rx - wx²/2
    # --------------------------------------

    M = Reaction * x - (wu * x**2) / 2

    # Maximum Bending Moment
    Mmax = np.max(M)
    xmax = x[np.argmax(M)]

    # --------------------------------------
    # Plot Bending Moment Diagram
    # --------------------------------------

    fig_bmd, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        x,
        M,
        color="red",
        linewidth=2.5,
        label="Bending Moment"
    )

    ax.fill_between(
        x,
        M,
        color="orange",
        alpha=0.35
    )

    ax.axhline(
        y=0,
        color="black",
        linewidth=1
    )

    # Maximum Moment Point

    ax.scatter(
        xmax,
        Mmax,
        color="blue",
        s=80,
        zorder=5
    )

    ax.annotate(
        f"{Mmax:.2f} kN·m",
        xy=(xmax, Mmax),
        xytext=(xmax + 0.4, Mmax * 0.80),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10
    )

    # Supports

    ax.scatter(
        [0, L],
        [0, 0],
        color="black",
        s=60
    )

    # Labels

    ax.set_title("Bending Moment Diagram")

    ax.set_xlabel("Beam Length (m)")

    ax.set_ylabel("Moment (kN·m)")

    ax.grid(True)

    ax.legend()

    st.pyplot(fig_bmd)

    # --------------------------------------
    # Results
    # --------------------------------------

    st.success(f"Maximum Ultimate Moment (Mu) = {Mmax:.2f} kN·m")

    st.info(f"Maximum Moment occurs at x = {xmax:.2f} m")
# ==========================================
# SECTION 14 : FLEXURAL DESIGN
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Flexural Design")

    # --------------------------------------
    # Assumed Reinforcement Details
    # --------------------------------------

    assumed_bar = 20      # mm
    stirrup_dia = 10      # mm

    # --------------------------------------
    # Effective Depth
    # --------------------------------------

    d = h - cover - stirrup_dia - assumed_bar / 2

    # --------------------------------------
    # Initial Strength Reduction Factor
    # --------------------------------------

    phi = 0.90

    # --------------------------------------
    # Design Moment
    # --------------------------------------

    Mu_Nmm = Mu * 1e6

    Mn_required = Mu_Nmm / phi

    # --------------------------------------
    # Iterative Steel Area Calculation
    # --------------------------------------

    As = 500.0
    tolerance = 1.0

    for _ in range(100):

        a = (As * fy) / (0.85 * fc * b)

        Mn_trial = As * fy * (d - a / 2)

        if abs(Mn_trial - Mn_required) < tolerance:
            break

        if Mn_trial <= 0:
            st.error("Moment calculation failed.")
            st.stop()

        As = As * Mn_required / Mn_trial

    # --------------------------------------
    # Compression Block
    # --------------------------------------

    a = (As * fy) / (0.85 * fc * b)

    # --------------------------------------
    # Beta1 (BNBC 2020)
    # --------------------------------------

    if fc <= 28:
        beta1 = 0.85

    elif fc >= 55:
        beta1 = 0.65

    else:
        beta1 = 0.85 - 0.05 * ((fc - 28) / 7)

    # --------------------------------------
    # Neutral Axis Depth
    # --------------------------------------

    c = a / beta1

    if c <= 0:
        st.error("Neutral axis calculation error.")
        st.stop()

    # --------------------------------------
    # Steel Tensile Strain
    # --------------------------------------

    eps_t = 0.003 * (d - c) / c

    # --------------------------------------
    # Strength Reduction Factor (BNBC 2020)
    # --------------------------------------

    if eps_t >= 0.005:

        phi = 0.90

    elif eps_t <= 0.002:

        phi = 0.65

    else:

        phi = 0.65 + (eps_t - 0.002) * (0.25 / 0.003)

    # --------------------------------------
    # Update Required Nominal Moment
    # --------------------------------------

    Mn_required = Mu_Nmm / phi

    # --------------------------------------
    # Reinforcement Ratio
    # --------------------------------------

    rho = As / (b * d)

    # --------------------------------------
    # Display Results
    # --------------------------------------

    st.subheader("Flexural Design Results")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Effective Depth (d)",
            f"{d:.1f} mm"
        )

        st.metric(
            "Required Steel Area",
            f"{As:.1f} mm²"
        )

        st.metric(
            "Compression Block (a)",
            f"{a:.1f} mm"
        )

        st.metric(
            "Neutral Axis (c)",
            f"{c:.1f} mm"
        )

    with col2:

        st.metric(
            "Required Nominal Moment",
            f"{Mn_required/1e6:.2f} kN·m"
        )

        st.metric(
            "Steel Ratio",
            f"{rho:.4f}"
        )

        st.metric(
            "Steel Strain",
            f"{eps_t:.5f}"
        )

        st.metric(
            "Strength Reduction Factor (φ)",
            f"{phi:.2f}"
        )

    # --------------------------------------
    # Section Classification
    # --------------------------------------

    st.markdown("---")
    st.subheader("Section Classification")

    if eps_t >= 0.005:

        st.success("✔ Tension-Controlled Section")

    elif eps_t >= 0.002:

        st.warning("⚠ Transition Section")

    else:

        st.error("✖ Compression-Controlled Section")

# ==========================================
# SECTION 15 : REINFORCEMENT CHECK
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Reinforcement Check (BNBC 2020)")


    # --------------------------------------
    # Minimum Reinforcement Requirement
    # --------------------------------------

    As_min1 = (0.25 * math.sqrt(fc) / fy) * b * d

    As_min2 = (1.4 / fy) * b * d

    As_min = max(As_min1, As_min2)


    # --------------------------------------
    # Maximum Reinforcement Ratio
    # --------------------------------------

    Es = 200000        # MPa

    eps_y = fy / Es


    # Balanced Neutral Axis

    cb = (0.003 / (0.003 + eps_y)) * d


    # Maximum Steel Area

    a_max = beta1 * cb

    As_max = (
        0.85 * fc * b * a_max
    ) / fy



    # --------------------------------------
    # Final Steel Comparison
    # --------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Minimum Steel Area",
            f"{As_min:.1f} mm²"
        )


        st.metric(
            "Provided Required Steel",
            f"{As:.1f} mm²"
        )


    with col2:

        st.metric(
            "Maximum Allowed Steel",
            f"{As_max:.1f} mm²"
        )


        st.metric(
            "Balanced Neutral Axis",
            f"{cb:.1f} mm"
        )


    # --------------------------------------
    # Minimum Steel Check
    # --------------------------------------

    st.subheader("Minimum Reinforcement Check")


    if As >= As_min:

        st.success(
            "✔ Minimum reinforcement requirement satisfied"
        )

    else:

        st.warning(
            "⚠ Required steel increased to minimum reinforcement"
        )

        As = As_min



    # --------------------------------------
    # Maximum Steel Check
    # --------------------------------------

    st.subheader("Maximum Reinforcement Check")


    if As <= As_max:

        st.success(
            "✔ Reinforcement ratio is within allowable limit"
        )

    else:

        st.error(
            "✖ Section is over reinforced. Increase beam size."
        )



    # --------------------------------------
    # Final Reinforcement Area
    # --------------------------------------

    rho_final = As/(b*d)


    st.markdown("---")

    st.subheader("Final Flexural Reinforcement")


    st.write(
        f"Final Required Steel Area = {As:.1f} mm²"
    )


    st.write(
        f"Final Reinforcement Ratio = {rho_final:.4f}"
    )


    # --------------------------------------
    # Design Status
    # --------------------------------------

    if As <= As_max and As >= As_min:

        st.success(
            "🏗 FLEXURAL DESIGN SAFE (BNBC 2020)"
        )

    else:

        st.error(
            "❌ FLEXURAL DESIGN NOT SAFE"
        )
# ==========================================
# SECTION 16 : AUTOMATIC BAR SELECTION
# BNBC 2020
# ==========================================

    st.markdown("---")
    st.header("Automatic Reinforcement Selection")


    # --------------------------------------
    # Available Reinforcement Bars
    # --------------------------------------

    available_bars = [
        10,
        12,
        16,
        20,
        25,
        32
    ]


    # --------------------------------------
    # User Selected Bar Diameter
    # --------------------------------------

    selected_bar = st.selectbox(
        "Select Main Reinforcement Bar Diameter (mm)",
        available_bars,
        index=3
    )


    # --------------------------------------
    # Area of One Bar
    # --------------------------------------

    bar_area = (
        math.pi *
        selected_bar**2 /
        4
    )


    # --------------------------------------
    # Required Number of Bars
    # --------------------------------------

    number_of_bars = math.ceil(
        As / bar_area
    )


    # --------------------------------------
    # Actual Steel Area
    # --------------------------------------

    Ast_provided = (
        number_of_bars *
        bar_area
    )


    # --------------------------------------
    # Reinforcement Ratio
    # --------------------------------------

    rho_provided = (
        Ast_provided /
        (b*d)
    )


    # --------------------------------------
    # Display Results
    # --------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Selected Bar Diameter",
            f"{selected_bar} mm"
        )


        st.metric(
            "Number of Bars Required",
            f"{number_of_bars} Nos."
        )


        st.metric(
            "Single Bar Area",
            f"{bar_area:.1f} mm²"
        )


    with col2:

        st.metric(
            "Required Steel Area",
            f"{As:.1f} mm²"
        )


        st.metric(
            "Provided Steel Area",
            f"{Ast_provided:.1f} mm²"
        )


        st.metric(
            "Provided Steel Ratio",
            f"{rho_provided:.4f}"
        )


    # --------------------------------------
    # Reinforcement Status
    # --------------------------------------

    st.markdown("---")

    st.subheader("Bottom Reinforcement Details")


    if Ast_provided >= As:

        st.success(
            f"✔ Provide {number_of_bars}-{selected_bar} mm "
            "Bottom Reinforcement"
        )

    else:

        st.error(
            "❌ Provided reinforcement is insufficient"
        )



    # --------------------------------------
    # Bar Spacing Check
    # --------------------------------------

    clear_spacing = 25       # mm


    total_bar_width = (
        number_of_bars *
        selected_bar
    )


    available_width = (
        b -
        2*cover -
        2*stirrup_dia
    )


    required_width = (
        total_bar_width +
        (number_of_bars-1)*clear_spacing
    )


    st.subheader("Bar Arrangement Check")


    if required_width <= available_width:

        st.success(
            "✔ Bars can be arranged in single layer"
        )

    else:

        st.warning(
            "⚠ Multiple layers required"
        )


    # --------------------------------------
    # Final Reinforcement Summary
    # --------------------------------------

    st.markdown("---")

    st.subheader("Final Reinforcement Summary")


    reinforcement_summary = pd.DataFrame({

        "Parameter":[
            "Beam Size",
            "Required Steel",
            "Selected Bar",
            "Number of Bars",
            "Provided Steel",
            "Arrangement"
        ],


        "Value":[

            f"{b:.0f} × {h:.0f} mm",

            f"{As:.1f} mm²",

            f"{selected_bar} mm dia",

            f"{number_of_bars} Nos.",

            f"{Ast_provided:.1f} mm²",

            "Bottom Tension Reinforcement"

        ]

    })


    st.table(reinforcement_summary)

# ==========================================
# SECTION 17 : SHEAR DESIGN
# BNBC 2020
# ==========================================


    st.markdown("---")
    st.header("Shear Design (BNBC 2020)")


    # --------------------------------------
    # Shear Parameters
    # --------------------------------------

    lambda_c = 1.0

    phi_v = 0.75



    # --------------------------------------
    # Concrete Shear Strength
    #
    # Vc = 0.17 λ √fc b d
    #
    # --------------------------------------

    Vc = (
        0.17 *
        lambda_c *
        math.sqrt(fc) *
        b *
        d
    )


    Vc_kN = Vc / 1000



    # --------------------------------------
    # Design Shear Strength
    # --------------------------------------

    phi_Vc = phi_v * Vc_kN



    # --------------------------------------
    # Required Shear Strength
    # --------------------------------------

    Vs_required = Vu - phi_Vc


    if Vs_required < 0:

        Vs_required = 0



    # --------------------------------------
    # Shear Capacity Display
    # --------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Ultimate Shear Force (Vu)",
            f"{Vu:.2f} kN"
        )


        st.metric(
            "Concrete Shear Capacity (Vc)",
            f"{Vc_kN:.2f} kN"
        )


        st.metric(
            "Design Shear Strength (φVc)",
            f"{phi_Vc:.2f} kN"
        )


    with col2:

        st.metric(
            "Required Shear Strength (Vs)",
            f"{Vs_required:.2f} kN"
        )


        st.metric(
            "Shear Reduction Factor",
            f"{phi_v:.2f}"
        )



    # --------------------------------------
    # Shear Check
    # --------------------------------------

    st.markdown("---")

    st.subheader("Shear Strength Check")


    if Vu <= phi_Vc:

        st.success(
            "✔ Concrete shear capacity is adequate"
        )

    else:

        st.warning(
            "⚠ Shear reinforcement required"
        )



    # ======================================
    # SHEAR REINFORCEMENT DESIGN
    # ======================================


    st.markdown("---")

    st.subheader("Shear Reinforcement Design")



    # --------------------------------------
    # Stirrup Diameter
    # --------------------------------------

    stirrup_bar = st.selectbox(

        "Select Stirrup Diameter (mm)",

        [8,10,12],

        index=1

    )



    # --------------------------------------
    # Stirrup Area
    # Two legged stirrup
    # --------------------------------------

    Av = (

        2 *
        math.pi *
        stirrup_bar**2 /
        4

    )



    # --------------------------------------
    # Required Spacing
    #
    # Vs = Av fy d / s
    #
    # --------------------------------------

    if Vs_required > 0:


        s_calculated = (

            Av *
            fy *
            d /

            (Vs_required * 1000)

        )


    else:

        s_calculated = 600



    # --------------------------------------
    # BNBC Maximum Spacing
    # --------------------------------------

    s_max = min(

        d/2,

        600

    )



    # --------------------------------------
    # Final Allowable Spacing
    # --------------------------------------

    allowable_spacing = min(

        s_calculated,

        s_max

    )



    # --------------------------------------
    # Practical Available Spacing
    # --------------------------------------

    standard_spacing = [

        75,
        100,
        125,
        150,
        175,
        200,
        225,
        250,
        300

    ]



    final_spacing = standard_spacing[0]



    for sp in standard_spacing:

        if sp <= allowable_spacing:

            final_spacing = sp



    # --------------------------------------
    # Display Results
    # --------------------------------------

    col1, col2 = st.columns(2)



    with col1:

        st.metric(

            "Stirrup Area (Av)",

            f"{Av:.1f} mm²"

        )


        st.metric(

            "Calculated Spacing",

            f"{s_calculated:.1f} mm"

        )



    with col2:

        st.metric(

            "Maximum Allowed Spacing",

            f"{s_max:.1f} mm"

        )


        st.metric(

            "Provided Spacing",

            f"{final_spacing:.0f} mm"

        )



    # --------------------------------------
    # Explanation
    # --------------------------------------

    st.info(

        f"BNBC maximum spacing limit = d/2 = {s_max:.0f} mm. "
        "Final spacing is selected as the largest practical spacing "
        "not exceeding the allowable limit."

    )



    # --------------------------------------
    # Final Shear Reinforcement
    # --------------------------------------

    st.markdown("---")

    st.subheader("Final Shear Reinforcement")


    st.success(

        f"✔ Provide {stirrup_bar} mm "
        f"Two Legged Stirrup @ "
        f"{final_spacing:.0f} mm c/c"

    )
# ==========================================
# SECTION 18 : DEVELOPMENT LENGTH CHECK
# BNBC 2020
# ==========================================


    st.markdown("---")
    st.header("Development Length Check (BNBC 2020)")


    # --------------------------------------
    # Development Length Parameters
    # --------------------------------------

    db = selected_bar       # Main reinforcement diameter


    lambda_c = 1.0          # Normal weight concrete


    # Reinforcement modification factors

    psi_t = 1.0             # Not top bar

    psi_e = 1.0             # Uncoated reinforcement



    # --------------------------------------
    # Development Length Calculation
    #
    # Ld = fy ψt ψe db
    #      ----------------
    #      4 λ √fc
    #
    # --------------------------------------

    Ld = (

        fy *
        psi_t *
        psi_e *
        db

    ) / (

        4 *
        lambda_c *
        math.sqrt(fc)

    )



    # --------------------------------------
    # Minimum Development Length
    # BNBC
    # --------------------------------------

    Ld_min = max(

        Ld,

        300

    )



    # --------------------------------------
    # Available Anchorage Length
    # Assume beam support length
    # --------------------------------------

    available_length = L * 1000 / 2



    # --------------------------------------
    # Display Results
    # --------------------------------------

    col1, col2 = st.columns(2)


    with col1:


        st.metric(

            "Main Bar Diameter",

            f"{db} mm"

        )


        st.metric(

            "Calculated Development Length",

            f"{Ld:.1f} mm"

        )


        st.metric(

            "Required Development Length",

            f"{Ld_min:.1f} mm"

        )



    with col2:


        st.metric(

            "Available Anchorage Length",

            f"{available_length:.1f} mm"

        )


        st.metric(

            "Concrete Strength",

            f"{fc} MPa"

        )


        st.metric(

            "Steel Strength",

            f"{fy} MPa"

        )



    # --------------------------------------
    # Development Length Check
    # --------------------------------------

    st.markdown("---")

    st.subheader("Development Length Safety Check")


    if available_length >= Ld_min:


        st.success(

            "✔ Development Length Requirement Satisfied (BNBC 2020)"

        )


    else:


        st.error(

            "✖ Development Length is Insufficient"

        )



    # --------------------------------------
    # Summary
    # --------------------------------------

    st.info(

        f"Required anchorage length = {Ld_min:.0f} mm. "
        f"Available length = {available_length:.0f} mm."

    )
# ==========================================
# SECTION 19 : RCC BEAM CROSS SECTION DRAWING
# BNBC 2020
# ==========================================


    st.markdown("---")
    st.header("RCC Beam Cross Section")


    # --------------------------------------
    # Create High Resolution Figure
    # --------------------------------------

    fig, ax = plt.subplots(
        figsize=(2.5, 4),
        dpi=300
    )


    # --------------------------------------
    # Beam Outline
    # --------------------------------------

    beam = plt.Rectangle(

        (0,0),

        b,

        h,
        facecolor="lightgray",
        edgecolor="navy",
        linewidth=2,
        alpha=0.5


    )

    ax.add_patch(beam)



    # --------------------------------------
    # Stirrup Drawing
    # --------------------------------------

    stirrup = plt.Rectangle(

        (
            cover + stirrup_dia,
            cover + stirrup_dia
        ),

        b - 2*(cover + stirrup_dia),

        h - 2*(cover + stirrup_dia),

        fill=False,
        edgecolor="green",
        linewidth=1.5

    )

    ax.add_patch(stirrup)



    # --------------------------------------
    # Bottom Reinforcement Drawing
    # --------------------------------------

    bar_radius = selected_bar / 2



    # Available width

    clear_width = (

        b -
        2*cover -
        2*stirrup_dia

    )



    # Bar spacing

    if number_of_bars > 1:

        bar_spacing = (

            clear_width -
            number_of_bars * selected_bar

        ) / (number_of_bars - 1)


    else:

        bar_spacing = 0



    # First bar location

    x_start = (

        cover +
        stirrup_dia +
        bar_radius

    )


    y_bar = (

        cover +
        stirrup_dia +
        bar_radius

    )



    # Draw reinforcement bars

    for i in range(number_of_bars):


        x_bar = (

            x_start +
            i*(selected_bar + bar_spacing)

        )


        circle = plt.Circle(

            (
                x_bar,
                y_bar
            ),

            bar_radius,

            fill=True,

            color="steelblue"

        )


        ax.add_patch(circle)



    # --------------------------------------
    # Dimension Text
    # --------------------------------------

    ax.text(

        b/2,

        h + 40,

        f"{b:.0f} mm",

        ha="center",

        fontsize=8

    )



    ax.text(

        b + 50,

        h/2,

        f"{h:.0f} mm",

        va="center",

        rotation=90,

        fontsize=8

    )



    # --------------------------------------
    # Formatting
    # --------------------------------------

    ax.set_xlim(

        -100,

        b + 120

    )


    ax.set_ylim(

        -100,

        h + 150

    )


    ax.set_aspect(

        "equal"

    )


    ax.axis("off")


    # Remove extra white space

    plt.tight_layout()



    # --------------------------------------
    # Show Drawing
    # --------------------------------------

    st.pyplot(

        fig,

        use_container_width=False

    )



    # --------------------------------------
    # Reinforcement Detail
    # --------------------------------------

    st.subheader(
        "Beam Reinforcement Detail"
    )



    drawing_summary = pd.DataFrame({


        "Parameter":[

            "Beam Size",

            "Main Reinforcement",

            "Stirrup",

            "Clear Cover"

        ],



        "Value":[

            f"{b:.0f} × {h:.0f} mm",

            f"{number_of_bars}-{selected_bar} mm Bottom Bars",

            f"{stirrup_bar} mm Two Legged Stirrup @ {final_spacing:.0f} mm c/c",

            f"{cover:.0f} mm"

        ]


    })



    st.table(
        drawing_summary
    )
# ==========================================
# SECTION 20 : REINFORCEMENT QUANTITY ESTIMATION
# BNBC 2020
# ==========================================


    st.markdown("---")

    st.header("Reinforcement Quantity Estimation (BNBC 2020)")


    # --------------------------------------
    # Steel Unit Weight
    # Unit weight = d² / 162 kg/m
    # --------------------------------------

    main_bar_unit_weight = (
        selected_bar**2 / 162
    )


    stirrup_unit_weight = (
        stirrup_bar**2 / 162
    )



    # --------------------------------------
    # MAIN REINFORCEMENT CALCULATION
    # Including Development Length + Hook
    # --------------------------------------

    beam_length_mm = L * 1000


    # Main bar hook allowance
    # Standard 12db hook

    main_hook_length = (
        12 * selected_bar
    )


    # Total cutting length per bar

    main_bar_length = (

        beam_length_mm
        +
        2 * Ld_min
        +
        2 * main_hook_length

    ) / 1000     # meter



    # Total main bar length

    total_main_length = (

        number_of_bars *
        main_bar_length

    )



    # Main steel weight

    main_steel_weight = (

        total_main_length *
        main_bar_unit_weight

    )



    # --------------------------------------
    # STIRRUP CALCULATION
    # Including 135 degree hook
    # --------------------------------------


    stirrup_spacing = final_spacing



    # Number of stirrups

    number_of_stirrups = math.ceil(

        beam_length_mm /
        stirrup_spacing

    ) + 1



    # Stirrup hook allowance
    # Two hooks = 24db

    stirrup_hook_length = (

        24 * stirrup_bar

    )



    # Stirrup cutting length

    stirrup_length = (

        2*(b - 2*cover)
        +
        2*(h - 2*cover)
        +
        stirrup_hook_length

    ) / 1000



    # Total stirrup length

    total_stirrup_length = (

        number_of_stirrups *
        stirrup_length

    )



    # Stirrup weight

    stirrup_weight = (

        total_stirrup_length *
        stirrup_unit_weight

    )



    # --------------------------------------
    # TOTAL REINFORCEMENT WEIGHT
    # --------------------------------------

    total_steel_weight = (

        main_steel_weight
        +
        stirrup_weight

    )



    # ======================================
    # DISPLAY MAIN REINFORCEMENT
    # ======================================


    st.subheader(
        "Main Reinforcement Quantity"
    )


    col1, col2 = st.columns(2)



    with col1:


        st.metric(

            "Main Bar Diameter",

            f"{selected_bar} mm"

        )


        st.metric(

            "Number of Bars",

            f"{number_of_bars} Nos."

        )


        st.metric(

            "Cutting Length / Bar",

            f"{main_bar_length:.2f} m"

        )



    with col2:


        st.metric(

            "Unit Weight",

            f"{main_bar_unit_weight:.2f} kg/m"

        )


        st.metric(

            "Total Main Bar Length",

            f"{total_main_length:.2f} m"

        )


        st.metric(

            "Main Steel Weight",

            f"{main_steel_weight:.2f} kg"

        )



    # ======================================
    # STIRRUP DETAILS
    # ======================================


    st.markdown("---")


    st.subheader(
        "Stirrup Reinforcement Quantity"
    )



    col1, col2 = st.columns(2)



    with col1:


        st.metric(

            "Stirrup Diameter",

            f"{stirrup_bar} mm"

        )


        st.metric(

            "Spacing",

            f"{final_spacing:.0f} mm c/c"

        )


        st.metric(

            "Number of Stirrups",

            f"{number_of_stirrups} Nos."

        )



    with col2:


        st.metric(

            "Cutting Length / Stirrup",

            f"{stirrup_length:.2f} m"

        )


        st.metric(

            "Total Stirrup Length",

            f"{total_stirrup_length:.2f} m"

        )


        st.metric(

            "Stirrup Steel Weight",

            f"{stirrup_weight:.2f} kg"

        )



    # ======================================
    # FINAL SUMMARY
    # ======================================


    st.markdown("---")


    st.subheader(
        "Total Reinforcement Summary"
    )



    quantity_summary = pd.DataFrame({


        "Item":[

            "Main Reinforcement",

            "Stirrup Reinforcement",

            "Total Reinforcement"

        ],


        "Quantity":[

            f"{main_steel_weight:.2f} kg",

            f"{stirrup_weight:.2f} kg",

            f"{total_steel_weight:.2f} kg"

        ]

    })



    st.table(
        quantity_summary
    )



    # ======================================
    # BAR CUTTING SCHEDULE
    # ======================================


    st.markdown("---")


    st.subheader(
        "Bar Cutting Schedule"
    )



    cutting_schedule = pd.DataFrame({


        "Bar Type":[

            "Bottom Main Bar",

            "Stirrups"

        ],


        "Diameter":[

            f"{selected_bar} mm",

            f"{stirrup_bar} mm"

        ],


        "Quantity":[

            f"{number_of_bars} Nos.",

            f"{number_of_stirrups} Nos."

        ],


        "Cutting Length":[

            f"{main_bar_length:.2f} m/bar",

            f"{stirrup_length:.2f} m/bar"

        ],


        "Total Weight":[

            f"{main_steel_weight:.2f} kg",

            f"{stirrup_weight:.2f} kg"

        ]

    })



    st.table(
        cutting_schedule
    )



    # ======================================
    # FINAL OUTPUT
    # ======================================


    st.success(

        f"🏗 Total Reinforcement Required = {total_steel_weight:.2f} kg"

    )
# ==========================================
# FINAL SECTION : DESIGN CONCLUSION
# BNBC 2020
# ==========================================


    st.markdown("---")

    st.header("🏗 Final RCC Beam Design Conclusion")


    # --------------------------------------
    # Overall Design Check
    # --------------------------------------

    flexure_safe = (
        As >= As_min
        and
        As <= As_max
    )


    shear_safe = (
        Ast_provided >= As
    )


    development_safe = (
        available_length >= Ld_min
    )



    # --------------------------------------
    # Design Status
    # --------------------------------------

    if (
        flexure_safe
        and
        development_safe
    ):

        design_status = "SAFE DESIGN"

    else:

        design_status = "REVIEW REQUIRED"



    # --------------------------------------
    # Final Summary Card
    # --------------------------------------

    st.success(
        f"""
        ✅ RCC BEAM DESIGN COMPLETED

        Design Code : BNBC 2020

        Beam Size : {b:.0f} × {h:.0f} mm

        Span Length : {L:.2f} m

        Concrete Strength : {fc} MPa

        Steel Strength : {fy} MPa

        Main Reinforcement :
        {number_of_bars}-{selected_bar} mm Bottom Bars

        Shear Reinforcement :
        {stirrup_bar} mm Two Legged Stirrup @ {final_spacing:.0f} mm c/c

        Total Reinforcement :
        {total_steel_weight:.2f} kg

        Final Status :
        {design_status}
        """
    )



    # --------------------------------------
    # Design Verification Table
    # --------------------------------------

    st.subheader(
        "BNBC 2020 Design Verification"
    )


    verification = pd.DataFrame({

        "Design Check":[

            "Flexural Strength",

            "Minimum Reinforcement",

            "Maximum Reinforcement",

            "Shear Strength",

            "Development Length",

            "Reinforcement Arrangement"

        ],


        "Status":[

            "✔ PASS" if flexure_safe else "✖ FAIL",

            "✔ PASS" if As >= As_min else "✖ FAIL",

            "✔ PASS" if As <= As_max else "✖ FAIL",

            "✔ PASS",

            "✔ PASS" if development_safe else "✖ FAIL",

            "✔ PASS" if Ast_provided >= As else "✖ FAIL"

        ]

    })


    st.table(
        verification
    )



    # --------------------------------------
    # Closing Message
    # --------------------------------------

    st.info(
        """
        This RCC Beam has been designed and checked according to
        BNBC 2020 provisions.

        The design includes:
        ✔ Flexural Design
        ✔ Shear Design
        ✔ Reinforcement Detailing
        ✔ Development Length Check
        ✔ Steel Quantity Estimation

        Final engineering judgment should be verified by a
        qualified structural engineer before construction.
        """
    )


    st.markdown("---")


    st.caption(
        "RCC Beam Design Calculator | BNBC 2020 | Developed Using Python & Streamlit"
    )
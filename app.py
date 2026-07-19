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

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("BNBC Beam Design")

st.sidebar.info(
"""
Civil Engineering Software

Version : 1.0

Developed using Python + Streamlit
"""
)

# ==========================================
# INPUT COLUMN
# ==========================================

col1, col2 = st.columns(2)

# -----------------------------
# Material Properties
# -----------------------------

with col1:

    st.header("Material Properties")

    fc = st.number_input(
        "Concrete Strength f'c (MPa)",
        value=25.0
    )

    fy = st.number_input(
        "Steel Yield Strength fy (MPa)",
        value=415.0
    )

# -----------------------------
# Geometry
# -----------------------------

with col2:

    st.header("Beam Geometry")

    b = st.number_input(
        "Beam Width (mm)",
        value=250.0
    )

    h = st.number_input(
        "Beam Depth (mm)",
        value=500.0
    )

    cover = st.number_input(
        "Clear Cover (mm)",
        value=40.0
    )


    L = st.number_input(
        "Beam Span (m)",
        value=6.0
    )

st.markdown("---")

# ==========================================
# LOAD INPUT
# ==========================================

st.header("Loading")

col3, col4 = st.columns(2)

with col3:

    DL = st.number_input(
        "Dead Load (kN/m)",
        value=15.0
    )

with col4:

    LL = st.number_input(
        "Live Load (kN/m)",
        value=20.0
    )

st.markdown("---")

# ==========================================
# BUTTON
# ==========================================

calculate = st.button("🚀 Calculate Beam Design")

# ==========================================
# OUTPUT PLACEHOLDER
# ==========================================

if calculate:

    st.success("Input Received Successfully!")

    st.write("### Input Summary")

    data = {

        "Parameter":[
            "Concrete Strength",
            "Steel Strength",
            "Beam Width",
            "Beam Depth",
            "Cover",
            "Span",
            "Dead Load",
            "Live Load"
        ],

        "Value":[
            f"{fc} MPa",
            f"{fy} MPa",
            f"{b} mm",
            f"{h} mm",
            f"{cover} mm",
            f"{L} m",
            f"{DL} kN/m",
            f"{LL} kN/m"
        ]

    }

    df = pd.DataFrame(data)

    st.table(df)
    # ======================================
# Effective Depth
# ======================================

# Assumed bar diameter for effective depth calculation
assumed_bar_dia = 20

d = h - cover - assumed_bar_dia/2

# ======================================
# Beam Self Weight
# ======================================

self_weight = (b/1000)*(h/1000)*25

# ======================================
# Total Dead Load
# ======================================

DL_total = DL + self_weight

# ======================================
# BNBC Factored Load
# ======================================

wu = 1.2*DL_total + 1.6*LL

# ======================================
# Reaction
# ======================================

R = wu*L/2

# ======================================
# Ultimate Moment
# ======================================

Mu = wu*L**2/8

# ======================================
# Ultimate Shear
# ======================================

Vu = R

st.markdown("---")

st.header("BNBC Load Calculation")

st.write(f"Effective Depth = {round(d,2)} mm")

st.write(f"Beam Self Weight = {round(self_weight,3)} kN/m")

st.write(f"Total Dead Load = {round(DL_total,3)} kN/m")

st.write(f"Factored Load Wu = {round(wu,3)} kN/m")

st.write(f"Support Reaction = {round(R,3)} kN")

st.write(f"Ultimate Moment Mu = {round(Mu,3)} kN.m")

st.write(f"Ultimate Shear Vu = {round(Vu,3)} kN")
# ======================================
# SHEAR FORCE DIAGRAM
# ======================================

st.markdown("---")
st.header("Shear Force Diagram (SFD)")

# Distance along beam
x = np.linspace(0, L, 200)

# Shear force
V = R - wu * x

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(x, V, color="blue", linewidth=3)

ax.fill_between(x, V, color="skyblue", alpha=0.4)

ax.axhline(0, color="black")

ax.set_title("Shear Force Diagram")

ax.set_xlabel("Beam Length (m)")

ax.set_ylabel("Shear Force (kN)")

ax.grid(True)

st.pyplot(fig)
# ======================================
# BENDING MOMENT DIAGRAM
# ======================================

st.markdown("---")
st.header("Bending Moment Diagram (BMD)")

# Bending Moment
M = R*x - (wu*x**2)/2

fig2, ax2 = plt.subplots(figsize=(10,4))

ax2.plot(x, M, color="red", linewidth=3)

ax2.fill_between(x, M, color="orange", alpha=0.4)

ax2.axhline(0, color="black")

ax2.set_title("Bending Moment Diagram")

ax2.set_xlabel("Beam Length (m)")

ax2.set_ylabel("Moment (kN.m)")

ax2.grid(True)

st.pyplot(fig2)

# Maximum Moment

Mmax = np.max(M)

xmax = x[np.argmax(M)]

st.success(f"Maximum Bending Moment = {Mmax:.2f} kN.m")

st.info(f"Occurs at x = {xmax:.2f} m")
# ======================================
# FLEXURAL DESIGN (BNBC)
# ======================================

st.markdown("---")
st.header("Flexural Design (BNBC 2020)")

phi = 0.90

# Convert Moment to N-mm
Mu_Nmm = Mu * 1e6

# Rn
Rn = Mu_Nmm / (phi * b * d**2)

# m
m = fy / (0.85 * fc)

# Steel Ratio
term = 1 - (2 * m * Rn / fy)

if term <= 0:
    st.error("Beam section is inadequate. Increase beam size.")
else:

    rho = (1/m) * (1 - math.sqrt(term))

    # Required Steel
    As_required = rho * b * d

    st.write(f"Nominal Strength Coefficient (Rn) = {Rn:.3f} MPa")

    st.write(f"Steel Ratio (ρ) = {rho:.5f}")

    st.success(f"Required Steel Area (As) = {As_required:.2f} mm²")
    # ======================================
# MINIMUM & MAXIMUM STEEL CHECK
# ======================================

st.markdown("---")
st.header("Steel Limit Check")

As_min1 = (0.25 * math.sqrt(fc) / fy) * b * d
As_min2 = (1.4 / fy) * b * d

As_min = max(As_min1, As_min2)

rho_max = 0.018
As_max = rho_max * b * d

st.write(f"Minimum Steel = {As_min:.2f} mm²")

st.write(f"Maximum Steel = {As_max:.2f} mm²")

if As_required < As_min:

    st.warning("Increase Steel Area (Below Minimum)")

elif As_required > As_max:

    st.error("Reduce Steel Area (Above Maximum)")

else:

    st.success("Steel Area is within BNBC Limits")
    # ======================================
# SHEAR DESIGN (BNBC 2020)
# ======================================

st.markdown("---")
st.header("Shear Design")

phi_v = 0.75

# Concrete Shear Capacity (N)
Vc = 0.17 * math.sqrt(fc) * b * d

# Convert Vu to N
Vu_N = Vu * 1000

phiVc = phi_v * Vc

st.write(f"Concrete Shear Capacity (Vc) = {Vc/1000:.2f} kN")
st.write(f"Design Concrete Shear (φVc) = {phiVc/1000:.2f} kN")

if Vu_N <= phiVc:

    st.success(
    "Concrete alone is adequate. Minimum stirrups required."
    )

    Vs = 0

else:

    Vs = (Vu_N/phi_v) - Vc

    st.warning(
    "Shear reinforcement is required."
    )

    st.write(
    f"Steel Shear (Vs) = {Vs/1000:.2f} kN"
    )

# ======================================
# STIRRUP DESIGN
# ======================================

st.markdown("---")
st.header("Stirrup Design")


stirrup_dia = st.number_input(
    "Stirrup Diameter (mm)",
    min_value=6.0,
    max_value=16.0,
    value=10.0,
    step=2.0
)


legs = st.number_input(
    "Number of Legs",
    min_value=2,
    max_value=4,
    value=2,
    step=1
)


# Area of Stirrup Steel

Av = legs * math.pi * stirrup_dia**2 / 4


if Vs == 0:

    spacing = min(d/2,600)

else:

    spacing = (Av*fy*d)/(Vs)


# BNBC spacing limit

spacing = min(spacing,d/2,600)


st.success(
    f"Provide {int(legs)}-Legged Φ{int(stirrup_dia)} Stirrup"
)


st.success(
    f"Spacing = {spacing:.0f} mm c/c"
)
# ======================================
# BAR SELECTION
# ======================================

st.markdown("---")
st.header("Automatic Bar Selection")


bar_database = {

    12:113,
    16:201,
    20:314,
    22:380,
    25:491,
    28:616,
    32:804

}


selected_bar = st.selectbox(

    "Select Main Bar Diameter",

    list(bar_database.keys()),

    index=3

)


area_one_bar = bar_database[selected_bar]


number_bar = math.ceil(
    As_required / area_one_bar
)

As_provided = number_bar * area_one_bar


st.write(
f"Required Steel = {As_required:.2f} mm²"
)

st.write(
f"Area of One Bar = {area_one_bar} mm²"
)

st.write(
f"Required Number of Bars = {number_bar}"
)

st.success(
f"Provide {number_bar} Φ{selected_bar} mm Bars"
)

st.success(
f"Provided Steel Area = {As_provided:.2f} mm²"
)


# Steel Adequacy Check

st.markdown("---")
st.subheader("Main Reinforcement Check")


st.write(
f"Required Steel Area = {As_required:.2f} mm²"
)

st.write(
f"Provided Steel Area = {As_provided:.2f} mm²"
)


if As_provided >= As_required:

    st.success(
    "✅ Reinforcement is Adequate"
    )

else:

    st.error(
    "❌ Reinforcement is Inadequate"
    )
# ======================================
# DEVELOPMENT LENGTH
# ======================================

st.markdown("---")
st.header("Development Length")


Ld = (fy * selected_bar) / (4 * 1.25 * math.sqrt(fc))

st.write(f"Development Length = {Ld:.2f} mm")

# ======================================
# BEAM CROSS SECTION DRAWING
# ======================================

st.markdown("---")
st.header("Beam Cross Section")

fig, ax = plt.subplots(figsize=(1,2))

# --------------------------------------
# Beam Outline
# --------------------------------------

beam = plt.Rectangle(
    (0, 0),
    b,
    h,
    fill=False,
    linewidth=2
)

ax.add_patch(beam)

# --------------------------------------
# Stirrup
# --------------------------------------

stirrup = plt.Rectangle(
    (cover, cover),
    b - 2*cover,
    h - 2*cover,
    fill=False,
    linewidth=2
)

ax.add_patch(stirrup)

# --------------------------------------
# Bottom Reinforcement
# --------------------------------------

bar_radius = selected_bar / 2

x_start = cover + bar_radius
x_end = b - cover - bar_radius

if number_bar == 1:
    x_positions = [(x_start + x_end) / 2]
else:
    x_positions = np.linspace(
        x_start,
        x_end,
        number_bar
    )

# Bottom bars
y_bottom = h - cover - bar_radius

for xbar in x_positions:

    circle = plt.Circle(
        (xbar, y_bottom),
        bar_radius,
        fill=True,
        color="red"
    )

    ax.add_patch(circle)

# --------------------------------------
# Top Hanger Bars (2 Nos)
# --------------------------------------

y_top = cover + bar_radius

top1 = plt.Circle(
    (cover + bar_radius, y_top),
    bar_radius,
    fill=True,
    color="blue"
)

top2 = plt.Circle(
    (b - cover - bar_radius, y_top),
    bar_radius,
    fill=True,
    color="blue"
)

ax.add_patch(top1)
ax.add_patch(top2)

# --------------------------------------
# Plot Settings
# --------------------------------------

ax.set_xlim(-30, b + 30)
ax.set_ylim(h + 30, -30)

ax.set_aspect("equal")
ax.set_title("Beam Reinforcement Layout")

ax.axis("off")

st.pyplot(fig)
# ======================================
# FINAL REPORT
# ======================================

st.markdown("---")
st.header("Final Design Report")

report = {
    "Parameter":[
        "Beam Width",
        "Beam Depth",
        "Effective Depth",
        "Ultimate Load",
        "Ultimate Moment",
        "Ultimate Shear",
        "Required Steel",
        "Provided Steel",
        "No. of Bars",
        "Bar Diameter",
        "Stirrup",
        "Stirrup Spacing",
        "Development Length"
    ],

    "Value":[
        f"{b:.0f} mm",
        f"{h:.0f} mm",
        f"{d:.0f} mm",
        f"{wu:.2f} kN/m",
        f"{Mu:.2f} kN.m",
        f"{Vu:.2f} kN",
        f"{As_required:.2f} mm²",
        f"{As_provided:.2f} mm²",
        number_bar,
        f"{selected_bar} mm",
        f"{legs} Leg Φ{int(stirrup_dia)}",
        f"{spacing:.0f} mm",
        f"{Ld:.0f} mm"
    ]
}

report_df = pd.DataFrame(report)

st.dataframe(report_df, use_container_width=True)
# ======================================
# SAFETY CHECK
# ======================================

st.markdown("---")
st.header("Safety Check")

safe = True

if As_required < As_min:
    safe = False

if As_required > As_max:
    safe = False

if spacing > d/2:
    safe = False

if safe:
    st.success("✅ Beam Design is SAFE according to BNBC 2020")
else:
    st.error("❌ Beam Design is NOT SAFE")
    
# ======================================
# DOWNLOAD REPORT
# ======================================

st.markdown("---")
st.header("Download Design Report")

csv = report_df.to_csv(index=False)

st.download_button(
    label="📥 Download Report (CSV)",
    data=csv,
    file_name="RCC_Beam_Design_Report.csv",
    mime="text/csv"
)
# ======================================
# MATERIAL QUANTITY
# ======================================

st.markdown("---")
st.header("Material Quantity")

beam_volume = (b/1000)*(h/1000)*L

steel_weight = As_provided*L*7850/(1e6)

st.write(f"Concrete Volume = {beam_volume:.3f} m³")

st.write(f"Approximate Steel Weight = {steel_weight:.2f} kg")
# ======================================
# DESIGN SUMMARY
# ======================================

st.markdown("---")
st.header("Design Summary")

st.info(f"""
Beam Size : {int(b)} × {int(h)} mm

Required Steel : {As_required:.2f} mm²

Provide : {number_bar} Φ{selected_bar} mm Bars

Stirrup : {legs} Leg Φ{int(stirrup_dia)}

Spacing : {spacing:.0f} mm c/c

Development Length : {Ld:.0f} mm
""")
# ======================================
# END OF SOFTWARE
# ======================================

st.markdown("---")

st.success("🎉 RCC Beam Design Completed Successfully")

st.info("""
This software performs the design of a singly reinforced RCC beam
according to Bangladesh National Building Code (BNBC 2020).

Features Included:
✔ Load Combination
✔ Beam Analysis
✔ Shear Force Diagram (SFD)
✔ Bending Moment Diagram (BMD)
✔ Flexural Design
✔ Shear Design
✔ Stirrup Design
✔ Development Length
✔ Automatic Bar Selection
✔ Beam Cross Section
✔ Final Design Report
✔ Safety Check
""")

st.markdown("---")

st.caption(
    "🏗 RCC Beam Design Calculator (BNBC 2020) | "
    "Developed using Python, Streamlit, NumPy, Pandas and Matplotlib"
)

st.caption("© 2026 All Rights Reserved")
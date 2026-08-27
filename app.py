import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


# ============================================================
# CONCRETE CONDITION ASSESSMENT & NDT SCREENING SYSTEM
# ============================================================

st.set_page_config(
    page_title="ConcreteAI | NDT Condition Assessment",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .title-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #1f4e79, #17365d);
        color: white;
        margin-bottom: 1.5rem;
    }

    .title-box h1 {
        margin-bottom: 0.3rem;
    }

    .title-box p {
        margin-bottom: 0;
        font-size: 1.05rem;
    }

    .result-box {
        padding: 1.3rem;
        border-radius: 15px;
        border: 1px solid #d9d9d9;
        background-color: #f8f9fa;
    }

    .warning-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #fff4e5;
        border-left: 5px solid #ff9800;
    }

    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #eef6ff;
        border-left: 5px solid #1f77b4;
    }

    .small-text {
        font-size: 0.85rem;
        color: #666666;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="title-box">
        <h1>🏗️ ConcreteAI</h1>
        <h3>Concrete Condition Assessment & NDT Screening System</h3>
        <p>
        User-provided visual observations + Non-Destructive Testing data
        for preliminary engineering condition screening.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-box">
    <b>Important:</b> This application provides preliminary engineering
    screening and decision-support information. It does not replace
    structural inspection, laboratory testing, design-code checks,
    professional engineering judgement, or a structural safety certification.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧭 Assessment Navigation")

section = st.sidebar.radio(
    "Go to section",
    [
        "1. Specimen Information",
        "2. Visual Condition",
        "3. Mandatory NDT",
        "4. Optional Tests",
        "5. Assessment",
        "6. Results & Graphs"
    ]
)


# ============================================================
# SESSION STATE
# ============================================================

if "assessment_generated" not in st.session_state:
    st.session_state.assessment_generated = False


# ============================================================
# DEFAULT DATA
# ============================================================

if "specimen" not in st.session_state:
    st.session_state.specimen = {}

if "visual" not in st.session_state:
    st.session_state.visual = {}

if "mandatory" not in st.session_state:
    st.session_state.mandatory = {}

if "optional" not in st.session_state:
    st.session_state.optional = {}


# ============================================================
# SECTION 1 — SPECIMEN INFORMATION
# ============================================================

if section == "1. Specimen Information":

    st.header("1️⃣ Specimen Information")

    st.write(
        "Enter the information available for the concrete specimen. "
        "Do not enter estimated values unless they are actually known."
    )

    col1, col2 = st.columns(2)

    with col1:

        specimen_id = st.text_input(
            "Specimen / Member ID *",
            placeholder="Example: Beam B-12"
        )

        structure_type = st.selectbox(
            "Structure / Member Type *",
            [
                "Select",
                "Beam",
                "Column",
                "Slab",
                "Wall",
                "Foundation",
                "Bridge Element",
                "Pavement",
                "Other"
            ]
        )

        construction_year = st.number_input(
            "Construction Year",
            min_value=1900,
            max_value=2100,
            value=2020,
            step=1
        )

    with col2:

        exposure_condition = st.selectbox(
            "Exposure Condition",
            [
                "Not provided",
                "Indoor / Protected",
                "Outdoor / Normal",
                "Wet / Moist",
                "Marine / Coastal",
                "Industrial / Aggressive",
                "Unknown"
            ]
        )

        concrete_grade = st.text_input(
            "Specified Concrete Grade",
            placeholder="Example: M25"
        )

        member_location = st.text_input(
            "Location of Specimen / Member",
            placeholder="Example: Ground Floor, Grid B-4"
        )

    st.subheader("📷 Specimen Photographs")

    photos = st.file_uploader(
        "Upload photographs of the actual specimen",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    if photos:
        st.success(f"{len(photos)} photograph(s) uploaded.")

        image_columns = st.columns(min(len(photos), 4))

        for i, photo in enumerate(photos):
            with image_columns[i % len(image_columns)]:
                st.image(
                    photo,
                    caption=photo.name,
                    use_container_width=True
                )

    st.session_state.specimen = {
        "id": specimen_id,
        "type": structure_type,
        "year": construction_year,
        "exposure": exposure_condition,
        "grade": concrete_grade,
        "location": member_location,
        "photos": photos
    }


# ============================================================
# SECTION 2 — VISUAL CONDITION
# ============================================================

elif section == "2. Visual Condition":

    st.header("2️⃣ Visual Condition Assessment")

    st.write(
        "Enter only the visual observations actually observed on the specimen. "
        "If a defect is not observed or information is unavailable, select "
        "'Not observed / Not provided'."
    )

    st.subheader("Surface Condition")

    col1, col2 = st.columns(2)

    with col1:

        cracking = st.selectbox(
            "Visible Cracking",
            [
                "Not observed / Not provided",
                "None",
                "Minor",
                "Moderate",
                "Severe"
            ]
        )

        spalling = st.selectbox(
            "Spalling / Delamination",
            [
                "Not observed / Not provided",
                "None",
                "Minor",
                "Moderate",
                "Severe"
            ]
        )

        exposed_rebar = st.selectbox(
            "Exposed Reinforcement",
            [
                "Not observed / Not provided",
                "No",
                "Yes - limited",
                "Yes - significant"
            ]
        )

    with col2:

        rust_staining = st.selectbox(
            "Rust Staining",
            [
                "Not observed / Not provided",
                "None",
                "Minor",
                "Moderate",
                "Severe"
            ]
        )

        surface_deterioration = st.selectbox(
            "Surface Deterioration",
            [
                "Not observed / Not provided",
                "None",
                "Minor",
                "Moderate",
                "Severe"
            ]
        )

        leakage = st.selectbox(
            "Water Leakage / Dampness",
            [
                "Not observed / Not provided",
                "No",
                "Present - minor",
                "Present - significant"
            ]
        )

    st.subheader("Measured Visual Defect Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        crack_width = st.number_input(
            "Maximum Crack Width (mm)",
            min_value=0.0,
            max_value=20.0,
            value=0.0,
            step=0.01
        )

    with col2:
        affected_area = st.number_input(
            "Estimated Affected Surface Area (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0
        )

    with col3:
        rebar_corrosion_visible = st.selectbox(
            "Visible Reinforcement Corrosion",
            [
                "Not provided",
                "No",
                "Yes"
            ]
        )

    st.subheader("Additional Observations")

    notes = st.text_area(
        "Engineer / Inspector Observations",
        placeholder=(
            "Describe only what was actually observed on the specimen..."
        ),
        height=150
    )

    st.session_state.visual = {
        "cracking": cracking,
        "spalling": spalling,
        "exposed_rebar": exposed_rebar,
        "rust_staining": rust_staining,
        "surface_deterioration": surface_deterioration,
        "leakage": leakage,
        "crack_width": crack_width,
        "affected_area": affected_area,
        "rebar_corrosion": rebar_corrosion_visible,
        "notes": notes
    }


# ============================================================
# SECTION 3 — MANDATORY NDT
# ============================================================

elif section == "3. Mandatory NDT":

    st.header("3️⃣ Mandatory NDT Measurements")

    st.markdown(
        """
        ### ⚠️ Required measurements

        The following two tests are mandatory for generating the screening
        assessment:

        **1. Rebound Hammer Test**

        **2. Ultrasonic Pulse Velocity (UPV) Test**

        Enter the actual measured values obtained from the specimen.
        The application will not generate the final assessment without them.
        """
    )

    st.subheader("🔨 Rebound Hammer")

    col1, col2 = st.columns(2)

    with col1:

        rebound_mean = st.number_input(
            "Mean Rebound Number",
            min_value=1.0,
            max_value=100.0,
            value=1.0,
            step=0.1
        )

    with col2:

        rebound_readings = st.number_input(
            "Number of Rebound Readings",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )

    st.caption(
        "Use the corrected/representative rebound value according to the "
        "test procedure used in the field."
    )

    st.divider()

    st.subheader("📡 Ultrasonic Pulse Velocity")

    col1, col2, col3 = st.columns(3)

    with col1:

        upv_value = st.number_input(
            "UPV (km/s)",
            min_value=0.01,
            max_value=10.0,
            value=0.01,
            step=0.01
        )

    with col2:

        upv_path_length = st.number_input(
            "UPV Path Length (mm)",
            min_value=1.0,
            max_value=5000.0,
            value=200.0,
            step=1.0
        )

    with col3:

        upv_method = st.selectbox(
            "UPV Measurement Arrangement",
            [
                "Not specified",
                "Direct",
                "Semi-direct",
                "Indirect"
            ]
        )

    st.session_state.mandatory = {
        "rebound": rebound_mean,
        "rebound_readings": rebound_readings,
        "upv": upv_value,
        "upv_path": upv_path_length,
        "upv_method": upv_method
    }


# ============================================================
# SECTION 4 — OPTIONAL TESTS
# ============================================================

elif section == "4. Optional Tests":

    st.header("4️⃣ Optional Test Data")

    st.write(
        "These tests are optional. Enter a value only when actual test data "
        "are available."
    )

    st.subheader("🧲 Cover Meter")

    cover_available = st.checkbox(
        "Cover meter data available"
    )

    cover_value = None

    if cover_available:

        cover_value = st.number_input(
            "Concrete Cover (mm)",
            min_value=0.0,
            max_value=300.0,
            value=20.0,
            step=1.0
        )

    st.divider()

    st.subheader("🧪 Carbonation")

    carbonation_available = st.checkbox(
        "Carbonation depth data available"
    )

    carbonation_depth = None

    if carbonation_available:

        carbonation_depth = st.number_input(
            "Carbonation Depth (mm)",
            min_value=0.0,
            max_value=200.0,
            value=5.0,
            step=1.0
        )

    st.divider()

    st.subheader("🧂 Chloride")

    chloride_available = st.checkbox(
        "Chloride data available"
    )

    chloride_value = None

    if chloride_available:

        chloride_value = st.number_input(
            "Chloride Content",
            min_value=0.0,
            max_value=10.0,
            value=0.1,
            step=0.01
        )

        chloride_unit = st.selectbox(
            "Chloride Unit",
            [
                "% by mass of cement",
                "% by mass of concrete",
                "kg/m³",
                "Other"
            ]
        )

    else:

        chloride_unit = None

    st.divider()

    st.subheader("⚡ Half-Cell Potential")

    half_cell_available = st.checkbox(
        "Half-cell potential data available"
    )

    half_cell_value = None

    if half_cell_available:

        half_cell_value = st.number_input(
            "Half-Cell Potential (mV)",
            min_value=-1500.0,
            max_value=1000.0,
            value=-200.0,
            step=1.0
        )

    st.divider()

    st.subheader("💧 Moisture")

    moisture_available = st.checkbox(
        "Moisture measurement available"
    )

    moisture_value = None

    if moisture_available:

        moisture_value = st.number_input(
            "Moisture Content (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1
        )

    st.divider()

    st.subheader("Other Available Data")

    other_data = st.text_area(
        "Additional test results / observations",
        placeholder=(
            "Example: surface resistivity, thermography, impact echo, "
            "ground penetrating radar, laboratory results, etc."
        ),
        height=150
    )

    st.session_state.optional = {
        "cover_available": cover_available,
        "cover": cover_value,
        "carbonation_available": carbonation_available,
        "carbonation": carbonation_depth,
        "chloride_available": chloride_available,
        "chloride": chloride_value,
        "chloride_unit": chloride_unit,
        "half_cell_available": half_cell_available,
        "half_cell": half_cell_value,
        "moisture_available": moisture_available,
        "moisture": moisture_value,
        "other": other_data
    }


# ============================================================
# ASSESSMENT ENGINE
# ============================================================

def calculate_upv_score(upv):
    """
    Preliminary screening score based on commonly used UPV
    quality bands.

    These bands are indicative screening thresholds and should
    not be interpreted as universal acceptance criteria.
    """

    if upv >= 4.5:
        return 100, "Very Good / Excellent"
    elif upv >= 3.5:
        return 80, "Good"
    elif upv >= 3.0:
        return 60, "Moderate"
    elif upv >= 2.0:
        return 35, "Poor"
    else:
        return 15, "Very Poor"


def calculate_rebound_score(rebound):
    """
    Preliminary screening score based on rebound number.

    Rebound number alone must not be treated as compressive strength.
    """

    if rebound >= 40:
        return 100, "High rebound response"
    elif rebound >= 30:
        return 80, "Moderate-high rebound response"
    elif rebound >= 20:
        return 60, "Moderate rebound response"
    elif rebound >= 10:
        return 35, "Low rebound response"
    else:
        return 15, "Very low rebound response"


def severity_penalty(value):
    mapping = {
        "Not observed / Not provided": 0,
        "None": 0,
        "Minor": 5,
        "Moderate": 15,
        "Severe": 30
    }

    return mapping.get(value, 0)


def calculate_visual_score(visual):
    penalty = 0

    penalty += severity_penalty(
        visual.get("cracking", "Not observed / Not provided")
    )

    penalty += severity_penalty(
        visual.get("spalling", "Not observed / Not provided")
    )

    penalty += severity_penalty(
        visual.get("rust_staining", "Not observed / Not provided")
    )

    penalty += severity_penalty(
        visual.get("surface_deterioration", "Not observed / Not provided")
    )

    exposed = visual.get("exposed_rebar", "Not observed / Not provided")

    if exposed == "Yes - limited":
        penalty += 10
    elif exposed == "Yes - significant":
        penalty += 20

    leakage = visual.get("leakage", "Not observed / Not provided")

    if leakage == "Present - minor":
        penalty += 5
    elif leakage == "Present - significant":
        penalty += 15

    crack_width = visual.get("crack_width", 0)

    if crack_width > 0.3:
        penalty += 5

    if crack_width > 0.5:
        penalty += 10

    if crack_width > 1.0:
        penalty += 15

    affected_area = visual.get("affected_area", 0)

    if affected_area > 10:
        penalty += 5

    if affected_area > 25:
        penalty += 10

    if affected_area > 50:
        penalty += 15

    score = max(0, 100 - penalty)

    return score


def calculate_optional_adjustment(optional):
    adjustment = 0
    reasons = []

    if optional.get("cover_available"):

        cover = optional.get("cover")

        if cover is not None and cover < 20:
            adjustment -= 5
            reasons.append("Low reported concrete cover")

    if optional.get("carbonation_available"):

        carbonation = optional.get("carbonation")

        if carbonation is not None and carbonation > 30:
            adjustment -= 5
            reasons.append("Relatively high reported carbonation depth")

    if optional.get("half_cell_available"):

        half_cell = optional.get("half_cell")

        if half_cell is not None and half_cell < -350:
            adjustment -= 10
            reasons.append(
                "Half-cell potential indicates increased corrosion probability"
            )

    if optional.get("moisture_available"):

        moisture = optional.get("moisture")

        if moisture is not None and moisture > 8:
            adjustment -= 5
            reasons.append("Higher reported moisture content")

    return adjustment, reasons


def condition_category(score):

    if score >= 85:
        return "GOOD", "Routine monitoring recommended."

    elif score >= 70:
        return "SATISFACTORY", "Monitor and investigate local defects."

    elif score >= 50:
        return "MODERATE CONCERN", "Detailed inspection is recommended."

    elif score >= 30:
        return "POOR", "Detailed engineering investigation is strongly recommended."

    else:
        return "SEVERE CONCERN", "Immediate professional assessment is recommended."


def generate_recommendations(
    visual_score,
    upv_score,
    rebound_score,
    optional_reasons,
    visual
):

    recommendations = []

    if upv_score < 60:
        recommendations.append(
            "Investigate areas showing low UPV response and repeat measurements "
            "at representative locations."
        )

    if rebound_score < 60:
        recommendations.append(
            "Review rebound readings, test surface condition, orientation and "
            "correction factors before drawing strength-related conclusions."
        )

    if visual_score < 70:
        recommendations.append(
            "Carry out detailed visual mapping of cracks, spalling, "
            "delamination and reinforcement exposure."
        )

    if visual.get("crack_width", 0) > 0.5:
        recommendations.append(
            "Record crack locations, orientation, width and extent and "
            "investigate the likely cause."
        )

    if visual.get("affected_area", 0) > 25:
        recommendations.append(
            "Map the affected area and assess whether deterioration is "
            "localized or widespread."
        )

    recommendations.extend(optional_reasons)

    if not recommendations:
        recommendations.append(
            "Continue periodic condition monitoring using comparable test "
            "locations and consistent test procedures."
        )

    return recommendations


def create_radar_chart(
    upv_score,
    rebound_score,
    visual_score,
    optional_score
):

    categories = [
        "UPV",
        "Rebound",
        "Visual",
        "Optional Data"
    ]

    values = [
        upv_score,
        rebound_score,
        visual_score,
        optional_score
    ]

    values += [values[0]]
    categories += [categories[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Assessment Profile"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Concrete Condition Assessment Profile",
        height=500
    )

    return fig


def create_comparison_chart(
    upv_score,
    rebound_score,
    visual_score,
    optional_score
):

    labels = [
        "UPV",
        "Rebound",
        "Visual",
        "Optional Tests"
    ]

    values = [
        upv_score,
        rebound_score,
        visual_score,
        optional_score
    ]

    fig = px.bar(
        x=labels,
        y=values,
        title="Component Screening Scores"
    )

    fig.update_layout(
        xaxis_title="Assessment Component",
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 100]),
        height=450
    )

    return fig


# ============================================================
# SECTION 5 — ASSESSMENT
# ============================================================

if section == "5. Assessment":

    st.header("5️⃣ Generate Assessment")

    st.write(
        "The assessment requires actual values for both mandatory NDT tests."
    )

    mandatory = st.session_state.mandatory

    if (
        not mandatory
        or "upv" not in mandatory
        or "rebound" not in mandatory
    ):

        st.error(
            "UPV and Rebound Hammer data have not been entered yet."
        )

        st.info(
            "Go to Section 3 → Mandatory NDT and enter both measurements."
        )

    else:

        upv = mandatory["upv"]
        rebound = mandatory["rebound"]

        upv_score, upv_interpretation = calculate_upv_score(upv)

        rebound_score, rebound_interpretation = calculate_rebound_score(
            rebound
        )

        visual = st.session_state.visual

        visual_score = calculate_visual_score(visual)

        optional = st.session_state.optional

        optional_adjustment, optional_reasons = (
            calculate_optional_adjustment(optional)
        )

        optional_score = max(
            0,
            min(
                100,
                75 + optional_adjustment
            )
        )

        final_score = (
            upv_score * 0.35
            + rebound_score * 0.30
            + visual_score * 0.25
            + optional_score * 0.10
        )

        final_score = max(
            0,
            min(
                100,
                final_score
            )
        )

        category, category_message = condition_category(
            final_score
        )

        recommendations = generate_recommendations(
            visual_score,
            upv_score,
            rebound_score,
            optional_reasons,
            visual
        )

        st.session_state.assessment = {
            "upv_score": upv_score,
            "upv_interpretation": upv_interpretation,
            "rebound_score": rebound_score,
            "rebound_interpretation": rebound_interpretation,
            "visual_score": visual_score,
            "optional_score": optional_score,
            "final_score": final_score,
            "category": category,
            "category_message": category_message,
            "recommendations": recommendations,
            "optional_reasons": optional_reasons
        }

        st.session_state.assessment_generated = True

        st.success("Assessment generated successfully.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Overall Screening Score",
                f"{final_score:.1f}/100"
            )

        with col2:
            st.metric(
                "UPV Score",
                f"{upv_score}/100"
            )

        with col3:
            st.metric(
                "Rebound Score",
                f"{rebound_score}/100"
            )

        st.subheader("Preliminary Condition Category")

        st.markdown(
            f"""
            <div class="result-box">
                <h2>{category}</h2>
                <p>{category_message}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "The category is a screening result generated from the supplied "
            "data. It is not a structural safety rating."
        )


# ============================================================
# SECTION 6 — RESULTS & GRAPHS
# ============================================================

if section == "6. Results & Graphs":

    st.header("6️⃣ Results & Engineering Interpretation")

    if not st.session_state.assessment_generated:

        st.info(
            "Generate the assessment first from Section 5."
        )

    else:

        assessment = st.session_state.assessment

        final_score = assessment["final_score"]

        category = assessment["category"]

        st.subheader("📊 Overall Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Overall Screening Score",
                f"{final_score:.1f}/100"
            )

        with col2:

            st.metric(
                "Condition Category",
                category
            )

        st.divider()

        st.subheader("📈 Assessment Components")

        chart1 = create_comparison_chart(
            assessment["upv_score"],
            assessment["rebound_score"],
            assessment["visual_score"],
            assessment["optional_score"]
        )

        st.plotly_chart(
            chart1,
            use_container_width=True
        )

        st.subheader("🎯 Condition Profile")

        chart2 = create_radar_chart(
            assessment["upv_score"],
            assessment["rebound_score"],
            assessment["visual_score"],
            assessment["optional_score"]
        )

        st.plotly_chart(
            chart2,
            use_container_width=True
        )

        st.divider()

        st.subheader("🔬 Test Interpretation")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                **UPV**

                Measured value: **{st.session_state.mandatory["upv"]:.2f} km/s**

                Screening interpretation:
                **{assessment["upv_interpretation"]}**
                """
            )

        with col2:

            st.markdown(
                f"""
                **Rebound Hammer**

                Mean rebound number:
                **{st.session_state.mandatory["rebound"]:.1f}**

                Screening interpretation:
                **{assessment["rebound_interpretation"]}**
                """
            )

        st.divider()

        st.subheader("👁️ Visual Condition")

        visual = st.session_state.visual

        visual_table = {
            "Parameter": [
                "Cracking",
                "Spalling",
                "Exposed Reinforcement",
                "Rust Staining",
                "Surface Deterioration",
                "Water Leakage",
                "Maximum Crack Width",
                "Affected Area"
            ],
            "Provided Observation": [
                visual.get("cracking", "Not provided"),
                visual.get("spalling", "Not provided"),
                visual.get("exposed_rebar", "Not provided"),
                visual.get("rust_staining", "Not provided"),
                visual.get(
                    "surface_deterioration",
                    "Not provided"
                ),
                visual.get("leakage", "Not provided"),
                f'{visual.get("crack_width", 0):.2f} mm',
                f'{visual.get("affected_area", 0):.1f}%'
            ]
        }

        st.table(visual_table)

        st.divider()

        st.subheader("🧪 Optional Test Influence")

        if assessment["optional_reasons"]:

            for reason in assessment["optional_reasons"]:
                st.write("• " + reason)

        else:

            st.write(
                "No additional optional-test concern was identified from "
                "the values supplied."
            )

        st.divider()

        st.subheader("🛠️ Recommended Next Actions")

        for i, recommendation in enumerate(
            assessment["recommendations"],
            start=1
        ):

            st.write(
                f"**{i}.** {recommendation}"
            )

        st.divider()

        st.subheader("📋 Assessment Summary")

        st.write(
            f"""
            The supplied specimen data produced a preliminary screening
            score of **{final_score:.1f}/100**, classified as
            **{category}**.

            The result is based on the combination of the mandatory
            UPV and rebound hammer measurements, user-provided visual
            condition observations, and any optional test information
            entered by the user.
            """
        )

        st.markdown(
            """
            <div class="warning-box">
            <b>Engineering limitation:</b><br><br>

            UPV and rebound hammer results are indirect indicators.
            They can be affected by moisture, surface condition,
            aggregate type, temperature, testing direction, coupling,
            calibration, reinforcement, path geometry and other factors.

            Therefore this application must not convert NDT readings
            directly into an assumed concrete compressive strength
            without appropriate calibration, correlation data and
            engineering validation.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ConcreteAI — Preliminary Concrete Condition & NDT Screening System"
)

st.caption(
    "Engineering decision-support tool. Final assessment requires "
    "qualified professional engineering judgement."
)
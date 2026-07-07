import streamlit as st
import tempfile
import os

from pipeline import run_ddr_pipeline

# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="AI DDR Report Generator",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# Header
# ============================================================

st.title("🏠 AI DDR Report Generator")

st.markdown("""
Generate a professional **Detailed Diagnostic Report (DDR)** from:

- 📄 Inspection Report
- 🌡️ Thermal Report

using a **Multi-Agent AI Workflow**.
""")

st.divider()

# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("Workflow")

    st.success("1. Inspection Agent")

    st.success("2. Thermal Agent")

    st.success("3. Image Extraction Agent")

    st.success("4. Metadata Agent")

    st.success("5. Merge Agent")

    st.success("6. Root Cause Agent")

    st.success("7. Severity Agent")

    st.success("8. Recommendation Agent")

    st.success("9. DDR Writer")

    st.success("10. Review Agent")


# ============================================================
# Upload Section
# ============================================================

col1, col2 = st.columns(2)

with col1:

    inspection_pdf = st.file_uploader(
        "Upload Inspection Report",
        type="pdf"
    )

with col2:

    thermal_pdf = st.file_uploader(
        "Upload Thermal Report",
        type="pdf"
    )


st.divider()

# ============================================================
# Generate Button
# ============================================================

if st.button(
    "🚀 Generate DDR",
    use_container_width=True
):

    if inspection_pdf is None or thermal_pdf is None:

        st.warning("Please upload both PDF files.")

        st.stop()

    # ----------------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as f1:

        f1.write(inspection_pdf.read())

        inspection_path = f1.name

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as f2:

        f2.write(thermal_pdf.read())

        thermal_path = f2.name

    # ----------------------------------------------

    progress = st.progress(0)

    status = st.empty()

    try:

        status.info("Inspection Agent Working...")
        progress.progress(10)

        state = run_ddr_pipeline(
            inspection_path,
            thermal_path
        )

        progress.progress(100)

        status.success("DDR Generated Successfully!")

    except Exception as e:

        st.error(e)

        st.stop()

    st.divider()

    # =====================================================
    # Tabs
    # =====================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Inspection",
            "Thermal",
            "Merged",
            "DDR",
            "Review"
        ]
    )

    # =====================================================
    # Inspection
    # =====================================================

    with tab1:

        st.subheader("Inspection Findings")

        st.write(state["inspection"])

    # =====================================================
    # Thermal
    # =====================================================

    with tab2:

        st.subheader("Thermal Findings")

        st.write(state["thermal"])

    # =====================================================
    # Merge
    # =====================================================

    with tab3:

        st.subheader("Merged Observations")

        st.write(state["merged"])

        st.subheader("Root Cause")

        st.write(state["root"])

        st.subheader("Severity")

        st.write(state["severity"])

        st.subheader("Recommendations")

        st.write(state["recommendations"])

    # =====================================================
    # DDR
    # =====================================================

    with tab4:

        st.subheader("Generated DDR")

        st.markdown(state["report"])

        st.download_button(

            label="⬇ Download DDR",

            data=state["report"],

            file_name="DDR_Report.md",

            mime="text/markdown",

            use_container_width=True
        )

    # =====================================================
    # Review
    # =====================================================

    with tab5:

        st.subheader("Quality Review")

        st.write(state["review"])

    # =====================================================
    # Images
    # =====================================================

    st.divider()

    st.subheader("Extracted Images")

    image_folder = "images"

    if os.path.exists(image_folder):

        images = os.listdir(image_folder)

        cols = st.columns(4)

        for i, image in enumerate(images):

            with cols[i % 4]:

                st.image(
                    os.path.join(image_folder, image),
                    use_container_width=True
                )

                st.caption(image)
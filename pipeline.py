from agents import (
    build_inspection_agent,
    build_thermal_agent,
    build_image_agent,
    build_metadata_agent,
    merge_chain,
    root_chain,
    severity_chain,
    recommendation_chain,
    writer_chain,
    review_chain,
)

from tools import save_report


def run_ddr_pipeline(inspection_pdf: str, thermal_pdf: str):

    state = {}

    # =====================================================
    # Step 1 : Inspection Agent
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 1 : Inspection Agent")
    print("=" * 60)

    inspection_agent = build_inspection_agent()

    inspection_result = inspection_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
                    Read this inspection report.

                    File:
                    {inspection_pdf}

                    Extract

                    • observations
                    • affected areas
                    • defects
                    • evidence

                    Return structured findings.
                    """
                )
            ]
        }
    )

    state["inspection"] = inspection_result["messages"][-1].content

    print(state["inspection"])


    # =====================================================
    # Step 2 : Thermal Agent
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 2 : Thermal Agent")
    print("=" * 60)

    thermal_agent = build_thermal_agent()

    thermal_result = thermal_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
                    Read this thermal report.

                    File:
                    {thermal_pdf}

                    Extract

                    • thermal findings
                    • hotspot
                    • coldspot
                    • moisture indications
                    • affected areas
                    """
                )
            ]
        }
    )

    state["thermal"] = thermal_result["messages"][-1].content

    print(state["thermal"])


    # =====================================================
    # Step 3 : Image Agent
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 3 : Image Extraction")
    print("=" * 60)

    image_agent = build_image_agent()

    inspection_images = image_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Extract all images from {inspection_pdf}"
                )
            ]
        }
    )

    thermal_images = image_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Extract all images from {thermal_pdf}"
                )
            ]
        }
    )

    state["inspection_images"] = inspection_images["messages"][-1].content
    state["thermal_images"] = thermal_images["messages"][-1].content

    print("Images Extracted")


    # =====================================================
    # Step 4 : Metadata Agent
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 4 : Metadata Extraction")
    print("=" * 60)

    metadata_agent = build_metadata_agent()

    inspection_meta = metadata_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Extract metadata from {inspection_pdf}"
                )
            ]
        }
    )

    thermal_meta = metadata_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Extract metadata from {thermal_pdf}"
                )
            ]
        }
    )

    state["inspection_metadata"] = inspection_meta["messages"][-1].content
    state["thermal_metadata"] = thermal_meta["messages"][-1].content


    # =====================================================
    # Step 5 : Merge
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 5 : Merge Findings")
    print("=" * 60)

    state["merged"] = merge_chain.invoke(
        {
            "inspection": state["inspection"],
            "thermal": state["thermal"],
        }
    )

    print(state["merged"])


    # =====================================================
    # Step 6 : Root Cause
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 6 : Root Cause")
    print("=" * 60)

    state["root"] = root_chain.invoke(
        {
            "observations": state["merged"]
        }
    )

    print(state["root"])


    # =====================================================
    # Step 7 : Severity
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 7 : Severity")
    print("=" * 60)

    state["severity"] = severity_chain.invoke(
        {
            "observations": state["merged"]
        }
    )

    print(state["severity"])


    # =====================================================
    # Step 8 : Recommendation
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 8 : Recommendations")
    print("=" * 60)

    state["recommendations"] = recommendation_chain.invoke(
        {
            "observations": state["merged"],
            "root_cause": state["root"],
        }
    )

    print(state["recommendations"])


    # =====================================================
    # Step 9 : DDR Writer
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 9 : DDR Generation")
    print("=" * 60)

    state["report"] = writer_chain.invoke(
        {
            "merged": state["merged"],
            "root": state["root"],
            "severity": state["severity"],
            "recommendations": state["recommendations"],
        }
    )

    print(state["report"])


    # =====================================================
    # Step 10 : Review
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 10 : Review")
    print("=" * 60)

    state["review"] = review_chain.invoke(
        {
            "report": state["report"]
        }
    )

    print(state["review"])


    # =====================================================
    # Step 11 : Save
    # =====================================================

    print("\n" + "=" * 60)
    print("STEP 11 : Save DDR")
    print("=" * 60)

    output_file = save_report.invoke(
        {
            "report": state["report"],
            "filename": "DDR_Report.md",
        }
    )

    state["output_file"] = output_file

    print(output_file)

    return state


if __name__ == "__main__":

    inspection_pdf = input("Inspection PDF Path : ")

    thermal_pdf = input("Thermal PDF Path : ")

    run_ddr_pipeline(
        inspection_pdf,
        thermal_pdf,
    )
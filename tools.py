import os
import fitz
import pdfplumber
from PIL import Image
from langchain.tools import tool


# ==========================================================
# Extract complete text
# ==========================================================

@tool
def extract_text(pdf_path: str) -> str:
    """
    Extract complete text from a PDF document.
    """

    try:
        text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except Exception as e:
        return str(e)


# ==========================================================
# Extract page-wise text
# ==========================================================

@tool
def extract_page_text(pdf_path: str) -> dict:
    """
    Extract text page by page.
    """

    try:

        pages = {}

        with pdfplumber.open(pdf_path) as pdf:

            for i, page in enumerate(pdf.pages):

                pages[f"Page {i+1}"] = page.extract_text()

        return pages

    except Exception as e:

        return {"error": str(e)}


# ==========================================================
# Extract Images
# ==========================================================

@tool
def extract_images(pdf_path: str,
                   output_folder: str = "images") -> list:
    """
    Extract all images from PDF.
    """

    try:

        os.makedirs(output_folder, exist_ok=True)

        doc = fitz.open(pdf_path)

        image_paths = []

        for page_number in range(len(doc)):

            page = doc.load_page(page_number)

            images = page.get_images(full=True)

            for index, img in enumerate(images):

                xref = img[0]

                base = doc.extract_image(xref)

                image_bytes = base["image"]

                ext = base["ext"]

                filename = f"page_{page_number+1}_{index}.{ext}"

                filepath = os.path.join(output_folder, filename)

                with open(filepath, "wb") as f:

                    f.write(image_bytes)

                image_paths.append(filepath)

        return image_paths

    except Exception as e:

        return [str(e)]


# ==========================================================
# Extract Metadata
# ==========================================================

@tool
def extract_metadata(pdf_path: str) -> dict:
    """
    Extract PDF metadata.
    """

    try:

        doc = fitz.open(pdf_path)

        metadata = doc.metadata

        metadata["pages"] = len(doc)

        return metadata

    except Exception as e:

        return {"error": str(e)}


# ==========================================================
# Extract Tables
# ==========================================================

@tool
def extract_tables(pdf_path: str) -> list:
    """
    Extract tables from PDF.
    """

    tables = []

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages):

                page_tables = page.extract_tables()

                for table in page_tables:

                    tables.append({
                        "page": page_number + 1,
                        "table": table
                    })

        return tables

    except Exception as e:

        return [{"error": str(e)}]


# ==========================================================
# Read Image Information
# ==========================================================

@tool
def image_details(image_path: str) -> dict:
    """
    Returns image size and format.
    """

    try:

        image = Image.open(image_path)

        return {
            "width": image.width,
            "height": image.height,
            "format": image.format
        }

    except Exception as e:

        return {"error": str(e)}


# ==========================================================
# Search Observation
# ==========================================================

@tool
def search_keyword(text: str,
                   keyword: str) -> str:
    """
    Search a keyword inside extracted text.
    """

    result = []

    for line in text.split("\n"):

        if keyword.lower() in line.lower():

            result.append(line)

    return "\n".join(result)


# ==========================================================
# Count Pages
# ==========================================================

@tool
def page_count(pdf_path: str) -> int:
    """
    Count total pages in PDF.
    """

    try:

        doc = fitz.open(pdf_path)

        return len(doc)

    except Exception:

        return -1


# ==========================================================
# Save Report
# ==========================================================

@tool
def save_report(report: str,
                filename: str = "DDR_Report.md") -> str:
    """
    Save generated report.
    """

    with open(filename, "w", encoding="utf-8") as f:

        f.write(report)

    return filename
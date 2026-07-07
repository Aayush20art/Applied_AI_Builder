# 🏠 AI-Powered Detailed Diagnostic Report (DDR) Generator

An AI-powered multi-agent system that automatically generates a **Detailed Diagnostic Report (DDR)** from an **Inspection Report** and a **Thermal Report**.

The system extracts observations, thermal findings, metadata, and images from both documents, intelligently merges the information, identifies probable root causes, assesses severity, recommends actions, and generates a structured client-ready DDR.

---

## 🚀 Live Demo

👉 **Live Application**

**:contentReference[oaicite:0]{index=0}**

---

# ✨ Features

- 📄 Upload Inspection Report PDF
- 🌡 Upload Thermal Report PDF
- 🤖 Multi-Agent AI Workflow
- 🖼 Automatic Image Extraction
- 📊 Metadata Extraction
- 📝 Area-wise Observation Extraction
- 🔍 Root Cause Analysis
- ⚠ Severity Assessment
- 💡 Recommendation Generation
- 📋 Professional DDR Generation
- ✅ Quality Review Agent
- 📥 Download Final Report

---

# 🧠 Multi-Agent Architecture

The application is designed using specialized AI agents, where every agent performs a single responsibility.

```
                    User Uploads
                           │
          ┌────────────────┴───────────────┐
          │                                │
Inspection Report                  Thermal Report
          │                                │
          ▼                                ▼
   Inspection Agent                Thermal Agent
          │                                │
          └──────────────┬─────────────────┘
                         ▼
               Image Extraction Agent
                         │
                         ▼
                 Metadata Agent
                         │
                         ▼
                 Merge Agent
                         │
                         ▼
              Root Cause Agent
                         │
                         ▼
             Severity Assessment Agent
                         │
                         ▼
            Recommendation Agent
                         │
                         ▼
                 DDR Writer Agent
                         │
                         ▼
                 Quality Review Agent
                         │
                         ▼
                  Final DDR Report
```

---

# 📂 Project Structure

```
AI-DDR-Generator/

│
├── app.py
├── pipeline.py
├── agents.py
├── tools.py
├── requirements.txt
│
├── images/
│
├── sample_reports/
│     ├── Inspection_Report.pdf
│     ├── Thermal_Report.pdf
│     └── Sample_DDR.pdf
│
└── README.md
```

---

# ⚙ Technologies Used

- Python
- Streamlit
- LangChain
- Mistral AI
- PyMuPDF
- pdfplumber
- Pillow
- Pydantic

---

# 🤖 AI Workflow

## 1. Inspection Agent

Extracts

- Property observations
- Defects
- Impacted areas
- Visual findings

---

## 2. Thermal Agent

Extracts

- Thermal anomalies
- Hotspots
- Coldspots
- Moisture indications

---

## 3. Image Extraction Agent

Extracts

- Inspection images
- Thermal images

---

## 4. Metadata Agent

Extracts

- PDF metadata
- Tables
- Page information

---

## 5. Merge Agent

Combines

- Inspection observations
- Thermal findings

Removes duplicate information.

---

## 6. Root Cause Agent

Determines the most probable reason behind observed defects using both reports.

---

## 7. Severity Agent

Classifies every issue into

- Low
- Medium
- High
- Critical

with reasoning.

---

## 8. Recommendation Agent

Suggests suitable corrective actions based on the identified issues.

---

## 9. DDR Writer Agent

Generates the final structured report containing

- Property Issue Summary
- Area-wise Observations
- Root Cause
- Severity
- Recommendations
- Additional Notes
- Missing Information

---

## 10. Review Agent

Performs final quality validation by checking

- Missing sections
- Duplicate observations
- Hallucinations
- Conflicting information
- Missing images

---

# 📄 Generated DDR Structure

The generated report contains:

- Property Issue Summary
- Area-wise Observations
- Probable Root Cause
- Severity Assessment
- Recommended Actions
- Additional Notes
- Missing or Unclear Information

---

# 📷 Image Handling

The application automatically extracts images from both reports and associates them with relevant observations.

If an expected image is unavailable, the report explicitly mentions:

```
Image Not Available
```

---

# ▶ Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd AI-DDR-Generator
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create

```
.streamlit/secrets.toml
```

Add

```toml
MISTRAL_API_KEY="YOUR_API_KEY"
```

---

# ▶ Run

```bash
streamlit run app.py
```

---

# 📌 Sample Input

- Inspection Report (PDF)
- Thermal Report (PDF)

---

# 📌 Output

A structured **Detailed Diagnostic Report (DDR)** containing

- Client-ready observations
- Thermal evidence
- Severity analysis
- Root cause
- Recommended actions

---

# 🎯 Assignment Objectives Covered

- ✅ Information Extraction
- ✅ Multi-document Reasoning
- ✅ Multi-Agent AI Workflow
- ✅ Image Extraction
- ✅ Conflict Handling
- ✅ Missing Information Handling
- ✅ Structured Report Generation
- ✅ Reliable AI Pipeline

---

# 📈 Future Improvements

- LangGraph State Management
- Vision-Language Models for Image Reasoning
- OCR Support for Scanned PDFs
- Automatic PDF DDR Export
- Interactive Report Editing
- Confidence Scores for AI Predictions
- Human-in-the-loop Validation

---

# 👨‍💻 Author

**Aayush Sharma**

AI/ML Engineer | Generative AI | LangChain | Streamlit | Multi-Agent Systems

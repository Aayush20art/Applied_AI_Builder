import streamlit as st
import os

# ==========================================================
# API Key
# ==========================================================

os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

# ==========================================================
# Imports
# ==========================================================

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import (
    extract_text,
    extract_page_text,
    extract_images,
    extract_tables,
    extract_metadata,
    search_keyword,
    save_report,
)

# ==========================================================
# LLM
# ==========================================================

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

# ==========================================================
# 1. Inspection Agent
# ==========================================================

def build_inspection_agent():

    return create_agent(
        model=llm,
        tools=[
            extract_text,
            extract_page_text,
            search_keyword,
        ]
    )

# ==========================================================
# 2. Thermal Agent
# ==========================================================

def build_thermal_agent():

    return create_agent(
        model=llm,
        tools=[
            extract_text,
            extract_page_text,
            search_keyword,
        ]
    )

# ==========================================================
# 3. Image Extraction Agent
# ==========================================================

def build_image_agent():

    return create_agent(
        model=llm,
        tools=[
            extract_images
        ]
    )

# ==========================================================
# 4. Metadata Agent
# ==========================================================

def build_metadata_agent():

    return create_agent(
        model=llm,
        tools=[
            extract_metadata,
            extract_tables
        ]
    )

# ==========================================================
# Merge Agent
# ==========================================================

merge_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
You are an expert building inspection analyst.

Merge information extracted from

Inspection Report

Thermal Report

Rules:

Remove duplicate observations.

Combine related findings.

Maintain area-wise structure.

Do NOT invent facts.

Mention conflicts if any.

Mention Not Available whenever information is missing.

Output JSON only.
"""
),

(
"human",
"""
Inspection Findings

{inspection}

Thermal Findings

{thermal}
"""
)

]
)

merge_chain = merge_prompt | llm | StrOutputParser()

# ==========================================================
# Root Cause Agent
# ==========================================================

root_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
You are a senior structural engineer.

Based ONLY on the provided observations,
identify the most probable root cause.

Never hallucinate.

If insufficient evidence exists,
write

Not Available
"""
),

(
"human",
"""
Observations

{observations}
"""
)

]
)

root_chain = root_prompt | llm | StrOutputParser()

# ==========================================================
# Severity Agent
# ==========================================================

severity_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
Assess issue severity.

Possible values

Low

Medium

High

Critical

Always provide reasoning.

Never guess.
"""
),

(
"human",
"""
Observations

{observations}
"""
)

]
)

severity_chain = severity_prompt | llm | StrOutputParser()

# ==========================================================
# Recommendation Agent
# ==========================================================

recommendation_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
Suggest client-friendly recommendations.

Recommendations must directly relate
to observations.

Do not invent treatments.

Mention Not Available if necessary.
"""
),

(
"human",
"""
Observations

{observations}

Root Cause

{root_cause}
"""
)

]
)

recommendation_chain = recommendation_prompt | llm | StrOutputParser()

# ==========================================================
# DDR Writer Agent
# ==========================================================

writer_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
You are an expert report writer.

Generate a professional DDR.

The report MUST contain

1 Property Issue Summary

2 Area-wise Observations

3 Probable Root Cause

4 Severity Assessment

5 Recommended Actions

6 Additional Notes

7 Missing or Unclear Information

Never invent facts.

Mention conflicts.

Mention Not Available whenever required.

Use simple language.
"""
),

(
"human",
"""
Merged Findings

{merged}

Root Cause

{root}

Severity

{severity}

Recommendations

{recommendations}
"""
)

]
)

writer_chain = writer_prompt | llm | StrOutputParser()

# ==========================================================
# Review Agent
# ==========================================================

review_prompt = ChatPromptTemplate.from_messages(

[
(
"system",
"""
You are a quality reviewer.

Check

Missing sections

Duplicate observations

Conflicting information

Hallucinations

Missing images

Return

Pass

or

List corrections.
"""
),

(
"human",
"""
DDR Report

{report}
"""
)

]
)

review_chain = review_prompt | llm | StrOutputParser()
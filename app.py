import os
import streamlit as st
from google import genai
import re

# Initialize the Gemini client securely
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- USER INTERFACE ---
st.title("AP Calculus BC AI Study Aid")

# Layout for selections
col1, col2 = st.columns(2)
with col1:
    unit = st.selectbox("Select Unit", [
        "Unit 1: Limits and Continuity",
        "Unit 2: Differentiation: Definition and Fundamental Properties",
        "Unit 3: Differentiation: Composite, Implicit, and Inverse Functions",
        "Unit 4: Contextual Applications of Differentiation",
        "Unit 5: Analytical Applications of Differentiation",
        "Unit 6: Integration and Accumulation of Change",
        "Unit 7: Differential Equations",
        "Unit 8: Applications of Integration",
        "Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
        "Unit 10: Infinite Sequences and Series"
    ])
with col2:
    topic = st.text_input("Enter a specific topic (e.g., Taylor Polynomials)")

# --- STATE MANAGEMENT ---
if "questions" not in st.session_state:
    st.session_state.questions = None
if "feedback" not in st.session_state:
    st.session_state.feedback = {"Easy": None, "Medium": None, "Hard": None}

# --- GENERATE QUESTIONS ---
if st.button("Generate Questions"):
    if topic:
        with st.spinner("Generating Easy, Medium, and Hard questions..."):
            prompt = f"""You are an AP Calculus BC teacher. Generate three separate multiple-choice questions on {unit}, specifically focusing on {topic}. 
            
            The three questions must have distinctly different difficulty levels: one Easy, one Medium, and one Hard.
            Format all mathematical expressions using standard inline LaTeX (wrapped in single dollar signs like $f(x) = x^2$).
            
            For each question, provide the question text and options labeled A, B, C, and D. Do NOT provide the correct answers or explanations yet.
            
            Label each section clearly with [EASY], [MEDIUM], and [HARD]."""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            raw_text = response.text
            
            # Robust parsing using Regular Expressions (ignores markdown, case, and extra spacing)
            easy_match = re.search(r'(?:\[?EASY\]?)(.*?)(?=\[?MEDIUM\]?|\[?HARD\]?|$)', raw_text, re.DOTALL | re.IGNORECASE)
            medium_match = re.search(r'(?:\[?MEDIUM\]?)(.*?)(?=\[?HARD\]?|$)', raw_text, re.DOTALL | re.IGNORECASE)
            hard_match = re.search(r'(?:\[?HARD\]?)(.*?)(?=$)', raw_text, re.DOTALL | re.IGNORECASE)
            
            st.session_state.questions = {
                "Easy": easy_match.group(1).strip() if easy_match else "Could not parse Easy question. Try again.",
                "Medium": medium_match.group(1).strip() if medium_match else "Could not parse Medium question. Try again.",
                "Hard": hard_match.group(1).strip() if hard_match else "Could not parse Hard question. Try again."
            }
            
            # Clear previous feedback on a new generation
            st.session_state.feedback = {"Easy": None, "Medium": None, "Hard": None}
    else:
        st.warning("Please enter a topic first.")

# --- DISPLAY QUESTIONS IN TABS ---
if st.session_state.questions:
    st.divider()
    
    # Create three visual tabs for the difficulties
    tab_easy, tab_medium, tab_hard = st.tabs(["🟢 Easy", "🟡 Medium", "🔴 Hard"])
    
    for diff, tab in [("Easy", tab_easy), ("Medium", tab_medium), ("Hard", tab_hard)]:
        with tab:
            st.subheader(f"{diff} Level Challenge")
            st.write(st.session_state.questions[diff])
            
            # Unique keys per tab prevent input cross-talk
            user_ans = st.text_input(f"Your Answer for {diff} (A, B, C, or D):", key=f"input_{diff}").upper()
            
            if st.button(f"Submit {diff} Answer", key=f"btn_{diff}"):
                if user_ans:
                    with st.spinner("Grading..."):
                        check_prompt = f"""The user answered {user_ans} to the following {diff} level AP Calculus BC question:
                        {st.session_state.questions[diff]}
                        
                        1. State whether the user is CORRECT or INCORRECT.
                        2. Explain the step-by-step mathematical reasoning using LaTeX formatting for formulas."""
                        
                        explanation = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=check_prompt
                        )
                        st.session_state.feedback[diff] = explanation.text
                else:
                    st.warning("Please enter an answer letter first.")
            
            # Keep feedback visible inside the respective tab
            if st.session_state.feedback[diff]:
                st.divider()
                st.subheader(f"{diff} Feedback")
                st.write(st.session_state.feedback[diff])

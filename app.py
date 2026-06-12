import streamlit as st
from openai import OpenAI

# Initialize the AI client securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- USER INTERFACE ---
st.title("AP Calculus BC AI Study Aid")

# Layout for selections
col1, col2 = st.columns(2)
with col1:
    unit = st.selectbox("Select Unit", [
        "Unit 8: Applications of Integration",
        "Unit 9: Parametric, Polar, and Vectors",
        "Unit 10: Infinite Sequences and Series"
    ])
with col2:
    topic = st.text_input("Enter a specific topic (e.g., Taylor Polynomials)")

# --- STATE MANAGEMENT ---
# Streamlit reruns the script on every interaction, so we store the question in session_state
if "question" not in st.session_state:
    st.session_state.question = None

# --- GENERATE QUESTION ---
if st.button("Generate Question"):
    if topic:
        with st.spinner("Generating question..."):
            prompt = f"""You are an AP Calculus BC teacher. Generate a single, challenging multiple-choice question on {unit}, specifically focusing on {topic}. 
            Provide the question and options labeled A, B, C, and D. 
            Do NOT provide the correct answer or explanation yet."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.question = response.choices[0].message.content
    else:
        st.warning("Please enter a topic first.")

# --- DISPLAY QUESTION & CHECK ANSWER ---
if st.session_state.question:
    st.divider()
    st.subheader("Your Question")
    st.write(st.session_state.question)
    
    user_answer = st.text_input("Enter your answer (A, B, C, or D):").upper()
    
    if st.button("Submit Answer"):
        if user_answer:
            with st.spinner("Grading..."):
                check_prompt = f"""The user answered {user_answer} to the following question:
                {st.session_state.question}
                
                1. State whether the user is CORRECT or INCORRECT.
                2. Explain the mathematical steps and reasoning to arrive at the correct answer."""
                
                explanation = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": check_prompt}]
                )
                st.subheader("Feedback & Explanation")
                st.write(explanation.choices[0].message.content)
        else:
            st.warning("Please enter an answer before submitting.")
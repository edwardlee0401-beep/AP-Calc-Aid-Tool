import os
import streamlit as st
from google import genai

# =====================================================================
# 1. API KEY & CLIENT SETUP
# =====================================================================
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("⚠️ API Key not found. Please set GEMINI_API_KEY in your environment variables or secrets.toml.")
    st.stop()

client = genai.Client(api_key=api_key)

# =====================================================================
# 2. CURRICULUM DATA DIRECTORY
# =====================================================================
CURRICULUM = {
    "Pre-algebra (Khan Academy)": {
        "Unit 1: Factors and multiples": ["Prime Factorization", "Greatest Common Factor (GCF)", "Least Common Multiple (LCM)"],
        "Unit 2: Patterns": ["Identifying Number Patterns", "Visual Patterns", "Pattern Rules"],
        "Unit 3: Ratios and rates": ["Introduction to Ratios", "Equivalent Ratios", "Unit Rates and Prices"],
        "Unit 4: Percentages": ["Introduction to Percents", "Percent of a Number", "Finding the Total from a Percent"],
        "Unit 5: Exponents intro and order of operations": ["Introduction to Exponents", "Order of Operations (PEMDAS)", "Evaluating Expressions with Exponents"],
        "Unit 6: Variables & expressions": ["Parts of Algebraic Expressions", "Evaluating Algebraic Expressions", "Writing Basic Algebraic Expressions"],
        "Unit 7: Equations & inequalities introduction": ["Testing Solutions to Equations", "One-Step Addition & Subtraction Equations", "Introduction to Inequalities"],
        "Unit 8: Percent & rational number word problems": ["Discount, Tax, and Tip Word Problems", "Markup and Commission", "Rational Number Word Problems"],
        "Unit 9: Proportional relationships": ["Identifying Proportional Relationships", "Constant of Proportionality", "Graphs of Proportional Relationships"],
        "Unit 10: One-step and two-step equations & inequalities": ["Solving Two-Step Equations", "Two-Step Equation Word Problems", "Solving and Graphing Two-Step Inequalities"],
        "Unit 11: Roots, exponents, & scientific notation": ["Square Roots and Cube Roots", "Properties of Exponents", "Scientific Notation Introduction"],
        "Unit 12: Multi-step equations": ["Equations with the Distributive Property", "Combining Like Terms to Solve Equations", "Equations with Variables on Both Sides"],
        "Unit 13: Two-variable equations": ["Solutions to Two-Variable Equations", "Completing Table of Values", "Graphing Two-Variable Equations"],
        "Unit 14: Functions and linear models": ["Introduction to Functions", "Linear vs. Nonlinear Functions", "Interpreting Linear Models"],
        "Unit 15: Systems of equations": ["Introduction to Systems of Equations", "Solving Systems by Graphing", "Determining the Number of Solutions"]
    },
    "Algebra 1 (Khan Academy)": {
        "Unit 1: Algebra foundations": ["Overview of Real Numbers", "Combining Like Terms", "The Distributive Property"],
        "Unit 2: Solving equations & inequalities": ["Linear Equations with Variables on Both Sides", "Linear Equations with No Solution or Infinitely Many Solutions", "Compound Inequalities"],
        "Unit 3: Working with units": ["Unit Conversion and Dimensional Analysis", "Word Problems with Multiple Units", "Scale and Accuracy"],
        "Unit 4: Linear equations & graphs": ["Slope of a Line", "Graphing in Slope-Intercept Form", "Horizontal and Vertical Lines"],
        "Unit 5: Forms of linear equations": ["Slope-Intercept Form", "Point-Slope Form", "Standard Form of Linear Equations"],
        "Unit 6: Systems of equations": ["Solving Systems by Substitution", "Solving Systems by Elimination", "Systems of Equations Word Problems"],
        "Unit 7: Inequalities (systems & graphs)": ["Graphing Two-Variable Linear Inequalities", "Systems of Linear Inequalities", "Word Problems with Systems of Inequalities"],
        "Unit 8: Functions": ["Evaluating Functions", "Domain and Range of Functions", "Features of Function Graphs"],
        "Unit 9: Sequences": ["Arithmetic Sequences", "Geometric Sequences", "Recursive vs. Explicit Formulas"],
        "Unit 10: Absolute value & piecewise functions": ["Solving Absolute Value Equations", "Graphing Absolute Value Functions", "Evaluating Piecewise Functions"],
        "Unit 11: Exponents & radicals": ["Exponent Properties Review", "Simplifying Square Roots", "Rational Exponents"],
        "Unit 12: Exponential growth & decay": ["Introduction to Exponential Functions", "Exponential Growth vs. Decay", "Exponential Word Problems"],
        "Unit 13: Quadratics: Multiplying & factoring": ["Multiplying Binomials", "Factoring Quadratics with Leading Coefficient 1", "Factoring by Grouping and Special Products"],
        "Unit 14: Quadratic functions & equations": ["Solving Quadratics by Factoring", "The Quadratic Formula", "Vertex Form and Graphing Parabolas"],
        "Unit 15: Irrational numbers": ["Rational vs. Irrational Numbers", "Approximating Irrational Numbers", "Properties of Rational and Irrational Numbers"]
    },
    "Geometry (Khan Academy)": {
        "Unit 1: Performing transformations": ["Translations", "Rotations", "Reflections"],
        "Unit 2: Transformation properties and proofs": ["Rigid Transformations and Congruence", "Symmetry", "Geometric Definitions"],
        "Unit 3: Congruence": ["Triangle Congruence (SSS, SAS, ASA, AAS)", "Congruence Proofs", "Properties of Isosceles and Equilateral Triangles"],
        "Unit 4: Similarity": ["Dilations", "Triangle Similarity Criteria (AA, SSS, SAS)", "Solving Problems with Similar Triangles"],
        "Unit 5: Right triangles & trigonometry": ["Pythagorean Theorem", "Special Right Triangles", "Trigonometric Ratios (Sine, Cosine, Tangent)"],
        "Unit 6: Analytic geometry": ["Distance and Midpoint Formulas", "Parallel and Perpendicular Lines on the Coordinate Plane", "Equations of Circles"],
        "Unit 7: Conic sections": ["Introduction to Conic Sections", "Parabolas in Geometric Form", "Focus and Directrix"],
        "Unit 8: Circles": ["Arc Length and Sector Area", "Inscribed Angles", "Properties of Tangents and Chords"],
        "Unit 9: Solid geometry": ["Volume of Prisms and Cylinders", "Volume of Pyramids and Cones", "Surface Area and Volume of Spheres"]
    },
    "Algebra 2 (Khan Academy)": {
        "Unit 1: Polynomial arithmetic": ["Adding and Subtracting Polynomials", "Multiplying Polynomials", "Binomial Theorem and Pascal's Triangle"],
        "Unit 2: Complex numbers": ["The Imaginary Unit i", "Adding and Subtracting Complex Numbers", "Multiplying and Dividing Complex Numbers"],
        "Unit 3: Polynomial factorization": ["Factoring Higher-Degree Polynomials", "Factoring Sum and Difference of Cubes", "The Remainder and Factor Theorems"],
        "Unit 4: Polynomial division": ["Polynomial Long Division", "Synthetic Division", "Dividing Polynomials by Linear Binomials"],
        "Unit 5: Polynomial graphs": ["End Behavior of Polynomial Functions", "Zeros and Multiplicity", "Sketching Graphs of Polynomials"],
        "Unit 6: Rational exponents and radicals": ["Simplifying Radical Expressions", "Solving Radical Equations", "Extraneous Solutions"],
        "Unit 7: Exponential models": ["Constructing Exponential Models", "Continuous Compound Interest (e)", "Exponential Regression Concepts"],
        "Unit 8: Logarithms": ["Introduction to Logarithms", "Properties of Logarithms", "Solving Exponential and Logarithmic Equations"],
        "Unit 9: Transformations of functions": ["Shifting Functions Horizontally and Vertically", "Reflecting and Scaling Functions", "Combining Function Transformations"],
        "Unit 10: Equations": ["Solving Rational Equations", "Solving Advanced Systems of Equations", "Graphing and Solving Non-Linear Equations"],
        "Unit 11: Trigonometry": ["The Unit Circle", "Radian Measure and Circular Functions", "Graphing Sine and Cosine Functions"],
        "Unit 12: Modeling": ["Fitting Linear and Exponential Models to Data", "Sinusoidal Models", "Analyzing Function Models in Context"]
    },
    "AP Precalculus (College Board)": {
        "Unit 1: Polynomial and Rational Functions": ["Change in Tandem and Rates of Change", "Polynomial Functions and End Behavior", "Rational Functions and Asymptotes", "Polynomial and Rational Inequalities"],
        "Unit 2: Exponential and Logarithmic Functions": ["Arithmetic and Geometric Sequences", "Exponential Functions and Modeling", "Logarithmic Expressions and Functions", "Logarithmic Scales and Equations"],
        "Unit 3: Trigonometric and Polar Functions": ["Periodic Phenomena and Sine/Cosine Functions", "The Unit Circle and Radian Measure", "Trigonometric Identities and Equations", "Polar Coordinates and Polar Function Graphs"],
        "Unit 4: Functions Involving Parameters, Vectors, and Matrices": ["Parametric Functions and Modeling", "Vectors in Two Dimensions", "Matrix Operations and Transformations", "Implicit Functions and Conic Sections"]
    },
    "AP Calculus AB/BC (College Board)": {
        "Unit 1: Limits and Continuity": ["Evaluating Limits Analytically", "The Squeeze Theorem", "Types of Discontinuities", "Intermediate Value Theorem"],
        "Unit 2: Differentiation: Definition and Basic Rules": ["Average vs. Instantaneous Rate of Change", "Power Rule, Product Rule, and Quotient Rule", "Derivatives of Trigonometric Functions"],
        "Unit 3: Differentiation: Composite, Implicit, and Inverse": ["The Chain Rule", "Implicit Differentiation", "Derivatives of Inverse Trigonometric Functions"],
        "Unit 4: Contextual Applications of Differentiation": ["Related Rates", "Linear Approximation and Differentials", "L'Hôpital's Rule"],
        "Unit 5: Analytical Applications of Differentiation": ["Mean Value Theorem", "Increasing/Decreasing Intervals and First Derivative Test", "Concavity and Second Derivative Test", "Optimization Problems"],
        "Unit 6: Integration and Accumulation of Change": ["Riemann Sums and Definite Integrals", "Fundamental Theorem of Calculus", "Integration by Substitution (u-sub)", "Integration by Parts (BC Only)"],
        "Unit 7: Differential Equations": ["Modeling Situations with Differential Equations", "Slope Fields", "Separable Differential Equations", "Euler's Method (BC Only)"],
        "Unit 8: Applications of Integration": ["Area Between Two Curves", "Volume by Disk and Washer Methods", "Volume by Cross Sections", "Arc Length (BC Only)"],
        "Unit 9: Parametric Equations, Polar Coordinates, and Vectors (BC Only)": ["Derivatives and Integrals of Parametric Equations", "Arc Length of Parametric Curves", "Vector-Valued Functions and Motion", "Area and Arc Length in Polar Coordinates"],
        "Unit 10: Infinite Sequences and Series (BC Only)": ["Convergence Tests (Ratio, Root, Integral, Comparison)", "Power Series and Radius of Convergence", "Taylor and Maclaurin Series", "Lagrange Error Bound"]
    }
}

# =====================================================================
# 3. SESSION STATE INITIALIZATION
# =====================================================================
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "question_type" not in st.session_state:
    st.session_state["question_type"] = "MCQ"

# =====================================================================
# 4. LOGIN SCREEN GATEKEEPER
# =====================================================================
if st.session_state["user_email"] is None:
    st.title("Welcome to the AI Math Study Portal 🎓")
    st.write("Please sign in with your email to access your personalized study session.")
    
    with st.form("login_form"):
        email_input = st.text_input("Email Address", placeholder="student@example.com")
        submit_login = st.form_submit_button("Sign In")
        
        if submit_login:
            if "@" in email_input and "." in email_input:
                st.session_state["user_email"] = email_input
                st.rerun()
            else:
                st.error("Please enter a valid email address.")
    st.stop()

# =====================================================================
# 5. MAIN NAVIGATION & HEADER
# =====================================================================
st.sidebar.write(f"👤 **Logged in as:** `{st.session_state['user_email']}`")
if st.sidebar.button("Log Out"):
    st.session_state["user_email"] = None
    st.session_state["current_question"] = None
    st.rerun()

st.title("📚 Interactive Math Study Center")
st.write("Select your curriculum, course, and topic to generate practice problems aligned with official standards.")

# =====================================================================
# 6. CASCADING CURRICULUM SELECTION
# =====================================================================
col1, col2, col3 = st.columns(3)

with col1:
    selected_course = st.selectbox("1. Select Course", list(CURRICULUM.keys()))

with col2:
    available_units = list(CURRICULUM[selected_course].keys())
    selected_unit = st.selectbox("2. Select Unit", available_units)

with col3:
    available_topics = CURRICULUM[selected_course][selected_unit]
    selected_topic = st.selectbox("3. Select Topic", available_topics)

is_ap_course = "AP" in selected_course
if is_ap_course:
    q_type = st.radio("Select Question Format:", ["Multiple Choice (MCQ)", "Free Response Question (FRQ)"], horizontal=True)
    st.session_state["question_type"] = "FRQ" if "FRQ" in q_type else "MCQ"
else:
    st.session_state["question_type"] = "MCQ"

# =====================================================================
# 7. QUESTION GENERATION LOGIC
# =====================================================================
if st.button("🚀 Generate Practice Problem", type="primary"):
    with st.spinner(f"Generating a high-quality {st.session_state['question_type']} problem for {selected_topic}..."):
        
        if st.session_state["question_type"] == "MCQ":
            prompt = f"""
            Create a standard {selected_course} Multiple Choice Question on the topic: '{selected_topic}' (Unit: {selected_unit}).
            The difficulty and style MUST strictly follow the { 'College Board AP Exam' if is_ap_course else 'Khan Academy' } curriculum standards.
            
            Format your response EXACTLY like this with no extra introductory text:
            QUESTION: [Write the question here using proper LaTeX for math equations]
            OPTION_A: [First option]
            OPTION_B: [Second option]
            OPTION_C: [Third option]
            OPTION_D: [Fourth option]
            CORRECT: [Just the letter A, B, C, or D]
            EXPLANATION: [Detailed, step-by-step LaTeX solution]
            """
        else:
            prompt = f"""
            Create an authentic College Board AP Exam style Free Response Question (FRQ) for {selected_course} on the topic: '{selected_topic}' (Unit: {selected_unit}).
            It should be a rigorous multi-part question (parts a, b, c) requiring complete algebraic and analytical justification.
            
            Format your response EXACTLY like this:
            QUESTION: [Write the full multi-part FRQ prompt here using proper LaTeX]
            RUBRIC: [Write out the official College Board style grading rubric. Detail exactly how points are awarded for each part, e.g., 'Part (a): 2 points (1 point for correct integral setup, 1 point for antiderivative and evaluation).']
            EXPLANATION: [Complete step-by-step model solution for all parts]
            """
            
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        st.session_state["current_question"] = response.text

# =====================================================================
# 8. DISPLAY QUESTION & INTERACTION LOGIC
# =====================================================================
if st.session_state["current_question"]:
    raw_text = st.session_state["current_question"]
    st.divider()
    
    if st.session_state["question_type"] == "MCQ":
        try:
            q_part = raw_text.split("QUESTION:")[1].split("OPTION_A:")[0].strip()
            opt_a = raw_text.split("OPTION_A:")[1].split("OPTION_B:")[0].strip()
            opt_b = raw_text.split("OPTION_B:")[1].split("OPTION_C:")[0].strip()
            opt_c = raw_text.split("OPTION_C:")[1].split("OPTION_D:")[0].strip()
            opt_d = raw_text.split("OPTION_D:")[1].split("CORRECT:")[0].strip()
            correct_ans = raw_text.split("CORRECT:")[1].split("EXPLANATION:")[0].strip()
            explanation = raw_text.split("EXPLANATION:")[1].strip()
            
            st.subheader("Practice Question")
            st.markdown(q_part)
            
            user_choice = st.radio(
                "Choose your answer:",
                options=[f"A)  {opt_a}", f"B)  {opt_b}", f"C)  {opt_c}", f"D)  {opt_d}"],
                index=None
            )
            
            if st.button("Check Answer"):
                if user_choice is None:
                    st.warning("Please select an option before checking!")
                else:
                    selected_letter = user_choice[0]
                    if selected_letter == correct_ans:
                        st.success(f"🎉 Correct! The answer is **{correct_ans}**.")
                    else:
                        st.error(f"❌ Incorrect. You chose **{selected_letter}**, but the correct answer is **{correct_ans}**.")
                    
                    with st.expander("📖 View Step-by-Step Explanation", expanded=True):
                        st.markdown(explanation)
        except Exception:
            st.error("There was a formatting error while parsing the generated multiple-choice options. Please click 'Generate' again.")
            st.write(raw_text)
            
    else:
        try:
            q_part = raw_text.split("QUESTION:")[1].split("RUBRIC:")[0].strip()
            rubric_part = raw_text.split("RUBRIC:")[1].split("EXPLANATION:")[0].strip()
            explanation_part = raw_text.split("EXPLANATION:")[1].strip()
            
            st.subheader("📝 Free Response Question (FRQ)")
            st.info("💡 **AP Exam Tip:** Be sure to show all mathematical setups, explicitly state any theorems used (e.g., MVT, IVT), and include proper units if applicable.")
            st.markdown(q_part)
            
            user_frq_answer = st.text_area(
                "Type your full step-by-step solution below:",
                height=220,
                placeholder="Part (a): To find the rate of change, differentiate...\nPart (b): Using the Mean Value Theorem..."
            )
            
            if st.button("Submit for AP Reader Grading"):
                if not user_frq_answer.strip():
                    st.warning("Please write out your solution before submitting!")
                else:
                    with st.spinner("An AI 'AP Reader' is evaluating your submission against the official College Board rubric..."):
                        grading_prompt = f"""
                        Act as an official College Board AP Exam Reader. Grade the student's Free Response submission based STRICTLY on the provided rubric.
                        
                        FRQ QUESTION:
                        {q_part}
                        
                        OFFICIAL RUBRIC:
                        {rubric_part}
                        
                        STUDENT SUBMISSION:
                        {user_frq_answer}
                        
                        Provide your evaluation in this exact structure:
                        1. **Total Score:** [X out of Y points]
                        2. **Point Breakdown:** Go step-by-step through the rubric and state whether the student earned or lost each specific point and explain why.
                        3. **Reader Feedback:** Constructive feedback on mathematical notation, justification completeness, and exam writing clarity.
                        """
                        
                        grade_response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=grading_prompt
                        )
                        
                        st.divider()
                        st.subheader("📋 AP Reader Score Report")
                        st.markdown(grade_response.text)
                        
                        with st.expander("🗝️ View Official College Board Rubric & Model Solution"):
                            st.markdown("### Official Rubric")
                            st.markdown(rubric_part)
                            st.markdown("### Model Solution")
                            st.markdown(explanation_part)
        except Exception:
            st.error("Could not parse the FRQ structure. Here is the raw generated problem:")
            st.markdown(raw_text)
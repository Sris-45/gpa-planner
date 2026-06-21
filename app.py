import streamlit as st
from itertools import product
import math

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="SSCBS GPA & CGPA Planner",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =====================================================================
# GLOBAL STYLES (Premium SaaS Dashboard)
# =====================================================================
st.markdown("""
<style>
/* CSS overrides to make Streamlit look like a SaaS app */
body, .stApp {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
.block-container {
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}
h1, h2, h3, h4, h5, h6 {
    color: #f0f6fc !important;
}
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.title-card {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #8b949e;
    font-size: 16px;
    margin-bottom: 24px;
    font-weight: 500;
}
.badge {
    padding: 4px 10px;
    border-radius: 20px;
    background: #1f6feb;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 8px;
}
.subtle {
    color: #8b949e;
    font-size: 14px;
}
/* Progress bar / Steps */
.step-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding: 0 10px;
}
.step {
    flex: 1;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    color: #8b949e;
    padding-bottom: 10px;
    border-bottom: 2px solid #30363d;
}
.step.active {
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
/* Override sliders and buttons */
.stButton>button {
    width: 100%;
    border-radius: 8px;
    padding: 12px 24px;
    background-color: #238636;
    color: white;
    font-weight: 600;
    border: none;
    transition: background-color 0.2s;
}
.stButton>button:hover {
    background-color: #2ea043;
    color: white;
}
.secondary-btn>button {
    background-color: #21262d;
    border: 1px solid #30363d;
    color: #c9d1d9;
}
.secondary-btn>button:hover {
    background-color: #30363d;
    border: 1px solid #8b949e;
}
/* Metric boxes */
.metric-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-title {
    font-size: 13px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #f0f6fc;
    margin-top: 8px;
}
.metric-gain {
    color: #3fb950;
    font-size: 14px;
    font-weight: 600;
    margin-top: 4px;
}
.diff-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #30363d;
}
.diff-item:last-child {
    border-bottom: none;
}
hr {
    border-color: #30363d;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# DATA CONFIGURATION
# =====================================================================
CONFIG = {
    "BMS": {
        1: {
            "Core Subjects": {
                "Fundamentals of Management": 4,
                "Financial Accounting & Analysis": 4,
                "Statistics": 4,
                "EVS": 2,
                "Basic IT Tools": 2,
            },
            "General Elective": {
                "_is_choice": True,
                "Entrepreneurship Essentials": 4,
                "Python Programming": 4,
            },
            "Additional Subject": {
                "_is_choice": True,
                "Fit India": 2,
                "Constitution": 2,
            }
        },
        2: {
            "Core Subjects": {
                "Macroeconomics": 4,
                "Introduction to Business Analytics": 4,
                "Organisational Behaviour": 4,
            },
            "General Elective": {
                "_is_choice": True,
                "Creativity & Innovation": 4,
            },
            "Professional Skill Subject": {
                "_is_choice": True,
                "Communication in Professional Life": 4,
                "Business Intelligence and Data Visualization": 4,
            },
            "Personal Development Subject": {
                "_is_choice": True,
                "Social & Emotional Learning": 2,
                "The Art of Being Happy": 2,
            },
            "Language": {
                "_is_choice": True,
                "Hindi": 2,
                "Sanskrit": 2,
                "Punjabi": 2,
                "Bengali": 2,
                "Other": 2,
            }
        }
    },
    "BBA FIA": {
        1: {
            "Core Subjects": {
                "Microeconomics": 4,
                "Financial Accounting & Analysis": 4,
                "Statistics": 4,
                "EVS": 2,
                "Basic IT Tools": 2,
            },
            "General Elective": {
                "_is_choice": True,
                "Entrepreneurship Essentials": 4,
                "Python Programming": 4,
            },
            "Additional Subject": {
                "_is_choice": True,
                "Fit India": 2,
                "Constitution": 2,
            }
        },
        2: {
            "Core Subjects": {
                "Macroeconomics": 4,
                "Introduction to Business Analytics": 4,
                "Organisational Behaviour": 4,
            },
            "General Elective": {
                "_is_choice": True,
                "Creativity & Innovation": 4,
            },
            "Professional Skill Subject": {
                "_is_choice": True,
                "Communication in Professional Life": 4,
                "Business Intelligence and Data Visualization": 4,
            },
            "Personal Development Subject": {
                "_is_choice": True,
                "Social & Emotional Learning": 2,
                "The Art of Being Happy": 2,
            },
            "Language": {
                "_is_choice": True,
                "Hindi": 2,
                "Sanskrit": 2,
                "Punjabi": 2,
                "Bengali": 2,
                "Other": 2,
            }
        }
    }
}

# =====================================================================
# STATE INITIALIZATION
# =====================================================================
if "step" not in st.session_state: st.session_state.step = 1
if "course" not in st.session_state: st.session_state.course = "BMS"
if "semester" not in st.session_state: st.session_state.semester = 1
if "subjects_sem1" not in st.session_state: st.session_state.subjects_sem1 = {}
if "subjects_sem2" not in st.session_state: st.session_state.subjects_sem2 = {}
if "gpas_sem1" not in st.session_state: st.session_state.gpas_sem1 = {}
if "gpas_sem2" not in st.session_state: st.session_state.gpas_sem2 = {}
if "locked_sem2" not in st.session_state: st.session_state.locked_sem2 = []
if "improve_sem1" not in st.session_state: st.session_state.improve_sem1 = False
if "improving_subjects" not in st.session_state: st.session_state.improving_subjects = []

# =====================================================================
# HELPER FUNCTIONS
# =====================================================================
def calculate_gpa(gpa_dict, credit_dict):
    if not credit_dict: return 0.0
    total_credits = sum(credit_dict.values())
    total_points = sum(gpa_dict.get(sub, 0) * cred for sub, cred in credit_dict.items())
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

def calculate_cgpa(gpas_1, creds_1, gpas_2, creds_2):
    total_credits = sum(creds_1.values()) + sum(creds_2.values())
    if total_credits == 0: return 0.0
    total_points = sum(gpas_1.get(sub, 0) * cred for sub, cred in creds_1.items()) + \
                   sum(gpas_2.get(sub, 0) * cred for sub, cred in creds_2.items())
    return round(total_points / total_credits, 2)

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def reset_app():
    st.session_state.step = 1
    st.session_state.gpas_sem1 = {}
    st.session_state.gpas_sem2 = {}

def my_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# =====================================================================
# UI COMPONENTS
# =====================================================================
def render_header():
    st.markdown("<div class='title-card'>SSCBS GPA & CGPA Planner</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Plan your semester strategically.<br>Discover the easiest path to improve your SGPA and overall CGPA.</div>", unsafe_allow_html=True)
    
    if st.session_state.step > 1:
        total_subjs = len(st.session_state.subjects_sem1)
        if st.session_state.semester == 2:
            total_subjs += len(st.session_state.subjects_sem2)
            
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 32px;'>
            <span class='badge' style='background:#21262d; border: 1px solid #30363d; color:#c9d1d9;'>Course: {st.session_state.course}</span>
            <span class='badge' style='background:#21262d; border: 1px solid #30363d; color:#c9d1d9;'>Semester {st.session_state.semester}</span>
        </div>
        """, unsafe_allow_html=True)

def render_steps():
    steps = ["Course", "Semester", "Academic Data", "Strategy", "Results"]
    html = "<div class='step-container'>"
    for i, s in enumerate(steps, 1):
        active = "active" if i == st.session_state.step else ""
        html += f"<div class='step {active}'>{i}. {s}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =====================================================================
# STEP 1: COURSE
# =====================================================================
if st.session_state.step == 1:
    render_header()
    render_steps()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Select Your Course</h3>", unsafe_allow_html=True)
    course = st.radio("Course", ["BMS", "BBA FIA"], index=0 if st.session_state.course == "BMS" else 1, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Next Step", use_container_width=True):
        st.session_state.course = course
        next_step()
        my_rerun()

# =====================================================================
# STEP 2: SEMESTER
# =====================================================================
elif st.session_state.step == 2:
    render_header()
    render_steps()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Select Current Semester</h3>", unsafe_allow_html=True)
    semester = st.radio("Semester", [1, 2], index=st.session_state.semester - 1, label_visibility="collapsed", format_func=lambda x: f"Semester {x}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            prev_step()
            my_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Next Step", use_container_width=True):
            st.session_state.semester = semester
            next_step()
            my_rerun()

# =====================================================================
# STEP 3: ACADEMIC DATA
# =====================================================================
elif st.session_state.step == 3:
    render_header()
    render_steps()
    
    course = st.session_state.course
    sem = st.session_state.semester
    
    subjects_sem1_dict = {}
    subjects_sem2_dict = {}
    
    # ------------------- SEMESTER 1 SECTION -------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if sem == 2:
        st.markdown("<h3 style='margin-top:0;'>SECTION A: Semester 1 Actual Results</h3>", unsafe_allow_html=True)
        st.markdown("<p class='subtle'>Load your previous semester subjects and enter the actual GPA obtained.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='margin-top:0;'>Semester 1 Current / Expected Performance</h3>", unsafe_allow_html=True)
        st.markdown("<p class='subtle'>Load your current subjects and enter your expected GPA.</p>", unsafe_allow_html=True)
        
    config_sem1 = CONFIG[course][1]
    
    for category, content in config_sem1.items():
        st.markdown(f"<div class='subtle' style='margin-top: 16px;'>{category}</div>", unsafe_allow_html=True)
        if content.get("_is_choice"):
            options = {k: v for k, v in content.items() if k != "_is_choice"}
            sel_sub = st.selectbox(f"Select {category}", list(options.keys()), key=f"s1_sel_{category}", label_visibility="collapsed")
            cred = options[sel_sub]
            subjects_sem1_dict[sel_sub] = cred
        else:
            for sub, cred in content.items():
                subjects_sem1_dict[sub] = cred
                
    st.session_state.subjects_sem1 = subjects_sem1_dict
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Render sliders for Sem 1
    for sub, cred in subjects_sem1_dict.items():
        if sub not in st.session_state.gpas_sem1:
            st.session_state.gpas_sem1[sub] = 6
        st.markdown(f"<div style='margin-top:8px;'><span class='badge'>{cred} credits</span> <strong>{sub}</strong></div>", unsafe_allow_html=True)
        st.session_state.gpas_sem1[sub] = st.slider("", 0, 10, st.session_state.gpas_sem1[sub], key=f"gpa1_{sub}")

    if sem == 2:
        current_cgpa = calculate_gpa(st.session_state.gpas_sem1, subjects_sem1_dict)
        st.success(f"**Current CGPA (Sem 1 SGPA): {current_cgpa}**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------- SEMESTER 2 SECTION -------------------
    if sem == 2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>SECTION B: Semester 2 Current / Expected Performance</h3>", unsafe_allow_html=True)
        st.markdown("<p class='subtle'>Load your Semester 2 subjects and enter your current or expected GPA.</p>", unsafe_allow_html=True)
        
        config_sem2 = CONFIG[course][2]
        
        for category, content in config_sem2.items():
            st.markdown(f"<div class='subtle' style='margin-top: 16px;'>{category}</div>", unsafe_allow_html=True)
            if content.get("_is_choice"):
                options = {k: v for k, v in content.items() if k != "_is_choice"}
                sel_sub = st.selectbox(f"Select {category}", list(options.keys()), key=f"s2_sel_{category}", label_visibility="collapsed")
                cred = options[sel_sub]
                subjects_sem2_dict[sel_sub] = cred
            else:
                for sub, cred in content.items():
                    subjects_sem2_dict[sub] = cred
                    
        st.session_state.subjects_sem2 = subjects_sem2_dict
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Render sliders for Sem 2
        for sub, cred in subjects_sem2_dict.items():
            if sub not in st.session_state.gpas_sem2:
                st.session_state.gpas_sem2[sub] = 6
            st.markdown(f"<div style='margin-top:8px;'><span class='badge'>{cred} credits</span> <strong>{sub}</strong></div>", unsafe_allow_html=True)
            st.session_state.gpas_sem2[sub] = st.slider("", 0, 10, st.session_state.gpas_sem2[sub], key=f"gpa2_{sub}")
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            prev_step()
            my_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Next Step", use_container_width=True):
            next_step()
            my_rerun()

# =====================================================================
# STEP 4: STRATEGY (LOCKS & TARGETS)
# =====================================================================
elif st.session_state.step == 4:
    render_header()
    render_steps()
    sem = st.session_state.semester
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Optimization Strategy</h3>", unsafe_allow_html=True)
    
    if sem == 2:
        st.markdown("<h5>Re-appear / Improvement Mode</h5>", unsafe_allow_html=True)
        improve = st.toggle("I plan to improve some Semester 1 subjects", value=st.session_state.improve_sem1)
        st.session_state.improve_sem1 = improve
        
        if improve:
            st.session_state.improving_subjects = st.multiselect(
                "Select Semester 1 subjects you plan to improve:",
                list(st.session_state.subjects_sem1.keys()),
                default=st.session_state.improving_subjects
            )
        else:
            st.session_state.improving_subjects = []
            
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h5>Lock Subjects</h5>", unsafe_allow_html=True)
        st.markdown("<p class='subtle'>Locked subjects will retain their current GPA in the calculation.</p>", unsafe_allow_html=True)
        st.session_state.locked_sem2 = st.multiselect(
            "Select Semester 2 subjects to lock:",
            list(st.session_state.subjects_sem2.keys()),
            default=st.session_state.locked_sem2
        )
    else:
        st.markdown("<h5>Lock Subjects</h5>", unsafe_allow_html=True)
        st.markdown("<p class='subtle'>Locked subjects will retain their current GPA in the calculation.</p>", unsafe_allow_html=True)
        st.session_state.locked_sem2 = st.multiselect(
            "Select Semester 1 subjects to lock:",
            list(st.session_state.subjects_sem1.keys()),
            default=st.session_state.locked_sem2
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Set Target</h3>", unsafe_allow_html=True)
    if sem == 2:
        target_type = st.radio("Target Metric", ["Target CGPA", "Target SGPA"], horizontal=True, index=0)
    else:
        target_type = st.radio("Target Metric", ["Target SGPA", "Target CGPA"], horizontal=True, index=0)
        
    achievable = [round(x/100, 2) for x in range(600, 1001)]
    target_val = st.select_slider("Select Target Value", options=achievable, value=achievable[200])
    st.session_state.target_type = target_type
    st.session_state.target_val = target_val
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            prev_step()
            my_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Run Optimizer", use_container_width=True):
            next_step()
            my_rerun()

# =====================================================================
# STEP 5: RESULTS DASHBOARD
# =====================================================================
elif st.session_state.step == 5:
    render_header()
    render_steps()
    
    sem = st.session_state.semester
    base_gpas1 = st.session_state.gpas_sem1
    base_gpas2 = st.session_state.gpas_sem2
    creds1 = st.session_state.subjects_sem1
    creds2 = st.session_state.subjects_sem2
    
    # Calculate Base Metrics
    base_sgpa1 = calculate_gpa(base_gpas1, creds1)
    if sem == 2:
        base_sgpa2 = calculate_gpa(base_gpas2, creds2)
        base_cgpa = calculate_cgpa(base_gpas1, creds1, base_gpas2, creds2)
    else:
        base_sgpa2 = 0.0
        base_cgpa = base_sgpa1
        
    # Optimization Engine
    modifiable = []
    ranges = []
    subject_credits = {}
    
    if sem == 2:
        for sub in st.session_state.improving_subjects:
            modifiable.append((1, sub))
            ranges.append(range(base_gpas1[sub], 11))
            subject_credits[(1, sub)] = creds1[sub]
        for sub in creds2:
            if sub not in st.session_state.locked_sem2:
                modifiable.append((2, sub))
                ranges.append(range(base_gpas2[sub], 11))
                subject_credits[(2, sub)] = creds2[sub]
    else:
        for sub in creds1:
            if sub not in st.session_state.locked_sem2:
                modifiable.append((1, sub))
                ranges.append(range(base_gpas1[sub], 11))
                subject_credits[(1, sub)] = creds1[sub]
                
    # Safeguard against too many combinations (e.g. > 10^6)
    total_combinations = math.prod(len(r) for r in ranges) if ranges else 0
    
    if total_combinations > 2000000:
        st.error(f"Too many combinations to calculate ({total_combinations:,}). Please go back and lock more subjects.")
        if st.button("Go Back"):
            prev_step()
            my_rerun()
        st.stop()
        
    results = []
    max_cgpa_achieved = 0.0
    max_sgpa_achieved = 0.0
    
    # Run optimizer combinations
    if modifiable:
        with st.spinner("Calculating optimal academic paths..."):
            for combo in product(*ranges):
                temp_gpas1 = base_gpas1.copy()
                temp_gpas2 = base_gpas2.copy()
                
                for i, (s_sem, sub) in enumerate(modifiable):
                    if s_sem == 1:
                        temp_gpas1[sub] = combo[i]
                    else:
                        temp_gpas2[sub] = combo[i]
                
                if sem == 2:
                    new_sgpa2 = calculate_gpa(temp_gpas2, creds2)
                    new_cgpa = calculate_cgpa(temp_gpas1, creds1, temp_gpas2, creds2)
                    max_cgpa_achieved = max(max_cgpa_achieved, new_cgpa)
                    max_sgpa_achieved = max(max_sgpa_achieved, new_sgpa2)
                    
                    if st.session_state.target_type == "Target CGPA" and new_cgpa >= st.session_state.target_val:
                        valid = True
                    elif st.session_state.target_type == "Target SGPA" and new_sgpa2 >= st.session_state.target_val:
                        valid = True
                    else:
                        valid = False
                else:
                    new_sgpa1 = calculate_gpa(temp_gpas1, creds1)
                    new_cgpa = new_sgpa1
                    max_cgpa_achieved = max(max_cgpa_achieved, new_cgpa)
                    max_sgpa_achieved = max(max_sgpa_achieved, new_sgpa1)
                    
                    if st.session_state.target_type == "Target CGPA" and new_cgpa >= st.session_state.target_val:
                        valid = True
                    elif st.session_state.target_type == "Target SGPA" and new_sgpa1 >= st.session_state.target_val:
                        valid = True
                    else:
                        valid = False
                        
                if valid:
                    effort = sum((combo[i] - (base_gpas1[sub] if s_sem == 1 else base_gpas2[sub])) * subject_credits[(s_sem, sub)] for i, (s_sem, sub) in enumerate(modifiable))
                    results.append({
                        "effort": effort,
                        "gpas1": temp_gpas1,
                        "gpas2": temp_gpas2,
                        "cgpa": new_cgpa,
                        "sgpa": new_sgpa2 if sem == 2 else new_sgpa1
                    })
    else:
        # No modifiable subjects
        res_cgpa = base_cgpa
        res_sgpa = base_sgpa2 if sem == 2 else base_sgpa1
        valid = False
        if st.session_state.target_type == "Target CGPA" and res_cgpa >= st.session_state.target_val:
            valid = True
        elif st.session_state.target_type == "Target SGPA" and res_sgpa >= st.session_state.target_val:
            valid = True
            
        max_cgpa_achieved = res_cgpa
        max_sgpa_achieved = res_sgpa
        
        if valid:
            results.append({
                "effort": 0,
                "gpas1": base_gpas1,
                "gpas2": base_gpas2,
                "cgpa": res_cgpa,
                "sgpa": res_sgpa
            })

    # DASHBOARD UI
    st.markdown("<h2 style='text-align:center;'>Top Summary</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-title'>Current CGPA</div>
            <div class='metric-value'>{base_cgpa}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if results:
        results.sort(key=lambda x: x["effort"])
        best = results[0]
        gain = round(best['cgpa'] - base_cgpa, 2)
        gain_str = f"+{gain}" if gain > 0 else str(gain)
        
        with c2:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>Projected CGPA</div>
                <div class='metric-value'>{best['cgpa']}</div>
                <div class='metric-gain'>Gain: {gain_str}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>Projected SGPA</div>
                <div class='metric-value'>{best['sgpa']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Recommendation Cards</h2>", unsafe_allow_html=True)
        
        # Display top 3 recommendations
        for idx, res in enumerate(results[:3]):
            card_gain = round(res['cgpa'] - base_cgpa, 2)
            card_gain_str = f"+{card_gain}" if card_gain > 0 else str(card_gain)
            
            html = f"""
            <div class='card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;'>
                    <h3 style='margin:0; color:#58a6ff;'>OPTION {idx+1}</h3>
                    <div class='badge' style='background:#238636; font-size:14px; padding:6px 14px;'>Effort Score: {res['effort']}</div>
                </div>
                
                <div style='display:flex; justify-content:space-between; margin-bottom: 24px; padding: 16px; background:#0d1117; border-radius:8px; border:1px solid #30363d;'>
                    <div style='text-align:center;'>
                        <div class='subtle'>Projected SGPA</div>
                        <div style='font-size:24px; font-weight:700; color:#f0f6fc;'>{res['sgpa']}</div>
                    </div>
                    <div style='text-align:center;'>
                        <div class='subtle'>Projected CGPA</div>
                        <div style='font-size:24px; font-weight:700; color:#f0f6fc;'>{res['cgpa']}</div>
                    </div>
                    <div style='text-align:center;'>
                        <div class='subtle'>CGPA Gain</div>
                        <div style='font-size:24px; font-weight:700; color:#3fb950;'>{card_gain_str}</div>
                    </div>
                </div>
                
                <h4 style='color:#8b949e; border-bottom:1px solid #30363d; padding-bottom:8px; margin-bottom:16px;'>Required Changes</h4>
            """
            
            changes_sem2 = []
            changes_sem1 = []
            
            if sem == 2:
                for sub in creds2:
                    if res['gpas2'][sub] > base_gpas2[sub]:
                        changes_sem2.append(f"<div class='diff-item'><span>{sub}</span> <strong>{base_gpas2[sub]} &rarr; {res['gpas2'][sub]}</strong></div>")
            
            for sub in (st.session_state.improving_subjects if sem == 2 else creds1):
                if res['gpas1'][sub] > base_gpas1[sub]:
                    changes_sem1.append(f"<div class='diff-item'><span>{sub}</span> <strong>{base_gpas1[sub]} &rarr; {res['gpas1'][sub]}</strong></div>")
            
            if sem == 2 and changes_sem2:
                html += f"<div style='margin-bottom:8px;'><span class='badge' style='background:#30363d; color:#c9d1d9;'>Semester 2</span></div>"
                html += "".join(changes_sem2)
                html += "<div style='height:16px;'></div>"
            
            if changes_sem1:
                label = "Semester 1 Improvement" if sem == 2 else "Semester 1"
                html += f"<div style='margin-bottom:8px;'><span class='badge' style='background:#30363d; color:#c9d1d9;'>{label}</span></div>"
                html += "".join(changes_sem1)
                
            if not changes_sem2 and not changes_sem1:
                html += "<div class='subtle' style='text-align:center; padding:16px;'>No changes required. Current GPA meets target.</div>"
                
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

    else:
        with c2:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>Max Possible CGPA</div>
                <div class='metric-value'>{max_cgpa_achieved}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>Max Possible SGPA</div>
                <div class='metric-value'>{max_sgpa_achieved}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        st.error(f"**Unable to reach the target metric.** The maximum achievable CGPA is {max_cgpa_achieved}.")

    st.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("Modify Strategy", use_container_width=True):
            prev_step()
            my_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Start New Plan", use_container_width=True):
            reset_app()
            my_rerun()

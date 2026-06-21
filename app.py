import streamlit as st
from itertools import product
import math

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="GPA Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================================
# GLOBAL STYLES (Premium SaaS Theme for PC)
# =====================================================================
st.markdown("""
<style>
/* Base Dark Theme Overrides */
.stApp {
    background-color: #0b0f19;
    color: #e2e8f0;
}
/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: #f7fafc !important;
    font-weight: 700 !important;
}
/* Header */
.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #63b3ed, #b794f4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    padding-top: 1rem;
}
.sub-title {
    text-align: center;
    color: #a0aec0;
    font-size: 1.125rem;
    margin-bottom: 3rem;
    font-weight: 500;
}
/* Step Indicator */
.step-indicator {
    display: flex;
    justify-content: space-between;
    margin-bottom: 3rem;
    background: #151b2b;
    padding: 1.5rem 2rem;
    border-radius: 0.75rem;
    border: 1px solid #2d3748;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.step-item {
    color: #718096;
    font-weight: 600;
    font-size: 1rem;
}
.step-item.active {
    color: #63b3ed;
    border-bottom: 2px solid #63b3ed;
    padding-bottom: 4px;
}
.step-item.completed {
    color: #cbd5e0;
}
/* Metric Cards */
.metric-card {
    background: #151b2b;
    border: 1px solid #2d3748;
    border-radius: 0.75rem;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    height: 100%;
}
.metric-value {
    font-size: 2.75rem;
    font-weight: 800;
    color: #f7fafc;
    margin: 0.5rem 0;
}
.metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.gain-positive { color: #48bb78; font-weight: 600; font-size: 0.95rem; }
.gain-negative { color: #f56565; font-weight: 600; font-size: 0.95rem; }
/* Option Cards */
.option-card {
    background: #151b2b;
    border: 1px solid #2d3748;
    border-radius: 0.75rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.option-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #2d3748;
    padding-bottom: 1rem;
}
.option-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #63b3ed;
    margin: 0;
}
.effort-badge {
    background: #276749;
    color: #c6f6d5;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 600;
}
.stats-grid {
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;
    background: #0b0f19;
    padding: 1.25rem;
    border-radius: 0.5rem;
    border: 1px solid #2d3748;
}
.stat-item {
    flex: 1;
    text-align: center;
}
.stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f7fafc;
}
.stat-label {
    font-size: 0.85rem;
    color: #a0aec0;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.change-item {
    display: flex;
    justify-content: space-between;
    padding: 0.85rem 1rem;
    background: #0b0f19;
    border-radius: 0.5rem;
    border: 1px solid #2d3748;
    margin-bottom: 0.5rem;
}
.sem-badge {
    display: inline-block;
    background: #2d3748;
    color: #e2e8f0;
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    margin-bottom: 0.75rem;
    margin-top: 1.25rem;
    font-weight: 600;
}
/* Fix slider padding on PC */
div[data-testid="stSlider"] {
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# DATA CONFIGURATION
# =====================================================================
CONFIG = {
    "BMS": {
        1: {
            "core": {"Fundamentals of Management": 4, "Financial Accounting & Analysis": 4, "Statistics": 4, "EVS": 2, "Basic IT Tools": 2},
            "electives": {
                "General Elective": {"Entrepreneurship Essentials": 4, "Python Programming": 4},
                "Additional Subject": {"Fit India": 2, "Constitution": 2}
            }
        },
        2: {
            "core": {"Macroeconomics": 4, "Introduction to Business Analytics": 4, "Organisational Behaviour": 4},
            "electives": {
                "General Elective": {"Creativity & Innovation": 4},
                "Professional Skill Subject": {"Communication in Professional Life": 4, "Business Intelligence and Data Visualization": 4},
                "Personal Development Subject": {"Social & Emotional Learning": 2, "The Art of Being Happy": 2},
                "Language": {"Hindi": 2, "Sanskrit": 2, "Punjabi": 2, "Bengali": 2, "Other Language": 2}
            }
        }
    },
    "BBA FIA": {
        1: {
            "core": {"Microeconomics": 4, "Financial Accounting & Analysis": 4, "Statistics": 4, "EVS": 2, "Basic IT Tools": 2},
            "electives": {
                "General Elective": {"Entrepreneurship Essentials": 4, "Python Programming": 4},
                "Additional Subject": {"Fit India": 2, "Constitution": 2}
            }
        },
        2: {
            "core": {"Macroeconomics": 4, "Introduction to Business Analytics": 4, "Organisational Behaviour": 4},
            "electives": {
                "General Elective": {"Creativity & Innovation": 4},
                "Professional Skill Subject": {"Communication in Professional Life": 4, "Business Intelligence and Data Visualization": 4},
                "Personal Development Subject": {"Social & Emotional Learning": 2, "The Art of Being Happy": 2},
                "Language": {"Hindi": 2, "Sanskrit": 2, "Punjabi": 2, "Bengali": 2, "Other Language": 2}
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
if "gpas_sem1" not in st.session_state: st.session_state.gpas_sem1 = {}
if "gpas_sem2" not in st.session_state: st.session_state.gpas_sem2 = {}

def spacer(rem=2):
    st.markdown(f"<div style='height: {rem}rem'></div>", unsafe_allow_html=True)

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def reset_app():
    st.session_state.step = 1
    st.session_state.gpas_sem1 = {}
    st.session_state.gpas_sem2 = {}

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

def my_rerun():
    if hasattr(st, "rerun"): st.rerun()
    else: st.experimental_rerun()

# =====================================================================
# UI LAYOUT SHELL
# =====================================================================
st.markdown("<div class='main-title'>SSCBS Academic Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Strategize your semesters. Discover the most efficient path to improve your CGPA.</div>", unsafe_allow_html=True)

steps = ["1. Setup Profile", "2. Academic Data", "3. Strategy & Targets", "4. Dashboard"]
html_steps = "<div class='step-indicator'>"
for i, s in enumerate(steps, 1):
    cls = "active" if i == st.session_state.step else ("completed" if i < st.session_state.step else "")
    html_steps += f"<div class='step-item {cls}'>{s}</div>"
html_steps += "</div>"
st.markdown(html_steps, unsafe_allow_html=True)

# We use an empty container to constrain the width nicely for PC without wrapping standard elements inside HTML
main_container = st.container()

with main_container:
    # -----------------------------------------------------------------
    # STEP 1: SETUP
    # -----------------------------------------------------------------
    if st.session_state.step == 1:
        st.markdown("### Profile Settings")
        st.caption("Tell us about your current academic standing.")
        spacer(1)
        
        c1, c2 = st.columns(2)
        with c1:
            course = st.radio("Course Program", ["BMS", "BBA FIA"], index=0 if st.session_state.course == "BMS" else 1)
        with c2:
            semester = st.radio("Current Semester", [1, 2], index=st.session_state.semester - 1)
            
        spacer(3)
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            if st.button("Continue to Academic Data →", type="primary", use_container_width=True):
                st.session_state.course = course
                st.session_state.semester = semester
                next_step()
                my_rerun()

    # -----------------------------------------------------------------
    # STEP 2: ACADEMIC DATA
    # -----------------------------------------------------------------
    elif st.session_state.step == 2:
        course = st.session_state.course
        sem = st.session_state.semester
        
        st.markdown(f"### Semester 1 Data {'(Actual Results)' if sem == 2 else '(Current/Expected)'}")
        if sem == 2:
            st.caption("Please select your subjects and enter your actual grades from Semester 1 to establish your baseline CGPA.")
        
        config1 = CONFIG[course][1]
        
        sem1_selections = {}
        if config1["electives"]:
            st.markdown("##### 1. Select Semester 1 Electives")
            cols_el1 = st.columns(len(config1["electives"]))
            for i, (cat, opts) in enumerate(config1["electives"].items()):
                with cols_el1[i]:
                    sel = st.selectbox(cat, list(opts.keys()), key=f"s1_sel_{cat}")
                    sem1_selections[sel] = opts[sel]
                    
        subjects_sem1_dict = {**config1["core"], **sem1_selections}
        st.session_state.subjects_sem1 = subjects_sem1_dict
        
        spacer(1)
        st.markdown("##### 2. Enter Subject Grades")
        cols_sl1 = st.columns(2)
        for i, (sub, cred) in enumerate(subjects_sem1_dict.items()):
            if sub not in st.session_state.gpas_sem1:
                st.session_state.gpas_sem1[sub] = 6
            with cols_sl1[i % 2]:
                st.session_state.gpas_sem1[sub] = st.slider(f"{sub} ({cred} Cr)", 0, 10, st.session_state.gpas_sem1[sub], key=f"gpa1_{sub}")

        if sem == 2:
            curr_cgpa = calculate_gpa(st.session_state.gpas_sem1, subjects_sem1_dict)
            st.info(f"**Current Baseline CGPA:** {curr_cgpa}")
            st.divider()
            
            st.markdown("### Semester 2 Data (Current/Expected)")
            st.caption("Select your current subjects and enter your expected grades.")
            config2 = CONFIG[course][2]
            
            sem2_selections = {}
            if config2["electives"]:
                st.markdown("##### 1. Select Semester 2 Electives")
                cols_el2 = st.columns(4)
                for i, (cat, opts) in enumerate(config2["electives"].items()):
                    with cols_el2[i % 4]:
                        sel = st.selectbox(cat, list(opts.keys()), key=f"s2_sel_{cat}")
                        sem2_selections[sel] = opts[sel]
                        
            subjects_sem2_dict = {**config2["core"], **sem2_selections}
            st.session_state.subjects_sem2 = subjects_sem2_dict
            
            spacer(1)
            st.markdown("##### 2. Enter Subject Grades")
            cols_sl2 = st.columns(2)
            for i, (sub, cred) in enumerate(subjects_sem2_dict.items()):
                if sub not in st.session_state.gpas_sem2:
                    st.session_state.gpas_sem2[sub] = 6
                with cols_sl2[i % 2]:
                    st.session_state.gpas_sem2[sub] = st.slider(f"{sub} ({cred} Cr)", 0, 10, st.session_state.gpas_sem2[sub], key=f"gpa2_{sub}")

        spacer(3)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("← Back", use_container_width=True):
                prev_step()
                my_rerun()
        with c3:
            if st.button("Continue to Strategy →", type="primary", use_container_width=True):
                next_step()
                my_rerun()

    # -----------------------------------------------------------------
    # STEP 3: STRATEGY
    # -----------------------------------------------------------------
    elif st.session_state.step == 3:
        sem = st.session_state.semester
        
        st.markdown("### Optimization Targets")
        st.caption("Set the academic goal you wish to achieve.")
        
        c_targ1, c_targ2 = st.columns(2)
        with c_targ1:
            target_type = st.radio("Target Metric", ["Target CGPA", "Target SGPA"] if sem == 2 else ["Target SGPA", "Target CGPA"], horizontal=True)
            st.session_state.target_type = target_type
        with c_targ2:
            achievable = [round(x/100, 2) for x in range(600, 1001)]
            target_val = st.select_slider("Target Value", options=achievable, value=achievable[200])
            st.session_state.target_val = target_val

        st.divider()
        st.markdown("### Constraints & Planning")
        st.caption("Customize how the optimizer evaluates possibilities.")
        
        c_str1, c_str2 = st.columns(2)
        with c_str1:
            if sem == 2:
                st.markdown("##### Re-appear / Improvement")
                st.session_state.improve_sem1 = st.toggle("I plan to re-appear for some Sem 1 subjects", st.session_state.get("improve_sem1", False))
                if st.session_state.improve_sem1:
                    st.session_state.improving_subjects = st.multiselect(
                        "Select Semester 1 subjects you plan to improve:",
                        list(st.session_state.subjects_sem1.keys()),
                        default=st.session_state.get("improving_subjects", [])
                    )
                else:
                    st.session_state.improving_subjects = []
            else:
                st.info("Re-appear mode is only available in Semester 2.")
                
        with c_str2:
            st.markdown("##### Lock Subjects")
            if sem == 2:
                st.session_state.locked_sem2 = st.multiselect(
                    "Lock Sem 2 subjects (keep grades fixed to current):",
                    list(st.session_state.subjects_sem2.keys()),
                    default=st.session_state.get("locked_sem2", [])
                )
            else:
                st.session_state.locked_sem1 = st.multiselect(
                    "Lock Sem 1 subjects (keep grades fixed to current):",
                    list(st.session_state.subjects_sem1.keys()),
                    default=st.session_state.get("locked_sem1", [])
                )

        spacer(3)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("← Back", use_container_width=True):
                prev_step()
                my_rerun()
        with c3:
            if st.button("Generate Strategy →", type="primary", use_container_width=True):
                next_step()
                my_rerun()

    # -----------------------------------------------------------------
    # STEP 4: DASHBOARD RESULTS
    # -----------------------------------------------------------------
    elif st.session_state.step == 4:
        sem = st.session_state.semester
        base_gpas1 = st.session_state.gpas_sem1
        base_gpas2 = st.session_state.gpas_sem2
        creds1 = st.session_state.subjects_sem1
        creds2 = st.session_state.subjects_sem2
        
        base_sgpa1 = calculate_gpa(base_gpas1, creds1)
        if sem == 2:
            base_sgpa2 = calculate_gpa(base_gpas2, creds2)
            base_cgpa = calculate_cgpa(base_gpas1, creds1, base_gpas2, creds2)
        else:
            base_sgpa2 = 0.0
            base_cgpa = base_sgpa1
            
        modifiable = []
        ranges = []
        subject_credits = {}
        
        if sem == 2:
            for sub in st.session_state.improving_subjects:
                modifiable.append((1, sub))
                ranges.append(range(base_gpas1[sub], 11))
                subject_credits[(1, sub)] = creds1[sub]
            for sub in creds2:
                if sub not in st.session_state.get("locked_sem2", []):
                    modifiable.append((2, sub))
                    ranges.append(range(base_gpas2[sub], 11))
                    subject_credits[(2, sub)] = creds2[sub]
        else:
            for sub in creds1:
                if sub not in st.session_state.get("locked_sem1", []):
                    modifiable.append((1, sub))
                    ranges.append(range(base_gpas1[sub], 11))
                    subject_credits[(1, sub)] = creds1[sub]
                    
        total_combinations = math.prod(len(r) for r in ranges) if ranges else 0
        
        if total_combinations > 5000000:
            st.error(f"Too many optimization variables ({total_combinations:,} paths). Please lock a few subjects to proceed.")
            if st.button("← Adjust Strategy"):
                prev_step()
                my_rerun()
            st.stop()
            
        results = []
        max_cgpa_achieved = 0.0
        max_sgpa_achieved = 0.0
        
        if modifiable:
            with st.spinner("Analyzing academic permutations..."):
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
                        
                        valid = (new_cgpa >= st.session_state.target_val) if st.session_state.target_type == "Target CGPA" else (new_sgpa2 >= st.session_state.target_val)
                    else:
                        new_sgpa1 = calculate_gpa(temp_gpas1, creds1)
                        new_cgpa = new_sgpa1
                        max_cgpa_achieved = max(max_cgpa_achieved, new_cgpa)
                        max_sgpa_achieved = max(max_sgpa_achieved, new_sgpa1)
                        
                        valid = (new_cgpa >= st.session_state.target_val) if st.session_state.target_type == "Target CGPA" else (new_sgpa1 >= st.session_state.target_val)
                            
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
            res_cgpa = base_cgpa
            res_sgpa = base_sgpa2 if sem == 2 else base_sgpa1
            max_cgpa_achieved = res_cgpa
            max_sgpa_achieved = res_sgpa
            
            valid = (res_cgpa >= st.session_state.target_val) if st.session_state.target_type == "Target CGPA" else (res_sgpa >= st.session_state.target_val)
            if valid:
                results.append({
                    "effort": 0, "gpas1": base_gpas1, "gpas2": base_gpas2, "cgpa": res_cgpa, "sgpa": res_sgpa
                })

        # --- Dashboard Top Metrics ---
        st.markdown("### Top Summary")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Current CGPA</div>
                <div class='metric-value'>{base_cgpa}</div>
            </div>
            """, unsafe_allow_html=True)
            
        if results:
            results.sort(key=lambda x: x["effort"])
            best = results[0]
            gain = round(best['cgpa'] - base_cgpa, 2)
            gain_html = f"<div class='gain-positive'>Gain: +{gain}</div>" if gain > 0 else (f"<div class='gain-negative'>Gain: {gain}</div>" if gain < 0 else "<div>Gain: 0.0</div>")
            
            with c2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Projected CGPA</div>
                    <div class='metric-value'>{best['cgpa']}</div>
                    {gain_html}
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Projected SGPA</div>
                    <div class='metric-value'>{best['sgpa']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            spacer(2)
            st.markdown("### Recommended Strategies")
            
            for idx, res in enumerate(results[:3]):
                opt_gain = round(res['cgpa'] - base_cgpa, 2)
                opt_gain_str = f"+{opt_gain}" if opt_gain > 0 else str(opt_gain)
                gain_color = "#48bb78" if opt_gain > 0 else "#a0aec0"
                
                html = f"""
                <div class='option-card'>
                    <div class='option-header'>
                        <h3 class='option-title'>Option {idx+1}</h3>
                        <div class='effort-badge'>Effort Score: {res['effort']}</div>
                    </div>
                    
                    <div class='stats-grid'>
                        <div class='stat-item'>
                            <div class='stat-label'>Projected SGPA</div>
                            <div class='stat-value'>{res['sgpa']}</div>
                        </div>
                        <div class='stat-item'>
                            <div class='stat-label'>Projected CGPA</div>
                            <div class='stat-value'>{res['cgpa']}</div>
                        </div>
                        <div class='stat-item'>
                            <div class='stat-label'>CGPA Gain</div>
                            <div class='stat-value' style='color:{gain_color};'>{opt_gain_str}</div>
                        </div>
                    </div>
                    
                    <div class='metric-label' style='margin-bottom:0.75rem;'>Required Changes</div>
                    <div class='changes-list'>
                """
                
                chg_sem2 = []
                chg_sem1 = []
                
                if sem == 2:
                    for sub in creds2:
                        if res['gpas2'][sub] > base_gpas2[sub]:
                            chg_sem2.append(f"<div class='change-item'><span>{sub}</span> <strong style='color:#f7fafc;'>{base_gpas2[sub]} &rarr; {res['gpas2'][sub]}</strong></div>")
                
                for sub in (st.session_state.improving_subjects if sem == 2 else creds1):
                    if res['gpas1'][sub] > base_gpas1[sub]:
                        chg_sem1.append(f"<div class='change-item'><span>{sub}</span> <strong style='color:#f7fafc;'>{base_gpas1[sub]} &rarr; {res['gpas1'][sub]}</strong></div>")
                        
                if sem == 2 and chg_sem2:
                    html += f"<div class='sem-badge'>Semester 2</div>"
                    html += "".join(chg_sem2)
                    
                if chg_sem1:
                    label = "Semester 1 Improvement" if sem == 2 else "Semester 1"
                    html += f"<div class='sem-badge'>{label}</div>"
                    html += "".join(chg_sem1)
                    
                if not chg_sem2 and not chg_sem1:
                    html += "<div class='subtle'>No improvements needed. Your baseline already meets the target.</div>"
                    
                html += "</div></div>"
                st.markdown(html, unsafe_allow_html=True)
                
        else:
            with c2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Max Possible CGPA</div>
                    <div class='metric-value'>{max_cgpa_achieved}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Max Possible SGPA</div>
                    <div class='metric-value'>{max_sgpa_achieved}</div>
                </div>
                """, unsafe_allow_html=True)
            spacer(1)
            st.error(f"**Target Unreachable.** Even with perfect 10s in all unlocked subjects, the maximum achievable CGPA is {max_cgpa_achieved}.")
            
        spacer(2)
        btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
        with btn_c1:
            if st.button("← Adjust Target", use_container_width=True):
                prev_step()
                my_rerun()
        with btn_c3:
            if st.button("Start Over", use_container_width=True):
                reset_app()
                my_rerun()

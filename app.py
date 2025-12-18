import streamlit as st
from itertools import product

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GPA Planner",
    page_icon="🎓",
    layout="centered",
)

# -------------------- GLOBAL STYLES --------------------
st.markdown("""
<style>
body { background-color: #0f1117; color: #ffffff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 5rem; max-width: 750px; }
.card { background: #1a1c23; border-radius: 20px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 12px 30px rgba(0,0,0,0.35); transition: all 0.2s ease-in-out; }
.card:hover { box-shadow: 0 20px 40px rgba(0,0,0,0.45); }
.title-card { text-align: center; font-size: 38px; font-weight: 700; letter-spacing: 1.2px; margin-bottom: 12px; color: #ffffff; }
.subtle { color: #9a9ea6; font-size: 14px; margin-top: 4px; }
.badge { display: inline-block; padding: 6px 14px; border-radius: 999px; background: #4f6ef7; color: white; font-size: 13px; margin-bottom: 8px; }
.stButton>button { border-radius: 16px; padding: 14px 20px; font-size: 16px; background: #4f6ef7; color: #fff; border: none; transition: all 0.2s ease-in-out; }
.stButton>button:hover { background: #3b55c7; }
.hero { font-size: 42px; font-weight: 700; letter-spacing: 0.5px; margin-top: 4px; color: #ffffff; }
h3 { font-weight: 600; font-size: 20px; margin-bottom: 6px; }
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE CARD --------------------
st.markdown("""
<div class="card title-card">
GPA Planner
</div>
""", unsafe_allow_html=True)

# -------------------- COURSE SELECTION --------------------
st.markdown("""
<div class="card">
<h3>Select your course</h3>
<p class="subtle">Subjects will adjust automatically based on your choice</p>
</div>
""", unsafe_allow_html=True)

course = st.radio("Course", ["BMS", "BBA FIA"], horizontal=True)

# -------------------- ELECTIVE SELECTION --------------------
st.markdown("""
<div class="card">
<h3>Choose your electives</h3>
<p class="subtle">Pick one from each slot</p>
</div>
""", unsafe_allow_html=True)

elective_1 = st.radio("Elective Slot 1", ["Entrepreneurship Essentials", "Python Programming"])
elective_2 = st.radio("Elective Slot 2", ["Fit India", "Constitution"])

# -------------------- SUBJECT DEFINITION --------------------
subjects = [
    ("Financial Accounting & Analysis", 4),
    ("Statistics", 4),
    (elective_1, 4),
    ("EVS", 2),
    ("Basic IT Tools", 2),
    (elective_2, 2),
]

if course == "BMS":
    subjects.insert(0, ("Fundamentals of Management", 4))
else:
    subjects.insert(0, ("Microeconomics", 4))

subjects_dict = dict(subjects)
total_credits = sum(c for _, c in subjects)

# -------------------- SESSION STATE --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {}
for s, _ in subjects:
    st.session_state.gpas.setdefault(s, 6)

# -------------------- GPA INPUT --------------------
st.markdown("""
<div class="card">
<h3>Enter subject GPAs</h3>
<p class="subtle">Tap carefully — sliders move in steps of 1</p>
</div>
""", unsafe_allow_html=True)

for sub, credits in subjects:
    st.markdown(f"""
    <div class="card">
        <span class="badge">{credits} credits</span><br>
        <strong>{sub}</strong>
    """, unsafe_allow_html=True)

    st.session_state.gpas[sub] = st.slider("", 0, 10, st.session_state.gpas[sub], step=1, key=sub)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA CALCULATION --------------------
def final_gpa():
    return round(sum(st.session_state.gpas[s] * subjects_dict[s] for s in subjects_dict) / total_credits, 2)

current_gpa = final_gpa()

# -------------------- SNAPSHOT --------------------
st.markdown(f"""
<div class="card">
<p class="subtle">Your current GPA</p>
<div class="hero">{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- TARGET GPA --------------------
st.markdown("""
<div class="card">
<h3>Target GPA</h3>
<p class="subtle">Pick a target from achievable values</p>
</div>
""", unsafe_allow_html=True)

# Achievable GPA list from 6 → 10 in multiples of 0.09 (precisely defined)
raw_gpas = [6.00, 6.09, 6.18, 6.27, 6.36, 6.45, 6.55, 6.64, 6.73, 6.82, 6.91,
            7.00, 7.09, 7.18, 7.27, 7.36, 7.45, 7.55, 7.64, 7.73, 7.82, 7.91,
            8.00, 8.09, 8.18, 8.27, 8.36, 8.45, 8.55, 8.64, 8.73, 8.82, 8.91,
            9.00, 9.09, 9.18, 9.27, 9.36, 9.45, 9.55, 9.64, 9.73, 9.82, 9.91, 10.00]

achievable_gpas = [float(f"{g:.2f}") for g in raw_gpas if g >= 8.00]  # start from 8

# Slider uses exact list values
target = st.select_slider("Target GPA", options=achievable_gpas, value=achievable_gpas[0])
st.write(f"Selected target GPA: **{target}**")

# -------------------- LOCKED SUBJECTS --------------------
fixed_subjects = st.multiselect("Select subjects to Lock", [s for s, _ in subjects])

# -------------------- OPTIMIZATION --------------------
if st.button("Show me the easiest paths", use_container_width=True):
    modifiable = [s for s, _ in subjects if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []
    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]
        achieved = round(sum(temp[s] * subjects_dict[s] for s in subjects_dict) / total_credits, 2)
        if achieved >= target:
            effort = sum((temp[s] - st.session_state.gpas[s]) * subjects_dict[s] for s in modifiable)
            results.append((achieved, effort, temp))

    if not results:
        # Maximum achievable GPA with current constraints
        all_combos = product(*[range(st.session_state.gpas[s], 11) for s in modifiable])
        max_gpa = 0
        for combo in all_combos:
            temp = st.session_state.gpas.copy()
            for i, s in enumerate(modifiable):
                temp[s] = combo[i]
            achieved = round(sum(temp[s] * subjects_dict[s] for s in subjects_dict) / total_credits, 2)
            if achieved > max_gpa:
                max_gpa = achieved
        st.info(f"Maximum achievable GPA with current constraints: **{max_gpa}**")
    else:
        results.sort(key=lambda x: x[1])  # sort by minimum effort
        st.success(f"Top 3 achievable strategies:")

        for idx, (ach, eff, dist) in enumerate(results[:3], start=1):
            st.markdown(f"""
            <div class="card">
            <strong>Option {idx}</strong><br>
            Final GPA: {ach} &nbsp;&nbsp; | &nbsp;&nbsp; Extra effort: {eff}
            </div>
            """, unsafe_allow_html=True)
            for s, _ in subjects:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

        # Dropdown for all combinations
        all_options = [f"Option {i+1}: GPA {ach}, Effort {eff}" for i, (ach, eff, _) in enumerate(results)]
        selected_option = st.selectbox("See all possible strategies", all_options)
        sel_idx = all_options.index(selected_option)
        _, _, sel_dist = results[sel_idx]
        st.markdown("<div class='card'>Details:</div>", unsafe_allow_html=True)
        for s, _ in subjects:
            diff = sel_dist[s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {sel_dist[s]} (+{diff})")

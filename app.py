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
body { background-color: #0f1117; }
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 5rem;
}
.card {
    background: #161b22;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}
.hero { font-size: 44px; font-weight: 700; }
.subtle { color: #8b949e; font-size: 14px; }
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: #1f6feb;
    color: white;
    font-size: 13px;
}
.stButton>button {
    border-radius: 14px;
    padding: 14px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- COURSE SELECTION --------------------
st.markdown("""
<div class="card">
<h3>Select your course</h3>
<p class="subtle">Subjects will adjust automatically</p>
</div>
""", unsafe_allow_html=True)

course = st.radio(
    "Course",
    ["BMS", "BBA FIA"],
    horizontal=True
)

# -------------------- ELECTIVE SELECTION --------------------
st.markdown("""
<div class="card">
<h3>Choose your electives</h3>
<p class="subtle">Pick one from each slot</p>
</div>
""", unsafe_allow_html=True)

elective_1 = st.radio(
    "Elective Slot 1",
    ["Entrepreneurship Essentials", "Python Programming"]
)

elective_2 = st.radio(
    "Elective Slot 2",
    ["Fit India", "Constitution"]
)

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
<p class="subtle">Tap carefully — sliders move in steps</p>
</div>
""", unsafe_allow_html=True)

for sub, credits in subjects:
    st.markdown(f"""
    <div class="card">
        <span class="badge">{credits} credits</span><br>
        <strong>{sub}</strong>
    """, unsafe_allow_html=True)

    st.session_state.gpas[sub] = st.slider(
        "",
        0, 10,
        st.session_state.gpas[sub],
        step=1,
        key=sub
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA CALCULATION --------------------
def final_gpa():
    return round(
        sum(st.session_state.gpas[s] * subjects_dict[s] for s in subjects_dict)
        / total_credits,
        2
    )

current_gpa = final_gpa()

# -------------------- SNAPSHOT --------------------
st.markdown(f"""
<div class="card">
<p class="subtle">Your current GPA</p>
<div class="hero">{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- TARGET PLANNER --------------------
st.markdown("""
<div class="card">
<h3>Target GPA</h3>
<p class="subtle">Higher targets require more effort</p>
</div>
""", unsafe_allow_html=True)

target = st.slider(
    "Target GPA",
    0.0, 10.0,
    value=max(7.5, current_gpa),
    step=0.1
)

fixed_subjects = st.multiselect(
    "Lock subjects you don’t want to push",
    [s for s, _ in subjects]
)

# -------------------- OPTIMIZATION --------------------
if st.button("🚀 Show me the easiest way", use_container_width=True):

    modifiable = [s for s, _ in subjects if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        achieved = round(
            sum(temp[s] * subjects_dict[s] for s in subjects_dict)
            / total_credits, 2
        )

        if achieved >= target:
            effort = sum(
                (temp[s] - st.session_state.gpas[s]) * subjects_dict[s]
                for s in modifiable
            )
            results.append((achieved, effort, temp))

    if not results:
        st.error("❌ Target not achievable with current constraints.")
    else:
        results.sort(key=lambda x: x[1])
        st.success("✅ Best possible strategy")

        ach, eff, dist = results[0]

        st.markdown(f"""
        <div class="card">
        <h3>Final GPA: {ach}</h3>
        <p class="subtle">Extra effort required: {eff}</p>
        </div>
        """, unsafe_allow_html=True)

        for s, _ in subjects:
            diff = dist[s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {dist[s]} (+{diff})")

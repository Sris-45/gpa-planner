import streamlit as st
from itertools import product

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GPA Planner",
    layout="centered",
)

# -------------------- GLOBAL STYLES (THEME AWARE) --------------------
st.markdown("""
<style>
.block-container {
    max-width: 750px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

.card {
    background: var(--secondary-background-color);
    color: var(--text-color);
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,0,0,0.06);
}

.title-card {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 0.6px;
}

.subtle {
    color: rgba(128,128,128,0.9);
    font-size: 14px;
}

.badge {
    padding: 6px 14px;
    border-radius: 999px;
    background: #4f6ef7;
    color: white;
    font-size: 13px;
}

.hero {
    font-size: 42px;
    font-weight: 700;
}

.stButton>button {
    border-radius: 16px;
    padding: 14px 20px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown('<div class="card title-card">GPA Planner</div>', unsafe_allow_html=True)

# -------------------- COURSE SELECTION --------------------
st.markdown('<div class="card"><h3>Select your course</h3></div>', unsafe_allow_html=True)

course = st.radio("Course", ["BMS", "BBA FIA"], horizontal=True)

# -------------------- ELECTIVES --------------------
st.markdown('<div class="card"><h3>Choose your electives</h3></div>', unsafe_allow_html=True)

elective_1 = st.radio("Elective Slot 1", ["Entrepreneurship Essentials", "Python Programming"])
elective_2 = st.radio("Elective Slot 2", ["Fit India", "Constitution"])

# -------------------- SUBJECT LIST --------------------
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

# -------------------- SESSION STATE (SAFE RESET) --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {}

# remove stale subjects
for key in list(st.session_state.gpas.keys()):
    if key not in subjects_dict:
        del st.session_state.gpas[key]

# add new subjects
for s in subjects_dict:
    st.session_state.gpas.setdefault(s, 6)

# -------------------- GPA INPUT --------------------
st.markdown('<div class="card"><h3>Enter subject GPAs</h3></div>', unsafe_allow_html=True)

for sub, credits in subjects:
    st.markdown(f"""
    <div class="card">
        <span class="badge">{credits} credits</span><br>
        <strong>{sub}</strong>
    """, unsafe_allow_html=True)

    st.session_state.gpas[sub] = st.slider(
        label="",
        min_value=0,
        max_value=10,
        value=st.session_state.gpas[sub],
        step=1,
        key=f"gpa_{sub}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA CALC --------------------
def calc_gpa(dist):
    return round(sum(dist[s] * subjects_dict[s] for s in subjects_dict) / total_credits, 2)

current_gpa = calc_gpa(st.session_state.gpas)

st.markdown(f"""
<div class="card">
<p class="subtle">Current GPA</p>
<div class="hero">{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- TARGET GPA --------------------
st.markdown('<div class="card"><h3>Target GPA</h3></div>', unsafe_allow_html=True)

achievable_gpas = [
    8.00, 8.09, 8.18, 8.27, 8.36, 8.45, 8.55, 8.64, 8.73, 8.82, 8.91,
    9.00, 9.09, 9.18, 9.27, 9.36, 9.45, 9.55, 9.64, 9.73, 9.82, 9.91, 10.00
]

target = st.select_slider(
    "Target GPA",
    options=achievable_gpas,
    value=8.00
)

# -------------------- LOCK SUBJECTS --------------------
fixed_subjects = st.multiselect(
    "Lock subjects",
    list(subjects_dict.keys())
)

st.caption(
    "Lock subjects whose GPA you want to keep fixed. "
    "The planner will adjust only the remaining subjects to reach your target."
)

# -------------------- OPTIMIZATION --------------------
if st.button("Show me the easiest paths", use_container_width=True):

    modifiable = [s for s in subjects_dict if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        achieved = calc_gpa(temp)
        if achieved >= target:
            effort = sum(
                (temp[s] - st.session_state.gpas[s]) * subjects_dict[s]
                for s in modifiable
            )
            results.append((achieved, effort, temp))

    if not results:
        max_gpa = current_gpa
        for combo in product(*ranges):
            temp = st.session_state.gpas.copy()
            for i, s in enumerate(modifiable):
                temp[s] = combo[i]
            max_gpa = max(max_gpa, calc_gpa(temp))

        st.info(f"Maximum achievable GPA with current constraints: **{max_gpa}**")

    else:
        results.sort(key=lambda x: x[1])
        st.success("Best possible strategy")

        top = results[0]
        st.markdown(f"""
        <div class="card">
        <strong>Final GPA:</strong> {top[0]}<br>
        <strong>Extra effort:</strong> {top[1]}
        </div>
        """, unsafe_allow_html=True)

        for s in subjects_dict:
            diff = top[2][s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {top[2][s]} (+{diff})")

        # Dropdown for all strategies
        labels = [f"GPA {a} | Effort {e}" for a, e, _ in results]
        choice = st.selectbox("All possible strategies", labels)

        idx = labels.index(choice)
        _, _, dist = results[idx]

        st.markdown('<div class="card"><strong>Details</strong></div>', unsafe_allow_html=True)
        for s in subjects_dict:
            diff = dist[s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {dist[s]} (+{diff})")

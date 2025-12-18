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
.block-container { max-width: 750px; padding-top: 2rem; padding-bottom: 5rem; }
.card {
    background: #1a1c23;
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.title-card {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
}
.subtle { color: #9a9ea6; font-size: 14px; }
.badge {
    padding: 6px 14px;
    border-radius: 999px;
    background: #4f6ef7;
    font-size: 13px;
}
.hero { font-size: 42px; font-weight: 700; }
.stButton>button {
    border-radius: 16px;
    padding: 14px 20px;
    background: #4f6ef7;
    color: #fff;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<div class='card title-card'>GPA Planner</div>", unsafe_allow_html=True)

# -------------------- COURSE --------------------
course = st.radio("Course", ["BMS", "BBA FIA"], horizontal=True)

# -------------------- ELECTIVES --------------------
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
current_subject_names = [s for s, _ in subjects]

# -------------------- SESSION STATE SYNC (CRITICAL FIX) --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {}

# Add missing subjects
for s in current_subject_names:
    if s not in st.session_state.gpas:
        st.session_state.gpas[s] = 6

# Remove subjects that no longer exist
for s in list(st.session_state.gpas.keys()):
    if s not in current_subject_names:
        del st.session_state.gpas[s]

# -------------------- GPA INPUT --------------------
st.markdown("<div class='card'><h3>Enter subject GPAs</h3></div>", unsafe_allow_html=True)

for sub, credits in subjects:
    st.markdown(
        f"<div class='card'><span class='badge'>{credits} credits</span><br><strong>{sub}</strong>",
        unsafe_allow_html=True
    )

    st.session_state.gpas[sub] = st.slider(
        "",
        0, 10,
        st.session_state.gpas[sub],
        step=1,
        key=sub
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA CALC --------------------
def calc_gpa(dist):
    return round(
        sum(dist[s] * subjects_dict[s] for s in subjects_dict) / total_credits,
        2
    )

current_gpa = calc_gpa(st.session_state.gpas)

st.markdown(f"""
<div class='card'>
<p class='subtle'>Your current GPA</p>
<div class='hero'>{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- TARGET GPA --------------------
achievable_gpas = [round(x / 100, 2) for x in range(800, 1001)]

target = st.select_slider(
    "Target GPA",
    options=achievable_gpas,
    value=achievable_gpas[0]
)

# -------------------- LOCKED SUBJECTS --------------------
st.markdown("""
<div class='card'>
<h3>Lock subjects</h3>
<p class='subtle'>
Lock subjects whose GPA you want to keep as they are.  
The planner will work out how the remaining subjects can be adjusted to reach your target.
</p>
</div>
""", unsafe_allow_html=True)

fixed_subjects = st.multiselect(
    "Select subjects to lock",
    current_subject_names
)

# -------------------- OPTIMIZATION --------------------
if st.button("Show me the easiest paths", use_container_width=True):

    modifiable = [s for s in current_subject_names if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []
    max_possible = 0

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        achieved = calc_gpa(temp)
        max_possible = max(max_possible, achieved)

        if achieved >= target:
            effort = sum(
                (temp[s] - st.session_state.gpas[s]) * subjects_dict[s]
                for s in modifiable
            )
            results.append((achieved, effort, temp))

    if not results:
        st.info(f"Maximum achievable GPA with current locks: **{max_possible}**")

    else:
        results.sort(key=lambda x: x[1])
        st.success("Top 3 easiest strategies")

        for i, (gpa, effort, dist) in enumerate(results[:3], 1):
            st.markdown(
                f"<div class='card'><strong>Option {i}</strong><br>"
                f"Final GPA: {gpa} | Extra effort: {effort}</div>",
                unsafe_allow_html=True
            )

            for s in current_subject_names:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

import streamlit as st
from itertools import product

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GPA Planner",
    layout="centered",
)

# -------------------- STYLES --------------------
st.markdown("""
<style>
.block-container {
    max-width: 750px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.card {
    background: #1a1c23;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
}

.title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
}

.subtle {
    color: #9a9ea6;
    font-size: 14px;
    margin-top: 4px;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: #4f6ef7;
    color: white;
    font-size: 13px;
    margin-bottom: 8px;
}

.hero {
    font-size: 42px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<div class='card title'>GPA Planner</div>", unsafe_allow_html=True)

# -------------------- COURSE --------------------
st.markdown("<div class='card'><strong>Select course</strong></div>", unsafe_allow_html=True)
course = st.radio("", ["BMS", "BBA FIA"], horizontal=True)

# -------------------- ELECTIVES --------------------
st.markdown("<div class='card'><strong>Choose electives</strong></div>", unsafe_allow_html=True)
elective_1 = st.radio("Elective slot 1", ["Entrepreneurship Essentials", "Python Programming"])
elective_2 = st.radio("Elective slot 2", ["Fit India", "Constitution"])

# -------------------- SUBJECTS --------------------
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
subject_names = [s for s, _ in subjects]
total_credits = sum(c for _, c in subjects)

# -------------------- SESSION STATE SYNC --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {}

for s in subject_names:
    st.session_state.gpas.setdefault(s, 6)

for s in list(st.session_state.gpas.keys()):
    if s not in subject_names:
        del st.session_state.gpas[s]

# -------------------- GPA INPUT --------------------
st.markdown("<div class='card'><strong>Enter subject GPAs</strong></div>", unsafe_allow_html=True)

for sub, credits in subjects:
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='badge'>{credits} credits</span>", unsafe_allow_html=True)
    st.markdown(f"**{sub}**")

    st.session_state.gpas[sub] = st.slider(
        label="",
        min_value=0,
        max_value=10,
        step=1,
        value=st.session_state.gpas[sub],
        key=f"gpa_{sub}"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA CALC --------------------
def calc_gpa(dist):
    return round(sum(dist[s] * subjects_dict[s] for s in subjects_dict) / total_credits, 2)

current_gpa = calc_gpa(st.session_state.gpas)

st.markdown(f"""
<div class='card'>
<p class='subtle'>Current GPA</p>
<div class='hero'>{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- TARGET GPA --------------------
achievable_gpas = [round(x / 100, 2) for x in range(800, 1001)]
target = st.select_slider("Target GPA", achievable_gpas, value=8.00)

# -------------------- LOCK SUBJECTS --------------------
st.markdown("""
<div class='card'>
<strong>Lock subjects</strong>
<p class='subtle'>
Lock subjects whose GPA you want to keep fixed.
The planner will adjust only the remaining subjects to reach your target.
</p>
</div>
""", unsafe_allow_html=True)

fixed_subjects = st.multiselect("", subject_names)

# -------------------- OPTIMIZATION --------------------
if st.button("Show me the easiest paths", use_container_width=True):

    modifiable = [s for s in subject_names if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []
    max_possible = current_gpa

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        gpa = calc_gpa(temp)
        max_possible = max(max_possible, gpa)

        if gpa >= target:
            effort = sum((temp[s] - st.session_state.gpas[s]) * subjects_dict[s] for s in modifiable)
            results.append((gpa, effort, temp))

    if not results:
        st.info(f"Maximum achievable GPA with current locks: **{max_possible}**")
    else:
        results.sort(key=lambda x: x[1])
        st.success("Best strategies")

        for i, (gpa, effort, dist) in enumerate(results[:3], 1):
            st.markdown(f"<div class='card'><strong>Option {i}</strong><br>Final GPA: {gpa} | Extra effort: {effort}</div>", unsafe_allow_html=True)
            for s in subject_names:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

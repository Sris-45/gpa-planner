import streamlit as st
from itertools import product

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GPA Planner",
    page_icon="🎓",
    layout="centered",
)

# -------------------- STYLES --------------------
st.markdown("""
<style>
body { background-color: #0f1117; }
.block-container { padding-top: 1.2rem; padding-bottom: 5rem; }
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

# -------------------- COURSE --------------------
st.markdown("<div class='card'><h3>Select your course</h3></div>", unsafe_allow_html=True)
course = st.radio("Course", ["BMS", "BBA FIA"], horizontal=True)

# -------------------- ELECTIVES --------------------
st.markdown("<div class='card'><h3>Choose electives</h3></div>", unsafe_allow_html=True)
elective_1 = st.radio("Elective Slot 1", ["Entrepreneurship Essentials", "Python Programming"])
elective_2 = st.radio("Elective Slot 2", ["Fit India", "Constitution"])

# -------------------- SUBJECT STRUCTURE --------------------
subjects = [
    ("Financial Accounting & Analysis", 4),
    ("Statistics", 4),
    (elective_1, 4),
    ("EVS", 2),
    ("Basic IT Tools", 2),
    (elective_2, 2),
]

subjects.insert(0, ("Fundamentals of Management", 4) if course == "BMS" else ("Microeconomics", 4))

credits = dict(subjects)
total_credits = sum(credits.values())

# -------------------- SESSION STATE --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {s: 6 for s in credits}

# -------------------- INPUT --------------------
st.markdown("<div class='card'><h3>Enter subject GPAs</h3></div>", unsafe_allow_html=True)

for s, c in subjects:
    st.markdown(f"<div class='card'><span class='badge'>{c} credits</span><br><b>{s}</b>", unsafe_allow_html=True)
    st.session_state.gpas[s] = st.slider("", 0, 10, st.session_state.gpas[s], step=1, key=s)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GPA FUNCTION --------------------
def compute_gpa(gpas):
    return round(sum(gpas[s] * credits[s] for s in credits) / total_credits, 2)

current_gpa = compute_gpa(st.session_state.gpas)

st.markdown(f"""
<div class='card'>
<p class='subtle'>Your current GPA</p>
<div class='hero'>{current_gpa}</div>
</div>
""", unsafe_allow_html=True)

# -------------------- VALID GPA TARGETS --------------------
possible_totals = set()
ranges = [range(0, 11)] * len(credits)

for combo in product(*ranges):
    total = sum(combo[i] * list(credits.values())[i] for i in range(len(combo)))
    possible_totals.add(round(total / total_credits, 2))

valid_targets = sorted(t for t in possible_totals if t >= current_gpa)

# -------------------- TARGET SELECTION --------------------
st.markdown("<div class='card'><h3>Select target GPA</h3></div>", unsafe_allow_html=True)

target = st.selectbox(
    "Target GPA (only valid values shown)",
    valid_targets
)

# -------------------- LOCK SUBJECTS --------------------
fixed = st.multiselect("Lock subjects you don’t want to improve", list(credits.keys()))

# -------------------- OPTIMIZATION --------------------
if st.button("🚀 Show me the easiest way", use_container_width=True):

    modifiable = [s for s in credits if s not in fixed]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    best = None

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        gpa = compute_gpa(temp)
        if gpa >= target:
            effort = sum((temp[s] - st.session_state.gpas[s]) * credits[s] for s in modifiable)
            if best is None or effort < best[1]:
                best = (gpa, effort, temp)

    if best is None:
        max_gpa = max(valid_targets)
        st.info(f"💡 With current constraints, the highest achievable GPA is **{max_gpa}**.")
    else:
        gpa, effort, dist = best
        st.success(f"✅ Best achievable GPA: {gpa}")

        for s in credits:
            diff = dist[s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {dist[s]} (+{diff})")

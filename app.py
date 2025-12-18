import streamlit as st
from itertools import product

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="GPA Planner",
    page_icon="🎓",
    layout="wide",
)

# -------------------- GLOBAL STYLES --------------------
st.markdown("""
<style>
body {
    background-color: #0f1117;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: #161b22;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.card h3 {
    margin-bottom: 0.5rem;
}
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: #1f6feb;
    color: white;
    font-size: 14px;
}
.subtle {
    color: #8b949e;
    font-size: 14px;
}
.divider {
    height: 1px;
    background: #30363d;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
subjects = {
    "Fundamentals of Management": 4,
    "Financial Accounting & Analysis": 4,
    "Statistics": 4,
    "Entrepreneurship Essentials": 4,
    "Fit India": 2,
    "EVS": 2,
    "Basic IT Tools": 2
}
total_credits = sum(subjects.values())

if "gpas" not in st.session_state:
    st.session_state.gpas = {s: 6 for s in subjects}

# -------------------- FUNCTIONS --------------------
def final_gpa(gpa_map):
    return round(
        sum(gpa_map[s] * subjects[s] for s in subjects) / total_credits,
        4
    )

# -------------------- HEADER --------------------
st.markdown("""
<div class="card">
    <h2>🎓 GPA Planner</h2>
    <p class="subtle">
        Plan. Optimize. Decide smarter — not harder.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- SECTION 1: GPA INPUT --------------------
st.markdown("""
<div class="card">
    <h3>📘 Enter Your Current GPAs</h3>
    <p class="subtle">Adjust subject GPAs using sliders</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(2)
for i, sub in enumerate(subjects):
    with cols[i % 2]:
        st.session_state.gpas[sub] = st.slider(
            sub,
            0, 10,
            st.session_state.gpas[sub],
            key=sub
        )

# -------------------- SECTION 2: GPA SNAPSHOT --------------------
current_gpa = final_gpa(st.session_state.gpas)

st.markdown("""
<div class="card">
    <h3>📊 Current Snapshot</h3>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Final GPA", current_gpa)
c2.metric("Total Subjects", len(subjects))
c3.metric("Total Credits", total_credits)

# -------------------- DIVIDER --------------------
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# -------------------- SECTION 3: TARGET PLANNER --------------------
st.markdown("""
<div class="card">
    <h3>🎯 Target GPA Planner</h3>
    <p class="subtle">
        Lock what you don’t want to change. Optimize what you can.
    </p>
</div>
""", unsafe_allow_html=True)

target = st.slider(
    "Target Final GPA",
    min_value=0.0,
    max_value=10.0,
    value=max(7.5, current_gpa),
    step=0.1
)

fixed_subjects = st.multiselect(
    "Subjects to keep unchanged",
    list(subjects.keys())
)

if st.button("🚀 Find Best Paths", use_container_width=True):
    modifiable = [s for s in subjects if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        achieved = final_gpa(temp)
        if achieved >= target:
            effort = sum(
                (temp[s] - st.session_state.gpas[s]) * subjects[s]
                for s in modifiable
            )
            results.append((achieved, effort, temp))

    if not results:
        st.error("❌ Target GPA is not achievable with current constraints.")
    else:
        results.sort(key=lambda x: x[1])
        st.success("✅ Best achievable strategies")

        for i, (ach, eff, dist) in enumerate(results[:3], 1):
            st.markdown(f"""
            <div class="card">
                <span class="badge">Option {i}</span>
                <h3>Achieved GPA: {ach}</h3>
                <p class="subtle">Extra weighted effort required: {eff}</p>
            """, unsafe_allow_html=True)

            for s in subjects:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

            st.markdown("</div>", unsafe_allow_html=True)

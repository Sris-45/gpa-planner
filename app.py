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
body {
    background-color: #0f1117;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}
.card {
    background: #161b22;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}
.hero {
    font-size: 48px;
    font-weight: 700;
}
.subtle {
    color: #8b949e;
    font-size: 14px;
}
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: #1f6feb;
    color: white;
    font-size: 13px;
    margin-bottom: 8px;
}
.stButton>button {
    border-radius: 14px;
    padding: 14px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA (ORDER MATTERS) --------------------
subjects = [
    ("Fundamentals of Management", 4),
    ("Financial Accounting & Analysis", 4),
    ("Statistics", 4),
    ("Entrepreneurship Essentials", 4),
    ("EVS", 2),
    ("Basic IT Tools", 2),
    ("Fit India", 2),
]

subjects_dict = dict(subjects)
total_credits = sum(c for _, c in subjects)

# -------------------- SESSION STATE --------------------
if "gpas" not in st.session_state:
    st.session_state.gpas = {s: 6 for s, _ in subjects}

if "show_all" not in st.session_state:
    st.session_state.show_all = False

# -------------------- FUNCTIONS --------------------
def final_gpa(gpa_map):
    return round(
        sum(gpa_map[s] * subjects_dict[s] for s, _ in subjects) / total_credits,
        2
    )

def effort_label(effort):
    if effort <= 6:
        return "Low effort 🙂"
    elif effort <= 14:
        return "Medium effort ⚠️"
    else:
        return "High effort 🔥"

# -------------------- HEADER --------------------
st.markdown("""
<div class="card">
    <h2>🎓 GPA Planner</h2>
    <p class="subtle">Know where you stand. Decide what to improve.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- CURRENT SNAPSHOT --------------------
current_gpa = final_gpa(st.session_state.gpas)

st.markdown(f"""
<div class="card">
    <p class="subtle">Your current GPA</p>
    <div class="hero">{current_gpa}</div>
    <p class="subtle">Based on your current inputs</p>
</div>
""", unsafe_allow_html=True)

# -------------------- GPA INPUT --------------------
st.markdown("""
<div class="card">
    <h3>Adjust your subject scores</h3>
    <p class="subtle">Only change what you’re unsure about</p>
</div>
""", unsafe_allow_html=True)

visible_subjects = subjects[:3] if not st.session_state.show_all else subjects

for sub, credits in visible_subjects:
    st.markdown(f"""
    <div class="card">
        <span class="badge">{credits} credits</span>
        <strong>{sub}</strong>
    """, unsafe_allow_html=True)

    st.session_state.gpas[sub] = st.slider(
        "",
        0, 10,
        st.session_state.gpas[sub],
        key=sub
    )

    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.show_all:
    if st.button("Show all subjects"):
        st.session_state.show_all = True
        st.rerun()

# -------------------- TARGET GPA --------------------
st.markdown("""
<div class="card">
    <h3>Set your target GPA</h3>
    <p class="subtle">Be realistic — effort increases fast</p>
</div>
""", unsafe_allow_html=True)

target = st.slider(
    "Target GPA",
    min_value=0.0,
    max_value=10.0,
    value=max(7.5, current_gpa),
    step=0.1
)

delta = target - current_gpa
if delta <= 0.5:
    st.caption("🟢 Comfortable jump")
elif delta <= 1.2:
    st.caption("🟡 Stretch but doable")
else:
    st.caption("🔴 Aggressive target")

# -------------------- LOCK SUBJECTS --------------------
st.markdown("""
<div class="card">
    <h3>Lock subjects</h3>
    <p class="subtle">Choose subjects you don’t want to push harder</p>
</div>
""", unsafe_allow_html=True)

fixed_subjects = st.multiselect(
    "Locked subjects",
    [s for s, _ in subjects]
)

# -------------------- ACTION --------------------
st.markdown("---")
find = st.button("🚀 Show me the easiest way", use_container_width=True)

if find:
    modifiable = [s for s, _ in subjects if s not in fixed_subjects]
    ranges = [range(st.session_state.gpas[s], 11) for s in modifiable]

    results = []

    for combo in product(*ranges):
        temp = st.session_state.gpas.copy()
        for i, s in enumerate(modifiable):
            temp[s] = combo[i]

        achieved = final_gpa(temp)
        if achieved >= target:
            effort = sum(
                (temp[s] - st.session_state.gpas[s]) * subjects_dict[s]
                for s in modifiable
            )
            results.append((achieved, effort, temp))

    if not results:
        st.error("❌ This target isn’t achievable with current constraints.")
    else:
        results.sort(key=lambda x: x[1])
        st.success("✅ Best achievable paths")

        for i, (ach, eff, dist) in enumerate(results[:2], 1):
            st.markdown(f"""
            <div class="card">
                <span class="badge">Option {i}</span>
                <h3>Final GPA: {ach}</h3>
                <p class="subtle">{effort_label(eff)}</p>
            """, unsafe_allow_html=True)

            for s, _ in subjects:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

            with st.expander("See effort details"):
                st.write(f"Weighted effort score: {eff}")

            st.markdown("</div>", unsafe_allow_html=True)


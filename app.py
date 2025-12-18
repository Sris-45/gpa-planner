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
        # Include both fixed and modifiable subjects
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
        # Sort by extra effort
        results.sort(key=lambda x: x[1])

        st.success(f"Top 3 achievable strategies:")

        # Show top 3 options
        for idx, (ach, eff, dist) in enumerate(results[:3], start=1):
            st.markdown(f"""
            <div class="card">
            <strong>Option {idx}</strong><br>
            Final GPA: {ach} &nbsp;&nbsp; | &nbsp;&nbsp; Extra effort: {eff}
            </div>
            """, unsafe_allow_html=True)

            # Subject-wise changes
            for s, _ in subjects:
                diff = dist[s] - st.session_state.gpas[s]
                if diff > 0:
                    st.write(f"• **{s}** → {dist[s]} (+{diff})")

        # -------------------- Dropdown for all combinations --------------------
        all_options = [f"Option {i+1}: GPA {ach}, Effort {eff}" for i, (ach, eff, _) in enumerate(results)]
        selected_option = st.selectbox("See all possible strategies", all_options)

        # Show details of selected combination
        sel_idx = all_options.index(selected_option)
        _, _, sel_dist = results[sel_idx]
        st.markdown("<div class='card'>Details:</div>", unsafe_allow_html=True)
        for s, _ in subjects:
            diff = sel_dist[s] - st.session_state.gpas[s]
            if diff > 0:
                st.write(f"• **{s}** → {sel_dist[s]} (+{diff})")

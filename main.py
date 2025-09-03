def perform_tax():
    st.session_state["ゴールド"] += 40
    st.session_state["民心"] -= 10
    st.session_state["ターン"] += 1

if st.button("徴税"):
    perform_tax()

st.write(f"ゴールド: {st.session_state['ゴールド']}")
st.write(f"民心: {st.session_state['民心']}")
st.write(f"ターン: {st.session_state['ターン']}")

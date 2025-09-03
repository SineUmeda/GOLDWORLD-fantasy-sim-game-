import streamlit as st
import random

# -------------------------
# 初期パラメータ
# -------------------------
if "turn" not in st.session_state:
    st.session_state.turn = 1
    st.session_state.資金 = 1000
    st.session_state.食料 = 100
    st.session_state.資源 = 50
    st.session_state.国民数 = 10
    st.session_state.建物 = {}

# -------------------------
# 建物リスト
# -------------------------
building_data = {
    "農場": {"base_cost": 200, "food_per_turn": 10},
    "鉱山": {"base_cost": 300, "resource_per_turn": 5},
    "住宅": {"base_cost": 500, "population_per_turn": 2},
    "税務署": {"base_cost": 400, "tax_per_turn": 50},
}

# -------------------------
# ランダムイベント
# -------------------------
positive_events = [
    "村人たちが豊作を祝い、食料が増えた。",
    "資源採掘に成功し、資源が増えた。",
    "思わぬ臨時収入で資金が増えた。",
]

negative_events = [
    "小規模火災が発生し、食料が減った。",
    "鉱山事故で資源が減った。",
    "疫病が流行し、国民数が減った。",
]

def run_event():
    event_type = random.choice(["positive", "negative"])
    if event_type == "positive":
        event = random.choice(positive_events)
        if "食料" in event:
            st.session_state.食料 += 10
        elif "資源" in event:
            st.session_state.資源 += 5
        elif "資金" in event:
            st.session_state.資金 += 100
    else:
        event = random.choice(negative_events)
        if "食料" in event:
            st.session_state.食料 = max(0, st.session_state.食料 - 10)
        elif "資源" in event:
            st.session_state.資源 = max(0, st.session_state.資源 - 5)
        elif "国民数" in event:
            st.session_state.国民数 = max(0, st.session_state.国民数 - 2)
    st.write(f"📜 イベント: {event}")

# -------------------------
# ターン進行
# -------------------------
def next_turn():
    st.session_state.turn += 1
    # 建物効果
    for b, level in st.session_state.建物.items():
        if b == "農場":
            st.session_state.食料 += building_data[b]["food_per_turn"] * level
        elif b == "鉱山":
            st.session_state.資源 += building_data[b]["resource_per_turn"] * level
        elif b == "住宅":
            st.session_state.国民数 += building_data[b]["population_per_turn"] * level
        elif b == "税務署":
            st.session_state.資金 += building_data[b]["tax_per_turn"] * level
    # ランダムイベント
    run_event()

# -------------------------
# UI
# -------------------------
st.title("🏰 シンプル王国シミュレーション")

st.write(f"ターン: {st.session_state.turn}")
st.write(f"資金: {st.session_state.資金} | 食料: {st.session_state.食料} | 資源: {st.session_state.資源} | 国民数: {st.session_state.国民数}")

st.subheader("建物一覧")
for b, info in building_data.items():
    level = st.session_state.建物.get(b, 0)
    cost = info["base_cost"] * (level + 1)
    if st.button(f"{b} (レベル{level}) - 建設/強化 {cost} 資金"):
        if st.session_state.資金 >= cost:
            st.session_state.資金 -= cost
            st.session_state.建物[b] = level + 1
            st.success(f"{b} をレベル {level+1} に建設/強化しました！")
        else:
            st.error("資金が足りません！")

st.button("次のターン", on_click=next_turn)

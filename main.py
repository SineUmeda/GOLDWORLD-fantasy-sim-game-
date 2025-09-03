import streamlit as st
import random

st.set_page_config(page_title="王国シミュレーション", layout="wide")

# 初期化
if "ターン" not in st.session_state:
    st.session_state["ターン"] = 1
if "ゴールド" not in st.session_state:
    st.session_state["ゴールド"] = 100
if "食料" not in st.session_state:
    st.session_state["食料"] = 50
if "民心" not in st.session_state:
    st.session_state["民心"] = 50
if "軍事力" not in st.session_state:
    st.session_state["軍事力"] = 20
if "魔力" not in st.session_state:
    st.session_state["魔力"] = 10
if "建物" not in st.session_state:
    st.session_state["建物"] = {}

# 建物データ
BUILDINGS = {
    "農場": {"食料": 5, "cost": 30},
    "金鉱": {"ゴールド": 10, "cost": 50},
    "兵舎": {"軍事力": 5, "cost": 40},
    "魔法塔": {"魔力": 5, "cost": 60},
}

# 建物効果を毎ターン適用（ゴールドは除外）
for name, level in st.session_state["建物"].items():
    for k, v in BUILDINGS[name].items():
        if k != "cost" and k != "ゴールド":
            st.session_state[k] += v*level

st.title(f"王国シミュレーション（ターン {st.session_state['ターン']}）")

# 資源表示
st.subheader("資源状況")
st.write(f"ゴールド: {st.session_state['ゴールド']}")
st.write(f"食料: {st.session_state['食料']}")
st.write(f"民心: {st.session_state['民心']}")
st.write(f"軍事力: {st.session_state['軍事力']}")
st.write(f"魔力: {st.session_state['魔力']}")

# 行動選択
st.subheader("行動を選択")
def 徴税():
    st.session_state["ゴールド"] += 40
    st.session_state["民心"] -= 10
def 農業投資():
    if st.session_state["ゴールド"] >= 20:
        st.session_state["ゴールド"] -= 20
        st.session_state["食料"] += 30
def 軍備拡張():
    if st.session_state["ゴールド"] >= 25 and st.session_state["食料"] >= 10:
        st.session_state["ゴールド"] -= 25
        st.session_state["食料"] -= 10
        st.session_state["軍事力"] += 20
def 魔法研究():
    if st.session_state["ゴールド"] >= 30:
        st.session_state["ゴールド"] -= 30
        st.session_state["魔力"] += 25
def 冒険者派遣():
    # ランダムイベント発生（簡易）
    effect = random.choice(["ゴールド+20","ゴールド-15","食料+10","民心-10"])
    if effect == "ゴールド+20": st.session_state["ゴールド"] += 20
    if effect == "ゴールド-15": st.session_state["ゴールド"] -= 15
    if effect == "食料+10": st.session_state["食料"] += 10
    if effect == "民心-10": st.session_state["民心"] -= 10
def 王国祭り開催():
    if st.session_state["ゴールド"] >= 30:
        st.session_state["ゴールド"] -= 30
        st.session_state["民心"] += 20

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("1: 徴税"):
        徴税()
        st.session_state["ターン"] += 1
        st.experimental_rerun()
with col2:
    if st.button("2: 農業投資"):
        農業投資()
        st.session_state["ターン"] += 1
        st.experimental_rerun()
with col3:
    if st.button("3: 軍備拡張"):
        軍備拡張()
        st.session_state["ターン"] += 1
        st.experimental_rerun()

col4, col5 = st.columns(2)
with col4:
    if st.button("4: 魔法研究"):
        魔法研究()
        st.session_state["ターン"] += 1
        st.experimental_rerun()
with col5:
    if st.button("5: 冒険者を派遣"):
        冒険者派遣()
        st.session_state["ターン"] += 1
        st.experimental_rerun()

if st.button("6: 王国祭り開催"):
    王国祭り開催()
    st.session_state["ターン"] += 1
    st.experimental_rerun()

# 建物購入
st.subheader("建物購入")
for name, data in BUILDINGS.items():
    cost = data["cost"]
    owned = st.session_state["建物"].get(name, 0)
    if st.button(f"{name} (Lv{owned}) - {cost}ゴールド"):
        if st.session_state["ゴールド"] >= cost:
            st.session_state["ゴールド"] -= cost
            st.session_state["建物"][name] = owned + 1
            st.session_state["ターン"] += 1
            st.experimental_rerun()

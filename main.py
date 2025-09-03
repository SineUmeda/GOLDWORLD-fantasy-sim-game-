import streamlit as st
import random

# 初期化
if 'turn' not in st.session_state:
    st.session_state.turn = 1
if 'ゴールド' not in st.session_state:
    st.session_state.ゴールド = 100
if '食料' not in st.session_state:
    st.session_state.食料 = 50
if '軍事力' not in st.session_state:
    st.session_state.軍事力 = 10
if '魔力' not in st.session_state:
    st.session_state.魔力 = 5
if '民心' not in st.session_state:
    st.session_state.民心 = 50
if '建物' not in st.session_state:
    st.session_state.建物 = {}

# 建物定義
BUILDINGS = {
    "農場": {"ゴールド": -20, "食料": 30, "cost": 20},
    "兵舎": {"ゴールド": -25, "軍事力": 20, "食料": -10, "cost": 40},
    "魔法塔": {"ゴールド": -30, "魔力": 25, "cost": 50},
}

# 行動定義
ACTIONS = {
    "徴税": {"ゴールド": 40, "民心": -10},
    "農業投資": {"食料": 30, "ゴールド": -20},
    "軍備拡張": {"軍事力": 20, "ゴールド": -25, "食料": -10},
    "魔法研究": {"魔力": 25, "ゴールド": -30},
    "冒険者派遣": {},  # ランダムイベント
    "王国祭り開催": {"民心": 20, "ゴールド": -30}
}

# ランダムイベント
EVENTS = [
    {"name": "村で小さな火災が発生", "effect": {"食料": -10}, "rarity":"些細な不運"},
    {"name": "王の財宝を発見", "effect": {"ゴールド": 50}, "rarity":"小さな幸運"},
    {"name": "隣国の襲撃", "effect": {"軍事力": -15, "民心": -10}, "rarity":"災害級"},
    {"name": "神の祝福", "effect": {"民心": 20, "ゴールド": 20}, "rarity":"神の祝福"},
    {"name": "天禍：竜巻", "effect": {"食料": -30, "民心": -20}, "rarity":"天禍"}
]

RARITY_WEIGHTS = {
    "些細な不運": 50,
    "小さな幸運": 40,
    "災害級": 8,
    "神の祝福": 2,
    "天禍": 1
}

st.title("王国シミュレーション")

st.subheader(f"ターン: {st.session_state.turn}")
st.write(f"ゴールド: {st.session_state.ゴールド}")
st.write(f"食料: {st.session_state.食料}")
st.write(f"軍事力: {st.session_state.軍事力}")
st.write(f"魔力: {st.session_state.魔力}")
st.write(f"民心: {st.session_state.民心}")

# 建物表示
st.subheader("建物")
for name, level in st.session_state.建物.items():
    st.write(f"{name} レベル{level}")

# 建物購入・強化
st.subheader("建物購入・強化")
for name, data in BUILDINGS.items():
    level = st.session_state.建物.get(name, 0)
    price = data["cost"] * (level+1)
    if st.button(f"{name}購入/強化 (次のレベル {level+1}, コスト {price} ゴールド)"):
        if st.session_state.ゴールド >= price:
            st.session_state.ゴールド -= price
            st.session_state.建物[name] = level + 1
            st.success(f"{name} をレベル {level+1} にしました！")
        else:
            st.warning("ゴールドが足りません！")

# 行動選択
st.subheader("行動")
action = st.selectbox("行動を選んでください", list(ACTIONS.keys()))
if st.button("実行"):
    if action == "冒険者派遣":
        # ランダムイベント
        event_pool = []
        for e in EVENTS:
            event_pool += [e]*RARITY_WEIGHTS[e["rarity"]]
        event = random.choice(event_pool)
        st.write(f"イベント発生: {event['name']} ({event['rarity']})")
        for k,v in event["effect"].items():
            st.session_state[k] += v
    else:
        for k,v in ACTIONS[action].items():
            st.session_state[k] += v

    # 建物効果
    for name, level in st.session_state.建物.items():
        for k,v in BUILDINGS[name].items():
            if k != "cost":
                st.session_state[k] += v*level

    # ターン進行
    st.session_state.turn += 1

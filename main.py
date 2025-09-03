import streamlit as st
import random

# 初期資源・建物
if "gold" not in st.session_state:
    st.session_state.update({
        "gold": 100,
        "food": 50,
        "military": 20,
        "magic": 10,
        "public": 50,
        "population": 50,
        "turn": 1,
        "buildings": {}
    })

# 建物定義
BUILDINGS = {
    "農場": {"cost": 50, "food": 20},
    "兵舎": {"cost": 70, "military": 15},
    "魔導塔": {"cost": 100, "magic": 25},
    "市場": {"cost": 80, "gold": 30},
    "図書館": {"cost": 90, "magic": 15, "public": 5}
}

# ランダムイベント
EVENTS = [
    {"name": "些細な幸運", "type": "positive", "effect": {"gold": +20}, "rarity": "ノーマル"},
    {"name": "神の祝福", "type": "positive", "effect": {"food": +30}, "rarity": "アンコモン"},
    {"name": "天禍（小規模）", "type": "negative", "effect": {"food": -20, "public": -10}, "rarity": "レア"},
    {"name": "天禍（中規模）", "type": "negative", "effect": {"gold": -30, "military": -10}, "rarity": "エピック"},
    {"name": "天禍（大災害）", "type": "negative", "effect": {"gold": -50, "military": -15, "food": -20}, "rarity": "レジェンド"}
]

RARITY_WEIGHTS = {"ノーマル":50, "アンコモン":30, "レア":15, "エピック":4, "レジェンド":1}

st.title("王国シミュレーションUI版 - フル機能")

# ターン表示
st.subheader(f"ターン {st.session_state.turn}")
st.write(f"ゴールド: {st.session_state.gold} | 食料: {st.session_state.food} | 軍事力: {st.session_state.military} | 魔力: {st.session_state.magic} | 民心: {st.session_state.public} | 国民: {st.session_state.population}")

# 建物UI
st.subheader("建物")
for name, info in BUILDINGS.items():
    level = st.session_state.buildings.get(name, 0)
    cost = info["cost"] * (level + 1)
    effect_desc = ", ".join([f"{k}+{v*(level+1)}" for k,v in info.items() if k!="cost"])
    st.write(f"{name} (Lv {level}) - コスト: {cost} - 効果: {effect_desc}")
    if st.button(f"{name} 購入/強化"):
        if st.session_state.gold >= cost:
            st.session_state.gold -= cost
            st.session_state.buildings[name] = level + 1
            st.success(f"{name}をLv{level+1}に強化しました！")
            st.experimental_rerun()
        else:
            st.error("ゴールドが足りません！")

# 行動選択
st.subheader("行動を選んでください")
actions = {
    "徴税": {"gold": 40, "public": -10},
    "農業投資": {"food":30, "gold":-20},
    "軍備拡張": {"military":20, "gold":-25, "food":-10},
    "魔法研究": {"magic":25, "gold":-30},
    "冒険者派遣": "event",
    "王国祭り": {"public":20, "gold":-30}
}
action = st.selectbox("行動", list(actions.keys()))

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
        for k,v in actions[action].items():
            st.session_state[k] += v

    # 建物効果適用
    for name, level in st.session_state.buildings.items():
        for k,v in BUILDINGS[name].items():
            if k != "cost":
                st.session_state[k] += v*level

    st.session_state.turn += 1
    st.experimental_rerun()

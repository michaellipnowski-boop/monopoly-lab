import streamlit as st
import random

# --- 1. DATA CONSTANTS ---
COLOR_MAP = {
    "Brown": "#955436", "Light Blue": "#AAE0FA", "Pink": "#D93A96", "Orange": "#F7941D",
    "Red": "#ED1B24", "Yellow": "#FEF200", "Green": "#1FB25A", "Dark Blue": "#0072BB",
    "Railroad": "#333333", "Utility": "#999999", "Action": "#FFFFFF", "Tax": "#D3D3D3", "Safe": "#FFFFFF"
}

PROPERTIES = {
    0: {"name": "GO", "type": "Safe"},
    1: {"name": "Mediterranean Avenue", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    2: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    3: {"name": "Baltic Avenue", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    7: {"name": "Chance", "type": "Action", "deck": "chance"},
    8: {"name": "Vermont Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Avenue", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    10: {"name": "Jail / Just Visiting", "type": "Safe"},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    13: {"name": "States Avenue", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Avenue", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900]},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    17: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    18: {"name": "Tennessee Avenue", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "New York Avenue", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000]},
    20: {"name": "Free Parking", "type": "Safe"},
    21: {"name": "Kentucky Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    22: {"name": "Chance", "type": "Action", "deck": "chance"},
    23: {"name": "Indiana Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois Avenue", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100]},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    26: {"name": "Atlantic Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    30: {"name": "Go To Jail", "type": "Action"},
    31: {"name": "Pacific Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    33: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    34: {"name": "Pennsylvania Avenue", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    36: {"name": "Chance", "type": "Action", "deck": "chance"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

CHANCE_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0}, {"text": "Advance to Illinois", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles", "effect": "move", "pos": 11}, {"text": "Bank pays $50", "effect": "cash", "amt": 50},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3}, {"text": "Go to Jail", "effect": "jail"},
    {"text": "Repairs: $25/h, $100/H", "effect": "repairs", "h": 25, "H": 100}, {"text": "Speeding fine $15", "effect": "cash", "amt": -15}
]

CHEST_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0}, {"text": "Bank error $200", "effect": "cash", "amt": 200},
    {"text": "Doctor fee $50", "effect": "cash", "amt": -50}, {"text": "Go to Jail", "effect": "jail"},
    {"text": "Inherit $100", "effect": "cash", "amt": 100}, {"text": "Birthday $10 each", "effect": "birthday", "amt": 10}
]

# --- 2. LOGIC GROUPS ---
COLOR_GROUPS = {}
RAILROADS = [5, 15, 25, 35]
UTILITIES = [12, 28]
for pid, info in PROPERTIES.items():
    if info.get('type') == "Street":
        COLOR_GROUPS.setdefault(info['color'], []).append(pid)

# --- 3. SESSION STATE ---
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if "rent" in PROPERTIES[pid] or PROPERTIES[pid].get("type") in ["Railroad", "Utility"]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.heat_map = [0] * 40
    st.session_state.current_p = 0
    st.session_state.last_move = "Ready to start."

def reset_lab():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# --- 4. ENGINE FUNCTIONS ---
def get_rent(pid, roll):
    owner = st.session_state.ownership[pid]
    info = PROPERTIES[pid]
    if info['type'] == "Street":
        h = st.session_state.houses[pid]
        base = info['rent'][h]
        if h == 0 and all(st.session_state.ownership[g] == owner for g in COLOR_GROUPS[info['color']]):
            return base * 2
        return base
    elif info['type'] == "Railroad":
        count = sum(1 for r in RAILROADS if st.session_state.ownership[r] == owner)
        return info['rent'][count-1]
    elif info['type'] == "Utility":
        count = sum(1 for u in UTILITIES if st.session_state.ownership[u] == owner)
        return (4 if count == 1 else 10) * roll
    return 0

def run_turn(silent=False):
    p = st.session_state.players[st.session_state.current_p]
    if p['cash'] < 0: 
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return

    roll = random.randint(1, 6) + random.randint(1, 6)
    p['pos'] = (p['pos'] + roll) % 40
    st.session_state.heat_map[p['pos']] += 1
    
    sq = PROPERTIES[p['pos']]
    if sq['type'] in ["Street", "Railroad", "Utility"]:
        owner = st.session_state.ownership.get(p['pos'], "Bank")
        if owner != "Bank" and owner != p['name']:
            rent = get_rent(p['pos'], roll)
            p['cash'] -= rent
            for op in st.session_state.players:
                if op['name'] == owner: op['cash'] += rent
    
    if not silent: st.session_state.last_move = f"{p['name']} landed on {sq['name']}."
    st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)

# --- 5. UI COMPONENTS ---
def draw_graphical_board():
    markers = [""] * 40
    for p in st.session_state.players: markers[p['pos']] += f"[{p['name'][0]}]"
    
    top = list(range(20, 31))
    bottom = list(range(10, -1, -1))
    
    cols = st.columns(11)
    for i, cell in enumerate(top):
        sq = PROPERTIES[cell]
        bg = COLOR_MAP.get(sq.get('color'), "#eee")
        with cols[i]:
            st.markdown(f"<div style='background:{bg}; height:5px;'></div>", unsafe_allow_html=True)
            st.caption(f"{cell}")
            st.write(markers[cell])

    st.markdown("---")
    cols = st.columns(11)
    for i, cell in enumerate(bottom):
        sq = PROPERTIES[cell]
        bg = COLOR_MAP.get(sq.get('color'), "#eee")
        with cols[i]:
            st.markdown(f"<div style='background:{bg}; height:5px;'></div>", unsafe_allow_html=True)
            st.caption(f"{cell}")
            st.write(markers[cell])

# --- 6. MAIN APP FLOW ---
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    count = st.number_input("Players", 2, 4, 2)
    names = [st.text_input(f"P{i+1} Name", f"Student {i+1}", key=f"in_{i}") for i in range(count)]
    if st.button("Setup Lab"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in names]
        st.session_state.phase = "SETUP"; st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customize Simulation")
    t1, t2 = st.tabs(["Ownership", "Houses"])
    
    with t1:
        for pid, sq in PROPERTIES.items():
            if "rent" in sq or sq['type'] in ["Railroad", "Utility"]:
                cols = st.columns([2, 1, 1, 1])
                cols[0].write(sq['name'])
                for i, p in enumerate(st.session_state.players):
                    is_o = st.session_state.ownership[pid] == p['name']
                    if cols[i+1].button(p['name'][0], key=f"o_{pid}_{i}", type="primary" if is_o else "secondary"):
                        st.session_state.ownership[pid] = "Bank" if is_o else p['name']; st.rerun()

    with t2:
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f"**{color} Group**")
                for pid in pids:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    h = st.session_state.houses[pid]
                    others = [st.session_state.houses[p] for p in pids if p != pid]
                    if c2.button("➖", key=f"dn_{pid}", disabled=not (h > 0 and all(h >= o for o in others))):
                        st.session_state.houses[pid] -= 1; st.rerun()
                    c3.write(h)
                    if c4.button("➕", key=f"up_{pid}", disabled=not (h < 5 and all(h <= o for o in others))):
                        st.session_state.houses[pid] += 1; st.rerun()

    if st.button("Start Live Mode"): st.session_state.phase = "LIVE"; st.rerun()

elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        st.sidebar.metric(p['name'], f"${p['cash']}")
    
    draw_graphical_board()
    
    st.markdown("### ⚡ Control Panel")
    c1, c2 = st.columns(2)
    if c1.button("Next Turn"): run_turn(); st.rerun()
    with c2:
        jump = st.number_input("Jump Turns", 1, 100000, 100)
        if st.button(f"Execute {jump}"):
            for _ in range(jump): run_turn(silent=True)
            st.rerun()
    
    st.info(st.session_state.last_move)
    if st.sidebar.button("RESET"): reset_lab()
    
    with st.expander("📈 Statistical Heatmap"):
        st.bar_chart(st.session_state.heat_map)

import streamlit as st
import random

# --- 1. DATA CONSTANTS ---
COLOR_MAP = {
    "Brown": "#955436", "Light Blue": "#AADEFC", "Pink": "#D93A96", "Orange": "#F7941D",
    "Red": "#ED1B24", "Yellow": "#FEF200", "Green": "#1FB25A", "Dark Blue": "#0072BB",
    "Railroad": "#000000", "Utility": "#717d7e"
}

PROPERTIES = {
    0: {"name": "GO", "type": "Safe"},
    1: {"name": "Mediterranean Avenue", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250], "price": 60, "house_cost": 50},
    2: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    3: {"name": "Baltic Avenue", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450], "price": 60, "house_cost": 50},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    6: {"name": "Oriental Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550], "price": 100, "house_cost": 50},
    7: {"name": "Chance", "type": "Action", "deck": "chance"},
    8: {"name": "Vermont Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550], "price": 100, "house_cost": 50},
    9: {"name": "Connecticut Avenue", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600], "price": 120, "house_cost": 50},
    10: {"name": "Jail / Just Visiting", "type": "Safe"},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750], "price": 140, "house_cost": 100},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "price": 150},
    13: {"name": "States Avenue", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750], "price": 140, "house_cost": 100},
    14: {"name": "Virginia Avenue", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900], "price": 160, "house_cost": 100},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950], "price": 180, "house_cost": 100},
    17: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    18: {"name": "Tennessee Avenue", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950], "price": 180, "house_cost": 100},
    19: {"name": "New York Avenue", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000], "price": 200, "house_cost": 100},
    20: {"name": "Free Parking", "type": "Safe"},
    21: {"name": "Kentucky Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050], "price": 220, "house_cost": 150},
    22: {"name": "Chance", "type": "Action", "deck": "chance"},
    23: {"name": "Indiana Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050], "price": 220, "house_cost": 150},
    24: {"name": "Illinois Avenue", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100], "price": 240, "house_cost": 150},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    26: {"name": "Atlantic Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150], "price": 260, "house_cost": 150},
    27: {"name": "Ventnor Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150], "price": 260, "house_cost": 150},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "price": 150},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200], "price": 280, "house_cost": 150},
    30: {"name": "Go To Jail", "type": "Action"},
    31: {"name": "Pacific Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275], "price": 300, "house_cost": 200},
    32: {"name": "North Carolina Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275], "price": 300, "house_cost": 200},
    33: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    34: {"name": "Pennsylvania Avenue", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400], "price": 320, "house_cost": 200},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    36: {"name": "Chance", "type": "Action", "deck": "chance"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500], "price": 350, "house_cost": 200},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000], "price": 400, "house_cost": 200}
}

# --- 2. SESSION STATE ---
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if "price" in PROPERTIES[pid]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.current_p = 0
    st.session_state.last_log = "Laboratory Ready."
    st.session_state.c_deck = list(range(16))
    st.session_state.ch_deck = list(range(16))

# --- 3. THE PROFESSOR'S JUMP ENGINE ---
def fast_forward(n_steps):
    for _ in range(n_steps):
        run_turn(is_auto=True)

# --- 4. EVEN BUILDING LOGIC ---
def can_build(pid, increase=True):
    info = PROPERTIES[pid]
    owner = st.session_state.ownership[pid]
    color = info['color']
    set_pids = [p for p,d in PROPERTIES.items() if d.get('color') == color]
    # Must own full set
    if not all(st.session_state.ownership[sp] == owner for sp in set_pids): return False
    current = st.session_state.houses[pid]
    others = [st.session_state.houses[sp] for sp in set_pids if sp != pid]
    if increase:
        if current >= 5: return False
        return all(current <= o for o in others)
    else:
        if current <= 0: return False
        return all(current >= o for o in others)

# --- 5. VISUAL BOARD COMPONENT ---
def draw_graphical_board():
    st.write("### 🗺️ Board Visualization")
    board_layout = [
        list(range(20, 31)), # Top
        [19, None, None, None, None, None, None, None, None, None, 31],
        [18, None, None, None, None, None, None, None, None, None, 32],
        [17, None, None, None, None, None, None, None, None, None, 33],
        [16, None, None, None, None, None, None, None, None, None, 34],
        [15, None, None, None, None, None, None, None, None, None, 35],
        [14, None, None, None, None, None, None, None, None, None, 36],
        [13, None, None, None, None, None, None, None, None, None, 37],
        [12, None, None, None, None, None, None, None, None, None, 38],
        [11, None, None, None, None, None, None, None, None, None, 39],
        list(reversed(range(0, 11))) # Bottom
    ]
    for row in board_layout:
        cols = st.columns(11)
        for i, pid in enumerate(row):
            if pid is not None:
                sq = PROPERTIES[pid]
                clr = COLOR_MAP.get(sq.get('color'), "#eee")
                tokens = "".join([p['name'][0] for p in st.session_state.players if p['pos'] == pid])
                cols[i].markdown(f"<div style='background:{clr}; height:40px; border:1px solid #999; text-align:center; font-size:10px;'>{pid}


{tokens}</div>", unsafe_allow_p_safe=True)
            else:
                cols[i].write("")

# --- 6. COLOR-CODED HUD ---
def render_hud():
    st.sidebar.title("📊 Player Stats")
    for p in st.session_state.players:
        with st.sidebar.expander(f"{p['name']} - ${p['cash']}", expanded=True):
            owned = [pid for pid, o in st.session_state.ownership.items() if o == p['name']]
            for clr_name, hex_code in COLOR_MAP.items():
                group = [pid for pid in owned if PROPERTIES[pid].get('color') == clr_name or (clr_name == "Railroad" and PROPERTIES[pid]['type']=="Railroad") or (clr_name == "Utility" and PROPERTIES[pid]['type']=="Utility")]
                if group:
                    st.markdown(f"<div style='border-left: 10px solid {hex_code}; padding-left:5px;'><b>{clr_name}</b></div>", unsafe_allow_html=True)
                    for pid in group:
                        h = st.session_state.houses.get(pid, 0)
                        st.text(f"  {PROPERTIES[pid]['name']} ({h}H)")

# --- 7. MAIN ENGINE (INCLUDES TURN LOGIC) ---

[Rest of engine logic: run_turn, handle_card, render_cash_and_jail as specified previously]
# --- 8. UI ELEMENTS ---
if st.session_state.phase == "LIVE":
    render_hud()
    draw_graphical_board()
    
    st.subheader("Teaching Controls")
    c1, c2 = st.columns(2)
    n_jump = c1.number_input("Jump Moves", 1, 1000000, 100)
    if c2.button(f"Execute {n_jump} Moves"):
        fast_forward(n_jump); st.rerun()
    
    with st.expander("🏗️ Manage Buildings (Even Rule)"):
        for pid, h in st.session_state.houses.items():
            if st.session_state.ownership[pid] != "Bank":
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.write(f"{PROPERTIES[pid]['name']}")
                if col2.button("-", key=f"m_{pid}", disabled=not can_build(pid, False)):
                    st.session_state.houses[pid] -= 1; st.rerun()
                if col3.button("+", key=f"p_{pid}", disabled=not can_build(pid, True)):
                    st.session_state.houses[pid] += 1; st.rerun()

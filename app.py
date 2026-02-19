import streamlit as st
import random

#Complete Color Mapping for all square types
COLOR_MAP = {
    "Brown": "#955436", "Light Blue": "#AAE0FA", "Pink": "#D93A96", "Orange": "#F7941D",
    "Red": "#ED1B24", "Yellow": "#FEF200", "Green": "#1FB25A", "Dark Blue": "#0072BB",
    "Railroad": "#000000", "Utility": "#808080", "Action": "#FFFFFF", "Tax": "#D3D3D3", "Safe": "#FFFFFF"
}

#Complete Property and Square Data
PROPERTIES = {
    0: {"name": "GO", "type": "Safe"},
    1: {"name": "Med. Ave", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    2: {"name": "Chest", "type": "Action", "deck": "chest"},
    3: {"name": "Baltic Ave", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading RR", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    7: {"name": "Chance", "type": "Action", "deck": "chance"},
    8: {"name": "Vermont Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Conn. Ave", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    10: {"name": "Jail", "type": "Safe"},
    11: {"name": "St. Charles", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    12: {"name": "Electric Co", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    13: {"name": "States Ave", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Ave", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900]},
    15: {"name": "Penn. RR", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    16: {"name": "St. James", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    17: {"name": "Chest", "type": "Action", "deck": "chest"},
    18: {"name": "Tenn. Ave", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "NY Ave", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000]},
    20: {"name": "Free Parking", "type": "Safe"},
    21: {"name": "Kentucky", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    22: {"name": "Chance", "type": "Action", "deck": "chance"},
    23: {"name": "Indiana", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100]},
    25: {"name": "B. & O. RR", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    26: {"name": "Atlantic", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    29: {"name": "Marvin Gard.", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    30: {"name": "Go To Jail", "type": "Action"},
    31: {"name": "Pacific", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "N. Carolina", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    33: {"name": "Chest", "type": "Action", "deck": "chest"},
    34: {"name": "Penn. Ave", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    36: {"name": "Chance", "type": "Action", "deck": "chance"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

#16-card Decks
CHANCE_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Advance to Illinois Ave", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles Place", "effect": "move", "pos": 11},
    {"text": "Advance to nearest Utility", "effect": "move_nearest_util"},
    {"text": "Advance to nearest Railroad", "effect": "move_nearest_rr"},
    {"text": "Bank pays dividend $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "noop"},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "General repairs: $25/house, $100/hotel", "effect": "repairs", "h": 25, "H": 100},
    {"text": "Speeding fine $15", "effect": "cash", "amt": -15},
    {"text": "Trip to Reading RR", "effect": "move", "pos": 5},
    {"text": "Advance to Boardwalk", "effect": "move", "pos": 39},
    {"text": "Elected Chairman. Pay each player $50", "effect": "birthday", "amt": -50},
    {"text": "Building loan matures. Collect $150", "effect": "cash", "amt": 150},
    {"text": "Crossword competition prize. Collect $100", "effect": "cash", "amt": 100}
]
CHEST_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Bank error $200", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee. Pay $50", "effect": "cash", "amt": -50},
    {"text": "From sale of stock get $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "noop"},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "Holiday fund matures. Receive $100", "effect": "cash", "amt": 100},
    {"text": "Income tax refund. Collect $20", "effect": "cash", "amt": 20},
    {"text": "Birthday. Collect $10 from everyone", "effect": "birthday", "amt": 10},
    {"text": "Life insurance matures. Collect $100", "effect": "cash", "amt": 100},
    {"text": "Hospital Fees. Pay $100", "effect": "cash", "amt": -100},
    {"text": "School fees. Pay $50", "effect": "cash", "amt": -50},
    {"text": "Consultancy fee. Collect $25", "effect": "cash", "amt": 25},
    {"text": "Street repairs: $40/house, $115/hotel", "effect": "repairs", "h": 40, "H": 115},
    {"text": "Beauty contest prize. Collect $10", "effect": "cash", "amt": 10},
    {"text": "You inherit $100", "effect": "cash", "amt": 100}
]

#Logic Groups
COLOR_GROUPS = {}
RAILROADS, UTILITIES = [], []
for pid, info in PROPERTIES.items():
    if info.get('type') == "Street":
        COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info.get('type') == "Railroad":
        RAILROADS.append(pid)
    elif info.get('type') == "Utility":
        UTILITIES.append(pid)

#Session State Persistence
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.p_count = 2
    st.session_state.p_names = ["Student A", "Student B"]
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if "rent" in PROPERTIES[pid] or PROPERTIES[pid].get("type") in ["Railroad", "Utility"]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.last_move = ""
    st.session_state.turn_count = 0
    st.session_state.current_p = 0
    c = list(range(16)); random.shuffle(c); st.session_state.c_deck_idx = c
    ch = list(range(16)); random.shuffle(ch); st.session_state.ch_deck_idx = ch

def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    owner = st.session_state.ownership[pid]
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

def draw_card(p, deck_type):
    if deck_type == "chance":
        idx = st.session_state.c_deck_idx.pop(0)
        st.session_state.c_deck_idx.append(idx)
        card = CHANCE_DECK[idx]
        name = "Chance"
    else:
        idx = st.session_state.ch_deck_idx.pop(0)
        st.session_state.ch_deck_idx.append(idx)
        card = CHEST_DECK[idx]
        name = "Community Chest"
    
    if card['effect'] == "move":
        p['pos'] = card['pos']
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
    elif card['effect'] == "cash":
        p['cash'] += card['amt']
    elif card['effect'] == "birthday":
        for op in st.session_state.players:
            if op['name'] != p['name']:
                op['cash'] -= card['amt']
                p['cash'] += card['amt']
    elif card['effect'] == "repairs":
        cost = sum((st.session_state.houses[pid]*(card['H'] if st.session_state.houses[pid]==5 else card['h'])) for pid in st.session_state.houses if st.session_state.ownership.get(pid) == p['name'])
        p['cash'] -= cost
    elif card['effect'] == "move_nearest_rr":
        p['pos'] = min([r for r in [5,15,25,35] if r > p['pos']] or [5])
    elif card['effect'] == "move_nearest_util":
        p['pos'] = min([u for u in [12,28] if u > p['pos']] or [12])
    return f"drew {name}: '{card['text']}'"

def run_turn(silent=False):
    p = st.session_state.players[st.session_state.current_p]
    if p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return False
    roll = random.randint(1,6) + random.randint(1,6)
    p['pos'] = (p['pos'] + roll) % 40
    sq = PROPERTIES.get(p['pos'], {"name": "Safe Square", "type": "Safe"})
    msg = f"{p['name']} rolled {roll} -> {sq['name']}. "
    if sq['type'] in ["Street", "Railroad", "Utility"]:
        owner = st.session_state.ownership.get(p['pos'], "Bank")
        if owner != "Bank" and owner != p['name']:
            rent = get_rent(p['pos'], roll)
            p['cash'] -= rent
            for op in st.session_state.players:
                if op['name'] == owner:
                    op['cash'] += rent
            msg += f"Paid ${rent} rent."
    elif sq['type'] == "Tax":
        tax = sq.get('cost', 100)
        p['cash'] -= tax
        msg += f"Paid ${tax} tax."
    elif sq['type'] == "Action":
        if p['pos'] == 30:
            p['pos'] = 10
            msg += "Go To Jail!"
        else:
            msg += draw_card(p, sq.get('deck', 'chance'))
    elif p['pos'] == 0:
        p['cash'] += 200
        msg += "Passed GO +$200."
    
    if not silent:
        st.session_state.last_move = msg
    st.session_state.turn_count += 1
    st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    return p['cash'] < 0

#--- UI PHASE 1: INIT ---
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    st.session_state.p_count = st.number_input("Players", 1, 8, value=st.session_state.p_count)
    while len(st.session_state.p_names) < st.session_state.p_count:
        st.session_state.p_names.append(f"Student {chr(65+len(st.session_state.p_names))}")
    temp_names = []
    for i in range(st.session_state.p_count):
        name = st.text_input(f"P{i+1}", st.session_state.p_names[i], key=f"n_{i}")
        temp_names.append(name)
    if st.button("Continue"):
        st.session_state.p_names = temp_names
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in temp_names]
        st.session_state.phase = "CHOICE"
        st.rerun()

#--- UI PHASE 2: CHOICE ---
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Select")
    c1, c2 = st.columns(2)
    if c1.button("Standard Simulation"):
        st.session_state.phase = "LIVE"
        st.rerun()
    if c2.button("Customization"):
        st.session_state.phase = "SETUP"
        st.rerun()
    if st.button("← Back to Players"):
        st.session_state.phase = "INIT"
        st.rerun()

#--- UI PHASE 3: SETUP ---
elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customization")
    t1, t2, t3 = st.tabs(["Properties Owned", "Houses Built", "Cash"])
    player_names = [p['name'] for p in st.session_state.players]

    with t1:
        def render_ownership_row(pid, label, color):
            st.markdown(f'<div style="background:{color}; padding:2px; border-radius:4px; margin-top:5px;"></div>', unsafe_allow_html=True)
            cols = st.columns([2] + [1]*len(player_names))
            cols[0].write(label)
            for i, p_name in enumerate(player_names):
                is_owner = (st.session_state.ownership[pid] == p_name)
                if cols[i+1].button(p_name, key=f"b_{pid}_{p_name}", type="primary" if is_owner else "secondary"):
                    st.session_state.ownership[pid] = "Bank" if is_owner else p_name
                    st.rerun()

        for color, pids in COLOR_GROUPS.items():
            for pid in pids:
                render_ownership_row(pid, PROPERTIES[pid]['name'], COLOR_MAP[color])
        for pid in RAILROADS:
            render_ownership_row(pid, PROPERTIES[pid]['name'], "#000")
        for pid in UTILITIES:
            render_ownership_row(pid, PROPERTIES[pid]['name'], "#808080")

    with t2:
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.write(f"{color} ({owners[0]})")
                for pid in pids:
                    h_counts = [st.session_state.houses[p] for p in pids]
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    if c2.button("➖", key=f"m_{pid}", disabled=st.session_state.houses[pid]==0 or st.session_state.houses[pid]<max(h_counts)):
                        st.session_state.houses[pid]-=1
                        st.rerun()
                    c2.write(f"{st.session_state.houses[pid]}")
                    if c3.button("➕", key=f"p_{pid}", disabled=st.session_state.houses[pid]==5 or st.session_state.houses[pid]>min(h_counts)):
                        st.session_state.houses[pid]+=1
                        st.rerun()

    with t3:
        for i, p in enumerate(st.session_state.players):
            p['cash'] = st.number_input(f"{p['name']} ($)", value=int(p['cash']), key=f"c_{i}")

    sc1, sc2 = st.columns([1,4])
    if sc1.button("← Back"):
        st.session_state.phase = "CHOICE"
        st.rerun()
    if sc2.button("🚀 Start"):
        st.session_state.phase = "LIVE"
        st.rerun()

#--- UI PHASE 4: LIVE ---
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    st.markdown(f'<span style="color:{COLOR_MAP[color]}">■</span> <b>{color}</b>', unsafe_allow_html=True)
                    st.write(", ".join([f"{PROPERTIES[pid]['name']} ({st.session_state.houses[pid]}🏠)" for pid in owned]))
    
    st.write("### 🗺️ Board Position")
    board_markers = [""] * 40
    for p in st.session_state.players:
        init = "".join([n[0] for n in p['name'].split()])
        board_markers[p['pos']] += f"[{init}]"

    # Define the 11x11 Grid coordinates for a Monopoly board
    top_row = list(range(20, 31))
    right_col = list(range(31, 40))
    bottom_row = list(range(10, -1, -1))
    left_col = list(range(19, 10, -1))

    # Construct the rows for rendering
    grid_rows = [top_row]
    for i in range(9):
        grid_rows.append([left_col[i]] + [""] * 9 + [right_col[i]])
    grid_rows.append(bottom_row)

    # Render Board
    for r in grid_rows:
        cols = st.columns(11)
        for i, cell in enumerate(r):
            if cell != "":
                label = PROPERTIES[cell]['name'][:5]
                color = COLOR_MAP.get(PROPERTIES[cell].get('color'), "#eee")
                html = f'<div style="background:{color}; border:1px solid #ccc; font-size:9px; height:45px; text-align:center; overflow:hidden; color:black;">{label}


<b>{board_markers[cell]}</b></div>'
                cols[i].markdown(html, unsafe_allow_html=True)
            else:
                cols[i].write("")

    st.markdown("---")
    lc1, lc2 = st.columns([1, 2])
    if lc1.button("Next Turn"):
        run_turn()
        st.rerun()
    with lc2:
        jump = st.number_input("Jump", 1, 1000000, 100, label_visibility="collapsed")
        if st.button(f"Jump {jump}"):
            st.session_state.last_move = f"Simulated {jump} turns."
            for _ in range(jump):
                if run_turn(silent=True):
                    break
            st.rerun()
    
    if st.session_state.last_move:
        st.info(st.session_state.last_move)
    if st.sidebar.button("RESET"):
        reset_lab()

# END OF CODE

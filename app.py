import streamlit as st
import random

#--- DATA CONSTANTS ---
COLOR_MAP = {
    "Brown": "#955436", "Light Blue": "#AAE0FA", "Pink": "#D93A96", "Orange": "#F7941D",
    "Red": "#ED1B24", "Yellow": "#FEF200", "Green": "#1FB25A", "Dark Blue": "#0072BB",
    "Railroad": "#000000", "Utility": "#808080", "Action": "#FFFFFF", "Tax": "#D3D3D3", "Safe": "#FFFFFF"
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

#--- DECKS ---
CHANCE_DECK = [
    {"text": "Advance to GO (Collect $200)", "effect": "move", "pos": 0},
    {"text": "Advance to Illinois Avenue", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles Place", "effect": "move", "pos": 11},
    {"text": "Advance to nearest Utility", "effect": "move_nearest_util"},
    {"text": "Advance to nearest Railroad", "effect": "move_nearest_rr"},
    {"text": "Bank pays dividend $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "General repairs: $25/house, $100/hotel", "effect": "repairs", "h": 25, "H": 100},
    {"text": "Speeding fine $15", "effect": "cash", "amt": -15},
    {"text": "Trip to Reading Railroad", "effect": "move", "pos": 5},
    {"text": "Advance to Boardwalk", "effect": "move", "pos": 39},
    {"text": "Elected Chairman. Pay each player $50", "effect": "birthday", "amt": -50},
    {"text": "Building loan matures. Collect $150", "effect": "cash", "amt": 150},
    {"text": "Crossword competition prize. Collect $100", "effect": "cash", "amt": 100}
]

CHEST_DECK = [
    {"text": "Advance to GO (Collect $200)", "effect": "move", "pos": 0},
    {"text": "Bank error in your favor. Collect $200", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee. Pay $50", "effect": "cash", "amt": -50},
    {"text": "From sale of stock get $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "Holiday fund matures. Receive $100", "effect": "cash", "amt": 100},
    {"text": "Income tax refund. Collect $20", "effect": "cash", "amt": 20},
    {"text": "It is your birthday. Collect $10 from everyone", "effect": "birthday", "amt": 10},
    {"text": "Life insurance matures. Collect $100", "effect": "cash", "amt": 100},
    {"text": "Hospital Fees. Pay $100", "effect": "cash", "amt": -100},
    {"text": "School fees. Pay $50", "effect": "cash", "amt": -50},
    {"text": "Consultancy fee. Collect $25", "effect": "cash", "amt": 25},
    {"text": "Street repairs: $40/house, $115/hotel", "effect": "repairs", "h": 40, "H": 115},
    {"text": "Beauty contest prize. Collect $10", "effect": "cash", "amt": 10},
    {"text": "You inherit $100", "effect": "cash", "amt": 100}
]

#--- LOGIC GROUPS ---
COLOR_GROUPS = {}
RAILROADS = []
UTILITIES = []
for pid, info in PROPERTIES.items():
    if info.get('type') == "Street":
        COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info.get('type') == "Railroad":
        RAILROADS.append(pid)
    elif info.get('type') == "Utility":
        UTILITIES.append(pid)

#--- SESSION STATE ---
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
    st.session_state.double_count = 0
    # Decks are now lists of indices available to be drawn
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)

def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

#--- HELPER LOGIC ---
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
        card = CHANCE_DECK[idx]
        name = "Chance"
    else:
        idx = st.session_state.ch_deck_idx.pop(0)
        card = CHEST_DECK[idx]
        name = "Community Chest"
    
    if card['effect'] == "move":
        p['pos'] = card['pos']
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "cash":
        p['cash'] += card['amt']
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "birthday":
        for op in st.session_state.players:
            if op['name'] != p['name']:
                op['cash'] -= card['amt']
                p['cash'] += card['amt']
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "repairs":
        cost = sum((st.session_state.houses[pid]*(card['H'] if st.session_state.houses[pid]==5 else card['h'])) for pid in st.session_state.houses if st.session_state.ownership.get(pid) == p['name'])
        p['cash'] -= cost
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "move_nearest_rr":
        p['pos'] = min([r for r in [5,15,25,35] if r > p['pos']] or [5])
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "move_nearest_util":
        p['pos'] = min([u for u in [12,28] if u > p['pos']] or [12])
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
    elif card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        # NOTE: Card is NOT added back to index list while held by player
    return f"drew {name}: '{card['text']}'"

def run_turn(silent=False):
    p = st.session_state.players[st.session_state.current_p]
    
    if p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        st.session_state.double_count = 0
        return False

    # Dice Roll
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    roll_sum = d1 + d2
    is_double = (d1 == d2)
    
    if is_double:
        st.session_state.double_count += 1
    else:
        st.session_state.double_count = 0

    # Speeding Rule
    if st.session_state.double_count >= 3:
        p['pos'] = 10
        msg = f"{p['name']} rolled doubles for the 3rd time! Go to Jail! 🚔"
        st.session_state.double_count = 0
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        p['pos'] = (p['pos'] + roll_sum) % 40
        sq = PROPERTIES.get(p['pos'])
        double_text = " (DOUBLES!)" if is_double else ""
        msg = f"{p['name']} rolled {d1}+{d2}={roll_sum}{double_text} -> {sq['name']}. "
        
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership.get(p['pos'], "Bank")
            if owner != "Bank" and owner != p['name']:
                rent = get_rent(p['pos'], roll_sum)
                p['cash'] -= rent
                for op in st.session_state.players:
                    if op['name'] == owner: op['cash'] += rent
                msg += f"Paid ${rent} rent."
        elif sq['type'] == "Tax":
            tax = sq.get('cost', 100)
            p['cash'] -= tax
            msg += f"Paid ${tax} tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30:
                p['pos'] = 10
                msg += "Go To Jail!"
                st.session_state.double_count = 0
            else:
                msg += draw_card(p, sq.get('deck', 'chance'))
        elif p['pos'] == 0:
            p['cash'] += 200
            msg += "Passed GO +$200."

        if not is_double:
            st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        else:
            msg += " Roll again!"

    if not silent:
        st.session_state.last_move = msg
    st.session_state.turn_count += 1
    return p['cash'] < 0

#--- PHASE 1: INIT ---
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    st.session_state.p_count = st.number_input("How many players?", 1, 8, value=st.session_state.p_count)
    while len(st.session_state.p_names) < st.session_state.p_count:
        st.session_state.p_names.append(f"Student {chr(65+len(st.session_state.p_names))}")
    temp_names = []
    for i in range(st.session_state.p_count):
        name = st.text_input(f"Player {i+1} Name", st.session_state.p_names[i], key=f"n_{i}")
        temp_names.append(name)
    if st.button("Continue to Mode Selection"):
        st.session_state.p_names = temp_names
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0, "goo_cards": []} for n in temp_names]
        st.session_state.phase = "CHOICE"
        st.rerun()

#--- PHASE 2: CHOICE ---
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Select")
    c1, c2 = st.columns(2)
    if c1.button("Standard Simulation"):
        st.session_state.phase = "LIVE"
        st.rerun()
    if c2.button("Customization"):
        st.session_state.phase = "SETUP"
        st.rerun()

#--- PHASE 3: SETUP ---
elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customization")
    t1, t2, t3 = st.tabs(["Properties Owned", "Houses Built", "Cash"])
    p_names = [p['name'] for p in st.session_state.players]

    with t1:
        for color, pids in COLOR_GROUPS.items():
            for pid in pids:
                st.markdown(f'<div style="background:{COLOR_MAP[color]}; height:4px; border-radius:2px;"></div>', unsafe_allow_html=True)
                cols = st.columns([2] + [1]*len(p_names))
                cols[0].write(PROPERTIES[pid]['name'])
                for i, p_n in enumerate(p_names):
                    is_own = (st.session_state.ownership[pid] == p_n)
                    if cols[i+1].button(p_n, key=f"o_{pid}{p_n}", type="primary" if is_own else "secondary"):
                        st.session_state.ownership[pid] = "Bank" if is_own else p_n
                        st.rerun()
        for pid in RAILROADS + UTILITIES:
            st.markdown(f'<div style="background:#000; height:4px; border-radius:2px;"></div>', unsafe_allow_html=True)
            cols = st.columns([2] + [1]*len(p_names))
            cols[0].write(PROPERTIES[pid]['name'])
            for i, p_n in enumerate(p_names):
                is_own = (st.session_state.ownership[pid] == p_n)
                if cols[i+1].button(p_n, key=f"o{pid}_{p_n}", type="primary" if is_own else "secondary"):
                    st.session_state.ownership[pid] = "Bank" if is_own else p_n
                    st.rerun()

    with t2:
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f'<div style="background:{COLOR_MAP[color]}; padding:5px; color:white; font-weight:bold; border-radius:5px;">{color} Group ({owners[0]})</div>', unsafe_allow_html=True)
                for pid in pids:
                    h_counts = [st.session_state.houses[p] for p in pids]
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    if c2.button("➖", key=f"m_{pid}", disabled=st.session_state.houses[pid]==0 or st.session_state.houses[pid]<max(h_counts)):
                        st.session_state.houses[pid]-=1; st.rerun()
                    c2.write(f"{st.session_state.houses[pid]}")
                    if c3.button("➕", key=f"p_{pid}", disabled=st.session_state.houses[pid]==5 or st.session_state.houses[pid]>min(h_counts)):
                        st.session_state.houses[pid]+=1; st.rerun()

    with t3:
        for i, p in enumerate(st.session_state.players):
            p['cash'] = st.number_input(f"Cash for {p['name']}", value=int(p['cash']), step=10, key=f"ci_{i}")

    if st.button("🚀 Start Live Lab"):
        st.session_state.phase = "LIVE"
        st.rerun()

#--- PHASE 4: LIVE ---
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            if p['goo_cards']:
                st.warning(f"🎟️ {len(p['goo_cards'])} Get Out of Jail Free Card(s)")
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    st.markdown(f'<span style="color:{COLOR_MAP[color]}">■</span> <b>{color}</b>', unsafe_allow_html=True)
                    st.write(", ".join([f"{PROPERTIES[pid]['name']} ({st.session_state.houses[pid]}🏠)" for pid in owned]))

    st.write("### 🗺️ Board Position")
    board_markers = [""] * 40
    for p in st.session_state.players:
        initials = "".join([n[0] for n in p['name'].split()])
        board_markers[p['pos']] += f"[{initials}]"

    top_row = list(range(20, 31))
    right_col = list(range(31, 40))
    bottom_row = list(range(10, -1, -1))
    left_col = list(range(19, 10, -1))

    cols_top = st.columns([1] + [1]*11 + [1])
    for i, cell in enumerate(top_row):
        cols_top[i+1].write(board_markers[cell])

    for r_idx in range(11):
        cols = st.columns([1] + [1]*11 + [1])
        if 1 <= r_idx <= 9: cols[0].write(board_markers[left_col[r_idx-1]])
        row_data = top_row if r_idx == 0 else (bottom_row if r_idx == 10 else [left_col[r_idx-1]] + [""]*9 + [right_col[r_idx-1]])
        for c_idx, cell in enumerate(row_data):
            target_col = cols[c_idx + 1]
            if cell != "":
                sq = PROPERTIES[cell]
                bg = COLOR_MAP.get(sq.get('color'), "#eee")
                with target_col.container():
                    st.markdown(f'<div style="background:{bg}; height:10px; border:0.5px solid #000;"></div>', unsafe_allow_html=True)
                    st.caption(sq['name'][:10])
                    if r_idx == 10: st.write(board_markers[cell])
        if 1 <= r_idx <= 9: cols[12].write(board_markers[right_col[r_idx-1]])

    st.markdown("---")
    lc1, lc2 = st.columns([1, 2])
    if lc1.button("Next Turn"):
        run_turn()
        st.rerun()
    with lc2:
        jump_val = st.number_input("Turn Jump", 1, 1000000, 100, label_visibility="collapsed")
        if st.button(f"Jump {jump_val} Turns"):
            for _ in range(jump_val):
                if run_turn(silent=True): break
            st.rerun()
    
    if st.session_state.last_move:
        st.info(st.session_state.last_move)
    if st.sidebar.button("RESET SIMULATION"):
        reset_lab()

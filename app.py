import streamlit as st
import random

# --- DATA CONSTANTS ---
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

# --- DECKS ---
CHANCE_DECK = [
    {"text": "Advance to GO (Collect $200)", "effect": "move", "pos": 0},
    {"text": "Advance to Illinois Avenue", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles Place", "effect": "move", "pos": 11},
    {"text": "Advance to nearest Utility", "effect": "move_nearest_util"},
    {"text": "Advance to nearest Railroad", "effect": "move_nearest_rr"},
    {"text": "Bank pays dividend $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3},
    {"text": "Go to Jail", "effect": "jail"},
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
    {"text": "Go to Jail", "effect": "jail"},
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

# --- LOGIC GROUPS ---
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

# --- SESSION STATE ---
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
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)

def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# --- HELPER LOGIC ---
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
        if count == 1:
            return 4 * roll
        else:
            return 10 * roll
    return 0

def send_to_jail(p):
    p['pos'] = 10
    p['in_jail'] = True
    p['jail_turns'] = 0
    st.session_state.double_count = 0

def draw_card(p, deck_type):
    if deck_type == "chance":
        idx = st.session_state.c_deck_idx.pop(0)
        card = CHANCE_DECK[idx]
        name = "Chance"
    else:
        idx = st.session_state.ch_deck_idx.pop(0)
        card = CHEST_DECK[idx]
        name = "Community Chest"
    
    msg = f"drew {name}: '{card['text']}'"
    
    if card['effect'] == "move":
        old_pos = p['pos']
        p['pos'] = card['pos']
        if p['pos'] < old_pos:
            p['cash'] += 200
    elif card['effect'] == "jail":
        send_to_jail(p)
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
        cost = 0
        for pid in st.session_state.houses:
            if st.session_state.ownership.get(pid) == p['name']:
                h_count = st.session_state.houses[pid]
                if h_count == 5:
                    cost += card['H']
                else:
                    cost += (h_count * card['h'])
        p['cash'] -= cost
    elif card['effect'] == "move_nearest_rr":
        targets = [5, 15, 25, 35]
        p['pos'] = min([r for r in targets if r > p['pos']] or [5])
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        p['pos'] = min([u for u in targets if u > p['pos']] or [12])
    elif card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        return msg
    
    if deck_type == "chance":
        st.session_state.c_deck_idx.append(idx)
    else:
        st.session_state.ch_deck_idx.append(idx)
    return msg

def run_turn(jail_action=None, silent=False):
    p = st.session_state.players[st.session_state.current_p]
    if p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return
    
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    roll_sum = d1 + d2
    is_double = (d1 == d2)
    
    # --- JAIL LOGIC ---
    if p.get('in_jail'):
        p['jail_turns'] += 1
        if jail_action is None:
            if p['goo_cards']:
                jail_action = "Use Card"
            elif p['jail_turns'] >= 3:
                jail_action = "Pay $50"
            else:
                jail_action = "Try Doubles"
        
        if jail_action == "Pay $50":
            p['cash'] -= 50
            p['in_jail'] = False
            if not silent:
                st.session_state.last_move = f"{p['name']} paid $50 to exit Jail."
        elif jail_action == "Use Card":
            card = p['goo_cards'].pop(0)
            if card['deck'] == "chance":
                st.session_state.c_deck_idx.append(card['index'])
            else:
                st.session_state.ch_deck_idx.append(card['index'])
            p['in_jail'] = False
            if not silent:
                st.session_state.last_move = f"{p['name']} used GOOJF card."
        else: # Try Doubles
            if is_double:
                p['in_jail'] = False
                if not silent:
                    st.session_state.last_move = f"{p['name']} rolled doubles and escaped!"
            elif p['jail_turns'] >= 3:
                p['cash'] -= 50
                p['in_jail'] = False
                if not silent:
                    st.session_state.last_move = f"{p['name']} failed 3 times, paid $50."
            else:
                if not silent:
                    st.session_state.last_move = f"{p['name']} failed doubles, stays in Jail."
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                st.session_state.turn_count += 1
                return
    
    # --- MOVEMENT ---
    if is_double and not p.get('in_jail'):
        st.session_state.double_count += 1
    else:
        st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        if not silent:
            st.session_state.last_move = f"{p['name']} rolled 3 doubles! Go to Jail!"
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        old_pos = p['pos']
        p['pos'] = (p['pos'] + roll_sum) % 40
        if p['pos'] < old_pos:
            p['cash'] += 200
        
        sq = PROPERTIES.get(p['pos'])
        msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "
        
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership.get(p['pos'], "Bank")
            if owner != "Bank" and owner != p['name']:
                rent = get_rent(p['pos'], roll_sum)
                p['cash'] -= rent
                for op in st.session_state.players:
                    if op['name'] == owner:
                        op['cash'] += rent
                msg += f"Paid ${rent} rent."
        elif sq['type'] == "Tax":
            p['cash'] -= sq.get('cost', 100)
            msg += f"Paid tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30:
                send_to_jail(p)
                msg += "Go To Jail!"
            else:
                msg += draw_card(p, sq.get('deck', 'chance'))
        
        if not silent:
            st.session_state.last_move = msg
        if not is_double:
            st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    
    st.session_state.turn_count += 1

# --- UI FLOW ---
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    st.session_state.p_count = st.number_input("How many players?", 1, 8, value=st.session_state.p_count)
    temp_names = []
    for i in range(st.session_state.p_count):
        name = st.text_input(f"Player {i+1}", f"Student {chr(65+i)}", key=f"n_{i}")
        temp_names.append(name)
    if st.button("Proceed to Mode Selection"):
        st.session_state.p_names = temp_names
        st.session_state.players = []
        for n in temp_names:
            st.session_state.players.append({"name": n, "cash": 1500, "pos": 0, "goo_cards": [], "in_jail": False, "jail_turns": 0})
        st.session_state.phase = "CHOICE"
        st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customization")
    t1, t2, t3 = st.tabs(["Properties owned", "Houses built", "Cash and jail"])
    p_names = [p['name'] for p in st.session_state.players]
    
    with t1:
        all_ownable = []
        for color, pids in COLOR_GROUPS.items():
            all_ownable.extend(pids)
        all_ownable.extend(RAILROADS)
        all_ownable.extend(UTILITIES)
        for pid in all_ownable:
            sq = PROPERTIES[pid]
            bg = COLOR_MAP.get(sq.get('color'), COLOR_MAP.get(sq['type']))
            st.markdown(f'<div style="background:{bg}; height:4px;"></div>', unsafe_allow_html=True)
            cols = st.columns([2] + [1]*len(p_names))
            cols[0].write(sq['name'])
            for i, p_n in enumerate(p_names):
                is_own = (st.session_state.ownership[pid] == p_n)
                if cols[i+1].button(p_n, key=f"set_o_{pid}{p_n}", type="primary" if is_own else "secondary"):
                    if is_own:
                        st.session_state.ownership[pid] = "Bank"
                    else:
                        st.session_state.ownership[pid] = p_n
                    st.rerun()
    
    with t2:
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f'<div style="background:{COLOR_MAP[color]}; padding:5px; border-radius:3px; color:white;"><b>{color} Group ({owners[0]})</b></div>', unsafe_allow_html=True)
                for pid in pids:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    h = st.session_state.houses[pid]
                    others = [st.session_state.houses[p] for p in pids if p != pid]
                    
                    # Even building logic: can't be more than 1 house apart
                    can_down = h > 0 and all(h >= o for o in others)
                    can_up = h < 5 and all(h <= o for o in others)
                    
                    if c2.button("➖", key=f"hm{pid}", disabled=not can_down):
                        st.session_state.houses[pid] -= 1; st.rerun()
                    c3.write(f"**{h}**")
                    if c4.button("➕", key=f"hp_{pid}", disabled=not can_up):
                        st.session_state.houses[pid] += 1; st.rerun()
            else:
                st.caption(f"_{color}: Group not fully owned by one player._")
    
    with t3:
        for i, p in enumerate(st.session_state.players):
            st.markdown(f"### {p['name']}")
            p['cash'] = st.number_input(f"Cash Amount for {p['name']}", value=int(p['cash']), step=50, key=f"set_c_{i}")
            p['in_jail'] = st.checkbox(f"Is {p['name']} currently in Jail?", value=p['in_jail'], key=f"set_j_{i}")
            
            # GOOJF Logic
            has_ch = any(c['deck'] == "chance" for c in p['goo_cards'])
            has_cc = any(c['deck'] == "chest" for c in p['goo_cards'])
            
            c1, c2 = st.columns(2)
            if c1.checkbox("Has Chance GOOJF Card", value=has_ch, key=f"goojf_ch_{i}"):
                if not has_ch:
                    if 6 in st.session_state.c_deck_idx:
                        st.session_state.c_deck_idx.remove(6)
                        p['goo_cards'].append({"deck": "chance", "index": 6})
            else:
                if has_ch:
                    p['goo_cards'] = [c for c in p['goo_cards'] if c['deck'] != "chance"]
                    if 6 not in st.session_state.c_deck_idx:
                        st.session_state.c_deck_idx.append(6)
            
            if c2.checkbox("Has Community Chest GOOJF Card", value=has_cc, key=f"goojf_cc_{i}"):
                if not has_cc:
                    if 4 in st.session_state.ch_deck_idx:
                        st.session_state.ch_deck_idx.remove(4)
                        p['goo_cards'].append({"deck": "chest", "index": 4})
            else:
                if has_cc:
                    p['goo_cards'] = [c for c in p['goo_cards'] if c['deck'] != "chest"]
                    if 4 not in st.session_state.ch_deck_idx:
                        st.session_state.ch_deck_idx.append(4)
    
    if st.button("Start Live Simulation"):
        st.session_state.phase = "LIVE"
        st.rerun()

elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Selection")
    c1, c2 = st.columns(2)
    if c1.button("Standard Simulation"):
        st.session_state.phase = "LIVE"; st.rerun()
    if c2.button("Customization Setup"):
        st.session_state.phase = "SETUP"; st.rerun()

elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            if p.get('in_jail'): st.error("IN JAIL 🚔")
            if p['goo_cards']: st.success(f"GOOJF Cards: {len(p['goo_cards'])}")
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    st.markdown(f'<span style="color:{COLOR_MAP[color]}">■</span> <b>{color}</b>', unsafe_allow_html=True)
                    st.write(", ".join([f"{PROPERTIES[pid]['name']} ({st.session_state.houses[pid]}🏠)" for pid in owned]))

    board_markers = [""] * 40
    for p in st.session_state.players:
        initials = "".join([n[0] for n in p['name'].split()])
        board_markers[p['pos']] += f"[{initials}]"

    top_row = list(range(20, 31))
    right_col = list(range(31, 40))
    bottom_row = list(range(10, -1, -1))
    left_col = list(range(19, 10, -1))

    cols_t = st.columns([1] + [1]*11 + [1])
    for i, cell in enumerate(top_row): cols_t[i+1].write(board_markers[cell])

    for r in range(11):
        cols = st.columns([1] + [1]*11 + [1])
        if 1 <= r <= 9: cols[0].write(board_markers[left_col[r-1]])
        
        row_data = []
        if r == 0: row_data = top_row
        elif r == 10: row_data = bottom_row
        else: row_data = [left_col[r-1]] + [""]*9 + [right_col[r-1]]
        
        for c, cell in enumerate(row_data):
            if cell != "":
                sq = PROPERTIES[cell]
                bg = COLOR_MAP.get(sq.get('color'), COLOR_MAP.get(sq.get('type'), "#eee"))
                with cols[c+1].container():
                    st.markdown(f'<div style="background:{bg}; height:8px;"></div>', unsafe_allow_html=True)
                    st.caption(sq['name'][:8])
                    if r == 10: st.write(board_markers[cell])
        
        if 1 <= r <= 9: cols[12].write(board_markers[right_col[r-1]])

    st.markdown("---")
    curr_p = st.session_state.players[st.session_state.current_p]
    st.write(f"👉 Current Turn: {curr_p['name']}")
    
    if curr_p.get('in_jail'):
        c1, c2, c3 = st.columns(3)
        if c1.button("Roll for Doubles"): run_turn(jail_action="Try Doubles"); st.rerun()
        if c2.button("Pay $50"): run_turn(jail_action="Pay $50"); st.rerun()
        if c3.button("Use GOOJF Card", disabled=not curr_p['goo_cards']): run_turn(jail_action="Use Card"); st.rerun()
    else:
        lc1, lc2 = st.columns([1, 2])
        if lc1.button("Next Turn", use_container_width=True): run_turn(); st.rerun()
        with lc2:
            j_val = st.number_input("Turns to Jump", 1, 10000, 100, label_visibility="collapsed")
            if st.button(f"Jump {j_val} Turns", use_container_width=True):
                for _ in range(j_val): run_turn(silent=True)
                st.rerun()

    if st.session_state.last_move: st.info(st.session_state.last_move)
    if st.sidebar.button("RESET SIMULATION"): reset_lab()

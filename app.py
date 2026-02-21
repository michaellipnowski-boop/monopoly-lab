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

# --- SESSION STATE INITIALIZATION ---
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
    st.session_state.jackpot = 0
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)
    st.session_state.rules = {
        "allow_debt": True, 
        "double_go": False, 
        "fp_jackpot": False, 
        "shuffle_mode": "Cyclic"
    }

def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# --- HELPER LOGIC ---
def charge_player(p, amt):
    p['cash'] -= amt
    if st.session_state.rules["fp_jackpot"] and amt > 0:
        st.session_state.jackpot += amt

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    owner = st.session_state.ownership[pid]
    if info['type'] == "Street":
        h = st.session_state.houses[pid]
        base = info['rent'][h]
        # Monopoly bonus
        if h == 0 and all(st.session_state.ownership[g] == owner for g in COLOR_GROUPS[info['color']]):
            return base * 2
        return base
    elif info['type'] == "Railroad":
        count = sum(1 for r in RAILROADS if st.session_state.ownership[r] == owner)
        return info['rent'][count-1]
    elif info['type'] == "Utility":
        count = sum(1 for u in UTILITIES if st.session_state.ownership[u] == owner)
        return (4 * roll) if count == 1 else (10 * roll)
    return 0

def send_to_jail(p):
    p['pos'] = 10
    p['in_jail'] = True
    p['jail_turns'] = 0
    st.session_state.double_count = 0

# --- THE REPAIRED DRAW_CARD (Surgical Fix) ---
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
    
    # Check for Get Out of Jail Free first
    if card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        return msg 
    
    # Movement logic with Pass GO safety
    if card['effect'] == "move":
        old_pos = p['pos']
        p['pos'] = card['pos']
        if p['pos'] < old_pos or p['pos'] == 0: 
            p['cash'] += 200
            
    elif card['effect'] == "jail":
        send_to_jail(p)
        
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
        
    elif card['effect'] == "cash":
        if card['amt'] < 0: 
            charge_player(p, abs(card['amt']))
        else: 
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
                cost += card['H'] if h_count == 5 else (h_count * card['h'])
        charge_player(p, cost)
        
    elif card['effect'] == "move_nearest_rr":
        targets = [5, 15, 25, 35]
        old_pos = p['pos']
        p['pos'] = min([r for r in targets if r > p['pos']] or [5])
        if p['pos'] < old_pos: p['cash'] += 200
        
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        old_pos = p['pos']
        p['pos'] = min([u for u in targets if u > p['pos']] or [12])
        if p['pos'] < old_pos: p['cash'] += 200
    
    # Shuffle mode handling
    if st.session_state.rules["shuffle_mode"] == "True Random":
        if deck_type == "chance": 
            st.session_state.c_deck_idx.append(idx)
            random.shuffle(st.session_state.c_deck_idx)
        else: 
            st.session_state.ch_deck_idx.append(idx)
            random.shuffle(st.session_state.ch_deck_idx)
    else:
        if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
        else: st.session_state.ch_deck_idx.append(idx)
        
    return msg

def run_turn(jail_action=None, silent=False):
    p = st.session_state.players[st.session_state.current_p]
    
    # Skip bankrupt players if debt isn't allowed
    if not st.session_state.rules["allow_debt"] and p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return
    
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    roll_sum, is_double = d1 + d2, (d1 == d2)
    
    # Jail Logic
    if p.get('in_jail'):
        if jail_action is None:
            if p['goo_cards']: jail_action = "Use Card"
            elif p['jail_turns'] >= 2: jail_action = "Pay $50"
            else: jail_action = "Try Doubles"
        
        if jail_action == "Pay $50":
            charge_player(p, 50); p['in_jail'] = False
            if not silent: st.session_state.last_move = f"{p['name']} paid $50 to exit Jail."
        elif jail_action == "Use Card":
            card = p['goo_cards'].pop(0)
            if card['deck'] == "chance": st.session_state.c_deck_idx.append(card['index'])
            else: st.session_state.ch_deck_idx.append(card['index'])
            p['in_jail'] = False
            if not silent: st.session_state.last_move = f"{p['name']} used GOOJF card."
        else: 
            if is_double:
                p['in_jail'] = False
                if not silent: st.session_state.last_move = f"{p['name']} rolled doubles and escaped!"
            elif p['jail_turns'] >= 2:
                charge_player(p, 50); p['in_jail'] = False
                if not silent: st.session_state.last_move = f"{p['name']} failed 3rd double, paid $50."
            else:
                p['jail_turns'] += 1
                if not silent: st.session_state.last_move = f"{p['name']} failed doubles."
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                st.session_state.turn_count += 1
                return

    # Normal Movement
    if is_double and not p.get('in_jail'): st.session_state.double_count += 1
    else: st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        if not silent: st.session_state.last_move = f"{p['name']} rolled 3 doubles! To Jail!"
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        old_pos = p['pos']
        p['pos'] = (p['pos'] + roll_sum) % 40
        
        # Standard Pass GO
        if p['pos'] < old_pos:
            p['cash'] += 400 if (st.session_state.rules["double_go"] and p['pos'] == 0) else 200
        
        sq = PROPERTIES.get(p['pos'])
        msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "
        
        # Landings
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership.get(p['pos'], "Bank")
            if owner != "Bank" and owner != p['name']:
                rent = get_rent(p['pos'], roll_sum)
                p['cash'] -= rent
                for op in st.session_state.players:
                    if op['name'] == owner: op['cash'] += rent
                msg += f"Paid ${rent} rent."
        elif sq['type'] == "Tax":
            charge_player(p, sq.get('cost', 100))
            msg += f"Paid tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30: 
                send_to_jail(p); msg += "Go To Jail!"
            else: 
                msg += draw_card(p, sq.get('deck', 'chance'))
        elif sq['name'] == "Free Parking" and st.session_state.rules["fp_jackpot"]:
            if st.session_state.jackpot > 0:
                p['cash'] += st.session_state.jackpot
                msg += f"Collected ${st.session_state.jackpot} Jackpot!"
                st.session_state.jackpot = 0
        
        if not silent: st.session_state.last_move = msg
        if not is_double: st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    st.session_state.turn_count += 1

# --- UI PHASES (FULL INTEGRITY RESTORED) ---

if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    st.markdown("---")
    st.session_state.p_count = st.number_input("How many players?", 1, 8, value=st.session_state.p_count)
    temp_names = []
    for i in range(st.session_state.p_count):
        name = st.text_input(f"Player {i+1} Name", f"Student {chr(65+i)}", key=f"init_n_{i}")
        temp_names.append(name)
    
    if st.button("Proceed to Global Rules", use_container_width=True):
        st.session_state.p_names = temp_names
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0, "goo_cards": [], "in_jail": False, "jail_turns": 0} for n in temp_names]
        st.session_state.phase = "RULES"
        st.rerun()

elif st.session_state.phase == "RULES":
    st.title("⚙️ Global Game Rules")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.rules["allow_debt"] = st.toggle("Allow Negative Balance (Bankrupt Logic)", value=st.session_state.rules["allow_debt"])
        st.session_state.rules["double_go"] = st.toggle("Landing on GO pays $400", value=st.session_state.rules["double_go"])
    with c2:
        st.session_state.rules["fp_jackpot"] = st.toggle("Free Parking Jackpot (Taxes/Fines)", value=st.session_state.rules["fp_jackpot"])
        st.session_state.rules["shuffle_mode"] = st.radio("Shuffle Mode", ["Cyclic", "True Random"])
    
    if st.button("Proceed to Mode Selection", use_container_width=True):
        st.session_state.phase = "CHOICE"
        st.rerun()

elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Selection")
    st.markdown("---")
    st.write("Would you like to start a fresh game or customize the board state (e.g., set specific property owners for a case study)?")
    c1, c2 = st.columns(2)
    if c1.button("Standard Simulation (All Bank)", use_container_width=True):
        st.session_state.phase = "LIVE"
        st.rerun()
    if c2.button("Customization Setup", use_container_width=True):
        st.session_state.phase = "SETUP"
        st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customization Mode")
    st.markdown("---")
    t1, t2, t3 = st.tabs(["Property Ownership", "Building Development", "Player Status"])
    
    p_names = [p['name'] for p in st.session_state.players]

    with t1:
        st.subheader("Assign Properties")
        # List properties by color groups
        for color, pids in COLOR_GROUPS.items():
            st.markdown(f"**{color} Group**")
            for pid in pids:
                sq = PROPERTIES[pid]
                cols = st.columns([2] + [1]*len(p_names))
                cols[0].write(sq['name'])
                for i, p_n in enumerate(p_names):
                    is_own = (st.session_state.ownership[pid] == p_n)
                    if cols[i+1].button(p_n, key=f"set_o_{pid}_{i}", type="primary" if is_own else "secondary"):
                        st.session_state.ownership[pid] = "Bank" if is_own else p_n
                        st.rerun()
            st.write("")

        st.markdown("**Special Properties**")
        for pid in RAILROADS + UTILITIES:
            sq = PROPERTIES[pid]
            cols = st.columns([2] + [1]*len(p_names))
            cols[0].write(sq['name'])
            for i, p_n in enumerate(p_names):
                is_own = (st.session_state.ownership[pid] == p_n)
                if cols[i+1].button(p_n, key=f"set_o_{pid}_{i}", type="primary" if is_own else "secondary"):
                    st.session_state.ownership[pid] = "Bank" if is_own else p_n
                    st.rerun()

    with t2:
        st.subheader("Manage Houses/Hotels")
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            # Only allow building if someone owns the whole monopoly
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f'<div style="background:{COLOR_MAP[color]}; padding:5px; border-radius:3px; color:white;"><b>{color} Monopoly: {owners[0]}</b></div>', unsafe_allow_html=True)
                for pid in pids:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    h = st.session_state.houses[pid]
                    if c2.button("➖", key=f"h_minus_{pid}"): 
                        st.session_state.houses[pid] = max(0, h-1)
                        st.rerun()
                    c3.write(f"**{h}**")
                    if c4.button("➕", key=f"h_plus_{pid}"): 
                        st.session_state.houses[pid] = min(5, h+1)
                        st.rerun()
            else:
                st.write(f"*{color} group is split or owned by Bank.*")

    with t3:
        st.subheader("Adjust Player Values")
        for i, p in enumerate(st.session_state.players):
            with st.expander(f"Adjust {p['name']}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    p['cash'] = st.number_input(f"Cash Amount", value=int(p['cash']), step=50, key=f"edit_cash_{i}")
                    p['in_jail'] = st.checkbox(f"Is in Jail?", value=p['in_jail'], key=f"edit_jail_{i}")
                with c2:
                    p['pos'] = st.slider(f"Board Position (Index)", 0, 39, value=p['pos'], key=f"edit_pos_{i}")
                    st.caption(f"Currently at: {PROPERTIES[p['pos']]['name']}")

    if st.button("Finalize and Start Simulation", use_container_width=True, type="primary"):
        st.session_state.phase = "LIVE"
        st.rerun()

elif st.session_state.phase == "LIVE":
    # --- Sidebar Ledger ---
    st.sidebar.title("📊 Game Ledger")
    if st.session_state.rules["fp_jackpot"]:
        st.sidebar.metric("Free Parking Jackpot", f"${st.session_state.jackpot}")
    
    for p in st.session_state.players:
        with st.sidebar.expander(f"{p['name']} | ${p['cash']}", expanded=True):
            st.write(f"📍 **{PROPERTIES[p['pos']]['name']}**")
            if p.get('in_jail'): st.error("Status: IN JAIL")
            if p['goo_cards']: st.success(f"GOOJF Cards: {len(p['goo_cards'])}")

    # --- Main Gameplay Area ---
    curr_p = st.session_state.players[st.session_state.current_p]
    st.subheader(f"👉 Current Turn: {curr_p['name']}")
    
    if curr_p.get('in_jail'):
        st.warning(f"{curr_p['name']} is in jail (Turn {curr_p['jail_turns']}/3)")
        c1, c2, c3 = st.columns(3)
        if c1.button("Roll for Doubles", use_container_width=True):
            run_turn("Try Doubles")
            st.rerun()
        if c2.button("Pay $50", use_container_width=True):
            run_turn("Pay $50")
            st.rerun()
        if c3.button("Use Card", use_container_width=True, disabled=not curr_p['goo_cards']):
            run_turn("Use Card")
            st.rerun()
    else:
        lc1, lc2 = st.columns([1, 2])
        if lc1.button("Execute Next Turn", use_container_width=True, type="primary"):
            run_turn()
            st.rerun()
        with lc2:
            j_val = st.number_input("Bulk Jump Turns", 1, 10000, 100, label_visibility="collapsed")
            if st.button(f"Jump {j_val} Turns", use_container_width=True):
                for _ in range(j_val): 
                    run_turn(silent=True)
                st.rerun()

    # --- Live Feed & Board State ---
    if st.session_state.last_move:
        st.info(st.session_state.last_move)
    
    st.markdown("---")
    st.caption(f"Turn Counter: {st.session_state.turn_count}")
    if st.sidebar.button("RESET LAB", use_container_width=True):
        reset_lab()

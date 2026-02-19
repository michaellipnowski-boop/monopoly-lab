import streamlit as st
import random

# --- 1. FULL DATA CONSTANTS ---
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

# --- 2. DECK DEFINITIONS ---
CHANCE_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
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
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Bank error. Collect $200", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee. Pay $50", "effect": "cash", "amt": -50},
    {"text": "From sale of stock get $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go to Jail", "effect": "jail"},
    {"text": "Holiday fund matures. Collect $100", "effect": "cash", "amt": 100},
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

# --- 3. SESSION STATE ---
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.p_count = 2
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if "price" in PROPERTIES[pid]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.current_p = 0
    st.session_state.double_count = 0
    st.session_state.last_log = "Laboratory Ready."
    st.session_state.c_deck = list(range(16))
    st.session_state.ch_deck = list(range(16))
    random.shuffle(st.session_state.c_deck)
    random.shuffle(st.session_state.ch_deck)

# --- 4. ENGINE LOGIC ---
def get_rent_due(pid, roll):
    owner = st.session_state.ownership[pid]
    info = PROPERTIES[pid]
    if info['type'] == "Street":
        h = st.session_state.houses[pid]
        rent = info['rent'][h]
        if h == 0:
            color = info['color']
            set_pids = [p for p,d in PROPERTIES.items() if d.get('color') == color]
            if all(st.session_state.ownership[sp] == owner for sp in set_pids):
                return rent * 2
        return rent
    elif info['type'] == "Railroad":
        rr_pids = [5, 15, 25, 35]
        count = sum(1 for r in rr_pids if st.session_state.ownership[r] == owner)
        return info['rent'][count-1]
    elif info['type'] == "Utility":
        u_pids = [12, 28]
        count = sum(1 for u in u_pids if st.session_state.ownership[u] == owner)
        return (4 if count == 1 else 10) * roll
    return 0

def handle_card(p, deck_type):
    deck = st.session_state.c_deck if deck_type == "chance" else st.session_state.ch_deck
    data = CHANCE_DECK if deck_type == "chance" else CHEST_DECK
    idx = deck.pop(0)
    card = data[idx]
    msg = f"Card: {card['text']}"
    
    if card['effect'] == "move":
        old = p['pos']
        p['pos'] = card['pos']
        if p['pos'] < old: p['cash'] += 200
    elif card['effect'] == "jail":
        p['pos'] = 10; p['in_jail'] = True; p['jail_turns'] = 0
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
    elif card['effect'] == "cash":
        p['cash'] += card['amt']
    elif card['effect'] == "birthday":
        for other in st.session_state.players:
            if other['name'] != p['name']:
                other['cash'] -= card['amt']
                p['cash'] += card['amt']
    elif card['effect'] == "repairs":
        total = 0
        for pid, h_count in st.session_state.houses.items():
            if st.session_state.ownership[pid] == p['name']:
                total += (card['H'] if h_count == 5 else (h_count * card['h']))
        p['cash'] -= total
    elif card['effect'] == "move_nearest_rr":
        rrs = [5, 15, 25, 35]
        target = next((r for r in rrs if r > p['pos']), 5)
        if target < p['pos']: p['cash'] += 200
        p['pos'] = target
    elif card['effect'] == "move_nearest_util":
        target = 28 if (12 < p['pos'] < 28) else 12
        if target < p['pos']: p['cash'] += 200
        p['pos'] = target
    elif card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        return msg
    
    deck.append(idx)
    return msg

def run_turn(jail_action=None):
    p = st.session_state.players[st.session_state.current_p]
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    roll, is_double = d1 + d2, (d1 == d2)
    log_msg = f"{p['name']} rolled {d1}+{d2}. "
    
    if p['in_jail']:
        p['jail_turns'] += 1
        if jail_action == "Pay $50":
            p['cash'] -= 50; p['in_jail'] = False
        elif jail_action == "Use Card":
            card = p['goo_cards'].pop(0)
            if card['deck'] == "chance": st.session_state.c_deck.append(card['index'])
            else: st.session_state.ch_deck.append(card['index'])
            p['in_jail'] = False
        elif is_double:
            p['in_jail'] = False
        elif p['jail_turns'] >= 3:
            p['cash'] -= 50; p['in_jail'] = False
        else:
            st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
            st.session_state.last_log = log_msg + "Still in jail."
            return

    if is_double: st.session_state.double_count += 1
    else: st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        p['pos'] = 10; p['in_jail'] = True; p['jail_turns'] = 0
        st.session_state.double_count = 0
        st.session_state.last_log = log_msg + "3 doubles! Go to Jail."
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        old = p['pos']
        p['pos'] = (p['pos'] + roll) % 40
        if p['pos'] < old: p['cash'] += 200
        sq = PROPERTIES[p['pos']]
        log_msg += f"Landed on {sq['name']}. "
        
        if "price" in sq:
            owner = st.session_state.ownership[p['pos']]
            if owner != "Bank" and owner != p['name']:
                due = get_rent_due(p['pos'], roll)
                p['cash'] -= due
                for op in st.session_state.players:
                    if op['name'] == owner: op['cash'] += due
                log_msg += f"Paid ${due} to {owner}."
        elif sq['type'] == "Tax":
            p['cash'] -= sq['cost']
            log_msg += f"Paid ${sq['cost']} tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30:
                p['pos'] = 10; p['in_jail'] = True; p['jail_turns'] = 0
                log_msg += "Go to Jail!"
            else:
                card_msg = handle_card(p, sq['deck'])
                log_msg += card_msg
        
        st.session_state.last_log = log_msg
        if not is_double:
            st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)

# --- 5. UI FLOW ---
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    st.session_state.p_count = st.number_input("How many players?", 1, 8, 2)
    names = [st.text_input(f"Player {i+1}", f"Student {chr(65+i)}", key=f"nm_{i}") for i in range(st.session_state.p_count)]
    if st.button("Initialize"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0, "goo_cards": [], "in_jail": False, "jail_turns": 0} for n in names]
        st.session_state.phase = "SETUP"; st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Setup Board State")
    p_names = [p['name'] for p in st.session_state.players]
    t1, t2, t3 = st.tabs(["Property Ownership", "Houses/Hotels", "GOOJF Toggler"])
    
    with t1:
        for pid, sq in PROPERTIES.items():
            if "price" in sq:
                cols = st.columns([2] + [1]*len(p_names))
                cols[0].write(sq['name'])
                for i, n in enumerate(p_names):
                    is_own = (st.session_state.ownership[pid] == n)
                    if cols[i+1].button(n, key=f"o_{pid}{i}", type="primary" if is_own else "secondary"):
                        st.session_state.ownership[pid] = "Bank" if is_own else n
                        st.rerun()
    
    with t2:
        for pid, h_count in st.session_state.houses.items():
            owner = st.session_state.ownership[pid]
            if owner != "Bank":
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"{PROPERTIES[pid]['name']} ({owner})")
                if c2.button("-", key=f"hm{pid}"): st.session_state.houses[pid] = max(0, h_count-1); st.rerun()
                if c3.button("+", key=f"hp_{pid}"): st.session_state.houses[pid] = min(5, h_count+1); st.rerun()

    with t3:
        for dk in ["chance", "chest"]:
            st.write(f"{dk.capitalize()} Card Holder")
            owner_n = "Bank"
            for p in st.session_state.players:
                if any(c['deck'] == dk for c in p['goo_cards']): owner_n = p['name']
            cols = st.columns(len(p_names))
            for i, n in enumerate(p_names):
                is_act = (owner_n == n)
                if cols[i].button(n, key=f"g_{dk}_{i}", type="primary" if is_act else "secondary"):
                    for pl in st.session_state.players: pl['goo_cards'] = [c for c in pl['goo_cards'] if c['deck'] != dk]
                    idx = 6 if dk == "chance" else 4
                    d_list = st.session_state.c_deck if dk == "chance" else st.session_state.ch_deck
                    if idx not in d_list: d_list.append(idx)
                    if not is_act:
                        d_list.remove(idx)
                        st.session_state.players[i]['goo_cards'].append({"deck": dk, "index": idx})
                    st.rerun()

    if st.button("Launch Simulation"): st.session_state.phase = "LIVE"; st.rerun()

elif st.session_state.phase == "LIVE":
    st.title("🎲 Live Simulation")
    curr = st.session_state.players[st.session_state.current_p]
    st.info(st.session_state.last_log)
    st.write(f"Current Turn: {curr['name']}")
    
    if curr['in_jail']:
        c1, c2, c3 = st.columns(3)
        if c1.button("Try for Doubles"): run_turn(); st.rerun()
        if c2.button("Pay $50"): run_turn("Pay $50"); st.rerun()
        if c3.button("Use Card", disabled=not curr['goo_cards']): run_turn("Use Card"); st.rerun()
    else:
        if st.button("Roll Dice"): run_turn(); st.rerun()
    
    st.sidebar.title("Player HUD")
    for p in st.session_state.players:
        st.sidebar.markdown(f"{p['name']}")
        st.sidebar.text(f"Cash: ${p['cash']}")
        st.sidebar.text(f"Position: {PROPERTIES[p['pos']]['name']}")
        if p['goo_cards']: st.sidebar.text(f"Cards: {len(p['goo_cards'])}")
    
    if st.sidebar.button("Full Reset"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

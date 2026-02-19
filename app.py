import streamlit as st
import random

# --- DATA CONSTANTS ---
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
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Advance to Illinois Avenue", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles Place", "effect": "move", "pos": 11},
    {"text": "Advance to nearest Utility", "effect": "move_nearest_util"},
    {"text": "Advance to nearest Railroad", "effect": "move_nearest_rr"},
    {"text": "Bank pays dividend $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3},
    {"text": "Go to Jail", "effect": "jail"},
    {"text": "General repairs", "effect": "repairs", "h": 25, "H": 100},
    {"text": "Speeding fine $15", "effect": "cash", "amt": -15},
    {"text": "Trip to Reading Railroad", "effect": "move", "pos": 5},
    {"text": "Advance to Boardwalk", "effect": "move", "pos": 39},
    {"text": "Elected Chairman", "effect": "birthday", "amt": -50},
    {"text": "Building loan matures", "effect": "cash", "amt": 150},
    {"text": "Crossword competition prize", "effect": "cash", "amt": 100}
]

CHEST_DECK = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Bank error", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee", "effect": "cash", "amt": -50},
    {"text": "From sale of stock get $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "goo_card"},
    {"text": "Go to Jail", "effect": "jail"},
    {"text": "Holiday fund matures", "effect": "cash", "amt": 100},
    {"text": "Income tax refund", "effect": "cash", "amt": 20},
    {"text": "It is your birthday", "effect": "birthday", "amt": 10},
    {"text": "Life insurance matures", "effect": "cash", "amt": 100},
    {"text": "Hospital Fees", "effect": "cash", "amt": -100},
    {"text": "School fees", "effect": "cash", "amt": -50},
    {"text": "Consultancy fee", "effect": "cash", "amt": 25},
    {"text": "Street repairs", "effect": "repairs", "h": 40, "H": 115},
    {"text": "Beauty contest prize", "effect": "cash", "amt": 10},
    {"text": "You inherit $100", "effect": "cash", "amt": 100}
]

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
    st.session_state.c_deck_idx = list(range(16))
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    random.shuffle(st.session_state.ch_deck_idx)

def reset_lab():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- SIMULATION HELPERS ---
def get_rent(pid, roll_sum=0):
    info = PROPERTIES[pid]
    owner = st.session_state.ownership[pid]
    if info['type'] == "Street":
        h_count = st.session_state.houses[pid]
        base = info['rent'][h_count]
        if h_count == 0:
            color = info['color']
            color_pids = [p for p, data in PROPERTIES.items() if data.get('color') == color]
            if all(st.session_state.ownership[cp] == owner for cp in color_pids):
                return base * 2
        return base
    elif info['type'] == "Railroad":
        rr_pids = [5, 15, 25, 35]
        count = sum(1 for r in rr_pids if st.session_state.ownership[r] == owner)
        return info['rent'][count - 1]
    elif info['type'] == "Utility":
        u_pids = [12, 28]
        count = sum(1 for u in u_pids if st.session_state.ownership[u] == owner)
        return (4 if count == 1 else 10) * roll_sum
    return 0

def send_to_jail(player):
    player['pos'] = 10
    player['in_jail'] = True
    player['jail_turns'] = 0
    st.session_state.double_count = 0

def draw_card(player, deck_type):
    if deck_type == "chance":
        idx = st.session_state.c_deck_idx.pop(0)
        card = CHANCE_DECK[idx]
    else:
        idx = st.session_state.ch_deck_idx.pop(0)
        card = CHEST_DECK[idx]
    
    if card['effect'] == "move":
        old = player['pos']
        player['pos'] = card['pos']
        if player['pos'] < old: player['cash'] += 200
    elif card['effect'] == "jail": send_to_jail(player)
    elif card['effect'] == "move_relative": player['pos'] = (player['pos'] + card['amt']) % 40
    elif card['effect'] == "cash": player['cash'] += card['amt']
    elif card['effect'] == "birthday":
        for other in st.session_state.players:
            if other['name'] != player['name']:
                other['cash'] -= card['amt']
                player['cash'] += card['amt']
    elif card['effect'] == "goo_card":
        player['goo_cards'].append({"deck": deck_type, "index": idx})
        return f"drew {deck_type} GOOJF card"
    
    if deck_type == "chance": st.session_state.c_deck_idx.append(idx)
    else: st.session_state.ch_deck_idx.append(idx)
    return f"drew {deck_type}: {card['text']}"

def run_turn(jail_action=None):
    p = st.session_state.players[st.session_state.current_p]
    if p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return
    
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    roll, is_double = d1 + d2, (d1 == d2)
    
    if p.get('in_jail'):
        p['jail_turns'] += 1
        if jail_action == "Pay $50":
            p['cash'] -= 50
            p['in_jail'] = False
        elif jail_action == "Use Card":
            card = p['goo_cards'].pop(0)
            if card['deck'] == "chance": st.session_state.c_deck_idx.append(card['index'])
            else: st.session_state.ch_deck_idx.append(card['index'])
            p['in_jail'] = False
        else:
            if is_double: p['in_jail'] = False
            elif p['jail_turns'] >= 3:
                p['cash'] -= 50
                p['in_jail'] = False
            else:
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                return

    if is_double and not p.get('in_jail'): st.session_state.double_count += 1
    else: st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        old = p['pos']
        p['pos'] = (p['pos'] + roll) % 40
        if p['pos'] < old: p['cash'] += 200
        sq = PROPERTIES[p['pos']]
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership[p['pos']]
            if owner != "Bank" and owner != p['name']:
                rent = get_rent(p['pos'], roll)
                p['cash'] -= rent
                for op in st.session_state.players:
                    if op['name'] == owner: op['cash'] += rent
        elif sq['type'] == "Tax": p['cash'] -= sq.get('cost', 100)
        elif sq['type'] == "Action":
            if p['pos'] == 30: send_to_jail(p)
            else: draw_card(p, sq.get('deck', 'chance'))
        if not is_double:
            st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    st.session_state.turn_count += 1

# --- UI FLOW ---
if st.session_state.phase == "INIT":
    st.title("Monopoly Stats Lab")
    st.session_state.p_count = st.number_input("How many players?", 1, 8, value=st.session_state.p_count)
    names = []
    for i in range(st.session_state.p_count):
        names.append(st.text_input(f"Player {i+1}", f"Student {chr(65+i)}", key=f"n_{i}"))
    if st.button("Initialize Game"):
        st.session_state.p_names = names
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0, "goo_cards": [], "in_jail": False} for n in names]
        st.session_state.phase = "SETUP"
        st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("Board Customization")
    t1, t2, t3 = st.tabs(["Ownership", "Development", "Status & Cards"])
    p_names = [p['name'] for p in st.session_state.players]
    
    with t1:
        for pid, sq in PROPERTIES.items():
            if "rent" in sq or sq['type'] in ["Railroad", "Utility"]:
                cols = st.columns([2] + [1]*len(p_names))
                cols[0].write(sq['name'])
                for i, n in enumerate(p_names):
                    is_own = (st.session_state.ownership[pid] == n)
                    if cols[i+1].button(n, key=f"o_{pid}{i}", type="primary" if is_own else "secondary"):
                        st.session_state.ownership[pid] = "Bank" if is_own else n
                        st.rerun()
    
    with t2:
        for pid, h in st.session_state.houses.items():
            owner = st.session_state.ownership[pid]
            if owner != "Bank":
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"{PROPERTIES[pid]['name']} ({owner})")
                if c2.button("-", key=f"hm{pid}"): st.session_state.houses[pid] = max(0, h-1); st.rerun()
                if c3.button("+", key=f"hp_{pid}"): st.session_state.houses[pid] = min(5, h+1); st.rerun()

    with t3:
        for i, p in enumerate(st.session_state.players):
            st.write(f"### {p['name']}")
            p['cash'] = st.number_input(f"Cash: {p['name']}", value=int(p['cash']), step=50, key=f"ca_{i}")
            p['in_jail'] = st.checkbox(f"In Jail: {p['name']}", value=p.get('in_jail', False), key=f"ja_{i}")
        
        st.markdown("---")
        st.subheader("Global GOOJF Tracker")
        
        # Chance Card
        st.write("Chance GOOJF Card Owner")
        ch_owner = "Bank"
        for p in st.session_state.players:
            if any(c['deck'] == "chance" for c in p['goo_cards']): ch_owner = p['name']
        ch_cols = st.columns(len(p_names))
        for i, n in enumerate(p_names):
            is_act = (ch_owner == n)
            if ch_cols[i].button(n, key=f"gch_{i}", type="primary" if is_act else "secondary"):
                for pl in st.session_state.players: pl['goo_cards'] = [c for c in pl['goo_cards'] if c['deck'] != "chance"]
                if 6 not in st.session_state.c_deck_idx: st.session_state.c_deck_idx.append(6)
                if not is_act:
                    st.session_state.c_deck_idx.remove(6)
                    st.session_state.players[i]['goo_cards'].append({"deck": "chance", "index": 6})
                st.rerun()

        # Chest Card
        st.write("Community Chest GOOJF Card Owner")
        cc_owner = "Bank"
        for p in st.session_state.players:
            if any(c['deck'] == "chest" for c in p['goo_cards']): cc_owner = p['name']
        cc_cols = st.columns(len(p_names))
        for i, n in enumerate(p_names):
            is_act = (cc_owner == n)
            if cc_cols[i].button(n, key=f"gcc_{i}", type="primary" if is_act else "secondary"):
                for pl in st.session_state.players: pl['goo_cards'] = [c for c in pl['goo_cards'] if c['deck'] != "chest"]
                if 4 not in st.session_state.ch_deck_idx: st.session_state.ch_deck_idx.append(4)
                if not is_act:
                    st.session_state.ch_deck_idx.remove(4)
                    st.session_state.players[i]['goo_cards'].append({"deck": "chest", "index": 4})
                st.rerun()

    if st.button("Finish Setup"):
        st.session_state.phase = "LIVE"
        st.rerun()

elif st.session_state.phase == "LIVE":
    st.title("Game Simulation")
    curr = st.session_state.players[st.session_state.current_p]
    st.write(f"Turn: {curr['name']}")
    
    if curr.get('in_jail'):
        c1, c2, c3 = st.columns(3)
        if c1.button("Try Doubles"): run_turn(jail_action="Try Doubles"); st.rerun()
        if c2.button("Pay $50"): run_turn(jail_action="Pay $50"); st.rerun()
        if c3.button("Use GOOJF", disabled=not curr['goo_cards']): run_turn(jail_action="Use Card"); st.rerun()
    else:
        if st.button("Roll Dice"): run_turn(); st.rerun()
    
    st.sidebar.title("Financials")
    for p in st.session_state.players:
        st.sidebar.write(f"{p['name']}: ${p['cash']}")
    if st.sidebar.button("Hard Reset"): reset_lab()

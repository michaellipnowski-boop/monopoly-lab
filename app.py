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
    1: {"name": "Mediterranean Avenue", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250], "price": 60, "h_cost": 50},
    2: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    3: {"name": "Baltic Avenue", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450], "price": 60, "h_cost": 50},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    6: {"name": "Oriental Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550], "price": 100, "h_cost": 50},
    7: {"name": "Chance", "type": "Action", "deck": "chance"},
    8: {"name": "Vermont Avenue", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550], "price": 100, "h_cost": 50},
    9: {"name": "Connecticut Avenue", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600], "price": 120, "h_cost": 50},
    10: {"name": "Jail / Just Visiting", "type": "Safe"},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750], "price": 140, "h_cost": 100},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "rent": [4, 10], "price": 150},
    13: {"name": "States Avenue", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750], "price": 140, "h_cost": 100},
    14: {"name": "Virginia Avenue", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900], "price": 160, "h_cost": 100},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950], "price": 180, "h_cost": 100},
    17: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    18: {"name": "Tennessee Avenue", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950], "price": 180, "h_cost": 100},
    19: {"name": "New York Avenue", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000], "price": 200, "h_cost": 100},
    20: {"name": "Free Parking", "type": "Safe"},
    21: {"name": "Kentucky Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050], "price": 220, "h_cost": 150},
    22: {"name": "Chance", "type": "Action", "deck": "chance"},
    23: {"name": "Indiana Avenue", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050], "price": 220, "h_cost": 150},
    24: {"name": "Illinois Avenue", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100], "price": 240, "h_cost": 150},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    26: {"name": "Atlantic Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150], "price": 260, "h_cost": 150},
    27: {"name": "Ventnor Avenue", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150], "price": 260, "h_cost": 150},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10], "price": 150},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200], "price": 280, "h_cost": 150},
    30: {"name": "Go To Jail", "type": "Action"},
    31: {"name": "Pacific Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275], "price": 300, "h_cost": 200},
    32: {"name": "North Carolina Avenue", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275], "price": 300, "h_cost": 200},
    33: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    34: {"name": "Pennsylvania Avenue", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400], "price": 320, "h_cost": 200},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200], "price": 200},
    36: {"name": "Chance", "type": "Action", "deck": "chance"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500], "price": 350, "h_cost": 200},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000], "price": 400, "h_cost": 200}
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
    st.session_state.jackpot = 0
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)
    st.session_state.rules = {
        "allow_debt": True, 
        "double_go": False, 
        "fp_jackpot": False, 
        "fp_initial": 0,
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
    # --- TRACK THE VISIT TO JAIL ---
    p['stats']['visits'][10] += 1
    p['stats']['times_in_jail'] += 1

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
    
    if card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        return msg
    
    if card['effect'] == "move":
        old_pos = p['pos']
        p['pos'] = card['pos']
        p['stats']['visits'][p['pos']] += 1
        if p['pos'] < old_pos: 
            p['cash'] += 200
            
    elif card['effect'] == "jail":
        send_to_jail(p)
        
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
        p['stats']['visits'][p['pos']] += 1
        
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
        for pid, h_count in st.session_state.houses.items():
            if st.session_state.ownership.get(pid) == p['name']:
                if h_count == 5:
                    cost += card['H']
                else:
                    cost += (h_count * card['h'])
        charge_player(p, cost)
        
    elif card['effect'] == "move_nearest_rr":
        targets = [5, 15, 25, 35]
        old_pos = p['pos']
        p['pos'] = min([r for r in targets if r > p['pos']] or [5])
        p['stats']['visits'][p['pos']] += 1
        if p['pos'] < old_pos: p['cash'] += 200
        
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        old_pos = p['pos']
        p['pos'] = min([u for u in targets if u > p['pos']] or [12])
        p['stats']['visits'][p['pos']] += 1
        if p['pos'] < old_pos: p['cash'] += 200

    if st.session_state.rules["shuffle_mode"] == "True Random":
        if deck_type == "chance": 
            st.session_state.c_deck_idx.append(idx)
            random.shuffle(st.session_state.c_deck_idx)
        else: 
            st.session_state.ch_deck_idx.append(idx)
            random.shuffle(st.session_state.ch_deck_idx)
    else:
        if deck_type == "chance": 
            st.session_state.c_deck_idx.append(idx)
        else: 
            st.session_state.ch_deck_idx.append(idx)
            
    return msg

def run_turn(jail_action=None, silent=False):
    p = st.session_state.players[st.session_state.current_p]
    
    if not st.session_state.rules["allow_debt"] and p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return
    
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    roll_sum = d1 + d2
    is_double = (d1 == d2)
    
    if p.get('in_jail'):
        if jail_action is None:
            # Policy-based automation
            if p['goo_cards']:
                jail_action = "Use Card"
            elif p['policy']['jail_exit'] == "Pay Immediately" and p['cash'] >= 50:
                jail_action = "Pay $50"
            elif p['jail_turns'] >= 2:
                jail_action = "Pay $50"
            else:
                jail_action = "Try Doubles"
        
        if jail_action == "Pay $50":
            charge_player(p, 50)
            p['in_jail'] = False
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
                charge_player(p, 50)
                p['in_jail'] = False
                if not silent: st.session_state.last_move = f"{p['name']} failed 3rd double attempt, paid $50."
            else:
                p['jail_turns'] += 1
                if not silent: st.session_state.last_move = f"{p['name']} failed doubles, stays in Jail."
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                st.session_state.turn_count += 1
                return
    
    if is_double and not p.get('in_jail'):
        st.session_state.double_count += 1
    else:
        st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        if not silent: st.session_state.last_move = f"{p['name']} rolled 3 doubles! Go to Jail!"
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    else:
        old_pos = p['pos']
        p['pos'] = (p['pos'] + roll_sum) % 40
        p['stats']['visits'][p['pos']] += 1
        
        if p['pos'] < old_pos:
            if st.session_state.rules["double_go"] and p['pos'] == 0:
                p['cash'] += 400
            else:
                p['cash'] += 200
        
        sq = PROPERTIES.get(p['pos'])
        msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "
        
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership.get(p['pos'], "Bank")
            if owner != "Bank" and owner != p['name']:
                rent = get_rent(p['pos'], roll_sum)
                
                # --- PRESERVE EXISTING LOGIC ---
                p['cash'] -= rent
                # Record the rent paid by the current player
                p['stats']['rent_paid'] += rent 
                
                for op in st.session_state.players:
                    if op['name'] == owner: 
                        op['cash'] += rent
                        # --- RECORD RENT COLLECTED BY THE OWNER ---
                        op['stats']['rent_collected'] += rent
                
                msg += f"Paid ${rent} rent. "
            elif owner == "Bank":
                # Policy-based Buying
                price = sq.get('price', 150)
                pol = p['policy']['buy_prop']
                res = p['policy']['buy_res']
                should_buy = (pol == "Always") or (pol == "Keep Reserve" and p['cash'] - price >= res)
                if should_buy and p['cash'] >= price:
                    st.session_state.ownership[p['pos']] = p['name']
                    p['cash'] -= price
                    msg += f"Bought for ${price}."
        elif sq['type'] == "Tax":
            charge_player(p, sq.get('cost', 100))
            msg += f"Paid tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30:
                send_to_jail(p)
                msg += "Go To Jail!"
            else:
                msg += draw_card(p, sq.get('deck', 'chance'))
        elif sq['name'] == "Free Parking" and st.session_state.rules["fp_jackpot"]:
            if st.session_state.jackpot > 0:
                p['cash'] += st.session_state.jackpot
                msg += f"Collected Jackpot of ${st.session_state.jackpot}!"
                st.session_state.jackpot = st.session_state.rules["fp_initial"]
        
        # Policy-based Building (Post-movement)
        build_pol = p['policy']['build_house']
        build_res = p['policy']['build_res']
        if build_pol != "Never":
            for color, pids in COLOR_GROUPS.items():
                if all(st.session_state.ownership[pid] == p['name'] for pid in pids):
                    # Monopoly owned - try to build
                    sorted_pids = sorted(pids, key=lambda x: st.session_state.houses[x])
                    for target_pid in sorted_pids:
                        h_cost = PROPERTIES[target_pid].get('h_cost', 50)
                        current_h = st.session_state.houses[target_pid]
                        # Check affordability & Reserve
                        can_afford = (build_pol == "Always" and p['cash'] >= h_cost) or \
                                     (build_pol == "Keep Reserve" and p['cash'] - h_cost >= build_res)
                        # Check even building rule
                        is_lowest = current_h < 5 and all(current_h <= st.session_state.houses[other] for other in pids)
                        
                        if can_afford and is_lowest:
                            st.session_state.houses[target_pid] += 1
                            p['cash'] -= h_cost
                            msg += f" Built house on {PROPERTIES[target_pid]['name']}."
                            break 

        if not silent: st.session_state.last_move = msg
        # --- PHASE 2: END OF TURN TRACKER ---
        # We record this here because the player's physical movement 
        # for this specific roll is now complete.
        p['stats']['ends'][p['pos']] += 1

        # Your existing turn-switching logic:
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
    if st.button("Proceed to Global Rules"):
        st.session_state.p_names = temp_names
        st.session_state.players = []
        for n in temp_names:
            st.session_state.players.append({
                "name": n, 
                "cash": 1500, 
                "pos": 0, 
                "goo_cards": [], 
                "in_jail": False, 
                "jail_turns": 0,
                "policy": {
                    "buy_prop": "Always", "buy_res": 500, 
                    "build_house": "Always", "build_res": 500,
                    "jail_exit": "Try Doubles"
                },
                # --- PHASE 1: STATS BUCKET ---
                "stats": {
                    "visits": {i: 0 for i in range(40)}, # Every square touched (e.g., landing on Chance)
                    "ends": {i: 0 for i in range(40)},   # Only where the player is when the turn is over
                    "rent_paid": 0,
                    "rent_collected": 0,
                    "times_in_jail": 0
                }
            })
        st.session_state.phase = "RULES"
        st.rerun()

elif st.session_state.phase == "RULES":
    st.title("⚙️ Global Game Rules")
    if st.button("⬅ Back to Player Assignment"):
        st.session_state.phase = "INIT"
        st.rerun()
    st.markdown("---")
    st.subheader("Cash rules")
    st.session_state.rules["allow_debt"] = st.toggle("Allow negative balances (No Bankruptcy)", value=st.session_state.rules["allow_debt"])
    st.subheader("Deck shuffling")
    st.session_state.rules["shuffle_mode"] = st.radio("Chance and Community Chest shuffle mode", ["Cyclic", "True Random"], index=0 if st.session_state.rules["shuffle_mode"] == "Cyclic" else 1)
    st.subheader("House rules")
    st.session_state.rules["double_go"] = st.toggle("Double GO ($400 for landing exactly on GO)", value=st.session_state.rules["double_go"])
    st.session_state.rules["fp_jackpot"] = st.toggle("Free parking jackpot (Collect Taxes/Fines)", value=st.session_state.rules["fp_jackpot"])
    if st.session_state.rules["fp_jackpot"]:
        new_initial = st.number_input("Initial Jackpot Amount", min_value=0, value=int(st.session_state.rules["fp_initial"]), step=50)
        if new_initial != st.session_state.rules["fp_initial"]:
            st.session_state.rules["fp_initial"] = new_initial
            st.session_state.jackpot = new_initial
    st.markdown("---")
    if st.button("Proceed to Player Policies", type="primary"):
        st.session_state.phase = "POLICIES"
        st.rerun()

elif st.session_state.phase == "POLICIES":
    st.title("🧠 Player Policies")
    # --- DROP-IN BACK BUTTON ---
    if st.button("⬅ Back to Global Rules"):
        st.session_state.phase = "RULES"
        st.rerun()
    st.markdown("---")
    for i, p in enumerate(st.session_state.players):
        with st.expander(f"Strategy: {p['name']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                p['policy']['buy_prop'] = st.selectbox("Property Buying", ["Always", "Keep Reserve", "Never"], key=f"pol_b_{i}")
                if p['policy']['buy_prop'] == "Keep Reserve":
                    p['policy']['buy_res'] = st.number_input("Reserve ($)", 0, 5000, p['policy']['buy_res'], 50, key=f"pol_br_{i}")
            with col2:
                p['policy']['build_house'] = st.selectbox("House Building", ["Always", "Keep Reserve", "Never"], key=f"pol_h_{i}")
                if p['policy']['build_house'] == "Keep Reserve":
                    p['policy']['build_res'] = st.number_input("Reserve ($)", 0, 5000, p['policy']['build_res'], 50, key=f"pol_hr_{i}")
            with col3:
                p['policy']['jail_exit'] = st.selectbox("Jail Strategy", ["Try Doubles", "Pay Immediately"], key=f"pol_j_{i}")
                
    if st.button("Proceed to Mode Selection"):
        st.session_state.phase = "CHOICE"
        st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Customization")
    # --- DROP-IN BACK BUTTON ---
    if st.button("⬅ Back to Mode Selection"):
        st.session_state.phase = "CHOICE"
        st.rerun()
    st.markdown("---")
    t1, t2, t3 = st.tabs(["Properties owned", "Houses built", "Cash, jail, and position"])
    p_names = [p['name'] for p in st.session_state.players]
    
    with t1:
        all_ownable = []
        for color, pids in COLOR_GROUPS.items(): all_ownable.extend(pids)
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
                    st.session_state.ownership[pid] = "Bank" if is_own else p_n
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
                    can_down = h > 0 and all(h >= o for o in others)
                    can_up = h < 5 and all(h <= o for o in others)
                    if c2.button("➖", key=f"hm{pid}", disabled=not can_down): st.session_state.houses[pid] -= 1; st.rerun()
                    c3.write(f"**{h}**")
                    if c4.button("➕", key=f"hp_{pid}", disabled=not can_up): st.session_state.houses[pid] += 1; st.rerun()
    
    with t3:
        st.markdown("### 🎫 Get Out of Jail Free Cards")
        for deck in ["chance", "chest"]:
            label = "Chance (Orange)" if deck == "chance" else "Community Chest (Yellow)"
            cols = st.columns([2] + [1]*len(p_names))
            cols[0].write(f"**{label}**")
            current_owner_name = "Bank"
            for p in st.session_state.players:
                if any(c['deck'] == deck for c in p['goo_cards']): current_owner_name = p['name']; break
            for i, p_n in enumerate(p_names):
                is_holder = (current_owner_name == p_n)
                if cols[i+1].button(p_n, key=f"goojf_{deck}_{p_n}", type="primary" if is_holder else "secondary"):
                    for p in st.session_state.players: p['goo_cards'] = [c for c in p['goo_cards'] if c['deck'] != deck]
                    target_idx = 6 if deck == "chance" else 4
                    if is_holder:
                        if deck == "chance": st.session_state.c_deck_idx.append(target_idx)
                        else: st.session_state.ch_deck_idx.append(target_idx)
                    else:
                        for p in st.session_state.players:
                            if p['name'] == p_n:
                                p['goo_cards'].append({"deck": deck, "index": target_idx})
                                if deck == "chance":
                                    if target_idx in st.session_state.c_deck_idx:
                                        st.session_state.c_deck_idx.remove(target_idx)
                                else:
                                    if target_idx in st.session_state.ch_deck_idx:
                                        st.session_state.ch_deck_idx.remove(target_idx)
                    st.rerun()
        st.markdown("---")
        for i, p in enumerate(st.session_state.players):
            st.markdown(f"#### 👤 {p['name']}")
            c1, c2 = st.columns([1, 2])
            with c1:
                p['cash'] = st.number_input(f"Cash", value=int(p['cash']), step=50, key=f"set_c_{i}")
                jail_val = st.checkbox(f"In Jail?", value=p['in_jail'], key=f"set_j_{i}")
                if jail_val:
                    p['in_jail'] = True
                    p['jail_turns'] = st.radio("Failed rolls:", [0, 1, 2], index=p['jail_turns'], key=f"jail_t_{i}", horizontal=True)
                else:
                    p['in_jail'] = False
                    p['jail_turns'] = 0
            with c2:
                valid_indices = [idx for idx in range(40) if idx != 30]
                def get_square_label(pos):
                    base = PROPERTIES[pos]['name']
                    if base in ["Chance", "Community Chest"]:
                        count = sum(1 for j in range(pos + 1) if PROPERTIES[j]['name'] == base)
                        return f"{base} ({'1st' if count==1 else '2nd' if count==2 else '3rd'})"
                    return base
                slider_pos = st.select_slider(f"Board Position", options=valid_indices, format_func=get_square_label, value=p['pos'] if not jail_val else 10, disabled=jail_val, key=f"set_p_{i}")
                p['pos'] = 10 if jail_val else slider_pos

    if st.button("Start Live Simulation"):
        st.session_state.phase = "LIVE"
        st.rerun()

elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Selection")
    # --- DROP-IN BACK BUTTON ---
    if st.button("⬅ Back to Player Policies"):
        st.session_state.phase = "POLICIES"
        st.rerun()
    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button("Standard Simulation"): st.session_state.phase = "LIVE"; st.rerun()
    if c2.button("Customization Setup"): st.session_state.phase = "SETUP"; st.rerun()

elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    # --- TURN COUNTER ---
    st.sidebar.metric("Total Turns Played", st.session_state.turn_count)
    st.sidebar.markdown("---")
    if st.session_state.rules["fp_jackpot"]:
        st.sidebar.metric("Free Parking Jackpot", f"${st.session_state.jackpot}")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            if p.get('in_jail'): st.error(f"IN JAIL 🚔 (Attempts: {p['jail_turns']})")
            for c in p['goo_cards']: st.success(f"GOOJF: {c['deck'].capitalize()}")
            # --- 1. Display Streets (Colored Blocks) ---
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    st.markdown(f'<span style="color:{COLOR_MAP[color]}">■</span> <b>{color}</b>', unsafe_allow_html=True)
                    is_mono = all(st.session_state.ownership[pid] == p['name'] for pid in pids)
                    st.write(", ".join([f"{PROPERTIES[pid]['name']}{' ('+str(st.session_state.houses[pid])+'🏠)' if is_mono else ''}" for pid in owned]))
            
            # --- 2. Display Railroads ---
            owned_rr = [pid for pid in RAILROADS if st.session_state.ownership[pid] == p['name']]
            if owned_rr:
                st.markdown(f"<b>🚂 Railroads ({len(owned_rr)})</b>", unsafe_allow_html=True)
                st.write(", ".join([PROPERTIES[pid]['name'] for pid in owned_rr]))
            
            # --- 3. Display Utilities ---
            owned_util = [pid for pid in UTILITIES if st.session_state.ownership[pid] == p['name']]
            if owned_util:
                st.markdown(f"<b>💡 Utilities ({len(owned_util)})</b>", unsafe_allow_html=True)
                st.write(", ".join([PROPERTIES[pid]['name'] for pid in owned_util]))

    board_markers = [""] * 40
    for p in st.session_state.players:
        initials = "".join([n[0] for n in p['name'].split()])
        jail_tag = "⛓️" if p.get('in_jail') else ""
        board_markers[p['pos']] += f"[{initials}{jail_tag}]"

    top_row = list(range(20, 31))
    right_col = list(range(31, 40))
    bottom_row = list(range(10, -1, -1))
    left_col = list(range(19, 10, -1))

    # --- RENDER BOARD ---
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
                    if r == 10 or cell in left_col or cell in right_col:
                        st.write(board_markers[cell])
        
        if 1 <= r <= 9: cols[12].write(board_markers[right_col[r-1]])

    st.markdown("---")
    curr_p = st.session_state.players[st.session_state.current_p]
    st.write(f"👉 Current Turn: **{curr_p['name']}**")
    
    # 1. Permanent Automation Row (Always Available)
    lc1, lc2 = st.columns([1, 2])
    with lc1:
        if st.button("Next Turn", use_container_width=True, type="primary"):
            run_turn()
            st.rerun()
    with lc2:
        col_v, col_b = st.columns([1, 1])
        with col_v:
            j_val = st.number_input("Turns to Jump", 1, 10000, 100, label_visibility="collapsed", key="jump_input")
        with col_b:
            if st.button(f"Jump {j_val} Turns", use_container_width=True):
                for _ in range(j_val): run_turn(silent=True)
                st.rerun()

    # 2. Contextual Jail Row (Appears ONLY if the current player is in jail)
    if curr_p.get('in_jail'):
        st.markdown("---")
        st.caption(f"🛠️ Manual Override for {curr_p['name']} (In Jail)")
        jc1, jc2, jc3 = st.columns(3)
        if jc1.button("Roll Doubles"): run_turn(jail_action="Try Doubles"); st.rerun()
        if jc2.button("Pay $50"): run_turn(jail_action="Pay $50"); st.rerun()
        if jc3.button("Use Card", disabled=not curr_p['goo_cards']): run_turn(jail_action="Use Card"); st.rerun()

    # 3. Status Message
    if st.session_state.last_move:
        st.info(st.session_state.last_move)

    # --- PHASE 3: ANALYTICS DASHBOARD ---
    st.markdown("---")
    st.header("🔬 Stats Analytics")
    
    t_visits, t_ends, t_fin = st.tabs(["🚶 Total Visits", "🛑 Turn Ends", "💰 Rent Flow"])
    
    with t_visits:
        # Aggregate visits from all players
        visit_data = {PROPERTIES[i]['name']: sum(p['stats']['visits'][i] for p in st.session_state.players) for i in range(40)}
        st.bar_chart(visit_data)

    with t_ends:
        # Aggregate where turns actually finish
        ends_data = {PROPERTIES[i]['name']: sum(p['stats']['ends'][i] for p in st.session_state.players) for i in range(40)}
        st.bar_chart(ends_data)

    with t_fin:
        # Show Rent Paid vs Collected per player
        fin_list = []
        for p in st.session_state.players:
            fin_list.append({"Player": p['name'], "Type": "Collected", "Amount": p['stats']['rent_collected']})
            fin_list.append({"Player": p['name'], "Type": "Paid", "Amount": p['stats']['rent_paid']})
        
        if fin_list:
            # We import it locally ONLY here so it doesn't mess with the rest of your app
            import pandas as pd 
            df_fin = pd.DataFrame(fin_list)
            st.bar_chart(data=df_fin, x="Player", y="Amount", color="Type", stack=False)
    
    if st.sidebar.button("RESET SIMULATION"):
        reset_lab()

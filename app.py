import streamlit as st
import random
import pandas as pd  # Added for data processing and Excel/CSV exports
from collections import defaultdict


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
    st.session_state.starting_players = None
    # Initialize using the INDEX (i) as the key so it matches game logic
    st.session_state.ownership = {
        i: "Bank" for i, p in PROPERTIES.items() 
        if isinstance(p, dict) and ("rent" in p or p.get("type") in ["Railroad", "Utility"])
    }
    st.session_state.houses = {pid: 0 for pid in range(40)}
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

#--- SPREADSHEET FUNCTIONALITY ---
def get_player_excel_data():
    import io
    
    output = io.BytesIO()
    # pd is now available from your top-level import
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for player in st.session_state.players:
            # --- REPLACED BLOCK: Groups multiple events per turn ---
            # defaultdict is now available from your top-level import
            grouped_events = defaultdict(list)
            for e in player['stats'].get('critical_moments', []):
                # Group by turn number
                grouped_events[e['turn']].append(str(e['event']))
            
            # Combine multiple events (e.g., "Bought Park Place ; Built house")
            event_map = {turn: " ; ".join(msgs) for turn, msgs in grouped_events.items()}
            
            history = player['stats']['cash_history']
            data = []
            
            for turn_idx in range(len(history)):
                # Get the event for this turn if it exists
                action = event_map.get(turn_idx, "")
                
                data.append({
                    "Turn": turn_idx,
                    "Cash Balance": history[turn_idx],
                    "Action/Acquisition": action
                })
            
            df = pd.DataFrame(data)
            # Save to a dedicated tab (Sheet name limit 31 chars)
            df.to_excel(writer, sheet_name=player['name'][:31], index=False)
            
            # Auto-adjust column width for readability
            worksheet = writer.sheets[player['name'][:31]]
            worksheet.set_column('C:C', 50) # Bumped to 50 for longer event strings
            
    return output.getvalue()

#--- GAME RESET ---
def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def restart_game():
    import copy
    import random

    # 1. Reset Board and Game State
    # 1. Initialize ALL 40 squares as "Bank" (or "None") to prevent look-up errors
    st.session_state.ownership = {str(idx): "Bank" for idx in range(40)}
    st.session_state.houses = {str(pid): 0 for pid in range(40)}
    st.session_state.last_move = "Game Restarted - Rules and custom totals preserved."
    st.session_state.turn_count = 0
    st.session_state.current_p = 0
    st.session_state.double_count = 0
    st.session_state.jackpot = st.session_state.rules["fp_initial"]

    st.session_state.master_log = [] 
    
    # 2. Initialize ALL 40 squares for property stats
    st.session_state.property_stats = {
        str(idx): {"revenue": 0, "expenses": 0} for idx in range(40)
    }

    
    
    # 2. Reshuffle Decks
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)
    
    # 3. Restore Players and Wipe Stats
    if "starting_players" in st.session_state:
        st.session_state.players = copy.deepcopy(st.session_state.starting_players)
        
        for p in st.session_state.players:
            p['stats'] = {
                "visits": {str(i): 0 for i in range(40)},
                "ends": {str(i): 0 for i in range(40)},
                "rent_paid": 0,
                "rent_collected": 0,
                "times_in_jail": 0,
                "cash_history": [p['cash']], 
                "critical_moments": []
            }
    
    # 4. The Final Kick
    st.rerun()

# --- HELPER LOGIC ---
def charge_player(p, amt):
    p['cash'] -= amt
    if st.session_state.rules["fp_jackpot"] and amt > 0:
        st.session_state.jackpot += amt

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    s_pid = str(pid)
    owner = st.session_state.ownership.get(s_pid)
    
    if not owner or owner == "Bank":
        return 0

    # 1. STREETS (Houses & Monopolies)
    if info['type'] == "Street":
        # SAFE LOOKUP: Only use the string key s_pid
        h = st.session_state.houses.get(s_pid, 0)
        base = info['rent'][h]
        
        if h == 0:
            group = COLOR_GROUPS[info['color']]
            owned_in_group = 0
            for g_id in group:
                curr = st.session_state.ownership.get(str(g_id))
                if curr and str(curr).strip().lower() == str(owner).strip().lower():
                    owned_in_group += 1
            if owned_in_group == len(group):
                return base * 2
        return base

    # 2. RAILROADS (Multi-ownership scaling)
    elif info['type'] == "Railroad":
        count = 0
        for r_id in [5, 15, 25, 35]:
            curr = st.session_state.ownership.get(str(r_id))
            if curr and str(curr).strip().lower() == str(owner).strip().lower():
                count += 1
        return info['rent'][max(0, count-1)]

    # 3. UTILITIES (Dice-roll based rent)
    elif info['type'] == "Utility":
        count = 0
        for u_id in [12, 28]:
            curr = st.session_state.ownership.get(str(u_id))
            if curr and str(curr).strip().lower() == str(owner).strip().lower():
                count += 1
        # roll is passed in from run_turn
        return (4 * roll) if count == 1 else (10 * roll)

    return 0

def send_to_jail(p):
    p['pos'] = 10
    p['in_jail'] = True
    p['jail_turns'] = 0
    st.session_state.double_count = 0
    # --- TRACK THE VISIT TO JAIL ---
    p['stats']['visits'][str(10)] += 1
    p['stats']['times_in_jail'] += 1

def attempt_buy_houses(p):
    # 1. Identify all color groups
    color_groups = {}
    # Use .items() because PROPERTIES is a dictionary!
    for idx, sq in PROPERTIES.items(): 
        if isinstance(sq, dict) and sq.get('type') == "Street":
            color = sq.get('color')
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(str(idx))

    for color, indices in color_groups.items():
        # 1. Manually count how many properties in this color the player actually owns
        player_owned_count = 0
        for idx in indices:
            # Wrap idx in str() to match the ownership dictionary keys
            owner_name = st.session_state.ownership.get(str(idx))
            if owner_name and str(owner_name).strip().lower() == str(p['name']).strip().lower():
                player_owned_count += 1
        
        # 2. DECISIVE CHECK: Do they own the WHOLE set?
        total_in_set = len(indices)
        is_monopoly = (player_owned_count == total_in_set) and (total_in_set > 0)
        
        if is_monopoly:
            # --- MONOPOLY TROPHY LOGIC (Only fires ONCE per color) ---
            monopoly_key = f"monopoly_achieved_{color}"
            if not p['stats'].get(monopoly_key):
                p['stats'][monopoly_key] = True
                if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                p['stats']['critical_moments'].append({
                    'turn': st.session_state.turn_count, 
                    'event': f"🏆 MONOPOLY: {color} set completed!"
                })

            # --- 3. BUILDING LOGIC (Only runs if they have a Monopoly) ---
            while True:
                # Wrap idx in str() to find the house count in the dictionary
                counts = [st.session_state.houses.get(str(idx), 0) for idx in indices]
                if all(c >= 5 for c in counts): break 
                
                target_idx = indices[counts.index(min(counts))]
                # Convert to int because the PROPERTIES dictionary keys are integers
                sq = PROPERTIES[int(target_idx)]
                h_price = sq.get('h_cost', 50) 
                
                if p['cash'] >= h_price:
                    p['cash'] -= h_price
                    # Use str(target_idx) to save the new house count
                    st.session_state.houses[str(target_idx)] = st.session_state.houses.get(str(target_idx), 0) + 1
                    
                    new_count = st.session_state.houses[str(target_idx)]
                    label = "Hotel" if new_count == 5 else f"House {new_count}"
                    event_text = f"🏗️ Built {label} on {sq['name']} (-${h_price})"
                    
                    if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                    p['stats']['critical_moments'].append({
                        'turn': st.session_state.turn_count, 
                        'event': event_text
                    })
                else:
                    break

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
    kept_card = False  # Initialize the flag
    
    if card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        kept_card = True  # Set flag so it's not added back to deck list
    
    elif card['effect'] == "move":
        # LANDMINE FIX: Force integer to protect % 40 math later
        old_pos = p['pos']
        p['pos'] = int(card['pos']) 
        if p['pos'] < old_pos: 
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
            # Normalized comparison to ensure no one skips paying the birthday gift!
            if str(op['name']).strip().lower() != str(p['name']).strip().lower():
                op['cash'] -= card['amt']
                p['cash'] += card['amt']
                
    elif card['effect'] == "repairs":
        cost = 0
        for pid, h_count in st.session_state.houses.items():
            # pid is already a string from our houses dict, 
            # so we use it directly to look up the owner
            owner = st.session_state.ownership.get(str(pid))
            # Use normalization to match the owner to the current player
            if owner and str(owner).strip().lower() == str(p['name']).strip().lower():
                if h_count == 5: # Hotel
                    cost += card['H']
                else: # Houses
                    cost += (h_count * card['h'])
        charge_player(p, cost)
        if "property_stats" in st.session_state and cost > 0:
            # Since we don't know which specific house needed repair in the card text,
            # most Monopoly sims distribute the cost or log it as a general 'Loss' 
            # for the player's overall ROI.
            p['stats']['rent_paid'] += cost # Or a dedicated 'maintenance_paid' stat
        
    elif card['effect'] == "move_nearest_rr":
        targets = [5, 15, 25, 35]
        old_pos = p['pos']
        p['pos'] = int(min([r for r in targets if r > p['pos']] or [5]))
        if p['pos'] < old_pos: p['cash'] += 200
        
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        old_pos = p['pos']
        p['pos'] = int(min([u for u in targets if u > p['pos']] or [12]))
        if p['pos'] < old_pos: p['cash'] += 200

    # --- FINAL DECK MANAGEMENT ---
    # Only put the card back if the player didn't KEEP it (GOOJF)
    if not kept_card:
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

def record_master_turn(p, msg):
    """Utility to capture the full state of a turn for the CSV log."""
    if "master_log" not in st.session_state:
        st.session_state.master_log = []
        
    st.session_state.master_log.append({
        "Turn": st.session_state.turn_count,
        "Player": p['name'],
        "Position": p['pos'],
        "Square": PROPERTIES[p['pos']]['name'],
        "Cash": p['cash'],
        "Action": msg.strip()
    })


def run_turn(jail_action=None, silent=False):
    p = st.session_state.players[st.session_state.current_p]
    
    if not st.session_state.rules["allow_debt"] and p['cash'] < 0:
        # 1. Sync cash history for ALL players so the graphs stay aligned
        for player in st.session_state.players:
            player['stats']['cash_history'].append(player['cash'])
        
        # 2. Increment the turn count (time still passed even if they are broke)
        st.session_state.turn_count += 1

        record_master_turn(p, "Turn skipped: Player is bankrupt/in debt.")
        
        # 3. Move to the next player and exit
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
                
                p['stats']['visits'][str(10)] += 1
                p['stats']['ends'][str(10)] += 1
                
                # --- INSERT THE HELPER CALL HERE ---
                record_master_turn(p, st.session_state.last_move)
                # ------------------------------------

                # Keep the cash history synced so the graph doesn't skip a turn
                for player in st.session_state.players:
                    player['stats']['cash_history'].append(player['cash'])
                
                # --- ADDED BUILDING OPPORTUNITY ---
                attempt_buy_houses(p) 
                # ----------------------------------

                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                st.session_state.turn_count += 1
                return
    
    if is_double and not p.get('in_jail'):
        st.session_state.double_count += 1
    else:
        st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        p['stats']['times_in_jail'] += 1
        if not silent: st.session_state.last_move = f"{p['name']} rolled 3 doubles! Go to Jail!"
        
        record_master_turn(p, st.session_state.last_move)

        # --- STATS SYNC ---
        p['stats']['visits'][str(10)] += 1
        p['stats']['ends'][str(10)] += 1
        # Keep the graph consistent
        for player in st.session_state.players:
            player['stats']['cash_history'].append(player['cash'])
        
        # --- BUILDING OPPORTUNITY ---
        attempt_buy_houses(p)
        
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        st.session_state.turn_count += 1
        # Stop here so the bottom of the function doesn't double-count this turn
        return
    else:
        old_pos = p['pos']
        p['pos'] = (p['pos'] + roll_sum) % 40
        
        if p['pos'] < old_pos:
            if st.session_state.rules["double_go"] and p['pos'] == 0:
                p['cash'] += 400
            else:
                p['cash'] += 200
        
        sq = PROPERTIES.get(p['pos'])
        msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "
        
        if sq['type'] in ["Street", "Railroad", "Utility", "Property"]:
            owner = st.session_state.ownership.get(str(p['pos']), "Bank")

            # CASE A: SOMEONE ELSE OWNS IT (RENT)
            if owner != "Bank" and str(owner).strip().lower() != str(p['name']).strip().lower():
                rent = get_rent(p['pos'], roll=roll_sum)
                p['cash'] -= rent
                p['stats']['rent_paid'] += rent 
                
                for op in st.session_state.players:
                    if str(op['name']).strip().lower() == str(owner).strip().lower():
                        op['cash'] += rent
                        op['stats']['rent_collected'] += rent
            
                if "property_stats" in st.session_state:
                    st.session_state.property_stats[str(p['pos'])]["revenue"] += rent
            
                # FIX: Directly use the info in the ticker message 
                # without looking for an 'event_msg' variable.
                msg += f"Paid ${rent} rent to {owner}. "
            
            # CASE B: BANK OWNS IT (PURCHASE)
            elif owner == "Bank":
                price = sq.get('price', 150)
                pol = p['policy']['buy_prop']
                res = p['policy']['buy_res']
                
                if pol == "Never Buy":
                    should_buy = False
                    msg += f" (Policy: Never Buy - skipped {sq['name']})." # <--- AUDIT LOG
                else:
                    should_buy = (pol == "Always") or (pol == "Keep Reserve" and p['cash'] - price >= res)
                    if not should_buy and p['cash'] >= price:
                        msg += f" (Policy: Keep Reserve - insufficient funds after reserve)." # <--- AUDIT LOG
                
                if should_buy and p['cash'] >= price:
                    st.session_state.ownership[str(p['pos'])] = p['name']
                    p['cash'] -= price
                    
                    # --- TRACK PROPERTY EXPENSE ---
                    if "property_stats" in st.session_state:
                        st.session_state.property_stats[str(p['pos'])]["expenses"] += price

                    # Monopoly logic is now handled by the Auditor function
                    buy_bonus = ""
                    
                    # Special labeling for Railroads/Utilities
                    extra_label = ""
                    if sq['type'] in ["Railroad", "Utility"]:
                        # We iterate through ownership items, ensuring we convert pid to int to look up in PROPERTIES
                        count = sum(1 for pid, o_name in st.session_state.ownership.items() 
                                    if o_name and str(o_name).strip().lower() == str(p['name']).strip().lower() 
                                    and PROPERTIES[int(pid)].get('type') == sq['type'])
                        label = "Utilities" if sq['type'] == "Utility" else "Railroads"
                        extra_label = f" [Total {label}: {count}]"

                    # --- LOG TO CRITICAL MOMENTS ---
                    if 'critical_moments' not in p['stats']:
                        p['stats']['critical_moments'] = []
                    
                    event_text = f"🏠 Bought {sq['name']} (-${price}){buy_bonus}{extra_label}"
                    p['stats']['critical_moments'].append({'turn': st.session_state.turn_count, 'event': event_text})
                    
                    msg += f"{event_text}. "
        elif sq['type'] == "Tax":
            charge_player(p, sq.get('cost', 100))
            msg += f"Paid tax."
        elif sq['type'] == "Action":
            if p['pos'] == 30:
                # 1. Record the visit to Square 30 BEFORE moving
                p['stats']['visits'][str(30)] += 1 
                # (Note: We don't record an 'end' here because they don't stay on 30)

                # 2. Move the player to 10
                send_to_jail(p)
                p['stats']['times_in_jail'] += 1
                msg += "Go To Jail!"

                record_master_turn(p, msg)
                
                # 3. Record the Visit and End at Square 10 (Jail)
                p['stats']['visits'][str(10)] += 1
                p['stats']['ends'][str(10)] += 1

                # --- BUILDING OPPORTUNITY ---
                attempt_buy_houses(p)
                
                # --- WEALTH SNAPSHOT (Safe Mode Sync) ---
                for player in st.session_state.players:
                    player['stats']['cash_history'].append(player['cash'])

                # --- EXIT THE TURN ---
                if not silent: st.session_state.last_move = msg
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                st.session_state.turn_count += 1
                return
            
            else:
                # Store the position BEFORE the card is drawn
                old_pos = p['pos']
                card_msg = draw_card(p, sq.get('deck', 'chance'))
                msg += f" {card_msg}"
                
                # --- ADD THIS FIX ---
                # Update old_pos so the movement check at the end of run_turn 
                # doesn't think the player moved "past Go" twice.
                old_pos = p['pos'] 
                # --------------------
                
                # --- NEW: IMMEDIATE JAIL CHECK ---
                if p.get('in_jail'):
                    p['stats']['visits'][str(10)] += 1
                    p['stats']['times_in_jail'] += 1
                    p['stats']['ends'][str(10)] += 1
                    
                    record_master_turn(p, msg)

                    for player in st.session_state.players:
                        player['stats']['cash_history'].append(player['cash'])
                    
                    if not silent: st.session_state.last_move = msg
                    st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                    st.session_state.turn_count += 1
                    return # Exit turn immediately
                # ---------------------------------
                
                # --- CLEANED CARD-MOVE PURCHASE LOGIC ---
                if p['pos'] != old_pos:
                    new_sq = PROPERTIES[p['pos']]
                    
                    if isinstance(new_sq, dict) and new_sq.get('type') in ["Property", "Railroad", "Utility", "Street"]:
                        owner = st.session_state.ownership.get(str(p['pos']), "Bank")
                        
                        if owner == "Bank":
                            price = new_sq.get('price', 150)
                            pol = p['policy']['buy_prop']
                            res = p['policy']['buy_res']

                            card_should_buy = False
                            if pol == "Never Buy":
                                msg += f" (Policy: Never Buy - skipped {new_sq['name']})."
                            else:
                                card_should_buy = (pol == "Always") or (pol == "Keep Reserve" and p['cash'] - price >= res)
                                if not card_should_buy and p['cash'] >= price:
                                    msg += f" (Policy: Keep Reserve - insufficient funds after reserve)."

                            if card_should_buy and p['cash'] >= price:
                                p['cash'] -= price
                                st.session_state.ownership[str(p['pos'])] = p['name']
                                
                                if "property_stats" in st.session_state:
                                    st.session_state.property_stats[str(p['pos'])]["expenses"] += price
                                
                                # --- RAILROAD / UTILITY COUNTER ---
                                extra_label = ""
                                if new_sq['type'] in ["Railroad", "Utility"]:
                                    count = sum(1 for pid, o_name in st.session_state.ownership.items() 
                                                if o_name and str(o_name).strip().lower() == str(p['name']).strip().lower() 
                                                and PROPERTIES[int(pid)].get('type') == new_sq['type'])
                                    label = "Utilities" if new_sq['type'] == "Utility" else "Railroads"
                                    extra_label = f" [Total {label}: {count}]"

                                # --- LOG TO CRITICAL MOMENTS ---
                                if 'critical_moments' not in p['stats']:
                                    p['stats']['critical_moments'] = []
                                
                                event_text = f"🏠 Bought {new_sq['name']} (-${price}){extra_label} [via Card]"
                                p['stats']['critical_moments'].append({'turn': st.session_state.turn_count, 'event': event_text})
                                
                                msg += f" Then bought {new_sq['name']}."
        
        elif sq['name'] == "Free Parking" and st.session_state.rules["fp_jackpot"]:
            if st.session_state.jackpot > 0:
                p['cash'] += st.session_state.jackpot
                msg += f"Collected Jackpot of ${st.session_state.jackpot}!"
                st.session_state.jackpot = st.session_state.rules["fp_initial"]
        
        # --- PHASE 2: END OF TURN TRACKER ---
        
        # 1. Handle house building (This handles the logic AND the Critical Moments logging)
        house_msg = attempt_buy_houses(p) 
        if house_msg:
            msg += f" {house_msg}"

        # 2. Finalize the UI message for the 'Last Move' ticker
        if not silent: 
            st.session_state.last_move = msg
            
        # 3. Record wealth snapshot for the graph
        for player in st.session_state.players:
            player['stats']['cash_history'].append(player['cash'])

        # 4. Record position stats
        p['stats']['visits'][str(p['pos'])] += 1
        p['stats']['ends'][str(p['pos'])] += 1

        record_master_turn(p, msg)

        # 5. Switch turn and increment turn count
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
                    "visits": {str(i): 0 for i in range(40)},
                    "ends": {str(i): 0 for i in range(40)},
                    "rent_paid": 0,
                    "rent_collected": 0,
                    "times_in_jail": 0,
                    "cash_history": [1500], # Initial starting value
                    "critical_moments": []  # <-- Change "events" to "critical_moments"
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
                # We check for the string version of the ID
                is_own = (st.session_state.ownership.get(str(pid)) == p_n)
                
                if cols[i+1].button(p_n, key=f"set_o_{pid}{p_n}", type="primary" if is_own else "secondary"):
                    # We SAVE as the string version of the ID
                    st.session_state.ownership[str(pid)] = "Bank" if is_own else p_n
                    st.rerun()
    
    with t2:
        for color, pids in COLOR_GROUPS.items():
            # 1. Safe owner lookup (handles number '1' or text '1')
            owners = []
            for p in pids:
                val = st.session_state.ownership.get(p) or st.session_state.ownership.get(str(p))
                owners.append(val)
            
            # 2. Strict Check: Hide the set unless a real player owns the WHOLE thing
            if len(set(owners)) == 1 and owners[0] not in ["Bank", None, "None", ""]:
                st.markdown(f'<div style="background:{COLOR_MAP[color]}; padding:5px; border-radius:3px; color:white;"><b>{color} Group ({owners[0]})</b></div>', unsafe_allow_html=True)
                
                for pid in pids:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    
                    # 3. Safe house count lookup
                    h = st.session_state.houses.get(pid, 0) if pid in st.session_state.houses else st.session_state.houses.get(str(pid), 0)
                    
                    # 4. Get house counts for others in the set (for even-building rules)
                    others = []
                    for p in pids:
                        if p != pid:
                            val_h = st.session_state.houses.get(p, 0) if p in st.session_state.houses else st.session_state.houses.get(str(p), 0)
                            others.append(val_h)
                    
                    # 5. Logic for the +/- buttons
                    can_down = h > 0 and all(h >= o for o in others)
                    can_up = h < 5 and all(h <= o for o in others)
                    
                    if c2.button("➖", key=f"hm{pid}", disabled=not can_down): 
                        key = pid if pid in st.session_state.houses else str(pid)
                        st.session_state.houses[key] -= 1
                        st.rerun()
                        
                    c3.write(f"**{h}**")
                    
                    if c4.button("➕", key=f"hp_{pid}", disabled=not can_up): 
                        key = pid if pid in st.session_state.houses else str(pid)
                        st.session_state.houses[key] += 1
                        st.rerun()
    
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
        import copy 
        
        # --- SAFE MODE: Ensure every player has the full policy set ---
        for p in st.session_state.players:
            # Check for keys missing from previous versions of the app
            if 'build_res' not in p['policy']: p['policy']['build_res'] = 500
            if 'build_house' not in p['policy']: p['policy']['build_house'] = "Always"
            if 'sell_house' not in p['policy']: p['policy']['sell_house'] = "Never"
            if 'jail_exit' not in p['policy']: p['policy']['jail_exit'] = "Try Doubles"
            
            # Initialize the first data point for the graph
            p['stats']['cash_history'] = [p['cash']]
        
        # --- THE CHANGE: CREATE THE SAVE POINT ---
        # This now saves the policies we just verified/added above
        st.session_state.starting_players = copy.deepcopy(st.session_state.players)
        
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
    if c1.button("Standard Simulation"):
        import copy
        st.session_state.players = []
        for name in st.session_state.p_names:
            st.session_state.players.append({
                "name": name,
                "cash": 1500,
                "pos": 0,
                "in_jail": False,     # Added for consistency
                "jail_turns": 0,
                "goo_cards": [],      # Added for consistency
                "policy": {
                    "buy_prop": "Always", 
                    "buy_res": 500,
                    "build_res": 500,      
                    "build_house": "Always", 
                    "sell_house": "Never",
                    "jail_exit": "Try Doubles"
                },
                "stats": {            # FULL SYNC WITH RESTART_GAME()
                    "visits": {str(i): 0 for i in range(40)},
                    "ends": {str(i): 0 for i in range(40)},
                    "rent_paid": 0,
                    "rent_collected": 0,
                    "times_in_jail": 0,
                    "cash_history": [1500],
                    "critical_moments": []
                }
            })
        
        st.session_state.starting_players = copy.deepcopy(st.session_state.players)
        st.session_state.phase = "LIVE"
        st.rerun()
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
            if p.get('in_jail'): 
                st.error(f"IN JAIL 🚔 (Attempts: {p['jail_turns']})")
            
            for c in p['goo_cards']: 
                st.success(f"GOOJF: {c['deck'].capitalize()}")
            
            # --- 1. Display Streets ---
            # This must be aligned with the 'if' and 'for' above
            for color_name, pids in COLOR_GROUPS.items():
                owned = []
                for pid in pids:
                    # Check for the ID as a number AND as a string
                    raw_owner = st.session_state.ownership.get(pid) or st.session_state.ownership.get(str(pid))
                    
                    # Normalize both names to ensure a perfect match
                    if raw_owner and str(raw_owner).strip().lower() == str(p['name']).strip().lower():
                        owned.append(pid)
                
                if owned:
                    hex_c = COLOR_MAP.get(color_name, "#eee")
                    st.markdown(f'<span style="color:{hex_c}">■</span> <b>{color_name}</b>', unsafe_allow_html=True)
                    
                    # Monopoly check: Do they own the whole group?
                    is_mono = (len(owned) == len(pids))
                    
                    prop_labels = []
                    for pid in owned:
                        p_data = PROPERTIES.get(pid)
                        if p_data:
                            label = p_data['name']
                            if is_mono:
                                # Safe house lookup using both key types
                                h_count = st.session_state.houses.get(pid) or st.session_state.houses.get(str(pid)) or 0
                                label += f" ({h_count}🏠)"
                            prop_labels.append(label)
                    st.write(", ".join(prop_labels))

            # --- 2. Railroads (Reverting to your original working logic) ---
            owned_rr = [pid for pid in RAILROADS if st.session_state.ownership.get(pid) == p['name'] or st.session_state.ownership.get(str(pid)) == p['name']]
            if owned_rr:
                rr_names = [PROPERTIES[pid]['name'] for pid in owned_rr if pid in PROPERTIES]
                st.markdown(f"<b>🚂 Railroads ({len(owned_rr)})</b>", unsafe_allow_html=True)
                st.write(", ".join(rr_names))

            # --- 3. Utilities (Reverting to your original working logic) ---
            owned_util = [pid for pid in UTILITIES if st.session_state.ownership.get(pid) == p['name'] or st.session_state.ownership.get(str(pid)) == p['name']]
            if owned_util:
                util_names = [PROPERTIES[pid]['name'] for pid in owned_util if pid in PROPERTIES]
                st.markdown(f"<b>💡 Utilities ({len(owned_util)})</b>", unsafe_allow_html=True)
                st.write(", ".join(util_names))

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
            j_val = st.number_input("Turns to Jump", 1, 1000000, 100, label_visibility="collapsed", key="jump_input")
        with col_b:
            if st.button(f"Jump {j_val} Turns", use_container_width=True):
                # 1. Initialize the Progress Bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(j_val):
                    run_turn(silent=True)
                    
                    if i % 100 == 0 or i == j_val - 1:
                        percent = (i + 1) / j_val
                        progress_bar.progress(percent)
                        status_text.text(f"Processing turn {i+1} of {j_val}...")

                # --- CORRECTED STEP 3 (Only one cleanup block!) ---
                progress_bar.progress(1.0) 
                status_text.text(f"✅ Simulation Complete! {j_val} turns processed.")
                
                import time
                time.sleep(0.5) 
                
                progress_bar.empty()
                status_text.empty()
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
    
    # NEW: Added t_wealth to the unpacking and "📈 Wealth Curve" to the list
    t_visits, t_ends, t_fin, t_wealth = st.tabs([
        "🚶 Total Visits", "🛑 Turn Ends", "💰 Rent Flow", "📈 Wealth Curve"
    ])
    
    with t_visits:
        # (Your existing visit logic stays here)
        # Change p['stats']['visits'][i] to p['stats']['visits'][str(i)]
        visit_data = {
            f"{i:02d}: {PROPERTIES[i]['name']}": sum(p['stats']['visits'][str(i)] for p in st.session_state.players) 
            for i in range(40)
        }
        st.bar_chart(visit_data)

    with t_ends:
        # (Your existing ends logic stays here)
        ends_data = {f"{i:02d}: {PROPERTIES[i]['name']}": sum(p['stats']['ends'][str(i)] for p in st.session_state.players) for i in range(40)}
        st.bar_chart(ends_data)

    with t_fin:
        # (Your existing rent logic stays here)
        fin_list = []
        for p in st.session_state.players:
            fin_list.append({"Player": p['name'], "Type": "Collected", "Amount": p['stats']['rent_collected']})
            fin_list.append({"Player": p['name'], "Type": "Paid", "Amount": p['stats']['rent_paid']})
        if fin_list:
            import pandas as pd 
            df_fin = pd.DataFrame(fin_list)
            st.bar_chart(data=df_fin, x="Player", y="Amount", color="Type", stack=False)

    with t_wealth:
        # --- 8 SPACES START HERE ---
        import pandas as pd
        history_dict = {p['name']: p['stats']['cash_history'] for p in st.session_state.players}
        if history_dict:
            df_history = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in history_dict.items()]))
            st.line_chart(df_history)
    
        st.markdown("### 📥 Download Lab Data")
        excel_data = get_player_excel_data()
        st.download_button(
            label="Download Detailed Player Spreadsheets (Excel)",
            data=excel_data,
            file_name=f"monopoly_wealth_turn_{st.session_state.turn_count}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("📊 Player Game Highlights")
        
        if "players" in st.session_state:
            # 1. Individual Player Expanders (Visual UI remains for highlights)
            cols = st.columns(len(st.session_state.players))
        
            for i, p in enumerate(st.session_state.players):
                with cols[i]:
                    with st.expander(f"📜 {p['name']} Log", expanded=False):
                        st.write(f"**Times in Jail:** {p['stats'].get('times_in_jail', 0)}")
                        st.divider()
                        
                        moments = p['stats'].get('critical_moments', [])
                        if moments:
                            for e in moments:
                                st.markdown(f"**Turn {e['turn']}:** {e['event']}")
                        else:
                            st.caption("No significant events recorded.")
        
            # 2. UPDATED: The Full Master Log Download
            # We check the master_log we built in run_turn instead of just the highlights
            if st.session_state.get('master_log'):
                df_master = pd.DataFrame(st.session_state.master_log)
                # Sort by turn so the CSV reads like a book
                df_master = df_master.sort_values("Turn", ascending=True)
                csv_data = df_master.to_csv(index=False).encode('utf-8')
                
                st.write("") # Spacer
                st.download_button(
                    label="📥 Download Full Simulation Log (CSV)",
                    data=csv_data,
                    file_name=f"monopoly_full_play_by_play_{st.session_state.turn_count}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No turns recorded in the master log yet.")
        else:
            st.info("Game not initialized.")
        # --- 8 SPACES END HERE ---

    # --- 4 SPACES START HERE (Back 4 spaces) ---
    # These are now outside the tab, but still inside the LIVE phase
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 RESTART GAME (Keep Policies)", use_container_width=True):
        if "starting_players" in st.session_state:
            restart_game()
        else:
            st.sidebar.warning("No active simulation to restart!")

    if st.sidebar.button("⚠️ RESET SIMULATION (Full Wipe)", type="secondary", use_container_width=True):
        reset_lab()

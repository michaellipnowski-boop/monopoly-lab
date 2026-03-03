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
    # 🏦 FIXED: Standardize the name to match Dashboard and Excel functions
    st.session_state.bank_audit = []

#--- SPREADSHEET FUNCTIONALITY ---
def get_full_log_excel():
    import io
    import pandas as pd
    
    if not st.session_state.get('master_log'):
        return None

    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            # Standard formats
            money_fmt = workbook.add_format({'num_format': '$#,##0', 'align': 'center'})
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
            
            # --- TAB 1: THE MASTER PLAY-BY-PLAY ---
            df_master = pd.DataFrame(st.session_state.master_log)
            df_master.to_excel(writer, sheet_name="0_Full_Play_by_Play", index=False)
            ws_master = writer.sheets["0_Full_Play_by_Play"]
            ws_master.set_column('F:F', 70) # Wide Action column
            ws_master.set_column('E:E', 15, money_fmt) # Cash column

            # --- TAB 2: THE GLOBAL BANKER'S AUDIT ---
            if 'bank_audit' in st.session_state and st.session_state.bank_audit:
                df_audit = pd.DataFrame(st.session_state.bank_audit)
                df_audit.to_excel(writer, sheet_name="1_Bank_Master_Ledger", index=False)
                ws_audit = writer.sheets["1_Bank_Master_Ledger"]
                ws_audit.set_column('D:E', 25, money_fmt)
                
                # Filtered Injections/Sinks Sub-Tabs
                df_injections = df_audit[df_audit['Contribution to Net Liquidity'] > 0]
                if not df_injections.empty:
                    df_injections.to_excel(writer, sheet_name="2_Injections_GO_Cards", index=False)

                df_sinks = df_audit[df_audit['Contribution to Net Liquidity'] < 0]
                if not df_sinks.empty:
                    df_sinks.to_excel(writer, sheet_name="3_Sinks_Assets_Taxes", index=False)

            # --- TAB 3: INDIVIDUAL PLAYER TABS (THE ECONOMIC FOOTPRINT) ---
            for i, p in enumerate(st.session_state.players):
                p_audit = [e for e in st.session_state.bank_audit if e['Player'] == p['name']]
                
                if p_audit:
                    df_p = pd.DataFrame(p_audit)
                    
                    # 🟢 Running Total unique to the student's tab
                    df_p['Running Liquidity (Tab Only)'] = df_p['Contribution to Net Liquidity'].cumsum()
                    
                    if 'Player' in df_p.columns:
                        df_p = df_p.drop(columns=['Player'])
                    
                    clean_name = "".join(filter(str.isalnum, p['name']))[:20]
                    safe_sheet_name = f"P{i}_{clean_name}_Audit"
                    df_p.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                    
                    # Format the student's tab
                    ws_p = writer.sheets[safe_sheet_name]
                    ws_p.set_column('B:B', 45) # Reason
                    ws_p.set_column('C:D', 25, money_fmt) # Money columns
                    # Add an auto-filter so students can sort by Turn or Amount
                    ws_p.autofilter(0, 0, len(df_p), len(df_p.columns) - 1)

        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Excel Export Error: {e}")
        return None

def log_bank_transaction(p_name, reason, amount):
    """
    Records interaction with the central bank. 
    Amounts entering the system (Go, Income) are positive.
    Amounts exiting the system (Property, Tax, Houses) are negative.
    """
    if 'bank_audit' not in st.session_state:
        st.session_state.bank_audit = []
    
    prev_total = st.session_state.bank_audit[-1]['Running Liquidity (Global)'] if st.session_state.bank_audit else 0
    new_global_total = prev_total + amount

    st.session_state.bank_audit.append({
        "Turn": st.session_state.get('turn_count', 0),
        "Player": p_name,
        "Event": reason,        # 🟢 UI Compatible Key
        "Reason": reason,       # Keep your original key
        "Amount": amount,       # 🟢 UI Compatible Key
        "Contribution to Net Liquidity": amount, # Keep your original key
        "Running Liquidity (Global)": new_global_total
    })
    

#--- GAME RESET ---
def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def restart_game():
    import copy
    import random
    import streamlit as st

    # 1. Restore Board and Game State FROM BLUEPRINT
    st.session_state.ownership = copy.deepcopy(st.session_state.get('starting_ownership', {}))
    st.session_state.houses = copy.deepcopy(st.session_state.get('starting_houses', {}))

    # 🏦 BANKER'S AUDIT: Full wipe
    st.session_state.bank_audit = []
    st.session_state.master_log = [] 
    
    # 🟢 SYNC FIX: Set turn_count to 0 so the Sidebar and Log start at the same "Baseline"
    st.session_state.turn_count = 0
    st.session_state.current_p = 0
    st.session_state.double_count = 0
    st.session_state.jackpot = st.session_state.rules.get("fp_initial", 0)
    st.session_state.last_move = "Game Restarted - Rules and custom setup restored."
    
    st.session_state.property_stats = {
        str(idx): {"revenue": 0, "expenses": 0} for idx in range(40)
    }

    # 2. Reshuffle Decks
    st.session_state.c_deck_idx = list(range(16))
    random.shuffle(st.session_state.c_deck_idx)
    st.session_state.ch_deck_idx = list(range(16))
    random.shuffle(st.session_state.ch_deck_idx)

    # 3. Smart Player Reset
    if "players" in st.session_state and "starting_players" in st.session_state:
        for i, p in enumerate(st.session_state.players):
            start_snap = st.session_state.starting_players[i]
            
            p['cash'] = start_snap.get('cash', 1500)
            p['pos'] = start_snap.get('pos', 0)
            p['in_jail'] = start_snap.get('in_jail', False)
            p['jail_turns'] = start_snap.get('jail_turns', 0)
            p['goo_cards'] = copy.deepcopy(start_snap.get('goo_cards', []))

            # 🏦 AUDIT: Initial Cash Injection
            log_bank_transaction(p['name'], "Initial Cash (Restart)", p['cash'])

            # STATS WIPE
            p['stats'] = {
                "visits": {str(idx): 0 for idx in range(40)},
                "ends": {str(idx): 0 for idx in range(40)},
                "rent_paid": 0, "rent_collected": 0, "times_in_jail": 0,
                "cash_history": [p['cash']], 
                "critical_moments": []
            }

            # 📜 LOG: Changed to Turn 0 for Sidebar Sync
            st.session_state.master_log.append({
                "Turn": 0,
                "Player": p['name'],
                "Position": p['pos'],
                "Square": PROPERTIES[p['pos']]['name'],
                "Cash": p['cash'],
                "Action": f"RESTART: Started with ${p['cash']}"
            })

        # --- LOOP B: ACCOUNT FOR PROPERTY SINKS ---
        for prop_id, owner_name in st.session_state.ownership.items():
            if owner_name and owner_name != "Bank":
                p_info = PROPERTIES[int(prop_id)]
                p_name = p_info['name']
                
                # 🏦 AUDIT: Property/House values subtracted from Bank liquidity
                price = p_info.get('price', 150)
                log_bank_transaction(owner_name, f"Parachute Asset: {p_name}", -price)
                
                h_count = st.session_state.houses.get(str(prop_id), 0)
                if h_count > 0:
                    h_cost = p_info.get('h_cost', 50)
                    total_h_val = h_count * h_cost
                    log_bank_transaction(owner_name, f"Parachute Houses: {p_name}", -total_h_val)
                
                # 📜 LOG: Record the asset restoration as Turn 0
                st.session_state.master_log.append({
                    "Turn": 0,
                    "Player": owner_name,
                    "Position": p_info.get('pos', int(prop_id)),
                    "Square": p_name,
                    "Cash": "N/A", # Asset value is already deducted from cash above
                    "Action": f"SETUP RESTORED: {p_name} assigned"
                })

    st.session_state.phase = "LIVE"
    st.rerun()

def get_house_count(pid):
    # Checks for "1" then checks for 1. Returns 0 if neither found.
    return st.session_state.houses.get(str(pid), st.session_state.houses.get(int(pid), 0))

def get_owner(pid):
    # Checks for "1" then checks for 1. Returns "Bank" if neither found.
    return st.session_state.ownership.get(str(pid), st.session_state.ownership.get(int(pid), "Bank"))

def get_effective_reserve(p, action_context):
    """
    Calculates the cash floor based on player policy and global rules.
    action_context: 'buy_prop' or 'build_house'
    """
    # 🟢 KEY FIX: Map the context to the correct policy key
    if action_context == 'buy_prop':
        pol = p['policy'].get('buy_prop', "Always")
        res_key = 'buy_res'
    else: # 'build_house'
        pol = p['policy'].get('build_house', "Always")
        res_key = 'build_res'
    
    # 1. Determine the base reserve
    if pol == "Keep Reserve":
        reserve = p['policy'].get(res_key, 500)
    elif pol == "Never":
        # If policy is Never, the reserve is effectively infinite 
        # (though run_turn handles "Never" earlier, this is a safe backup)
        reserve = float('inf')
    else:
        # "Always" players have no floor
        reserve = -float('inf')
    
    # 2. Factor in Global Rules (Debt protection)
    # Note: Use the exact key from your rules dict (allow_debt)
    global_allow_debt = st.session_state.rules.get("allow_debt", True)
    if not global_allow_debt:
        # If debt is NOT allowed, the floor can never be lower than 0
        return max(0, reserve)
        
    return reserve

# --- DEBUGGER ---
def verify_sim_integrity():
    total_turns = st.session_state.turn_count
    total_visits = sum(sum(p['stats']['visits'].values()) for p in st.session_state.players)
    
    # This displays it nicely in the Streamlit UI
    st.sidebar.divider()
    st.sidebar.subheader("System Integrity")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Turns", total_turns)
    col2.metric("Visits", total_visits)
    
    if total_visits < total_turns:
        st.sidebar.error("⚠️ Data Leak Detected")


# --- HELPER LOGIC ---
def charge_player(p, amt):
    # 1. Deduct the cash
    p['cash'] -= amt
    
    # 🏦 JACKPOT LOGIC
    # If the Jackpot rule is on, money goes to the center of the board, 
    # not the Bank's vault.
    if st.session_state.rules.get("fp_jackpot", False) and amt > 0:
        st.session_state.jackpot += amt
        # We do NOT log_bank_transaction here because the money 
        # is still "in the game" (on the Free Parking square).
    
    # 🟢 2. Debt Alert (Internal logging)
    if p['cash'] < 0:
        event_text = f"🚨 Went into DEBT (-${abs(p['cash'])}) after paying ${amt}"
        if 'critical_moments' in p['stats']:
            # Prevent spamming debt messages if they are already in debt
            if not any("DEBT" in m['event'] for m in p['stats']['critical_moments'][-1:]):
                p['stats']['critical_moments'].append({
                    'turn': st.session_state.turn_count, 
                    'event': event_text
                })

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    
    # 🟢 SURGERY: Use helpers to resolve ownership and house counts immediately
    owner = get_owner(pid)
    
    if not owner or owner == "Bank":
        return 0

    owner_norm = str(owner).strip().lower()

    # 1. STREETS (Houses & Monopolies)
    if info['type'] == "Street":
        # 🟢 SURGERY: Use helper here too
        h = get_house_count(pid)
        
        rent_list = info.get('rent', [0])
        base = rent_list[min(h, len(rent_list)-1)]
        
        # Monopoly check (Double rent for 0 houses)
        if h == 0:
            group = COLOR_GROUPS.get(info['color'], [])
            owned_in_group = 0
            for g_id in group:
                curr = get_owner(g_id)
                if curr and str(curr).strip().lower() == owner_norm:
                    owned_in_group += 1
            if owned_in_group == len(group) and len(group) > 0:
                return base * 2
        return base

    # 2. RAILROADS
    elif info['type'] == "Railroad":
        count = 0
        for r_id in [5, 15, 25, 35]:
            curr = get_owner(r_id)
            if curr and str(curr).strip().lower() == owner_norm:
                count += 1
        r_rents = info.get('rent', [25, 50, 100, 200])
        return r_rents[max(0, min(count-1, len(r_rents)-1))]

    # 3. UTILITIES
    elif info['type'] == "Utility":
        count = 0
        for u_id in [12, 28]:
            curr = get_owner(u_id)
            if curr and str(curr).strip().lower() == owner_norm:
                count += 1
        
        multiplier = 4 if count == 1 else 10
        return multiplier * roll

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
    actions = []
    # 1. Identify all color groups
    color_groups = {}
    for idx, sq in PROPERTIES.items(): 
        if isinstance(sq, dict) and sq.get('type') == "Street":
            color = sq.get('color')
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(str(idx))

    for color, indices in color_groups.items():
        # 1. Count ownership
        player_owned_count = 0
        for idx in indices:
            owner_name = get_owner(idx)
            if owner_name and str(owner_name).strip().lower() == str(p['name']).strip().lower():
                player_owned_count += 1
        
        # 2. Monopoly Check
        total_in_set = len(indices)
        is_monopoly = (player_owned_count == total_in_set) and (total_in_set > 0)
        
        if is_monopoly:
            # Monopoly Trophy (Once per color)
            monopoly_key = f"monopoly_achieved_{color}"
            if not p['stats'].get(monopoly_key):
                p['stats'][monopoly_key] = True
                if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                p['stats']['critical_moments'].append({
                    'turn': st.session_state.turn_count, 
                    'event': f"🏆 MONOPOLY: {color} set completed!"
                })

            # Building Policy Check
            if p['policy'].get('build_house') == "Never":
                continue 

            while True:
                # 🟢 SAFE SYNC: Ensure we get the latest counts (AI + Manual UI)
                counts = [get_house_count(idx) for idx in indices]
                
                if all(c >= 5 for c in counts): 
                    break 
                
                # Identify property with fewest houses to build evenly
                target_idx = indices[counts.index(min(counts))]
                sq = PROPERTIES[int(target_idx)]
                h_price = sq.get('h_cost', 50) 
                
                effective_floor = get_effective_reserve(p, 'build_house')

                # Decision Logic
                if (p['cash'] - h_price) >= effective_floor:
                    p['cash'] -= h_price
                    
                    current_h = get_house_count(target_idx)
                    new_count = current_h + 1
                    label = "Hotel" if new_count == 5 else f"House {new_count}"

                    # 🏦 BANKER'S AUDIT
                    log_bank_transaction(p['name'], f"Built {label} on {sq['name']}", -h_price)
                    
                    # Update house count in state (Force String Key)
                    st.session_state.houses[str(target_idx)] = new_count
                    
                    # Update logs
                    actions.append(f"{label} on {sq['name']}")
                    if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                    p['stats']['critical_moments'].append({
                        'turn': st.session_state.turn_count, 
                        'event': f"🏗️ Built {label} on {sq['name']} (-${h_price})"
                    })
                else:
                    break

    if actions:
        return "🏗️ Built: " + ", ".join(actions) + "."
    return ""

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
            # 🏦 BANKER'S AUDIT: Record the salary from a card move
            log_bank_transaction(p['name'], "Passed GO (via Card)", 200)
            
        p['stats']['visits'][str(p['pos'])] += 1
            
    elif card['effect'] == "jail":
        send_to_jail(p)
        
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
        # --- ADD THIS LINE ---
        p['stats']['visits'][str(p['pos'])] += 1
        
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
        if p['pos'] < old_pos: 
            p['cash'] += 200
            # 🏦 ADD THIS:
            log_bank_transaction(p['name'], "Passed GO (Nearest RR Card)", 200)
        p['stats']['visits'][str(p['pos'])] += 1
        
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        old_pos = p['pos']
        p['pos'] = int(min([u for u in targets if u > p['pos']] or [12]))
        if p['pos'] < old_pos: 
            p['cash'] += 200
            # 🏦 ADD THIS:
            log_bank_transaction(p['name'], "Passed GO (Nearest Util Card)", 200)
        p['stats']['visits'][str(p['pos'])] += 1

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
                
    # --- POST-MOVE EVALUATION (The Policy Leak Fix) ---
    # If the card moved the player, we must check if they want to buy the new property
    move_effects = ["move", "move_relative", "move_nearest_rr", "move_nearest_util"]
    if card['effect'] in move_effects:
        sq = PROPERTIES[p['pos']]
        owner = st.session_state.ownership.get(str(p['pos']), "Bank")
        
        if owner == "Bank" and sq['type'] in ["Street", "Railroad", "Utility"]:
            price = sq.get('price', 150)
            pol = p['policy'].get('buy_prop', "Always")
            
            should_buy_card = False
            # 🟢 Apply the exact same logic as your dice rolls
            if pol == "Never":
                msg += f" 🚫 (Policy: Never Buy Properties - skipped {sq['name']} after card move)."
            elif pol == "Always":
                should_buy_card = True
            elif pol == "Keep Reserve":
                floor = get_effective_reserve(p, 'buy_prop')
                if p['cash'] - price >= floor:
                    should_buy_card = True
                else:
                    msg += f" 💰 (Policy: Reserve - skipped {sq['name']} after card move)."
            
            # 🟢 EXECUTE PURCHASE
            if should_buy_card and p['cash'] >= price:
                st.session_state.ownership[str(p['pos'])] = p['name']
                p['cash'] -= price

                # 🏦 ADD THIS LINE: Banker's Audit for Card Purchases
                log_bank_transaction(p['name'], f"Bought {sq['name']} (Card)", -price)
                
                # Log to stats
                if "property_stats" in st.session_state:
                    st.session_state.property_stats[str(p['pos'])]["expenses"] += price
                
                event_text = f"🏠 Bought {sq['name']} (-${price}) via card"
                if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                p['stats']['critical_moments'].append({'turn': st.session_state.turn_count, 'event': event_text})
                msg += f" {event_text}."
        
    return msg

def record_master_turn(p, msg):
    """Utility to capture the full state of a turn for the CSV log."""
    if "master_log" not in st.session_state:
        st.session_state.master_log = []
        
    # 🟢 SAFE LOOKUP: Ensures the Square name is found without crashing
    try:
        current_square = PROPERTIES[p['pos']]['name']
    except (IndexError, KeyError, TypeError):
        current_square = "N/A"

    st.session_state.master_log.append({
        "Turn": st.session_state.turn_count,
        "Player": p['name'],
        "Position": p['pos'],
        "Square": current_square,
        "Cash": p['cash'],
        "Action": msg.strip()
    })


def run_turn(jail_action=None, silent=False):
    # 🟢 SYNC FIX: Every time this function is called, the turn counter advances.
    st.session_state.turn_count += 1
    
    p = st.session_state.players[st.session_state.current_p]
    
    # --- 1. THE DEBT CHECK (Safe Mode Sync) ---
    if not st.session_state.rules["allow_debt"] and p['cash'] < 0:
        # Record wealth for all players so history lengths stay equal
        for player in st.session_state.players:
            player['stats']['cash_history'].append(player['cash'])

        msg = f"Turn skipped: {p['name']} is bankrupt/in debt."
        record_master_turn(p, msg)
        
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return
    
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    roll_sum = d1 + d2
    is_double = (d1 == d2)
    
    # --- 2. JAIL LOGIC ---
    if p.get('in_jail'):
        if jail_action is None:
            if p['goo_cards']: jail_action = "Use Card"
            elif p['policy']['jail_exit'] == "Pay Immediately" and p['cash'] >= 50: jail_action = "Pay $50"
            elif p['jail_turns'] >= 2: jail_action = "Pay $50"
            else: jail_action = "Try Doubles"
        
        if jail_action == "Pay $50":
            charge_player(p, 50)
            log_bank_transaction(p['name'], "Jail Exit Fee", -50)
            p['in_jail'] = False
        elif jail_action == "Use Card":
            card = p['goo_cards'].pop(0)
            if card['deck'] == "chance": st.session_state.c_deck_idx.append(card['index'])
            else: st.session_state.ch_deck_idx.append(card['index'])
            p['in_jail'] = False
        else: # Try Doubles
            if is_double:
                p['in_jail'] = False # Escaped! We allow the code to flow to movement below.
            elif p['jail_turns'] >= 2:
                charge_player(p, 50)
                log_bank_transaction(p['name'], "Jail Exit Fee", -50)
                p['in_jail'] = False
            else: # Failed to roll doubles
                p['jail_turns'] += 1
                p['stats']['visits'][str(10)] += 1
                p['stats']['ends'][str(10)] += 1
                for player in st.session_state.players:
                    player['stats']['cash_history'].append(player['cash'])
                record_master_turn(p, f"{p['name']} stays in Jail.")
                st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
                return

    # --- 3. MOVEMENT LOGIC ---
    if is_double and not p.get('in_jail'):
        st.session_state.double_count += 1
    else:
        st.session_state.double_count = 0
    
    if st.session_state.double_count >= 3:
        send_to_jail(p)
        msg = f"{p['name']} rolled 3 doubles! Go to Jail!" 
        for player in st.session_state.players:
            player['stats']['cash_history'].append(player['cash'])
        record_master_turn(p, msg)
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return

    old_pos = p['pos']
    p['pos'] = (p['pos'] + roll_sum) % 40
    p['stats']['visits'][str(p['pos'])] += 1
    
    # Pass Go Check
    if p['pos'] < old_pos or (old_pos > 30 and p['pos'] == 0):
        salary = 400 if (st.session_state.rules["double_go"] and p['pos'] == 0) else 200
        p['cash'] += salary
        log_bank_transaction(p['name'], "Passed GO (Salary)", salary)

    sq = PROPERTIES.get(p['pos'])
    msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "

    # --- 4. SQUARE INTERACTION ---
    if sq['type'] in ["Street", "Railroad", "Utility", "Property"]:
        owner = st.session_state.ownership.get(str(p['pos']), "Bank")
        if owner != "Bank" and str(owner).lower() != str(p['name']).lower():
            rent = get_rent(p['pos'], roll=roll_sum)
            p['cash'] -= rent
            p['stats']['rent_paid'] += rent
            # Transfer rent to owner
            for op in st.session_state.players:
                if str(op['name']).lower() == str(owner).lower():
                    op['cash'] += rent
                    op['stats']['rent_collected'] += rent
            msg += f"Paid ${rent} rent to {owner}. "
        elif owner == "Bank":
            price = sq.get('price', 150)
            # Standard Dice Purchase
            if p['policy']['buy_prop'] != "Never" and p['cash'] >= price:
                # Re-check reserve policy
                floor = get_effective_reserve(p, 'buy_prop')
                if p['policy']['buy_prop'] != "Keep Reserve" or (p['cash'] - price >= floor):
                    st.session_state.ownership[str(p['pos'])] = p['name']
                    p['cash'] -= price
                    log_bank_transaction(p['name'], f"Bought {sq['name']}", -price)
                    msg += f"🏠 Bought {sq['name']} (-${price})."

    elif sq['type'] == "Tax":
        tax = sq.get('cost', 100)
        charge_player(p, tax)
        log_bank_transaction(p['name'], f"Paid {sq['name']}", -tax)
        msg += f"Paid {sq['name']} (${tax})."

    elif sq['type'] == "Action":
        if p['pos'] == 30:
            send_to_jail(p)
            msg += "Go To Jail!"
        else:
            # Delegate movement and card-purchases to draw_card
            card_msg = draw_card(p, sq.get('deck', 'chance'))
            msg += f" {card_msg}"

    elif sq['name'] == "Free Parking" and st.session_state.rules["fp_jackpot"]:
        if st.session_state.jackpot > 0:
            p['cash'] += st.session_state.jackpot
            log_bank_transaction(p['name'], "Collected Jackpot", st.session_state.jackpot)
            msg += f"Collected Jackpot of ${st.session_state.jackpot}!"
            st.session_state.jackpot = st.session_state.rules["fp_initial"]

    # --- 5. WRAP UP ---
    house_msg = attempt_buy_houses(p) # Also logs its own Banker Audit transactions
    if house_msg: msg += f" {house_msg}"
    
    if not silent: st.session_state.last_move = msg
    
    # 🟢 CRITICAL SYNC: All player history lists must grow together
    for player in st.session_state.players:
        player['stats']['cash_history'].append(player['cash'])
    
    p['stats']['ends'][str(p['pos'])] += 1
    record_master_turn(p, msg)

    # Move to next player if not doubles (or if in jail)
    if not is_double or p.get('in_jail'):
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
            

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
                buy_opts = ["Always", "Keep Reserve", "Never"]
                # 🟢 Look up the current saved policy to find its position (0, 1, or 2)
                curr_b = p['policy'].get('buy_prop', "Always")
                # This line finds the index so the dropdown "stays" on your choice
                b_idx = buy_opts.index(curr_b) if curr_b in buy_opts else 0
                
                p['policy']['buy_prop'] = st.selectbox(
                    "Property Buying", buy_opts, index=b_idx, key=f"pol_b_{i}"
                )
                
                if p['policy']['buy_prop'] == "Keep Reserve":
                    p['policy']['buy_res'] = st.number_input(
                        "Reserve ($)", 0, 5000, 
                        value=p['policy'].get('buy_res', 500), 
                        step=50, key=f"pol_br_{i}"
                    )
        
            with col2:
                build_opts = ["Always", "Keep Reserve", "Never"]
                curr_h = p['policy'].get('build_house', "Always")
                h_idx = build_opts.index(curr_h) if curr_h in build_opts else 0
                
                p['policy']['build_house'] = st.selectbox(
                    "House Building", build_opts, index=h_idx, key=f"pol_h_{i}"
                )
                
                if p['policy']['build_house'] == "Keep Reserve":
                    p['policy']['build_res'] = st.number_input(
                        "Reserve ($)", 0, 5000, 
                        value=p['policy'].get('build_res', 500), 
                        step=50, key=f"pol_hr_{i}"
                    )

            with col3:
                jail_opts = ["Try Doubles", "Pay Immediately"]
                curr_j = p['policy'].get('jail_exit', "Try Doubles")
                j_idx = jail_opts.index(curr_j) if curr_j in jail_opts else 0
                
                p['policy']['jail_exit'] = st.selectbox(
                    "Jail Strategy", jail_opts, index=j_idx, key=f"pol_j_{i}"
                )
                
    if st.button("Proceed to Mode Selection"):
        # 🟢 THE FORCE-SAVE: Explicitly push UI values into the player objects
        # before we change the phase.
        for i, p in enumerate(st.session_state.players):
            p['policy']['buy_prop'] = st.session_state.get(f"pol_b_{i}", p['policy']['buy_prop'])
            p['policy']['build_house'] = st.session_state.get(f"pol_h_{i}", p['policy']['build_house'])
            p['policy']['jail_exit'] = st.session_state.get(f"pol_j_{i}", p['policy']['jail_exit'])
            # Do the same for reserves if you use them
            if f"pol_br_{i}" in st.session_state:
                p['policy']['buy_res'] = st.session_state[f"pol_br_{i}"]
        
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
            # 1. Force everything to strings for a clean lookup
            owners = [st.session_state.ownership.get(str(p), "Bank") for p in pids]
            
            # 2. Strict Check: If the set length is 1, everyone in the list is the same owner
            if len(set(owners)) == 1 and owners[0] not in ["Bank", None, "None", ""]:
                # THE UI WILL NOW APPEAR
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

    if st.button("Start Live Simulation", type="primary", use_container_width=True):
        import copy 
    
        # --- 📸 0. THE BOARD BLUEPRINT ---
        # Normalize house keys to strings for reliable lookup
        current_houses = {str(k): v for k, v in st.session_state.houses.items()}
        st.session_state.starting_houses = copy.deepcopy(current_houses)
        st.session_state.starting_ownership = copy.deepcopy(st.session_state.ownership)
        
        # Initialize Audit & Logs
        st.session_state.master_log = []
        st.session_state.bank_audit = [] 
        st.session_state.turn_count = 0 
    
        # 🟢 STEP 1: Loop through players to set their Economic Footprint
        for p in st.session_state.players:
            # 🛡️ WEALTH CURVE PROTECTION: Graph starts at the set Cash value
            p['stats']['cash_history'] = [p['cash']]
            p['stats']['critical_moments'] = []

            # 🏦 BANKER'S AUDIT: Injection (M1 Money Supply starts here)
            log_bank_transaction(p['name'], "SETUP: Starting Cash Injection", p['cash'])
    
            # Baseline Master Log Entry (Turn 0)
            st.session_state.master_log.append({
                "Turn": 0, "Player": p['name'], "Position": p['pos'],
                "Square": PROPERTIES[p['pos']]['name'], "Cash": p['cash'],
                "Action": f"SETUP: Started with ${p['cash']}"
            })
    
            # 🏗️ Record Assets (Land vs. Houses)
            for prop_id_str, owner_name in st.session_state.ownership.items():
                if owner_name == p['name']:
                    pid = int(prop_id_str)
                    p_info = PROPERTIES[pid]
                    p_name = p_info['name']
                    prop_price = p_info.get('price', 0)
                    
                    # 📜 1. Master Log: The Deed Assignment
                    st.session_state.master_log.append({
                        "Turn": 0, "Player": p['name'], "Position": p['pos'],
                        "Square": PROPERTIES[p['pos']]['name'], "Cash": p['cash'],
                        "Action": f"PARACHUTE ASSET: Began game owning {p_name}"
                    })
                    # 🏦 2. Banker's Audit: The Deed Sink
                    log_bank_transaction(p['name'], f"SETUP: Asset Deed ({p_name})", -prop_price)
    
                    # 🏠 3. Houses/Hotels (Consolidated per Property)
                    h_count = current_houses.get(str(pid), 0)
                    if h_count > 0:
                        h_price = p_info.get('house_price', p_info.get('h_cost', 50))
                        total_h_cost = h_count * h_price
                        label = "a HOTEL" if h_count == 5 else f"{h_count} House(s)"
                        
                        # 📜 Master Log: The Development Summary
                        st.session_state.master_log.append({
                            "Turn": 0, "Player": p['name'], "Position": p['pos'],
                            "Square": PROPERTIES[p['pos']]['name'], "Cash": p['cash'],
                            "Action": f"PARACHUTE SETUP: Started with {label} on {p_name}"
                        })
                        # 🏦 Banker's Audit: The Development Sink
                        log_bank_transaction(p['name'], f"SETUP: {label} on {p_name}", -total_h_cost)
        
        # 🏁 STEP 2: Finalize Snapshot and Launch the LIVE phase
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
        
        # 🏦 STEP 0: INITIALIZE AUDITS & BOARD (The Clean Slate)
        st.session_state.master_log = []
        st.session_state.bank_audit = [] 
        st.session_state.turn_count = 0 
        st.session_state.ownership = {}
        st.session_state.houses = {str(i): 0 for i in range(40)}
    
        # 🟢 STEP 1: Loop through EXISTING players to reset values
        for p in st.session_state.players:
            p['cash'] = 1500
            p['pos'] = 0
            p['in_jail'] = False
            p['jail_turns'] = 0
            p['goo_cards'] = []
            
            # 🛡️ NOTE: p['policy'] is PRESERVED here (Safe Mode)
    
            # 🏦 STEP 2: BANKER'S AUDIT (Record the $1500 Injection)
            log_bank_transaction(p['name'], "STANDARD SETUP: Starting Cash", 1500)
    
            # 📜 STEP 3: MASTER LOG (Record the Turn 0 Baseline)
            st.session_state.master_log.append({
                "Turn": 0, "Player": p['name'], "Position": 0,
                "Square": "GO", "Cash": 1500,
                "Action": "STANDARD SETUP: Game Start"
            })
    
            # STEP 4: Reset Stats for the fresh run
            p['stats'] = {
                "visits": {str(idx): 0 for idx in range(40)},
                "ends": {str(idx): 0 for idx in range(40)},
                "rent_paid": 0,
                "rent_collected": 0,
                "times_in_jail": 0,
                "cash_history": [1500],
                "critical_moments": []
            }
        
        # STEP 5: Create snapshot and launch
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
            # --- 🛡️ STRATEGY & RESERVES (SYNCED WITH ENGINE) ---
            
            # 1. Get Effective Reserves from your function
            buy_floor = get_effective_reserve(p, 'buy_prop')
            build_floor = get_effective_reserve(p, 'build_house')
            
            # 2. Helper to turn those numbers into your specific phrasing
            def get_policy_text(floor):
                if floor == float('inf'):
                    return "Blocked (Never)"
                if floor == -float('inf'):
                    return "Unlimited Debt" if st.session_state.rules.get("allow_debt") else "Zero-Cash Floor"
                if floor < 0:
                    return f"${abs(floor)} Debt Limit"
                return f"${floor} Cash Cushion"

            # 3. Color Coding
            buy_pol = p['policy'].get('buy_prop', 'Always')
            build_pol = p['policy'].get('build_house', 'Always')
            b_color = "red" if buy_pol == "Never" else "orange" if buy_pol == "Keep Reserve" else "green"
            h_color = "red" if build_pol == "Never" else "orange" if build_pol == "Keep Reserve" else "green"

            # 4. Display synchronized info
            st.markdown(f"**Prop Buying:** :{b_color}[{buy_pol}]")
            st.caption(f"🛡️ {get_policy_text(buy_floor)}")
            
            # Show "Spendable" only if there is a finite floor to calculate against
            if buy_floor not in [float('inf'), -float('inf')]:
                safe_cash = max(0, p['cash'] - buy_floor)
                st.caption(f"💰 Spendable: ${safe_cash}")

            st.markdown(f"**Building:** :{h_color}[{build_pol}]")
            st.caption(f"🏠 {get_policy_text(build_floor)}")

            st.markdown("---")
            
            if build_pol == "Keep Reserve":
                build_floor = max(global_limit, p['policy'].get('build_res', 0))
                st.caption(f"🏠 Build Floor: **${build_floor}**")
            
            st.markdown("---")

            # --- STATUS & CARDS ---
            if p.get('in_jail'): 
                st.error(f"IN JAIL 🚔 (Attempts: {p['jail_turns']})")
            
            for c in p['goo_cards']: 
                st.success(f"GOOJF: {c['deck'].capitalize()}")
            
            # --- 1. Display Streets (Using your successful Railroad logic style) ---
            for color_name, pids in COLOR_GROUPS.items():
                owned_ids = [pid for pid in pids if get_owner(pid) == p['name']]
                
                if owned_ids:
                    hex_c = COLOR_MAP.get(color_name, "#eee")
                    st.markdown(f'<span style="color:{hex_c}">■</span> <b>{color_name}</b>', unsafe_allow_html=True)
                    
                    is_mono = (len(owned_ids) == len(pids))
                    street_labels = []
                    for s_pid in owned_ids:
                        p_data = PROPERTIES.get(s_pid)
                        name = p_data['name'] if p_data else f"Prop {s_pid}"
                        if is_mono:
                            h_count = get_house_count(s_pid)
                            name += f" ({h_count}🏠)"
                        street_labels.append(name)
                    st.write(", ".join(street_labels))

            # --- 2. Railroads ---
            owned_rr = [pid for pid in RAILROADS if get_owner(pid) == p['name']]
            if owned_rr:
                rr_names = [PROPERTIES[pid]['name'] for pid in owned_rr if pid in PROPERTIES]
                st.markdown(f"<b>🚂 Railroads ({len(owned_rr)})</b>", unsafe_allow_html=True)
                st.write(", ".join(rr_names))

            # --- 3. Utilities ---
            owned_util = [pid for pid in UTILITIES if get_owner(pid) == p['name']]
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

   # --- PHASE 3: ANALYTICS DASHBOARD (Visuals Only) ---
    st.markdown("---")
    st.header("🔬 Stats Analytics")
    
    t_visits, t_ends, t_fin, t_wealth, t_bank = st.tabs([
        "🚶 Visits", "🛑 Ends", "💰 Rent", "📈 Wealth", "🏦 Banker's Audit"
    ])
    
    with t_visits:
        visit_data = {
            f"{i:02d}: {PROPERTIES[i]['name']}": sum(p['stats']['visits'].get(str(i), 0) for p in st.session_state.players) 
            for i in range(40)
        }
        st.bar_chart(visit_data)

    with t_ends:
        ends_data = {
            f"{i:02d}: {PROPERTIES[i]['name']}": sum(p['stats']['ends'].get(str(i), 0) for p in st.session_state.players) 
            for i in range(40)
        }
        st.bar_chart(ends_data)

    with t_fin:
        fin_list = []
        for p in st.session_state.players:
            fin_list.append({"Player": p['name'], "Type": "Collected", "Amount": p['stats']['rent_collected']})
            fin_list.append({"Player": p['name'], "Type": "Paid", "Amount": p['stats']['rent_paid']})
        if fin_list:
            df_fin = pd.DataFrame(fin_list)
            st.bar_chart(data=df_fin, x="Player", y="Amount", color="Type", stack=False)

    with t_wealth:
        # 1. Gather history
        history_dict = {p['name']: p['stats']['cash_history'] for p in st.session_state.players}
        
        # 🟢 THE FIX: Check if there is actually any DATA inside those history lists
        has_data = any(len(v) > 0 for v in history_dict.values())
        
        if not has_data:
            st.info("📈 Wealth Curve will appear here after the first turn.")
            st.warning("Note: At Turn 0, only 'Parachute' setup is recorded. Roll the dice to begin the trend!")
        else:
            # 2. Show the Visual Chart
            # Safe conversion: dict of series handles mismatched lengths perfectly
            df_history = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in history_dict.items()]))
            
            st.subheader("Player Net Liquidity Over Time")
            st.line_chart(df_history)
            
            st.divider()
            
            # 3. Add the ACTUAL Excel Export Button
            # 🟢 Use the 2026 Audit super-function
            excel_data = get_full_log_excel() 
            
            if excel_data:
                st.download_button(
                    label="📥 Download Detailed Player Audit (Multi-Tab Excel)",
                    data=excel_data,
                    file_name=f"monopoly_audit_turn_{st.session_state.turn_count}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key=f"wealth_tab_excel_btn_{st.session_state.turn_count}" 
                )

    with t_bank:
        st.header("🏦 Central Bank Audit")
        st.info("This ledger tracks the 'Money Supply'. Inflows (GO/Cards) increase liquidity; Outflows (Deeds/Houses/Taxes) sink capital into the bank.")

        # 🟢 THE FIX: Guard against empty lists or missing columns
        audit_list = st.session_state.get('bank_audit', [])
        
        if not audit_list:
            st.warning("No bank transactions recorded. Run a turn to see the audit!")
        else:
            # 1. Prepare Data
            df_bank = pd.DataFrame(audit_list)
            
            # 🟢 THE CRITICAL CHECK: Does 'Amount' actually exist in the data?
            if 'Amount' in df_bank.columns:
                # Calculate Metrics
                total_injected = df_bank[df_bank['Amount'] > 0]['Amount'].sum()
                total_sunk = abs(df_bank[df_bank['Amount'] < 0]['Amount'].sum())
                net_liquidity = total_injected - total_sunk
                
                # 2. Key Performance Indicators
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Injected (GO/Cards)", f"${total_injected}")
                m2.metric("Total Sunk (Assets/Taxes)", f"${total_sunk}")
                m3.metric("Net Game Liquidity", f"${net_liquidity}", 
                          delta="Inflationary" if net_liquidity > 0 else "Contractionary")

                st.divider()

                # 3. 📈 The Liquidity Curve
                st.subheader("Out of the Bank Over Time")
                df_bank['Running_Total'] = df_bank['Amount'].cumsum()
                df_bank['Breakeven'] = 0 
                
                st.line_chart(
                    df_bank, 
                    x="Turn", 
                    y=["Running_Total", "Breakeven"], 
                    color=["#FF4B4B", "#808080"]
                )
                st.caption("🔴 Red Line: Net Liquidity (Money in Game) | ⚪ Grey Line: Breakeven ($0 Horizon)")
                
                st.divider()

                # 4. 📋 The Raw Audit Table
                st.subheader("Transaction History")
                # Filter columns safely to avoid KeyError
                cols_to_show = [c for c in ['Turn', 'Player', 'Reason', 'Amount'] if c in df_bank.columns]
                st.dataframe(df_bank[cols_to_show], use_container_width=True, hide_index=True)
                
                # 5. 📥 The Download Button
                excel_data = get_full_log_excel()
                if excel_data:
                    st.download_button(
                        label="📥 Download Full Banker's Audit (Excel)",
                        data=excel_data,
                        file_name=f"bank_audit_turn_{st.session_state.turn_count}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                # If we have a list but it's malformed/empty DataFrame
                st.error("Audit data detected, but the 'Amount' column is missing. Run a turn to refresh.")
    

    # --- 📂 DATA WAREHOUSE & GAME HIGHLIGHTS ---
    st.markdown("---")
    st.header("📂 Data Warehouse & Game Highlights")

    if "players" in st.session_state and len(st.session_state.players) > 0:
        # A. PLAYER GAME HIGHLIGHTS
        with st.expander("🚩 Player Milestones & Critical Moments", expanded=True):
            cols = st.columns(len(st.session_state.players))
            for i, p in enumerate(st.session_state.players):
                with cols[i]:
                    with st.expander(f"👤 {p['name']} Details", expanded=False):
                        st.write(f"**Jail Stays:** {p['stats'].get('times_in_jail', 0)}")
                        st.divider()
                        moments = p['stats'].get('critical_moments', [])
                        if moments:
                            for e in moments:
                                st.markdown(f"**T{e['turn']}:** {e['event']}")
                        else:
                            st.caption("No significant events.")

        # Generate the Excel data once to be used by both buttons
        # This function now includes the "Individual Footprint" tabs automatically
        full_excel_data = get_full_log_excel() 

        # 📥 Button 1: Individual Audit Focus
        if full_excel_data:
            st.download_button(
                label="📥 Download Detailed Player Spreadsheets (Excel)",
                data=full_excel_data,
                file_name=f"monopoly_lab_audit_T{st.session_state.turn_count}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"audit_xl_btn_{st.session_state.turn_count}"
            )

        # 📜 Master Log Display
        with st.expander("📜 Full Play-by-Play Master Log", expanded=False):
            if st.session_state.get('master_log') and len(st.session_state.master_log) > 0:
                df_master = pd.DataFrame(st.session_state.master_log)
                # Ensure chronological order
                df_master["Turn"] = pd.to_numeric(df_master["Turn"], errors='coerce')
                df_master = df_master.sort_values(by=["Turn", "Player"], ascending=[True, True])
        
                st.dataframe(df_master, width="stretch", hide_index=True)
                st.write("") 
                
                # 📥 Button 2: Full Master Audit Focus
                if full_excel_data:
                    st.download_button(
                        label="📥 Download Full Log (Multi-Tab Excel)",
                        data=full_excel_data,
                        file_name=f"monopoly_master_audit_T{st.session_state.turn_count}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"global_log_xl_{st.session_state.turn_count}"
                    )
            else:
                st.info("No turns have been recorded in the master log yet. Run some turns to see data!")
        
        
        
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
    
            else:
                st.info("No turns recorded in the master log yet.")
        else:
            st.info("Game not initialized.")
        # --- 8 SPACES END HERE ---

    # --- 4 SPACES START HERE (Back 4 spaces) ---
    # These are now outside the tab, but still inside the LIVE phase
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 RESTART GAME (Keep Policies and Customizations)", use_container_width=True):
        if "starting_players" in st.session_state:
            restart_game()
        else:
            st.sidebar.warning("No active simulation to restart!")

    st.sidebar.markdown("---")

    # 2. Your existing Reset button
    if st.sidebar.button("⚠️ RESET SIMULATION (Full Wipe)", type="secondary", use_container_width=True):
        reset_lab()

    # --- SIDEBAR CONTROL CENTER ---
    # st.sidebar.divider()

    # 🟢 Call the integrity check here so it displays its metrics
    verify_sim_integrity()

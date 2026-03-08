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

def stamp_property_ledger(pid, event_type, 
                          deed=0, monopoly=0, 
                          h1=0, h2=0, h3=0, h4=0, hotel=0):
    """
    The Single Source of Truth for property history.
    Calculates a 'total' automatically for audit consistency.
    Negative values = Investments (Costs), Positive = Revenue (Rent).
    """
    # Ensure the dictionary exists (failsafe)
    if "property_ledgers" not in st.session_state:
         st.session_state.property_ledgers = {str(i): [] for i in range(40)}
         
    # Sum the marginal components for the 'Total' column
    row_total = deed + monopoly + h1 + h2 + h3 + h4 + hotel
    
    entry = {
        "turn": st.session_state.turn_count,
        "event": event_type,
        "deed": int(deed),
        "monopoly": int(monopoly),
        "h1": int(h1), "h2": int(h2), "h3": int(h3), "h4": int(h4), "hotel": int(hotel),
        "total": int(row_total)
    }
    
    st.session_state.property_ledgers[str(pid)].append(entry)

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
    # 🟢 2. Set Jackpot based on the rule
    st.session_state.jackpot = st.session_state.rules["fp_initial"] if st.session_state.rules["fp_jackpot"] else 0

    # 🟢 3. Initialize Audit with the "Seed" entry if applicable
    st.session_state.bank_audit = []
    
    if st.session_state.rules["fp_jackpot"] and st.session_state.jackpot > 0:
        st.session_state.bank_audit.append({
            "turn": 0,
            "player": "Bank",
            "reason": "🏦 Initial Jackpot Seed (Game Start)",
            "amount": float(st.session_state.jackpot)
        })

    # 🟢 Initialize Property Cash Flow Ledgers
    # Stores a list of 'stamps' for every square on the board (0-39)
    if "property_ledgers" not in st.session_state:
        st.session_state.property_ledgers = {str(i): [] for i in range(40)}


#--- SPREADSHEET FUNCTIONALITY ---
def get_full_log_excel(mode="audit"):
    import io
    import pandas as pd
    import streamlit as st
    
    # 🟢 SAFE MODE: Ensure data exists
    if not st.session_state.get('bank_audit') and mode == "audit":
        return None

    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            if mode == "audit":
                # --- 🏦 TYPE 1: THE FORENSIC AUDIT (Financial Focus) ---
                money_fmt = workbook.add_format({'num_format': '$#,##0.00', 'align': 'center'})
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
                
                # Tab 1: Global Ledger
                df_audit = pd.DataFrame(st.session_state.bank_audit)
                df_audit.to_excel(writer, sheet_name="1_Bank_Master_Ledger", index=False)
                ws_audit = writer.sheets["1_Bank_Master_Ledger"]
                ws_audit.set_column('D:E', 25, money_fmt)
                
                # Tab 2+: Player Ledgers
                for i, p in enumerate(st.session_state.players):
                    p_audit = [e for e in st.session_state.bank_audit if e['Player'] == p['name']]
                    if p_audit:
                        df_p = pd.DataFrame(p_audit)
                        df_p['Running Total'] = df_p['Money In'].cumsum()
                        clean_name = "".join(filter(str.isalnum, p['name']))[:20]
                        df_p.drop(columns=['Player']).to_excel(writer, sheet_name=f"P{i}_{clean_name}_Ledger", index=False)
                        writer.sheets[f"P{i}_{clean_name}_Ledger"].set_column('C:D', 20, money_fmt)

            elif mode == "narrative":
                # --- 📖 TYPE 2: THE PLAY-BY-PLAY LOG (Full Game History) ---
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#DEEBF7', 'border': 1})
                
                if st.session_state.get('master_log'):
                    df_master = pd.DataFrame(st.session_state.master_log)
                    df_master["Turn"] = pd.to_numeric(df_master["Turn"], errors='coerce')
                    df_master = df_master.sort_values(by=["Turn", "Player"], ascending=[True, True])
                    
                    df_master.to_excel(writer, sheet_name="Full_Play_by_Play", index=False)
                    ws_master = writer.sheets["Full_Play_by_Play"]
                    ws_master.set_column('C:C', 65)
                    
                    for i, p in enumerate(st.session_state.players):
                        p_history = df_master[df_master['Player'] == p['name']].copy()
                        if not p_history.empty:
                            clean_name = "".join(filter(str.isalnum, p['name']))[:20]
                            sheet_name = f"P{i}_{clean_name}_History"
                            p_history.drop(columns=['Player']).to_excel(writer, sheet_name=sheet_name, index=False)
                            writer.sheets[sheet_name].set_column('B:B', 65)

            elif mode == "milestones":
                # --- 🚩 TYPE 3: THE STORYBOOK (Critical Moments Focus) ---
                # Using a distinct color (Yellow) to distinguish it from Narrative (Blue)
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#FFEB9C', 'border': 1})
                
                # Tab 1: All Critical Moments (Global Story)
                all_moments = []
                for p in st.session_state.players:
                    for m in p['stats'].get('critical_moments', []):
                        all_moments.append({"Player": p['name'], "Turn": m['turn'], "Event": m['event']})
                
                if all_moments:
                    df_global = pd.DataFrame(all_moments).sort_values(by="Turn")
                    df_global.to_excel(writer, sheet_name="All_Critical_Moments", index=False)
                    ws_global = writer.sheets["All_Critical_Moments"]
                    ws_global.set_column('C:C', 70)
                    # Apply header style
                    for col_num, value in enumerate(df_global.columns.values):
                        ws_global.write(0, col_num, value, header_fmt)

                # Tab 2+: Individual Player Milestones
                for i, p in enumerate(st.session_state.players):
                    p_moments = p['stats'].get('critical_moments', [])
                    if p_moments:
                        df_p = pd.DataFrame(p_moments)
                        clean_name = "".join(filter(str.isalnum, p['name']))[:20]
                        sheet_name = f"P{i}_{clean_name}_Milestones"
                        df_p.to_excel(writer, sheet_name=sheet_name, index=False)
                        ws_p = writer.sheets[sheet_name]
                        ws_p.set_column('B:B', 70)
                        # Apply header style
                        for col_num, value in enumerate(df_p.columns.values):
                            ws_p.write(0, col_num, value, header_fmt)

        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Excel Export Error: {e}")
        return None


def log_bank_transaction(p_name, reason, amount):
    if 'bank_audit' not in st.session_state:
        st.session_state.bank_audit = []
    
    # Force whole numbers immediately
    amt = int(amount)
    
    # Calculate global liquidity using integer math
    prev_total = int(st.session_state.bank_audit[-1]['Running Total Money In']) if st.session_state.bank_audit else 0
    new_total = prev_total + amt

    st.session_state.bank_audit.append({
        "Turn": st.session_state.get('turn_count', 0),
        "Player": p_name,
        "Event": reason,
        "Money In": amt,
        "Running Total Money In": new_total 
    })


def log_parachuted_asset(p_name, property_name):
    """Logs asset allocation to both the UI highlights and the Excel audit."""
    turn = st.session_state.get('turn_count', 0)
    event_text = f"🪂 PARACHUTED: Received {property_name} via setup/allocation."
    
    # 1. Update Critical Moments for the UI
    for p in st.session_state.players:
        if p['name'] == p_name:
            if 'critical_moments' not in p['stats']: 
                p['stats']['critical_moments'] = []
            p['stats']['critical_moments'].append({
                'turn': turn, 
                'event': event_text
            })
            break
    
    # 2. Update Banker's Audit for the spreadsheet ($0 transaction)
    log_bank_transaction(
        p_name=p_name,
        reason=f"Asset Allocation: {property_name} (Parachuted)",
        amount=0  
    )

def generate_true_audit_excel():
    import io
    output = io.BytesIO()
    
    # 1. Pull the financial audit (This is df_base in your UI)
    bank_data = st.session_state.get('bank_audit', [])
    
    if not bank_data:
        return None

    # 2. Replicate UI Filtering Logic for Specialized Tabs
    df_base = pd.DataFrame(bank_data)
    df_injections = df_base[df_base["Money In"] > 0].copy()
    df_sinks = df_base[df_base["Money In"] < 0].copy()

    # 3. Create the Workbook
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # --- TAB 1: MASTER LEDGER ---
        # Consistent with your UI: cols_master = ["Turn", "Player", "Event", "Money In", "Running Total Money In"]
        cols_master = ["Turn", "Player", "Event", "Money In", "Running Total Money In"]
        df_base[cols_master].to_excel(writer, sheet_name='Master Ledger', index=False)
        
        # --- TAB 2: INJECTIONS AND GO ---
        if not df_injections.empty:
            df_injections["Running Total Money In"] = df_injections["Money In"].cumsum()
            df_injections[cols_master].to_excel(writer, sheet_name='Injections and Go', index=False)
            
        # --- TAB 3: SINKS AND TAXES ---
        if not df_sinks.empty:
            df_sinks["Running Total Money In"] = df_sinks["Money In"].cumsum()
            df_sinks[cols_master].to_excel(writer, sheet_name='Sinks and Taxes', index=False)

        # --- TABS 4 to N: PLAYER SPECIFIC LEDGERS ---
        for p in st.session_state.players:
            df_p = df_base[df_base["Player"] == p['name']].copy()
            
            # Clean tab name
            safe_name = "".join(filter(str.isalnum, p['name']))[:25]
            sheet_label = f"Player_{safe_name}"
            
            if not df_p.empty:
                # Recalculate personal running total to match UI logic
                df_p["Running Total Money In"] = df_p["Money In"].cumsum()
                # Use columns consistent with player tabs: ["Turn", "Event", "Money In", "Running Total Money In"]
                cols_p = ["Turn", "Event", "Money In", "Running Total Money In"]
                df_p[cols_p].to_excel(writer, sheet_name=sheet_label, index=False)
            else:
                pd.DataFrame(columns=["Turn", "Event", "Money In", "Running Total Money In"]).to_excel(writer, sheet_name=sheet_label, index=False)

    return output.getvalue()



#--- GAME RESET ---
def reset_lab():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def restart_game():
    import copy
    import random
    import streamlit as st

    # 0. First, we clear the slate
    st.session_state.bank_audit = []
    st.session_state.master_log = [] 
    
    # 🟢 This wipes OLD history, NOT the blueprint
    st.session_state.property_ledgers = {str(i): [] for i in range(40)}

    # 1. Restore Board and Game State FROM BLUEPRINT
    st.session_state.ownership = copy.deepcopy(st.session_state.get('starting_ownership', {}))
    st.session_state.houses = copy.deepcopy(st.session_state.get('starting_houses', {}))

    # 🏦 BANKER'S AUDIT: Full wipe
    st.session_state.bank_audit = []
    st.session_state.master_log = [] 
    
    # 🟢 FORENSIC SYNC: Re-seed the Jackpot and Log the Injection
    if st.session_state.rules.get("fp_jackpot"):
        seed = st.session_state.rules.get("fp_initial", 0)
        st.session_state.jackpot = seed
        if seed > 0:
            st.session_state.bank_audit.append({
                "turn": 0,
                "player": "Bank",
                "reason": "🏦 Initial Jackpot Seed (RESTART)",
                "amount": float(seed)
            })
    else:
        st.session_state.jackpot = 0
    
    # 🟢 SYNC FIX: Baseline counters
    st.session_state.turn_count = 0
    st.session_state.current_p = 0
    st.session_state.double_count = 0
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
            log_bank_transaction(
                p_name=p['name'], 
                reason="Initial Cash Injection", 
                amount=float(p['cash'])
            )

            # 🏦 STATS WIPE & INITIAL MOMENT
            p['stats'] = {
                "visits": {str(idx): 0 for idx in range(40)},
                "ends": {str(idx): 0 for idx in range(40)},
                "rent_paid": 0, "rent_collected": 0, "times_in_jail": 0,
                "cash_history": [p['cash']], 
                "critical_moments": [{
                    "turn": 0, 
                    "event": f"💰 RESTART: Started with ${p['cash']}"
                }]
            }

            # 📜 LOG: Master Log Entry (Turn 0 for Sidebar Sync)
            st.session_state.master_log.append({
                "Turn": 0,
                "Player": p['name'],
                "Position": p['pos'],
                "Square": PROPERTIES[p['pos']]['name'],
                "Cash": p['cash'],
                "Action": f"RESTART: Started with ${p['cash']}"
            })

        # --- LOOP B: ACCOUNT FOR PROPERTY SINKS (RESTART SYNC) ---
        for prop_id, owner_name in st.session_state.ownership.items():
            if owner_name and owner_name != "Bank":
                pid_int = int(prop_id)
                p_info = PROPERTIES[pid_int]
                p_name = p_info['name']
                price = p_info.get('price', 150)
                
                # 🔍 Find the player object to update their specific UI highlights
                owner_obj = next((pl for pl in st.session_state.players if pl['name'] == owner_name), None)
                
                # 🟢 [NEW] STAMP: Land investment for Property Ledger
                stamp_property_ledger(pid_int, "🪂 INITIAL: Parachuted Deed", deed=-price)

                # 🟢 [NEW] STAMP: Monopoly status (if applicable at start)
                if check_monopoly(pid_int):
                    stamp_property_ledger(pid_int, "🪂 INITIAL: Monopoly Obtained")

                if owner_obj:
                    owner_obj['stats']['critical_moments'].append({
                        "turn": 0, 
                        "event": f"🪂 RESTART: Restored ownership of {p_name}"
                    })

                # 🏦 AUDIT: Property values subtracted from Bank liquidity
                log_bank_transaction(owner_name, f"Setup: {p_name} Value", -float(price))
                
                h_count = st.session_state.houses.get(str(prop_id), 0)
                if h_count > 0:
                    h_cost = p_info.get('h_cost', 50)
                    total_h_val = h_count * h_cost
                    label = "a HOTEL" if h_count == 5 else f"{h_count} House(s)"
                    
                    # 🟢 [NEW] STAMP: Sequential house investments for Property Ledger
                    if h_count >= 1: stamp_property_ledger(pid_int, "🪂 INITIAL: House 1", h1=-h_cost)
                    if h_count >= 2: stamp_property_ledger(pid_int, "🪂 INITIAL: House 2", h2=-h_cost)
                    if h_count >= 3: stamp_property_ledger(pid_int, "🪂 INITIAL: House 3", h3=-h_cost)
                    if h_count >= 4: stamp_property_ledger(pid_int, "🪂 INITIAL: House 4", h4=-h_cost)
                    if h_count == 5: stamp_property_ledger(pid_int, "🪂 INITIAL: Hotel", hotel=-h_cost)

                    if owner_obj:
                        owner_obj['stats']['critical_moments'].append({
                            "turn": 0, 
                            "event": f"🏗️ RESTART: {p_name} restored with {label}"
                        })

                    # 🏦 AUDIT: House values subtracted from Bank liquidity
                    log_bank_transaction(owner_name, f"Setup: {p_name} Improvements", -float(total_h_val))
                
                # 📜 LOG: Record the asset restoration in Master Log
                st.session_state.master_log.append({
                    "Turn": 0,
                    "Player": owner_name,
                    "Position": p_info.get('pos', pid_int),
                    "Square": p_name,
                    "Cash": "N/A", 
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
def check_monopoly(pos):
    sq = PROPERTIES[pos]
    if sq['type'] != "Street":
        return False
    
    color = sq.get('color')
    owner = st.session_state.ownership.get(str(pos))
    
    if not owner or owner == "Bank":
        return False

    # Find all properties of the same color
    same_color_indices = [
        i for i, p in enumerate(PROPERTIES) 
        if p.get('color') == color
    ]
    
    # Check if the same owner owns all of them
    return all(
        st.session_state.ownership.get(str(idx)) == owner 
        for idx in same_color_indices
    )


def charge_player(p, amt, destination="bank"):
    # 1. Physical wallet deduction
    p['cash'] -= amt
    
    # 🏦 MACRO ECONOMY LOGIC
    if destination == "jackpot" and st.session_state.rules.get("fp_jackpot", False):
        # INTERNAL MOVE: Money stays in the "M1" supply (Jackpot)
        st.session_state.jackpot += amt
        # No Banker's Audit log here—the game's total cash is unchanged.
    else:
        # OUTFLOW: Money leaves the game ecosystem to the Bank
        log_bank_transaction(
            p_name=p['name'], 
            reason="Bank Outflow (Fee/Tax/Asset)", 
            amount=-amt
        )
    
    # 🚨 CRITICAL MOMENT: Debt is a major narrative inflection
    if p['cash'] < 0:
        event_text = f"🚨 Went into DEBT (-${abs(p['cash'])})"
        if not any("DEBT" in m['event'] for m in p['stats']['critical_moments'][-1:]):
            p['stats']['critical_moments'].append({
                'turn': st.session_state.turn_count, 
                'event': event_text
            })

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    owner = get_owner(pid)
    
    if not owner or owner == "Bank":
        return 0

    owner_norm = str(owner).strip().lower()

    # 1. STREETS (Houses & Monopolies)
    if info['type'] == "Street":
        h = get_house_count(pid)
        rent_list = info.get('rent', [0])
        base = rent_list[min(h, len(rent_list)-1)]
        
        # 🟢 CLEANED: Using your new helper function
        if h == 0 and check_monopoly(pid):
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
    # Track builds this turn to group logs: {target_idx: {'count': X, 'cost': Y, 'name': Z}}
    session_builds = {}
    
    # 1. Identify all color groups
    color_groups = {}
    for idx, sq in PROPERTIES.items(): 
        if isinstance(sq, dict) and sq.get('type') == "Street":
            color = sq.get('color')
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(str(idx))

    for color, indices in color_groups.items():
        # ownership check...
        player_owned_count = sum(1 for idx in indices if get_owner(idx) == p['name'])
        total_in_set = len(indices)
        is_monopoly = (player_owned_count == total_in_set) and (total_in_set > 0)
        
        if is_monopoly:
            # Building Policy Check
            if p['policy'].get('build_house') == "Never":
                continue 

            while True:
                counts = [get_house_count(idx) for idx in indices]
                if all(c >= 5 for c in counts): 
                    break 
                
                target_idx = indices[counts.index(min(counts))]
                sq = PROPERTIES[int(target_idx)]
                h_price = int(sq.get('h_cost', 50)) # Ensure integer
                
                effective_floor = get_effective_reserve(p, 'build_house')

                if (p['cash'] - h_price) >= effective_floor:
                    # 🏦 Audit: Deducts cash & logs to Bank outflow
                    charge_player(p, h_price, destination="bank") 
                    
                    # 🏗️ State Update: Calculate new count locally
                    current_h = get_house_count(target_idx)
                    new_count = current_h + 1
                    
                    # Write to state using string key (standardizing for your getter)
                    st.session_state.houses[str(target_idx)] = new_count
                    
                    # 🟢 [NEW] FORENSIC STAMP: Record this specific investment layer
                    label = "Hotel" if new_count == 5 else f"House {new_count}"
                    column_key = "hotel" if new_count == 5 else f"h{new_count}"
                    
                    # This tells the ledger: "Put this cost in the 'h3' column" (or whichever unit it is)
                    stamp_property_ledger(
                        int(target_idx), 
                        f"Built {label}", 
                        **{column_key: -h_price}
                    )
                    
                    # 📝 Grouping Logic for Storybook
                    if target_idx not in session_builds:
                        session_builds[target_idx] = {'units': 0, 'total_cost': 0, 'name': sq['name']}
                    session_builds[target_idx]['units'] += 1
                    session_builds[target_idx]['total_cost'] += h_price

                    # 🏷️ Narrative Labeling
                    actions.append(f"{label} on {sq['name']}")
                else:
                    break

    # 🚩 REMOVED the redundant log_bank_transaction loop here to avoid double-logging!

    # 🚩 RESTORED: Log Capital Improvements to Critical Moments (The Forensic Narrative)
    if session_builds:
        summary_parts = [f"{d['units']}x on {d['name']}" for d in session_builds.values()]
        total_spent = sum(d['total_cost'] for d in session_builds.values())
        
        p['stats']['critical_moments'].append({
            "turn": st.session_state.turn_count,
            "event": f"🏗️ Capital Expansion: Built {', '.join(summary_parts)} (Total: ${total_spent})"
        })

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
    kept_card = False  
    
    if card['effect'] == "goo_card":
        p['goo_cards'].append({"deck": deck_type, "index": idx})
        kept_card = True  
    
    elif card['effect'] == "move":
        old_pos = p['pos']
        p['pos'] = int(card['pos']) 
        if p['pos'] < old_pos: 
            p['cash'] += 200
            # 🟢 Cleaned: Removed 200.0
            log_bank_transaction(p_name=p['name'], reason="Passed GO (Card Move)", amount=200)
            # 🟢 TICKER FIX: Added visibility
            msg += " | 💸 Collected $200 for passing GO."
            
        p['stats']['visits'][str(p['pos'])] += 1
            
    elif card['effect'] == "jail":
        send_to_jail(p)
        msg += " | 👮 Go To Jail!"
        
    elif card['effect'] == "move_relative":
        p['pos'] = (p['pos'] + card['amt']) % 40
        p['stats']['visits'][str(p['pos'])] += 1
        
    elif card['effect'] == "cash":
        # 🟢 Cleaned: Use int() instead of float()
        amount = int(card['amt'])
        if amount < 0: 
            charge_player(p, abs(amount))
            log_bank_transaction(
                p_name=p['name'], 
                reason=f"Card: {card['text'][:30]}...", 
                amount=amount 
            )
        else: 
            p['cash'] += amount
            log_bank_transaction(
                p_name=p['name'], 
                reason=f"Card: {card['text'][:30]}...", 
                amount=amount
            )
            
    elif card['effect'] == "birthday":
        gift = int(card['amt'])
        for op in st.session_state.players:
            if str(op['name']).strip().lower() != str(p['name']).strip().lower():
                op['cash'] -= gift
                p['cash'] += gift
                
    elif card['effect'] == "repairs":
        cost = 0
        for pid, h_count in st.session_state.houses.items():
            owner = st.session_state.ownership.get(str(pid))
            if owner and str(owner).strip().lower() == str(p['name']).strip().lower():
                this_prop_cost = 0
                if h_count == 5: # Hotel
                    this_prop_cost = int(card['H'])
                else: # Houses
                    this_prop_cost = (h_count * int(card['h']))
                
                cost += this_prop_cost
                
                # 🟢 [NEW] FORENSIC STAMP: Log maintenance per property
                if this_prop_cost > 0:
                    stamp_property_ledger(
                        int(pid), 
                        f"🛠️ Repairs: {card['text'][:20]}...", 
                        maintenance=-this_prop_cost
                    )
        
        charge_player(p, cost)
        
        if cost > 0:
            # 🟢 Cleaned: Removed -float(cost)
            log_bank_transaction(
                p_name=p['name'], 
                reason="Maintenance: Property Repairs (Card)", 
                amount=-cost
            )
            # 🟢 TICKER FIX: Added visibility
            msg += f" | 🔧 Paid ${cost} in repairs."
            
        if "property_stats" in st.session_state and cost > 0:
            p['stats']['rent_paid'] += cost
        
    elif card['effect'] == "move_nearest_rr":
        targets = [5, 15, 25, 35]
        old_pos = p['pos']
        p['pos'] = int(min([r for r in targets if r > p['pos']] or [5]))
        if p['pos'] < old_pos: 
            p['cash'] += 200
            log_bank_transaction(p_name=p['name'], reason="Passed GO (Nearest RR Card)", amount=200)
            # 🟢 TICKER FIX: Added visibility
            msg += " | 💸 Collected $200 for passing GO."
        p['stats']['visits'][str(p['pos'])] += 1
        
    elif card['effect'] == "move_nearest_util":
        targets = [12, 28]
        old_pos = p['pos']
        p['pos'] = int(min([u for u in targets if u > p['pos']] or [12]))
        if p['pos'] < old_pos: 
            p['cash'] += 200
            log_bank_transaction(p_name=p['name'], reason="Passed GO (Nearest Util Card)", amount=200)
            # 🟢 TICKER FIX: Added visibility
            msg += " | 💸 Collected $200 for passing GO."
        p['stats']['visits'][str(p['pos'])] += 1

    # --- FINAL DECK MANAGEMENT ---
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
                
    # --- POST-MOVE EVALUATION (Refined for Square Interactions) ---
    move_effects = ["move", "move_relative", "move_nearest_rr", "move_nearest_util"]
    if card['effect'] in move_effects:
        sq = PROPERTIES[p['pos']]
        owner = st.session_state.ownership.get(str(p['pos']), "Bank")
        
        # 1. Handle Property/Rent Interactions
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            if owner != "Bank" and str(owner).lower() != str(p['name']).lower():
                # --- CUMULATIVE MULTIPLIER LOGIC ---
                multiplier = 1
                reasons = []

                # A. Handle Special Card Effects
                if card['effect'] == "move_nearest_rr":
                    multiplier *= 2
                    reasons.append("2x Card Bonus")
                
                # B. Handle Utility Special Case (10x NEW Roll)
                if card['effect'] == "move_nearest_util":
                    # 🎲 NEW: Official rules require a fresh throw for this card
                    new_d1 = random.randint(1, 6)
                    new_d2 = random.randint(1, 6)
                    new_roll = new_d1 + new_d2
                    
                    rent = 10 * new_roll
                    reasons.append(f"10x NEW Roll [{new_d1}+{new_d2}={new_roll}]")
                else:
                    # Standard Rent Calculation (with Monopoly check)
                    base_rent = int(get_rent(p['pos']))
                    if sq['type'] == "Street" and check_monopoly(p['pos']):
                        if st.session_state.houses.get(str(p['pos']), 0) == 0:
                            # We don't multiply here because get_rent already did it!
                            reasons.append("2x Monopoly Bonus")
                    
                    rent = int(base_rent * multiplier)

                # --- EXECUTE TRANSFER ---
                p['cash'] -= rent
                p['stats']['rent_paid'] += rent
                
                # 🟢 [NEW] FORENSIC STAMP: Expense side
                stamp_property_ledger(p['pos'], f"Rent Paid (via {name} Card)", rent_exp=-rent)
                
                for op in st.session_state.players:
                    if str(op['name']).lower() == str(owner).lower():
                        op['cash'] += rent
                        op['stats']['rent_collected'] += rent
                        
                        # 🟢 [NEW] FORENSIC STAMP: Income side
                        stamp_property_ledger(p['pos'], f"Rent Collected (via Card)", rent_inc=rent)
                
                # Build the "Forensic Receipt"
                receipt = f" ({' + '.join(reasons)})" if reasons else ""
                msg += f" | Paid ${rent} rent to {owner}{receipt}."
            
            elif owner == "Bank":
                price = int(sq.get('price', 150))
                pol = p['policy'].get('buy_prop', "Always")
                
                should_buy_card = False
                if pol == "Always":
                    should_buy_card = True
                elif pol == "Keep Reserve":
                    floor = get_effective_reserve(p, 'buy_prop')
                    if p['cash'] - price >= floor:
                        should_buy_card = True
                
                if should_buy_card and p['cash'] >= price:
                    st.session_state.ownership[str(p['pos'])] = p['name']
                    charge_player(p, price, destination="bank")
                    
                    # 🟢 [NEW] FORENSIC STAMP: Record the Investment
                    stamp_property_ledger(p['pos'], "Property Purchase (via Card)", deed=-price)
                    
                    # 🎯 [NEW] MONOPOLY CHECK: Does this buy double the rent?
                    if check_monopoly(p['pos']):
                        color = PROPERTIES[p['pos']]['color']
                        for idx, prop in enumerate(PROPERTIES):
                            if prop.get('color') == color:
                                stamp_property_ledger(idx, "🎯 Monopoly Achieved")
                    
                    if "property_stats" in st.session_state:
                        st.session_state.property_stats[str(p['pos'])]["expenses"] += price
                    
                    event_text = f"🏠 Bought {sq['name']} (-${price}) via card"
                    if 'critical_moments' not in p['stats']: p['stats']['critical_moments'] = []
                    p['stats']['critical_moments'].append({'turn': st.session_state.turn_count, 'event': event_text})
                    msg += f" | {event_text}."

        # 2. Handle Tax Interactions (Fixes the Income Tax bug!)
        elif sq['type'] == "Tax":
            tax = sq.get('cost', 200)
            charge_player(p, tax, destination="jackpot")
            msg += f" | ⚠️ Paid {sq['name']} (${tax}) via card."

        # 3. Handle Go To Jail (Fixes landing on square 30 via card)
        elif sq['type'] == "Action" and p['pos'] == 30:
            send_to_jail(p)
            msg += " | 👮 Go To Jail (Landed via card)!"

        # 4. Handle Free Parking / Jackpot Collection
        elif sq['name'] == "Free Parking":
            if st.session_state.rules.get("fp_jackpot") and st.session_state.jackpot > 0:
                amount = st.session_state.jackpot
                p['cash'] += amount
                # Log it since money is moving from the "Pool" to a "Player"
                log_bank_transaction(p_name=p['name'], reason="Jackpot Collection (Card Move)", amount=amount)
                st.session_state.jackpot = 0
                msg += f" | 💰 Collected Jackpot (${amount}) via card!"
            else:
                msg += " | 🅿️ Resting on Free Parking."
        
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
            log_bank_transaction(p_name=p['name'], reason="Jail Exit Fee", amount=-50)
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
                log_bank_transaction(p_name=p['name'], reason="Jail Exit Fee", amount=-50)
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
    
    # 🟢 1. Identify Square & Start Message
    sq = PROPERTIES.get(p['pos'])
    msg = f"{p['name']} rolled {d1}+{d2}={roll_sum} -> {sq['name']}. "

    # 🟢 2. Pass Go Check
    if p['pos'] < old_pos or (old_pos > 30 and p['pos'] == 0):
        salary = 400 if (st.session_state.rules["double_go"] and p['pos'] == 0) else 200
        p['cash'] += salary
        log_bank_transaction(p['name'], "Passed GO (Salary)", salary)
        # Added leading space and a pipe | for visual clarity
        msg += f" | 💸 Collected ${salary} for passing GO. "

    # --- 4. SQUARE INTERACTION ---
    if sq['type'] in ["Street", "Railroad", "Utility", "Property"]:
        owner = st.session_state.ownership.get(str(p['pos']), "Bank")
        if owner != "Bank" and str(owner).lower() != str(p['name']).lower():
            rent = get_rent(p['pos'], roll=roll_sum)
            p['cash'] -= rent
            p['stats']['rent_paid'] += rent

            # 🟢 FORENSIC STAMP: Log the Expense (The Payer's side)
            stamp_property_ledger(p['pos'], f"Rent Paid by {p['name']}", rent_exp=-rent)
            
            # Transfer rent to owner
            for op in st.session_state.players:
                if str(op['name']).lower() == str(owner).lower():
                    op['cash'] += rent
                    op['stats']['rent_collected'] += rent

                    # 🟢 FORENSIC STAMP: Log the Income (The Owner's side)
                    # This now only fires exactly once when the owner is found.
                    stamp_property_ledger(p['pos'], f"Rent Collected by {op['name']}", rent_inc=rent)
            
            msg += f"Paid ${rent} rent to {owner}. "
            
        elif owner == "Bank":
            price = sq.get('price', 150)
            if p['policy']['buy_prop'] != "Never" and p['cash'] >= price:
                floor = get_effective_reserve(p, 'buy_prop')
                if p['policy']['buy_prop'] != "Keep Reserve" or (p['cash'] - price >= floor):
                    # --- EXISTING: Update State ---
                    st.session_state.ownership[str(p['pos'])] = p['name']
                    charge_player(p, price, destination="bank")
                    
                    # 🟢 [NEW] FORENSIC STAMP: Record the Deed Purchase
                    stamp_property_ledger(p['pos'], "Property Purchase", deed=-price)

                    # 🎯 [NEW] MONOPOLY CHECK: Does this buy double the rent?
                    if check_monopoly(p['pos']):
                        color = PROPERTIES[p['pos']]['color']
                        # Stamp EVERY property in this color set so their history explains the 2x rent
                        for idx, prop in enumerate(PROPERTIES):
                            if prop.get('color') == color:
                                stamp_property_ledger(idx, "🎯 Monopoly Achieved")

                    # --- EXISTING: UI & Logs ---
                    p['stats']['critical_moments'].append({
                        "turn": st.session_state.turn_count,
                        "event": f"🏠 Acquired {sq['name']} for ${price}"
                    })
                    msg += f" | 🏠 Bought {sq['name']} (-${price})."
                    
    elif sq['type'] == "Tax":
        tax = sq.get('cost', 200)
        charge_player(p, tax, destination="jackpot")
        msg += f" | ⚠️ Paid {sq['name']} (${tax})."

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
            amt = int(st.session_state.jackpot)
            p['cash'] += amt
            
            # 🟢 1. Log the Player's Stimulus
            log_bank_transaction(
                p_name=p['name'], 
                reason="🎁 Economic Stimulus: Free Parking Jackpot", 
                amount=float(amt)
            )
            msg += f"Collected Jackpot of ${amt}! "
            
            # 🟢 2. Log the Bank's Re-Injection (The Replacement Seed)
            seed_amt = st.session_state.rules["fp_initial"]
            if seed_amt > 0:
                log_bank_transaction(
                    p_name="Bank", 
                    reason="🏦 Jackpot Re-Seed (System Injection)", 
                    amount=float(seed_amt)
                )
            
            # 🟢 3. Reset the State
            st.session_state.jackpot = seed_amt
        
    # --- 5. WRAP UP ---
    house_msg = attempt_buy_houses(p)
    if house_msg: 
        msg += f" | 🏗️ {house_msg}"
    
    # 🟢 NEW: Clean up the final string (prevents collisions and double spaces)
    msg = msg.strip().replace("  ", " ")
    
    if not silent: 
        st.session_state.last_move = msg
    
    # 🟢 CRITICAL SYNC: All player history lists must grow together
    for player in st.session_state.players:
        player['stats']['cash_history'].append(player['cash'])
    
    p['stats']['ends'][str(p['pos'])] += 1
    
    # Permanent record entry
    record_master_turn(p, msg)

    # Move to next player if not doubles (or if in jail)
    if not is_double or p.get('in_jail'):
        st.session_state.double_count = 0 
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
    
        # 🟢 STEP 1: Loop through players (CASH & STATS INITIALIZATION)
        for p in st.session_state.players:
            # Wealth Curve Protection: Start the history with the initial cash
            p['stats']['cash_history'] = [p['cash']]
            
            # 📜 NEW: Initialize Critical Moments with the Starting Capital
            # This ensures the table is NEVER empty on Turn 0.
            p['stats']['critical_moments'] = [{
                'turn': 0, 
                'event': f"💰 INITIAL: Received starting capital of ${p['cash']}"
            }]

            # 🏦 BANKER'S AUDIT: Starting Cash Injection for the Excel file
            log_bank_transaction(p['name'], "SETUP: Starting Cash Injection", p['cash'])
            
            # 📜 Master Log: Baseline Entry for the turn-by-turn table
            st.session_state.master_log.append({
                "Turn": 0, "Player": p['name'], "Position": p['pos'],
                "Square": PROPERTIES[p['pos']]['name'], "Cash": p['cash'],
                "Action": f"SETUP: Started with ${p['cash']}"
            })

        # 🏗️ STEP 1.5: Record Assets (Loop through properties only ONCE)
        for prop_id_str, owner_name in st.session_state.ownership.items():
            if owner_name != "Bank":
                pid = int(prop_id_str)
                p_info = PROPERTIES[pid]
                p_name = p_info['name']
                
                # Find the owner's object to update their specific stats bucket
                owner_obj = next((pl for pl in st.session_state.players if pl['name'] == owner_name), None)
                if not owner_obj:
                    continue

                p_pos = owner_obj['pos']
                p_cash = owner_obj['cash']

                # 🟢 NEW: Record the Asset in the Player's Critical Moments UI
                owner_obj['stats']['critical_moments'].append({
                    'turn': 0, 
                    'event': f"🪂 PARACHUTED: Started game owning {p_name}"
                })

                # 🏦 1. Banker's Audit: The Deed Sink
                prop_price = p_info.get('price', 0)
                log_bank_transaction(owner_name, f"SETUP: Asset Deed ({p_name})", -prop_price)

                # 📜 2. Master Log: The Deed Assignment
                st.session_state.master_log.append({
                    "Turn": 0, "Player": owner_name, "Position": p_pos,
                    "Square": PROPERTIES[p_pos]['name'], "Cash": p_cash,
                    "Action": f"PARACHUTE ASSET: Began game owning {p_name}"
                })

                # 🏠 3. Houses/Hotels (Consolidated per Property)
                h_count = current_houses.get(str(pid), 0)
                if h_count > 0:
                    h_price = p_info.get('house_price', p_info.get('h_cost', 50))
                    total_h_cost = h_count * h_price
                    label = "a HOTEL" if h_count == 5 else f"{h_count} House(s)"
                    
                    # 🟢 NEW: Record Development in Critical Moments UI
                    owner_obj['stats']['critical_moments'].append({
                        'turn': 0, 
                        'event': f"🏗️ SETUP: {p_name} pre-developed with {label}"
                    })

                    # 🏦 Banker's Audit: Consolidated Entry
                    log_bank_transaction(owner_name, f"SETUP: {label} on {p_name}", -total_h_cost)

                    # 📜 Master Log: The Development Summary
                    st.session_state.master_log.append({
                        "Turn": 0, "Player": owner_name, "Position": p_pos,
                        "Square": PROPERTIES[p_pos]['name'], "Cash": p_cash,
                        "Action": f"PARACHUTE SETUP: Started with {label} on {p_name}"
                    })
        
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
    
            # 🏦 STEP 2: BANKER'S AUDIT (Record the $1500 Initial Capital)
            log_bank_transaction(
                p_name=p['name'], 
                reason="System: Initial Capital Endowment", 
                amount=1500.0
            )
    
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
                # 🟢 THE FIX: Add the narrative event here!
                "critical_moments": [{
                    "turn": 0, 
                    "event": "🚀 Game Start: Initial Capital Endowment of $1,500 received."
                }]
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
        # 🟢 Clean Jackpot (Whole number with commas)
        st.sidebar.metric("Free Parking Jackpot", f"${int(st.session_state.jackpot):,}")
        
    for p in st.session_state.players:
        # 🟢 Clean Expander Title
        cash_pretty = f"${p['cash']:,.0f}"
        with st.sidebar.expander(f"👤 {p['name']} - {cash_pretty}", expanded=True):
            # --- 🛡️ STRATEGY & RESERVES (SYNCED WITH ENGINE) ---
            
            # 1. Get Effective Reserves
            buy_floor = get_effective_reserve(p, 'buy_prop')
            build_floor = get_effective_reserve(p, 'build_house')
            
            # 2. Helper updated to strip decimals from policy text
            def get_policy_text(floor):
                if floor == float('inf'):
                    return "Blocked (Never)"
                if floor == -float('inf'):
                    return "Unlimited Debt" if st.session_state.rules.get("allow_debt") else "Zero-Cash Floor"
                if floor < 0:
                    return f"${int(abs(floor)):,} Debt Limit"
                return f"${int(floor):,} Cash Cushion"

            # 3. Color Coding
            buy_pol = p['policy'].get('buy_prop', 'Always')
            build_pol = p['policy'].get('build_house', 'Always')
            b_color = "red" if buy_pol == "Never" else "orange" if buy_pol == "Keep Reserve" else "green"
            h_color = "red" if build_pol == "Never" else "orange" if build_pol == "Keep Reserve" else "green"

            # 4. Display synchronized info
            st.markdown(f"**Prop Buying:** :{b_color}[{buy_pol}]")
            st.caption(f"🛡️ {get_policy_text(buy_floor)}")
            
            # 🟢 Clean Spendable display
            if buy_floor not in [float('inf'), -float('inf')]:
                safe_cash = max(0, p['cash'] - buy_floor)
                st.caption(f"💰 Spendable: ${safe_cash:,.0f}")

            st.markdown(f"**Building:** :{h_color}[{build_pol}]")
            st.caption(f"🏠 {get_policy_text(build_floor)}")

            st.markdown("---")
            
            if build_pol == "Keep Reserve":
                # Ensure floor is clean for the caption
                b_floor_val = int(get_effective_reserve(p, 'build_house'))
                st.caption(f"🏠 Build Floor: **${b_floor_val:,}**")
            
            st.markdown("---")

            # --- STATUS & CARDS ---
            if p.get('in_jail'): 
                st.error(f"IN JAIL 🚔 (Attempts: {p['jail_turns']})")
            
            for c in p['goo_cards']: 
                st.success(f"GOOJF: {c['deck'].capitalize()}")
            
            # --- 1. Display Streets ---
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
            df_history = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in history_dict.items()]))
            
            # CHANGE: Renamed from "Net Liquidity" to "Cash Balances"
            st.subheader("Player Cash Balances Over Time")
            st.line_chart(df_history)
            
            st.divider()
            
            # CHANGE: Swapped mode from "audit" to "narrative" 
            # to download the Play-by-Play spreadsheet instead of the banker audit.
            narrative_excel = get_full_log_excel(mode="narrative") 
            
            if narrative_excel:
                st.download_button(
                    label="📥 Download Full Play-by-Play Spreadsheet (Excel)", # Updated label
                    data=narrative_excel,
                    file_name=f"monopoly_play_by_play_T{st.session_state.turn_count}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key=f"wealth_tab_narrative_btn_{st.session_state.turn_count}" # Unique key
                )

    with t_bank:
        st.header("🏦 Central Bank Audit Warehouse")
        st.info("This ledger tracks the 'Money Supply' across specialized accounting tabs.")
    
        # 1. Guard against empty lists
        audit_list = st.session_state.get('bank_audit', [])
        
        if not audit_list:
            st.warning("No bank transactions recorded. Run a turn or start a simulation to see the audit!")
        else:
            df_base = pd.DataFrame(audit_list)
    
            # 2. 📊 High-Level Metrics
            total_injected = df_base[df_base['Money In'] > 0]['Money In'].sum()
            total_sunk = abs(df_base[df_base['Money In'] < 0]['Money In'].sum())
            net_liquidity = total_injected - total_sunk
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Injected", f"${total_injected:,.2f}")
            m2.metric("Total Sunk", f"${total_sunk:,.2f}")
            m3.metric("Net Game Liquidity", f"${net_liquidity:,.2f}", 
                      delta="Inflationary" if net_liquidity > 0 else "Contractionary")
    
            st.divider()
    
            # 3. 📑 The 5+ Tab Spreadsheet Overhaul
            tab_names = ["Master Ledger", "Injections & Go", "Sinks & Taxes"] + [f"Player: {p['name']}" for p in st.session_state.players]
            tabs = st.tabs(tab_names)
    
            # --- TAB 1: MASTER LEDGER & ECONOMY CHART ---
            with tabs[0]:
                st.subheader("📈 Money Supply")
                # Create a dedicated chart dataframe with a zero-baseline
                df_chart = df_base.copy()
                df_chart['Breakeven'] = 0
                
                st.line_chart(
                    df_chart, 
                    x="Turn", 
                    y=["Running Total Money In", "Breakeven"], 
                    color=["#FF4B4B", "#808080"]
                )
                st.caption("🔴 Red Line: Net Game Liquidity | ⚪ Grey Line: $0 Breakeven")
                
                # 🟢 THE SAFE CHANGE: Replaced st.spacer with st.write
                st.write("") 
                
                st.subheader("Transaction History")
                cols_master = ["Turn", "Player", "Event", "Money In", "Running Total Money In"]
                st.dataframe(df_base[cols_master], use_container_width=True, hide_index=True)
        
            # --- TAB 2: INJECTIONS & GO CARDS ---
            with tabs[1]:
                df_injections = df_base[df_base["Money In"] > 0].copy()
                df_injections["Running Total Money In"] = df_injections["Money In"].cumsum()
                st.dataframe(df_injections[["Turn", "Player", "Event", "Money In", "Running Total Money In"]], 
                             use_container_width=True, hide_index=True)
    
            # --- TAB 3: SINKS, ASSETS & TAXES ---
            with tabs[2]:
                df_sinks = df_base[df_base["Money In"] < 0].copy()
                df_sinks["Running Total Money In"] = df_sinks["Money In"].cumsum()
                st.dataframe(df_sinks[["Turn", "Player", "Event", "Money In", "Running Total Money In"]], 
                             use_container_width=True, hide_index=True)
    
            # --- TABS 4+: PLAYER SPECIFIC LEDGERS ---
            for i, p in enumerate(st.session_state.players):
                with tabs[i + 3]:
                    df_p = df_base[df_base["Player"] == p['name']].copy()
                    df_p["Running Total Money In"] = df_p["Money In"].cumsum()
                    st.dataframe(df_p[["Turn", "Event", "Money In", "Running Total Money In"]], 
                                 use_container_width=True, hide_index=True)
    
            # --- 4. 📥 Download Button ---
            st.divider()
            try:
                # 🔴 OLD INCORRECT LINE:
                # excel_data = get_full_log_excel(mode="audit") 
                
                # 🟢 NEW CORRECT LINE:
                excel_data = generate_true_audit_excel() 
            
                if excel_data:
                    st.download_button(
                        label="📥 Download Full Banker's Audit (Excel)",
                        data=excel_data,
                        file_name=f"bank_audit_turn_{st.session_state.turn_count}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Excel Error: {e}")
    

    # --- 📂 DATA WAREHOUSE & GAME HIGHLIGHTS ---
    st.markdown("---")
    st.header("📂 Data Warehouse & Game Highlights")

    if "players" in st.session_state and len(st.session_state.players) > 0:
        
        # 🚩 1. Player Milestones & Critical Moments (The main container you like)
        with st.expander("🚩 Player Milestones & Critical Moments", expanded=True):
            cols = st.columns(len(st.session_state.players))
            for i, p in enumerate(st.session_state.players):
                with cols[i]:
                    with st.expander(f"👤 {p['name']} Critical Moments", expanded=False):
                        st.write(f"**Jail Stays:** {p['stats'].get('times_in_jail', 0)}")
                        st.divider()
                        moments = p['stats'].get('critical_moments', [])
                        if moments:
                            for e in moments:
                                st.markdown(f"**` T{e['turn']} `** {e['event']}")
                        else:
                            st.caption("No significant events.")
            
            st.divider()
            
            # Only the Storybook remains here
            milestone_excel = get_full_log_excel(mode="milestones")
            if milestone_excel:
                st.download_button(
                    label="📥 Download Player Milestone Storybook (Excel)",
                    data=milestone_excel,
                    file_name=f"monopoly_milestones_T{st.session_state.turn_count}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"milestone_xl_btn_{st.session_state.turn_count}",
                    use_container_width=True
                )

        # 📜 2. Full Play-by-Play Master Log
        with st.expander("📜 Full Play-by-Play Master Log", expanded=False):
            if st.session_state.get('master_log') and len(st.session_state.master_log) > 0:
                df_master = pd.DataFrame(st.session_state.master_log)
                df_master["Turn"] = pd.to_numeric(df_master["Turn"], errors='coerce')
                df_master = df_master.sort_values(by=["Turn", "Player"], ascending=[True, True])
                st.dataframe(df_master, use_container_width=True, hide_index=True)
                
                narrative_excel = get_full_log_excel(mode="narrative")
                if narrative_excel:
                    st.download_button(
                        label="📥 Download Full Play-by-Play Spreadsheet (Excel)",
                        data=narrative_excel,
                        file_name=f"monopoly_play_by_play_T{st.session_state.turn_count}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"narrative_log_warehouse_{st.session_state.turn_count}",
                        use_container_width=True
                    )
    else:
        st.info("Start the game to populate the Data Warehouse.")
        
        
        
        
    st.sidebar.markdown("---")

    # 1. RESTART GAME (Keep Policies and Customizations) button
    if st.sidebar.button("🔄 RESTART GAME (Keep Policies and Customizations)", use_container_width=True):
        if "starting_players" in st.session_state:
            restart_game()
        else:
            st.sidebar.warning("No active simulation to restart!")

    # 2. RESET SIMULATION (Full Wipe)
    if st.sidebar.button("⚠️ RESET SIMULATION (Full Wipe)", type="secondary", use_container_width=True):
        reset_lab()

    # --- SIDEBAR CONTROL CENTER ---
    # st.sidebar.divider()

    # 🟢 Call the integrity check here so it displays its metrics
    verify_sim_integrity()

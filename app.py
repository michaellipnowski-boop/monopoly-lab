import streamlit as st
import random

#Mapping Monopoly colors to Web-friendly Hex codes
COLOR_MAP = {
    "Brown": "#955436", "Light Blue": "#AAE0FA", "Pink": "#D93A96", "Orange": "#F7941D",
    "Red": "#ED1B24", "Yellow": "#FEF200", "Green": "#1FB25A", "Dark Blue": "#0072BB",
    "Railroad": "#000000", "Utility": "#BDBDBD"
}

#Full Property and Special Square Data
PROPERTIES = {
    1: {"name": "Mediterranean Ave", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    2: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    3: {"name": "Baltic Ave", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    7: {"name": "Chance", "type": "Action", "deck": "chance"},
    8: {"name": "Vermont Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Ave", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    13: {"name": "States Ave", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Ave", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900]},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    17: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    18: {"name": "Tennessee Ave", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "New York Ave", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000]},
    21: {"name": "Kentucky Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    22: {"name": "Chance", "type": "Action", "deck": "chance"},
    23: {"name": "Indiana Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois Ave", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100]},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    26: {"name": "Atlantic Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    31: {"name": "Pacific Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    33: {"name": "Community Chest", "type": "Action", "deck": "chest"},
    34: {"name": "Pennsylvania Ave", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    36: {"name": "Chance", "type": "Action", "deck": "chance"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

#Classic Chance Deck (16 Cards)
CHANCE_DECK_DATA = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Advance to Illinois Ave", "effect": "move", "pos": 24},
    {"text": "Advance to St. Charles Place", "effect": "move", "pos": 11},
    {"text": "Advance to nearest Utility (10x roll)", "effect": "move_nearest_util"},
    {"text": "Advance to nearest Railroad", "effect": "move_nearest_rr"},
    {"text": "Bank pays you dividend of $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "noop"},
    {"text": "Go Back 3 Spaces", "effect": "move_relative", "amt": -3},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "General repairs: $25/house, $100/hotel", "effect": "repairs", "h": 25, "H": 100},
    {"text": "Speeding fine $15", "effect": "cash", "amt": -15},
    {"text": "Take a trip to Reading Railroad", "effect": "move", "pos": 5},
    {"text": "Advance to Boardwalk", "effect": "move", "pos": 39},
    {"text": "Elected Chairman. Pay each player $50", "effect": "birthday", "amt": -50},
    {"text": "Building loan matures. Collect $150", "effect": "cash", "amt": 150},
    {"text": "Crossword competition prize. Collect $100", "effect": "cash", "amt": 100}
]

#Classic Community Chest Deck (16 Cards)
CHEST_DECK_DATA = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Bank error in your favor. Collect $200", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee. Pay $50", "effect": "cash", "amt": -50},
    {"text": "From sale of stock you get $50", "effect": "cash", "amt": 50},
    {"text": "Get Out of Jail Free", "effect": "noop"},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "Holiday Fund matures. Receive $100", "effect": "cash", "amt": 100},
    {"text": "Income tax refund. Collect $20", "effect": "cash", "amt": 20},
    {"text": "Birthday. Collect $10 from every player", "effect": "birthday", "amt": 10},
    {"text": "Life insurance matures. Collect $100", "effect": "cash", "amt": 100},
    {"text": "Hospital Fees. Pay $100", "effect": "cash", "amt": -100},
    {"text": "School fees. Pay $50", "effect": "cash", "amt": -50},
    {"text": "Consultancy fee. Collect $25", "effect": "cash", "amt": 25},
    {"text": "Street repairs: $40/house, $115/hotel", "effect": "repairs", "h": 40, "H": 115},
    {"text": "Beauty contest prize. Collect $10", "effect": "cash", "amt": 10},
    {"text": "You inherit $100", "effect": "cash", "amt": 100}
]

#Grouping Logic
COLOR_GROUPS = {}
RAILROADS, UTILITIES = [], []
for pid, info in PROPERTIES.items():
    if info.get('type') == "Street": COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info.get('type') == "Railroad": RAILROADS.append(pid)
    elif info.get('type') == "Utility": UTILITIES.append(pid)

#Session Initialization
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if PROPERTIES[pid].get("type") in ["Street", "Railroad", "Utility"]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.log = ["Lab initialized."]
    st.session_state.turn_count = 0
    st.session_state.current_p = 0
    c_idx = list(range(16)); random.shuffle(c_idx); st.session_state.c_deck = c_idx
    ch_idx = list(range(16)); random.shuffle(ch_idx); st.session_state.ch_deck = ch_idx

def reset_lab():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

def get_rent(pid, roll=0):
    info = PROPERTIES[pid]
    owner = st.session_state.ownership[pid]
    if info['type'] == "Street":
        h = st.session_state.houses[pid]
        base = info['rent'][h]
        if h == 0 and all(st.session_state.ownership[g] == owner for g in COLOR_GROUPS[info['color']]): return base * 2
        return base
    elif info['type'] == "Railroad":
        count = sum(1 for r in RAILROADS if st.session_state.ownership[r] == owner)
        return info['rent'][count-1]
    elif info['type'] == "Utility":
        count = sum(1 for u in UTILITIES if st.session_state.ownership[u] == owner)
        return (4 if count == 1 else 10) * roll
    return 0

def draw_card(player, deck_type):
    if deck_type == "chance":
        i = st.session_state.c_deck.pop(0); st.session_state.c_deck.append(i)
        card = CHANCE_DECK_DATA[i]; name = "Chance"
    else:
        i = st.session_state.ch_deck.pop(0); st.session_state.ch_deck.append(i)
        card = CHEST_DECK_DATA[i]; name = "Community Chest"
    
    if card['effect'] == "move": player['pos'] = card['pos']
    elif card['effect'] == "move_relative": player['pos'] = (player['pos'] + card['amt']) % 40
    elif card['effect'] == "cash": player['cash'] += card['amt']
    elif card['effect'] == "birthday":
        for p in st.session_state.players:
            if p['name'] != player['name']:
                p['cash'] -= card['amt']; player['cash'] += card['amt']
    elif card['effect'] == "repairs":
        total = 0
        for pid, h_count in st.session_state.houses.items():
            if st.session_state.ownership[pid] == player['name']:
                total += card['H'] if h_count == 5 else (h_count * card['h'])
        player['cash'] -= total
    return f"drew {name}: '{card['text']}'"

def run_turn():
    p = st.session_state.players[st.session_state.current_p]
    if p['cash'] < 0:
        st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
        return False
    
    roll = random.randint(1,6) + random.randint(1,6)
    p['pos'] = (p['pos'] + roll) % 40
    sq = PROPERTIES.get(p['pos'], {"name": "Safe Square", "type": "Safe"})
    msg = f"{p['name']} rolled {roll} -> {sq['name']}. "
    
    if sq['type'] in ["Street", "Railroad", "Utility"]:
        owner = st.session_state.ownership[p['pos']]
        if owner != "Bank" and owner != p['name']:
            rent = get_rent(p['pos'], roll)
            p['cash'] -= rent
            for op in st.session_state.players:
                if op['name'] == owner: op['cash'] += rent
            msg += f"Paid ${rent} rent."
    elif sq['type'] == "Tax":
        p['cash'] -= sq['cost']
        msg += f"Paid ${sq['cost']} tax."
    elif sq['type'] == "Action":
        msg += draw_card(p, sq['deck'])
    elif p['pos'] == 0:
        p['cash'] += 200
        msg += "GO! +$200."
    
    st.session_state.log.insert(0, f"T{st.session_state.turn_count}: {msg}")
    st.session_state.turn_count += 1
    st.session_state.current_p = (st.session_state.current_p + 1) % len(st.session_state.players)
    return p['cash'] < 0

#UI: PHASE 1
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    n = st.number_input("Players", 1, 8, 2)
    names = [st.text_input(f"P{i+1}", f"Student {chr(65+i)}", key=f"in_{i}") for i in range(n)]
    if st.button("Continue"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in names]
        st.session_state.phase = "CHOICE"; st.rerun()

#UI: PHASE 2
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Select")
    if st.button("Standard Simulation"): st.session_state.phase = "LIVE"; st.rerun()
    if st.button("God Mode (Wave Setup)"): st.session_state.phase = "SETUP"; st.rerun()

#UI: PHASE 3
elif st.session_state.phase == "SETUP":
    st.title("🏗️ God Mode Wave Configuration")
    tab1, tab2, tab3 = st.tabs(["Wave 1: Ownership", "Wave 2: Even Development", "Wave 3: Capital"])
    p_names = ["Bank"] + [p['name'] for p in st.session_state.players]

    with tab1:
        st.subheader("Property Deeds")
        for color, pids in COLOR_GROUPS.items():
            st.markdown(f'<div style="background:{COLOR_MAP[color]}; padding:5px; border-radius:3px; color:black;"><b>{color}</b></div>', unsafe_allow_html=True)
            bulk = st.selectbox(f"Assign {color} set to:", p_names, key=f"bulk_{color}")
            if bulk != "Bank":
                for pid in pids: st.session_state.ownership[pid] = bulk
            for pid in pids:
                st.session_state.ownership[pid] = st.selectbox(PROPERTIES[pid]['name'], p_names, index=p_names.index(st.session_state.ownership[pid]), key=f"w1_o_{pid}")
        st.markdown("---")
        st.write("Railroads & Utilities")
        for pid in (RAILROADS + UTILITIES):
            st.session_state.ownership[pid] = st.selectbox(PROPERTIES[pid]['name'], p_names, index=p_names.index(st.session_state.ownership[pid]), key=f"w1_o_{pid}")

    with tab2:
        st.subheader("Development Wave (Even Build Rules)")
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[p] for p in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f'<div style="border-left: 10px solid {COLOR_MAP[color]}; padding-left:10px;"><b>{color} Group ({owners[0]})</b></div>', unsafe_allow_html=True)
                total_h = st.number_input(f"Total Houses for {color}", 0, len(pids)*5, sum(st.session_state.houses[p] for p in pids), key=f"w2_h_{color}")
                if st.button(f"Distribute Evenly: {color}", key=f"w2_btn_{color}"):
                    base = total_h // len(pids)
                    extra = total_h % len(pids)
                    for i, pid in enumerate(pids):
                        st.session_state.houses[pid] = base + (1 if i < extra else 0)
                    st.rerun()
            else:
                st.caption(f"{color} set not owned by a single player.")

    with tab3:
        st.subheader("Bank Balances")
        for i, p in enumerate(st.session_state.players):
            p['cash'] = st.number_input(f"{p['name']} Cash ($)", value=int(p['cash']), key=f"w3_ca_{i}")
        if st.button("🚀 Launch Simulation"):
            st.session_state.phase = "LIVE"; st.rerun()

#UI: PHASE 4
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    h_msg = ", ".join([f"{PROPERTIES[pid]['name']} ({st.session_state.houses[pid]}🏠)" for pid in owned])
                    st.write(f"{color}: {h_msg}")
    if st.sidebar.button("RESET LAB"): reset_lab()
    
    col1, col2 = st.columns([1, 2])
    if col1.button("Next Turn"): run_turn(); st.rerun()
    with col2:
        jump = st.number_input("Turns", 1, 1000, 100, label_visibility="collapsed")
        if st.button(f"Jump {jump} Turns"):
            for _ in range(jump):
                if run_turn(): break
            st.rerun()
    st.code("\n".join(st.session_state.log[:15]))

# END OF CODE

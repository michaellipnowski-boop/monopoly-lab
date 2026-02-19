import streamlit as st
import random

#Mapping Monopoly colors to Web-friendly Hex codes
COLOR_MAP = {
    "Brown": "#955436",
    "Light Blue": "#AAE0FA",
    "Pink": "#D93A96",
    "Orange": "#F7941D",
    "Red": "#ED1B24",
    "Yellow": "#FEF200",
    "Green": "#1FB25A",
    "Dark Blue": "#0072BB",
    "Railroad": "#000000",
    "Utility": "#BDBDBD"
}

#Full Property and Special Square Data
PROPERTIES = {
    1: {"name": "Mediterranean Ave", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    2: {"name": "Community Chest", "type": "Action"},
    3: {"name": "Baltic Ave", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    4: {"name": "Income Tax", "type": "Tax", "cost": 200},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    7: {"name": "Chance", "type": "Action"},
    8: {"name": "Vermont Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Ave", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    13: {"name": "States Ave", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Ave", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900]},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    17: {"name": "Community Chest", "type": "Action"},
    18: {"name": "Tennessee Ave", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "New York Ave", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000]},
    21: {"name": "Kentucky Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    22: {"name": "Chance", "type": "Action"},
    23: {"name": "Indiana Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois Ave", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100]},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    26: {"name": "Atlantic Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    31: {"name": "Pacific Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    33: {"name": "Community Chest", "type": "Action"},
    34: {"name": "Pennsylvania Ave", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    36: {"name": "Chance", "type": "Action"},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    38: {"name": "Luxury Tax", "type": "Tax", "cost": 100},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

#Deck definition for Chance and Community Chest
CHANCE_CARDS = [
    {"text": "Advance to GO", "effect": "move", "pos": 0},
    {"text": "Bank error in your favor. Collect $200", "effect": "cash", "amt": 200},
    {"text": "Doctor's fee. Pay $50", "effect": "cash", "amt": -50},
    {"text": "Go to Jail", "effect": "move", "pos": 10},
    {"text": "It is your birthday. Collect $10 from every player", "effect": "birthday", "amt": 10},
    {"text": "Life insurance matures. Collect $100", "effect": "cash", "amt": 100},
    {"text": "Hospital Fees. Pay $100", "effect": "cash", "amt": -100},
    {"text": "School fees. Pay $50", "effect": "cash", "amt": -50},
    {"text": "Receive $25 consultancy fee", "effect": "cash", "amt": 25},
    {"text": "Beauty contest. Collect $10", "effect": "cash", "amt": 10}
]

#Structural grouping for UI and logic
COLOR_GROUPS = {}
RAILROADS = []
UTILITIES = []
for pid, info in PROPERTIES.items():
    if info.get('type') == "Street": COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info.get('type') == "Railroad": RAILROADS.append(pid)
    elif info.get('type') == "Utility": UTILITIES.append(pid)

#Session State initialization
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.num_players = 2
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES if "rent" in PROPERTIES[pid] or PROPERTIES[pid].get("type") in ["Railroad", "Utility"]}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES if PROPERTIES[pid].get("type") == "Street"}
    st.session_state.log = ["Lab initialized."]
    st.session_state.turn_count = 0
    st.session_state.current_player_idx = 0
    st.session_state.chance_deck = list(range(len(CHANCE_CARDS)))
    random.shuffle(st.session_state.chance_deck)

#Helper function to clear state
def reset_lab():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

#Rent calculation engine
def get_rent(prop_id, roll=0):
    info = PROPERTIES[prop_id]
    owner = st.session_state.ownership[prop_id]
    if info['type'] == "Street":
        h = st.session_state.houses[prop_id]
        base = info['rent'][h]
        if h == 0 and owner != "Bank":
            if all(st.session_state.ownership[gid] == owner for gid in COLOR_GROUPS[info['color']]): return base * 2
        return base
    elif info['type'] == "Railroad":
        count = sum(1 for rid in RAILROADS if st.session_state.ownership.get(rid) == owner)
        return info['rent'][count - 1] if count > 0 else 0
    elif info['type'] == "Utility":
        count = sum(1 for uid in UTILITIES if st.session_state.ownership.get(uid) == owner)
        return (4 if count == 1 else 10) * roll
    return 0

#Card drawing logic
def handle_action(player, square_name):
    idx = st.session_state.chance_deck.pop(0)
    card = CHANCE_CARDS[idx]
    st.session_state.chance_deck.append(idx)
    msg = f"drew {square_name}: '{card['text']}'"
    if card['effect'] == "move": player['pos'] = card['pos']
    elif card['effect'] == "cash": player['cash'] += card['amt']
    elif card['effect'] == "birthday":
        for p in st.session_state.players:
            if p['name'] != player['name']:
                p['cash'] -= card['amt']
                player['cash'] += card['amt']
    return msg

#Main game turn logic
def run_turn():
    p_idx = st.session_state.current_player_idx
    player = st.session_state.players[p_idx]
    if player['cash'] < 0:
        st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
        return False
    roll = random.randint(1, 6) + random.randint(1, 6)
    player['pos'] = (player['pos'] + roll) % 40
    landed_id = player['pos']
    msg = f"{player['name']} rolled {roll} and landed on "
    if landed_id in PROPERTIES:
        sq = PROPERTIES[landed_id]
        msg += f"{sq['name']}. "
        if sq['type'] in ["Street", "Railroad", "Utility"]:
            owner = st.session_state.ownership[landed_id]
            if owner != "Bank" and owner != player['name']:
                rent = get_rent(landed_id, roll)
                player['cash'] -= rent
                for p in st.session_state.players:
                    if p['name'] == owner: p['cash'] += rent
                msg += f"Paid ${rent} rent to {owner}."
            elif owner == player['name']: msg += "Own property."
            else: msg += "Unowned."
        elif sq['type'] == "Tax":
            player['cash'] -= sq['cost']
            msg += f"Paid ${sq['cost']} tax."
        elif sq['type'] == "Action":
            card_msg = handle_action(player, sq['name'])
            msg += card_msg
    else:
        if landed_id == 0: player['cash'] += 200; msg += "GO! +$200."
        else: msg += "Safe zone."
    st.session_state.log.insert(0, f"T{st.session_state.turn_count}: {msg}")
    st.session_state.turn_count += 1
    st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
    return player['cash'] < 0

#UI PHASE 1: INIT
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    n = st.number_input("Players", 1, 8, st.session_state.num_players)
    names = [st.text_input(f"Name {i+1}", f"Student {chr(65+i)}", key=f"init_{i}") for i in range(n)]
    if st.button("Continue"):
        st.session_state.num_players = n
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in names]
        st.session_state.phase = "CHOICE"; st.rerun()

#UI PHASE 2: MODE CHOICE
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Mode Select")
    if st.button("Standard Simulation"): st.session_state.phase = "LIVE"; st.rerun()
    if st.button("Custom Scenario (God Mode)"): st.session_state.phase = "SETUP"; st.rerun()

#UI PHASE 3: SCENARIO SETUP
elif st.session_state.phase == "SETUP":
    st.title("🏗️ God Mode Builder")
    t1, t2, t3 = st.tabs(["Ownership", "Houses", "Cash"])
    with t1:
        opts = ["Bank"] + [p['name'] for p in st.session_state.players]
        for color, pids in COLOR_GROUPS.items():
            st.markdown(f"{color}")
            for pid in pids:
                st.session_state.ownership[pid] = st.radio(PROPERTIES[pid]['name'], opts, index=opts.index(st.session_state.ownership[pid]), horizontal=True, key=f"own_{pid}")
        st.markdown("Railroads")
        for pid in RAILROADS:
            st.session_state.ownership[pid] = st.radio(PROPERTIES[pid]['name'], opts, index=opts.index(st.session_state.ownership[pid]), horizontal=True, key=f"own_{pid}")
        st.markdown("Utilities")
        for pid in UTILITIES:
            st.session_state.ownership[pid] = st.radio(PROPERTIES[pid]['name'], opts, index=opts.index(st.session_state.ownership[pid]), horizontal=True, key=f"own_{pid}")
    with t2:
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[pid] for pid in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.write(f"{color} ({owners[0]})")
                for pid in pids:
                    st.session_state.houses[pid] = st.number_input(PROPERTIES[pid]['name'], 0, 5, st.session_state.houses[pid], key=f"h_{pid}")
    with t3:
        for p in st.session_state.players: p['cash'] = st.number_input(f"{p['name']} Cash", value=int(p['cash']), key=f"cash_{p['name']}")
    if st.button("Launch Lab"): st.session_state.phase = "LIVE"; st.rerun()

#UI PHASE 4: LIVE ENGINE
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        with st.sidebar.expander(f"👤 {p['name']} - ${p['cash']}", expanded=True):
            for color, pids in COLOR_GROUPS.items():
                owned = [pid for pid in pids if st.session_state.ownership[pid] == p['name']]
                if owned:
                    st.write(f"{color}")
                    for pid in owned:
                        h = st.session_state.houses.get(pid, 0)
                        st.write(f"- {PROPERTIES[pid]['name']} ({h}🏠)" if h > 0 else f"- {PROPERTIES[pid]['name']}")
            own_rr = [pid for pid in RAILROADS if st.session_state.ownership.get(pid) == p['name']]
            if own_rr:
                st.write("Railroads")
                for r in own_rr: st.write(f"- {PROPERTIES[r]['name']}")
            own_ut = [pid for pid in UTILITIES if st.session_state.ownership.get(pid) == p['name']]
            if own_ut:
                st.write("Utilities")
                for u in own_ut: st.write(f"- {PROPERTIES[u]['name']}")
    if st.sidebar.button("RESET LAB"): reset_lab()
    if st.button("Next Turn"): run_turn(); st.rerun()
    st.code("\n".join(st.session_state.log[:20]))

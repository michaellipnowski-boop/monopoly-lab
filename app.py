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

#Combined Data Dictionary for Streets, Railroads, and Utilities
PROPERTIES = {
    1: {"name": "Mediterranean Ave", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    3: {"name": "Baltic Ave", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    8: {"name": "Vermont Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Ave", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    12: {"name": "Electric Company", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    13: {"name": "States Ave", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Ave", "type": "Street", "color": "Pink", "rent": [12, 60, 180, 500, 700, 900]},
    15: {"name": "Pennsylvania Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    16: {"name": "St. James Place", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    18: {"name": "Tennessee Ave", "type": "Street", "color": "Orange", "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "New York Ave", "type": "Street", "color": "Orange", "rent": [16, 80, 220, 600, 800, 1000]},
    21: {"name": "Kentucky Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    23: {"name": "Indiana Ave", "type": "Street", "color": "Red", "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois Ave", "type": "Street", "color": "Red", "rent": [20, 100, 300, 750, 925, 1100]},
    25: {"name": "B. & O. Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    26: {"name": "Atlantic Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor Ave", "type": "Street", "color": "Yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    28: {"name": "Water Works", "type": "Utility", "color": "Utility", "rent": [4, 10]},
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    31: {"name": "Pacific Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    34: {"name": "Pennsylvania Ave", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

#Grouping indices for setup logic
COLOR_GROUPS = {}
RAILROADS = []
UTILITIES = []
for pid, info in PROPERTIES.items():
    if info['type'] == "Street":
        COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info['type'] == "Railroad":
        RAILROADS.append(pid)
    elif info['type'] == "Utility":
        UTILITIES.append(pid)

#Initialize Session State
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.num_players = 2
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES}
    st.session_state.log = ["Lab initialized."]
    st.session_state.turn_count = 0
    st.session_state.current_player_idx = 0

#Helper function to reset the app state
def reset_lab():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

#Rent calculation logic handling monopolies, railroads, and utilities
def get_rent(prop_id, roll=0):
    info = PROPERTIES[prop_id]
    owner = st.session_state.ownership[prop_id]
    if info['type'] == "Street":
        houses = st.session_state.houses[prop_id]
        base_rent = info['rent'][houses]
        if houses == 0 and owner != "Bank":
            color = info['color']
            if all(st.session_state.ownership[gid] == owner for gid in COLOR_GROUPS[color]):
                return base_rent * 2
        return base_rent
    elif info['type'] == "Railroad":
        count = sum(1 for rid in RAILROADS if st.session_state.ownership[rid] == owner)
        return info['rent'][count - 1] if count > 0 else 0
    elif info['type'] == "Utility":
        count = sum(1 for uid in UTILITIES if st.session_state.ownership[uid] == owner)
        multiplier = 4 if count == 1 else 10
        return multiplier * roll
    return 0

#Core turn processing logic
def run_turn():
    p_idx = st.session_state.current_player_idx
    player = st.session_state.players[p_idx]
    if player['cash'] < 0:
        st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
        return False
    
    die1, die2 = random.randint(1, 6), random.randint(1, 6)
    roll = die1 + die2
    player['pos'] = (player['pos'] + roll) % 40
    landed_id = player['pos']
    msg = f"{player['name']} rolled {roll} and landed on "
    
    if landed_id in PROPERTIES:
        prop = PROPERTIES[landed_id]
        owner = st.session_state.ownership[landed_id]
        msg += f"{prop['name']}. "
        if owner != "Bank" and owner != player['name']:
            rent = get_rent(landed_id, roll)
            player['cash'] -= rent
            for p in st.session_state.players:
                if p['name'] == owner: p['cash'] += rent
            msg += f"Paid ${rent} rent to {owner}."
        elif owner == player['name']: msg += "their own property."
        else: msg += "unowned land."
    else:
        if landed_id == 0:
            msg += "GO! +$200."
            player['cash'] += 200
        else: msg += "a non-property square."
    
    st.session_state.log.insert(0, f"Turn {st.session_state.turn_count}: {msg}")
    st.session_state.turn_count += 1
    st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
    if player['cash'] < 0:
        st.session_state.log.insert(0, f"⚠️ BANKRUPTCY: {player['name']}!")
        return True
    return False

#UI PHASE 1: Initialization
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab: Initialization")
    val = st.session_state.get("num_players", 2)
    st.session_state.num_players = st.number_input("How many players?", 1, 8, val)
    new_names = []
    for i in range(st.session_state.num_players):
        existing = st.session_state.players[i]['name'] if i < len(st.session_state.players) else f"Student {chr(65+i)}"
        name = st.text_input(f"Player {i+1} Name", value=existing, key=f"p_{i}")
        new_names.append(name)
    if st.button("Continue"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in new_names]
        st.session_state.phase = "CHOICE"
        st.rerun()

#UI PHASE 2: Choice between Default and Custom
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Simulation Selection")
    c1, c2 = st.columns(2)
    if c1.button("Standard (Default)"):
        st.session_state.phase = "LIVE"
        st.rerun()
    if c2.button("Scenario (God Mode)"):
        st.session_state.phase = "SETUP"
        st.rerun()
    if st.button("← Back"):
        st.session_state.phase = "INIT"
        st.rerun()

#UI PHASE 3: Scenario Setup (God Mode)
elif st.session_state.phase == "SETUP":
    st.title("🏗️ God Mode: Scenario Builder")
    if st.button("← Back"):
        st.session_state.phase = "CHOICE"
        st.rerun()
    tabs = st.tabs(["Ownership", "Development", "Cash"])
    with tabs[0]:
        opts = ["Bank"] + [p['name'] for p in st.session_state.players]
        
        # Loop through streets by color
        for color, pids in COLOR_GROUPS.items():
            st.markdown(f'<div style="border-left: 10px solid {COLOR_MAP[color]}; padding-left:10px; margin-bottom:10px;"><b>{color} Group</b></div>', unsafe_allow_html=True)
            for pid in pids:
                c = st.columns([3, 5])
                c[0].write(PROPERTIES[pid]['name'])
                curr = st.session_state.ownership.get(pid, "Bank")
                st.session_state.ownership[pid] = c[1].radio(f"O_{pid}", opts, index=opts.index(curr), horizontal=True, label_visibility="collapsed")
        
        # Loop through railroads
        st.markdown('<div style="border-left: 10px solid #000; padding-left:10px; margin-bottom:10px;"><b>Railroads</b></div>', unsafe_allow_html=True)
        for pid in RAILROADS:
            c = st.columns([3, 5])
            c[0].write(PROPERTIES[pid]['name'])
            curr = st.session_state.ownership.get(pid, "Bank")
            st.session_state.ownership[pid] = c[1].radio(f"O_{pid}", opts, index=opts.index(curr), horizontal=True, label_visibility="collapsed")
        
        # Loop through utilities
        st.markdown('<div style="border-left: 10px solid #BDBDBD; padding-left:10px; margin-bottom:10px;"><b>Utilities</b></div>', unsafe_allow_html=True)
        for pid in UTILITIES:
            c = st.columns([3, 5])
            c[0].write(PROPERTIES[pid]['name'])
            curr = st.session_state.ownership.get(pid, "Bank")
            st.session_state.ownership[pid] = c[1].radio(f"O_{pid}", opts, index=opts.index(curr), horizontal=True, label_visibility="collapsed")

    with tabs[1]:
        # Development controls for house building
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[pid] for pid in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.markdown(f"#### {color} Group ({owners[0]})")
                for pid in pids:
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    curr = st.session_state.houses[pid]
                    can_sub, can_add = (curr > 0 and all(curr >= st.session_state.houses[o] for o in pids)), (curr < 5 and all(curr <= st.session_state.houses[o] for o in pids))
                    if c2.button("➖", key=f"s_{pid}", disabled=not can_sub):
                        st.session_state.houses[pid] -= 1
                        st.rerun()
                    if c3.button("➕", key=f"a_{pid}", disabled=not can_add):
                        st.session_state.houses[pid] += 1
                        st.rerun()
    with tabs[2]:
        # Manual cash adjustment
        for i, p in enumerate(st.session_state.players):
            p['cash'] = st.number_input(f"{p['name']} Cash", value=int(p['cash']), key=f"c_{i}")
    if st.button("🚀 Launch Simulation", type="primary"):
        st.session_state.phase = "LIVE"
        st.rerun()

#UI PHASE 4: Live Simulation
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        st.sidebar.markdown(f"{p['name']}: ${p['cash']}")
    if st.sidebar.button("RESET LAB"): reset_lab()
    c1, c2 = st.columns([1, 2])
    if c1.button("Step"): run_turn(); st.rerun()
    with c2:
        jc = st.columns([1, 1])
        jn = jc[0].number_input("Turns", 1, 1000, 100, label_visibility="collapsed")
        if jc[1].button(f"Go {jn}"):
            for _ in range(jn):
                if run_turn(): break
            st.rerun()
    st.code("\n".join(st.session_state.log[:20]))

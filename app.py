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
    "Railroad": "#000000"
}

#Combined Data Dictionary for all Property types including Railroads
PROPERTIES = {
    1: {"name": "Mediterranean Ave", "type": "Street", "color": "Brown", "rent": [2, 10, 30, 90, 160, 250]},
    3: {"name": "Baltic Ave", "type": "Street", "color": "Brown", "rent": [4, 20, 60, 180, 320, 450]},
    5: {"name": "Reading Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    6: {"name": "Oriental Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    8: {"name": "Vermont Ave", "type": "Street", "color": "Light Blue", "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Ave", "type": "Street", "color": "Light Blue", "rent": [8, 40, 100, 300, 450, 600]},
    11: {"name": "St. Charles Place", "type": "Street", "color": "Pink", "rent": [10, 50, 150, 450, 625, 750]},
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
    29: {"name": "Marvin Gardens", "type": "Street", "color": "Yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    31: {"name": "Pacific Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Ave", "type": "Street", "color": "Green", "rent": [26, 130, 390, 900, 1100, 1275]},
    34: {"name": "Pennsylvania Ave", "type": "Street", "color": "Green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    35: {"name": "Short Line Railroad", "type": "Railroad", "color": "Railroad", "rent": [25, 50, 100, 200]},
    37: {"name": "Park Place", "type": "Street", "color": "Dark Blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    39: {"name": "Boardwalk", "type": "Street", "color": "Dark Blue", "rent": [50, 200, 600, 1400, 1700, 2000]}
}

#Grouping logic for streets and railroads
COLOR_GROUPS = {}
RAILROADS = []
for pid, info in PROPERTIES.items():
    if info['type'] == "Street":
        COLOR_GROUPS.setdefault(info['color'], []).append(pid)
    elif info['type'] == "Railroad":
        RAILROADS.append(pid)

#Initialize Session State variables
if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.num_players = 2
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES}
    st.session_state.log = ["Lab initialized."]
    st.session_state.turn_count = 0
    st.session_state.current_player_idx = 0

#Function to clear state and restart
def reset_lab():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

#Rent calculation logic handling monopolies and railroads
def get_rent(prop_id):
    info = PROPERTIES[prop_id]
    owner = st.session_state.ownership[prop_id]
    if info['type'] == "Street":
        houses = st.session_state.houses[prop_id]
        base_rent = info['rent'][houses]
        if houses == 0 and owner != "Bank":
            color = info['color']
            group = COLOR_GROUPS[color]
            if all(st.session_state.ownership[gid] == owner for gid in group):
                return base_rent * 2
        return base_rent
    elif info['type'] == "Railroad":
        rr_owned = [rid for rid in RAILROADS if st.session_state.ownership[rid] == owner]
        count = len(rr_owned)
        return info['rent'][count - 1] if count > 0 else 0
    return 0

#Core turn logic with bankruptcy stop
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
        prop_name = PROPERTIES[landed_id]['name']
        owner = st.session_state.ownership[landed_id]
        msg += f"{prop_name}. "
        if owner != "Bank" and owner != player['name']:
            rent = get_rent(landed_id)
            player['cash'] -= rent
            for p in st.session_state.players:
                if p['name'] == owner:
                    p['cash'] += rent
            msg += f"Paid ${rent} rent to {owner}."
        elif owner == player['name']:
            msg += "their own property."
        else:
            msg += "unowned land."
    else:
        if landed_id == 0:
            msg += "GO! Collected $200."
            player['cash'] += 200
        else:
            msg += "a non-property square."
    st.session_state.log.insert(0, f"Turn {st.session_state.turn_count}: {msg}")
    st.session_state.turn_count += 1
    st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
    if player['cash'] < 0:
        st.session_state.log.insert(0, f"⚠️ BANKRUPTCY: {player['name']}!")
        return True
    return False

#UI PHASE 1: Initialization and Naming
if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab: Initialization")
    val = st.session_state.get("num_players", 2)
    st.session_state.num_players = st.number_input("How many players?", 1, 8, val)
    new_names = []
    for i in range(st.session_state.num_players):
        existing_name = f"Student {chr(65+i)}"
        if i < len(st.session_state.players):
            existing_name = st.session_state.players[i]['name']
        name = st.text_input(f"Player {i+1} Name", value=existing_name, key=f"name_input_{i}")
        new_names.append(name)
    if st.button("Continue to Game Options"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in new_names]
        st.session_state.phase = "CHOICE"
        st.rerun()

#UI PHASE 2: Route Selection
elif st.session_state.phase == "CHOICE":
    st.title("⚖️ Choose Your Simulation Type")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Standard Game (Default)"):
            st.session_state.phase = "LIVE"
            st.rerun()
    with col2:
        if st.button("Custom Scenario (God Mode)"):
            st.session_state.phase = "SETUP"
            st.rerun()
    if st.button("← Back to Player Names"):
        st.session_state.phase = "INIT"
        st.rerun()

#UI PHASE 3: Scenario Setup (God Mode)
elif st.session_state.phase == "SETUP":
    st.title("🏗️ Scenario Builder (God Mode)")
    if st.button("← Back to Selection"):
        st.session_state.phase = "CHOICE"
        st.rerun()
    tabs = st.tabs(["Ownership", "Development", "Cash"])
    with tabs[0]:
        st.write("### Wave 1: Assign Deeds")
        for pid, info in PROPERTIES.items():
            hex_c = COLOR_MAP.get(info['color'], "#eee")
            cols = st.columns([0.2, 2.8, 5])
            cols[0].markdown(f'<div style="background-color:{hex_c}; width:20px; height:20px; border-radius:3px; margin-top:5px;"></div>', unsafe_allow_html=True)
            cols[1].write(f"{info['name']}")
            opts = ["Bank"] + [p['name'] for p in st.session_state.players]
            current_owner = st.session_state.ownership.get(pid, "Bank")
            idx = opts.index(current_owner) if current_owner in opts else 0
            st.session_state.ownership[pid] = cols[2].radio(f"O_{pid}", opts, index=idx, horizontal=True, label_visibility="collapsed")
    with tabs[1]:
        st.write("### Wave 2: Houses (Nanny Logic)")
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[pid] for pid in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                hex_c = COLOR_MAP.get(color, "#eee")
                st.markdown(f'<h4 style="color:{hex_c}; border-bottom: 2px solid {hex_c};">{color} Group ({owners[0]})</h4>', unsafe_allow_html=True)
                for pid in pids:
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(PROPERTIES[pid]['name'])
                    curr = st.session_state.houses[pid]
                    can_sub = curr > 0 and all(curr >= st.session_state.houses[o] for o in pids)
                    can_add = curr < 5 and all(curr <= st.session_state.houses[o] for o in pids)
                    if c2.button("➖", key=f"s_{pid}", disabled=not can_sub):
                        st.session_state.houses[pid] -= 1
                        st.rerun()
                    if c3.button("➕", key=f"a_{pid}", disabled=not can_add):
                        st.session_state.houses[pid] += 1
                        st.rerun()
            else:
                st.write(f"{color}: No Monopoly.")
    with tabs[2]:
        for i, p in enumerate(st.session_state.players):
            p['cash'] = st.number_input(f"{p['name']} Cash", value=int(p['cash']), key=f"cash_in_{i}")
    if st.button("🚀 Launch Simulation", type="primary"):
        st.session_state.phase = "LIVE"
        st.rerun()

#UI PHASE 4: Simulation Engine (Live)
elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        st.sidebar.markdown(f"{p['name']}: ${p['cash']}")
    if st.sidebar.button("RESET LAB"): reset_lab()
    c1, col_jump = st.columns([1, 2])
    if c1.button("Step Turn"):
        run_turn()
        st.rerun()
    with col_jump:
        j_cols = st.columns([1, 1])
        jump_n = j_cols[0].number_input("Turns", 1, 1000, 100, label_visibility="collapsed")
        if j_cols[1].button(f"Jump {jump_n}"):
            for _ in range(jump_n):
                if run_turn(): break
            st.rerun()
    st.write(f"### Log (Turn {st.session_state.turn_count})")
    st.code("\n".join(st.session_state.log[:20]))

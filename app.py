import streamlit as st
import random

PROPERTIES = {
    1: {"name": "Mediterranean Ave", "color": "Brown", "price": 60, "rent": [2, 10, 30, 90, 160, 250]},
    3: {"name": "Baltic Ave", "color": "Brown", "price": 60, "rent": [4, 20, 60, 180, 320, 450]},
    6: {"name": "Oriental Ave", "color": "Light Blue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    8: {"name": "Vermont Ave", "color": "Light Blue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    9: {"name": "Connecticut Ave", "color": "Light Blue", "price": 120, "rent": [8, 40, 100, 300, 450, 600]},
    11: {"name": "St. Charles Place", "color": "Pink", "price": 140, "rent": [10, 50, 150, 450, 625, 750]},
    13: {"name": "States Ave", "color": "Pink", "price": 140, "rent": [10, 50, 150, 450, 625, 750]},
    14: {"name": "Virginia Ave", "color": "Pink", "price": 160, "rent": [12, 60, 180, 500, 700, 900]},
    16: {"name": "St. James Place", "color": "Orange", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    18: {"name": "Tennessee Ave", "color": "Orange", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    19: {"name": "New York Ave", "color": "Orange", "price": 200, "rent": [16, 80, 220, 600, 800, 1000]},
    21: {"name": "Kentucky Ave", "color": "Red", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    23: {"name": "Indiana Ave", "color": "Red", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    24: {"name": "Illinois Ave", "color": "Red", "price": 240, "rent": [20, 100, 300, 750, 925, 1100]},
    26: {"name": "Atlantic Ave", "color": "Yellow", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    27: {"name": "Ventnor Ave", "color": "Yellow", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    29: {"name": "Marvin Gardens", "color": "Yellow", "price": 280, "rent": [24, 120, 360, 850, 1025, 1200]},
    31: {"name": "Pacific Ave", "color": "Green", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    32: {"name": "North Carolina Ave", "color": "Green", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    34: {"name": "Pennsylvania Ave", "color": "Green", "price": 320, "rent": [28, 150, 450, 1000, 1200, 1400]},
    37: {"name": "Park Place", "color": "Dark Blue", "price": 350, "rent": [35, 175, 500, 1100, 1300, 1500]},
    39: {"name": "Boardwalk", "color": "Dark Blue", "price": 400, "rent": [50, 200, 600, 1400, 1700, 2000]}
}

COLOR_GROUPS = {}
for pid, info in PROPERTIES.items():
    COLOR_GROUPS.setdefault(info['color'], []).append(pid)

if "phase" not in st.session_state:
    st.session_state.phase = "INIT"
    st.session_state.players = []
    st.session_state.ownership = {pid: "Bank" for pid in PROPERTIES}
    st.session_state.houses = {pid: 0 for pid in PROPERTIES}
    st.session_state.log = ["Lab initialized."]
    st.session_state.turn_count = 0
    st.session_state.current_player_idx = 0

def reset_lab():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def get_rent(prop_id):
    houses = st.session_state.houses[prop_id]
    owner = st.session_state.ownership[prop_id]
    base_rent = PROPERTIES[prop_id]['rent'][houses]
    if houses == 0 and owner != "Bank":
        color = PROPERTIES[prop_id]['color']
        group = COLOR_GROUPS[color]
        if all(st.session_state.ownership[gid] == owner for gid in group):
            return base_rent * 2
    return base_rent

def run_turn():
    p_idx = st.session_state.current_player_idx
    player = st.session_state.players[p_idx]
    if player['cash'] < 0:
        st.session_state.current_player_idx = (p_idx + 1) % len(st.session_state.players)
        return
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

if st.session_state.phase == "INIT":
    st.title("🎲 Monopoly Stats Lab")
    num_p = st.number_input("How many players?", 1, 8, 2)
    names = []
    for i in range(num_p):
        names.append(st.text_input(f"Player {i+1} Name", f"Student {chr(65+i)}"))
    if st.button("Proceed to Scenario Builder"):
        st.session_state.players = [{"name": n, "cash": 1500, "pos": 0} for n in names]
        st.session_state.phase = "SETUP"
        st.rerun()

elif st.session_state.phase == "SETUP":
    st.title("🏗️ Scenario Builder (God Mode)")
    tabs = st.tabs(["Ownership", "Development", "Cash"])
    with tabs[0]:
        st.write("### Wave 1: Assign Deeds")
        for pid, info in PROPERTIES.items():
            cols = st.columns([2, 5])
            cols[0].write(f"{info['name']}")
            opts = ["Bank"] + [p['name'] for p in st.session_state.players]
            st.session_state.ownership[pid] = cols[1].radio(f"O_{pid}", opts, index=opts.index(st.session_state.ownership[pid]), horizontal=True, label_visibility="collapsed")
    with tabs[1]:
        st.write("### Wave 2: Houses (Nanny Logic)")
        for color, pids in COLOR_GROUPS.items():
            owners = [st.session_state.ownership[pid] for pid in pids]
            if len(set(owners)) == 1 and owners[0] != "Bank":
                st.write(f"#### {color} Group ({owners[0]})")
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
        for p in st.session_state.players:
            p['cash'] = st.number_input(f"{p['name']} Cash", value=int(p['cash']))
    if st.button("🚀 Launch Simulation", type="primary"):
        st.session_state.phase = "LIVE"
        st.rerun()

elif st.session_state.phase == "LIVE":
    st.sidebar.title("📊 Ledger")
    for p in st.session_state.players:
        st.sidebar.write(f"{p['name']}: ${p['cash']}")
    if st.sidebar.button("RESET LAB"): reset_lab()
    c1, c2, c3 = st.columns([1, 1, 1])
    if c1.button("Step Turn"):
        run_turn()
        st.rerun()
    jump_n = c2.number_input("Jump", 1, 1000, 100)
    if c3.button(f"Go {jump_n}"):
        for _ in range(jump_n): run_turn()
        st.rerun()
    st.write(f"### Log (Turn {st.session_state.turn_count})")
    st.code("\n".join(st.session_state.log[:20]))

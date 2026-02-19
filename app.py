import streamlit as st
import random

--- 1. DATA DEFINITIONS ---
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

def run_turn():
p_idx = st.session_state.current_player_idx
player = st.session_state.players[p_idx]

if st.session_state.phase == "INIT":
st.title("🎲 Monopoly Stats Lab")
num_p = st.number_input("How many players?", 1, 8, 2)
names = []
for i in range(num_p):
names.append(st.text_input(f"Player {i+1} Name", f"Student {chr(65+i)}"))

elif st.session_state.phase == "SETUP":
st.title("🏗️ Scenario Builder (God Mode)")
tabs = st.tabs(["Ownership", "Development", "Cash"])

elif st.session_state.phase == "LIVE":
st.sidebar.title("📊 Lab Status")
for p in st.session_state.players:
st.sidebar.markdown(f"{p['name']}: ${p['cash']}")

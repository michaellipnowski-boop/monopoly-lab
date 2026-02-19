import streamlit as st
import pandas as pd
import random
import plotly.express as px
import copy
import pprint

# ==========================================
# PART 1: THE ENGINE
# ==========================================

class MonopolySimulator:
    def __init__(self):
        self.props = {
            1:  {'name': 'Mediterranean Ave', 'color': 'Brown', 'price': 60, 'h_price': 50, 'rents': [2, 10, 30, 90, 160, 250], 'size': 2},
            3:  {'name': 'Baltic Ave', 'color': 'Brown', 'price': 60, 'h_price': 50, 'rents': [4, 20, 60, 180, 320, 450], 'size': 2},
            5:  {'name': 'Reading Railroad', 'color': 'Railroad', 'price': 200, 'h_price': 0, 'rents': [25, 50, 100, 200], 'size': 4},
            6:  {'name': 'Oriental Ave', 'color': 'Light Blue', 'price': 100, 'h_price': 50, 'rents': [6, 30, 90, 270, 400, 550], 'size': 3},
            8:  {'name': 'Vermont Ave', 'color': 'Light Blue', 'price': 100, 'h_price': 50, 'rents': [6, 30, 90, 270, 400, 550], 'size': 3},
            9:  {'name': 'Connecticut Ave', 'color': 'Light Blue', 'price': 120, 'h_price': 50, 'rents': [8, 40, 100, 300, 450, 600], 'size': 3},
            11: {'name': 'St. Charles Place', 'color': 'Pink', 'price': 140, 'h_price': 100, 'rents': [10, 50, 150, 450, 625, 750], 'size': 3},
            12: {'name': 'Electric Company', 'color': 'Utility', 'price': 150, 'h_price': 0, 'rents': [4, 10], 'size': 2},
            13: {'name': 'States Ave', 'color': 'Pink', 'price': 140, 'h_price': 100, 'rents': [10, 50, 150, 450, 625, 750], 'size': 3},
            14: {'name': 'Virginia Ave', 'color': 'Pink', 'price': 160, 'h_price': 100, 'rents': [12, 60, 180, 500, 700, 900], 'size': 3},
            15: {'name': 'Pennsylvania Railroad', 'color': 'Railroad', 'price': 200, 'h_price': 0, 'rents': [25, 50, 100, 200], 'size': 4},
            16: {'name': 'St. James Place', 'color': 'Orange', 'price': 180, 'h_price': 100, 'rents': [14, 70, 200, 550, 750, 950], 'size': 3},
            18: {'name': 'Tennessee Ave', 'color': 'Orange', 'price': 180, 'h_price': 100, 'rents': [14, 70, 200, 550, 750, 950], 'size': 3},
            19: {'name': 'New York Ave', 'color': 'Orange', 'price': 200, 'h_price': 100, 'rents': [16, 80, 220, 600, 800, 1000], 'size': 3},
            21: {'name': 'Kentucky Ave', 'color': 'Red', 'price': 220, 'h_price': 150, 'rents': [18, 90, 250, 700, 875, 1050], 'size': 3},
            23: {'name': 'Indiana Ave', 'color': 'Red', 'price': 220, 'h_price': 150, 'rents': [18, 90, 250, 700, 875, 1050], 'size': 3},
            24: {'name': 'Illinois Ave', 'color': 'Red', 'price': 240, 'h_price': 150, 'rents': [20, 100, 300, 750, 925, 1100], 'size': 3},
            25: {'name': 'B. & O. Railroad', 'color': 'Railroad', 'price': 200, 'h_price': 0, 'rents': [25, 50, 100, 200], 'size': 4},
            26: {'name': 'Atlantic Ave', 'color': 'Yellow', 'price': 260, 'h_price': 150, 'rents': [22, 110, 330, 800, 975, 1150], 'size': 3},
            27: {'name': 'Ventnor Ave', 'color': 'Yellow', 'price': 260, 'h_price': 150, 'rents': [22, 110, 330, 800, 975, 1150], 'size': 3},
            28: {'name': 'Water Works', 'color': 'Utility', 'price': 150, 'h_price': 0, 'rents': [4, 10], 'size': 2},
            29: {'name': 'Marvin Gardens', 'color': 'Yellow', 'price': 280, 'h_price': 150, 'rents': [24, 120, 360, 850, 1025, 1200], 'size': 3},
            31: {'name': 'Pacific Ave', 'color': 'Green', 'price': 300, 'h_price': 200, 'rents': [26, 130, 390, 900, 1100, 1275], 'size': 3},
            32: {'name': 'North Carolina Ave', 'color': 'Green', 'price': 300, 'h_price': 200, 'rents': [26, 130, 390, 900, 1100, 1275], 'size': 3},
            34: {'name': 'Pennsylvania Ave', 'color': 'Green', 'price': 320, 'h_price': 200, 'rents': [28, 150, 450, 1000, 1200, 1400], 'size': 3},
            35: {'name': 'Short Line Railroad', 'color': 'Railroad', 'price': 200, 'h_price': 0, 'rents': [25, 50, 100, 200], 'size': 4},
            37: {'name': 'Park Place', 'color': 'Dark Blue', 'price': 350, 'h_price': 200, 'rents': [35, 175, 500, 1100, 1300, 1500], 'size': 2},
            39: {'name': 'Boardwalk', 'color': 'Dark Blue', 'price': 400, 'h_price': 200, 'rents': [50, 200, 600, 1400, 1700, 2000], 'size': 2}
        }
        self.name_to_idx = {v['name'].lower().strip(): k for k, v in self.props.items()}
        self.house_counts = {i: 0 for i in self.props.keys()}
        self.owner_map = {}
        self.chance_deck = ["GO", "ILLINOIS", "ST_CHARLES", "UTIL", "RAIL", "BANK_50", "GOJF", "BACK_3", "JAIL", "REPAIR", "POOR_15", "READING", "BOARDWALK", "CH_PAY_50", "CH_INC_150"]
        self.comm_deck = ["GO", "BANK_200", "DOC_50", "STOCK_50", "GOJF", "JAIL", "OP_50", "HOLIDAY_100", "TAX_20", "BIRTH_10", "LIFE_100", "HOSP_100", "SCHOOL_150", "CONSULT_25", "REPAIR", "STREET_40"]
        random.shuffle(self.chance_deck); random.shuffle(self.comm_deck)

class Player:
    def __init__(self, name, policy=None, start_bal=1500, start_pos=0, in_jail=False, jail_turns=0, gojf_count=0):
        self.name = name
        self.balance = start_bal
        self.position = start_pos
        self._owned_indices = set()
        self.gojf_count = gojf_count
        self.in_jail = in_jail
        self.jail_turns = jail_turns
        self.sim_ref = None
        self.global_bal_hist = [start_bal]
        self.global_nw_hist = [start_bal]
        default_policy = {'build_buffer': 500, 'jail_strategy': 'roll', 'buy_threshold': 0}
        self.policy = default_policy
        if policy: self.policy.update(policy)

    def get_net_worth(self):
        if not self.sim_ref: return self.balance
        p_val = sum(self.sim_ref.props[i]['price'] for i in self._owned_indices)
        h_val = sum(self.sim_ref.house_counts[i] * self.sim_ref.props[i]['h_price'] for i in self._owned_indices if self.sim_ref.props[i]['h_price'] > 0)
        return self.balance + p_val + h_val

    def adjust_balance(self, amount, controller, cause="Unknown"):
        self.balance += amount
        if self.balance < 0: controller.log_liquidity_event(self.name, self.balance, "NEGATIVE", cause)

    def play_turn(self, sim, controller, opponents):
        if self.in_jail:
            self.jail_turns += 1
            r1, r2 = random.randint(1,6), random.randint(1,6)
            if r1 == r2 or self.jail_turns >= 3: self.in_jail = False
            else: return

        d1, d2 = random.randint(1,6), random.randint(1,6)
        old_pos = self.position
        self.position = (self.position + d1 + d2) % 40
        if self.position < old_pos: self.adjust_balance(200, controller, "Passing GO")
        
        # Simple Landing logic for Web Demo
        pos = self.position
        if pos == 30: self.position = 10; self.in_jail = True
        elif pos in sim.props:
            prop = sim.props[pos]; owner = sim.owner_map.get(pos)
            if owner is None and self.balance >= prop['price']:
                self.balance -= prop['price']
                self._owned_indices.add(pos); sim.owner_map[pos] = self
            elif owner and owner != self:
                rent = prop['rents'][sim.house_counts[pos]]
                self.adjust_balance(-rent, controller, f"Rent to {owner.name}")
                owner.adjust_balance(rent, controller, "Collected Rent")

class GameController:
    def __init__(self, player_configs):
        self.sim = MonopolySimulator()
        self.players = [Player(c['name'], c.get('policy'), c.get('balance', 1500)) for c in player_configs]
        for p in self.players: p.sim_ref = self.sim
        self.turn_idx = 0
        self.liquidity_events = []
        self.roll_count = 0

    def simulate_turns(self, n):
        for _ in range(n):
            p = self.players[self.turn_idx]
            p.play_turn(self.sim, self, [])
            for pl in self.players:
                pl.global_bal_hist.append(pl.balance)
                pl.global_nw_hist.append(pl.get_net_worth())
            self.turn_idx = (self.turn_idx + 1) % len(self.players)
            self.roll_count += 1

    def log_liquidity_event(self, name, balance, direction, cause):
        self.liquidity_events.append((self.roll_count, name, balance, direction, cause))

# ==========================================
# PART 2: THE DASHBOARD (Web UI)
# ==========================================

st.set_page_config(page_title="Monopoly Stats Lab", layout="wide")
st.title("🎲 Monopoly Probability & Stats Lab")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Simulation Settings")
sim_turns = st.sidebar.slider("Number of Turns", 50, 1000, 200)
start_cash = st.sidebar.number_input("Starting Cash ($)", value=1500)
player_count = st.sidebar.radio("Number of Players", [2, 3, 4])

if st.sidebar.button("Run Simulation"):
    # Setup Players
    configs = [{'name': f"Student {chr(65+i)}", 'balance': start_cash} for i in range(player_count)]
    game = GameController(configs)
    
    # Run
    game.simulate_turns(sim_turns)
    
    # --- METRICS ---
    st.subheader("Final Standings")
    cols = st.columns(len(game.players))
    for i, p in enumerate(game.players):
        cols[i].metric(p.name, f"${p.balance}", f"NW: ${p.get_net_worth()}")

    # --- CHARTING ---
    st.divider()
    chart_data = []
    for p in game.players:
        for turn, val in enumerate(p.global_bal_hist):
            chart_data.append({"Turn": turn, "Cash": val, "Player": p.name})
    
    df = pd.DataFrame(chart_data)
    fig = px.line(df, x="Turn", y="Cash", color="Player", title="Wealth Distribution Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # --- LOGS ---
    st.subheader("Liquidity & Event Log")
    if game.liquidity_events:
        log_df = pd.DataFrame(game.liquidity_events, columns=['Turn', 'Player', 'Balance', 'Status', 'Cause'])
        st.table(log_df)
    else:
        st.write("No major liquidity events (bankruptcies) recorded.")

    # --- EXPORT ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Raw Data (CSV)", data=csv, file_name="monopoly_results.csv", mime="text/csv")

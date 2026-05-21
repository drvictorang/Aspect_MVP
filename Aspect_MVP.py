import streamlit as st
import time

# --- 1. INITIAL SETUP & SESSION STATE ---
st.set_page_config(page_title="ASPECT: Deep Heuristic Audit", layout="wide")

# Initialize timestamps in session state to persist across reruns
if 'active' not in st.session_state:
    st.session_state.active = False
    st.session_state.t0 = 0  # Start Button Click
    st.session_state.t1 = 0  # Discovery Finished
    st.session_state.t2 = 0  # Declaration Finished
    st.session_state.t3 = 0  # Execution Finished

# --- 2. SIDEBAR: THRESHOLD SETTINGS ---
with st.sidebar:
    st.header("1. Threshold Settings (ms)")
    
    st.subheader("Discovery (Reading)")
    min_disco = st.number_input("Min Discovery", value=1000)
    max_disco = st.number_input("Max Discovery", value=6000)
    
    st.subheader("Declaration (Logic)")
    min_decl = st.number_input("Min Declaration", value=1000)
    max_decl = st.number_input("Max Declaration", value=6000)
    
    st.subheader("Execution (Calculation)")
    min_exec = st.number_input("Min Execution", value=1000)
    max_exec = st.number_input("Max Execution", value=6000)
    
    st.divider()
    if st.button("🔄 RESET ALL DATA"):
        for key in ['t0', 't1', 't2', 't3']: st.session_state[key] = 0
        st.session_state.active = False
        st.rerun()

# --- 3. MAIN CONTENT: THE CHALLENGE ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.title("ASPECT: Deep Heuristic Audit")
    st.markdown("### 🧩 The Heuristic Challenge")
    st.info("The cost of petrol for a 240-km journey for a car which runs 12 km on each liter of petrol is $24. "
            "What would be the cost of petrol for a 500-km journey for a van which runs 10 km on each liter of petrol?")

    # START TRIGGER
    if not st.session_state.active:
        if st.button("▶️ START FORENSIC AUDIT", type="primary"):
            st.session_state.t0 = time.time() * 1000
            st.session_state.active = True
            st.rerun()
    
    # NODES (Sequential Visibility)
    if st.session_state.active:
        # Node 1
        st.markdown("---")
        st.markdown("### 🔍 Node 1: Discovery")
        q1 = st.radio("What is the cost per litre?", ["$1.10", "$1.20", "$1.30"], index=None)
        if q1 and st.session_state.t1 == 0:
            st.session_state.t1 = time.time() * 1000
            st.rerun()

        # Node 2
        if st.session_state.t1 > 0:
            st.markdown("### ⚠️ Node 2: Declaration")
            q2 = st.radio("How many litres are needed for the van?", ["40 Litres", "45 Litres", "50 Litres"], index=None)
            if q2 and st.session_state.t2 == 0:
                st.session_state.t2 = time.time() * 1000
                st.rerun()

        # Node 3
        if st.session_state.t2 > 0:
            st.markdown("### ⚙️ Node 3: Execution")
            q3 = st.radio("Calculate total cost for the Van:", ["$55.00", "$60.00", "$65.00"], index=None)
            if q3 and st.session_state.t3 == 0:
                st.session_state.t3 = time.time() * 1000
                st.rerun()

# --- 4. RIGHT CONTENT: HEURISTIC DASHBOARD ---
with col_right:
    st.header("Heuristic Dashboard")
    st.divider()

    # Calculation 1: Discovery = T1 - T0
    if st.session_state.t1 > 0:
        d_time = int(st.session_state.t1 - st.session_state.t0)
        st.subheader(f"Discovery: {d_time} ms = {d_time/60000:.2f} minutes")
        if d_time < min_disco: res = "Result: Guessing"
        elif d_time > max_disco: res = "Result: Logic Lag / Overload"
        else: res = "Result: Within Threshold"
        st.write(res)

    # Calculation 2: Declaration = T2 - T1
    if st.session_state.t2 > 0:
        decl_time = int(st.session_state.t2 - st.session_state.t1)
        st.subheader(f"Declaration: {decl_time} ms = {decl_time/60000:.2f} minutes")
        if decl_time < min_decl: res = "Result: Impulsive / No Strategy"
        elif decl_time > max_decl: res = "Result: Cognitive Stalling"
        else: res = "Result: Within Threshold"
        st.write(res)

    # Calculation 3: Execution = T3 - T2
    if st.session_state.t3 > 0:
        e_time = int(st.session_state.t3 - st.session_state.t2)
        st.subheader(f"Execution: {e_time}ms = {e_time/60000:.2f} minutes")
        if e_time < min_exec: res = "Result: Guessing / No Strategy"
        elif e_time > max_exec: res = "Result: Slow Computation"
        else: res = "Result: Within Threshold"
        st.write(res)
        st.success("Audit Complete.")

# --- NEW: TOTAL TIME CALCULATION ---
        st.divider()
        total_time_ms = int(st.session_state.t3 - st.session_state.t0)
        total_minutes = total_time_ms / 60000
        
        st.subheader("📊 Audit Summary")
        st.metric("Total Time Taken", f"{total_time_ms}ms", f"{total_minutes:.2f}minutes")
        st.success("Full Forensic Audit Logged.")

import streamlit as st
import time
import pandas as pd
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="ASPECT Heuristic Engine", layout="wide")

# 2. SESSION STATE DATA STORAGE (Internal Database)
if 'db' not in st.session_state:
    st.session_state.db = []

# 3. SIDEBAR: TESTER AUTH
with st.sidebar:
    st.header("Diagnostic Control")
    tester_email = st.text_input("Tester Email:", placeholder="student@example.com")
    st.divider()
    
    # DOWNLOAD BUTTON (The Investor Proof)
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Export Logic Database (CSV)",
            data=csv,
            file_name=f"ASPECT_Logic_Audit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )

# 4. MAIN INTERFACE
st.title("ASPECT: Heuristic Logic Auditor")
st.info("**Challenge:** 5:6:10 Ratio | 10% Fee | $88,800 Payout. Find Gross Profit.")

# CHRONOMETRY
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# MULTI-NODE QUESTIONS
q1 = st.radio("1. What is the 'Logical Anchor'?", ["Fee", "Net Profit", "Remainder"], index=None)
q2 = st.radio("2. How many 'units' represent the Remainder?", ["10", "11", "21"], index=None)
q3 = st.radio("3. C's 10% Fee is calculated from...?", ["Gross Profit", "Net Profit"], index=None)

# 5. THE SUBMISSION LOGIC
if st.button("Submit & Record Audit"):
    if not tester_email:
        st.warning("Identification Required.")
    elif None in [q1, q2, q3]:
        st.warning("All Logic Nodes must be completed.")
    else:
        # Calculate Metrics
        end_time = time.time()
        latency = end_time - st.session_state.start_time
        score = sum([q1 == "Remainder", q2 == "21", q3 == "Net Profit"])
        
        # Save to Internal Database
        audit_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Email": tester_email,
            "Latency_Seconds": round(latency, 2),
            "Logic_Score": f"{score}/3",
            "Node_1": q1,
            "Node_2": q2,
            "Node_3": q3
        }
        st.session_state.db.append(audit_entry)
        
        # UI FEEDBACK
        st.success(f"Audit Complete. Data Logged for {tester_email}")
        
        col1, col2 = st.columns(2)
        col1.metric("Decision Latency", f"{round(latency, 2)}s")
        col2.metric("Heuristic Accuracy", f"{score}/3")
        
        if score < 3:
            st.error("Recursive Success Fireback Engaged. View Alpha Path below.")
            st.image("https://via.placeholder.com/800x400.png?text=ALPHA+PATH:+Visual+Hierarchy+Bridge")
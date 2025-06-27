import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import get_batsman_vs_bowler_stats

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("deliveries.csv")

# App Title
# st.title("🏏 IPL BattleGround: Batsman vs Bowler")
# st.markdown("<h1 style='margin-bottom: 0;'>🏏 IPL BattleGround</h1>", unsafe_allow_html=True)
# st.markdown("<h1 style='margin-top: 0; color:#D4AF7F;'>Batsman vs Bowler</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 0;'>
    <h1 style='margin-bottom: 0;'>🏏 IPL BattleGround</h1>
    <h3 style='margin-top: 0; color:#D4AF7F;'>Batsman vs Bowler</h3>
</div>
""", unsafe_allow_html=True)
# Sidebar Selections
batsmen = sorted(df['batter'].unique())
bowlers = sorted(df['bowler'].unique())

col1, col2 = st.columns(2)
with col1:
    batsman = st.selectbox("Select Batsman", batsmen, index=batsmen.index("V Kohli") if "V Kohli" in batsmen else 0)
with col2:
    bowler = st.selectbox("Select Bowler", bowlers, index=bowlers.index("JJ Bumrah") if "JJ Bumrah" in bowlers else 0)

# Centered Button
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    clicked = st.button("⚔️ Compare Duel", use_container_width=True)

if clicked:
    stats = get_batsman_vs_bowler_stats(df, batsman, bowler)

    # Header
    st.markdown(f"### 🔍 {batsman} vs {bowler}")

    # Metric Stats
    m1, m2, m3 = st.columns(3)
    m1.metric("🏏 Runs", stats["Runs"])
    m2.metric("🎯 Balls", stats["Balls Faced"])
    m3.metric("☠️ Outs", stats["Outs"])

    m4, m5, m6 = st.columns(3)
    m4.metric("💣 SR", stats["Strike Rate"])
    m5.metric("🔥 Avg", stats["Average"])
    m6.metric("🚀 4s / 6s", f"{stats['Fours']} / {stats['Sixes']}")

    st.markdown("---")

    # Clamp dominance between 0 and 100
    dom = max(0, min(stats["Batsman Dominance %"], 100))

    # Chart Layout
    colL, colR = st.columns([1, 2])

    with colL:
        # Pie Chart
        labels = [batsman, bowler]
        sizes = [dom, 100 - dom]
        colors = ['#1f77b4', '#d62728']

        fig1, ax1 = plt.subplots(figsize=(3, 3))
        wedges, texts, autotexts = ax1.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors
        )
        ax1.axis('equal')
        st.pyplot(fig1)

    with colR:
        # Confidence Meter
        st.markdown("### 📈 Confidence Meter")

        sr = stats["Strike Rate"]
        avg = stats["Average"]

        if avg >= 30 and sr >= 135:
            confidence = 90
            desc = f"🔥 {batsman} is in total control against {bowler}"
        elif avg >= 25 and sr >= 120:
            confidence = 70
            desc = f"✅ Slight edge to {batsman}"
        elif avg < 25 and sr < 130:
            confidence = 40
            desc = f"🎯 {bowler} has restricted {batsman} well"
        elif avg < 20 or sr < 110:
            confidence = 30
            desc = f"🧊 Strong advantage for {bowler}"
        else:
            confidence = 50
            desc = f"⚔️ Balanced battle"

        st.progress(confidence / 100)
        st.caption(desc)

# app.py - Streamlit dashboard for LA Airbnb analysis (with .csv.gz support)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text

# ---------- 1. Sidebar – data source ----------------------------------------

# Just load your already-processed dataframe:
df = pd.read_parquet("prepared_airbnb.parquet")
# ... rest of the code remains unchanged ...

# ---------- 2. Standard cleaning -------------------------------------------
df = df.dropna(subset=["price", "comments"])
df["price"] = df["price"].replace(r"[\$,]", "", regex=True).astype(float)
df["room_type"] = df["room_type"].astype("category")
df["neighbourhood"] = df["neighbourhood"].astype("category")


# helper columns
df["price_bin"] = pd.qcut(
    df["price"], 5, labels=["Very Low", "Low", "Mid", "High", "Very High"]
)
def lab(x):
    if x > 0.5:
        return "Positive"
    if x < -0.5:
        return "Negative"
    return "Neutral"
df["sentiment_label"] = df["sentiment"].apply(lab)

# ---------- 3. Main page ----------------------------------------------------
st.title("Airbnb LA: Data-Driven Launch Playbook")

st.markdown(
"""
This dashboard helps a **first-time LA Airbnb host** answer four key questions:  
1. Does pricing affect review risk?  
2. Which property type is safest for reputation?  
3. What complaints dominate bad reviews?  
4. Which neighbourhoods yield high price **and** high ratings?
"""
)

# === 3.1 Sentiment vs Price (Charts 1-2) ====================================
st.header("1 · Does Price Drive Reviews?")

pivot = (
    pd.crosstab(df["price_bin"], df["sentiment_label"], normalize="index") * 100
)[["Negative", "Neutral", "Positive"]]

fig1, ax1 = plt.subplots(figsize=(8,4))
pivot.plot(kind="bar", stacked=True, color=["red","gray","green"], ax=ax1)
ax1.set_ylabel("% of Reviews")
ax1.set_xlabel("Price Category")
ax1.set_title("Review Sentiment Distribution by Price Category")
ax1.tick_params(axis="x", rotation=0)
fig1.tight_layout()

# render full-width
st.pyplot(fig1, use_container_width=True)

neg_rate = (
    df.groupby("price_bin")["sentiment_label"]
    .apply(lambda x: (x=="Negative").mean())
)
fig2, ax2 = plt.subplots(figsize=(8,3.5))
neg_rate.plot(kind="bar", color="crimson", ax=ax2)
ax2.set_ylabel("P( Negative Review )")
ax2.set_xlabel("Price Category")
ax2.set_title("Probability of Negative Review vs Price")
ax2.tick_params(axis="x", rotation=0)
fig2.tight_layout()
st.pyplot(fig2, use_container_width=True)

st.info("Pricing higher only marginally reduces bad-review risk.")

# === 3.2 Sentiment vs Room Type (Charts 3-4) ================================
st.header("2 · Which Property Type Protects Reputation?")

pivot_rt = (
    pd.crosstab(df["room_type"], df["sentiment_label"], normalize="index")*100
)[["Negative","Neutral","Positive"]]

fig3, ax3 = plt.subplots(figsize=(8,3.5))
pivot_rt.plot(kind="bar", stacked=True, color=["red","gray","green"], ax=ax3)
ax3.set_ylabel("% of Reviews")
ax3.set_xlabel("Room Type")
ax3.set_title("Sentiment Distribution by Room Type")
ax3.tick_params(axis="x", rotation=0)
fig3.tight_layout()
st.pyplot(fig3, use_container_width=True)

neg_rate_rt = (
    df.groupby("room_type")["sentiment_label"]
    .apply(lambda x:(x=="Negative").mean())
)
fig4, ax4 = plt.subplots(figsize=(8,3.5))
neg_rate_rt.plot(kind="bar", color="crimson", ax=ax4)
ax4.set_ylabel("P( Negative Review )")
ax4.set_xlabel("Room Type")
ax4.set_title("Negative-Review Risk by Room Type")
ax4.tick_params(axis="x", rotation=0)
fig4.tight_layout()
st.pyplot(fig4, use_container_width=True)

# === 3.3 Top Complaint Keywords (Chart 5) ===================================
st.header("3 · What Actually Triggers Bad Reviews?")

negatives = df[df["sentiment_label"]=="Negative"].copy()
keywords = ['wifi','internet','noise','dirty','clean','parking','air','heat',
            'hot','smell','bed','shower','host','bugs','checkin']
for kw in keywords:
    negatives[kw] = negatives["comments"].str.lower().str.contains(kw)

keyword_counts = {kw:negatives[kw].sum() for kw in keywords}
top5 = dict(sorted(keyword_counts.items(), key=lambda kv: kv[1], reverse=True)[:5])

fig5, ax5 = plt.subplots(figsize=(8,3.5))
ax5.barh(list(reversed(list(top5.keys()))), list(reversed(list(top5.values()))),
         color="crimson")
ax5.set_xlabel("Mentions in Negative Reviews")
ax5.set_ylabel("Complaint Keywords")
ax5.set_title("Top Complaint Keywords")
ax5.tick_params(axis="y", rotation=0)
st.pyplot(fig5, use_container_width=True)

# === 3.4  Neighbourhood Scatter (Price ↑ & Sentiment ↑) =====================
st.header("4 · Where to Launch? Price & Ratings by Neighbourhood")
st.image(
    "neighborhood_scatter.png",  # Make sure the PNG is in your project folder
    caption="Top-Tier LA Neighborhoods (Price ↑ & Sentiment ↑)",
    use_container_width=True # was use_column_width=True
)
# ---------- 4. Footer -------------------------------------------------------
st.markdown("---")
st.markdown("**Flores, Claudine Yeszha | Olaira, Eljane | Reyes, Samantha Clariz**")

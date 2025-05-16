# app.py  ── Streamlit dashboard (image-only version)
import streamlit as st

# ───────────────────────  Title & intro  ────────────────────────────
st.title("Airbnb LA: Data-Driven Launch Playbook")
st.markdown(
"""
This dashboard helps a **first-time LA Airbnb host** answer four key questions:

1. Does pricing affect bad-review risk?  
2. Which property type is safest for reputation?  
3. What complaints dominate negative reviews?  
4. Where should you launch to command **high price _and_ high ratings?**
"""
)

# ───────────────────────  1. Price vs. Reviews  ─────────────────────
st.header("1 · Does Price Drive Reviews?")
st.image(
    "price_sentiment_distribution.png",
    caption="Review Sentiment Distribution by Price Category",
    use_container_width=True
)
st.image(
    "probability_of_negative_review.png",
    caption="Probability of Getting a Negative Review by Price Category",
    use_container_width=True
)

# ───────────────────────  2. Room-Type Safety  ──────────────────────
st.header("2 · Which Property Type Protects Reputation?")
st.image(
    "room_type_sentiment.png",
    caption="Sentiment Distribution by Room Type",
    use_container_width=True
)

# ───────────────────────  3. Complaint Themes  ──────────────────────
st.header("3 · What Actually Triggers Bad Reviews?")
st.image(
    "top_complaint.png",
    caption="Top Complaint Keywords in Negative Reviews",
    use_container_width=True
)
st.image(
    "top5_complaint.png",
    caption="Top 5 Complaint Issues in Negative Reviews",
    use_container_width=True
)

# ───────────────────────  4. Launch Location  ───────────────────────
st.header("4 · Where to Launch? Price & Ratings by Neighbourhood")
st.image(
    "neighborhood_scatter.png",
    caption="Top-Tier LA Neighborhoods (Price ↑ & Sentiment ↑)",
    use_container_width=True
)

# ---------- 4. Footer -------------------------------------------------------
st.markdown("---")
st.markdown("**Flores, Claudine Yeszha | Olaira, Eljane | Reyes, Samantha Clariz**")

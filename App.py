import streamlit as st
import pandas as pd

st.set_page_config(page_title="Garment Workers Weekly Calculator", layout="centered")
st.title("🧵 Garment Workers Weekly Earnings Calculator")

# ------------------- SESSION STATE -------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ------------------- ADD NEW SUIT FORM -------------------
with st.form("add_suit", clear_on_submit=True):
    suit_name = st.text_input("Suit Name")
    total_pieces = st.number_input("Total Pieces", min_value=0, step=1)
    price_per_piece = st.number_input("Price per Piece", min_value=0.0, step=0.5, format="%.2f")

    submitted = st.form_submit_button("➕ Add Suit")
    if submitted and suit_name and total_pieces > 0 and price_per_piece > 0:
        suit_price = total_pieces * price_per_piece
        st.session_state.data.append({
            "Suit Name": suit_name,
            "Total Pieces": total_pieces,
            "Price per Piece": price_per_piece,
            "Total Suit Price": suit_price
        })

# ------------------- DISPLAY DATA -------------------
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    # Calculate totals
    total_pieces_sum = df["Total Pieces"].sum()
    total_price_sum = df["Total Suit Price"].sum()

    # Create total row
    total_row = pd.DataFrame({
        "Suit Name": ["TOTAL"],
        "Total Pieces": [total_pieces_sum],
        "Price per Piece": [""],
        "Total Suit Price": [total_price_sum]
    })

    df_with_total = pd.concat([df, total_row], ignore_index=True)

    st.subheader("📋 Weekly Work Summary")
    st.dataframe(df_with_total, use_container_width=True)

    # ------------------- DELETE BUTTONS -------------------
    st.subheader("🗑️ Manage Rows")
    for i, row in df.iterrows():
        if st.button(f"❌ Delete {row['Suit Name']}", key=f"del_{i}"):
            st.session_state.data.pop(i)
            st.rerun()

    # ------------------- CLEAR ALL -------------------
    if st.button("🔄 Clear All Data"):
        st.session_state.data = []
        st.rerun()

else:
    st.info("No data added yet. Start by entering suit details above.")

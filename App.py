import streamlit as st
import pandas as pd
from io import BytesIO

# ------------------- PAGE SETTINGS -------------------
st.set_page_config(page_title="Garment Workers Weekly Calculator", layout="centered")
st.title("🧵 Garment Workers Weekly Earnings Calculator")

st.markdown("Enter the details of each suit below:")

# ------------------- SESSION STATE -------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ------------------- ADD NEW SUIT FORM -------------------
with st.form("add_suit", clear_on_submit=True):
    suit_name = st.text_input("Suit Name")   # Name of suit (text input)
    total_pieces = st.number_input("Total Pieces", min_value=0, step=1)  # Pieces made
    price_per_piece = st.number_input("Price per Piece", min_value=0.0, step=0.5, format="%.2f")  # Rate per piece

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

    # Create a Total row
    total_row = pd.DataFrame({
        "Suit Name": ["TOTAL"],
        "Total Pieces": [total_pieces_sum],
        "Price per Piece": [""],   # leave empty
        "Total Suit Price": [total_price_sum]
    })

    # Append Total row to df
    df_with_total = pd.concat([df, total_row], ignore_index=True)

    # Show summary table
    st.subheader("📋 Weekly Work Summary")
    st.dataframe(df_with_total, use_container_width=True)

    # ------------------- EXPORT OPTIONS -------------------
    st.subheader("📂 Export Options")

    # CSV Export
    csv = df_with_total.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download as CSV",
        data=csv,
        file_name="weekly_earnings.csv",
        mime="text/csv"
    )

    # Excel Export
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_with_total.to_excel(writer, index=False, sheet_name="Weekly Earnings")
        worksheet = writer.sheets["Weekly Earnings"]
        worksheet.set_column("A:D", 20)

    st.download_button(
        "⬇️ Download as Excel",
        data=output.getvalue(),
        file_name="weekly_earnings.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Reset Button
    if st.button("🔄 Clear All Data"):
        st.session_state.data = []
        st.experimental_rerun()

else:
    st.info("No data added yet. Start by entering suit details above.")

import streamlit as st

st.set_page_config(page_title="Pip Navigator", page_icon="📊", layout="centered")
st.title("📊 Pip Navigator")

# Add logo
st.image("https://i.ibb.co/DKSzM3f/pipnav-logo.webp", width=120)

st.markdown("Select the instrument type to calculate pip risk, gain, R:R ratio, and dollar risk.")

# Choose asset type
asset_type = st.selectbox("🔹 Select Instrument", ["Forex (5 decimals)", "Gold (2 decimals)"])

# Set pip value based on instrument
pip_value_per_lot = 10 if "Gold" in asset_type else 1

# Set decimal precision based on instrument
decimals = "%.2f" if "Gold" in asset_type else "%.5f"

# Inputs
entry = st.number_input("Entry Price", format=decimals)
stop_loss = st.number_input("Stop Loss", format=decimals)
take_profit = st.number_input("Take Profit", format=decimals)
position = st.selectbox("Position Type", ["Buy", "Sell"])

st.markdown("---")
st.subheader("💰 Risk Management")
account_balance = st.number_input("Account Balance ($)", min_value=0.0, step=100.0)
risk_percent = st.number_input("Risk %", min_value=0.0, max_value=100.0, step=0.1)

# Calculate
if st.button("Calculate"):
    try:
        # Pip Calculation
        if position.lower() == "buy":
            pips_risked = abs(entry - stop_loss)
            pips_gained = abs(take_profit - entry)
        else:
            pips_risked = abs(stop_loss - entry)
            pips_gained = abs(entry - take_profit)

        if pips_risked == 0:
            st.error("❌ Invalid Stop Loss. Risk cannot be zero.")
        else:
            rr_ratio = round(pips_gained / pips_risked, 2)

            # Dollar risk and profit
            money_risked = pips_risked * pip_value_per_lot
            money_gained = pips_gained * pip_value_per_lot

            # Recommended lot size
            risk_amount = (account_balance * (risk_percent / 100))
            recommended_lot = round(risk_amount / money_risked, 2) if money_risked > 0 else 0

            st.success("✅ Calculation Results")
            st.write(f"🔸 **Pips Risked**: `{pips_risked:.2f}`")
            st.write(f"🔸 **Pips Gained**: `{pips_gained:.2f}`")
            st.write(f"🔸 **R:R Ratio**: `{rr_ratio}`")
            st.write(f"💸 **Risk Amount per 1 Lot**: `${money_risked:.2f}`")
            st.write(f"💵 **Profit per 1 Lot**: `${money_gained:.2f}`")
            st.write(f"📈 **Recommended Lot Size**: `{recommended_lot} lot`")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

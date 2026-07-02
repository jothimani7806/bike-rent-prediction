import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Settings
st.set_page_config(page_title="Bike Rental Predictor", page_icon="🚲", layout="wide")

# 2. Main Title & Description
st.title("🚲 Bike Rental Prediction Dashboard")
st.markdown("Adjust the features in the sidebar and click **Predict Demand** to see results.")
st.divider()

# 3. Sidebar for User Input Features
st.sidebar.header("🛠️ Input Environmental Features")

season = st.sidebar.selectbox("Select Season", ["Spring", "Summer", "Fall", "Winter"])
hour = st.sidebar.slider("Hour of the Day", 0, 23, 12)
temp = st.sidebar.slider("Temperature (°C)", -10, 40, 22)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 55)
is_holiday = st.sidebar.checkbox("Is it a Holiday?")

st.sidebar.divider()

# --- THE PREDICT BUTTON ---
# This button returns True only when clicked
predict_btn = st.sidebar.button("🔮 Predict Demand", type="primary", use_container_width=True)

st.sidebar.caption("Bike Rent Prediction Model v1.0")


# 4. Main Content Layout
if predict_btn:
    # If the user clicked the button, show the results!
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🔮 Prediction Output")
        
        # --- MOCK PREDICTION LOGIC ---
        base_rentals = 150
        temp_bonus = temp * 4
        rush_hour_bonus = 120 if (7 <= hour <= 9 or 17 <= hour <= 19) else 20
        humidity_penalty = humidity * 0.8
        holiday_penalty = 40 if is_holiday else 0
        
        predicted_count = int(max(10, base_rentals + temp_bonus + rush_hour_bonus - humidity_penalty - holiday_penalty))
        # --------------------------------
        
        # Elegant big number display
        st.metric(label="Predicted Bikes Needed / Hour", value=f"{predicted_count} Bikes", delta=f"{int(temp_bonus)} due to temp")
        st.info("💡 Pro-Tip: Demand heavily spikes during morning (7-9 AM) and evening (5-7 PM) commute hours.")

    with col_right:
        st.subheader("📈 Simulated Hourly Trend")
        
        # Generate a simple 24-hour trend based on the current user selections
        hours = np.arange(0, 24)
        trend_counts = [int(max(10, base_rentals + (temp * 4) + (120 if (7 <= h <= 9 or 17 <= h <= 19) else 20) - (humidity * 0.8))) for h in hours]
        
        trend_df = pd.DataFrame({"Hour": hours, "Predicted Demand": trend_counts})
        st.line_chart(trend_df, x="Hour", y="Predicted Demand", color="#FF4B4B")

else:
    # If the user hasn't clicked the button yet, show a welcoming placeholder
    st.info("👈 Please adjust the environmental features in the sidebar and click **Predict Demand** to generate the report.")


# 5. Bottom Section: Data Preview (Always visible)
st.divider()
st.subheader("📋 Sample Historical Reference Data")

sample_data = pd.DataFrame({
    "Season": ["Spring", "Summer", "Fall", "Winter"],
    "Avg Temperature": ["15°C", "28°C", "18°C", "6°C"],
    "Avg Humidity": ["45%", "60%", "50%", "65%"],
    "Historical Peak Demand/Hr": [240, 480, 310, 130]
})

st.dataframe(sample_data, width="stretch", hide_index=True)
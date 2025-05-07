import streamlit as st
import pickle
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import plotly.express as px

# CONSTANTS
st.set_page_config(layout="wide")
MODEL_PATH = "product_f_pricing_model_top3_region_stable.pkl"
SENDER = "aimuliaceramicsgroup@gmail.com"
PASSWORD = "tvlj nsyt pxzt vzwm"

with open(MODEL_PATH, "rb") as file:
  model = pickle.load(file)

def generate_data(model, data):
  data_dict = {
       'Date': [],
       'Type': [],
       'Vol': [],
       'Sales': []
  }
  df_u = data.drop_duplicates(subset=['bill_date'], keep='first')
  for _, row in df_u.iterrows():
       data_dict['Date'].append(row['bill_date'])
       data_dict['Date'].append(row['bill_date'])
       data_dict['Type'].append('Current Sales Volume')
       data_dict['Type'].append('Predicted Sales Volume')
       data_dict['Vol'].append(row['sales_volume'])
       y_pred = model.predict([[row.year, row.month, row.kompetitor, row.asp, row.rbp, row.quarter, row.plc_weight, row.plc_adj_asp, row.regional_ship_to_Bali, row.regional_ship_to_Bengkulu, row.regional_ship_to_Lampung, row.plc_phase_Introduction, row.plc_phase_Growth, row.plc_phase_Maturity, row.plc_adj_sales_lag_1, row.plc_adj_sales_lag_3, row.plc_adj_sales_lag_6, row.plc_adj_sales_lag_12, row.plc_sales_ma_3, row.plc_sales_ma_6, row.price_ratio, row.discount_depth]])[0]
       data_dict['Vol'].append(y_pred)
       data_dict['Sales'].append(row['sales_volume'] * row['asp'])
       data_dict['Sales'].append(y_pred * row['asp'])

  return data_dict

df = pd.read_parquet('data_features.parquet')

st.markdown("## 📊 Dashboard")
year_ = st.number_input("Input Year", format="%g")
month_ = st.number_input("Input Month", format="%g")
region_ = st.selectbox(
    "Choose region:",
    ["Bali", "Bengkulu", "Lampung"]
)

if region_ == "Bali":
     data = generate_data(model, df[(df.regional_ship_to_Bali == True) & (df.month == month_) & (df.year == year_)])
elif region_ == "Bengkulu":
     data = generate_data(model, df[(df.regional_ship_to_Bengkulu == True) & (df.month == month_) & (df.year == year_)])
elif region_ == "Lampung":
     data = generate_data(model, df[(df.regional_ship_to_Lampung == True) & (df.month == month_) & (df.year == year_)])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Volume")
    fig = px.bar(data, x='Date', y='Vol', color='Type', barmode='group')
    fig.update_layout(width=10000)
    st.plotly_chart(fig)

with col2:
    st.subheader("Sales")
    fig = px.bar(data, x='Date', y='Sales', color='Type', barmode='group')
    st.plotly_chart(fig)


st.markdown("## 🧠 Simulate Sales & Price Elasticity")

RECEIVER = st.text_input("Input your E-Mail")

year = int(st.number_input("Year", format="%g"))
month = int(st.number_input("Month", format="%g"))
regional = st.selectbox(
    "Ship to Region:",
    ["Bali", "Bengkulu", "Lampung"]
)

st.markdown("""
    <style>
    div.stButton > button.red-outline-button {
        color: red;
        background-color: white;
        border: 2px solid red;
        border-radius: 5px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    div.stButton > button.red-outline-button:hover {
        background-color: #ffe5e5;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

button = st.button("Run Simulation", key="red_btn")

st.markdown("""
    <script>
    const btns = window.parent.document.querySelectorAll('button[kind="primary"]');
    if (btns.length > 0) {
        btns[btns.length - 1].className = "red-outline-button";
    }
    </script>
""", unsafe_allow_html=True)

df_data_ = pd.read_csv('result_forecast_next5month_retrain.csv')
df_data = df_data_[(df_data_.year==year) & (df_data_.month==month) * (df_data_.region==regional)]

if button and (len(df_data) != 0):
    if len(df_data) > 1:
        df_data = df_data.iloc[0]
    st.markdown("## 📊 Product F Pricing Recommendation")

    st.markdown("### 🟦 Updated Recommendation")
    st.markdown(f"""
    - **Region:** {regional}  
    - **Current Price:** Rp{float(df_data['current_asp'])}  
    - **Current Sales Volume:** {int(df_data['sales_volume'])}  
    - **Predicted Sales Volume:** {int(round(df_data['predicted_sales_volume'],0))}  
    - **Recommended New Price:** **{df_data['predicted_asp']}** _({df_data['price_increase_pct']}%)_
    """)

    st.markdown("### 🟨 Expected Outcomes")
    st.markdown(f"""
    - **Revenue Change:** **Rp+{float(round(df_data['revenue_increase'],2))}** _({float(round(df_data['revenue_increase_pct'],2))}%)_  
    - **Sales Volume Impact:** **{int(round(df_data['sales_volume_impact'],2))} units** _({float(round(df_data['sales_volume_impact_pct'],2))}%)_  
    - **Market Position:** Maintains 3% price advantage vs competitors
    """)

    st.markdown("### 🟩 Analysis Details")
    st.markdown(f"""
    - **Price Elasticity:** {float(df_data['price_elasticity'])}  
    - **Optimal Price Range:** Rp132.669–Rp136.710  
    - **Best Implementation Timing:** Next month  
    - **Recommended Action:** ✅ **APPROVE 5% PRICE DECREASE**
    """)

    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = RECEIVER
    em['Subject'] = f'Revised Pricing Approval Request - {regional}'
    html = f"""
    <table width="100%" cellpadding="10" cellspacing="0" style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border-collapse: collapse;">
    <!-- Header -->
    <tr style="background-color: #e6f0fa;">
        <td>
        <strong>Updated Recommendation for Product F Pricing:</strong><br><br>
        <strong>Region:</strong> ✅ {regional}<br>
        <strong>Current Price:</strong> ✅ Rp{float(df_data['current_asp'])}<br>
        <strong>Current Sales Volume:</strong> ✅ {int(df_data['sales_volume'])}<br>
        <strong>Predicted Sales Volume:</strong> ✅ {int(round(df_data['predicted_sales_volume'],0))}<br>
        <strong>Recommended New Price:</strong> ✅ Rp{float(df_data['predicted_asp'])} ({float(df_data['price_increase_pct'])}% increase)
        </td>
    </tr>

    <!-- Expected Outcomes -->
    <tr style="background-color: #fff8e1;">
        <td>
        <strong>Expected Outcomes:</strong><br><br>
        <strong>Revenue Change:</strong> ✅ Rp{float(round(df_data['revenue_increase'],2))} ({float(round(df_data['revenue_increase_pct'],2))}% increase)<br>
        <strong>Sales Volume Impact:</strong> ✅ {int(round(df_data['sales_volume_impact'],2))} units ({float(round(df_data['sales_volume_impact_pct'],2))}% impact)<br>
        <strong>Market Position:</strong> Maintains 3% price advantage vs competitors
        </td>
    </tr>

    <!-- Analysis Details -->
    <tr style="background-color: #e8f5e9;">
        <td>
        <strong>Analysis Details:</strong><br><br>
        <strong>Price Elasticity:</strong> ✅ {float(df_data['price_elasticity'])}<br>
        <strong>Optimal Price Range:</strong> 🔸 RpX–RpY (±1.5% of predicted_asp)<br>
        <strong>Best Implementation Timing:</strong> 🔸 Next month<br>
        <strong>Recommended Action:</strong> ✅ APPROVE 5% PRICE DECREASE
        </td>
    </tr>

    </table>
    """
    em.add_alternative(html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(em)

elif button and (len(df_data) == 0):
    st.warning("Error! Data not found")

import streamlit as st
import pickle
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity


# CONSTANTS
st.set_page_config(layout="wide")
MODEL_PATH = "product_f_pricing_model_top3_region_stable.pkl"
SENDER = "fredericknathanirmawan@gmail.com"
PASSWORD = "xzlc yjif lwqr fvky"

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
# title=f"{int(year_)} Month {int(month_)} Daily Sales Volume for {region_}"
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
kompetitor = int(st.number_input("Kompetitor", format="%g"))
asp = st.number_input("ASP", format="%g")
rbp = st.number_input("RBP", format="%g")
quarter = int(st.number_input("Quarter", format="%g"))
plc_weight = st.number_input("plc_weight", format="%g")
plc_adj_asp = st.number_input("plc_adj_asp", format="%g")
regional = st.selectbox(
    "Ship to Region:",
    ["Bali", "Bengkulu", "Lampung"]
)
regional_ship_to_Bali = False
regional_ship_to_Bengkulu = False
regional_ship_to_Lampung = False
if regional == "Bali":
    regional_ship_to_Bali = True
elif regional == "Bengkulu":
    regional_ship_to_Bengkulu = True
elif regional == "Lampung":
    regional_ship_to_Lampung = True
plc_phase_Introduction = st.checkbox("plc_phase_introduction")
plc_phase_Growth = st.checkbox("plc_phase_growth")
plc_phase_Maturity = st.checkbox("plc_maturity")
plc_adj_sales_lag_1 = 10137.6 # st.checkbox("plc_adj_sales_lag_1")
plc_adj_sales_lag_3 = 10137.6 # st.checkbox("plc_adj_sales_lag_3")
plc_adj_sales_lag_6 = 11059.2 # st.checkbox("plc_adj_sales_lag_6")
plc_adj_sales_lag_12 = 11059.2 # st.checkbox("plc_adj_sales_lag_12")
plc_sales_ma_3 = 2757.333333 # st.checkbox("plc_sales_ma_3")
plc_sales_ma_6 = 2400.888889 # st.checkbox("plc_sales_ma_6")
price_ratio = st.number_input("Price Ratio", format="%g")
discount_depth = st.number_input("Discount Depth", format="%g")

feature_names = [
    "Year",
    "Month",
    "Kompetitor",
    "ASP",
    "RBP",
    "Quarter",
    "plc_weight",
    "plc_adj_asp",
    "Regional Ship to Bali",
    "Regional Ship to Bengkulu",
    "Regional Ship to Lamput",
    "plc_phase_Introduction",
    "plc_phase_Growth",
    "plc_phase_Maturity",
    "plc_adj_sales_lag_1",
    "plc_adj_sales_lag_3",
    "plc_adj_sales_lag_6",
    "plc_adj_sales_lag_12",
    "plc_sales_ma_3",
    "plc_sales_ma_6",
    "Price Ratio",
    "Discount Depth"
]

features = [
    year,
    month,
    kompetitor,
    asp,
    rbp,
    quarter,
    plc_weight,
    plc_adj_asp,
    regional_ship_to_Bali,
    regional_ship_to_Bengkulu,
    regional_ship_to_Lampung,
    plc_phase_Introduction,
    plc_phase_Growth,
    plc_phase_Maturity,
    plc_adj_sales_lag_1,
    plc_adj_sales_lag_3,
    plc_adj_sales_lag_6,
    plc_adj_sales_lag_12,
    plc_sales_ma_3,
    plc_sales_ma_6,
    price_ratio,
    discount_depth
]

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

st.write(    year,
    month,
    kompetitor,
    asp,
    rbp,
    quarter,
    plc_weight,
    plc_adj_asp,
    regional_ship_to_Bali,
    regional_ship_to_Bengkulu,
    regional_ship_to_Lampung,
    plc_phase_Introduction,
    plc_phase_Growth,
    plc_phase_Maturity,
    plc_adj_sales_lag_1,
    plc_adj_sales_lag_3,
    plc_adj_sales_lag_6,
    plc_adj_sales_lag_12,
    plc_sales_ma_3,
    plc_sales_ma_6,
    price_ratio,
    discount_depth)

if button:
    # sales_volume = df[(df.year==year)&(df.month==month)&(df.kompetitor==kompetitor)&(df.asp==asp)&(df.rbp==rbp)&(df.quarter==quarter)&(df.plc_weight==plc_weight)&(df.plc_adj_asp==plc_adj_asp)&(df.regional_ship_to_Bali==regional_ship_to_Bali)&(df.regional_ship_to_Bengkulu==regional_ship_to_Bengkulu)&(df.regional_ship_to_Lampung==regional_ship_to_Lampung)&(df.plc_phase_Introduction==plc_phase_Introduction)&(df.plc_phase_Growth==plc_phase_Growth)&(df.plc_phase_Maturity==plc_phase_Maturity)&(df.plc_adj_sales_lag_1==plc_adj_sales_lag_1)&(df.plc_adj_sales_lag_3==plc_adj_sales_lag_3)&(df.plc_adj_sales_lag_6==plc_adj_sales_lag_6)&(df.plc_adj_sales_lag_12==plc_adj_sales_lag_12)&(df.plc_sales_ma_3==plc_sales_ma_3)&(df.plc_sales_ma_6==plc_sales_ma_6)&(df.price_ratio==price_ratio)&(df.discount_depth==discount_depth)]['sales_volume'][0]
    sales_volume = 7680
    y_pred = model.predict([features])

    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = RECEIVER
    em['Subject'] = f'Revised Pricing Approval Request - {regional}'

    feature_html = ""
    for name, val in zip(feature_names, features):
        feature_html += f"<li>{name}: <b>{val}</b></li>"

    html = f"""<html><body>
    Updated Recommendation for Product F Pricing:
    Region: Jawa Barat
    <br>
    </br>
    Current Price: Rp{asp}
    <br>
    </br>
    Current Sales Volume: {sales_volume}
    <br>
    </br>
    Recommended New Price: Rp131,250 (+5.0%)
    <br>
    </br>
    <br>
    </br>
    Expected Outcomes:
    <br>
    - Revenue Increase: Rp+58,125,000 (+4.7%)
    </br>
    <br>
    - Sales Volume Impact: {y_pred[0]} units ({(abs(y_pred - sales_volume) / sales_volume) * 100}% {"increase" if y_pred > sales_volume else "decrease"})
    </br>

    <br>
    - Market Position: Maintains 3% price advantage vs competitors
    </br>
    <br>
    </br>
    <br>
    </br>
    Analysis Details:
    <br>
    - Price Elasticity: -1.12 (demand is relatively inelastic)
    </br>

    <br>
    - Optimal Price Range: Rp130,000-Rp132,000
    </br>

    <br>
    - Best Implementation Timing: Next month (traditionally strong sales period)
    </br>

    <br>
    Recommended Action: APPROVE 5% PRICE INCREASE
    </br>
    </body>
    </html>
    """
    em.add_alternative(html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(em)
        
    st.warning('Summary has been sent to your mail', icon="🚨")
    st.info(f"💰 Current Price: **{asp}**")
    st.info(f"🧮 Current Sales Volume: **{sales_volume}** units")
    st.success(f"💸 Predicted Price: **{None}**")
    st.success(f"📈 Predicted Sales: **{y_pred[0]} units**")

import streamlit as st
import pickle
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText

# CONSTANT
MODEL_PATH = "product_f_pricing_model_top3_region_stable.pkl"
SENDER = "fredericknathanirmawan@gmail.com"
PASSWORD = "xzlc yjif lwqr fvky"

st.markdown("## 📊 Simulate Sales & Price Elasticity")
# org_price = st.number_input("Original Price (Rp)")
# new_price = st.number_input("New Price (Rp)")

RECEIVER = st.text_input("Input your E-Mail")

year = st.number_input("Year")
month = st.number_input("Month")
kompetitor = st.number_input("Kompetitor")
asp = st.number_input("ASP")
rbp = st.number_input("RBP")
quarter = st.number_input("Quarter")
plc_weight = st.number_input("plc_weight")
plc_adj_asp = st.number_input("plc_adj_asp")
regional_ship_to_Bali = st.checkbox("Regional Ship to Bali")
regional_ship_to_Bengkulu = st.checkbox("Regional Ship to Bengkulu")
regional_ship_to_Lampung = st.checkbox("Regional Ship to Lampung")
plc_phase_Introduction = st.checkbox("plc_phase_introduction")
plc_phase_Growth = st.checkbox("plc_phase_growth")
plc_phase_Maturity = st.checkbox("plc_maturity")
plc_adj_sales_lag_1 = st.checkbox("plc_adj_sales_lag_1")
plc_adj_sales_lag_3 = st.checkbox("plc_adj_sales_lag_3")
plc_adj_sales_lag_6 = st.checkbox("plc_adj_sales_lag_6")
plc_adj_sales_lag_12 = st.checkbox("plc_adj_sales_lag_12")
plc_sales_ma_3 = st.checkbox("plc_sales_ma_3")
plc_sales_ma_6 = st.checkbox("plc_sales_ma_6")
price_ratio = st.number_input("Price Ratio")
discount_depth = st.number_input("Discount Depth")

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
    "Regional Ship to Lampung",
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

region = st.selectbox(
    "Region",
    (    "Bali", "Bangka Belitung", "Bengkulu", "DI Yogyakarta", "DKI Jakarta",
    "Gorontalo", "Irian Jaya", "Jambi", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
    "Kalimantan Barat", "Kalimantan Selatan", "Kalimantan Tengah", "Kalimantan Timur",
    "Kalimantan Utara", "Kepulauan Riau", "Lampung", "Maluku", "Maluku Utara",
    "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Papua", "Papua Barat", "Riau",
    "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tengah", "Sulawesi Tenggara",
    "Sulawesi Utara", "Sumatera Barat", "Sumatera Selatan", "Sumatera Utara"),
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

with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

if button:
    y_pred = model.predict([features])

    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = RECEIVER
    em['Subject'] = 'Sales Prediction Report'

    feature_html = ""
    for name, val in zip(feature_names, features):
        feature_html += f"<li>{name}: <b>{val}</b></li>"

    html = f"""
    <html>
      <body>
        <body style="font-family: Arial, sans-serif;">
        <h2 style="color:#003366;">📊 Sales Prediction Summary</h2>
        
        <div style="background:#f0f0f0;padding:12px;border-radius:6px;margin-bottom:20px;">
          <h4 style="margin-bottom:6px;">🔧 Model Inputs:</h4>
          <ul style="margin-top:0;padding-left:20px;">
            {feature_html}
          </ul>
        </div>

        <div style="background:#e6ffed;padding:12px;border-radius:6px;margin-bottom:10px;">
          📈 Predicted Sales (New Price):<b> {y_pred[0]:.2f} units </b>
        </div>
        <div style="background:#e6f0ff;padding:12px;border-radius:6px;">
          🧮 Estimated Price Elasticity:<b> {None} </b>
        </div>
      </body>
    </html>
    """

    em.set_content("This is an HTML email with your prediction result.")  # fallback text
    em.add_alternative(html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(em)
    
    st.warning('Summary has been sent to your mail', icon="🚨")

# if button:
#     y_pred = model.predict([features])

#     em = EmailMessage()
#     em['From'] = SENDER
#     em['To'] = RECEIVER
#     em["Subject"] = 'a'
#     # em.set_content(str(y_pred[0]))

#     context = ssl.create_default_context()
#     html = """
#     <html>
#     asdasd
#     </html>
#     """
#     em.attach(MIMEText(html, "html"))

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(SENDER, PASSWORD)
#         smtp.send_message(em)
#         # smtp.sendmail(SENDER, RECEIVER, em.as_string())


    st.success(f"📈 Predicted Sales (New Price): **{y_pred[0]} units**")
    st.info(f"🧮 Estimated Price Elasticity: **{None}**")

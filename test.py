import streamlit as st
import pandas as pd

# ================= CONFIG =================

CSV_FILE_PATH = r"C:\Users\adity\Desktop\Customer support model\Customer_support_data.csv"

# ================= LOAD DATA =================

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE_PATH)
    df['Order_id'] = df['Order_id'].astype(str)
    return df

df = load_data()

# ================= INDEXING (SUPER FAST) =================

@st.cache_data
def create_index(df):
    order_index = {}

    for _, row in df.iterrows():
        order_index[row['Order_id']] = row

    return order_index

order_index = create_index(df)

# ================= GUARDRAILS =================

def input_guardrail(user_input):
    blocked_patterns = ["hack", "bypass", "ignore instructions", "pretend you are", "act as"]
    return not any(p in user_input.lower() for p in blocked_patterns)


def domain_check(query):
    allowed = ["order", "refund", "delivery", "payment", "status", "issue"]
    return any(word in query.lower() for word in allowed)


def output_guardrail(response):
    if "maybe" in response.lower():
        return "⚠️ Not sure. Connecting to human agent."
    return response


def refusal_response():
    return "🚫 I cannot assist with that request. Please contact support."

# ================= MEMORY =================

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "order_id" not in st.session_state:
    st.session_state.order_id = None

# ================= FAST SEARCH =================

def search_order_fast(order_id):
    return order_index.get(str(order_id), None)

# ================= AGENT =================

def agent_response(user_input):

    # Guardrail
    if not input_guardrail(user_input):
        return refusal_response()

    # Memory
    if "same issue" in user_input.lower():
        user_input = st.session_state.last_query

    st.session_state.last_query = user_input

    # Domain check
    if not domain_check(user_input):
        return "⚠️ I only handle customer support queries."

    # Ask Order ID if missing
    if st.session_state.order_id is None:
        return "📦 Please provide your Order ID."

    order_id = st.session_state.order_id
    row = search_order_fast(order_id)

    if row is None:
        return "❌ Order not found. Please check your Order ID."

    # ================= RESPONSE LOGIC =================

    if "status" in user_input.lower() or "order" in user_input.lower():
        response = f"""
🧾 Order ID: {order_id}
📦 Status: {row['category']} - {row['Sub-category']}
📅 Order Date: {row['order_date_time']}
"""

    elif "refund" in user_input.lower():
        response = f"""
💰 Refund Info:
Issue Reported: {row['Issue_reported at']}
Response Time: {row['issue_responded']}
"""

    elif "delivery" in user_input.lower():
        response = f"""
🚚 Delivery Details:
City: {row['Customer_City']}
Product: {row['Product_category']}
Price: ₹{row['Item_price']}
"""

    elif "payment" in user_input.lower():
        response = f"""
💳 Payment Info:
Amount: ₹{row['Item_price']}
Channel: {row['channel_name']}
"""

    else:
        response = f"""
📊 General Info:
Agent: {row['Agent_name']}
Manager: {row['Manager']}
CSAT Score: {row['CSAT Score']}
"""

    return output_guardrail(response)

# ================= UI =================

st.set_page_config(page_title="AI Customer Support Agent", page_icon="🤖")

st.title("🤖 AI Customer Support Agent")
st.write("Fast AI support system powered by indexed search ⚡")

# Order ID input
order_id_input = st.text_input("Enter Order ID (required):")

if order_id_input:
    st.session_state.order_id = order_id_input

# Query input
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        response = agent_response(user_input)
        st.success(response)
import streamlit as st

# ================= GUARDRAILS =================

def input_guardrail(user_input):
    blocked_patterns = [
        "hack", "bypass", "ignore instructions",
        "pretend you are", "act as"
    ]
    return not any(p in user_input.lower() for p in blocked_patterns)


def domain_check(query):
    allowed = ["order", "refund", "delivery", "payment"]
    return any(word in query.lower() for word in allowed)


def output_guardrail(response):
    if "maybe" in response.lower():
        return "⚠️ Not sure. Connecting to human agent."
    return response


def refusal_response():
    return "🚫 I cannot assist with that request. Please contact support."


# ================= TOOLS =================

faq_db = {
    "refund": "Refund will be processed within 5-7 business days.",
    "delivery": "Delivery takes 3-5 days.",
    "payment": "We accept UPI, cards, and net banking.",
    "order status": "Please provide your order ID."
}


def get_faq_answer(user_input):
    for key in faq_db:
        if key in user_input.lower():
            return faq_db[key]
    return None


def check_order(order_id):
    status = ["Processing", "Shipped", "Out for delivery", "Delivered"]
    return f"Order {order_id} status: {status[int(order_id) % 4]}"


# ================= MEMORY =================

if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# ================= AGENT =================

def agent_response(user_input):

    # Input Guardrail
    if not input_guardrail(user_input):
        return refusal_response()

    # Memory
    if "same issue" in user_input.lower():
        user_input = st.session_state.last_query

    st.session_state.last_query = user_input

    # Domain Guardrail
    if not domain_check(user_input):
        return "⚠️ I only handle customer support queries."

    # Reasoning
    if "refund" in user_input.lower():
        intent = "refund_query"
    elif "order" in user_input.lower():
        intent = "order_query"
    elif "delivery" in user_input.lower():
        intent = "delivery_query"
    else:
        intent = "unknown"

    # Tool: FAQ
    faq_answer = get_faq_answer(user_input)
    if faq_answer:
        return output_guardrail(f"🧠 Intent: {intent}\n\n{faq_answer}")

    # Tool: Order tracking
    if "order id" in user_input.lower():
        return check_order("1234")

    return "👨‍💼 I’m not sure. Connecting to human agent..."


# ================= UI =================

st.set_page_config(page_title="AI Customer Support Agent", page_icon="🤖")

st.title("🤖 AI Customer Support Agent")
st.write("Ask me about orders, refunds, delivery, or payments.")

user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        response = agent_response(user_input)
        st.success(response)
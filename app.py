import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from openai import OpenAI
import os

# --- 1. PRIVACY & SECURITY ---
# Hardcoded password for your private AI (Change this!)
USER_PASSWORD = "my_secret_nepse_password"

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == USER_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Password for Private Access", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password for Private Access", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()  # Stop the app if password is wrong

# --- 2. MAIN APP CONFIGURATION ---
st.set_page_config(page_title="My Private NEPSE AI", page_icon="📈", layout="wide")
st.title("📈 Private NEPSE AI Advisor & Predictor")

# Set your OpenAI API Key securely in your environment variables
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-placeholder-key"))

# --- 3. DATA FETCHING (Mock for NEPSE) ---
@st.cache_data
def load_nepse_data(symbol):
    """
    Since NEPSE doesn't have a free official API, you will eventually 
    need to write a scraper or use a third-party Nepali API here.
    For now, we generate dummy historical data for the architecture.
    """
    dates = pd.date_range(start="2023-01-01", end=pd.Timestamp.today(), freq="B")
    # Random walk to simulate stock prices
    prices = np.round(np.cumsum(np.random.randn(len(dates)) * 10) + 500, 2)
    df = pd.DataFrame({"Date": dates, "Close": prices})
    return df

# --- 4. PREDICTION MODEL (Basic Moving Average/ML Placeholder) ---
def predict_future(df, days=5):
    """Simple trend prediction based on moving averages."""
    last_price = df['Close'].iloc[-1]
    trend = df['Close'].diff().mean()
    future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=days, freq="B")
    future_prices = [last_price + (trend * i) + (np.random.randn() * 5) for i in range(1, days+1)]
    return pd.DataFrame({"Date": future_dates, "Predicted_Close": future_prices})

# --- 5. UI TABS ---
tab1, tab2 = st.tabs(["📊 Market Analysis & Prediction", "🤖 Personal AI Tutor"])

with tab1:
    st.header("Stock Analysis")
    symbol = st.selectbox("Select Share Symbol (Mock Data)", ["NABIL", "NICA", "NTC", "CIT", "SHIVM"])
    
    df = load_nepse_data(symbol)
    
    # Plot historical data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Historical Price'))
    
    # Prediction
    st.subheader(f"Prediction for next 5 days for {symbol}")
    pred_df = predict_future(df, 5)
    fig.add_trace(go.Scatter(x=pred_df['Date'], y=pred_df['Predicted_Close'], mode='lines+markers', name='Prediction', line=dict(dash='dash', color='red')))
    
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(pred_df)

with tab2:
    st.header("Your Personal NEPSE Advisor")
    st.markdown("Ask me anything about trading strategies, portfolio management, or technical analysis.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a private financial advisor and tutor specializing in the Nepal Stock Exchange (NEPSE). You give highly accurate, cautious, and educational advice."}
        ]

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask your AI advisor... (e.g., 'Teach me about RSI indicators')"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            # Generate AI response
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=st.session_state.messages
            )
            msg = response.choices[0].message.content
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(msg)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error("Error communicating with AI. Please make sure your OpenAI API key is set.")

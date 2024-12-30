import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Générer des données fictives
np.random.seed(42)
dates = [datetime.now() - timedelta(minutes=i) for i in range(500)]
prices = np.cumsum(np.random.randn(500)) + 10

# Convertir en DataFrame
data = pd.DataFrame({'Date': dates[::-1], 'Close': prices[::-1]})
data.set_index('Date', inplace=True)

# Paramètres interactifs
st.sidebar.title("Scalping Tool Parameters")
ema_short = st.sidebar.slider("EMA Short Period", 5, 50, 9)
ema_long = st.sidebar.slider("EMA Long Period", 10, 100, 21)
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 7)
rsi_overbought = st.sidebar.slider("RSI Overbought Level", 50, 100, 80)
rsi_oversold = st.sidebar.slider("RSI Oversold Level", 0, 50, 20)

# Calcul des EMA
data['EMA_Short'] = data['Close'].ewm(span=ema_short).mean()
data['EMA_Long'] = data['Close'].ewm(span=ema_long).mean()

# Calcul du RSI
delta = data['Close'].diff(1)
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=rsi_period).mean()
avg_loss = loss.rolling(window=rsi_period).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Signaux
data['Buy_Signal'] = (data['EMA_Short'] > data['EMA_Long']) & (data['RSI'] < rsi_oversold)
data['Sell_Signal'] = (data['EMA_Short'] < data['EMA_Long']) & (data['RSI'] > rsi_overbought)

# Graphique interactif
st.title("Scalping Tool: EMA & RSI")
fig, ax = plt.subplots(figsize=(14, 7))

# Tracer les prix et EMA
ax.plot(data.index, data['Close'], label='Close Price', alpha=0.75)
ax.plot(data.index, data['EMA_Short'], label=f'EMA {ema_short}', alpha=0.75)
ax.plot(data.index, data['EMA_Long'], label=f'EMA {ema_long}', alpha=0.75)

# Ajouter les signaux
ax.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], label='Buy Signal', marker='^', color='green', alpha=1)
ax.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], label='Sell Signal', marker='v', color='red', alpha=1)

# Légendes et titres
ax.set_title("Scalping Tool Visualization")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid()

st.pyplot(fig)

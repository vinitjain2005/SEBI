import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta


@st.cache_data(show_spinner=False, ttl=3600)
def _fetch_history(ticker: str, days: int = 60) -> pd.DataFrame:
	try:
		data = yf.download(ticker, period=f"{days}d", interval="1d", progress=False, auto_adjust=True)
		data = data.reset_index()
		if data is None or data.empty:
			raise ValueError('No data')
		return data
	except Exception:
		# Fallback: synthetic random-walk data for demo stability
		dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='D')
		prices = np.cumprod(1 + np.random.normal(0, 0.01, size=days)) * 100
		return pd.DataFrame({'Date': dates, 'Close': prices})


def _plot_price(df: pd.DataFrame, title: str):
	if df.empty:
		st.warning('No data available')
		return
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
	fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Price')
	st.plotly_chart(fig, use_container_width=True)


def _update_position(portfolio: dict, symbol: str, qty: int, price: float) -> None:
	positions = portfolio['positions']
	cash = portfolio['cash']
	cost = qty * price
	if qty > 0 and cash < cost:
		st.error('Not enough cash')
		return
	positions.setdefault(symbol, {'qty': 0, 'avg': 0.0})
	pos = positions[symbol]
	new_qty = pos['qty'] + qty
	if new_qty < 0:
		st.error('Cannot sell more than held')
		return
	if qty > 0:
		pos['avg'] = (pos['avg'] * pos['qty'] + cost) / max(new_qty, 1)
		portfolio['cash'] -= cost
	elif qty < 0:
		portfolio['cash'] -= cost  # qty negative, increases cash
	pos['qty'] = new_qty
	if pos['qty'] == 0:
		positions.pop(symbol, None)
	portfolio['history'].append({'ts': datetime.utcnow().isoformat(), 'symbol': symbol, 'qty': qty, 'price': price})


def _portfolio_value(portfolio: dict, prices: dict) -> float:
	value = portfolio['cash']
	for sym, pos in portfolio['positions'].items():
		price = prices.get(sym, pos['avg'])
		value += pos['qty'] * price
	return float(value)


def render_simulator() -> None:
	st.title('Virtual Trading (Delayed/Synthetic Data)')
	portfolio = st.session_state['portfolio']

	symbols = st.text_input('Symbols (comma-separated)', 'INFY.NS, ITC.NS, SBIN.NS')
	symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]

	prices = {}
	cols = st.columns(2)
	for i, sym in enumerate(symbol_list[:6]):
		with cols[i % 2]:
			df = _fetch_history(sym, 120)
			if not df.empty:
				last_price = float(df['Close'].iloc[-1])
				prices[sym] = last_price
				label = f"{sym} last: {last_price:.2f} {'(synthetic)' if 'yfinance' not in str(df.columns) else ''}"
				st.caption(label)
				_plot_price(df.tail(60), f"{sym} - Last 60 days")
				qty = st.number_input(f"Qty for {sym}", min_value=1, max_value=10000, value=10, step=1, key=f"qty_{sym}")
				c1, c2 = st.columns(2)
				with c1:
					if st.button(f"Buy {sym}", key=f"buy_{sym}"):
						_update_position(portfolio, sym, qty, last_price)
				with c2:
					if st.button(f"Sell {sym}", key=f"sell_{sym}"):
						_update_position(portfolio, sym, -qty, last_price)
			else:
				st.warning(f"No data for {sym}")

	st.subheader('Portfolio')
	if portfolio['positions']:
		rows = []
		for sym, pos in portfolio['positions'].items():
			mkt = prices.get(sym, pos['avg'])
			unreal = (mkt - pos['avg']) * pos['qty']
			rows.append({'Symbol': sym, 'Qty': pos['qty'], 'Avg Price': round(pos['avg'], 2), 'Market': round(mkt, 2), 'Unrealized PnL': round(unreal, 2)})
		st.dataframe(rows, use_container_width=True)
	else:
		st.write('No positions yet.')

	# Export history
	hist = pd.DataFrame(portfolio['history'])
	if not hist.empty:
		csv = hist.to_csv(index=False).encode('utf-8')
		st.download_button('Download Trade History (CSV)', data=csv, file_name='trade_history.csv', mime='text/csv')

	total_value = _portfolio_value(portfolio, prices)
	st.metric('Cash', f"₹{portfolio['cash']:.2f}")
	st.metric('Total Value', f"₹{total_value:.2f}")

import streamlit as st

LESSONS = [
	{
		'key': 'basics',
		'title': 'Stock Market Basics',
		'content': 'Learn what stocks, exchanges, and indices are. Understand primary vs secondary markets.'
	},
	{
		'key': 'risk',
		'title': 'Risk Assessment',
		'content': 'Learn risk-return tradeoff, volatility, drawdowns, diversification, asset allocation.'
	},
	{
		'key': 'algo',
		'title': 'Algo Trading & HFT',
		'content': 'Understand basic algos, backtesting, latency, market microstructure, and risks.'
	},
	{
		'key': 'portfolio',
		'title': 'Portfolio Diversification',
		'content': 'Build diversified portfolios across sectors/assets and rebalance periodically.'
	},
	{
		'key': 'orders',
		'title': 'Order Types',
		'content': 'Market vs Limit vs Stop orders; IOC/Day; impact on execution and slippage.'
	},
	{
		'key': 'costs',
		'title': 'Costs & Taxes',
		'content': 'Brokerage, STT, stamp duty, GST; turnover; short vs long-term capital gains basics.'
	},
	{
		'key': 'psych',
		'title': 'Investor Psychology',
		'content': 'Common biases: herd behavior, loss aversion, overconfidence; set rules to mitigate.'
	},
]


def render_tutorials() -> None:
	st.title('Tutorials')

	completed = st.session_state.get('progress', {})

	for lesson in LESSONS:
		completed_flag = bool(completed.get(lesson['key']))
		with st.expander(f"{lesson['title']} {'✅' if completed_flag else ''}", expanded=False):
			st.write(lesson['content'])
			st.markdown('**Key takeaways:**')
			st.markdown('- Keep costs low, diversify, and be long-term oriented.')
			st.markdown('- Use limit orders when liquidity is thin; avoid illiquid names.')
			st.markdown('- Backtest responsibly; past performance is not indicative of future results.')
			if st.button('Mark complete', key=f"done_{lesson['key']}"):
				st.session_state['progress'][lesson['key']] = True
				st.success('Marked as complete!')

	st.sidebar.metric('Lessons completed', sum(1 for l in LESSONS if completed.get(l['key'])), len(LESSONS))

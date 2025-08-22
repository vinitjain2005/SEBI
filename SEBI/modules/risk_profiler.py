import streamlit as st

QUESTIONS = [
	('Time horizon for investments?', ['<1 year', '1-3 years', '3-5 years', '5+ years'], [0,1,2,3]),
	('How do you react to 10% drop?', ['Sell all', 'Sell some', 'Hold', 'Buy more'], [0,1,2,3]),
	('Primary goal?', ['Capital preservation', 'Income', 'Growth', 'Aggressive growth'], [0,1,2,3]),
	('Experience level?', ['New', 'Some', 'Experienced', 'Expert'], [0,1,2,3]),
]


def _classify(score: int) -> str:
	if score <= 3:
		return 'Conservative'
	elif score <= 7:
		return 'Balanced'
	else:
		return 'Aggressive'


def render_risk_profiler():
	st.title('Risk Profiler')
	score = 0
	for i, (q, options, weights) in enumerate(QUESTIONS):
		ans = st.radio(q, options, index=None, key=f"risk_{i}")
		if ans is not None:
			score += weights[options.index(ans)]

	if st.button('Calculate Profile'):
		profile = _classify(score)
		st.session_state['risk_profile'] = profile
		st.success(f'Your profile: {profile}')
		if profile == 'Conservative':
			st.write('Start with Basics, Risk Assessment, and Costs & Taxes.')
		elif profile == 'Balanced':
			st.write('Add Portfolio Diversification and Order Types.')
		else:
			st.write('Explore Algo/HFT concepts carefully and Investor Psychology.')

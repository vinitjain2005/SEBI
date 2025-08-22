import streamlit as st
from modules.utils import append_leaderboard_entry

QUESTIONS = [
	{
		'q': 'Which of these best describes diversification?',
		'options': ['Putting all money in one stock', 'Spreading investments across assets', 'Timing the market', 'Day trading daily'],
		'answer': 1,
		'expl': 'Diversification reduces unsystematic risk by spreading exposure.'
	},
	{
		'q': 'Higher expected return usually comes with…',
		'options': ['Lower risk', 'No risk', 'Higher risk', 'Guaranteed profit'],
		'answer': 2,
		'expl': 'Risk-return tradeoff: higher return potential requires higher risk.'
	},
	{
		'q': 'HFT strategies are most sensitive to…',
		'options': ['Long-term fundamentals', 'Transaction latency', 'P/E ratio', 'Dividend yield'],
		'answer': 1,
		'expl': 'HFT depends on low latency infrastructure and microstructure.'
	},
	{
		'q': 'A limit order will…',
		'options': ['Execute at any price immediately', 'Execute at your specified price or better', 'Never execute', 'Always execute worse than market'],
		'answer': 1,
		'expl': 'Limit orders control execution price but may miss fills.'
	},
	{
		'q': 'What helps reduce impact of behavioral biases?',
		'options': ['Impulse trading', 'No plan', 'Rules-based approach', 'Chasing hot tips'],
		'answer': 2,
		'expl': 'Rules and checklists reduce impulsive decisions.'
	},
]


def render_quizzes() -> None:
	st.title('Quizzes')
	selected = {}
	for idx, q in enumerate(QUESTIONS):
		st.subheader(f"Q{idx+1}. {q['q']}")
		selected[idx] = st.radio('Choose one', q['options'], index=None, key=f"q_{idx}")

	name = st.text_input('Your name for leaderboard (optional)')

	if st.button('Submit Quiz'):
		score = 0
		for idx, q in enumerate(QUESTIONS):
			choice = selected[idx]
			if choice is None:
				st.warning(f"Question {idx+1} not answered")
				continue
			if q['options'].index(choice) == q['answer']:
				score += 1
				st.success(f"Q{idx+1}: Correct! {q['expl']}")
			else:
				correct = q['options'][q['answer']]
				st.error(f"Q{idx+1}: Incorrect. Correct: {correct}. {q['expl']}")

		st.subheader(f"Score: {score} / {len(QUESTIONS)}")
		best = st.session_state.get('best_quiz_score', 0)
		if score > best:
			st.session_state['best_quiz_score'] = score
			st.balloons()
			st.info('New best score!')
		else:
			st.info(f"Best score so far: {best} / {len(QUESTIONS)}")

		if name.strip():
			append_leaderboard_entry(name, score)
			st.success('Added to leaderboard!')

		# Show leaderboard
		lb = st.session_state.get('leaderboard', [])
		if lb:
			st.subheader('Leaderboard (Top)')
			for i, row in enumerate(lb[:10], start=1):
				st.write(f"{i}. {row['name']} — {row['score']}")

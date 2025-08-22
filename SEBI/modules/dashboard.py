import streamlit as st
from typing import List


BADGE_RULES = [
	('Learner', lambda progress, score: len([k for k,v in progress.items() if v]) >= 1),
	('Quiz Novice', lambda progress, score: score >= 2),
	('Quiz Pro', lambda progress, score: score >= 4),
	('Diversifier', lambda progress, score: progress.get('portfolio')),
]


def _compute_strengths_weaknesses(score: int, total: int) -> str:
	if total == 0:
		return 'No quiz attempts yet.'
	ratio = score / total
	if ratio >= 0.8:
		return 'Strong grasp. Consider advanced topics: options basics, ETFs.'
	elif ratio >= 0.5:
		return 'Decent understanding. Review risk, orders, psychology.'
	else:
		return 'Start with basics and risk assessment lessons first.'


def render_dashboard():
	st.title('Dashboard')
	progress = st.session_state.get('progress', {})
	score = st.session_state.get('best_quiz_score', 0)
	total = 5

	st.metric('Lessons Completed', sum(1 for v in progress.values() if v))
	st.metric('Best Quiz Score', score)
	st.write(_compute_strengths_weaknesses(score, total))

	st.subheader('Badges')
	badges: List[str] = [name for name, rule in BADGE_RULES if rule(progress, score)]
	if badges:
		st.write(', '.join(badges))
	else:
		st.write('No badges yet. Complete lessons and quizzes to earn some!')

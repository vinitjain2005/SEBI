import streamlit as st
import requests
from pathlib import Path
import json
from typing import List, Dict, Any


def ensure_session_state() -> None:
	if 'progress' not in st.session_state:
		st.session_state['progress'] = {}
	if 'portfolio' not in st.session_state:
		st.session_state['portfolio'] = {
			'cash': 100000.0,
			'positions': {},
			'history': [],
		}
	if 'best_quiz_score' not in st.session_state:
		st.session_state['best_quiz_score'] = 0
	if 'risk_profile' not in st.session_state:
		st.session_state['risk_profile'] = 'Unprofiled'
	if 'leaderboard' not in st.session_state:
		st.session_state['leaderboard'] = []


# ---------- Persistence ----------
_STATE_DIR = Path.home() / ".sebi_app"
_STATE_DIR.mkdir(parents=True, exist_ok=True)
_STATE_FILE = _STATE_DIR / "state.json"
_LEADERBOARD_FILE = _STATE_DIR / "leaderboard.json"


def load_state() -> None:
	try:
		if _STATE_FILE.exists():
			data = json.loads(_STATE_FILE.read_text(encoding='utf-8'))
			st.session_state['progress'] = data.get('progress', {})
			st.session_state['portfolio'] = data.get('portfolio', st.session_state['portfolio'])
			st.session_state['best_quiz_score'] = data.get('best_quiz_score', 0)
			st.session_state['risk_profile'] = data.get('risk_profile', 'Unprofiled')
		if _LEADERBOARD_FILE.exists():
			st.session_state['leaderboard'] = json.loads(_LEADERBOARD_FILE.read_text(encoding='utf-8'))
	except Exception:
		pass


def save_state() -> None:
	try:
		payload = {
			'progress': st.session_state.get('progress', {}),
			'portfolio': st.session_state.get('portfolio', {}),
			'best_quiz_score': st.session_state.get('best_quiz_score', 0),
			'risk_profile': st.session_state.get('risk_profile', 'Unprofiled'),
		}
		_STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
		_LEADERBOARD_FILE.write_text(json.dumps(st.session_state.get('leaderboard', []), ensure_ascii=False, indent=2), encoding='utf-8')
	except Exception:
		pass


def append_leaderboard_entry(name: str, score: int) -> None:
	try:
		entry = {'name': name.strip() or 'Anonymous', 'score': int(score)}
		lb: List[Dict[str, Any]] = st.session_state.get('leaderboard', [])
		lb.append(entry)
		lb.sort(key=lambda x: x['score'], reverse=True)
		st.session_state['leaderboard'] = lb[:25]
		_LEADERBOARD_FILE.write_text(json.dumps(st.session_state['leaderboard'], ensure_ascii=False, indent=2), encoding='utf-8')
	except Exception:
		pass


def render_learn_hub() -> None:
	st.title('Learn Hub: Resources & Links')
	st.write('Access curated educational resources from SEBI, NISM, and exchanges.')
	
	st.subheader('Quick Links')
	st.markdown('- [SEBI Investor Education](https://investor.sebi.gov.in)')
	st.markdown('- [NISM Certifications](https://www.nism.ac.in)')
	st.markdown('- [NSE Investor](https://www.nseindia.com/invest)')
	st.markdown('- [BSE Investor](https://www.bseindia.com/investors)')
	
	st.subheader('Educational Content')
	st.markdown('**Stock Market Basics:**')
	st.markdown('- What are stocks and how they work')
	st.markdown('- Primary vs Secondary markets')
	st.markdown('- Understanding market indices')
	
	st.markdown('**Risk Management:**')
	st.markdown('- Risk-return tradeoff')
	st.markdown('- Diversification strategies')
	st.markdown('- Asset allocation principles')
	
	st.markdown('**Trading Fundamentals:**')
	st.markdown('- Order types (Market, Limit, Stop)')
	st.markdown('- Trading costs and taxes')
	st.markdown('- Behavioral biases to avoid')

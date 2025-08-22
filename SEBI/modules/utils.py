import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
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


@st.cache_data(show_spinner=False, ttl=600)
def _fetch_text_from_url(url: str) -> str:
	try:
		resp = requests.get(url, timeout=15)
		resp.raise_for_status()
		soup = BeautifulSoup(resp.text, 'html.parser')
		for tag in soup(['script', 'style', 'noscript']):
			tag.decompose()
		text = ' '.join(soup.get_text(separator=' ').split())
		return text[:100000]
	except Exception as e:
		return f'ERROR: {e}'


@st.cache_data(show_spinner=False, ttl=3600)
def _summarize_text(text: str, sentences: int = 5) -> str:
	try:
		parser = PlaintextParser.from_string(text, Tokenizer('english'))
		summarizer = LsaSummarizer()
		summary_sentences = summarizer(parser.document, sentences)
		return ' '.join(str(s) for s in summary_sentences) or text[:1500]
	except Exception:
		return text[:1500]


@st.cache_data(show_spinner=False, ttl=3600)
def _translate_text(text: str, target_lang: str) -> str:
	try:
		return GoogleTranslator(source='auto', target=target_lang).translate(text)
	except Exception as e:
		return f'Translation error: {e}'


def render_learn_hub() -> None:
	st.title('Learn Hub: Translate & Summarize')
	st.write('Provide a URL (SEBI/NISM/Exchanges) or paste text. Choose language to translate.')

	col1, col2 = st.columns(2)
	with col1:
		url = st.text_input('Source URL (optional)')
		raw_text = st.text_area('Or paste text', height=160)
	with col2:
		lang = st.selectbox('Target language', ['hi', 'bn', 'ta'], index=0)
		do_summarize = st.checkbox('Summarize before translating', value=True)
		num_sentences = st.slider('Summary sentences', 3, 10, 5)

	st.markdown('**Quick demo (SEBI circular):**')
	c1, c2, c3 = st.columns(3)
	with c1:
		if st.button('Demo in Hindi'):
			_demo_process('https://www.sebi.gov.in/legal/circulars', 'hi', do_summarize, num_sentences)
	with c2:
		if st.button('Demo in Tamil'):
			_demo_process('https://www.sebi.gov.in/legal/circulars', 'ta', do_summarize, num_sentences)
	with c3:
		if st.button('Demo in Bengali'):
			_demo_process('https://www.sebi.gov.in/legal/circulars', 'bn', do_summarize, num_sentences)

	if st.button('Process'):
		source_text = ''
		if url:
			source_text = _fetch_text_from_url(url)
			if source_text.startswith('ERROR:'):
				st.error(source_text)
				return
		elif raw_text.strip():
			source_text = raw_text.strip()
		else:
			st.warning('Enter a URL or paste some text.')
			return

		to_translate = _summarize_text(source_text, sentences=num_sentences) if do_summarize else source_text[:5000]
		translated = _translate_text(to_translate, lang)

		st.subheader('Original (truncated)')
		st.write(to_translate[:1500] + ('…' if len(to_translate) > 1500 else ''))

		st.subheader('Translated')
		st.write(translated)


def _demo_process(url: str, lang: str, do_summarize: bool, num_sentences: int) -> None:
	text = _fetch_text_from_url(url)
	if text.startswith('ERROR:'):
		st.error(text)
		return
	to_translate = _summarize_text(text, sentences=num_sentences) if do_summarize else text[:5000]
	translated = _translate_text(to_translate, lang)
	st.subheader('Translated Demo')
	st.write(translated)

import streamlit as st
from modules.tutorials import render_tutorials
from modules.quizzes import render_quizzes
from modules.simulator import render_simulator
from modules.utils import ensure_session_state, render_learn_hub, load_state, save_state
from modules.dashboard import render_dashboard
from modules.risk_profiler import render_risk_profiler


st.set_page_config(page_title="Investor Education Prototype", page_icon="📈", layout="wide")

ensure_session_state()
load_state()

st.sidebar.title("Investor Education")
st.sidebar.info("Educational prototype inspired by SEBI's investor education initiative. Data is delayed and for learning only.")
page = st.sidebar.radio(
	"Navigate",
	[
		"Dashboard",
		"Tutorials",
		"Quizzes",
		"Virtual Trading",
		"Learn Hub (Translate & Summarize)",
		"Risk Profiler",
		"Resources",
	],
)

if page == "Dashboard":
	render_dashboard()
elif page == "Tutorials":
	render_tutorials()
elif page == "Quizzes":
	render_quizzes()
elif page == "Virtual Trading":
	render_simulator()
elif page == "Learn Hub (Translate & Summarize)":
	render_learn_hub()
elif page == "Risk Profiler":
	render_risk_profiler()
else:
	st.title('Resources')
	st.markdown('- [SEBI - Investor Education](https://investor.sebi.gov.in)')
	st.markdown('- [NISM Certifications](https://www.nism.ac.in)')
	st.markdown('- [NSE Investor](https://www.nseindia.com/invest)')
	st.markdown('- [BSE Investor](https://www.bseindia.com/investors)')

# Certificate download when quiz score high
best = st.session_state.get('best_quiz_score', 0)
if best >= 4:
	st.sidebar.download_button(
		label="Download Certificate",
		data=f"Certificate of Completion\n\nThis certifies that the user completed the quiz with score {best}.",
		file_name="certificate.txt",
		mime="text/plain",
	)

if st.sidebar.button("Save Progress"):
	save_state()
	st.sidebar.success("Saved!")

st.caption("© 2025 Investor Education Prototype • For education only")

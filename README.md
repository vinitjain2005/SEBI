---

# 📈 SEBI Investor Education & Awareness App

An interactive prototype app designed to **educate retail investors** about the stock market, risk management, and investment best practices. The app provides tutorials, quizzes, simulated trading, and resources in **vernacular languages**, making financial literacy accessible to everyone.

---

## 🌟 Problem Statement

Many retail investors in India lack the knowledge to navigate the securities market, leading to poor investment decisions or reliance on unverified advice. Most online resources are available only in English, creating a **language barrier** for a majority of investors.

---

## 🎯 Solution

The app provides:

* 📘 **Engaging tutorials** on stock market basics, risk assessment, algo trading, and diversification.
* 🧩 **Interactive quizzes** to test and reinforce knowledge.
* 📊 **Virtual trading simulator** with delayed market data to practice trading safely.
* 🌐 **Vernacular translation & summarization** of trusted resources (SEBI, NISM, Stock Exchanges).
* 📈 **Progress tracking** to personalize learning.

---

## ⚙️ Tech Stack

* **Frontend**: React.js (with interactive UI components)
* **Backend**: FastAPI (Python) + Uvicorn
* **Database**: SQLite / PostgreSQL (for user progress & quiz scores)
* **APIs**: Market data (delayed), Translation API for vernacular support

---

## 🚀 Features

* Tutorials → Structured lessons on stock markets
* Quizzes → Self-assessment with instant feedback
* Virtual Trading → Learn by doing in a risk-free environment
* Learn Hub → Translate and summarize SEBI/NISM resources
* Resources → Curated links to trusted financial education sites

---

## 📂 Project Structure

```
SEBI/
│── frontend/       # React app (UI/UX)
│── backend/        # FastAPI backend (APIs, DB, trading logic)
│── .venv/          # Virtual environment
│── requirements.txt # Python dependencies
│── package.json    # Frontend dependencies
│── README.md       # Project documentation
```

---

## 🛠️ Setup & Installation

### Clone the repository

```bash
git clone https://github.com/vinitjain2005/SEBI.git
cd SEBI
```

### Run Command 

```bash
cd C:\Users\jainv\OneDrive\Desktop\SEBI\SEBI
python -m streamlit run app.py
```

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

The app will run at:
https://qpn0jxrk-8502.inc1.devtunnels.ms/
---

## 📌 Context

This project is **inspired by SEBI’s push for financial literacy and investor awareness**. It aims to bridge the gap between **complex market knowledge** and **common retail investors** through technology, gamification, and vernacular language support.

---


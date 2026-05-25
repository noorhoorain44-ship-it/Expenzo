# 💰 Noor Expense Tracker — Streamlit Edition

A modern web-based expense tracker built with Streamlit, featuring a futuristic dark UI and all the powerful features from the original CLI version.

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run expensetracker.py
```

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Multi-User Auth** | Register/login with SHA-256 hashed passwords |
| 👤 **Guest Mode** | Try without creating an account |
| 🏠 **Live Dashboard** | Today / weekly / monthly spending + budget progress |
| ➕ **Add Expenses** | 20 categories, tags, payment methods, notes |
| ✏️ **Edit / Delete** | Modify or remove any expense by ID |
| 🔍 **Smart Search** | Search by keyword, tag, category |
| 🔎 **Advanced Filters** | Filter by date range, month, year, category, payment, tag |
| 💼 **Budget Manager** | Set monthly budgets per category with live progress bars |
| 🚨 **Budget Alerts** | Visual warnings at 80% and 100% of budget |
| 📊 **Analytics** | Monthly summary, category breakdown (pie chart), trends, YTD report |
| 🔁 **Recurring Expenses** | Daily / weekly / monthly auto-applied expenses |
| 🎯 **Savings Goals** | Create goals, track progress, celebrate completion |
| 📤 **CSV Export** | Export all expenses to CSV |
| 📦 **JSON Export/Import** | Full backup and restore support |
| 📥 **CSV Import** | Import from any CSV file |
| 💱 **Multi-Currency** | USD, EUR, GBP, INR, PKR, JPY, AUD, CAD |
| 🎨 **Beautiful UI** | Futuristic dark theme with cyan accents |
| 🌐 **Cross-Platform** | Runs in any browser |

## 📁 Project Structure

```
noor-expense-tracker-streamlit/
├── expensetracker.py    # 🐍 Main Streamlit application
├── requirements.txt     # 📦 Python dependencies
└── README.md            # 📖 This file
```

## 🛠️ Data Storage

All data is stored locally in `~/.noorexpense_streamlit/`:

| File | Description |
|---|---|
| `users.json` | User accounts & passwords |
| `expenses.json` | All expense records |
| `budgets.json` | Monthly budget limits |
| `recurring.json` | Recurring expense rules |
| `goals.json` | Savings goals |
| `settings.json` | App preferences |

## 💱 Supported Currencies

| Code | Symbol | Currency |
|---|---|---|
| USD | $ | US Dollar |
| EUR | € | Euro |
| GBP | £ | British Pound |
| INR | ₹ | Indian Rupee |
| PKR | ₨ | Pakistani Rupee |
| JPY | ¥ | Japanese Yen |
| AUD | A$ | Australian Dollar |
| CAD | C$ | Canadian Dollar |

## 🔒 Security

- Passwords hashed with SHA-256
- No plaintext storage
- All data stays local — never sent to any server

## 🚀 Deployment

### Local
```bash
streamlit run expensetracker.py
```

### Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your repo

---

Built with ❤️ by Noor Hoorain

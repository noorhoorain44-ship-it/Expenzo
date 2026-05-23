# 💰 Noor Expense Tracker

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-cyan?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Author](https://img.shields.io/badge/Author-Noor%20Hoorain-magenta?style=for-the-badge)

**An advanced, futuristic CLI expense tracker built in pure Python.**  
*Feature-rich · Cross-platform · Multi-user · Beautiful terminal UI*

</div>

---

```
  ███╗   ██╗ ██████╗  ██████╗ ██████╗
  ████╗  ██║██╔═══██╗██╔═══██╗██╔══██╗
  ██╔██╗ ██║██║   ██║██║   ██║██████╔╝
  ██║╚██╗██║██║   ██║██║   ██║██╔══██╗
  ██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║
  ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
         💰 EXPENSE TRACKER v2.0.0
          Developed by Noor Hoorain
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Multi-User Auth** | Register/login with SHA-256 hashed passwords |
| 🏠 **Live Dashboard** | Today / weekly / monthly spending + budget progress bars |
| ➕ **Add Expenses** | 19 categories, tags, payment methods, notes |
| ✏️ **Edit / Delete** | Modify or remove any expense by ID |
| 🔍 **Smart Search** | Search by keyword, tag, category |
| 🔎 **Advanced Filters** | Filter by date range, month, year, category, payment, tag |
| 💼 **Budget Manager** | Set monthly budgets per category with live %-used bars |
| 🚨 **Budget Alerts** | Auto-warns at 80% and 100% of budget |
| 📊 **Analytics** | Monthly summary, category breakdown, trends, YTD report |
| 📉 **Spending Trends** | 6-month visual bar chart in terminal |
| 🔁 **Recurring Expenses** | Daily / weekly / monthly auto-applied expenses |
| 🎯 **Savings Goals** | Create goals, track progress, celebrate completion |
| 📤 **CSV Export** | Export all expenses to CSV for Excel/Sheets |
| 📦 **JSON Export/Import** | Full backup and restore support |
| 📥 **CSV Import** | Import from any CSV file |
| 📜 **Audit Logging** | Every action is logged with timestamp |
| 💱 **Multi-Currency** | USD, EUR, GBP, INR, PKR, JPY, AUD, CAD |
| 🎨 **Beautiful UI** | Rich colours via `colorama` + `rich` (graceful fallback) |
| 🌐 **Cross-Platform** | Windows 10/11, Kali Linux, Ubuntu, Debian, macOS |
| 👤 **Guest Mode** | Try without creating an account |

---

## 📁 Project Structure

```
noor-expense-tracker/
├── expensetracker.py   # 🐍 Main application (all features in one file)
├── install.sh          # 🐧 Linux / macOS / Kali installer
├── install.bat         # 🪟 Windows installer
├── requirements.txt    # 📦 Python dependencies
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 This file
```

---

## 🚀 Installation

### 🐧 Linux / Kali Linux / macOS

**Quick install:**
```bash
git clone https://github.com/noorhoorain44-ship-it/noor-expense-tracker.git
cd noor-expense-tracker
chmod +x install.sh
./install.sh
```

**Then launch:**
```bash
expense
```

**Manual install:**
```bash
pip3 install colorama rich
python3 expensetracker.py
```

---

### 🪟 Windows 10 / 11

**Option A — Installer (Recommended):**
1. Download or clone this repository
2. Double-click `install.bat`
3. Follow the on-screen steps
4. Use the **Desktop shortcut** or type `expense` in CMD/PowerShell

**Option B — Manual:**
```powershell
pip install colorama rich
python expensetracker.py
```

---

### ✅ Requirements

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| colorama | ≥ 0.4 (optional, for colour) |
| rich | ≥ 13 (optional, enhanced UI) |

> 💡 The app works perfectly **without** `colorama` or `rich` — they are optional enhancements.

---

## 📸 Screenshots

### Dashboard
```
╔══════════════════════════════════════════════════════════════════╗
║          💰 NOOR EXPENSE TRACKER v2.0.0                         ║
║                   🏠 Dashboard                                   ║
╚══════════════════════════════════════════════════════════════════╝

  👤 User: noor  |  💱 USD  |  Saturday, 01 Jan 2025

  ──────────────────────────────────────────────────────────────────
  📆 Today        :   $12.50
  📅 This Week    :   $87.30
  🗓️  This Month   :  $342.10  [███████░░░ 68% of budget]
  💼 All Time     : $4,821.00
  🎯 Active Goals : 3
```

### Budget Tracker
```
  🍔 Food & Dining          ████████░░  82%   $410.00/$500.00
  🚗 Transport              ███░░░░░░░  34%   $102.00/$300.00
  🏠 Housing & Rent         ██████████ 100%  $1200.00/$1200.00  ⚠️
```

### Monthly Analytics
```
  2025-01   $1,240.50  ████████████████████████
  2024-12   $1,080.20  ████████████████████
  2024-11     $980.00  ██████████████████
```

---

## 🧭 Menu Navigation

```
  [1]  🏠 Dashboard
  [2]  ➕ Add Expense
  [3]  📋 View / Filter Expenses
  [4]  ✏️  Edit Expense
  [5]  🗑️  Delete Expense
  [6]  🔍 Search Expenses
  [7]  💼 Budget Manager
  [8]  📊 Analytics & Reports
  [9]  🔁 Recurring Expenses
  [10] 🎯 Savings Goals
  [11] 📤 Export / Import
  [12] ⚙️  Settings
  [0]  🚪 Logout
```

---

## 🗂️ Data Storage

All data is stored locally in your home directory — no cloud, no tracking:

| File | Location |
|---|---|
| Expenses | `~/.noorexpense/expenses.json` |
| Budgets | `~/.noorexpense/budgets.json` |
| Users | `~/.noorexpense/users.json` |
| Recurring | `~/.noorexpense/recurring.json` |
| Goals | `~/.noorexpense/goals.json` |
| Audit log | `~/.noorexpense/audit.log` |
| Exports | `~/NoorExpenseExports/` |

---

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

---

## 🔒 Security

- Passwords are hashed using **SHA-256** before storage
- No plaintext passwords are ever written to disk
- All actions are recorded in the **audit log**
- Data stored locally — never sent anywhere

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 🐛 Known Issues / FAQ

**Q: The app shows plain text without colours.**  
A: Run `pip install colorama rich` to enable coloured output.

**Q: `expense` command not found on Linux.**  
A: Run `source ~/.bashrc` or restart your terminal after install.

**Q: Windows Defender blocks install.bat.**  
A: Right-click → Properties → Unblock, then run again.

**Q: How do I backup my data?**  
A: Use **Export → JSON** from the app, or copy `~/.noorexpense/` manually.

---

## 📄 License

```
MIT License — Copyright (c) 2025 Noor Hoorain

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software to use, copy, modify, merge, publish, and
distribute it, subject to the conditions in the LICENSE file.
```

---

## 👩‍💻 Author

<div align="center">

**Noor Hoorain**  
🐙 GitHub: [@noorhoorain44-ship-it](https://github.com/noorhoorain44-ship-it)

*Built with ❤️ and Python*

</div>

---

<div align="center">

⭐ **If you found this useful, please star the repo!** ⭐

</div>

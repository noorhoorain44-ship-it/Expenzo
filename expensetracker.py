#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          💰 NOOR EXPENSE TRACKER - Advanced Edition 💰          ║
║                  Developed by Noor Hoorain                       ║
║             GitHub: github.com/noorhoorain44-ship-it             ║
║                        Version 2.0.0                             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import csv
import time
import platform
import hashlib
import getpass
import calendar
import shutil
from datetime import datetime, timedelta
from collections import defaultdict

# ─── Optional rich/colorama imports ───────────────────────────────────────────
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import track
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# ─── Constants ────────────────────────────────────────────────────────────────
VERSION          = "2.0.0"
AUTHOR           = "Noor Hoorain"
GITHUB           = "github.com/noorhoorain44-ship-it"
DATA_DIR         = os.path.join(os.path.expanduser("~"), ".noorexpense")
EXPENSES_FILE    = os.path.join(DATA_DIR, "expenses.json")
BUDGETS_FILE     = os.path.join(DATA_DIR, "budgets.json")
USERS_FILE       = os.path.join(DATA_DIR, "users.json")
SETTINGS_FILE    = os.path.join(DATA_DIR, "settings.json")
RECURRING_FILE   = os.path.join(DATA_DIR, "recurring.json")
GOALS_FILE       = os.path.join(DATA_DIR, "goals.json")
LOGS_FILE        = os.path.join(DATA_DIR, "audit.log")
EXPORT_DIR       = os.path.join(os.path.expanduser("~"), "NoorExpenseExports")

CATEGORIES = [
    "🍔 Food & Dining",
    "🚗 Transport",
    "🏠 Housing & Rent",
    "💊 Health & Medical",
    "🎮 Entertainment",
    "🛍️  Shopping",
    "📚 Education",
    "💡 Utilities",
    "✈️  Travel",
    "👔 Personal Care",
    "💼 Business",
    "🎁 Gifts & Donations",
    "💰 Savings & Investments",
    "📱 Technology",
    "🐾 Pets",
    "🍕 Subscriptions",
    "🏋️  Fitness",
    "🔧 Maintenance",
    "📦 Miscellaneous",
]

CURRENCIES = {
    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹",
    "JPY": "¥", "PKR": "₨", "AUD": "A$", "CAD": "C$",
}

# ─── Colour helpers ───────────────────────────────────────────────────────────
def c(text, color=""):
    if COLORAMA_AVAILABLE:
        colors = {
            "red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW,
            "blue": Fore.BLUE, "cyan": Fore.CYAN, "magenta": Fore.MAGENTA,
            "white": Fore.WHITE, "bold": Style.BRIGHT, "reset": Style.RESET_ALL,
        }
        return f"{colors.get(color,'')}{text}{Style.RESET_ALL}"
    return text

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def pause():
    input(c("\n  ⏎  Press Enter to continue...", "cyan"))

def line(char="─", width=66):
    print(c(char * width, "blue"))

def header(title):
    clear()
    width = 66
    print(c("╔" + "═" * (width-2) + "╗", "cyan"))
    print(c("║" + f"  💰 NOOR EXPENSE TRACKER v{VERSION}  ".center(width-2) + "║", "cyan"))
    print(c("║" + f"  {title}  ".center(width-2) + "║", "yellow"))
    print(c("╚" + "═" * (width-2) + "╝", "cyan"))
    print()

def success(msg): print(c(f"\n  ✅  {msg}", "green"))
def error(msg):   print(c(f"\n  ❌  {msg}", "red"))
def warn(msg):    print(c(f"\n  ⚠️   {msg}", "yellow"))
def info(msg):    print(c(f"\n  ℹ️   {msg}", "cyan"))

# ─── Storage helpers ──────────────────────────────────────────────────────────
def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)

def load(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def audit(username, action):
    with open(LOGS_FILE, "a") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] USER={username} ACTION={action}\n")

# ─── Auth ─────────────────────────────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def login():
    header("🔐 Login / Register")
    users = load(USERS_FILE, {})
    print(c("  [1] Login\n  [2] Register\n  [3] Guest Mode\n  [0] Exit\n", "white"))
    choice = input(c("  → Choose: ", "cyan")).strip()

    match choice:
        case "1":
            uname = input(c("  Username: ", "yellow")).strip()
            pw    = getpass.getpass(c("  Password: ", "yellow"))
            if uname in users and users[uname]["password"] == hash_pw(pw):
                success(f"Welcome back, {uname}!")
                audit(uname, "LOGIN")
                time.sleep(0.8)
                return uname
            else:
                error("Invalid credentials.")
                pause()
                return login()

        case "2":
            uname = input(c("  New username: ", "yellow")).strip()
            if not uname:
                error("Username cannot be empty.")
                pause()
                return login()
            if uname in users:
                warn("Username already taken.")
                pause()
                return login()
            pw = getpass.getpass(c("  Password: ", "yellow"))
            pw2 = getpass.getpass(c("  Confirm password: ", "yellow"))
            if pw != pw2:
                error("Passwords do not match.")
                pause()
                return login()
            currency = input(c("  Preferred currency (USD/EUR/GBP/INR/PKR...): ", "yellow")).upper().strip() or "USD"
            if currency not in CURRENCIES:
                currency = "USD"
            users[uname] = {"password": hash_pw(pw), "currency": currency, "created": str(datetime.now())}
            save(USERS_FILE, users)
            success(f"Account created! Welcome, {uname}!")
            audit(uname, "REGISTER")
            time.sleep(0.8)
            return uname

        case "3":
            info("Entering Guest Mode (data not saved between sessions).")
            time.sleep(0.8)
            return "__guest__"

        case "0":
            print(c("\n  👋 Goodbye!\n", "magenta"))
            sys.exit(0)

        case _:
            error("Invalid option.")
            pause()
            return login()

# ─── Expense helpers ──────────────────────────────────────────────────────────
def get_currency(username):
    users = load(USERS_FILE, {})
    code  = users.get(username, {}).get("currency", "USD")
    return CURRENCIES.get(code, "$"), code

def all_expenses(username):
    data = load(EXPENSES_FILE, {})
    return data.get(username, [])

def save_expenses(username, expenses):
    data = load(EXPENSES_FILE, {})
    data[username] = expenses
    save(EXPENSES_FILE, data)

def next_id(expenses):
    return max((e["id"] for e in expenses), default=0) + 1

def fmt_amt(symbol, amount):
    return c(f"{symbol}{amount:,.2f}", "green")

# ─── Feature: Add Expense ─────────────────────────────────────────────────────
def add_expense(username):
    header("➕ Add New Expense")
    symbol, code = get_currency(username)
    expenses = all_expenses(username)

    print(c("  ─── Categories ───────────────────────────\n", "blue"))
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {c(str(i).rjust(2),'yellow')}. {cat}")
    print()

    try:
        cat_idx = int(input(c("  Select category number: ", "cyan"))) - 1
        if not 0 <= cat_idx < len(CATEGORIES):
            error("Invalid category.")
            pause(); return
        category = CATEGORIES[cat_idx]

        amount_str = input(c(f"  Amount ({code}): ", "cyan")).strip()
        amount = float(amount_str)
        if amount <= 0:
            error("Amount must be positive.")
            pause(); return

        description = input(c("  Description: ", "cyan")).strip() or "No description"
        date_str    = input(c("  Date (YYYY-MM-DD) [Enter=today]: ", "cyan")).strip()
        date        = date_str if date_str else datetime.now().strftime("%Y-%m-%d")
        datetime.strptime(date, "%Y-%m-%d")  # validate

        tags_raw = input(c("  Tags (comma-separated, optional): ", "cyan")).strip()
        tags     = [t.strip() for t in tags_raw.split(",") if t.strip()]

        payment  = input(c("  Payment method (Cash/Card/UPI/Other) [Cash]: ", "cyan")).strip() or "Cash"
        notes    = input(c("  Notes (optional): ", "cyan")).strip()

        expense = {
            "id": next_id(expenses),
            "category": category,
            "amount": round(amount, 2),
            "description": description,
            "date": date,
            "tags": tags,
            "payment": payment,
            "notes": notes,
            "added_at": str(datetime.now()),
        }
        expenses.append(expense)
        save_expenses(username, expenses)

        # Budget check
        check_budget_alert(username, category, symbol)

        success(f"Expense added! [{fmt_amt(symbol, amount)}] — {description}")
        audit(username, f"ADD_EXPENSE id={expense['id']} amt={amount}")

    except ValueError as e:
        error(f"Invalid input: {e}")
    pause()

# ─── Feature: View Expenses ───────────────────────────────────────────────────
def view_expenses(username, filter_fn=None, title="All Expenses"):
    header(f"📋 {title}")
    symbol, _ = get_currency(username)
    expenses = all_expenses(username)
    if filter_fn:
        expenses = [e for e in expenses if filter_fn(e)]

    if not expenses:
        warn("No expenses found.")
        pause(); return

    expenses_sorted = sorted(expenses, key=lambda x: x["date"], reverse=True)

    # Table header
    print(c(f"  {'ID':>4}  {'Date':<12} {'Category':<22} {'Amount':>10}  {'Description':<25} {'Pay':<8}", "yellow"))
    line()
    total = 0
    for e in expenses_sorted:
        total += e["amount"]
        print(f"  {c(str(e['id']).rjust(4),'magenta')}  "
              f"{e['date']:<12} "
              f"{e['category']:<22} "
              f"{fmt_amt(symbol, e['amount']):>10}  "
              f"{e['description'][:24]:<25} "
              f"{e['payment']:<8}")
    line()
    print(c(f"  Total: {symbol}{total:,.2f}  ({len(expenses_sorted)} records)", "cyan"))
    pause()

# ─── Feature: Edit / Delete ───────────────────────────────────────────────────
def edit_expense(username):
    header("✏️  Edit Expense")
    view_expenses(username)
    expenses = all_expenses(username)
    if not expenses:
        return
    try:
        eid = int(input(c("  Enter Expense ID to edit: ", "cyan")))
        idx = next((i for i, e in enumerate(expenses) if e["id"] == eid), None)
        if idx is None:
            error("ID not found.")
            pause(); return
        e = expenses[idx]
        print(c(f"\n  Editing: {e['description']} | {e['date']} | {e['amount']}", "yellow"))
        print(c("  (Press Enter to keep current value)\n", "white"))

        new_desc = input(c(f"  Description [{e['description']}]: ", "cyan")).strip()
        new_amt  = input(c(f"  Amount [{e['amount']}]: ", "cyan")).strip()
        new_date = input(c(f"  Date [{e['date']}]: ", "cyan")).strip()
        new_pay  = input(c(f"  Payment [{e['payment']}]: ", "cyan")).strip()
        new_notes= input(c(f"  Notes [{e.get('notes','')}]: ", "cyan")).strip()

        if new_desc:  e["description"] = new_desc
        if new_amt:   e["amount"] = round(float(new_amt), 2)
        if new_date:  e["date"] = new_date
        if new_pay:   e["payment"] = new_pay
        if new_notes: e["notes"] = new_notes
        e["updated_at"] = str(datetime.now())
        expenses[idx] = e
        save_expenses(username, expenses)
        success("Expense updated!")
        audit(username, f"EDIT_EXPENSE id={eid}")
    except (ValueError, StopIteration):
        error("Invalid input.")
    pause()

def delete_expense(username):
    header("🗑️  Delete Expense")
    view_expenses(username)
    expenses = all_expenses(username)
    if not expenses:
        return
    try:
        eid = int(input(c("  Enter Expense ID to delete: ", "cyan")))
        match_ = next((e for e in expenses if e["id"] == eid), None)
        if not match_:
            error("ID not found.")
            pause(); return
        confirm = input(c(f"  Delete '{match_['description']}' ({match_['amount']})? (y/N): ", "yellow")).lower()
        if confirm == "y":
            expenses = [e for e in expenses if e["id"] != eid]
            save_expenses(username, expenses)
            success("Expense deleted.")
            audit(username, f"DELETE_EXPENSE id={eid}")
        else:
            info("Cancelled.")
    except ValueError:
        error("Invalid ID.")
    pause()

# ─── Feature: Search ──────────────────────────────────────────────────────────
def search_expenses(username):
    header("🔍 Search Expenses")
    keyword = input(c("  Enter keyword (description/tag/category): ", "cyan")).strip().lower()
    if not keyword:
        warn("Empty search query.")
        pause(); return
    view_expenses(username,
                  filter_fn=lambda e: (keyword in e["description"].lower() or
                                       keyword in e["category"].lower() or
                                       any(keyword in t.lower() for t in e.get("tags", []))),
                  title=f"Search: '{keyword}'")

# ─── Feature: Budget Manager ──────────────────────────────────────────────────
def budget_menu(username):
    while True:
        header("💼 Budget Manager")
        budgets = load(BUDGETS_FILE, {}).get(username, {})
        symbol, _ = get_currency(username)
        now = datetime.now()

        print(c("  Current Monthly Budgets:\n", "yellow"))
        if budgets:
            for cat, bamt in budgets.items():
                spent = sum(e["amount"] for e in all_expenses(username)
                            if e["category"] == cat and e["date"].startswith(f"{now.year}-{now.month:02d}"))
                pct   = (spent / bamt * 100) if bamt else 0
                bar   = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
                color = "red" if pct >= 90 else ("yellow" if pct >= 70 else "green")
                print(f"  {cat:<25}  {c(bar, color)}  {c(f'{pct:.0f}%', color)}  {symbol}{spent:,.2f}/{symbol}{bamt:,.2f}")
        else:
            info("No budgets set.")

        print(c("\n  [1] Set/Update Budget\n  [2] Delete Budget\n  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":
                for i, cat in enumerate(CATEGORIES, 1):
                    print(f"  {c(str(i).rjust(2),'yellow')}. {cat}")
                try:
                    ci   = int(input(c("  Category #: ", "cyan"))) - 1
                    cat  = CATEGORIES[ci]
                    bamt = float(input(c(f"  Monthly budget for {cat}: {symbol}", "cyan")))
                    all_b = load(BUDGETS_FILE, {})
                    all_b.setdefault(username, {})[cat] = bamt
                    save(BUDGETS_FILE, all_b)
                    success(f"Budget set: {cat} = {symbol}{bamt:,.2f}")
                    audit(username, f"SET_BUDGET cat={cat} amt={bamt}")
                except (ValueError, IndexError):
                    error("Invalid input.")
                pause()

            case "2":
                cat_name = input(c("  Category name to delete: ", "cyan")).strip()
                all_b = load(BUDGETS_FILE, {})
                if username in all_b and cat_name in all_b[username]:
                    del all_b[username][cat_name]
                    save(BUDGETS_FILE, all_b)
                    success("Budget deleted.")
                else:
                    error("Budget not found.")
                pause()

            case "0":
                break

def check_budget_alert(username, category, symbol):
    budgets = load(BUDGETS_FILE, {}).get(username, {})
    if category not in budgets:
        return
    bamt  = budgets[category]
    now   = datetime.now()
    spent = sum(e["amount"] for e in all_expenses(username)
                if e["category"] == category and e["date"].startswith(f"{now.year}-{now.month:02d}"))
    pct = spent / bamt * 100 if bamt else 0
    if pct >= 100:
        warn(f"🚨 OVER BUDGET! {category}: {symbol}{spent:.2f} / {symbol}{bamt:.2f} ({pct:.0f}%)")
    elif pct >= 80:
        warn(f"⚠️  Budget Warning! {category}: {pct:.0f}% used ({symbol}{spent:.2f}/{symbol}{bamt:.2f})")

# ─── Feature: Analytics ───────────────────────────────────────────────────────
def analytics_menu(username):
    while True:
        header("📊 Analytics & Reports")
        print(c("  [1] Monthly Summary\n"
                "  [2] Category Breakdown\n"
                "  [3] Daily Average\n"
                "  [4] Top 5 Expenses\n"
                "  [5] Spending Trend (Last 6 Months)\n"
                "  [6] Payment Method Breakdown\n"
                "  [7] Year-to-Date Report\n"
                "  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1": monthly_summary(username)
            case "2": category_breakdown(username)
            case "3": daily_average(username)
            case "4": top_expenses(username)
            case "5": spending_trend(username)
            case "6": payment_breakdown(username)
            case "7": ytd_report(username)
            case "0": break
            case _: error("Invalid option."); pause()

def monthly_summary(username):
    header("📅 Monthly Summary")
    symbol, _ = get_currency(username)
    expenses = all_expenses(username)
    monthly = defaultdict(float)
    for e in expenses:
        ym = e["date"][:7]
        monthly[ym] += e["amount"]
    if not monthly:
        warn("No data."); pause(); return
    print(c(f"  {'Month':<12} {'Total':>12}  Bar Chart", "yellow"))
    line()
    max_val = max(monthly.values()) or 1
    for ym in sorted(monthly.keys(), reverse=True)[:12]:
        amt = monthly[ym]
        bar = "█" * int(amt / max_val * 30)
        print(f"  {ym:<12} {fmt_amt(symbol, amt):>12}  {c(bar, 'cyan')}")
    pause()

def category_breakdown(username):
    header("📂 Category Breakdown")
    symbol, _ = get_currency(username)
    month_str = input(c("  Month (YYYY-MM) [Enter=current]: ", "cyan")).strip()
    if not month_str:
        month_str = datetime.now().strftime("%Y-%m")
    expenses  = [e for e in all_expenses(username) if e["date"].startswith(month_str)]
    if not expenses:
        warn("No expenses for this month."); pause(); return
    by_cat = defaultdict(float)
    for e in expenses:
        by_cat[e["category"]] += e["amount"]
    total = sum(by_cat.values()) or 1
    print(c(f"\n  Breakdown for {month_str}:\n", "yellow"))
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct = amt / total * 100
        bar = "█" * int(pct / 3)
        print(f"  {cat:<25}  {fmt_amt(symbol, amt):>10}  {c(f'{pct:5.1f}%','yellow')}  {c(bar,'magenta')}")
    line()
    print(c(f"  {'TOTAL':<25}  {symbol}{total:,.2f}", "cyan"))
    pause()

def daily_average(username):
    header("📈 Daily Average Spending")
    symbol, _ = get_currency(username)
    expenses = all_expenses(username)
    if not expenses:
        warn("No data."); pause(); return
    dates  = sorted(set(e["date"] for e in expenses))
    total  = sum(e["amount"] for e in expenses)
    days   = max((datetime.strptime(dates[-1], "%Y-%m-%d") - datetime.strptime(dates[0], "%Y-%m-%d")).days, 1)
    avg    = total / days
    print(f"\n  Total expenses : {fmt_amt(symbol, total)}")
    print(f"  Days tracked   : {c(str(days), 'yellow')}")
    print(f"  Daily average  : {fmt_amt(symbol, avg)}")
    print(f"  Weekly avg     : {fmt_amt(symbol, avg * 7)}")
    print(f"  Monthly avg    : {fmt_amt(symbol, avg * 30)}")
    pause()

def top_expenses(username):
    header("🏆 Top 10 Expenses")
    symbol, _ = get_currency(username)
    expenses = sorted(all_expenses(username), key=lambda x: -x["amount"])[:10]
    if not expenses:
        warn("No data."); pause(); return
    for rank, e in enumerate(expenses, 1):
        print(f"  {c(f'#{rank}','yellow')}  {fmt_amt(symbol, e['amount']):>10}  {e['description'][:30]:<32}  {e['date']}")
    pause()

def spending_trend(username):
    header("📉 Spending Trend – Last 6 Months")
    symbol, _ = get_currency(username)
    expenses = all_expenses(username)
    now   = datetime.now()
    months = [(now - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(5, -1, -1)]
    print(c(f"\n  {'Month':<10} {'Amount':>10}  Trend\n", "yellow"))
    prev = None
    for ym in months:
        amt = sum(e["amount"] for e in expenses if e["date"].startswith(ym))
        if prev is not None:
            arrow = c("▲", "red") if amt > prev else (c("▼", "green") if amt < prev else c("─", "white"))
        else:
            arrow = " "
        bar = "█" * int(amt / 500) if amt else ""
        print(f"  {ym:<10} {fmt_amt(symbol, amt):>10}  {arrow} {c(bar[:40], 'cyan')}")
        prev = amt
    pause()

def payment_breakdown(username):
    header("💳 Payment Method Breakdown")
    symbol, _ = get_currency(username)
    expenses = all_expenses(username)
    by_pay   = defaultdict(float)
    for e in expenses:
        by_pay[e.get("payment", "Cash")] += e["amount"]
    total = sum(by_pay.values()) or 1
    for method, amt in sorted(by_pay.items(), key=lambda x: -x[1]):
        pct = amt / total * 100
        bar = "█" * int(pct / 4)
        print(f"  {method:<12}  {fmt_amt(symbol, amt):>10}  {c(f'{pct:5.1f}%','yellow')}  {c(bar,'blue')}")
    pause()

def ytd_report(username):
    header("📆 Year-to-Date Report")
    symbol, _ = get_currency(username)
    year      = str(datetime.now().year)
    expenses  = [e for e in all_expenses(username) if e["date"].startswith(year)]
    total     = sum(e["amount"] for e in expenses)
    by_cat    = defaultdict(float)
    for e in expenses:
        by_cat[e["category"]] += e["amount"]
    print(c(f"\n  Year: {year}  |  Total: {symbol}{total:,.2f}  |  Records: {len(expenses)}\n", "cyan"))
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct = amt / total * 100 if total else 0
        print(f"  {cat:<25}  {fmt_amt(symbol, amt):>10}  {c(f'{pct:5.1f}%','yellow')}")
    pause()

# ─── Feature: Recurring Expenses ──────────────────────────────────────────────
def recurring_menu(username):
    while True:
        header("🔁 Recurring Expenses")
        recurring = load(RECURRING_FILE, {}).get(username, [])
        symbol, _ = get_currency(username)

        if recurring:
            print(c(f"  {'ID':>3}  {'Name':<20} {'Amount':>10}  {'Frequency':<12} {'Next Due':<12}", "yellow"))
            line()
            for r in recurring:
                print(f"  {c(str(r['id']).rjust(3),'magenta')}  {r['name']:<20} "
                      f"{fmt_amt(symbol, r['amount']):>10}  {r['frequency']:<12} {r['next_due']:<12}")
        else:
            info("No recurring expenses set.")

        print(c("\n  [1] Add Recurring\n  [2] Delete Recurring\n  [3] Apply Due Today\n  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":
                try:
                    name  = input(c("  Name: ", "cyan")).strip()
                    amt   = float(input(c(f"  Amount ({symbol}): ", "cyan")))
                    freq  = input(c("  Frequency (daily/weekly/monthly): ", "cyan")).strip().lower()
                    cat_i = int(input(c("  Category #: ", "cyan"))) - 1
                    cat   = CATEGORIES[cat_i]
                    start = input(c("  Start date (YYYY-MM-DD) [today]: ", "cyan")).strip() or datetime.now().strftime("%Y-%m-%d")
                    all_r = load(RECURRING_FILE, {})
                    lst   = all_r.get(username, [])
                    rid   = max((r["id"] for r in lst), default=0) + 1
                    lst.append({"id": rid, "name": name, "amount": amt, "frequency": freq,
                                "category": cat, "next_due": start})
                    all_r[username] = lst
                    save(RECURRING_FILE, all_r)
                    success("Recurring expense added!")
                except (ValueError, IndexError):
                    error("Invalid input.")
                pause()

            case "2":
                try:
                    rid  = int(input(c("  ID to delete: ", "cyan")))
                    all_r = load(RECURRING_FILE, {})
                    lst   = [r for r in all_r.get(username, []) if r["id"] != rid]
                    all_r[username] = lst
                    save(RECURRING_FILE, all_r)
                    success("Deleted.")
                except ValueError:
                    error("Invalid ID.")
                pause()

            case "3":
                apply_recurring(username)

            case "0":
                break

def apply_recurring(username):
    today = datetime.now().strftime("%Y-%m-%d")
    all_r = load(RECURRING_FILE, {})
    lst   = all_r.get(username, [])
    expenses = all_expenses(username)
    applied  = 0
    for r in lst:
        if r["next_due"] <= today:
            expenses.append({
                "id": next_id(expenses), "category": r["category"],
                "amount": r["amount"], "description": f"[Recurring] {r['name']}",
                "date": today, "tags": ["recurring"], "payment": "Auto",
                "notes": "", "added_at": str(datetime.now()),
            })
            # advance next_due
            nd = datetime.strptime(r["next_due"], "%Y-%m-%d")
            match r["frequency"]:
                case "daily":   nd += timedelta(days=1)
                case "weekly":  nd += timedelta(weeks=1)
                case "monthly": nd = nd.replace(month=nd.month % 12 + 1) if nd.month < 12 else nd.replace(year=nd.year + 1, month=1)
            r["next_due"] = nd.strftime("%Y-%m-%d")
            applied += 1
    save_expenses(username, expenses)
    all_r[username] = lst
    save(RECURRING_FILE, all_r)
    if applied:
        success(f"{applied} recurring expense(s) applied for today.")
    else:
        info("No recurring expenses due today.")
    pause()

# ─── Feature: Savings Goals ───────────────────────────────────────────────────
def goals_menu(username):
    while True:
        header("🎯 Savings Goals")
        goals  = load(GOALS_FILE, {}).get(username, [])
        symbol, _ = get_currency(username)

        if goals:
            for g in goals:
                pct = (g["saved"] / g["target"] * 100) if g["target"] else 0
                bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                color = "green" if pct >= 100 else ("yellow" if pct >= 50 else "cyan")
                print(f"\n  📌 {c(g['name'],'yellow')} — Target: {symbol}{g['target']:,.2f}")
                print(f"     {c(bar, color)} {c(f'{pct:.1f}%', color)}  Saved: {symbol}{g['saved']:,.2f}")
        else:
            info("No goals set.")

        print(c("\n  [1] Add Goal\n  [2] Contribute to Goal\n  [3] Delete Goal\n  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":
                try:
                    name   = input(c("  Goal name: ", "cyan")).strip()
                    target = float(input(c(f"  Target amount ({symbol}): ", "cyan")))
                    all_g  = load(GOALS_FILE, {})
                    lst    = all_g.get(username, [])
                    gid    = max((g["id"] for g in lst), default=0) + 1
                    lst.append({"id": gid, "name": name, "target": target, "saved": 0.0,
                                "created": str(datetime.now())})
                    all_g[username] = lst
                    save(GOALS_FILE, all_g)
                    success("Goal created!")
                except ValueError:
                    error("Invalid input.")
                pause()

            case "2":
                try:
                    gid  = int(input(c("  Goal ID: ", "cyan")))
                    amt  = float(input(c(f"  Amount to add ({symbol}): ", "cyan")))
                    all_g = load(GOALS_FILE, {})
                    for g in all_g.get(username, []):
                        if g["id"] == gid:
                            g["saved"] = round(g["saved"] + amt, 2)
                            if g["saved"] >= g["target"]:
                                success(f"🎉 Goal '{g['name']}' achieved!")
                            break
                    save(GOALS_FILE, all_g)
                    success("Contribution saved!")
                except ValueError:
                    error("Invalid input.")
                pause()

            case "3":
                try:
                    gid   = int(input(c("  Goal ID to delete: ", "cyan")))
                    all_g = load(GOALS_FILE, {})
                    all_g[username] = [g for g in all_g.get(username, []) if g["id"] != gid]
                    save(GOALS_FILE, all_g)
                    success("Goal deleted.")
                except ValueError:
                    error("Invalid ID.")
                pause()

            case "0":
                break

# ─── Feature: Export / Import ─────────────────────────────────────────────────
def export_menu(username):
    while True:
        header("📤 Export / Import")
        print(c("  [1] Export to CSV\n"
                "  [2] Export to JSON\n"
                "  [3] Import from CSV\n"
                "  [4] Import from JSON\n"
                "  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1": export_csv(username)
            case "2": export_json(username)
            case "3": import_csv(username)
            case "4": import_json(username)
            case "0": break
            case _: error("Invalid option."); pause()

def export_csv(username):
    expenses = all_expenses(username)
    if not expenses:
        warn("No expenses to export."); pause(); return
    fname = os.path.join(EXPORT_DIR, f"expenses_{username}_{datetime.now():%Y%m%d_%H%M%S}.csv")
    with open(fname, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id","date","category","amount","description","payment","tags","notes"])
        writer.writeheader()
        for e in expenses:
            row = {k: e.get(k, "") for k in ["id","date","category","amount","description","payment","notes"]}
            row["tags"] = ",".join(e.get("tags", []))
            writer.writerow(row)
    success(f"Exported to:\n  {fname}")
    audit(username, f"EXPORT_CSV count={len(expenses)}")
    pause()

def export_json(username):
    expenses = all_expenses(username)
    if not expenses:
        warn("No expenses."); pause(); return
    fname = os.path.join(EXPORT_DIR, f"expenses_{username}_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(fname, "w") as f:
        json.dump(expenses, f, indent=2)
    success(f"Exported to:\n  {fname}")
    audit(username, f"EXPORT_JSON count={len(expenses)}")
    pause()

def import_csv(username):
    fpath = input(c("  CSV file path: ", "cyan")).strip().strip('"')
    if not os.path.exists(fpath):
        error("File not found."); pause(); return
    expenses = all_expenses(username)
    count = 0
    with open(fpath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append({
                "id": next_id(expenses), "date": row.get("date",""),
                "category": row.get("category","📦 Miscellaneous"),
                "amount": float(row.get("amount", 0)),
                "description": row.get("description","Imported"),
                "payment": row.get("payment","Unknown"),
                "tags": [t for t in row.get("tags","").split(",") if t],
                "notes": row.get("notes",""),
                "added_at": str(datetime.now()),
            })
            count += 1
    save_expenses(username, expenses)
    success(f"Imported {count} expense(s).")
    audit(username, f"IMPORT_CSV count={count}")
    pause()

def import_json(username):
    fpath = input(c("  JSON file path: ", "cyan")).strip().strip('"')
    if not os.path.exists(fpath):
        error("File not found."); pause(); return
    try:
        with open(fpath) as f:
            imported = json.load(f)
        expenses = all_expenses(username)
        for e in imported:
            e["id"] = next_id(expenses)
            expenses.append(e)
        save_expenses(username, expenses)
        success(f"Imported {len(imported)} expense(s).")
        audit(username, f"IMPORT_JSON count={len(imported)}")
    except Exception as ex:
        error(f"Import failed: {ex}")
    pause()

# ─── Feature: Settings ────────────────────────────────────────────────────────
def settings_menu(username):
    while True:
        header("⚙️  Settings")
        users    = load(USERS_FILE, {})
        settings = load(SETTINGS_FILE, {}).get(username, {})
        user_cfg = users.get(username, {})

        print(c(f"  Username     : {username}", "yellow"))
        print(c(f"  Currency     : {user_cfg.get('currency','USD')}", "yellow"))
        print(c(f"  Theme        : {settings.get('theme','default')}", "yellow"))
        print(c(f"  Account Since: {user_cfg.get('created','N/A')[:10]}", "yellow"))

        print(c("\n  [1] Change Currency\n"
                "  [2] Change Password\n"
                "  [3] View Audit Log\n"
                "  [4] Clear All My Data\n"
                "  [5] About\n"
                "  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":
                print(c(f"\n  Available: {', '.join(CURRENCIES.keys())}", "cyan"))
                cur = input(c("  New currency code: ", "cyan")).upper().strip()
                if cur in CURRENCIES:
                    users[username]["currency"] = cur
                    save(USERS_FILE, users)
                    success(f"Currency updated to {cur}.")
                else:
                    error("Unsupported currency.")
                pause()

            case "2":
                if username == "__guest__":
                    warn("Guests cannot change passwords."); pause(); continue
                pw  = getpass.getpass(c("  Current password: ", "yellow"))
                if users[username]["password"] != hash_pw(pw):
                    error("Incorrect password."); pause(); continue
                np  = getpass.getpass(c("  New password: ", "yellow"))
                np2 = getpass.getpass(c("  Confirm: ", "yellow"))
                if np != np2:
                    error("Passwords don't match."); pause(); continue
                users[username]["password"] = hash_pw(np)
                save(USERS_FILE, users)
                success("Password changed.")
                audit(username, "CHANGE_PASSWORD")
                pause()

            case "3":
                header("📜 Audit Log (Last 20 Entries)")
                try:
                    with open(LOGS_FILE) as f:
                        lines = [l for l in f.readlines() if f"USER={username}" in l]
                    for l in lines[-20:]:
                        print(c(f"  {l.rstrip()}", "white"))
                except FileNotFoundError:
                    info("No log entries yet.")
                pause()

            case "4":
                confirm = input(c("  ⚠️  Type DELETE to confirm clearing ALL your data: ", "red")).strip()
                if confirm == "DELETE":
                    save_expenses(username, [])
                    all_b = load(BUDGETS_FILE, {}); all_b.pop(username, None); save(BUDGETS_FILE, all_b)
                    all_g = load(GOALS_FILE, {});   all_g.pop(username, None); save(GOALS_FILE, all_g)
                    all_r = load(RECURRING_FILE,{}); all_r.pop(username, None); save(RECURRING_FILE, all_r)
                    success("All data cleared.")
                    audit(username, "CLEAR_ALL_DATA")
                else:
                    info("Cancelled.")
                pause()

            case "5":
                about_screen()

            case "0":
                break

def about_screen():
    header("ℹ️  About")
    print(c(f"""
  ╔══════════════════════════════════════════════════════╗
  ║        💰 NOOR EXPENSE TRACKER v{VERSION}              ║
  ║                                                      ║
  ║   Developed by : {AUTHOR:<35}║
  ║   GitHub       : {GITHUB:<35}║
  ║   Platform     : {platform.system()} {platform.release():<28}║
  ║   Python       : {sys.version.split()[0]:<35}║
  ║                                                      ║
  ║   Features:                                          ║
  ║   • Multi-user auth with hashed passwords            ║
  ║   • 19 spending categories                           ║
  ║   • Budget tracking & alerts                         ║
  ║   • Recurring expense automation                     ║
  ║   • Savings goals tracker                            ║
  ║   • Full analytics & trend reports                   ║
  ║   • CSV & JSON import/export                         ║
  ║   • Audit logging                                    ║
  ║   • Cross-platform (Windows/Linux/macOS)             ║
  ╚══════════════════════════════════════════════════════╝
""", "cyan"))
    pause()

# ─── Dashboard ────────────────────────────────────────────────────────────────
def dashboard(username):
    header("🏠 Dashboard")
    symbol, code = get_currency(username)
    expenses  = all_expenses(username)
    now       = datetime.now()
    this_month = now.strftime("%Y-%m")
    this_week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")

    monthly_total = sum(e["amount"] for e in expenses if e["date"].startswith(this_month))
    weekly_total  = sum(e["amount"] for e in expenses if e["date"] >= this_week_start)
    today_total   = sum(e["amount"] for e in expenses if e["date"] == now.strftime("%Y-%m-%d"))
    all_time      = sum(e["amount"] for e in expenses)

    budgets = load(BUDGETS_FILE, {}).get(username, {})
    total_budget = sum(budgets.values())
    budget_pct   = (monthly_total / total_budget * 100) if total_budget else 0

    goals = load(GOALS_FILE, {}).get(username, [])
    recurring = load(RECURRING_FILE, {}).get(username, [])
    due_today = [r for r in recurring if r["next_due"] <= now.strftime("%Y-%m-%d")]

    print(c(f"  👤 User: {username}  |  💱 Currency: {code}  |  📅 {now.strftime('%A, %d %b %Y')}\n", "cyan"))
    line()
    print(f"  📆 Today        : {fmt_amt(symbol, today_total)}")
    print(f"  📅 This Week    : {fmt_amt(symbol, weekly_total)}")
    print(f"  🗓️  This Month   : {fmt_amt(symbol, monthly_total)}", end="")
    if total_budget:
        color = "red" if budget_pct >= 90 else ("yellow" if budget_pct >= 70 else "green")
        bar   = "█" * int(budget_pct / 10) + "░" * (10 - int(budget_pct / 10))
        print(f"  [{c(bar, color)} {c(f'{budget_pct:.0f}%', color)} of budget]")
    else:
        print()
    print(f"  💼 All Time     : {fmt_amt(symbol, all_time)}")
    print(f"  🎯 Active Goals : {c(str(len(goals)), 'yellow')}")
    if due_today:
        print(c(f"\n  ⚠️  {len(due_today)} recurring expense(s) due today!", "red"))
    line()
    pause()

# ─── Filter views ─────────────────────────────────────────────────────────────
def filter_menu(username):
    while True:
        header("🔎 Filter & View Expenses")
        print(c("  [1] This Month\n"
                "  [2] This Year\n"
                "  [3] Custom Date Range\n"
                "  [4] By Category\n"
                "  [5] By Payment Method\n"
                "  [6] By Tag\n"
                "  [7] All Expenses\n"
                "  [0] Back\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":
                ym = datetime.now().strftime("%Y-%m")
                view_expenses(username, lambda e: e["date"].startswith(ym), f"Expenses — {ym}")
            case "2":
                yr = str(datetime.now().year)
                view_expenses(username, lambda e: e["date"].startswith(yr), f"Expenses — {yr}")
            case "3":
                d1 = input(c("  From (YYYY-MM-DD): ", "cyan")).strip()
                d2 = input(c("  To   (YYYY-MM-DD): ", "cyan")).strip()
                view_expenses(username, lambda e: d1 <= e["date"] <= d2, f"{d1} to {d2}")
            case "4":
                for i, cat in enumerate(CATEGORIES, 1):
                    print(f"  {c(str(i).rjust(2),'yellow')}. {cat}")
                try:
                    ci = int(input(c("  Category #: ", "cyan"))) - 1
                    cat = CATEGORIES[ci]
                    view_expenses(username, lambda e, c=cat: e["category"] == c, cat)
                except (ValueError, IndexError):
                    error("Invalid."); pause()
            case "5":
                method = input(c("  Payment method: ", "cyan")).strip()
                view_expenses(username, lambda e: e.get("payment","").lower() == method.lower(), f"Payment: {method}")
            case "6":
                tag = input(c("  Tag: ", "cyan")).strip().lower()
                view_expenses(username, lambda e: any(tag in t.lower() for t in e.get("tags", [])), f"Tag: {tag}")
            case "7":
                view_expenses(username)
            case "0":
                break
            case _:
                error("Invalid option."); pause()

# ─── Main Menu ────────────────────────────────────────────────────────────────
def main_menu(username):
    apply_recurring(username)   # auto-apply due recurring on startup
    while True:
        header("📌 Main Menu")
        print(c(f"  Logged in as: {c(username, 'yellow')}\n", "white"))
        print(c(
            "  [1]  🏠 Dashboard\n"
            "  [2]  ➕ Add Expense\n"
            "  [3]  📋 View / Filter Expenses\n"
            "  [4]  ✏️  Edit Expense\n"
            "  [5]  🗑️  Delete Expense\n"
            "  [6]  🔍 Search Expenses\n"
            "  [7]  💼 Budget Manager\n"
            "  [8]  📊 Analytics & Reports\n"
            "  [9]  🔁 Recurring Expenses\n"
            "  [10] 🎯 Savings Goals\n"
            "  [11] 📤 Export / Import\n"
            "  [12] ⚙️  Settings\n"
            "  [0]  🚪 Logout\n", "white"))
        choice = input(c("  → Choose: ", "cyan")).strip()

        match choice:
            case "1":  dashboard(username)
            case "2":  add_expense(username)
            case "3":  filter_menu(username)
            case "4":  edit_expense(username)
            case "5":  delete_expense(username)
            case "6":  search_expenses(username)
            case "7":  budget_menu(username)
            case "8":  analytics_menu(username)
            case "9":  recurring_menu(username)
            case "10": goals_menu(username)
            case "11": export_menu(username)
            case "12": settings_menu(username)
            case "0":
                audit(username, "LOGOUT")
                success("Logged out successfully.")
                time.sleep(0.5)
                break
            case _:
                error("Invalid option, please try again.")
                pause()

# ─── Splash Screen ────────────────────────────────────────────────────────────
def splash():
    clear()
    art = r"""
  ███╗   ██╗ ██████╗  ██████╗ ██████╗
  ████╗  ██║██╔═══██╗██╔═══██╗██╔══██╗
  ██╔██╗ ██║██║   ██║██║   ██║██████╔╝
  ██║╚██╗██║██║   ██║██║   ██║██╔══██╗
  ██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║
  ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
     💰 EXPENSE TRACKER  v{VERSION}
"""
    print(c(art.format(VERSION=VERSION), "cyan"))
    print(c(f"     Developed by {AUTHOR}", "yellow"))
    print(c(f"     {GITHUB}\n", "white"))
    time.sleep(1.2)

# ─── Entry Point ──────────────────────────────────────────────────────────────
def main():
    ensure_dirs()
    splash()
    while True:
        username = login()
        main_menu(username)
        again = input(c("\n  Switch account? (y/N): ", "cyan")).strip().lower()
        if again != "y":
            print(c("\n  👋 Thank you for using Noor Expense Tracker!\n", "magenta"))
            sys.exit(0)

if __name__ == "__main__":
    main()

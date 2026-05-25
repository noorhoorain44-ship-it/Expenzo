import streamlit as st
import json
import os
import hashlib
import datetime
import csv
import io
from datetime import datetime, timedelta
import pandas as pd

# ============== CONFIGURATION ==============
DATA_DIR = os.path.expanduser("~/.noorexpense_streamlit")
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "users": os.path.join(DATA_DIR, "users.json"),
    "expenses": os.path.join(DATA_DIR, "expenses.json"),
    "budgets": os.path.join(DATA_DIR, "budgets.json"),
    "recurring": os.path.join(DATA_DIR, "recurring.json"),
    "goals": os.path.join(DATA_DIR, "goals.json"),
    "settings": os.path.join(DATA_DIR, "settings.json"),
}

CURRENCIES = {
    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹",
    "PKR": "₨", "JPY": "¥", "AUD": "A$", "CAD": "C$"
}

CATEGORIES = [
    "🍔 Food & Dining", "🚗 Transport", "🏠 Housing & Rent", "💡 Utilities",
    "🛒 Groceries", "🏥 Healthcare", "🎬 Entertainment", "📚 Education",
    "👕 Clothing", "💻 Electronics", "✈️ Travel", "🎁 Gifts",
    "💼 Insurance", "💳 Subscriptions", "🐶 Pets", "🧹 Household",
    "💇 Personal Care", "🏋️ Fitness", "🎮 Hobbies", "📦 Other"
]

PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Mobile Payment", "Crypto", "Other"]

# ============== INITIALIZATION ==============
def init_data():
    for key, path in FILES.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                if key == "settings":
                    json.dump({"currency": "USD", "theme": "light"}, f)
                else:
                    json.dump({} if key == "users" else [], f)

init_data()

# ============== HELPER FUNCTIONS ==============
def load_data(key):
    with open(FILES[key], "r") as f:
        return json.load(f)

def save_data(key, data):
    with open(FILES[key], "w") as f:
        json.dump(data, f, indent=2, default=str)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_currency_symbol():
    settings = load_data("settings")
    return CURRENCIES.get(settings.get("currency", "USD"), "$")

def format_currency(amount):
    return f"{get_currency_symbol()}{float(amount):,.2f}"

def get_user_expenses(username):
    expenses = load_data("expenses")
    return [e for e in expenses if e.get("user") == username]

def get_next_id(items):
    if not items:
        return 1
    return max([int(i.get("id", 0)) for i in items]) + 1

def get_month_start():
    today = datetime.now()
    return today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def get_week_start():
    today = datetime.now()
    return today - timedelta(days=today.weekday())

# ============== AUTHENTICATION ==============
def login_page():
    st.markdown("""
        <div style="text-align:center; padding: 2rem;">
            <h1 style="font-size: 3rem; color: #00d4ff;">💰 Noor Expense Tracker</h1>
            <p style="font-size: 1.2rem; color: #888;">v2.0.0 — Streamlit Edition</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True, type="primary"):
                users = load_data("users")
                if username in users and users[username]["password"] == hash_password(password):
                    st.session_state["user"] = username
                    st.session_state["currency"] = users[username].get("currency", "USD")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

            if st.button("👤 Continue as Guest", use_container_width=True):
                st.session_state["user"] = "guest"
                st.session_state["currency"] = "USD"
                st.rerun()

        with tab2:
            new_user = st.text_input("Username", key="reg_user")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
            currency = st.selectbox("Currency", list(CURRENCIES.keys()), key="reg_currency")

            if st.button("Register", use_container_width=True, type="primary"):
                users = load_data("users")
                if not new_user or not new_pass:
                    st.error("Please fill all fields")
                elif new_user in users:
                    st.error("Username already exists")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")
                else:
                    users[new_user] = {
                        "password": hash_password(new_pass),
                        "currency": currency,
                        "created": datetime.now().isoformat()
                    }
                    save_data("users", users)
                    st.success("Account created! Please login.")

# ============== DASHBOARD ==============
def dashboard():
    st.markdown(f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1>🏠 Dashboard</h1>
            <p>👤 {st.session_state["user"]} | 💱 {st.session_state.get("currency", "USD")} | {datetime.now().strftime("%A, %d %b %Y")}</p>
        </div>
    """, unsafe_allow_html=True)

    expenses = get_user_expenses(st.session_state["user"])
    today = datetime.now().date()
    week_start = get_week_start().date()
    month_start = get_month_start().date()

    today_total = sum(float(e["amount"]) for e in expenses if datetime.fromisoformat(e["date"]).date() == today)
    week_total = sum(float(e["amount"]) for e in expenses if datetime.fromisoformat(e["date"]).date() >= week_start)
    month_total = sum(float(e["amount"]) for e in expenses if datetime.fromisoformat(e["date"]).date() >= month_start)
    all_time = sum(float(e["amount"]) for e in expenses)

    goals = load_data("goals")
    user_goals = [g for g in goals if g.get("user") == st.session_state["user"]]
    active_goals = len([g for g in user_goals if not g.get("completed", False)])

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("📆 Today", today_total, "#00d4ff"),
        ("📅 This Week", week_total, "#00ff88"),
        ("🗓️ This Month", month_total, "#ffaa00"),
        ("💼 All Time", all_time, "#ff6b6b"),
        ("🎯 Active Goals", active_goals, "#cc66ff")
    ]

    for col, (label, value, color) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}22, {color}11); 
                            border-left: 4px solid {color}; 
                            padding: 1rem; border-radius: 8px;">
                    <p style="margin:0; color:#888; font-size:0.9rem;">{label}</p>
                    <h3 style="margin:0; color:{color};">{format_currency(value) if isinstance(value, float) else value}</h3>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Budget Progress
    budgets = load_data("budgets")
    user_budgets = [b for b in budgets if b.get("user") == st.session_state["user"]]

    if user_budgets:
        st.subheader("💼 Budget Progress")
        for budget in user_budgets:
            cat = budget["category"]
            limit = float(budget["limit"])
            spent = sum(float(e["amount"]) for e in expenses 
                       if e.get("category") == cat 
                       and datetime.fromisoformat(e["date"]).date() >= month_start)
            pct = min(100, (spent / limit * 100)) if limit > 0 else 0

            color = "#00ff88" if pct < 80 else "#ffaa00" if pct < 100 else "#ff4444"
            warning = " ⚠️" if pct >= 100 else ""

            st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                        <span>{cat}</span>
                        <span>{format_currency(spent)}/{format_currency(limit)}{warning}</span>
                    </div>
                    <div style="background:#333; height:20px; border-radius:10px; overflow:hidden;">
                        <div style="background:{color}; width:{pct}%; height:100%; transition:width 0.5s;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Recent Expenses
    st.subheader("📋 Recent Expenses")
    if expenses:
        recent = sorted(expenses, key=lambda x: x["date"], reverse=True)[:5]
        df = pd.DataFrame(recent)
        df["amount"] = df["amount"].apply(lambda x: format_currency(x))
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(df[["id", "date", "category", "amount", "description"]], use_container_width=True, hide_index=True)
    else:
        st.info("No expenses yet. Add your first expense!")

# ============== ADD EXPENSE ==============
def add_expense():
    st.markdown("<h1 style='text-align:center;'>➕ Add Expense</h1>", unsafe_allow_html=True)

    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.now())
            amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
            category = st.selectbox("Category", CATEGORIES)
        with col2:
            payment = st.selectbox("Payment Method", PAYMENT_METHODS)
            tags = st.text_input("Tags (comma separated)")
            recurring = st.checkbox("Make Recurring")

        description = st.text_area("Description/Notes")

        if recurring:
            rec_type = st.selectbox("Recurring Type", ["Daily", "Weekly", "Monthly"])

        submitted = st.form_submit_button("💾 Save Expense", use_container_width=True, type="primary")

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than 0")
                return

            expenses = load_data("expenses")
            new_expense = {
                "id": get_next_id(expenses),
                "user": st.session_state["user"],
                "date": date.isoformat(),
                "amount": amount,
                "category": category,
                "payment_method": payment,
                "tags": [t.strip() for t in tags.split(",") if t.strip()],
                "description": description,
                "created": datetime.now().isoformat()
            }
            expenses.append(new_expense)
            save_data("expenses", expenses)

            if recurring:
                recurring_data = load_data("recurring")
                recurring_data.append({
                    "id": get_next_id(recurring_data),
                    "user": st.session_state["user"],
                    "expense_id": new_expense["id"],
                    "type": rec_type,
                    "amount": amount,
                    "category": category,
                    "payment_method": payment,
                    "description": description,
                    "tags": new_expense["tags"],
                    "next_date": date.isoformat(),
                    "active": True
                })
                save_data("recurring", recurring_data)

            st.success(f"Expense saved! {format_currency(amount)} for {category}")

# ============== VIEW & FILTER ==============
def view_expenses():
    st.markdown("<h1 style='text-align:center;'>📋 View & Filter Expenses</h1>", unsafe_allow_html=True)

    expenses = get_user_expenses(st.session_state["user"])

    with st.expander("🔎 Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date_from = st.date_input("From", value=None)
            date_to = st.date_input("To", value=None)
        with col2:
            cat_filter = st.multiselect("Categories", CATEGORIES)
            pay_filter = st.multiselect("Payment Methods", PAYMENT_METHODS)
        with col3:
            tag_filter = st.text_input("Search Tags")
            min_amount = st.number_input("Min Amount", min_value=0.0, step=10.0)
            max_amount = st.number_input("Max Amount", min_value=0.0, step=100.0)

    filtered = expenses
    if date_from:
        filtered = [e for e in filtered if datetime.fromisoformat(e["date"]).date() >= date_from]
    if date_to:
        filtered = [e for e in filtered if datetime.fromisoformat(e["date"]).date() <= date_to]
    if cat_filter:
        filtered = [e for e in filtered if e.get("category") in cat_filter]
    if pay_filter:
        filtered = [e for e in filtered if e.get("payment_method") in pay_filter]
    if tag_filter:
        filtered = [e for e in filtered if any(tag_filter.lower() in t.lower() for t in e.get("tags", []))]
    if min_amount > 0:
        filtered = [e for e in filtered if float(e["amount"]) >= min_amount]
    if max_amount > 0:
        filtered = [e for e in filtered if float(e["amount"]) <= max_amount]

    if filtered:
        df = pd.DataFrame(filtered)
        df["amount"] = df["amount"].apply(lambda x: format_currency(x))
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(df[["id", "date", "category", "amount", "payment_method", "description", "tags"]], 
                    use_container_width=True, hide_index=True)

        total = sum(float(e["amount"]) for e in filtered)
        st.metric("Total Filtered", format_currency(total))
    else:
        st.info("No expenses match your filters")

# ============== EDIT/DELETE ==============
def edit_expense():
    st.markdown("<h1 style='text-align:center;'>✏️ Edit / 🗑️ Delete Expense</h1>", unsafe_allow_html=True)

    expenses = get_user_expenses(st.session_state["user"])

    if not expenses:
        st.info("No expenses to edit")
        return

    expense_ids = {f"#{e['id']} - {e['category']} - {format_currency(e['amount'])} ({e['date'][:10]})": e for e in expenses}
    selected = st.selectbox("Select Expense", list(expense_ids.keys()))

    if selected:
        expense = expense_ids[selected]

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_date = st.date_input("Date", datetime.fromisoformat(expense["date"]))
                new_amount = st.number_input("Amount", value=float(expense["amount"]), min_value=0.0, step=0.01)
                new_cat = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(expense["category"]) if expense["category"] in CATEGORIES else 0)
            with col2:
                new_pay = st.selectbox("Payment Method", PAYMENT_METHODS, index=PAYMENT_METHODS.index(expense["payment_method"]) if expense["payment_method"] in PAYMENT_METHODS else 0)
                new_tags = st.text_input("Tags", ", ".join(expense.get("tags", [])))
                new_desc = st.text_area("Description", expense.get("description", ""))

            col_save, col_del = st.columns(2)
            with col_save:
                save_btn = st.form_submit_button("💾 Update", use_container_width=True, type="primary")
            with col_del:
                del_btn = st.form_submit_button("🗑️ Delete", use_container_width=True)

            if save_btn:
                expense["date"] = new_date.isoformat()
                expense["amount"] = new_amount
                expense["category"] = new_cat
                expense["payment_method"] = new_pay
                expense["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                expense["description"] = new_desc
                save_data("expenses", expenses)
                st.success("Expense updated!")
                st.rerun()

            if del_btn:
                expenses.remove(expense)
                save_data("expenses", expenses)
                st.success("Expense deleted!")
                st.rerun()

# ============== SEARCH ==============
def search_expenses():
    st.markdown("<h1 style='text-align:center;'>🔍 Search Expenses</h1>", unsafe_allow_html=True)

    query = st.text_input("Search by keyword, tag, or description", placeholder="e.g., grocery, uber, rent...")

    if query:
        expenses = get_user_expenses(st.session_state["user"])
        results = []

        for e in expenses:
            search_text = f"{e.get('description', '')} {e.get('category', '')} {' '.join(e.get('tags', []))} {e.get('payment_method', '')}".lower()
            if query.lower() in search_text:
                results.append(e)

        if results:
            df = pd.DataFrame(results)
            df["amount"] = df["amount"].apply(lambda x: format_currency(x))
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(df[["id", "date", "category", "amount", "description", "tags"]], use_container_width=True, hide_index=True)
            st.metric("Results Found", len(results))
        else:
            st.warning("No matches found")

# ============== BUDGET MANAGER ==============
def budget_manager():
    st.markdown("<h1 style='text-align:center;'>💼 Budget Manager</h1>", unsafe_allow_html=True)

    budgets = load_data("budgets")
    user_budgets = [b for b in budgets if b.get("user") == st.session_state["user"]]

    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        with col1:
            budget_cat = st.selectbox("Category", CATEGORIES)
        with col2:
            budget_limit = st.number_input("Monthly Limit", min_value=0.0, step=10.0, format="%.2f")

        if st.form_submit_button("➕ Add Budget", use_container_width=True, type="primary"):
            existing = [b for b in user_budgets if b["category"] == budget_cat]
            if existing:
                existing[0]["limit"] = budget_limit
            else:
                budgets.append({
                    "id": get_next_id(budgets),
                    "user": st.session_state["user"],
                    "category": budget_cat,
                    "limit": budget_limit
                })
            save_data("budgets", budgets)
            st.success(f"Budget set for {budget_cat}: {format_currency(budget_limit)}")
            st.rerun()

    st.divider()
    st.subheader("Current Budgets")

    expenses = get_user_expenses(st.session_state["user"])
    month_start = get_month_start().date()

    for budget in user_budgets:
        cat = budget["category"]
        limit = float(budget["limit"])
        spent = sum(float(e["amount"]) for e in expenses 
                   if e.get("category") == cat 
                   and datetime.fromisoformat(e["date"]).date() >= month_start)
        pct = min(100, (spent / limit * 100)) if limit > 0 else 0

        col_info, col_bar, col_del = st.columns([2, 4, 1])
        with col_info:
            st.write(f"**{cat}**")
            st.caption(f"{format_currency(spent)} / {format_currency(limit)}")
        with col_bar:
            color = "#00ff88" if pct < 80 else "#ffaa00" if pct < 100 else "#ff4444"
            st.markdown(f"""
                <div style="background:#333; height:25px; border-radius:12px; overflow:hidden; margin-top:10px;">
                    <div style="background:{color}; width:{pct}%; height:100%;"></div>
                </div>
                <p style="text-align:center; margin:0; font-size:0.8rem;">{pct:.1f}%</p>
            """, unsafe_allow_html=True)
        with col_del:
            if st.button("🗑️", key=f"del_budget_{budget['id']}"):
                budgets.remove(budget)
                save_data("budgets", budgets)
                st.rerun()

# ============== ANALYTICS ==============
def analytics():
    st.markdown("<h1 style='text-align:center;'>📊 Analytics & Reports</h1>", unsafe_allow_html=True)

    expenses = get_user_expenses(st.session_state["user"])

    if not expenses:
        st.info("No data to analyze yet")
        return

    # Monthly Summary
    st.subheader("📅 Monthly Summary")
    df = pd.DataFrame(expenses)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month")["amount"].sum().reset_index()
    monthly["month_str"] = monthly["month"].astype(str)

    st.bar_chart(monthly.set_index("month_str")["amount"])

    # Category Breakdown
    st.subheader("🍰 Category Breakdown")
    cat_data = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(cat_data.reset_index().rename(columns={"amount": "Total"}), use_container_width=True)
    with col2:
        import plotly.express as px
        fig = px.pie(values=cat_data.values, names=cat_data.index, title="Spending by Category")
        st.plotly_chart(fig, use_container_width=True)

    # Payment Method Analysis
    st.subheader("💳 Payment Method Analysis")
    pay_data = df.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
    st.bar_chart(pay_data)

    # YTD Report
    st.subheader("📈 Year to Date")
    current_year = datetime.now().year
    ytd = df[df["date"].dt.year == current_year]
    if not ytd.empty:
        ytd_total = ytd["amount"].sum()
        ytd_avg = ytd["amount"].mean()
        ytd_count = len(ytd)

        c1, c2, c3 = st.columns(3)
        c1.metric("YTD Total", format_currency(ytd_total))
        c2.metric("Average/Expense", format_currency(ytd_avg))
        c3.metric("Total Transactions", ytd_count)

# ============== RECURRING ==============
def recurring_expenses():
    st.markdown("<h1 style='text-align:center;'>🔁 Recurring Expenses</h1>", unsafe_allow_html=True)

    recurring = load_data("recurring")
    user_recurring = [r for r in recurring if r.get("user") == st.session_state["user"]]

    if user_recurring:
        for rec in user_recurring:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.write(f"**{rec['category']}**")
                    st.caption(rec.get("description", "No description"))
                with col2:
                    st.write(format_currency(rec["amount"]))
                with col3:
                    st.write(f"🔁 {rec['type']}")
                    st.caption(f"Next: {rec.get('next_date', 'N/A')[:10]}")
                with col4:
                    if st.button("🗑️", key=f"del_rec_{rec['id']}"):
                        recurring.remove(rec)
                        save_data("recurring", recurring)
                        st.rerun()
                st.divider()
    else:
        st.info("No recurring expenses set up")

# ============== SAVINGS GOALS ==============
def savings_goals():
    st.markdown("<h1 style='text-align:center;'>🎯 Savings Goals</h1>", unsafe_allow_html=True)

    goals = load_data("goals")
    user_goals = [g for g in goals if g.get("user") == st.session_state["user"]]

    with st.form("goal_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            goal_name = st.text_input("Goal Name")
        with col2:
            goal_target = st.number_input("Target Amount", min_value=0.0, step=100.0)
        with col3:
            goal_deadline = st.date_input("Deadline", datetime.now() + timedelta(days=90))

        if st.form_submit_button("➕ Add Goal", use_container_width=True, type="primary"):
            goals.append({
                "id": get_next_id(goals),
                "user": st.session_state["user"],
                "name": goal_name,
                "target": goal_target,
                "saved": 0.0,
                "deadline": goal_deadline.isoformat(),
                "completed": False,
                "created": datetime.now().isoformat()
            })
            save_data("goals", goals)
            st.success(f"Goal created: {goal_name}")
            st.rerun()

    st.divider()

    for goal in user_goals:
        target = float(goal["target"])
        saved = float(goal.get("saved", 0))
        pct = min(100, (saved / target * 100)) if target > 0 else 0

        col1, col2, col3 = st.columns([3, 4, 2])
        with col1:
            st.write(f"**{goal['name']}**")
            st.caption(f"Deadline: {goal['deadline'][:10]}")
        with col2:
            st.markdown(f"""
                <div style="background:#333; height:20px; border-radius:10px; overflow:hidden;">
                    <div style="background:{'#00ff88' if pct >= 100 else '#00d4ff'}; width:{pct}%; height:100%;"></div>
                </div>
                <p style="text-align:center; margin:0;">{format_currency(saved)} / {format_currency(target)} ({pct:.1f}%)</p>
            """, unsafe_allow_html=True)
        with col3:
            add_save = st.number_input("Add", min_value=0.0, step=10.0, key=f"save_{goal['id']}")
            if st.button("💰 Save", key=f"btn_save_{goal['id']}"):
                goal["saved"] = saved + add_save
                if goal["saved"] >= target:
                    goal["completed"] = True
                    st.balloons()
                save_data("goals", goals)
                st.rerun()
            if st.button("🗑️", key=f"del_goal_{goal['id']}"):
                goals.remove(goal)
                save_data("goals", goals)
                st.rerun()

        if goal.get("completed"):
            st.success("🎉 Goal completed!")
        st.divider()

# ============== EXPORT/IMPORT ==============
def export_import():
    st.markdown("<h1 style='text-align:center;'>📤 Export / 📥 Import</h1>", unsafe_allow_html=True)

    expenses = get_user_expenses(st.session_state["user"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Export Data")

        # CSV Export
        if expenses:
            df = pd.DataFrame(expenses)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # JSON Export
        all_data = {
            "expenses": expenses,
            "budgets": [b for b in load_data("budgets") if b.get("user") == st.session_state["user"]],
            "goals": [g for g in load_data("goals") if g.get("user") == st.session_state["user"]],
            "recurring": [r for r in load_data("recurring") if r.get("user") == st.session_state["user"]],
            "exported": datetime.now().isoformat()
        }
        json_str = json.dumps(all_data, indent=2, default=str)
        st.download_button(
            label="📦 Download JSON Backup",
            data=json_str,
            file_name=f"noor_expense_backup_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

    with col2:
        st.subheader("📥 Import Data")

        uploaded = st.file_uploader("Upload JSON Backup", type=["json"])
        if uploaded:
            try:
                data = json.load(uploaded)
                if st.button("🔄 Restore Data", use_container_width=True, type="primary"):
                    for key in ["expenses", "budgets", "goals", "recurring"]:
                        if key in data:
                            existing = load_data(key)
                            for item in data[key]:
                                item["user"] = st.session_state["user"]
                                existing.append(item)
                            save_data(key, existing)
                    st.success("Data restored successfully!")
            except Exception as e:
                st.error(f"Error importing: {e}")

        uploaded_csv = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_csv:
            try:
                df = pd.read_csv(uploaded_csv)
                if st.button("📊 Import CSV", use_container_width=True):
                    expenses = load_data("expenses")
                    for _, row in df.iterrows():
                        expenses.append({
                            "id": get_next_id(expenses),
                            "user": st.session_state["user"],
                            "date": str(row.get("date", datetime.now().date())),
                            "amount": float(row.get("amount", 0)),
                            "category": row.get("category", "📦 Other"),
                            "payment_method": row.get("payment_method", "Other"),
                            "description": row.get("description", ""),
                            "tags": row.get("tags", "").split(",") if pd.notna(row.get("tags")) else []
                        })
                    save_data("expenses", expenses)
                    st.success("CSV imported!")
            except Exception as e:
                st.error(f"Error importing CSV: {e}")

# ============== SETTINGS ==============
def settings():
    st.markdown("<h1 style='text-align:center;'>⚙️ Settings</h1>", unsafe_allow_html=True)

    settings_data = load_data("settings")
    users = load_data("users")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💱 Currency")
        new_currency = st.selectbox("Select Currency", list(CURRENCIES.keys()), 
                                   index=list(CURRENCIES.keys()).index(st.session_state.get("currency", "USD")))
        if st.button("💾 Save Currency", use_container_width=True):
            settings_data["currency"] = new_currency
            st.session_state["currency"] = new_currency
            save_data("settings", settings_data)
            if st.session_state["user"] != "guest":
                users[st.session_state["user"]]["currency"] = new_currency
                save_data("users", users)
            st.success(f"Currency set to {new_currency}")

    with col2:
        st.subheader("🔐 Account")
        if st.session_state["user"] != "guest":
            old_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")

            if st.button("🔄 Change Password", use_container_width=True):
                user_data = users.get(st.session_state["user"], {})
                if user_data.get("password") != hash_password(old_pass):
                    st.error("Current password is incorrect")
                elif new_pass != confirm_pass:
                    st.error("New passwords do not match")
                elif not new_pass:
                    st.error("Password cannot be empty")
                else:
                    users[st.session_state["user"]]["password"] = hash_password(new_pass)
                    save_data("users", users)
                    st.success("Password changed!")
        else:
            st.info("Guest users cannot change password")

    st.divider()

    st.subheader("🗑️ Data Management")
    col_del1, col_del2 = st.columns(2)
    with col_del1:
        if st.button("🗑️ Clear All My Data", use_container_width=True, type="secondary"):
            if st.checkbox("I understand this cannot be undone"):
                for key in ["expenses", "budgets", "goals", "recurring"]:
                    data = load_data(key)
                    data = [d for d in data if d.get("user") != st.session_state["user"]]
                    save_data(key, data)
                st.success("All data cleared!")
                st.rerun()
    with col_del2:
        st.info("⚠️ This will delete all your expenses, budgets, goals, and recurring items permanently.")

# ============== MAIN APP ==============
def main():
    st.set_page_config(
        page_title="Noor Expense Tracker",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        }
        .stSidebar {
            background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        }
        h1, h2, h3 {
            color: #00d4ff !important;
        }
        .stButton>button {
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,212,255,0.3);
        }
        .stMetric {
            background: rgba(0,212,255,0.1);
            border-radius: 10px;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    if "user" not in st.session_state:
        login_page()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align:center; padding: 1rem 0;">
                <h2 style="color:#00d4ff; margin:0;">💰 Noor</h2>
                <p style="color:#888; font-size:0.8rem;">Expense Tracker v2.0</p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        menu = st.radio("Navigation", [
            "🏠 Dashboard",
            "➕ Add Expense",
            "📋 View & Filter",
            "✏️ Edit / Delete",
            "🔍 Search",
            "💼 Budget Manager",
            "📊 Analytics",
            "🔁 Recurring",
            "🎯 Savings Goals",
            "📤 Export / Import",
            "⚙️ Settings"
        ], label_visibility="collapsed")

        st.divider()

        st.markdown(f"""
            <div style="text-align:center; padding: 1rem; background:rgba(0,212,255,0.1); border-radius:10px;">
                <p style="margin:0; color:#00d4ff;">👤 {st.session_state["user"]}</p>
                <p style="margin:0; color:#888; font-size:0.8rem;">💱 {st.session_state.get("currency", "USD")}</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            del st.session_state["user"]
            del st.session_state["currency"]
            st.rerun()

    # Route to pages
    if menu == "🏠 Dashboard":
        dashboard()
    elif menu == "➕ Add Expense":
        add_expense()
    elif menu == "📋 View & Filter":
        view_expenses()
    elif menu == "✏️ Edit / Delete":
        edit_expense()
    elif menu == "🔍 Search":
        search_expenses()
    elif menu == "💼 Budget Manager":
        budget_manager()
    elif menu == "📊 Analytics":
        analytics()
    elif menu == "🔁 Recurring":
        recurring_expenses()
    elif menu == "🎯 Savings Goals":
        savings_goals()
    elif menu == "📤 Export / Import":
        export_import()
    elif menu == "⚙️ Settings":
        settings()

if __name__ == "__main__":
    main()

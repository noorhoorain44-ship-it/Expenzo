#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║         💰 NOOR EXPENSE TRACKER — Linux/macOS Installer         ║
# ║              Developed by Noor Hoorain                           ║
# ║          github.com/noorhoorain44-ship-it                        ║
# ╚══════════════════════════════════════════════════════════════════╝

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

INSTALL_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/noorexpense"
VENV_DIR="$APP_DIR/venv"
SCRIPT_NAME="expense"

banner() {
  echo -e "${CYAN}"
  echo "  ╔════════════════════════════════════════════════╗"
  echo "  ║   💰  NOOR EXPENSE TRACKER  INSTALLER         ║"
  echo "  ║   Developed by Noor Hoorain                    ║"
  echo "  ║   github.com/noorhoorain44-ship-it              ║"
  echo "  ╚════════════════════════════════════════════════╝"
  echo -e "${RESET}"
}

info()    { echo -e "${CYAN}  [INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}  [OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}  [WARN]${RESET}  $*"; }
error()   { echo -e "${RED}  [ERROR]${RESET} $*"; exit 1; }

banner

# ── 1. Python check ───────────────────────────────────────────────
info "Checking Python 3.8+ ..."
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 -c "import sys; print(sys.version_info[:2])")
  success "Found Python3: $(python3 --version)"
else
  error "Python 3 not found. Install it with:\n  sudo apt install python3   OR   brew install python3"
fi

# ── 2. pip check ──────────────────────────────────────────────────
info "Checking pip ..."
if ! python3 -m pip --version &>/dev/null; then
  warn "pip not found. Attempting to install ..."
  python3 -m ensurepip --upgrade || \
    (command -v apt-get &>/dev/null && sudo apt-get install -y python3-pip) || \
    (command -v dnf    &>/dev/null && sudo dnf install -y python3-pip) || \
    error "Could not install pip. Please install manually."
fi
success "pip OK"

# ── 3. Create directories ─────────────────────────────────────────
info "Creating application directories ..."
mkdir -p "$APP_DIR" "$INSTALL_DIR"
success "Directories created: $APP_DIR"

# ── 4. Virtual environment ────────────────────────────────────────
info "Creating virtual environment ..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
success "Virtual environment ready: $VENV_DIR"

# ── 5. Install dependencies ───────────────────────────────────────
info "Installing dependencies ..."
pip install --upgrade pip --quiet
pip install colorama rich --quiet
success "Dependencies installed (colorama, rich)"

# ── 6. Copy script ────────────────────────────────────────────────
info "Installing expensetracker.py ..."
SCRIPT_SRC="$(dirname "$0")/expensetracker.py"
if [[ ! -f "$SCRIPT_SRC" ]]; then
  error "expensetracker.py not found in the same directory as install.sh"
fi
cp "$SCRIPT_SRC" "$APP_DIR/expensetracker.py"
chmod +x "$APP_DIR/expensetracker.py"
success "Script installed to $APP_DIR"

# ── 7. Create launcher ────────────────────────────────────────────
info "Creating launcher command '$SCRIPT_NAME' ..."
cat > "$INSTALL_DIR/$SCRIPT_NAME" << EOF
#!/usr/bin/env bash
source "$VENV_DIR/bin/activate"
python3 "$APP_DIR/expensetracker.py" "\$@"
EOF
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
success "Launcher created: $INSTALL_DIR/$SCRIPT_NAME"

# ── 8. PATH check ─────────────────────────────────────────────────
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  warn "$INSTALL_DIR is not in your PATH."
  echo -e "${YELLOW}  Add this line to your ~/.bashrc or ~/.zshrc:${RESET}"
  echo -e "  ${BOLD}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
  echo ""
  # Auto-append for bash
  SHELL_RC="$HOME/.bashrc"
  [[ "$SHELL" == *zsh* ]] && SHELL_RC="$HOME/.zshrc"
  echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
  info "Auto-appended to $SHELL_RC — restart your terminal or run: source $SHELL_RC"
fi

# ── 9. Desktop shortcut (Linux only) ─────────────────────────────
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  DESKTOP_DIR="$HOME/.local/share/applications"
  mkdir -p "$DESKTOP_DIR"
  cat > "$DESKTOP_DIR/noor-expense-tracker.desktop" << EOF
[Desktop Entry]
Version=2.0
Type=Application
Name=Noor Expense Tracker
Comment=Advanced CLI Expense Tracker by Noor Hoorain
Exec=bash -c 'source $VENV_DIR/bin/activate && python3 $APP_DIR/expensetracker.py'
Icon=utilities-finance
Terminal=true
Categories=Finance;Utility;
EOF
  success "Desktop shortcut created"
fi

# ── Done ──────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}  ✅  Installation complete!${RESET}"
echo ""
echo -e "${CYAN}  ▶  Run the app:${RESET}  ${BOLD}expense${RESET}"
echo -e "${CYAN}  ▶  Or directly:${RESET} ${BOLD}python3 $APP_DIR/expensetracker.py${RESET}"
echo ""
echo -e "${YELLOW}  Developed by Noor Hoorain — github.com/noorhoorain44-ship-it${RESET}"
echo ""

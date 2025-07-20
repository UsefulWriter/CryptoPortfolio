# PySide6 Constants and Styles for Crypto Portfolio Tracker

# Window settings
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 600

# Colors (using Qt-compatible hex format)
COLOR_PRIMARY = "#76d4d6"  # Vibrant Blue for accents and buttons
COLOR_PRIMARY_ACTIVE = "#0056b3"  # Darker blue for button hover
COLOR_TEXT_DARK = "#212529"  # Dark gray for body text
COLOR_BACKGROUND_LIGHT = "#F8F9FA"  # Light gray/white for backgrounds
COLOR_SUCCESS_GREEN = "#28A745"  # Green for BTC or positive elements
COLOR_NEUTRAL_GRAY = "#6C757D"  # Medium gray for ETH or neutral
COLOR_WARNING_RED = "#DC3545"  # Red for XRP or warnings
COLOR_BORDER = "#DEE2E6"  # Light border color
COLOR_HOVER = "#E9ECEF"  # Hover effect

# Chart colors
CHART_COLORS = [COLOR_SUCCESS_GREEN, COLOR_NEUTRAL_GRAY, COLOR_WARNING_RED]

# Font settings
FONT_FAMILY = "Arial"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 12
FONT_SIZE_HEADING = 14

# Spacing and dimensions
MARGIN_SMALL = 5
MARGIN_NORMAL = 10
MARGIN_LARGE = 20
BUTTON_HEIGHT = 32
INPUT_HEIGHT = 28
LIST_MIN_HEIGHT = 200
PLOT_WIDTH = 600
PLOT_HEIGHT = 400

# Widget sizes
LABEL_MIN_WIDTH = 80
INPUT_MIN_WIDTH = 100
BUTTON_MIN_WIDTH = 120

# Constants for defaults
DEFAULT_ENTRY_VALUE = "0"
LAST_FETCHED_DEFAULT = "Last Fetched: Never"

# File paths
HOLDINGS_FILE_PATH = "crypto_holdings.json"
SCENARIOS_FILE_PATH = "future_scenarios.json"

# API endpoints
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"

# Qt StyleSheet for modern appearance
APP_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLOR_BACKGROUND_LIGHT};
}}

QWidget {{
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_NORMAL}px;
    color: {COLOR_TEXT_DARK};
}}

QPushButton {{
    background-color: {COLOR_PRIMARY};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    min-height: {BUTTON_HEIGHT - 16}px;
    min-width: {BUTTON_MIN_WIDTH}px;
}}

QPushButton:hover {{
    background-color: {COLOR_PRIMARY_ACTIVE};
}}

QPushButton:pressed {{
    background-color: {COLOR_PRIMARY_ACTIVE};
    padding: 9px 15px 7px 17px;
}}

QLineEdit {{
    border: 2px solid {COLOR_BORDER};
    border-radius: 4px;
    padding: 4px 8px;
    background-color: white;
    min-height: {INPUT_HEIGHT - 8}px;
    min-width: {INPUT_MIN_WIDTH}px;
}}

QLineEdit:focus {{
    border-color: {COLOR_PRIMARY};
}}

QLabel {{
    color: {COLOR_TEXT_DARK};
    min-width: {LABEL_MIN_WIDTH}px;
}}

QLabel[heading="true"] {{
    font-size: {FONT_SIZE_HEADING}px;
    font-weight: bold;
    color: {COLOR_PRIMARY};
    margin: {MARGIN_NORMAL}px 0px;
}}

QTextEdit {{
    border: 2px solid {COLOR_BORDER};
    border-radius: 4px;
    background-color: white;
    padding: 8px;
}}

QListWidget {{
    border: 2px solid {COLOR_BORDER};
    border-radius: 4px;
    background-color: white;
    min-height: {LIST_MIN_HEIGHT}px;
    padding: 4px;
}}

QListWidget::item {{
    padding: 4px 8px;
    border-bottom: 1px solid {COLOR_BORDER};
}}

QListWidget::item:selected {{
    background-color: {COLOR_PRIMARY};
    color: white;
}}

QListWidget::item:hover {{
    background-color: {COLOR_HOVER};
}}

QScrollArea {{
    border: none;
    background-color: {COLOR_BACKGROUND_LIGHT};
}}

QFrame {{
    background-color: {COLOR_BACKGROUND_LIGHT};
}}

QGroupBox {{
    font-weight: bold;
    border: 2px solid {COLOR_BORDER};
    border-radius: 4px;
    margin: {MARGIN_NORMAL}px 0px;
    padding-top: {MARGIN_NORMAL}px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: {MARGIN_NORMAL}px;
    padding: 0px 5px 0px 5px;
    color: {COLOR_PRIMARY};
}}
"""
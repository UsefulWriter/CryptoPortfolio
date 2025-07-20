# Constants for colors
COLOR_PRIMARY = '#76d4d6'  # Vibrant Blue for accents and buttons
COLOR_PRIMARY_ACTIVE = '#0056b3'  # Darker blue for button hover
COLOR_TEXT_DARK = '#212529'  # Dark gray for body text
COLOR_BACKGROUND_LIGHT = '#F8F9FA'  # Light gray/white for backgrounds
COLOR_SUCCESS_GREEN = '#28A745'  # Green for BTC or positive elements
COLOR_NEUTRAL_GRAY = '#6C757D'  # Medium gray for ETH or neutral
COLOR_WARNING_RED = '#DC3545'  # Red for XRP or warnings

# Constants for UI dimensions and styles
WINDOW_GEOMETRY = "1600x800"
TEXT_WIDGET_HEIGHT = 10
TEXT_WIDGET_WIDTH = 80
LISTBOX_HEIGHT = 10
LISTBOX_WIDTH = 100
FIGURE_SIZE_LARGE = (8, 6)
FIGURE_SIZE_MEDIUM = (6, 6)
FONT_BODY = ('Arial', 10)
FONT_HEADING = ('Arial', 12, 'bold')
FONT_BUTTON = ('Arial', 10, 'bold')
BUTTON_PADDING = 10

# Constants for defaults
DEFAULT_ENTRY_VALUE = "0"
LAST_FETCHED_DEFAULT = "Last Fetched: Never"

# File paths
HOLDINGS_FILE_PATH = "crypto_holdings.json"
SCENARIOS_FILE_PATH = "future_scenarios.json"

# API endpoints
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
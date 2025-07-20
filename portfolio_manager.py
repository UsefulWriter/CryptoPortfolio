import json
import os
from tkinter import messagebox
from constants import HOLDINGS_FILE_PATH, SCENARIOS_FILE_PATH, DEFAULT_ENTRY_VALUE


class PortfolioManager:
    def __init__(self):
        self.holdings = {"btc": 0, "eth": 0, "xrp": 0}
        self.future_prices = []
        self.scenarios = []

    def load_holdings(self):
        if os.path.exists(HOLDINGS_FILE_PATH):
            try:
                with open(HOLDINGS_FILE_PATH, "r") as f:
                    data = json.load(f)
                self.holdings = {
                    "btc": data.get("btc", 0),
                    "eth": data.get("eth", 0),
                    "xrp": data.get("xrp", 0)
                }
                return True, "Holdings loaded from file."
            except Exception as e:
                return False, f"Failed to load holdings: {e}"
        else:
            return False, "No holdings file found."

    def save_holdings(self, btc_amount, eth_amount, xrp_amount):
        try:
            self.holdings = {
                "btc": float(btc_amount),
                "eth": float(eth_amount),
                "xrp": float(xrp_amount)
            }
            with open(HOLDINGS_FILE_PATH, "w") as f:
                json.dump(self.holdings, f)
            return True, "Holdings saved to file."
        except ValueError:
            return False, "Invalid input for holdings amounts."
        except Exception as e:
            return False, f"Failed to save holdings: {e}"

    def load_future_prices(self):
        if os.path.exists(SCENARIOS_FILE_PATH):
            try:
                with open(SCENARIOS_FILE_PATH, "r") as f:
                    data = json.load(f)
                self.future_prices = [tuple(d) for d in data]
                return True
            except Exception as e:
                return False
        return False

    def save_future_prices(self):
        try:
            data = [list(p) for p in self.future_prices]
            with open(SCENARIOS_FILE_PATH, "w") as f:
                json.dump(data, f)
            return True, "Scenarios saved to file."
        except Exception as e:
            return False, f"Failed to save scenarios: {e}"

    def add_future_scenario(self, btc_price, eth_price, xrp_price):
        try:
            future_btc_price = float(btc_price)
            future_eth_price = float(eth_price)
            future_xrp_price = float(xrp_price)
            self.future_prices.append((future_btc_price, future_eth_price, future_xrp_price))
            return True
        except ValueError:
            return False

    def calculate_scenarios(self, current_prices):
        if not current_prices:
            return

        try:
            btc_owned = self.holdings["btc"]
            eth_owned = self.holdings["eth"]
            xrp_owned = self.holdings["xrp"]

            current_btc_worth = btc_owned * current_prices["btc"]
            current_eth_worth = eth_owned * current_prices["eth"]
            current_xrp_worth = xrp_owned * current_prices["xrp"]
            current_total_worth = current_btc_worth + current_eth_worth + current_xrp_worth

            self.scenarios = [(current_total_worth, current_btc_worth, current_eth_worth, current_xrp_worth)]

            for future_btc_price, future_eth_price, future_xrp_price in self.future_prices:
                future_btc_worth = btc_owned * future_btc_price
                future_eth_worth = eth_owned * future_eth_price
                future_xrp_worth = xrp_owned * future_xrp_price
                future_total_worth = future_btc_worth + future_eth_worth + future_xrp_worth
                self.scenarios.append((future_total_worth, future_btc_worth, future_eth_worth, future_xrp_worth))

            return True
        except Exception:
            return False

    def get_current_worth_text(self, current_prices):
        if not current_prices:
            return "Current Worth: Not fetched yet"
        
        btc_owned = self.holdings["btc"]
        eth_owned = self.holdings["eth"]
        xrp_owned = self.holdings["xrp"]

        current_btc_worth = btc_owned * current_prices["btc"]
        current_eth_worth = eth_owned * current_prices["eth"]
        current_xrp_worth = xrp_owned * current_prices["xrp"]
        current_total_worth = current_btc_worth + current_eth_worth + current_xrp_worth

        return f"Current Worth: BTC ${current_btc_worth:.2f}, ETH ${current_eth_worth:.2f}, XRP ${current_xrp_worth:.2f}, Total ${current_total_worth:.2f}"

    def get_scenarios_display_data(self, current_prices):
        scenarios_display = []
        for i, (total, btc_worth, eth_worth, xrp_worth) in enumerate(self.scenarios):
            if i == 0:
                btc_price = current_prices.get('btc', 0)
                eth_price = current_prices.get('eth', 0)
                xrp_price = current_prices.get('xrp', 0)
                display_str = f"Current: Prices (BTC ${btc_price:.2f}, ETH ${eth_price:.2f}, XRP ${xrp_price:.4f}) | Worth: Total ${total:.2f}, BTC ${btc_worth:.2f}, ETH ${eth_worth:.2f}, XRP ${xrp_worth:.2f}"
            else:
                future_btc_price, future_eth_price, future_xrp_price = self.future_prices[i - 1]
                display_str = f"Future {i}: Prices (BTC ${future_btc_price:.2f}, ETH ${future_eth_price:.2f}, XRP ${future_xrp_price:.4f}) | Worth: Total ${total:.2f}, BTC ${btc_worth:.2f}, ETH ${eth_worth:.2f}, XRP ${xrp_worth:.2f}"
            scenarios_display.append(display_str)
        return scenarios_display

    def reorder_future_prices(self, from_index, to_index):
        if from_index < 1 or to_index < 1:
            return False
        
        fp_from_index = from_index - 1
        fp_to_index = to_index - 1
        
        if 0 <= fp_from_index < len(self.future_prices) and 0 <= fp_to_index < len(self.future_prices):
            fp_item = self.future_prices.pop(fp_from_index)
            self.future_prices.insert(fp_to_index, fp_item)
            return True
        return False

    def get_portfolio_allocation_data(self, current_prices):
        if not current_prices:
            return None
        
        btc_owned = self.holdings["btc"]
        eth_owned = self.holdings["eth"]
        xrp_owned = self.holdings["xrp"]

        current_btc_worth = btc_owned * current_prices["btc"]
        current_eth_worth = eth_owned * current_prices["eth"]
        current_xrp_worth = xrp_owned * current_prices["xrp"]
        total_worth = current_btc_worth + current_eth_worth + current_xrp_worth

        if total_worth == 0:
            return None

        return {
            "labels": ['BTC', 'ETH', 'XRP'],
            "sizes": [current_btc_worth, current_eth_worth, current_xrp_worth],
            "total": total_worth
        }
import urllib.request
import json
import ssl
import datetime
from constants_pyside6 import COINGECKO_API_URL


class CryptoAPI:
    def __init__(self):
        self.current_prices = {}
        self.market_info = {}
        self.last_fetched = None

    def fetch_prices(self):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(COINGECKO_API_URL, context=ctx) as response:
                data = json.loads(response.read().decode())

            self.current_prices = {
                "btc": data['bitcoin']['usd'],
                "eth": data['ethereum']['usd'],
                "xrp": data['ripple']['usd']
            }

            self.market_info = {
                "btc": {
                    "market_cap": data['bitcoin']['usd_market_cap'],
                    "24h_vol": data['bitcoin']['usd_24h_vol'],
                    "24h_change": data['bitcoin']['usd_24h_change']
                },
                "eth": {
                    "market_cap": data['ethereum']['usd_market_cap'],
                    "24h_vol": data['ethereum']['usd_24h_vol'],
                    "24h_change": data['ethereum']['usd_24h_change']
                },
                "xrp": {
                    "market_cap": data['ripple']['usd_market_cap'],
                    "24h_vol": data['ripple']['usd_24h_vol'],
                    "24h_change": data['ripple']['usd_24h_change']
                }
            }

            self.last_fetched = datetime.datetime.now()
            return True

        except Exception as e:
            raise e

    def get_current_prices(self):
        return self.current_prices

    def get_market_info(self):
        return self.market_info

    def get_last_fetched(self):
        return self.last_fetched

    def format_market_info(self):
        if not self.current_prices or not self.market_info:
            return "No market data available"
        
        btc_info = f"BTC: Price ${self.current_prices['btc']:.2f}, Market Cap ${self.market_info['btc']['market_cap']:,.2f}, 24h Vol ${self.market_info['btc']['24h_vol']:,.2f}, 24h Change {self.market_info['btc']['24h_change']:.2f}%\n"
        eth_info = f"ETH: Price ${self.current_prices['eth']:.2f}, Market Cap ${self.market_info['eth']['market_cap']:,.2f}, 24h Vol ${self.market_info['eth']['24h_vol']:,.2f}, 24h Change {self.market_info['eth']['24h_change']:.2f}%\n"
        xrp_info = f"XRP: Price ${self.current_prices['xrp']:.4f}, Market Cap ${self.market_info['xrp']['market_cap']:,.2f}, 24h Vol ${self.market_info['xrp']['24h_vol']:,.2f}, 24h Change {self.market_info['xrp']['24h_change']:.2f}%"
        
        return btc_info + eth_info + xrp_info
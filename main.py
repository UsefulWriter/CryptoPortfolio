import tkinter as tk
from tkinter import messagebox, ttk

from constants import *
from crypto_api import CryptoAPI
from portfolio_manager import PortfolioManager
from ui_components import PlotManager, DragDropListbox, UIStyleManager


class CryptoPortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Portfolio Tracker")
        self.geometry(WINDOW_GEOMETRY)

        # Initialize components
        self.crypto_api = CryptoAPI()
        self.portfolio_manager = PortfolioManager()
        
        # ttk Style
        self.style = ttk.Style(self)
        UIStyleManager.configure_styles(self.style)

        # Create canvas and scrollbar for scrolling the entire app
        self.canvas = tk.Canvas(self, bg=COLOR_BACKGROUND_LIGHT)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame to hold all widgets
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update scroll region when inner frame changes size
        self.inner_frame.bind("<Configure>", self.on_frame_configure)


        # Variables for owned amounts
        self.btc_owned_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)
        self.eth_owned_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)
        self.xrp_owned_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)

        # Variables for future prices
        self.future_btc_price_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)
        self.future_eth_price_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)
        self.future_xrp_price_var = tk.StringVar(value=DEFAULT_ENTRY_VALUE)

        # Frames for layout
        self.left_frame = ttk.Frame(self.inner_frame)
        self.left_frame.grid(row=0, column=0, sticky="n")

        # Display areas
        self.current_worth_label = ttk.Label(self.left_frame, text="Current Worth: Not fetched yet")
        self.market_info_text = tk.Text(self.left_frame, height=TEXT_WIDGET_HEIGHT, width=TEXT_WIDGET_WIDTH, bg='white',
                                        fg=COLOR_TEXT_DARK)
        self.scenarios_listbox = tk.Listbox(self.left_frame, height=LISTBOX_HEIGHT, width=LISTBOX_WIDTH, bg='white',
                                            fg=COLOR_TEXT_DARK)  # Increased width

        # Last fetched label
        self.last_fetched_label = ttk.Label(self.left_frame, text=LAST_FETCHED_DEFAULT)

        # Plot frame on the right
        self.plot_frame = ttk.Frame(self.inner_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=20)
        
        # Initialize plot manager
        self.plot_manager = PlotManager(self.plot_frame)

        self.create_widgets()
        self.portfolio_manager.load_future_prices()
        self.load_holdings()
        self.auto_fetch_prices()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_widgets(self):
        row = 0
        # Holdings section
        ttk.Label(self.left_frame, text="Owned Amounts:", style='Heading.TLabel').grid(row=row, column=0, sticky="w")
        row += 1
        ttk.Label(self.left_frame, text="BTC:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.btc_owned_var).grid(row=row, column=1)
        row += 1
        ttk.Label(self.left_frame, text="ETH:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.eth_owned_var).grid(row=row, column=1)
        row += 1
        ttk.Label(self.left_frame, text="XRP:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.xrp_owned_var).grid(row=row, column=1)
        row += 1

        ttk.Button(self.left_frame, text="Save Holdings", command=self.save_holdings).grid(row=row, column=0)
        ttk.Button(self.left_frame, text="Load Holdings", command=self.load_holdings).grid(row=row, column=1)
        ttk.Button(self.left_frame, text="Fetch Current Prices", command=self.fetch_prices).grid(row=row, column=2)
        row += 1

        # Last fetched label
        self.last_fetched_label.grid(row=row, column=0, columnspan=3, sticky="w")
        row += 1

        # Current worth display
        self.current_worth_label.grid(row=row, column=0, columnspan=3, sticky="w")
        row += 1

        # Market info
        ttk.Label(self.left_frame, text="Market Info:", style='Heading.TLabel').grid(row=row, column=0, sticky="w")
        row += 1
        self.market_info_text.grid(row=row, column=0, columnspan=3)
        row += 1

        # Future scenarios section
        ttk.Label(self.left_frame, text="Future Scenario Prices:", style='Heading.TLabel').grid(row=row, column=0,
                                                                                                sticky="w")
        row += 1
        ttk.Label(self.left_frame, text="BTC:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.future_btc_price_var).grid(row=row, column=1)
        row += 1
        ttk.Label(self.left_frame, text="ETH:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.future_eth_price_var).grid(row=row, column=1)
        row += 1
        ttk.Label(self.left_frame, text="XRP:").grid(row=row, column=0)
        ttk.Entry(self.left_frame, textvariable=self.future_xrp_price_var).grid(row=row, column=1)
        row += 1

        ttk.Button(self.left_frame, text="Add Future Scenario", command=self.add_scenario).grid(row=row, column=0,
                                                                                                columnspan=1)
        ttk.Button(self.left_frame, text="Save Scenarios", command=self.save_scenarios).grid(row=row, column=1)
        ttk.Button(self.left_frame, text="Load Scenarios", command=self.load_scenarios).grid(row=row, column=2)
        row += 1

        # Scenarios list
        ttk.Label(self.left_frame, text="Scenarios:", style='Heading.TLabel').grid(row=row, column=0, sticky="w")
        row += 1
        self.scenarios_listbox.grid(row=row, column=0, columnspan=3)
        self.dnd_listbox = DragDropListbox(self.scenarios_listbox, self.reorder_scenarios)
        row += 1

        # Plot buttons
        ttk.Button(self.left_frame, text="Plot Scenarios", command=self.plot_scenarios).grid(row=row, column=0,
                                                                                                   columnspan=3)
        row += 1
        ttk.Button(self.left_frame, text="Plot Portfolio Allocation", command=self.plot_portfolio_allocation).grid(
            row=row, column=0, columnspan=3)
        row += 1

        # Graph display label in plot_frame
        ttk.Label(self.plot_frame, text="Graph Display Area:", style='Heading.TLabel').pack()

    def reorder_scenarios(self, from_index, to_index):
        if self.portfolio_manager.reorder_future_prices(from_index, to_index):
            self.recalculate_scenarios()


    def load_holdings(self):
        success, message = self.portfolio_manager.load_holdings()
        if success:
            self.btc_owned_var.set(str(self.portfolio_manager.holdings["btc"]))
            self.eth_owned_var.set(str(self.portfolio_manager.holdings["eth"]))
            self.xrp_owned_var.set(str(self.portfolio_manager.holdings["xrp"]))
            messagebox.showinfo("Success", message)
            current_prices = self.crypto_api.get_current_prices()
            if current_prices:
                self.recalculate_scenarios()
        else:
            messagebox.showinfo("Info", message)

    def save_holdings(self):
        success, message = self.portfolio_manager.save_holdings(
            self.btc_owned_var.get(),
            self.eth_owned_var.get(),
            self.xrp_owned_var.get()
        )
        if success:
            messagebox.showinfo("Success", message)
            current_prices = self.crypto_api.get_current_prices()
            if current_prices:
                self.recalculate_scenarios()
        else:
            messagebox.showerror("Error", message)

    def auto_fetch_prices(self):
        try:
            self.fetch_prices()
        except Exception as e:
            messagebox.showinfo("Info", f"Auto-fetch failed: {e}. Use the 'Fetch Current Prices' button to retry.")

    def fetch_prices(self):
        try:
            if self.crypto_api.fetch_prices():
                self.market_info_text.delete(1.0, tk.END)
                self.market_info_text.insert(tk.END, self.crypto_api.format_market_info())
                
                last_fetched = self.crypto_api.get_last_fetched()
                if last_fetched:
                    self.last_fetched_label.config(
                        text=f"Last Fetched: {last_fetched.strftime('%Y-%m-%d %H:%M:%S')}")
                
                self.recalculate_scenarios()
        except Exception as e:
            raise e

    def recalculate_scenarios(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            return

        # Update portfolio manager with current holdings
        self.portfolio_manager.save_holdings(
            self.btc_owned_var.get(),
            self.eth_owned_var.get(),
            self.xrp_owned_var.get()
        )
        
        if self.portfolio_manager.calculate_scenarios(current_prices):
            self.current_worth_label.config(
                text=self.portfolio_manager.get_current_worth_text(current_prices))
            self.update_scenarios_listbox()
        else:
            messagebox.showerror("Error", "Invalid holdings amounts.")

    def add_scenario(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            messagebox.showerror("Error", "Fetch current prices first.")
            return

        if self.portfolio_manager.add_future_scenario(
            self.future_btc_price_var.get(),
            self.future_eth_price_var.get(),
            self.future_xrp_price_var.get()
        ):
            self.recalculate_scenarios()
            # Clear future inputs
            self.future_btc_price_var.set(DEFAULT_ENTRY_VALUE)
            self.future_eth_price_var.set(DEFAULT_ENTRY_VALUE)
            self.future_xrp_price_var.set(DEFAULT_ENTRY_VALUE)
        else:
            messagebox.showerror("Error", "Invalid input for future prices.")

    def save_scenarios(self):
        success, message = self.portfolio_manager.save_future_prices()
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def load_scenarios(self):
        if self.portfolio_manager.load_future_prices():
            self.recalculate_scenarios()
            messagebox.showinfo("Success", "Scenarios loaded from file.")
        else:
            messagebox.showinfo("Info", "No scenarios file found.")

    def update_scenarios_listbox(self):
        self.scenarios_listbox.delete(0, tk.END)
        current_prices = self.crypto_api.get_current_prices()
        scenarios_display = self.portfolio_manager.get_scenarios_display_data(current_prices)
        for display_str in scenarios_display:
            self.scenarios_listbox.insert(tk.END, display_str)

    def plot_scenarios(self):
        self.plot_manager.embed_scenarios_plot(self.portfolio_manager.scenarios)

    def plot_portfolio_allocation(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            messagebox.showerror("Error", "Fetch current prices first.")
            return
            
        allocation_data = self.portfolio_manager.get_portfolio_allocation_data(current_prices)
        if allocation_data:
            self.plot_manager.embed_portfolio_allocation(allocation_data)
        else:
            messagebox.showerror("Error", "Invalid holdings amounts.")


if __name__ == "__main__":
    app = CryptoPortfolioApp()
    app.mainloop()
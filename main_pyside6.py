import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                              QVBoxLayout, QSplitter, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from constants_pyside6 import *
from crypto_api import CryptoAPI
from portfolio_manager import PortfolioManager
from ui_components_pyside6 import (HoldingsWidget, ScenariosWidget, InfoDisplayWidget, 
                                  PlotControlWidget, PlotWidget, DragDropListWidget)


class CryptoPortfolioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Portfolio Tracker")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize components
        self.crypto_api = CryptoAPI()
        self.portfolio_manager = PortfolioManager()
        
        # Setup UI
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()
        
        # Load data
        self.load_initial_data()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(MARGIN_NORMAL, MARGIN_NORMAL, MARGIN_NORMAL, MARGIN_NORMAL)
        
        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (plots)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([800, 800])
        
    def create_left_panel(self):
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(MARGIN_NORMAL)
        
        # Holdings widget
        self.holdings_widget = HoldingsWidget()
        left_layout.addWidget(self.holdings_widget)
        
        # Info display widget
        self.info_widget = InfoDisplayWidget()
        left_layout.addWidget(self.info_widget)
        
        # Scenarios widget
        self.scenarios_widget = ScenariosWidget()
        left_layout.addWidget(self.scenarios_widget)
        
        # Scenarios list
        scenarios_group = QGroupBox("Scenarios List")
        scenarios_layout = QVBoxLayout(scenarios_group)
        
        self.scenarios_list = DragDropListWidget()
        scenarios_layout.addWidget(self.scenarios_list)
        
        left_layout.addWidget(scenarios_group)
        
        # Plot controls
        self.plot_controls = PlotControlWidget()
        left_layout.addWidget(self.plot_controls)
        
        # Add stretch to push everything to top
        left_layout.addStretch()
        
        return left_widget
        
    def create_right_panel(self):
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Plot area title
        plot_group = QGroupBox("Charts and Visualizations")
        plot_layout = QVBoxLayout(plot_group)
        
        self.plot_widget = PlotWidget()
        plot_layout.addWidget(self.plot_widget)
        
        right_layout.addWidget(plot_group)
        
        return right_widget
        
    def apply_styles(self):
        self.setStyleSheet(APP_STYLESHEET)
        
        # Set font for the application
        font = QFont(FONT_FAMILY, FONT_SIZE_NORMAL)
        self.setFont(font)
        
    def connect_signals(self):
        # Holdings widget signals
        self.holdings_widget.holdings_changed.connect(self.on_holdings_changed)
        self.holdings_widget.save_requested.connect(self.save_holdings)
        self.holdings_widget.load_requested.connect(self.manual_load_holdings)
        self.holdings_widget.fetch_prices_requested.connect(self.fetch_prices)
        
        # Scenarios widget signals
        self.scenarios_widget.scenario_added.connect(self.add_scenario)
        self.scenarios_widget.scenarios_saved.connect(self.save_scenarios)
        self.scenarios_widget.scenarios_loaded.connect(self.load_scenarios)
        
        # Plot controls signals
        self.plot_controls.plot_scenarios_requested.connect(self.plot_scenarios)
        self.plot_controls.plot_allocation_requested.connect(self.plot_allocation)
        
        # List reordering signal
        self.scenarios_list.items_reordered.connect(self.reorder_scenarios)
        
    def load_initial_data(self):
        # Load saved data
        self.portfolio_manager.load_future_prices()
        self.load_holdings()
        
        # Auto-fetch prices
        QTimer.singleShot(100, self.auto_fetch_prices)
        
    def auto_fetch_prices(self):
        try:
            self.fetch_prices()
        except Exception as e:
            QMessageBox.information(self, "Info", 
                                   f"Auto-fetch failed: {e}. Use the 'Fetch Current Prices' button to retry.")
    
    def fetch_prices(self):
        try:
            if self.crypto_api.fetch_prices():
                # Update market info display
                self.info_widget.update_market_info(self.crypto_api.format_market_info())
                
                # Update last fetched timestamp
                last_fetched = self.crypto_api.get_last_fetched()
                if last_fetched:
                    self.info_widget.update_last_fetched(
                        f"Last Fetched: {last_fetched.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Recalculate scenarios
                self.recalculate_scenarios()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch prices: {e}")
    
    def on_holdings_changed(self):
        # Recalculate when holdings change
        current_prices = self.crypto_api.get_current_prices()
        if current_prices:
            self.recalculate_scenarios()
    
    def save_holdings(self):
        holdings = self.holdings_widget.get_holdings()
        success, message = self.portfolio_manager.save_holdings(
            holdings['btc'], holdings['eth'], holdings['xrp'])
        
        if success:
            QMessageBox.information(self, "Success", message)
            current_prices = self.crypto_api.get_current_prices()
            if current_prices:
                self.recalculate_scenarios()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def load_holdings(self):
        success, message = self.portfolio_manager.load_holdings()
        if success:
            # Update UI with loaded holdings
            holdings = self.portfolio_manager.holdings
            self.holdings_widget.set_holdings(holdings['btc'], holdings['eth'], holdings['xrp'])
            # Only show success message when manually loading, not on startup
            
            current_prices = self.crypto_api.get_current_prices()
            if current_prices:
                self.recalculate_scenarios()
        # Don't show "file not found" messages on startup
    
    def manual_load_holdings(self):
        success, message = self.portfolio_manager.load_holdings()
        if success:
            # Update UI with loaded holdings
            holdings = self.portfolio_manager.holdings
            self.holdings_widget.set_holdings(holdings['btc'], holdings['eth'], holdings['xrp'])
            QMessageBox.information(self, "Success", message)
            
            current_prices = self.crypto_api.get_current_prices()
            if current_prices:
                self.recalculate_scenarios()
        else:
            QMessageBox.information(self, "Info", message)
    
    def add_scenario(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            QMessageBox.critical(self, "Error", "Fetch current prices first.")
            return
        
        future_prices = self.scenarios_widget.get_future_prices()
        if self.portfolio_manager.add_future_scenario(
            future_prices['btc'], future_prices['eth'], future_prices['xrp']):
            self.recalculate_scenarios()
        else:
            QMessageBox.critical(self, "Error", "Invalid input for future prices.")
    
    def save_scenarios(self):
        success, message = self.portfolio_manager.save_future_prices()
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def load_scenarios(self):
        if self.portfolio_manager.load_future_prices():
            self.recalculate_scenarios()
            QMessageBox.information(self, "Success", "Scenarios loaded from file.")
        else:
            QMessageBox.information(self, "Info", "No scenarios file found.")
    
    def recalculate_scenarios(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            return
        
        # Update portfolio manager with current holdings
        holdings = self.holdings_widget.get_holdings()
        self.portfolio_manager.save_holdings(holdings['btc'], holdings['eth'], holdings['xrp'])
        
        if self.portfolio_manager.calculate_scenarios(current_prices):
            # Update current worth display
            self.info_widget.update_current_worth(
                self.portfolio_manager.get_current_worth_text(current_prices))
            
            # Update scenarios list
            self.update_scenarios_list()
        else:
            QMessageBox.critical(self, "Error", "Invalid holdings amounts.")
    
    def update_scenarios_list(self):
        self.scenarios_list.clear()
        current_prices = self.crypto_api.get_current_prices()
        scenarios_display = self.portfolio_manager.get_scenarios_display_data(current_prices)
        
        for display_str in scenarios_display:
            self.scenarios_list.addItem(display_str)
    
    def reorder_scenarios(self, from_index, to_index):
        if self.portfolio_manager.reorder_future_prices(from_index, to_index):
            self.recalculate_scenarios()
    
    def plot_scenarios(self):
        self.plot_widget.plot_scenarios(self.portfolio_manager.scenarios)
    
    def plot_allocation(self):
        current_prices = self.crypto_api.get_current_prices()
        if not current_prices:
            QMessageBox.critical(self, "Error", "Fetch current prices first.")
            return
        
        allocation_data = self.portfolio_manager.get_portfolio_allocation_data(current_prices)
        if allocation_data:
            self.plot_widget.plot_portfolio_allocation(allocation_data)
        else:
            QMessageBox.critical(self, "Error", "Invalid holdings amounts.")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Crypto Portfolio Tracker")
    app.setOrganizationName("CryptoTracker")
    
    # Create and show main window
    window = CryptoPortfolioApp()
    window.show()
    
    # Start event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
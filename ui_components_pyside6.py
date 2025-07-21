from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QLabel, QPushButton, QLineEdit, QTextEdit, QListWidget, 
                              QGroupBox, QMessageBox, QScrollArea, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QObject, QMimeData
from PySide6.QtGui import QDrag, QPainter, QPixmap
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from constants_pyside6 import *


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(PLOT_WIDTH, PLOT_HEIGHT)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = None
        
    def clear_plot(self):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def plot_scenarios(self, scenarios):
        if len(scenarios) < 2:
            QMessageBox.information(self, "Info", "Add at least one future scenario to plot.")
            return

        self.clear_plot()

        times = list(range(len(scenarios)))
        totals = [s[0] for s in scenarios]
        btc_worths = [s[1] for s in scenarios]
        eth_worths = [s[2] for s in scenarios]
        xrp_worths = [s[3] for s in scenarios]

        fig = Figure(figsize=(8, 6))
        fig.patch.set_facecolor(COLOR_BACKGROUND_LIGHT)
        ax = fig.add_subplot(111)
        
        ax.plot(times, totals, marker='o', label='Total Portfolio', color=COLOR_PRIMARY, linewidth=2)
        ax.plot(times, btc_worths, marker='o', label='BTC', color=COLOR_SUCCESS_GREEN, linewidth=2)
        ax.plot(times, eth_worths, marker='o', label='ETH', color=COLOR_NEUTRAL_GRAY, linewidth=2)
        ax.plot(times, xrp_worths, marker='o', label='XRP', color=COLOR_WARNING_RED, linewidth=2)

        ax.set_xticks(times)
        ax.set_xticklabels(['Current'] + [f'Future {i}' for i in range(1, len(scenarios))])
        ax.set_xlabel('Scenarios')
        ax.set_ylabel('Worth ($)')
        ax.set_title('Portfolio Worth Over Scenarios', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)

    def plot_portfolio_allocation(self, allocation_data):
        if not allocation_data:
            QMessageBox.information(self, "Info", "No holdings to plot.")
            return

        self.clear_plot()

        labels = allocation_data["labels"]
        sizes = allocation_data["sizes"]
        colors = CHART_COLORS

        fig = Figure(figsize=(6, 6))
        fig.patch.set_facecolor(COLOR_BACKGROUND_LIGHT)
        ax = fig.add_subplot(111)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=140)
        ax.set_title('Current Portfolio Allocation', fontweight='bold')

        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)


class DragDropListWidget(QListWidget):
    items_reordered = Signal(int, int)  # from_index, to_index
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def dropEvent(self, event):
        if event.source() == self:
            from_index = self.currentRow()
            super().dropEvent(event)
            to_index = self.currentRow()
            
            # Don't allow moving the "Current" item (index 0)
            if from_index == 0 or to_index == 0:
                return
                
            if from_index != to_index:
                self.items_reordered.emit(from_index, to_index)


class HoldingsWidget(QGroupBox):
    holdings_changed = Signal()
    save_requested = Signal()
    load_requested = Signal()
    fetch_prices_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__("Portfolio Holdings", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        # Holdings inputs
        row = 0
        layout.addWidget(QLabel("BTC:"), row, 0)
        self.btc_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        self.btc_input.textChanged.connect(lambda: self.holdings_changed.emit())
        layout.addWidget(self.btc_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("ETH:"), row, 0)
        self.eth_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        self.eth_input.textChanged.connect(lambda: self.holdings_changed.emit())
        layout.addWidget(self.eth_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("XRP:"), row, 0)
        self.xrp_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        self.xrp_input.textChanged.connect(lambda: self.holdings_changed.emit())
        layout.addWidget(self.xrp_input, row, 1)
        
        # Buttons
        row += 1
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Holdings")
        save_btn.clicked.connect(self.save_requested.emit)
        button_layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load Holdings")
        load_btn.clicked.connect(self.load_requested.emit)
        button_layout.addWidget(load_btn)
        
        fetch_btn = QPushButton("Fetch Current Prices")
        fetch_btn.clicked.connect(self.fetch_prices_requested.emit)
        button_layout.addWidget(fetch_btn)
        
        layout.addLayout(button_layout, row, 0, 1, 2)
        
    def get_holdings(self):
        return {
            'btc': self.btc_input.text(),
            'eth': self.eth_input.text(),
            'xrp': self.xrp_input.text()
        }
        
    def set_holdings(self, btc, eth, xrp):
        self.btc_input.setText(str(btc))
        self.eth_input.setText(str(eth))
        self.xrp_input.setText(str(xrp))


class ScenariosWidget(QGroupBox):
    scenario_added = Signal()
    scenarios_saved = Signal()
    scenarios_loaded = Signal()
    
    def __init__(self, parent=None):
        super().__init__("Future Scenarios", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        # Future price inputs
        row = 0
        layout.addWidget(QLabel("Future BTC Price:"), row, 0)
        self.future_btc_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        layout.addWidget(self.future_btc_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Future ETH Price:"), row, 0)
        self.future_eth_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        layout.addWidget(self.future_eth_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Future XRP Price:"), row, 0)
        self.future_xrp_input = QLineEdit(DEFAULT_ENTRY_VALUE)
        layout.addWidget(self.future_xrp_input, row, 1)
        
        # Buttons
        row += 1
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Scenario")
        add_btn.clicked.connect(self._add_scenario)
        button_layout.addWidget(add_btn)
        
        save_btn = QPushButton("Save Scenarios")
        save_btn.clicked.connect(self.scenarios_saved.emit)
        button_layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load Scenarios")
        load_btn.clicked.connect(self.scenarios_loaded.emit)
        button_layout.addWidget(load_btn)
        
        layout.addLayout(button_layout, row, 0, 1, 2)
        
    def _add_scenario(self):
        self.scenario_added.emit()
        # Clear inputs after adding
        self.future_btc_input.setText(DEFAULT_ENTRY_VALUE)
        self.future_eth_input.setText(DEFAULT_ENTRY_VALUE)
        self.future_xrp_input.setText(DEFAULT_ENTRY_VALUE)
        
    def get_future_prices(self):
        return {
            'btc': self.future_btc_input.text(),
            'eth': self.future_eth_input.text(),
            'xrp': self.future_xrp_input.text()
        }


class InfoDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Current worth label
        self.current_worth_label = QLabel("Current Worth: Not fetched yet")
        self.current_worth_label.setProperty("heading", True)
        layout.addWidget(self.current_worth_label)
        
        # Last fetched label
        self.last_fetched_label = QLabel(LAST_FETCHED_DEFAULT)
        layout.addWidget(self.last_fetched_label)
        
        # Market info display
        market_group = QGroupBox("Market Information")
        market_layout = QVBoxLayout(market_group)
        market_layout.setContentsMargins(5, 5, 5, 5)  # Add some margins
        
        # Use QTextEdit with proper configuration
        self.market_info_text = QTextEdit()
        self.market_info_text.setMinimumHeight(80)
        self.market_info_text.setMaximumHeight(120)  # Reduce height to eliminate empty space
        self.market_info_text.setReadOnly(True)
        self.market_info_text.setPlainText("Click 'Fetch Current Prices' to load market data...")
        market_layout.addWidget(self.market_info_text)
        
        layout.addWidget(market_group)
        
    def update_current_worth(self, text):
        self.current_worth_label.setText(text)
        
    def update_last_fetched(self, text):
        self.last_fetched_label.setText(text)
        
    def update_market_info(self, text):
        # Using QTextEdit with proper methods - temporarily enable editing for update
        self.market_info_text.setReadOnly(False)
        self.market_info_text.clear()
        self.market_info_text.setPlainText(text)
        self.market_info_text.setReadOnly(True)
        print(f"Market info updated successfully")  # Debug


class PlotControlWidget(QWidget):
    plot_scenarios_requested = Signal()
    plot_allocation_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        scenarios_btn = QPushButton("Plot Scenarios")
        scenarios_btn.clicked.connect(self.plot_scenarios_requested.emit)
        layout.addWidget(scenarios_btn)
        
        allocation_btn = QPushButton("Plot Portfolio Allocation")
        allocation_btn.clicked.connect(self.plot_allocation_requested.emit)
        layout.addWidget(allocation_btn)
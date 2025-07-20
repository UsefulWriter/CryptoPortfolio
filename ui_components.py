import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import *


class PlotManager:
    def __init__(self, plot_frame):
        self.plot_frame = plot_frame

    def clear_plot_frame(self):
        for widget in self.plot_frame.winfo_children()[1:]:
            widget.destroy()

    def embed_scenarios_plot(self, scenarios):
        if len(scenarios) < 2:
            messagebox.showinfo("Info", "Add at least one future scenario to plot.")
            return

        self.clear_plot_frame()

        times = list(range(len(scenarios)))
        totals = [s[0] for s in scenarios]
        btc_worths = [s[1] for s in scenarios]
        eth_worths = [s[2] for s in scenarios]
        xrp_worths = [s[3] for s in scenarios]

        fig = Figure(figsize=FIGURE_SIZE_LARGE)
        fig.patch.set_facecolor(COLOR_BACKGROUND_LIGHT)
        ax = fig.add_subplot(111)
        ax.plot(times, totals, marker='o', label='Total Portfolio', color=COLOR_PRIMARY)
        ax.plot(times, btc_worths, marker='o', label='BTC', color=COLOR_SUCCESS_GREEN)
        ax.plot(times, eth_worths, marker='o', label='ETH', color=COLOR_NEUTRAL_GRAY)
        ax.plot(times, xrp_worths, marker='o', label='XRP', color=COLOR_WARNING_RED)

        ax.set_xticks(times)
        ax.set_xticklabels(['Current'] + [f'Future {i}' for i in range(1, len(scenarios))])
        ax.set_xlabel('Scenarios')
        ax.set_ylabel('Worth ($)')
        ax.set_title('Portfolio Worth Over Scenarios')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def embed_portfolio_allocation(self, allocation_data):
        if not allocation_data:
            messagebox.showinfo("Info", "No holdings to plot.")
            return

        labels = allocation_data["labels"]
        sizes = allocation_data["sizes"]
        colors = [COLOR_SUCCESS_GREEN, COLOR_NEUTRAL_GRAY, COLOR_WARNING_RED]

        self.clear_plot_frame()

        fig = Figure(figsize=FIGURE_SIZE_MEDIUM)
        fig.patch.set_facecolor(COLOR_BACKGROUND_LIGHT)
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.set_title('Current Portfolio Allocation')

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


class DragDropListbox:
    def __init__(self, listbox, reorder_callback):
        self.listbox = listbox
        self.reorder_callback = reorder_callback
        self.drag_start_index = None
        self.setup_dnd()

    def setup_dnd(self):
        self.listbox.bind("<Button-1>", self.start_drag)
        self.listbox.bind("<B1-Motion>", self.drag_motion)
        self.listbox.bind("<ButtonRelease-1>", self.drop)

    def start_drag(self, event):
        index = self.listbox.nearest(event.y)
        if index > 0:
            self.drag_start_index = index
            self.listbox.config(cursor="hand2")
        else:
            self.drag_start_index = None

    def drag_motion(self, event):
        if self.drag_start_index is not None:
            pass

    def drop(self, event):
        if self.drag_start_index is None:
            return

        new_index = self.listbox.nearest(event.y)
        if new_index <= 0 or new_index == self.drag_start_index:
            self.listbox.config(cursor="")
            self.drag_start_index = None
            return

        item = self.listbox.get(self.drag_start_index)
        self.listbox.delete(self.drag_start_index)
        self.listbox.insert(new_index, item)

        self.reorder_callback(self.drag_start_index, new_index)

        self.listbox.config(cursor="")
        self.drag_start_index = None


class UIStyleManager:
    @staticmethod
    def configure_styles(style):
        style.theme_use('clam')
        style.configure('TLabel', foreground=COLOR_TEXT_DARK, background=COLOR_BACKGROUND_LIGHT, font=FONT_BODY)
        style.configure('Heading.TLabel', foreground=COLOR_PRIMARY, font=FONT_HEADING)
        style.configure('TButton', background=COLOR_PRIMARY, foreground='white', font=FONT_BUTTON,
                         padding=BUTTON_PADDING)
        style.map('TButton', background=[('active', COLOR_PRIMARY_ACTIVE)])
        style.configure('TEntry', fieldbackground='white', foreground=COLOR_TEXT_DARK)
        style.configure('TFrame', background=COLOR_BACKGROUND_LIGHT)
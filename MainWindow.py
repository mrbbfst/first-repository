from CommonWindows import BaseWindow
import tkinter as tk
from CheckWindow import CheckWindow
from ProductWindow import ProductWindow
from PlotsWindow import PlotsWindow

class Window(BaseWindow):

    root =tk.Tk()

    def create_ui(self):
        self.button_open_create_product_dialog = tk.Button(
            text="Відкрити вікно створення товара", 
            command=self.open_product_window
            )
        self.button_open_create_check_dialog = tk.Button(
            text="Відкрити вікно створення чека", 
            command=self.open_check_window
            )
        self.button_open_plots = tk.Button(
            text="Відкрити вікно графіків",
            command=self.open_plots_window
        )
        

    def setup_layout(self):
        self.button_open_create_check_dialog.grid(row=0, column=0)
        self.button_open_create_product_dialog.grid(row=0,column=1)
        self.root.resizable(width=False, height=False)
        self.button_open_plots.grid(row=1, column=0)

    def __init__(self) -> None:
        super().__init__()
        self.create_ui()
        self.setup_layout()
        self.root.mainloop()

    def open_product_window(self):
        pw = ProductWindow(self.root)

    def open_check_window(self):
        cw = CheckWindow(self.root)

    def open_plots_window(self):
        pw = PlotsWindow(self.root)

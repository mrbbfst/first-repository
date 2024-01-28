from abc import ABC, abstractmethod
import tkinter as tk

class BaseWindow:

    @abstractmethod
    def create_ui(self):
        pass

    @abstractmethod
    def setup_layout(self):
        pass

class BaseSubWindow(BaseWindow):

    opened_windows = dict()

    def __init__(self, parent, title) -> None:
        if not title in self.opened_windows or self.opened_windows[title]==0:
            self.root = tk.Toplevel(parent)
            self.root.title(title)
            self.root.resizable(False, False)
            self.create_ui()
            self.setup_layout()
            self.setup_window()
            self.root.protocol("WM_DELETE_WINDOW", self.destroy_window)
            self.opened_windows[title] = 1
            self.root.mainloop()

    def destroy_window(self):
        self.opened_windows[self.root.title()] = 0
        self.root.destroy()
    


    @abstractmethod
    def setup_window(self):
        pass

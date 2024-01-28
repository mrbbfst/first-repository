from CommonWindows import BaseSubWindow
from PlotsBuilder import PlotsBuilder
import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from SettingsConstants import PlotType, PlotViewType

class PlotsWindow(BaseSubWindow):

    def __init__(self, parent) -> None:
        super().__init__(parent, "Графіки")


    def setup_window(self):
        self.create_plot_type_menu()
        self.builder = PlotsBuilder()
        self.bind_calendars()
        self.create_plot_view_type_menu()

    def bind_calendars(self):
        self.calendar_from.bind("<<CalendarSelected>>", self.on_calendar_from_selected)
        self.calendar_to.bind("<<CalendarSelected>>", self.on_calendar_to_selected)

    def on_calendar_from_selected(self, event):
        self.builder.add_date_from(self.calendar_from.get_date())

    def on_calendar_to_selected(self, event):
        self.builder.add_date_to(self.calendar_to.get_date())

    def create_plot_type_menu(self):
        self.plot_types = ("Графік кількості продажів", "Графік сум продажів")
        self.selected_plot_type = tk.StringVar(self.root)
        self.selected_plot_type.set(self.plot_types[0])
        self.plot_type = tk.OptionMenu(self.root, 
                                        self.selected_plot_type, 
                                       *self.plot_types)
        self.plot_type.grid(row=3, column=0)

    def create_plot_view_type_menu(self):
        self.plot_view_types = ('Графік', 'Стовпчаста діаграма', )
        self.selected_plot_view_type = tk.StringVar(self.root)
        self.selected_plot_view_type.set(self.plot_view_types[0])
        self.plot_view_type = tk.OptionMenu(self.root, 
                                        self.selected_plot_view_type, 
                                       *self.plot_view_types)
        self.plot_view_type.grid(row=4, column=0)

    def create_ui(self):
        self.calendar_from = Calendar(self.root, selectmode="day")
        self.calendar_to = Calendar(self.root, selectmode="day")
        self.label_from = tk.Label(self.root, text="Дата початку")
        self.label_to = tk.Label(self.root, text="Дата кінця")
        self.button_make_plot = tk.Button(self.root, text="Побудувати графік", command=self.make_plot)
        
    def make_plot(self):
        if self.builder.date_to is not None and self.builder.date_from is not None \
            and self.builder.date_to < self.builder.date_from:
            messagebox.showwarning("Помилка", "Дата кінця менша за дата початку")
            return
        plot_type = self.selected_plot_type.get()
        self.builder.add_plot_view_type(PlotViewType.BAR \
                                        if self.selected_plot_view_type.get() == 'Стовпчаста діаграма' \
                                        else PlotViewType.PLOT)
        if plot_type == "Графік кількості продажів":
            self.builder.add_plot_type(PlotType.PLOT_BY_DAY_CHECK_COUTN) \
                    .build()
        elif plot_type == "Графік сум продажів":
            self.builder.add_plot_type(PlotType.PLOT_BY_DAY_SUM) \
                    .build()

    def setup_layout(self):
        self.calendar_from.grid(row=1, column=0)
        self.calendar_to.grid(row=1, column=1)
        self.label_from.grid(row=0, column=0)
        self.label_to.grid(row=0, column=1)
        self.button_make_plot.grid(row=3, column=1)
        
from CommonWindows import BaseSubWindow

import tkinter as tk
from tkinter import messagebox

from db_api import Session, engine
from db_api import Product


class ProductWindow(BaseSubWindow):

    def create_ui(self):
        self.titleUi = tk.Entry(self.root)
        self.priceUi = tk.Entry(self.root)
        self.barcodeUi = tk.Entry(self.root)
        self.countUi = tk.Entry(self.root)
        self.guarantee = tk.Entry(self.root)
        self.labelTitle = tk.Label(self.root, text="Назва")
        self.labelPrice = tk.Label(self.root,text="Ціна")
        self.labelBarcode = tk.Label(self.root,text="Штрихкод")
        self.labelCount = tk.Label(self.root, text="Кількість")
        self.labelGuarantee = tk.Label(self.root, text="Гарантія")
        self.submit = tk.Button(self.root, 
                                text="Підтвердити", 
                                command=self.submit_product)

    def setup_layout(self):
        self.labelTitle.grid(row=0,column=0)
        self.titleUi.grid(row=0,column=1)
        self.labelPrice.grid(row=1,column=0)
        self.priceUi.grid(row=1,column=1)
        self.labelBarcode.grid(row=2,column=0)
        self.barcodeUi.grid(row=2,column=1)
        self.labelCount.grid(row=3,column=0)
        self.countUi.grid(row=3,column=1)
        self.labelGuarantee.grid(row=4,column=0)
        self.guarantee.grid(row=4,column=1)
        self.submit.grid(row=5,column=1, columnspan=2)

    def __init__(self, parent) -> None:
        super().__init__(parent, "Додати товар")


    def submit_product(self):
        count = 0
        price = 0
        guarantee = 0
        try:
            count = int(self.countUi.get())
            price = float(self.priceUi.get())
            guarantee = int(self.guarantee.get())
            if count <1 or price <=0 or guarantee <1:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Помилка", "Кількість,ціна та гарантія мають бути числами більшими за 0")
            return
        if self.barcodeUi.get() == "":
            messagebox.showwarning("Помилка", "Штрихкод не може бути пустим")
            return
        if self.titleUi.get() == "":
            messagebox.showwarning("Помилка", "Назва не може бути пустою")
            return
        
        product = Product(title=self.titleUi.get(),
                            price=price,
                            barcode=self.barcodeUi.get(),
                            count=count,
                            guarantee=guarantee)
        with Session(engine) as session:
            session.add(product)
            session.commit()
            self.root.destroy()
            messagebox.showinfo("Успіх", "Товар додано")

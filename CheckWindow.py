from CommonWindows import BaseSubWindow
import tkinter as tk
from db_api import Session, engine

from db_api import Product, Check

from tkinter import messagebox
from sqlalchemy import select

class CheckWindow(BaseSubWindow): 

    def create_ui(self):
        self.products = tk.Listbox(self.root)
        self.labelProduct = tk.Label(self.root, text="Виберіть товар")
        self.labelAmount = tk.Label(self.root, text="Сума чека")
        self.amountEntry = tk.Label(self.root, text="0")
        self.buttonSubmit = tk.Button(self.root, text="Створити", command=self.submit_check)
        self.selected_products = tk.Listbox(self.root)
        self.button_add_product_to_cart = tk.Button(self.root, 
                                                    text="Додати товар", 
                                                    command=self.add_product_to_cart)
        self.button_remove_from_cart = tk.Button(self.root,
                                                text="Видалити товар",
                                                command=self.remove_from_cart)

    def setup_layout(self):
        self.labelProduct.grid(row=0, column=0)
        self.products.grid(row=0, column=1, rowspan=2)
        self.button_remove_from_cart.grid(row=2, column=2)
        self.labelAmount.grid(row=2, column=0)
        self.amountEntry.grid(row=2, column=1)
        self.buttonSubmit.grid(row=3, column=0, columnspan=1)
        self.selected_products.grid(row=0, column=2, rowspan=2)
        self.button_add_product_to_cart.grid(row=1, column=0)


    def __init__(self, parent) -> None:
        super().__init__(parent, "Створити чек")

    def setup_window(self):
        self.fill_product_list()
        self.selected=list()
        self.totalAmount=0
        
    def fetch_products(self):
        with Session(engine) as session:
            resultProducts = session.execute(select(Product))
            #products2 = session.execute(select)
            return resultProducts.scalars().all()
        
    def submit_check(self):
        if not self.totalAmount is None and not self.totalAmount==0:
            check = Check(amount=self.totalAmount,
                                items=self.selected)
            with Session(engine) as session:
                
                session.add(check)
                session.commit()
                self.destroy_window()
                messagebox.showinfo("Успіх", "Чек створено.")
        else:
            messagebox.showwarning("Помилка", "Чек не може бути пустим")


    def fill_product_list(self):
        self.lst = self.fetch_products()

        for i in range(len(self.lst)):
            self.products.insert(i, self.lst[i].title)

    def add_product_to_cart(self):
        lst = self.products.curselection()
        for i in lst:
            self.selected.append(self.lst[i])
        self.update_cart_view()

    def update_cart_view(self):
        self.totalAmount=0
        self.selected_products.delete(0, tk.END)
        for i in range(len(self.selected)):
            self.selected_products.insert(i, self.selected[i].title)
            self.totalAmount+=self.selected[i].price
        self.amountEntry.config(text=self.totalAmount)

    def remove_from_cart(self):
        for i in self.selected_products.curselection():
            del self.selected[i]
        self.update_cart_view()

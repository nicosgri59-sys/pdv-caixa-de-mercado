import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class PDVApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=16)
        self.master = master
        self.itens = []

        self.grid(sticky="nsew")
        self.master.title("PDV Caixa de Mercado")
        self.master.geometry("880x560")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self._build_header()
        self._build_form()
        self._build_cart()
        self._build_totals()
        self._update_totals()

    def _build_header(self) -> None:
        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(header, text="PDV Caixa de Mercado", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")

        date_label = ttk.Label(
            header,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            foreground="#6b7280",
        )
        date_label.grid(row=1, column=0, sticky="w")

        finalize_button = ttk.Button(header, text="Finalizar venda", command=self._finalize_sale)
        finalize_button.grid(row=0, column=1, rowspan=2, sticky="e")

    def _build_form(self) -> None:
        form = ttk.LabelFrame(self, text="Adicionar produto", padding=12)
        form.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Produto").grid(row=0, column=0, sticky="w")
        self.product_entry = ttk.Entry(form)
        self.product_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        ttk.Label(form, text="Quantidade").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.qty_entry = ttk.Spinbox(form, from_=1, to=99, width=5)
        self.qty_entry.set("1")
        self.qty_entry.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))

        ttk.Label(form, text="Preço (R$)").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.price_entry = ttk.Entry(form)
        self.price_entry.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(8, 0))

        add_button = ttk.Button(form, text="Adicionar", command=self._add_item)
        add_button.grid(row=0, column=2, rowspan=3, padx=(16, 0), sticky="ns")

    def _build_cart(self) -> None:
        cart = ttk.LabelFrame(self, text="Carrinho", padding=12)
        cart.grid(row=2, column=0, sticky="nsew", pady=(16, 0))
        cart.columnconfigure(0, weight=1)
        cart.rowconfigure(0, weight=1)

        self.cart_list = tk.Listbox(cart, height=8)
        self.cart_list.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(cart, orient="vertical", command=self.cart_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.cart_list.configure(yscrollcommand=scrollbar.set)

        remove_button = ttk.Button(cart, text="Remover selecionado", command=self._remove_item)
        remove_button.grid(row=1, column=0, columnspan=2, sticky="e", pady=(8, 0))

    def _build_totals(self) -> None:
        totals = ttk.LabelFrame(self, text="Pagamento", padding=12)
        totals.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        totals.columnconfigure(1, weight=1)

        ttk.Label(totals, text="Desconto (R$)").grid(row=0, column=0, sticky="w")
        self.discount_entry = ttk.Entry(totals)
        self.discount_entry.insert(0, "0")
        self.discount_entry.grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.discount_entry.bind("<KeyRelease>", lambda _event: self._update_totals())

        ttk.Label(totals, text="Valor recebido (R$)").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.received_entry = ttk.Entry(totals)
        self.received_entry.insert(0, "0")
        self.received_entry.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        self.received_entry.bind("<KeyRelease>", lambda _event: self._update_totals())

        self.subtotal_label = ttk.Label(totals, text="Subtotal: R$ 0,00", font=("Segoe UI", 10, "bold"))
        self.subtotal_label.grid(row=0, column=2, sticky="e")

        self.total_label = ttk.Label(totals, text="Total: R$ 0,00", font=("Segoe UI", 12, "bold"))
        self.total_label.grid(row=1, column=2, sticky="e", pady=(8, 0))

        self.change_label = ttk.Label(totals, text="Troco: R$ 0,00", foreground="#0f766e")
        self.change_label.grid(row=2, column=2, sticky="e", pady=(8, 0))

    def _add_item(self) -> None:
        name = self.product_entry.get().strip()
        if not name:
            return
        try:
            qty = int(self.qty_entry.get())
        except ValueError:
            qty = 1
        try:
            price = float(self.price_entry.get().replace(",", "."))
        except ValueError:
            price = 0.0

        total = qty * price
        self.itens.append({"name": name, "qty": qty, "price": price, "total": total})
        self.cart_list.insert(tk.END, f"{qty}x {name} - {format_currency(total)}")
        self.product_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.qty_entry.set("1")
        self._update_totals()

    def _remove_item(self) -> None:
        selection = self.cart_list.curselection()
        if not selection:
            return
        index = selection[0]
        self.cart_list.delete(index)
        self.itens.pop(index)
        self._update_totals()

    def _update_totals(self) -> None:
        subtotal = sum(item["total"] for item in self.itens)
        try:
            discount = float(self.discount_entry.get().replace(",", "."))
        except ValueError:
            discount = 0.0
        try:
            received = float(self.received_entry.get().replace(",", "."))
        except ValueError:
            received = 0.0

        total = max(subtotal - discount, 0.0)
        change = max(received - total, 0.0)

        self.subtotal_label.config(text=f"Subtotal: {format_currency(subtotal)}")
        self.total_label.config(text=f"Total: {format_currency(total)}")
        self.change_label.config(text=f"Troco: {format_currency(change)}")

    def _finalize_sale(self) -> None:
        messagebox.showinfo("Venda finalizada", "Venda finalizada com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    app = PDVApp(root)
    root.mainloop()

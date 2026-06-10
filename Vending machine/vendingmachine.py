import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Initial machine balance
machine_balance = 0.0

#this is themenu of the vending machine
# this is the section: drinks
drinks = {
    "D1": {"name": "Coca Cola", "price": 3.0, "stock": 11},
    "D2": {"name": "Pepsi", "price": 3.5, "stock": 10},
    "D3": {"name": "Sprite", "price": 1.0, "stock": 10},
    "D4": {"name": "Fanta", "price": 2.5, "stock": 12},
    "D5": {"name": "Water", "price": 1.0, "stock": 14},
    "D6": {"name": "Mountain Dew", "price": 3.0, "stock": 8},
    "D7": {"name": "Apple Juice", "price": 2.5, "stock": 18},
    "D8": {"name": "Energy Drink", "price": 4.0, "stock": 5}
}
# this is the section: snacks
snacks = {
    "S1": {"name": "Lays", "price": 1.7, "stock": 16},
    "S2": {"name": "Cookies", "price": 2.5, "stock": 14},
    "S3": {"name": "Salted Popcorn", "price": 4.0, "stock": 8},
    "S4": {"name": "Biscuits", "price": 1.5, "stock": 10},
    "S5": {"name": "Salted Nuts", "price": 5.0, "stock": 16},
    "S6": {"name": "Caramal Popcorn", "price": 9.5, "stock": 15},
    "S7": {"name": "Cotton Candy", "price": 1.5, "stock": 7},
    "S8": {"name": "Peanuts", "price": 2.6, "stock": 17}
}
# this is the section:coffee
coffees = {
    "C1": {"name": "Espresso", "price": 5.0, "stock": 18},
    "C2": {"name": "Americano", "price": 5.5, "stock": 7},
    "C3": {"name": "Cappuccino", "price": 4.5, "stock": 9},
    "C4": {"name": "Latte", "price": 4.7, "stock": 6},
    "C5": {"name": "Mocha", "price": 5.5, "stock": 5},
    "C6": {"name": "French Vanila", "price": 4.9, "stock": 6},
    "C7": {"name": "Matcha", "price": 6.5, "stock": 5},
    "C8": {"name": "Cold Coffee", "price": 4.2, "stock": 6}
}
# this is the section: chocolates
chocolates = {
    "CH1": {"name": "Dairy Milk", "price": 2.5, "stock": 10},
    "CH2": {"name": "KitKat", "price": 2.0, "stock": 10},
    "CH3": {"name": "Snickers", "price": 2.5, "stock": 10},
    "CH4": {"name": "Mars", "price": 2.5, "stock": 10},
    "CH5": {"name": "Ferrero Rocher", "price": 5.0, "stock": 5},
    "CH6": {"name": "Milky Way", "price": 2.0, "stock": 10},
    "CH7": {"name": "Bounty", "price": 2.5, "stock": 8},
    "CH8": {"name": "Toblerone", "price": 4.5, "stock": 6}
}

# this is how we display the menu
menu = {
    "1": {"section": "Drinks", "items": drinks},
    "2": {"section": "Snacks", "items": snacks},
    "3": {"section": "Coffees", "items": coffees},
    "4": {"section": "Chocolates", "items": chocolates},
    "0": {"section": "Exit"}
}

# this is for the suggestions of items
suggestions = {
    "Drinks": ["Snacks", "Chocolates"],
    "Snacks": ["Drinks", "Coffees"],
    "Coffees": ["Chocolates"],
    "Chocolates": ["Coffees", "Drinks"]
}
# this is for the payment menu
payment_menu = {
    "1": "Cash",
    "2": "Card"
}

# this is the function to display the menu.
def showmenu():
    print("\n=== MAIN MENU ===")
    for k, v in menu.items():
        print(f"{k} : {v['section']}")
# this is the function to display the items in the selected section
def showitems(items):
    print("\nCode   Item               Price  Stock")
    print("--------------------------------------")
    for code, item in items.items():
        print(f"{code}  {item['name']:18} ${item['price']}   {item['stock']}")
# this is the function for the suggestions based on the users selection.
def recommendations(section, cart):
    if section in suggestions:
        print("\nSuggested Sections:")
        for s in suggestions[section]:
            print("-", s)
        # this is to ask the user if the user wants to add the sugested items to the cart
        choice = input("Would you like to add any recommended items? (Yes/No): ").lower() 
        if choice == "Yes".lower():
            for key, value in menu.items():
                if value["section"] in suggestions[section]:
                    print(f"{key} → {value['section']}")
            # this is to selct the the key of the section to add the item
            sec_key = input("Select the section key: ") 
            if sec_key in menu:
                items = menu[sec_key]["items"]
                showitems(items)
                code = input("Put the item code here: ").upper() 
                # this is to add the selected item to the cart.
                if code in items and items[code]["stock"] > 0:
                    cart.append(items[code])
                    items[code]["stock"] -= 1
                    print(f"Added {items[code]['name']} to cart")
# this is the function for payment
def payment(total):
    global machine_balance
    print("\n=== PAYMENT ===")
    for k, v in payment_menu.items():
        print(f"{k} → {v}")
    # this is to select the payment method
    p = input("Select the payment key: ") 
    # this is for the cash payment
    if p == "1":
        cash = float(input("Put money in here: $"))
        # this is to check whether the cash is enough 
        if cash >= total:
            machine_balance += total
            print(f"Change: ${round(cash - total, 2)}")
            return True
        else:
            print("Insufficient funds") 
            return False
    # this is for the card payment
    elif p == "2":
        machine_balance += total
        print("Successful card payment") 
        return True
    else:
        print(" Payment is invalid.") 
        return False

# Tkinter GUI for the vending machine.
class VendingMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        self.root.geometry("980x720")
        self.root.resizable(False, False)

        self.cart = []
        self.current_section_key = "1"
        self.section_buttons = {}
        self.selected_item = None

        self.setup_styles()
        self.create_widgets()
        self.show_section("1")

    # This controls the colors and fonts used by the GUI.
    def setup_styles(self):
        self.colors = {
            "background": "#eef2ff",
            "panel": "#ffffff",
            "primary": "#4f46e5",
            "primary_dark": "#3730a3",
            "accent": "#06b6d4",
            "success": "#16a34a",
            "warning": "#f59e0b",
            "danger": "#dc2626",
            "text": "#111827",
            "muted": "#6b7280",
            "border": "#c7d2fe",
            "soft": "#f8fafc"
        }

        self.root.configure(bg=self.colors["background"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["background"])
        style.configure("Panel.TFrame", background=self.colors["panel"])
        style.configure("Title.TLabel", font=("Arial", 22, "bold"), background=self.colors["primary"], foreground="white")
        style.configure("Subtitle.TLabel", font=("Arial", 10), background=self.colors["primary"], foreground="#dbeafe")
        style.configure("Header.TLabel", font=("Arial", 13, "bold"), background=self.colors["panel"], foreground=self.colors["text"])
        style.configure("Info.TLabel", font=("Arial", 10, "bold"), background=self.colors["panel"], foreground=self.colors["primary_dark"])
        style.configure("DetailTitle.TLabel", font=("Arial", 11, "bold"), background=self.colors["soft"], foreground=self.colors["primary_dark"])
        style.configure("Detail.TLabel", font=("Arial", 10), background=self.colors["soft"], foreground=self.colors["text"])
        style.configure("Status.TLabel", font=("Arial", 10, "bold"), background=self.colors["primary_dark"], foreground="white")

        style.configure("TButton", font=("Arial", 10, "bold"), padding=9, borderwidth=0)
        style.configure("Section.TButton", background="#e0e7ff", foreground=self.colors["primary_dark"])
        style.map("Section.TButton", background=[("active", "#c7d2fe")])
        style.configure("Active.Section.TButton", background=self.colors["primary"], foreground="white")
        style.configure("Primary.TButton", background=self.colors["accent"], foreground="white")
        style.map("Primary.TButton", background=[("active", "#0891b2")])
        style.configure("Success.TButton", background=self.colors["success"], foreground="white")
        style.map("Success.TButton", background=[("active", "#15803d")])
        style.configure("Warning.TButton", background=self.colors["warning"], foreground="white")
        style.map("Warning.TButton", background=[("active", "#d97706")])
        style.configure("Danger.TButton", background=self.colors["danger"], foreground="white")
        style.map("Danger.TButton", background=[("active", "#b91c1c")])

        style.configure("Treeview", rowheight=30, font=("Arial", 10), background="white", fieldbackground="white", foreground=self.colors["text"])
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.colors["primary"], foreground="white")
        style.map("Treeview", background=[("selected", self.colors["accent"])], foreground=[("selected", "white")])

    # This builds the main layout of the vending machine window.
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=90)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title = ttk.Label(header_frame, text="WELCOME TO THE VENDING MACHINE", style="Title.TLabel")
        title.pack(pady=(16, 2))
        subtitle = ttk.Label(header_frame, text="Choose your section, add items, then pay by cash or card", style="Subtitle.TLabel")
        subtitle.pack()

        main_frame = tk.Frame(self.root, bg=self.colors["background"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=(18, 10))

        left_frame = tk.Frame(main_frame, bg=self.colors["panel"], bd=0, highlightthickness=1, highlightbackground=self.colors["border"])
        left_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=12, ipady=12)

        ttk.Label(left_frame, text="Sections", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        for key, value in menu.items():
            if key != "0":
                button = ttk.Button(
                    left_frame,
                    text=value["section"],
                    style="Section.TButton",
                    command=lambda section_key=key: self.show_section(section_key)
                )
                button.pack(fill="x", pady=4)
                self.section_buttons[key] = button

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=15)
        self.balance_label = ttk.Label(left_frame, text="Machine balance: $0.00", style="Info.TLabel")
        self.balance_label.pack(anchor="w", pady=4)

        self.item_detail_frame = tk.Frame(left_frame, bg=self.colors["soft"], highlightthickness=1, highlightbackground=self.colors["border"])
        self.item_detail_frame.pack(fill="x", pady=(18, 0), ipadx=10, ipady=10)
        ttk.Label(self.item_detail_frame, text="Selected Item", style="DetailTitle.TLabel").pack(anchor="w")
        self.detail_name = ttk.Label(self.item_detail_frame, text="Choose an item", style="Detail.TLabel")
        self.detail_name.pack(anchor="w", pady=(8, 2))
        self.detail_code = ttk.Label(self.item_detail_frame, text="Code: -", style="Detail.TLabel")
        self.detail_code.pack(anchor="w")
        self.detail_price = ttk.Label(self.item_detail_frame, text="Price: -", style="Detail.TLabel")
        self.detail_price.pack(anchor="w")
        self.detail_stock = ttk.Label(self.item_detail_frame, text="Stock: -", style="Detail.TLabel")
        self.detail_stock.pack(anchor="w")

        content_frame = tk.Frame(main_frame, bg=self.colors["panel"], bd=0, highlightthickness=1, highlightbackground=self.colors["border"])
        content_frame.pack(side="left", fill="both", expand=True, ipadx=14, ipady=14)

        self.section_label = ttk.Label(content_frame, text="", style="Header.TLabel")
        self.section_label.pack(anchor="w")

        columns = ("code", "name", "price", "stock")
        self.items_table = ttk.Treeview(content_frame, columns=columns, show="headings", height=12)
        self.items_table.heading("code", text="Code")
        self.items_table.heading("name", text="Item")
        self.items_table.heading("price", text="Price")
        self.items_table.heading("stock", text="Stock")
        self.items_table.column("code", width=80, anchor="center")
        self.items_table.column("name", width=220)
        self.items_table.column("price", width=100, anchor="center")
        self.items_table.column("stock", width=100, anchor="center")
        self.items_table.pack(fill="x", pady=10)
        self.items_table.bind("<<TreeviewSelect>>", self.update_item_details)

        action_frame = tk.Frame(content_frame, bg=self.colors["panel"])
        action_frame.pack(fill="x", pady=5)
        ttk.Button(action_frame, text="+ Add Selected Item", style="Primary.TButton", command=self.add_selected_item).pack(side="left", padx=(0, 8))
        ttk.Button(action_frame, text="Clear Cart", style="Danger.TButton", command=self.clear_cart).pack(side="left", padx=8)
        ttk.Button(action_frame, text="Pay by Cash", style="Warning.TButton", command=lambda: self.checkout("Cash")).pack(side="right", padx=(8, 0))
        ttk.Button(action_frame, text="Pay by Card", style="Success.TButton", command=lambda: self.checkout("Card")).pack(side="right", padx=8)

        bottom_frame = tk.Frame(content_frame, bg=self.colors["panel"])
        bottom_frame.pack(fill="both", expand=True, pady=(10, 0))

        cart_frame = tk.Frame(bottom_frame, bg=self.colors["panel"])
        cart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(cart_frame, text="Cart", style="Header.TLabel").pack(anchor="w")
        self.cart_list = tk.Listbox(
            cart_frame,
            height=8,
            bg="#f8fafc",
            fg=self.colors["text"],
            selectbackground=self.colors["accent"],
            selectforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            font=("Arial", 10)
        )
        self.cart_list.pack(fill="both", expand=True, pady=5)
        self.total_label = ttk.Label(cart_frame, text="Total: $0.00", style="Header.TLabel")
        self.total_label.pack(anchor="w")

        suggestion_frame = tk.Frame(bottom_frame, bg=self.colors["panel"])
        suggestion_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ttk.Label(suggestion_frame, text="Suggested Sections", style="Header.TLabel").pack(anchor="w")
        self.suggestion_list = tk.Listbox(
            suggestion_frame,
            height=8,
            bg="#f8fafc",
            fg=self.colors["text"],
            selectbackground=self.colors["primary"],
            selectforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            font=("Arial", 10)
        )
        self.suggestion_list.pack(fill="both", expand=True, pady=5)
        ttk.Button(suggestion_frame, text="Open Suggested Section", style="Section.TButton", command=self.open_suggestion).pack(fill="x")

        status_frame = tk.Frame(self.root, bg=self.colors["primary_dark"], height=34)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        self.status_label = ttk.Label(status_frame, text="Ready. Select an item to begin.", style="Status.TLabel")
        self.status_label.pack(anchor="w", padx=20, pady=7)

    # This shows all items from the selected section.
    def show_section(self, section_key):
        self.current_section_key = section_key
        section = menu[section_key]["section"]
        items = menu[section_key]["items"]

        for key, button in self.section_buttons.items():
            button.configure(style="Active.Section.TButton" if key == section_key else "Section.TButton")

        self.section_label.config(text=f"{section} Menu")
        self.items_table.delete(*self.items_table.get_children())
        for code, item in items.items():
            self.items_table.insert("", "end", values=(code, item["name"], f"${item['price']:.2f}", item["stock"]))

        self.update_suggestions(section)
        self.clear_item_details()
        self.set_status(f"Showing {section}. Select an item to see details.")

    # This updates the selected item card beside the menu.
    def update_item_details(self, event=None):
        selected = self.items_table.selection()
        if not selected:
            self.clear_item_details()
            return

        code, name, price, stock = self.items_table.item(selected[0], "values")
        self.selected_item = code
        self.detail_name.config(text=name)
        self.detail_code.config(text=f"Code: {code}")
        self.detail_price.config(text=f"Price: {price}")
        self.detail_stock.config(text=f"Stock: {stock}")
        self.set_status(f"Selected {name}. Press Add Selected Item to add it to your cart.")

    # This resets the selected item card.
    def clear_item_details(self):
        self.selected_item = None
        self.detail_name.config(text="Choose an item")
        self.detail_code.config(text="Code: -")
        self.detail_price.config(text="Price: -")
        self.detail_stock.config(text="Stock: -")

    # This updates the message bar at the bottom of the app.
    def set_status(self, message):
        self.status_label.config(text=message)

    # This updates the suggested sections based on the selected section.
    def update_suggestions(self, section):
        self.suggestion_list.delete(0, tk.END)
        for suggested_section in suggestions.get(section, []):
            self.suggestion_list.insert(tk.END, suggested_section)

    # This opens a section that the suggestions list recommends.
    def open_suggestion(self):
        selected = self.suggestion_list.curselection()
        if not selected:
            self.set_status("Please select a suggested section first.")
            messagebox.showinfo("No suggestion selected", "Please select a suggested section first.")
            return

        section_name = self.suggestion_list.get(selected[0])
        for key, value in menu.items():
            if value["section"] == section_name:
                self.show_section(key)
                return

    # This adds the selected table item to the cart and reduces its stock.
    def add_selected_item(self):
        selected = self.items_table.selection()
        if not selected:
            self.set_status("No item selected. Choose an item from the table first.")
            messagebox.showinfo("No item selected", "Please select an item first.")
            return

        code = self.items_table.item(selected[0], "values")[0]
        items = menu[self.current_section_key]["items"]
        item = items[code]

        if item["stock"] <= 0:
            self.set_status(f"{item['name']} is out of stock.")
            messagebox.showwarning("Out of stock", f"{item['name']} is out of stock.")
            return

        item["stock"] -= 1
        self.cart.append(item)
        self.refresh_cart()
        self.show_section(self.current_section_key)
        self.set_status(f"Added {item['name']} to cart.")
        messagebox.showinfo("Added to cart", f"Added {item['name']} to cart.")

    # This refreshes the cart list, total, and machine balance label.
    def refresh_cart(self):
        self.cart_list.delete(0, tk.END)
        for item in self.cart:
            self.cart_list.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")

        total = sum(item["price"] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")
        self.balance_label.config(text=f"Machine balance: ${machine_balance:.2f}")
        self.set_status(f"Cart has {len(self.cart)} item(s). Total: ${total:.2f}")

    # This removes all current cart items and returns them to stock.
    def clear_cart(self):
        if not self.cart:
            self.set_status("Cart is already empty.")
            return

        for cart_item in self.cart:
            for section in menu.values():
                if "items" in section:
                    for item in section["items"].values():
                        if item is cart_item:
                            item["stock"] += 1

        self.cart.clear()
        self.refresh_cart()
        self.show_section(self.current_section_key)
        self.set_status("Cart cleared and stock restored.")

    # This handles cash and card checkout.
    def checkout(self, method):
        global machine_balance

        if not self.cart:
            self.set_status("Add an item before paying.")
            messagebox.showinfo("Empty cart", "Please add an item before paying.")
            return

        total = sum(item["price"] for item in self.cart)

        if method == "Cash":
            cash = simpledialog.askfloat("Cash Payment", f"Total is ${total:.2f}. Enter cash amount:")
            if cash is None:
                self.set_status("Cash payment cancelled.")
                return
            if cash < total:
                self.set_status("Insufficient cash entered.")
                messagebox.showwarning("Insufficient funds", "The cash amount is not enough.")
                return
            change = cash - total
            machine_balance += total
            self.set_status(f"Cash payment complete. Change: ${change:.2f}")
            messagebox.showinfo("Payment successful", f"Payment accepted.\nChange: ${change:.2f}\nGather your items.")
        else:
            machine_balance += total
            self.set_status("Card payment complete. Gather your items.")
            messagebox.showinfo("Payment successful", "Successful card payment.\nGather your items.")

        self.cart.clear()
        self.refresh_cart()
        self.show_section(self.current_section_key)


# Start the Tkinter vending machine app.
if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineGUI(root)
    root.mainloop()

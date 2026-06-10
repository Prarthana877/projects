import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import BytesIO
from PIL import Image, ImageTk

# --- PREMIUM THEME ---
COLORS = {
    "bg": "#0f172a",        # Deep Navy
    "card": "#1e293b",      # Slate
    "accent": "#ef4444",    # Pokedex Red
    "text": "#f8fafc",      # White
    "blue": "#38bdf8",      # Info Blue
    "green": "#22c55e",     # Success Green
    "yellow": "#fbbf24"     # Stats Gold
}

# --- POKEAPI INTERACTIONS ---
# Handles all API requests to PokeAPI
class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2"

# Fetches detailed data for a specific Pokémon by name or ID
    def fetch_pokemon(self, query):
        try:
            res = requests.get(f"{self.BASE_URL}/pokemon/{query.lower().strip()}", timeout=10)
            if res.status_code != 200: return None
            data = res.json()
            return {
                "name": data["name"].title(),
                "id": data["id"],
                "height": data["height"] / 10,
                "weight": data["weight"] / 10,
                "types": [t["type"]["name"].upper() for t in data["types"]],
                "stats": {s["stat"]["name"].upper().replace("-", " "): s["base_stat"] for s in data["stats"]},
                "img": data["sprites"]["other"]["official-artwork"]["front_default"]
            }
        except: return None

# Fetches the evolution chain for a specific Pokémon by name
    def fetch_evolutions(self, name):
        try:
            # Species -> Chain URL -> Chain Data
            s_res = requests.get(f"{self.BASE_URL}/pokemon-species/{name.lower()}/")
            chain_url = s_res.json()['evolution_chain']['url']
            c_res = requests.get(chain_url)
            chain = c_res.json()['chain']
            
            evos = []
            curr = chain
            while curr:
                evos.append(curr['species']['name'].title())
                curr = curr['evolves_to'][0] if curr['evolves_to'] else None
            return evos
        except: return ["No Data"]

# Fetches a list of the first 151 Pokémon
    def get_list(self):
        try:
            res = requests.get(f"{self.BASE_URL}/pokemon?limit=151")
            return [{"id": i+1, "name": p["name"].title()} for i, p in enumerate(res.json()["results"])]
        except: return []

# --- MAIN APPLICATION ---
# Primary Tkinter Application for the Pokédex
class PokedexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PRO-DEX ULTIMATE")
        self.geometry("1000x750")
        self.configure(bg=COLORS["bg"])
        self.api = PokeAPI()
        self.img_ref = None
        self.show_home()

# Clears all widgets from the main window
    def clear(self):
        for w in self.winfo_children(): w.destroy()

# Creates a styled button
    def create_btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd, bg=color, fg="white", 
                        font=("Arial", 11, "bold"), relief="flat", padx=20, pady=10, cursor="hand2")

# Displays the home screen with navigation options
    def show_home(self):
        self.clear()
        f = tk.Frame(self, bg=COLORS["bg"])
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(f, text="POKÉDEX", font=("Impact", 80), bg=COLORS["bg"], fg=COLORS["accent"]).pack()
        tk.Label(f, text="SYSTEM ONLINE // GEN-1 DATABASE", font=("Courier", 12), bg=COLORS["bg"], fg=COLORS["blue"]).pack(pady=(0,40))

        self.create_btn(f, "SEARCH TERMINAL", self.show_search, COLORS["blue"]).pack(pady=10, fill="x")
        self.create_btn(f, "LIST ALL POKÉMON", self.show_list, COLORS["green"]).pack(pady=10, fill="x")

# Displays the search interface for querying Pokémon
    def show_search(self):
        self.clear()
        # Top Nav
        nav = tk.Frame(self, bg=COLORS["bg"], padx=20, pady=10)
        nav.pack(fill="x")
        self.create_btn(nav, "← BACK", self.show_home, COLORS["card"]).pack(side="left")

        # Search Row
        s_frame = tk.Frame(self, bg=COLORS["bg"], padx=50)
        s_frame.pack(fill="x", pady=10)
        self.entry = tk.Entry(s_frame, font=("Consolas", 18), bg=COLORS["card"], fg=COLORS["text"], borderwidth=0, insertbackground="white")
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,10))
        self.entry.bind("<Return>", lambda e: self.run_search())
        self.create_btn(s_frame, "ANALYZE", self.run_search, COLORS["accent"]).pack(side="right")

        # Main Display Content
        self.content = tk.Frame(self, bg=COLORS["bg"], padx=50)
        self.content.pack(fill="both", expand=True)

        self.img_box = tk.Label(self.content, bg=COLORS["card"], width=400, height=400)
        self.img_box.pack(side="left", padx=(0,20))

        self.info_box = tk.Text(self.content, bg=COLORS["card"], fg=COLORS["text"], font=("Consolas", 12), padx=20, pady=20, relief="flat")
        self.info_box.pack(side="right", fill="both", expand=True)
        self.info_box.tag_configure("h", font=("Consolas", 18, "bold"), foreground=COLORS["yellow"])

# Executes the search and updates the UI with results
    def run_search(self):
        query = self.entry.get()
        data = self.api.fetch_pokemon(query)
        if not data:
            messagebox.showerror("Error", "SUBJECT NOT FOUND"); return

        # Update Text Details
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert(tk.END, f"{data['name']} [#{data['id']}]\n", "h")
        self.info_box.insert(tk.END, f"TYPE: {' / '.join(data['types'])}\n")
        self.info_box.insert(tk.END, f"HT: {data['height']}m | WT: {data['weight']}kg\n")
        self.info_box.insert(tk.END, f"{'—'*30}\nBASE STATS:\n")

        # Stats with Bars
        for stat, val in data['stats'].items():
            bar = "█" * (val // 10)
            self.info_box.insert(tk.END, f"{stat:<12}: {val:>3} {bar}\n")

        # Evolution Button (Dynamic placement)
        self.create_btn(self.info_box, "VIEW EVOLUTIONS", 
                        lambda: messagebox.showinfo("Evolutions", " ➔ ".join(self.api.fetch_evolutions(data['name']))),
                        COLORS["accent"]).pack(side="bottom", pady=10)

        # Update Image
        res = requests.get(data['img'])
        img = Image.open(BytesIO(res.content)).resize((380,380))
        self.img_ref = ImageTk.PhotoImage(img)
        self.img_box.config(image=self.img_ref)

# Displays the list of all Pokémon in a table
    def show_list(self):
        self.clear()
        nav = tk.Frame(self, bg=COLORS["bg"], padx=20, pady=10)
        nav.pack(fill="x")
        self.create_btn(nav, "← BACK", self.show_home, COLORS["card"]).pack(side="left")

        # Table Styling
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=COLORS["card"], foreground="white", fieldbackground=COLORS["card"], rowheight=30)
        s.configure("Treeview.Heading", background=COLORS["blue"], foreground="white", font=("Arial", 10, "bold"))

        # Table Setup
        tree = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        tree.heading("ID", text="INDEX")
        tree.heading("Name", text="POKÉMON NAME")
        tree.column("ID", width=100, anchor="center")
        tree.pack(fill="both", expand=True, padx=50, pady=20)

# Populate Table
        for p in self.api.get_list():
            tree.insert("", "end", values=(f"#{p['id']}", p['name']))

# --- RUN APPLICATION ---
if __name__ == "__main__":
    PokedexApp().mainloop()
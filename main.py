import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

class PlantIDSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Identification System")
        self.root.geometry("900x500")

        self.prolog = Prolog()
        self.prolog.consult("plants.pl")

        self.plants_cache = []
        self.create_widgets()
        self.load_all_plants()

    def create_widgets(self):
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="Soil Type:").grid(row=0, column=0, padx=5, pady=5)
        self.soil_var = tk.StringVar()
        self.soil_combo = ttk.Combobox(filter_frame, textvariable=self.soil_var, state="readonly")
        self.soil_combo['values'] = ("any", "loamy", "sandy")
        self.soil_combo.current(0)
        self.soil_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Sunlight:").grid(row=0, column=2, padx=5, pady=5)
        self.sun_var = tk.StringVar()
        self.sun_combo = ttk.Combobox(filter_frame, textvariable=self.sun_var, state="readonly")
        self.sun_combo['values'] = ("any", "full_sun", "partial_shade", "shade")
        self.sun_combo.current(0)
        self.sun_combo.grid(row=0, column=3, padx=5, pady=5)

        self.edible_var = tk.StringVar(value="any")
        self.edible_check = ttk.Checkbutton(filter_frame, text="Edible only", command=self.toggle_edible)
        self.edible_check.grid(row=0, column=4, padx=5, pady=5)
        self.is_edible = False

        ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=5, padx=5, pady=5)

        search_frame = ttk.LabelFrame(self.root, text="Search Plant")
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_plant).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(search_frame, text="Clear Search", command=self.clear_search).grid(row=0, column=3, padx=5, pady=5)

        list_frame = ttk.Frame(self.root)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

        self.plant_listbox = tk.Listbox(list_frame, width=30, height=25)
        self.plant_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.plant_listbox.bind('<<ListboxSelect>>', self.show_details)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.plant_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.plant_listbox.config(yscrollcommand=scrollbar.set)

        details_frame = ttk.LabelFrame(self.root, text="Plant Details")
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.name_label = ttk.Label(details_frame, text="", font=("Arial", 18, "bold"))
        self.name_label.pack(pady=10)

        ttk.Label(details_frame, text="Description:", font=("Arial", 14, "underline")).pack(anchor=tk.W, padx=5)
        self.desc_text = tk.Text(details_frame, height=5, wrap=tk.WORD)
        self.desc_text.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(details_frame, text="Care Tips:", font=("Arial", 14, "underline")).pack(anchor=tk.W, padx=5)
        self.tips_text = tk.Text(details_frame, height=5, wrap=tk.WORD)
        self.tips_text.pack(fill=tk.X, padx=5, pady=5)

    def toggle_edible(self):
        self.is_edible = not self.is_edible

    def load_all_plants(self):
        self.plants_cache.clear()
        self.plant_listbox.delete(0, tk.END)

        query = "plant(Name, CommonName, Soil, Sunlight, Edible, Description, Tips)"
        for sol in self.prolog.query(query):
            plant = {k: (v.decode() if isinstance(v, bytes) else v) for k, v in sol.items()}
            self.plants_cache.append(plant)
            self.plant_listbox.insert(tk.END, plant["CommonName"])

    def apply_filters(self):
        soil = self.soil_var.get()
        sun = self.sun_var.get()
        edible = "yes" if self.is_edible else "any"

        filtered = []
        for p in self.plants_cache:
            if soil != "any" and p["Soil"] != soil:
                continue
            if sun != "any" and p["Sunlight"] != sun:
                continue
            if edible == "yes" and p["Edible"] != "yes":
                continue
            filtered.append(p)

        if not filtered:
            messagebox.showinfo("No Results", "No plants found matching your filters.")
            self.load_all_plants()
            return

        self.plant_listbox.delete(0, tk.END)
        for p in filtered:
            self.plant_listbox.insert(tk.END, p["CommonName"])

    def search_plant(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showinfo("Input Error", "Please enter a search keyword.")
            return
        matches = [p for p in self.plants_cache if keyword in p["CommonName"].lower() or keyword in p["Name"].lower()]
        if not matches:
            messagebox.showinfo("No Results", "No plants found matching your search.")
            self.load_all_plants()
            return

        self.plant_listbox.delete(0, tk.END)
        for p in matches:
            self.plant_listbox.insert(tk.END, p["CommonName"])

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_all_plants()

    def show_details(self, event):
        if not self.plant_listbox.curselection():
            return
        index = self.plant_listbox.curselection()[0]
        selected_common_name = self.plant_listbox.get(index)

        plant = next((p for p in self.plants_cache if p["CommonName"] == selected_common_name), None)
        if not plant:
            return

        self.name_label.config(text=plant["CommonName"])
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, plant["Description"])
        self.tips_text.delete("1.0", tk.END)
        self.tips_text.insert(tk.END, plant["Tips"])

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantIDSystem(root)
    root.mainloop() 
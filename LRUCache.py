import tkinter as tk
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value  # move to end (MRU)
            return value
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # pop LRU
        self.cache[key] = value

class LRUCacheGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LRU Cache Visualizer")
        self.cache = None
        self.capacity = 3  # default

        self.setup_widgets()
        self.draw_cache()

    def setup_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Capacity:").grid(row=0, column=0)
        self.cap_entry = tk.Entry(frame, width=5)
        self.cap_entry.grid(row=0, column=1)
        self.cap_entry.insert(0, str(self.capacity))
        tk.Button(frame, text="Set", command=self.set_capacity).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Put key:").grid(row=1, column=0)
        self.put_key_entry = tk.Entry(frame, width=5)
        self.put_key_entry.grid(row=1, column=1)
        tk.Label(frame, text="Value:").grid(row=1, column=2)
        self.put_val_entry = tk.Entry(frame, width=5)
        self.put_val_entry.grid(row=1, column=3)
        tk.Button(frame, text="Put", command=self.put).grid(row=1, column=4, padx=5)

        tk.Label(frame, text="Get key:").grid(row=2, column=0)
        self.get_key_entry = tk.Entry(frame, width=5)
        self.get_key_entry.grid(row=2, column=1)
        tk.Button(frame, text="Get", command=self.get).grid(row=2, column=2, padx=5)
        self.get_result = tk.Label(frame, text="")
        self.get_result.grid(row=2, column=3, columnspan=2)

        self.canvas = tk.Canvas(self.root, width=500, height=120, bg='white')
        self.canvas.pack(pady=10)

        self.status = tk.Label(self.root, text="", fg="#1976d2")
        self.status.pack()

    def set_capacity(self):
        try:
            cap = int(self.cap_entry.get())
            if cap <= 0:
                raise ValueError
            self.capacity = cap
            self.cache = LRUCache(self.capacity)
            self.status.config(text=f"Cache reset with capacity {self.capacity}")
            self.draw_cache()
        except ValueError:
            self.status.config(text="Capacity must be a positive integer.")

    def put(self):
        key = self.put_key_entry.get()
        val = self.put_val_entry.get()
        if key == '' or val == '':
            self.status.config(text="Both key and value required for put.")
            return
        if self.cache is None:
            self.cache = LRUCache(self.capacity)
        evicted = None
        if key not in self.cache.cache and len(self.cache.cache) >= self.cache.capacity:
            evicted = next(iter(self.cache.cache))
        self.cache.put(key, val)
        if evicted:
            self.status.config(text=f"Evicted LRU key: {evicted}")
        else:
            self.status.config(text=f"Put ({key}, {val})")
        self.draw_cache()

    def get(self):
        key = self.get_key_entry.get()
        if key == '':
            self.status.config(text="Key required for get.")
            return
        if self.cache is None:
            self.cache = LRUCache(self.capacity)
        val = self.cache.get(key)
        if val == -1:
            self.get_result.config(text="Not found", fg="red")
            self.status.config(text=f"Get {key}: Not found")
        else:
            self.get_result.config(text=f"{val}", fg="green")
            self.status.config(text=f"Get {key}: {val}")
        self.draw_cache(highlight=key if val != -1 else None)

    def draw_cache(self, highlight=None):
        self.canvas.delete("all")
        if self.cache is None:
            return
        x0, y0 = 30, 40
        w, h = 70, 50
        gap = 20
        items = list(self.cache.cache.items())
        for idx, (k, v) in enumerate(items):
            x = x0 + idx * (w + gap)
            color = '#90caf9'  # normal
            outline = 'black'
            if idx == 0:
                color = '#fff59d'  # LRU
            if idx == len(items) - 1:
                color = '#a5d6a7'  # MRU
            if highlight is not None and str(k) == str(highlight):
                outline = '#d32f2f'
                color = '#ffd54f'
            self.canvas.create_rectangle(x, y0, x + w, y0 + h, fill=color, outline=outline, width=4)
            self.canvas.create_text(x + w // 2, y0 + h // 2 - 10, text=f"{k}", font=("Arial", 16, "bold"))
            self.canvas.create_text(x + w // 2, y0 + h // 2 + 15, text=f"{v}", font=("Arial", 14))
        if items:
            # LRU label
            self.canvas.create_text(x0 - 30, y0 + h // 2, text="LRU", font=("Arial", 12, "bold"))
            # MRU label
            self.canvas.create_text(x0 + (len(items) - 1) * (w + gap) + w + 30, y0 + h // 2, text="MRU", font=("Arial", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = LRUCacheGUI(root)
    root.mainloop()

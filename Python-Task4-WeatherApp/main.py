import threading
import tkinter as tk
from datetime import datetime

from weather_api import get_current_weather
class WeatherDashboard(tk.Tk):
    """A polished Tkinter weather dashboard with a lightweight animated UI."""

    THEMES = {
        "Clear": ("#173B6C", "#F6B73C", "☀"), "Clouds": ("#334E68", "#7F9DB5", "☁"),
        "Rain": ("#19324D", "#3B82B6", "☂"), "Drizzle": ("#19324D", "#4B93C4", "☂"),
        "Thunderstorm": ("#241B3B", "#7057A6", "ϟ"), "Snow": ("#31536E", "#91B8CF", "❄"),
        "Mist": ("#465B66", "#8DA6AA", "≋"), "Fog": ("#465B66", "#8DA6AA", "≋"),
        "Haze": ("#5A4B3B", "#B68D56", "☼"),
    }

    def __init__(self):
        super().__init__()
        self.title("Nimbus • Weather Dashboard")
        self.geometry("920x680")
        self.minsize(820, 620)
        self.configure(bg="#12213A")
        self.recent_cities, self.loading_tick, self.is_loading = [], 0, False
        self._build_ui()
        self._clock()
        self.city_entry.focus_set()

    def _label(self, parent, text="", size=12, weight="normal", fg="#FFFFFF", bg=None, **kwargs):
        return tk.Label(parent, text=text, font=("Segoe UI", size, weight), fg=fg, bg=bg or parent.cget("bg"), **kwargs)

    def _build_ui(self):
        self.header = tk.Frame(self, bg="#12213A")
        self.header.pack(fill="x", padx=38, pady=(26, 14))
        self._label(self.header, "NIMBUS", 18, "bold").pack(side="left")
        self._label(self.header, "YOUR PERSONAL WEATHER DESK", 8, "bold", "#8FA6C7").pack(side="left", padx=12, pady=7)
        self.clock_label = self._label(self.header, "", 10, "normal", "#C8D7EA")
        self.clock_label.pack(side="right", pady=5)

        search = tk.Frame(self, bg="#203653", padx=16, pady=12)
        search.pack(fill="x", padx=38)
        self.city_entry = tk.Entry(search, font=("Segoe UI", 13), bg="#203653", fg="#9FB3CE", insertbackground="#FFFFFF", relief="flat", bd=0)
        self.city_entry.insert(0, "Search any city…")
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.city_entry.bind("<FocusIn>", self._clear_placeholder)
        self.city_entry.bind("<Return>", lambda _event: self.fetch_weather())
        self.search_button = tk.Button(search, text="SEARCH  →", command=self.fetch_weather, font=("Segoe UI", 10, "bold"), fg="#12213A", bg="#F6C453", activebackground="#FFE08A", relief="flat", cursor="hand2", padx=17, pady=9)
        self.search_button.pack(side="right", padx=(12, 0))

        self.hero = tk.Frame(self, bg="#173B6C", padx=32, pady=24)
        self.hero.pack(fill="x", padx=38, pady=16)
        left = tk.Frame(self.hero, bg="#173B6C")
        left.pack(side="left", fill="both", expand=True)
        self.location = self._label(left, "READY WHEN YOU ARE", 11, "bold", "#DDEBFA")
        self.location.pack(anchor="w")
        self.condition = self._label(left, "Search a city to see the forecast", 17)
        self.condition.pack(anchor="w", pady=(7, 13))
        self.range_label = self._label(left, "Live weather from OpenWeather", 10, "normal", "#C8D7EA")
        self.range_label.pack(anchor="w")
        right = tk.Frame(self.hero, bg="#173B6C")
        right.pack(side="right")
        self.weather_icon = self._label(right, "☀", 48, "normal", "#FFE08A")
        self.weather_icon.pack(side="left", padx=(0, 10))
        self.temperature = self._label(right, "--°", 47, "bold")
        self.temperature.pack(side="left")

        self.status = self._label(self, "Type a city and press Enter", 10, "normal", "#9FB3CE")
        self.status.pack(anchor="w", padx=42, pady=(0, 8))
        self.stats = tk.Frame(self, bg="#12213A")
        self.stats.pack(fill="both", expand=True, padx=38)
        self.stat_values = {}
        cards = [("◉", "FEELS LIKE", "--°", "feels"), ("◈", "HUMIDITY", "--%", "humidity"), ("➶", "WIND", "-- m/s", "wind"), ("◌", "VISIBILITY", "-- km", "visibility"), ("↑", "SUNRISE", "--:--", "sunrise"), ("↓", "SUNSET", "--:--", "sunset")]
        for index, (icon, title, value, key) in enumerate(cards):
            card = tk.Frame(self.stats, bg="#203653", padx=17, pady=14)
            card.grid(row=index // 3, column=index % 3, sticky="nsew", padx=5, pady=5)
            self._label(card, icon, 16, "bold", "#F6C453").pack(anchor="w")
            self._label(card, title, 8, "bold", "#9FB3CE").pack(anchor="w", pady=(6, 2))
            value_label = self._label(card, value, 16, "bold")
            value_label.pack(anchor="w")
            self.stat_values[key] = value_label
        for column in range(3): self.stats.grid_columnconfigure(column, weight=1)
        for row in range(2): self.stats.grid_rowconfigure(row, weight=1)

        recent = tk.Frame(self, bg="#12213A")
        recent.pack(fill="x", padx=38, pady=(9, 22))
        self._label(recent, "RECENT", 8, "bold", "#8FA6C7").pack(side="left", padx=(4, 12))
        self.recent_area = tk.Frame(recent, bg="#12213A")
        self.recent_area.pack(side="left")

    def _clear_placeholder(self, _event=None):
        if self.city_entry.get() == "Search any city…":
            self.city_entry.delete(0, tk.END)
            self.city_entry.configure(fg="#FFFFFF")

    def fetch_weather(self, city=None):
        if self.is_loading: return
        city = city or self.city_entry.get().strip()
        if not city or city == "Search any city…":
            self.status.config(text="Please enter a city name first.", fg="#FFCF70")
            self.city_entry.focus_set()
            return
        self.is_loading, self.loading_tick = True, 0
        self.search_button.config(state="disabled", bg="#9A7B3C")
        self.status.config(fg="#C8D7EA")
        self._loading_animation()
        threading.Thread(target=self._request_weather, args=(city,), daemon=True).start()

    def _request_weather(self, city):
        result = get_current_weather(city)
        self.after(0, lambda: self._finish_request(result))

    def _loading_animation(self):
        if not self.is_loading: return
        self.status.config(text=f"Fetching live weather{'.' * (self.loading_tick % 4)}")
        self.loading_tick += 1
        self.after(350, self._loading_animation)

    def _finish_request(self, result):
        self.is_loading = False
        self.search_button.config(state="normal", bg="#F6C453")
        if not result["success"]:
            self.status.config(text=result["error"], fg="#FF9C9C")
            return
        self._show_weather(result)

    def _show_weather(self, data):
        dark, accent, icon = self.THEMES.get(data["condition"], self.THEMES["Clouds"])
        self._paint_hero(self.hero, dark)
        self.weather_icon.config(text=icon, fg="#FFE08A" if data["condition"] == "Clear" else "#FFFFFF")
        self.location.config(text=f"{data['city'].upper()}, {data['country']}")
        self.condition.config(text=data["description"].title())
        self.temperature.config(text=f"{data['temperature']:.0f}°")
        low, high = data["temp_min"] or data["temperature"], data["temp_max"] or data["temperature"]
        self.range_label.config(text=f"Low {low:.0f}°  •  High {high:.0f}°  •  Pressure {data['pressure']} hPa")
        values = {"feels": f"{data['feels_like']:.0f}°C", "humidity": f"{data['humidity']}%", "wind": f"{data['wind_speed']:.1f} m/s", "visibility": f"{data['visibility']:.1f} km", "sunrise": data["sunrise"], "sunset": data["sunset"]}
        for key, value in values.items(): self.stat_values[key].config(text=value)
        self.status.config(text="Updated just now  •  Live conditions", fg=accent)
        self._add_recent(data["city"])

    def _paint_hero(self, widget, color):
        widget.configure(bg=color)
        for child in widget.winfo_children():
            child.configure(bg=color)
            if isinstance(child, tk.Frame): self._paint_hero(child, color)

    def _add_recent(self, city):
        self.recent_cities = [item for item in self.recent_cities if item.lower() != city.lower()]
        self.recent_cities = [city] + self.recent_cities[:3]
        for child in self.recent_area.winfo_children(): child.destroy()
        for name in self.recent_cities:
            tk.Button(self.recent_area, text=name, command=lambda value=name: self.fetch_weather(value), font=("Segoe UI", 9), fg="#DDEBFA", bg="#203653", activebackground="#2D4B70", activeforeground="#FFFFFF", relief="flat", cursor="hand2", padx=10, pady=5).pack(side="left", padx=3)

    def _clock(self):
        self.clock_label.config(text=datetime.now().strftime("%a, %d %b  •  %I:%M %p"))
        self.after(1000, self._clock)


if __name__ == "__main__":
    WeatherDashboard().mainloop()

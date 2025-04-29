import customtkinter as ctk
import requests
import json
import os
from tkinter import ttk
import tkinter as tk
from countries import COUNTRIES
from PIL import Image
import CTkToolTip


# set default appearance
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window configuration
        self.title("WeatherWisp")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.iconbitmap("icons/logo.ico")

        # load settings
        self.settings_file = "settings.json"
        self.load_settings()

        # sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # sidebar title with icon
        weather_icon = ctk.CTkImage(Image.open("icons/logo.png"), size=(30, 30))
        self.sidebar_title = ctk.CTkLabel(self.sidebar_frame, text=" WeatherWisp", font=ctk.CTkFont(size=20, weight="bold"), image=weather_icon, compound="left")
        self.sidebar_title.pack(pady=20, padx=20)

        # dark mode toggle
        self.dark_mode_switch = ctk.CTkSwitch(self.sidebar_frame, text=" Dark Mode", command=self.toggle_theme)
        self.dark_mode_switch.pack(pady=10, padx=20)
        self.dark_mode_switch.select() if self.settings.get("dark_mode", True) else self.dark_mode_switch.deselect()

        # about button with icon
        about_icon = ctk.CTkImage(Image.open("icons/about.png"), size=(20, 20))
        self.about_button = ctk.CTkButton(self.sidebar_frame, text="About", command=self.show_about, image=about_icon, compound="left", width=140, height=40, fg_color="#1E90FF", hover_color="#00BFFF")
        self.about_button.pack(pady=10, padx=20, fill="x")

        # settings button with icon
        settings_icon = ctk.CTkImage(Image.open("icons/settings.png"), size=(20, 20))
        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings, image=settings_icon, compound="left", width=140, height=40, fg_color="#1E90FF", hover_color="#00BFFF")
        self.settings_button.pack(pady=10, padx=20, fill="x")

        # main content frame
        self.main_frame = ctk.CTkFrame(self, width=800, height=600)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # country selection
        self.country_label = ctk.CTkLabel(self.main_frame, text="Select Country:", font=ctk.CTkFont(size=16))
        self.country_label.pack(pady=(20, 5))

        self.countries = COUNTRIES
        self.country_var = tk.StringVar(value=self.settings.get("last_country", "United States"))
        favourite_countries = self.settings.get("favourite_countries", [])
        all_countries = favourite_countries + [c for c in self.countries.keys() if c not in favourite_countries]
        self.country_dropdown = ttk.Combobox(self.main_frame, textvariable=self.country_var, values=all_countries, state="readonly", width=30)
        self.country_dropdown.pack(pady=5)

        # city entry
        self.city_label = ctk.CTkLabel(self.main_frame, text="Enter City:", font=ctk.CTkFont(size=16))
        self.city_label.pack(pady=(20, 5))

        self.city_entry = ctk.CTkEntry(self.main_frame, width=300)
        self.city_entry.pack(pady=5)
        self.city_entry.insert(0, self.settings.get("last_city", ""))

        # get weather button with icon
        search_icon = ctk.CTkImage(Image.open("icons/search.png"), size=(20, 20))
        self.weather_button = ctk.CTkButton(self.main_frame, text="Get Weather", command=self.get_weather, image=search_icon, compound="left")
        self.weather_button.pack(pady=20)

        # weather display frame
        self.weather_frame = ctk.CTkFrame(self.main_frame)
        self.weather_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.weather_display = ctk.CTkLabel(self.weather_frame, text="Weather information will appear here", font=ctk.CTkFont(size=14), wraplength=800, justify="left")
        self.weather_display.pack(pady=10)

        self.air_quality_display = ctk.CTkLabel(self.weather_frame, text="Air quality information will appear here", font=ctk.CTkFont(size=14), wraplength=600, justify="center")
        self.air_quality_display.pack(pady=10)

        # api key
        self.api_key = ""

    def load_settings(self):
        self.settings = {}
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        # ensure favourite_countries exists, default to empty list
        if "favourite_countries" not in self.settings:
            self.settings["favourite_countries"] = []

    def save_settings(self):
        self.settings.update({"dark_mode": self.dark_mode_switch.get() == 1, "last_country": self.country_var.get(), "last_city": self.city_entry.get()})
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f)

    def add_favourite_country(self, country, display_label):
        # add a country to the favourites list and update the JSON file
        if country and country in self.countries and country != "Select a country":
            # get the current list of favourites, or initialize an empty list
            favourite_countries = self.settings.get("favourite_countries", [])
            if country not in favourite_countries:  # avoid duplicates
                favourite_countries.append(country)
                self.settings["favourite_countries"] = favourite_countries
                self.save_settings()  # save to JSON
                # update the display label
                display_label.configure(text="Favourites: " + ", ".join(favourite_countries))
            else:
                display_label.configure(text="Favourites: " + ", ".join(favourite_countries) + " (Already added)")

    def clear_favourite_countries(self, display_label):
        # clear the favourite countries list and update the JSON file
        self.settings["favourite_countries"] = []
        self.save_settings()
        display_label.configure(text="Favourites: None")

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.dark_mode_switch.get() == 1 else "light")
        self.save_settings()

    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("300x200")
        about_window.resizable(width=False, height=False)
        about_label = ctk.CTkLabel(about_window, text="WeatherWisp v1.0\nCreated with CustomTkinter\nWeather data from OpenWeatherMap\n\nCreated by Dmitrijs Dunajevs", font=ctk.CTkFont(size=14))
        about_label.pack(pady=20)

    def show_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(width=False, height=False)
        # label for favourite countries
        settings_label = ctk.CTkLabel(settings_window, text="Manage Favourite Countries", font=ctk.CTkFont(size=16, weight="bold"))
        settings_label.pack(pady=10)

        # dropdown for selecting a country
        favourite_country_var = tk.StringVar(value="Select a country")
        favourite_country_dropdown = ttk.Combobox(settings_window, textvariable=favourite_country_var, values=list(self.countries.keys()), state="readonly", width=30)
        favourite_country_dropdown.pack(pady=5)

        # frame to hold the buttons horizontally
        button_frame = ctk.CTkFrame(settings_window)
        button_frame.pack(pady=10)

        # button to add the selected country
        add_button = ctk.CTkButton(button_frame, text="Add to Favourites", command=lambda: self.add_favourite_country(favourite_country_var.get(), favourite_display))
        add_button.pack(side="left", padx=(0, 10))  # add padding to the right of the button
        CTkToolTip.CTkToolTip(add_button, message="Select a country from the dropdown and click to add it to your favourites list.")

        # button to clear favourites
        clear_button = ctk.CTkButton(button_frame, text="Clear Favourites", command=lambda: self.clear_favourite_countries(favourite_display))
        clear_button.pack(side="left", padx=(10, 0))  # add padding to the left of the button
        CTkToolTip.CTkToolTip(clear_button, message="Click to remove all countries from your favourites list.")

        # display current favourite countries
        favourite_display = ctk.CTkLabel(settings_window, text="Favourites: " + ", ".join(self.settings.get("favourite_countries", [])), font=ctk.CTkFont(size=14), wraplength=350)
        favourite_display.pack(pady=10)


    def get_weather(self):
        city = self.city_entry.get().strip()
        country_code = self.countries[self.country_var.get()]

        if not city:
            self.weather_display.configure(text="Error: Please enter a city name", text_color="red")
            return

        self.weather_display.configure(text="Fetching weather data...", text_color="white" if ctk.get_appearance_mode() == "Dark" else "black")
        self.air_quality_display.configure(text="Fetching air quality data...")
        self.update()

        try:
            # get weather data
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={self.api_key}&units=metric"
            weather_response = requests.get(weather_url, timeout=5)
            weather_data = weather_response.json()

            if weather_data["cod"] != 200:
                self.weather_display.configure(text=f"Error: {weather_data['message']}", text_color="red")
                self.air_quality_display.configure(text="")
                return

            # get air quality data (using coordinates from weather response)
            lat = weather_data["coord"]["lat"]
            lon = weather_data["coord"]["lon"]
            air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
            air_response = requests.get(air_url, timeout=5)
            air_response.raise_for_status()
            air_data = air_response.json()

            # parse and format weather data
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]
            wind_speed = weather_data["wind"]["speed"]

            weather_text = (f"Weather in {city}, {self.country_var.get()}:\n"
                            f"🌡️ Temperature: {temp}°C\n"
                            f"🌡️ Feels like: {feels_like}°C\n"
                            f"💧      Humidity: {humidity}%\n"
                            f"☁️   Conditions: {description.capitalize()}\n"
                            f"💨    Wind speed: {wind_speed} m/s")

            self.weather_display.configure(text=weather_text, text_color="white" if ctk.get_appearance_mode() == "Dark" else "black")

            # parse and format air quality data
            aqi = air_data["list"][0]["main"]["aqi"]
            aqi_text = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor"
            }.get(aqi, "Unknown")

            components = air_data["list"][0]["components"]
            aqi_explanation = "AQI ranges: 1=Good (0-50), 2=Fair (51-100), 3=Moderate (101-150), 4=Poor (151-200), 5=Very Poor (201+)"
            air_text = (f"Air Quality Index: {aqi_text} (AQI: {aqi})\n"
                        f"{aqi_explanation}\n"
                        f"PM2.5:  {components['pm2_5']:>6.1f} µg/m³\n"
                        f"PM10:   {components['pm10']:>6.1f} µg/m³\n"
                        f"CO:       {components['co']:>6.1f} µg/m³")

            self.air_quality_display.configure(text=air_text)

            # save settings
            self.save_settings()

        except requests.ConnectionError:
            self.weather_display.configure(text="Error: No internet connection", text_color="red")
            self.air_quality_display.configure(text="")
        except requests.Timeout:
            self.weather_display.configure(text="Error: Request timed out", text_color="red")
            self.air_quality_display.configure(text="")
        except requests.RequestException as e:
            self.weather_display.configure(text=f"Error: {str(e)}", text_color="red")
            self.air_quality_display.configure(text="")
        except Exception as e:
            self.weather_display.configure(text=f"Unexpected error: {str(e)}", text_color="red")
            self.air_quality_display.configure(text="")


if __name__ == "__main__":
    app = App()
    app.mainloop()


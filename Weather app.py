import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

def search_weather():
    location = location_entry.get()
    weather_data = get_weather(location)
    if weather_data:
        weather_info, weather_icon = parse_weather_data(weather_data)
        display_weather(weather_info, weather_icon)
    else:
        messagebox.showerror("Error", "Failed to fetch weather information.")

def get_weather(location):
    api_key = "83aaadcc9359f19321bb879138c0b9eb"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def parse_weather_data(data):
    weather_info = {
        "Location": data["name"],
        "Temperature": f"{data['main']['temp']}°C",
        "Humidity": f"{data['main']['humidity']}%",
        "Weather": data["weather"][0]["description"]
    }
    weather_icon_code = data["weather"][0]["icon"]
    return weather_info, weather_icon_code

def display_weather(weather_info, weather_icon_code):
    weather_text = ""
    for key, value in weather_info.items():
        weather_text += f"{key}: {value}\n"
    weather_label.config(text=weather_text)

    icon_url = f"http://openweathermap.org/img/wn/{weather_icon_code}.png"
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        icon_data = BytesIO(icon_response.content)
        image = Image.open(icon_data)
        image = image.resize((50, 50))  # Corrected
        weather_icon = ImageTk.PhotoImage(image)
        weather_icon_label.config(image=weather_icon)
        weather_icon_label.image = weather_icon  # Keep reference to prevent garbage collection
    else:
        messagebox.showerror("Error", "Failed to fetch weather icon.")

root = tk.Tk()
root.title("Weather App")

location_label = tk.Label(root, text="Enter city:")
location_label.grid(row=0, column=0, padx=10, pady=10)
location_entry = tk.Entry(root)
location_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=search_weather)
search_button.grid(row=0, column=2, padx=10, pady=10)

weather_label = tk.Label(root, text="")
weather_label.grid(row=1, columnspan=3, padx=10, pady=10)

weather_icon_label = tk.Label(root)
weather_icon_label.grid(row=2, columnspan=3, padx=10, pady=10)

root.mainloop()

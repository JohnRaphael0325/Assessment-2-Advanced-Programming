import tkinter as tk
from tkinter import messagebox
import requests  # To get the Pokémon data from the API
from PIL import Image, ImageTk  # To handle and display images in Tkinter
from io import BytesIO  # To convert the API image data into an image

# Class to store the Pokémon's information
class Pokemon:
    def __init__(self, name, types, stats, image_url):
        # Store the Pokémon's name, types, stats, and image URL
        self.name = name
        self.types = types
        self.stats = stats
        self.image_url = image_url

# Function to get the data from the PokéAPI
def get_pokemon(pokemon_name):
    # Sends a request to the API using the Pokémon name
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    
    if response.status_code != 200:
        return None  # If Pokémon not found, return None

    data = response.json()  # Convert the API response to JSON

    # Get the Pokémon name and format it nicely
    name = data["name"].capitalize()

    # Get all Pokémon types from the API
    types = []
    for t in data["types"]:
        types.append(t["type"]["name"].capitalize())

    # Store key Pokémon stats
    stats = {
        "HP": data["stats"][0]["base_stat"],
        "Attack": data["stats"][1]["base_stat"],
        "Defense": data["stats"][2]["base_stat"],
        "Speed": data["stats"][5]["base_stat"]
    }

    # Get the Pokémon image URL
    image_url = data["sprites"]["front_default"]

    # Create and return the Pokémon object
    return Pokemon(name, types, stats, image_url)

# Function to show Pokémon info in the GUI
def show_pokemon():
    pokemon_name = entry.get().strip()  # Get user input from entry box
    if not pokemon_name:
        messagebox.showwarning("Input Error", "Enter Pokémon name or ID.")
        return

    pokemon = get_pokemon(pokemon_name)  # Getting Pokémon data
    if not pokemon:
        messagebox.showerror("Not Found", "Pokémon not found.")
        return
 
    # Update labels with Pokémon info
    name_label.config(text="NAME: " + pokemon.name.upper())
    type_label.config(text="TYPE: " + ", ".join(pokemon.types).upper())

    # Show stats
    stats_label.config(text=f"HP: {pokemon.stats['HP']}\n"
                            f"Attack: {pokemon.stats['Attack']}\n"
                            f"Defense: {pokemon.stats['Defense']}\n"
                            f"Speed: {pokemon.stats['Speed']}")

    # Getting and display Pokémon image
    image_data = Image.open(BytesIO(requests.get(pokemon.image_url).content)).resize((120,120))
    pokemon_image = ImageTk.PhotoImage(image_data)
    image_label.config(image=pokemon_image)
    image_label.image = pokemon_image  # Keep reference to avoid disappearing

# GUI Setup
root = tk.Tk()
root.title("Pokédex")
root.geometry("430x620")
root.resizable(False, False)
root.configure(bg="#c62828")

# Title label
tk.Label(root, text="POKÉDEX", font=("Arial Black", 24), fg="white", bg="#c62828").pack(pady=12)

# Frame for search bar and button
search_frame = tk.Frame(root, bg="#c62828")
search_frame.pack(pady=5)
entry = tk.Entry(search_frame, width=26, font=("Segoe UI",12))  # Entry box
entry.pack(pady=6)
tk.Button(search_frame, text="SCAN", font=("Segoe UI",11,"bold"), bg="#eeeeee", width=12, command=show_pokemon).pack(pady=6) # Calls show_pokemon on click

# Frame to display Pokémon details
screen_frame = tk.Frame(root, bg="#1c1c1c", bd=4, relief="sunken")
screen_frame.pack(padx=22, pady=20, fill="both", expand=True)

# Labels to show name, type, stats, and image
name_label = tk.Label(screen_frame, text="NAME:", font=("Courier New",13,"bold"), fg="#00e676", bg="#1c1c1c")
name_label.pack(anchor="w", padx=12, pady=6)

type_label = tk.Label(screen_frame, text="TYPE:", font=("Courier New",12), fg="#00e676", bg="#1c1c1c")
type_label.pack(anchor="w", padx=12)

stats_label = tk.Label(screen_frame, text="", font=("Courier New",12), fg="#00e676", bg="#1c1c1c", justify="left")
stats_label.pack(anchor="w", padx=12, pady=12)

image_label = tk.Label(screen_frame, bg="#1c1c1c")
image_label.pack(pady=10)

# Run the GUI
root.mainloop()

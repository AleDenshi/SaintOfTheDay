import csv
from discord import Embed, File, Color
from PIL import Image

def get_color(filename: str) -> Color:
    try:
        with Image.open(filename) as img:
            img = img.convert("RGBA")
            img = img.resize((1,1), resample=0)
            main_color = img.getpixel((0,0))
            r, g, b, a = main_color 
            return Color.from_rgb(r,g,b)
    except:
        return Color.from_rgb(255,255,255)

def get_response(date: str) -> Embed:
    with open('saints.csv', mode='r') as file:
        saints = csv.DictReader(file)
        for row in saints:
            if row["Date"] == date:
                name = row["Name"]
                titles = row["Titles"]
                years = row["Years"]
                description = row["Description"]
                print("Setting up embed...")	
                # Set up the embed
                embedVar = Embed(title=name, description=description, color=get_color("images/" + date + ".jpg"))
                embedVar.add_field(name="Years", value="*" + years + "*", inline=True)
                embedVar.add_field(name="Titles", value="*" + titles + "*", inline=True)
                # Check for the existence of an image
                try:
                    image = File("images/" + date + ".jpg")
                    print("Image found!")
                    print("Trying to set image URL...")
                    embedVar.set_image(url="attachment://" + date + ".jpg")
                except Exception as e:
                    print(e, "\nNo image found, proceeding with default.")
                print(embedVar)	
                return embedVar


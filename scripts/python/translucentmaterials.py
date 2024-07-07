# Print translucent materials

import os
import PIL.Image

image_files = "D:\\SteamLibrary\\steamapps\\common\\GarrysMod\\garrysmod\\addons\\robloxmaterials\\materialsrc\\kiwifruitdev\\robloxmaterials\\raw"
filter = "1_diff.png"

for file in os.listdir(image_files):
    if file.endswith(filter):
        image = PIL.Image.open(image_files + "\\" + file)
        if image.mode == "RGBA":
            # Check if any pixel has an alpha value less than 255
            #pixel_count = 0
            for pixel in image.getdata():
                if pixel[3] < 255:
                    print("\"" + file.replace(filter, "").lower() + "\",")
                    break
                    #pixel_count += 1
            #if pixel_count > 0:
                #print("[\"" + file.replace(filter, "").lower() + "\", " + str(pixel_count) + "],")

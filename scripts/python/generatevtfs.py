# Convert PNG files to VTF files using the VTFCmd command line tool

# Settings
vtfcmd = "vtfcmd"
imagemagick = "magick"
invert_green_channel = True
skip_existing_files = True
skip_copying_files = False
pre2022_materials_only = True

# Input files
image_files = "D:\\SteamLibrary\\steamapps\\common\\GarrysMod\\garrysmod\\addons\\robloxmaterials\\materialsrc\\kiwifruitdev\\robloxmaterials"
raw_subdirectory = "\\raw"
image_format = "png"
diffuse_suffix = "1_diff"
normal_suffix = "1_nmap"

# Output files
output_vtf_directory = "D:\\SteamLibrary\\steamapps\\common\\GarrysMod\\garrysmod\\addons\\robloxmaterials\\materials\\kiwifruitdev\\robloxmaterials"
output_subdirectory = "\\%MATERIAL%"
output_diffuse_name = "diffuse"
output_normal_name = "normal"

# General VTF settings
vtf_normal_format = "dxt1"
vtf_alpha_format = "dxt5"
vtf_mipmap = True
vtf_mipmap_filter = "box"
vtf_mipmap_sharpen_filter = "sharpensoft"
vtf_resize = True
vtf_resize_method = "nearest"
vtf_resize_filter = "triangle"
vtf_resize_sharpen_filter = "none"
vtf_clamp = True
vtf_clamp_width = 4096
vtf_clamp_height = 4096

# Advanced VTF settings
vtf_version = "7.2"
vtf_reflectivity = True
vtf_thumbnail = True

import os
import subprocess
import re
import PIL.Image
from vars import materials, translucent_materials, brickcolors, textureless_materials, pre2022_materials

materials_directory = "D:\\SteamLibrary\\steamapps\\common\\GarrysMod\\garrysmod\\addons\\robloxmaterials\\materials"

# Process or copy PNG files to output directory with new name (normal maps need inverted green channel if enabled)
for file in os.listdir(image_files + raw_subdirectory):
    if file.endswith(image_format) and (file.endswith(diffuse_suffix + "." + image_format) or file.endswith(normal_suffix + "." + image_format)):
        print(file)
        input_file = image_files + raw_subdirectory + "\\" + file
        material = file.replace(diffuse_suffix, "").replace(normal_suffix, "").replace("." + image_format, "").lower()
        if material in textureless_materials:
            continue
        if pre2022_materials_only and material not in pre2022_materials:
            continue
        directory = output_subdirectory.replace("%MATERIAL%", material)
        if not os.path.exists(image_files + directory):
            os.makedirs(image_files + directory)
        output_file = image_files + directory
        if file.endswith(diffuse_suffix + "." + image_format):
            output_file += "\\" + output_diffuse_name + "." + image_format
            if skip_existing_files and os.path.exists(output_file):
                continue
            if not skip_copying_files:
                print("Copying " + file + " to " + output_file)
                subprocess.run([imagemagick, input_file, output_file])
                if material in translucent_materials:
                    # Translucent materials:
                    # Use imagemagick to make an opaque background
                    # For each brickcolor, copy the translucent image over the opaque background
                    # Save as output, replacing output_diffuse_name in output_file with the brickcolor name
                    print("Processing " + file + " (translucent)")
                    temp_file = output_file.replace("." + image_format, "_temp." + image_format)
                    temp2_file = output_file.replace("." + image_format, "_temp2." + image_format)
                    subprocess.run([imagemagick, input_file, "-alpha", "off", temp_file])
                    for brickcolor in brickcolors:
                        brickcolor_name = brickcolor[0].lower().replace(" ", "_").replace("(", "").replace(")", "")
                        brickcolor_name = brickcolor_name.replace("/", "").replace(".", "").replace(",", "").replace("-", "")
                        new_output_file = output_file.replace(output_diffuse_name, brickcolor_name)
                        if skip_existing_files and os.path.exists(new_output_file):
                            continue
                        if not skip_copying_files:
                            print("Copying translucent variant of " + file + " to " + new_output_file)
                            # Scale each pixel color by brickcolor[1] (RGB value) using pillow
                            red_scale = int(brickcolor[1].split(", ")[0]) / 255
                            green_scale = int(brickcolor[1].split(", ")[1]) / 255
                            blue_scale = int(brickcolor[1].split(", ")[2]) / 255
                            image = PIL.Image.open(input_file)
                            image = image.convert("RGBA")
                            pixels = image.load()
                            for x in range(image.width):
                                for y in range(image.height):
                                    r, g, b, a = pixels[x, y]
                                    pixels[x, y] = (int(r * red_scale), int(g * green_scale), int(b * blue_scale), a)
                            # Save temporary image
                            image.save(temp2_file)
                            # Overlay the temporary image over the opaque background
                            subprocess.run([imagemagick, "composite", temp2_file, temp_file, new_output_file])
                    # Remove temporary images
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    if os.path.exists(temp2_file):
                        os.remove(temp2_file)
                    if os.path.exists(output_file):
                        os.remove(output_file)
        elif file.endswith(normal_suffix + "." + image_format):
            print("Processing " + file + " (normal)")
            output_file += "\\" + output_normal_name + "." + image_format
            #vtf_command.append("-flag")
            #vtf_command.append("normal")
            if skip_existing_files and os.path.exists(output_file):
                continue
            if not skip_copying_files:
                if invert_green_channel:
                    print("Inverting green channel for " + file)
                    subprocess.run([imagemagick, input_file, "-channel", "G", "-negate", output_file])

for material in materials:
    if material[0] in textureless_materials:
        continue
    if pre2022_materials_only and material[0] not in pre2022_materials:
        continue
    directory = output_subdirectory.replace("%MATERIAL%", material[0])
    vtf_directory = output_vtf_directory + output_subdirectory.replace("%MATERIAL%", material[0])
    if not os.path.exists(vtf_directory):
        os.makedirs(vtf_directory)
    vtf_command = [
        vtfcmd,
    ]
    vtf_command.append("-folder")
    vtf_command.append(image_files + directory + "\\*." + image_format)
    vtf_command.append("-output")
    vtf_command.append(vtf_directory)
    vtf_command.append("-format")
    vtf_command.append(vtf_normal_format)
    vtf_command.append("-alphaformat")
    vtf_command.append(vtf_alpha_format)
    vtf_command.append("-version")
    vtf_command.append(vtf_version)
    if not vtf_mipmap:
        vtf_command.append("-nomipmaps")
    else:
        vtf_command.append("-mfilter")
        vtf_command.append(vtf_mipmap_filter)
        vtf_command.append("-msharpen")
        vtf_command.append(vtf_mipmap_sharpen_filter)
    if vtf_resize:
        vtf_command.append("-resize")
        vtf_command.append("-rmethod")
        vtf_command.append(vtf_resize_method)
        vtf_command.append("-rfilter")
        vtf_command.append(vtf_resize_filter)
        vtf_command.append("-rsharpen")
        vtf_command.append(vtf_resize_sharpen_filter)
        if vtf_clamp:
            vtf_command.append("-rclampwidth")
            vtf_command.append(str(vtf_clamp_width))
            vtf_command.append("-rclampheight")
            vtf_command.append(str(vtf_clamp_height))
    if not vtf_reflectivity:
        vtf_command.append("-noreflectivity")
    if not vtf_thumbnail:
        vtf_command.append("-nothumbnail")
    print("Converting images to VTF...")
    print(vtf_command)
    subprocess.run(vtf_command)


# Generate VMT files for each Roblox BrickColor enum

pre2022_materials_only = True

# Import vars.py
from vars import materials, brickcolors, textureless_materials, translucent_materials, pre2022_materials, surfacetypes, textureless_surfacetypes

import os

vmt_template = '''*SHADER*
{
    $basetexture "kiwifruitdev/robloxmaterials/*MATERIAL1*/diffuse"
    $bumpmap "kiwifruitdev/robloxmaterials/*MATERIAL2*/normal"
    %keywords "kiwifruitdev,roblox,*MATERIAL2*"
    $surfaceprop "*SURFACEPROP*"
    $*COLOR* "{ *R* *G* *B* }"
}'''

vmt_template_translucent = '''*SHADER*
{
    $basetexture "kiwifruitdev/robloxmaterials/*MATERIAL1*/*BRICKCOLOR*"
    $bumpmap "kiwifruitdev/robloxmaterials/*MATERIAL2*/normal"
    %keywords "kiwifruitdev,roblox,*MATERIAL2*,rblxtrans"
    $surfaceprop "*SURFACEPROP*"
}'''

materials_directory = "D:\\SteamLibrary\\steamapps\\common\\GarrysMod\\garrysmod\\addons\\robloxmaterials\\materials"
filepath_template = "kiwifruitdev\\robloxmaterials\\*MATERIAL*\\*BRICKCOLOR*.vmt"

shaders = [
    ["LightmappedGeneric", "color", ""],
    #["VertexLitGeneric", "color2", "models\\"],
]

combined_materials = []
combined_textureless = []
combined_pre2022 = []

for material in materials:
    combined_materials.append(material)
    if material[0] in textureless_materials:
        combined_textureless.append(material[0])
    if material[0] in pre2022_materials:
        combined_pre2022.append(material[0])

for surface in surfacetypes:
    combined_materials.append(surface)
    if surface[0] in textureless_surfacetypes:
        combined_textureless.append(surface[0])
    combined_pre2022.append(surface[0])

for shader in shaders:
    for material in combined_materials:
        # Skip textureless materials
        if material[0] in combined_textureless:
            continue
        # Skip materials that are not pre-2022
        if pre2022_materials_only and material[0] not in combined_pre2022:
            continue
        for brickcolor in brickcolors:
            materialbase = material[0]
            if material[0] == "diamondplate":
                materialbase = "plastic"
            vmt = vmt_template
            if material[0] in translucent_materials:
                vmt = vmt_template_translucent
            brickcolor_name = brickcolor[0].lower().replace(" ", "_").replace("(", "").replace(")", "")
            brickcolor_name = brickcolor_name.replace("/", "").replace(".", "").replace(",", "").replace("-", "")
            brickcolor_rgb = brickcolor[1].split(", ")
            vmt = vmt.replace("*SHADER*", shader[0]).replace("*COLOR*", shader[1])
            vmt = vmt.replace("*MATERIAL1*", materialbase).replace("*MATERIAL2*", material[0]).replace("*BRICKCOLOR*", brickcolor_name)
            vmt = vmt.replace("*R*", brickcolor_rgb[0]).replace("*G*", brickcolor_rgb[1]).replace("*B*", brickcolor_rgb[2])
            vmt = vmt.replace("*SURFACEPROP*", material[1])
            filepath = shader[2] + filepath_template.replace("*MATERIAL*", material[0]).replace("*BRICKCOLOR*", brickcolor_name)
            # Create folders if they don't exist
            os.makedirs(os.path.dirname(f"{materials_directory}\\{filepath}"), exist_ok=True)
            with open(f"{materials_directory}\\{filepath}", "w") as file:
                file.write(vmt)
            print(f"Generated {filepath}")
            
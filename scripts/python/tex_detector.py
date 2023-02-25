# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json


# Config Path
CONFIG_REL_PATH = "../../config.json"
CONFIG_PATH = "D:/Scripts/Maya/ezMaterialBuilder/config.json"
TEX_FILE = "D:/Pictures/F14D_low_Body_v03_Diffuse.1001.png"


class TextureTypeDetector:
    """
    def __init__(self):
        self.keywords = []
        self.load_settings()

    def load_settings(self):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            self.settings = config["keywords"]
            print("Loaded")

    def detect_tex_type(self, file_name):
        file_name = os.path.splitext(os.path.basename(file_name))[0]
        file_name = file_name.lower()

        for tex_type, keywords in self.settings.items():
            for keyword in keywords:
                if keyword.lower() in file_name:
                    return tex_type

        return None
    """

    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.keywords = json.load(f)["keywords"]


    def detect_texture(self, file_name):
        for texture_type, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in filename.lower():
                    return texture_type
        return None

# Test
file_name = TEX_FILE
detector = TextureTypeDetector()
texture_type = detector.detect_tex_type(file_name)
print("Texture type:", texture_type)

"""
new_texture_type = 'Emissive'
new_keywords = ['emissive', 'glow']
add_texture_type(new_texture_type, new_keywords)
"""

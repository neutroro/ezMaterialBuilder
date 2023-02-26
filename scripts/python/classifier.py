# -*- coding: utf-8 -*-
from __future__ import print_function
import maya.cmds as cmds
import settings


# Config Path
CONFIG_REL_PATH = "../../config.json"
CONFIG_PATH = "D:/Scripts/Maya/ezMaterialBuilder/config.json"


class TextureClassifier:
    def __init__(self):
        names = settings.MAPS.keys()
        self.keywords = {}
        for n in names:
            keyword = settings.MAPS[n]["keywords"]
            self.keywords[n] = keyword
        #print("LOADED: ", self.keywords)

    def classify_tex(self, filename):
        for texture_type, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in filename.lower():
                    return texture_type
        return None

    def open_explorer(self):
        try:
            img_filter = "ImageFiles (*.*)"
            self.path_selected_list = cmds.fileDialog2(ff=img_filter, ds=1, fm=4)
            print("Map selected:", self.path_selected_list)
        except TypeError:
            pass

    def tex_classification(self):
        self.type_selected_list = []
        for path in self.path_selected_list:
            tex_type = self.classify_tex(path)
            self.type_selected_list.append(tex_type)
        print("tex_type: ", self.type_selected_list)
        #return self.path_selected, tex_type_list

    def classify(self):
        self.open_explorer()
        self.tex_classification()
        return self.path_selected_list, self.type_selected_list


# Debug
# classifier = TextureClassifier(CONFIG_FILE)
# classifier.run()

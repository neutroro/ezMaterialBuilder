# -*- coding: utf-8 -*-


# Texture loading settings
maps = {
    "AO": {
        "keywords": ["ao", "ambientocclusion", "ambient_occlusion"],
        "connection": [".outColor", ".input2"]
    },

    "BASECOLOR": {
        "keywords": ["diffuse", "color", "basecolor"],
        "connection": [".outColor", ".baseColor"]
    },

    "COAT": {
        "keywords": ["coat", "ambientocclusion", "ambient_occlusion"],
        "connection": [".outAlpha", ".coat"]
    },

    "DISPLACEMENT": {
        "keywords": ["disp", "displacement", "height"],
        "connection": [".outAlpha", ".displacement"]
    },

    "EMISSION": {
        "keywords": ["emission", "emit"],
        "connection": [".outAlpha", ".emission"]
    },

    "METALNESS": {
        "keywords": ["metal", "metalness"],
        "connection": [".outAlpha", ".metalness"]
    },

    "NORMAL": {
        "keywords": ["normal"],
        "connection": [".outColor", ".input"]
    },

    "OPACITY": {
        "keywords":["opacity"],
        "connection": [".outColor", ".opacity"]
    },

    "ROUGHNESS": {
        "keywords": ["rough", "roughness"],
        "connection": [".outAlpha", ".specularRoughness"]
    }
}
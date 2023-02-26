# -*- coding: utf-8 -*-


# Please list the maps you will use
LIST = [
    "AO", "BASECOLOR", "COAT", "DISPLACEMENT", "EMISSION", "METALNESS", "NORMAL", "OPACITY", "ROUGHNESS", "SPECULAR", "TRANSMISSION"
    ]

# Texture loading settings
MAPS = {
    "AO": {
        "keywords": ["ao", "ambientocclusion", "ambient_occlusion"],
        "connection": [".outColor", ".input2"]
    },

    "BASECOLOR": {
        "keywords": ["diffuse", "color", "basecolor"],
        "connection": [".outColor", ".baseColor"]
    },

    "COAT": {
        "keywords": ["coat"],
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
    },
    
    "SPECULAR": {
        "keywords": ["spec", "specular"],
        "connection": [".outAlpha", ".specular"]
    },

    "TRANSMISSION": {
        "keywords": ["trans", "transmission"],
        "connection": [".outAlpha", ".transmission"]
    }
}

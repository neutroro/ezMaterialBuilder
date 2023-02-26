# -*- coding: utf-8 -*-
from __future__ import print_function
import maya.cmds as cmds
import pymel.core as pm
import classifier
import settings


CONFIG_FILE = "D:/Scripts/Maya/ezMaterialBuilder/config.json"
classifier = classifier.TextureClassifier()
# classifier.run()


# List of maps to use
MAP_LIST = ["AO", "BASECOLOR", "COAT", "DISPLACEMENT", "EMISSION", "METALNESS", "NORMAL", "OPACITY", "ROUGHNESS", "SPECULAR", "SSS", "TRANSMISSION"]
map_path_dict = {}
map_cs_dict = {}
map_alpha_dict = {}

names = settings.maps.keys()
connection = {}
for n in names:
    connect = settings.maps[n]["connection"]
    connection[n] = connect
print("LOADED : ", connection)


# Open explorer
def open_browser(ws, tf_name):
    try:
        imgFilter = "ImageFiles (*.*)"
        map_path = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)[0]
        pm.textField(tf_name, edit=1, text=map_path)
    except TypeError:
        pass


# Listup all map paths
def apply_map_path(ws):
    for tf, map in zip(tf_maplist, MAP_LIST):
        map_path = pm.textField(tf, q=True, text=True)
        if map_path == "not selected":
            map_path_dict[map] = "None"
        else:
            map_path_dict[map] = map_path
    print("Path: ", map_path_dict)
    return map_path_dict


def apply_color_space(ws):
    for om, map in zip(om_maplist, MAP_LIST):
        color_space = pm.optionMenu(om, q=True, v=True)
        map_cs_dict[map] = color_space
    print("ColorSpace: ", map_cs_dict)
    return map_cs_dict


def apply_alpha_luminace(ws):
    for al, map in zip(al_maplist, MAP_LIST):
        a_is_luminance = pm.checkBox(al, q=True, v=True)
        map_alpha_dict[map] = a_is_luminance
    print("Alpha is Lum: ", map_alpha_dict)
    return map_alpha_dict


def apply_common_settings(ws):
    if pm.checkBox("checkbox_udim", q=True, v=True):
        udim = 3
    else:
        udim = 0
    ignore_cs = pm.checkBox("checkbox_ignore_cs", q=True, v=True)
    print("UDIM:", udim)
    print("IGNORE_CS:", ignore_cs)
    return udim, ignore_cs


def get_all_attrs(ws):
    apply_map_path(ws)
    apply_color_space(ws)
    apply_alpha_luminace(ws)
    apply_common_settings(ws)


def get_mat_name(ws):
    mat_name = pm.textField("tf_matname", q=True, text=True)
    return mat_name


# Create file nodes
def create_file_nodes(ws):
    file_nodelist = []
    for map in map_enabled:
        coord_name = "coord_" + map
        coord2d = cmds.shadingNode("place2dTexture", asUtility=True, name=coord_name)
        file_node_name = "file_" + map
        file_node = cmds.shadingNode("file", asTexture=True, name=file_node_name)
        cmds.defaultNavigation(ce=True, s=coord2d, d=file_node)
        file_nodelist.append(file_node)
    return file_nodelist


# Setup aiStandardSurface
def material_setup(ws):
    file_nodelist = create_file_nodes(ws)
    matname = get_mat_name(ws)
    path = apply_map_path(ws)
    cs = apply_color_space(ws)
    aisl = apply_alpha_luminace(ws)
    udim, ignore_cs = apply_common_settings(ws)

    if map_enabled:
        ai_mat = cmds.shadingNode("aiStandardSurface", asShader=True, name=matname)
        for map, file_node in zip(map_enabled, file_nodelist):
            connect_from = connection[map][0]
            connect_to = connection[map][1]

            # Set file nodes attributes
            cmds.setAttr(file_node + ".ignoreColorSpaceFileRules", ignore_cs)
            cmds.setAttr(file_node + ".uvTilingMode", udim)
            cmds.setAttr(file_node + ".colorSpace", cs[map], type="string")
            cmds.setAttr(file_node + ".alphaIsLuminance", aisl[map])
            cmds.setAttr(file_node + ".fileTextureName", path[map], type="string")

            if map == "AO":
                try:
                    ai_mult = cmds.shadingNode("aiMultiply", asShader=True, name=matname + "_Mult")
                    cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=ai_mult + connect_to)
                    cmds.defaultNavigation(ce=True, s=ai_mult + ".outColor", d=ai_mat + ".baseColor")
                except NameError:
                    cmds.warning("AO file is not selected.")

            elif map == "BASECOLOR":
                if "AO" in map_enabled:
                    try:
                        cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=ai_mult + ".input1")
                    except NameError:
                        cmds.warning("")
                else:
                    try:
                        cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=ai_mat + connect_to)
                    except NameError:
                        cmds.warning("")

            elif map == "DISPLACEMENT":
                try:
                    disp_shader = cmds.shadingNode("displacementShader", asShader=True, name=matname + "_DisplacementShader")
                    disp_sg = cmds.sets(r=True, nss=True, em=True, name=matname + "_dsSG")
                    cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=disp_shader + connect_to)
                    cmds.defaultNavigation(ce=True, s=disp_shader + ".displacement", d=disp_sg + ".displacementShader")
                    cmds.defaultNavigation(ce=True, s=ai_mat + ".outColor", d=disp_sg + ".surfaceShader")
                except NameError:
                    cmds.warning("DISPLACEMENT file is not selected.")

            elif map == "NORMAL":
                try:
                    ai_normal = cmds.shadingNode("aiNormalMap", asShader=True, name=matname + "_NormalMap")
                    cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=ai_normal + connect_to)
                    cmds.defaultNavigation(ce=True, s=ai_normal + ".outValue", d=ai_mat + ".normalCamera")
                except NameError:
                    cmds.warning("NORMAL file is not selected.")

            else:
                try:
                    cmds.defaultNavigation(ce=True, s=file_node + connect_from, d=ai_mat + connect_to)
                except NameError:
                    cmds.warning("")

    else:
        cmds.warning("! No active textures. Please activate one of the checkboxes !")


def auto_append(ws):
    path_selected, type_selected = classifier.classify()
    cb_selected_list = []
    tf_selected_list = []
    for type, paths in zip(type_selected, path_selected):
        if type == None:
            print(paths)
            message =  '"', paths, '" is unknown texture type. Please assign manually.'
            cmds.warning(message)
        else:
            cb_selected = "checkbox_" + type.lower()
            cb_selected_list.append(cb_selected)
            tf_selected = "textfield_" + type.lower()
            tf_selected_list.append(tf_selected)
            # print(cb_selected)

    cb_unselected_list = set(cb_maps) ^ set(cb_selected_list)
    for sel in cb_selected_list:
        pm.checkBox(sel, edit=True, v=True)
    for usel in cb_unselected_list:
        pm.checkBox(usel, edit=True, v=False)
    change_tab(ws)

    for tfs, path in zip(tf_selected_list, path_selected):
        pm.textField(tfs, edit=1, text=path)


# ChangeUI
# List of checked checkboxes
def change_tab(ws):
    global map_enabled
    map_enabled = []
    for (cb, fl, map) in zip(cb_maps, fl_maplist, MAP_LIST):
        if pm.checkBox(cb, q=True, v=True):
            pm.frameLayout(fl, q=True, edit=True, cl=False, en=True)
            map_enabled.append(map)
        else:
            pm.frameLayout(fl, q=True, edit=True, cl=True, en=False)
    # print(map_enabled)


def createAll(ws):
    mat_name = get_mat_name(ws)
    if mat_name == "":
        pm.warning('Please enter in the "Common Settings - Material Name" ')
    else:
        material_setup(ws)


# ui setting
def open_ui():
    if pm.window("mainWin", ex=True):
        pm.deleteUI("mainWin", wnd=True)
    with pm.window("mainWin", t="ezMaterialBuilder") as wn:
        global cb_maps, fl_maplist, tf_maplist, om_maplist, al_maplist
        cb_maps = []
        fl_maplist = []
        tf_maplist = []
        om_maplist = []
        al_maplist = []

        with pm.columnLayout(w=610):
            ws = {}
            with pm.horizontalLayout(ratios=[1, 4], spacing=10):
                # Mesh map selection
                with pm.columnLayout():
                    with pm.frameLayout(l="Maps", bgs=True, w=120):
                        with pm.verticalLayout(spacing=10):
                            for map in MAP_LIST:
                                cb_map = "checkbox_" + map.lower()
                                cb_maps.append(cb_map)
                                pm.checkBox(cb_map, l=map, v=False, cc=pm.Callback(change_tab, ws))
                            pm.button(l="Auto Assign", command=pm.Callback(auto_append, ws))

                # Material settings
                with pm.columnLayout():
                    height = len(MAP_LIST) * 23 + 88
                    with pm.scrollLayout(w=460, h=height, vst=True): # height = 88 + 22*n
                        # Common Settings
                        with pm.frameLayout(l="Common Settings", bgs=True, w=440):
                            with pm.verticalLayout(spacing=5):
                                with pm.horizontalLayout(ratios=[1, 4], spacing=5):
                                    pm.text(l="Material Name", al="right", rs=False)
                                    pm.textField("tf_matname", tx="", h=20)
                                with pm.horizontalLayout(ratios=[1, 1, 2, 1], spacing=5):
                                    pm.text(l="")
                                    pm.checkBox("checkbox_udim", l="UDIM")
                                    pm.checkBox("checkbox_ignore_cs", l="Ignore CS File Rules", v=True)
                                    #pm.button(l="Auto append")

                        # Mesh map settings
                        for map in MAP_LIST:
                            fl_map = "framelayout_" + map.lower()
                            fl_maplist.append(fl_map)
                            tf_map = "textfield_" + map.lower()
                            tf_maplist.append(tf_map)
                            om_map = "optionmenu_" + map.lower()
                            om_maplist.append(om_map)
                            al_map = "aluminance_" + map.lower()
                            al_maplist.append(al_map)

                            pm.frameLayout(fl_map, l=map, cll=True, cl=True, en=False, bgs=True, w=440)
                            with pm.verticalLayout(ratios=[1, 1, 1, 1], spacing=4):
                                with pm.horizontalLayout(ratios=[2, 7, 1], spacing=4):
                                    pm.text(l="Image Name", al="right", rs=False)
                                    pm.textField(tf_map, text="not selected", h=20, w=230)
                                    pm.symbolButton("browser1", image="navButtonBrowse.png",
                                                    command=pm.Callback(open_browser, ws, tf_map))

                                pm.text(" File Attributes", al="left", font='boldLabelFont')

                                with pm.horizontalLayout(ratios=[2, 7, 1], spacing=4):
                                    pm.text(l="Color Space", al="right")
                                    pm.optionMenu(om_map, en=True, acc=True)
                                    pm.menuItem("mi_srgb", l="sRGB")
                                    pm.menuItem("mi_raw", l="Raw")

                                with pm.horizontalLayout(ratios=[1, 4], spacing=4):
                                    pm.text(l="")
                                    pm.checkBox(al_map, l="Alpha is Luminance", v=False, en=True)

                    # Buttons
                    with pm.horizontalLayout(ratios=[1, 1], spacing=4):
                        pm.button(label="Build Material", w=220, command=pm.Callback(createAll, ws))
                        pm.button(label="Debug", w=220, command=pm.Callback(get_all_attrs, ws))


def run():
    open_ui()


run()

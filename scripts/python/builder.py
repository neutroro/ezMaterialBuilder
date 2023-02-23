from collections import defaultdict
import pymel.core as pm
import tex_detector


# Test tex_detector module
file_name = "F14D_low_Body_v03_Metalness.1001.png"
detector = tex_detector.TextureTypeDetector()
texture_type = detector.detect_tex_type(file_name)
print "Texture type:", texture_type

map_dict = defaultdict(list)
map_path_dict = {}

# Open explorer
def open_browser(ws, tf_name):
    try:
        imgFilter = "ImageFiles (*.*)"
        map_path = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)[0]
        pm.textField(tf_name, edit=1, text=map_path)
        #print "Map path: ", map_path
        #return map_path
    except TypeError:
        pass


# Get file path
def apply_map_path(ws, tf_name, map_name):
    map_path = pm.textField(tf_name, q=True, text=True)
    map_path_dict[map_name] = map_path
    print map_path_dict
    return map_path_dict


def select_map(ws, tf_name, map_name):
    open_browser(ws, tf_name)
    map_path_dict = apply_map_path(ws, tf_name, map_name)
    return map_path_dict


def browserDiff(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapDiff = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textDiff = mapDiff[0]
        pm.textField("tfDiffuse", edit=1, text=textDiff)
    except TypeError:
        pass


def browserNormal(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapNormal = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textNormal = mapNormal[0]
        pm.textField("tfNormal", edit=1, text=textNormal)
    except TypeError:
        pass


def browserDisplace(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapDisplace = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textDisplace = mapDisplace[0]
        pm.textField("tfDisplace", edit=1, text=textDisplace)
    except TypeError:
        pass


# Get file path
def setDiffMapPath(ws):
    global txDiff
    txDiff = ""
    text_in_d = pm.textField('tfDiffuse', q=True, text=True)
    txDiff = text_in_d


def setNormalMapPath(ws):
    global txNormal
    txNormal = ""
    text_in_n = pm.textField('tfNormal', q=True, text=True)
    txNormal = text_in_n


def setDisplaceMapPath(ws):
    global txDisplace
    txDisplace = ""
    text_in_dis = pm.textField('tfDisplace', q=True, text=True)
    txDisplace = text_in_dis


def selectDiff(ws):
    browserDiff(ws)
    setDiffMapPath(ws)


# Create file nodes
def create_file_nodes(ws):
    for m in map_enabled:
        coord_name = "coord_" + m
        coord2d = pm.shadingNode(
            "place2dTexture", asUtility=True, name=coord_name)
        file_node_name = "file_" + m
        file_node = pm.shadingNode("file", asTexture=True, name=file_node_name)
        pm.defaultNavigation(ce=True, s=coord2d, d=file_node)


def getMatName(ws):
    global mat_name
    mat_name = pm.textField("tf_matname", q=True, text=True)
    return mat_name


def initAttrs():
    for cs in maplist:
        cs_type = "sRGB"
    return cs


def set_attrs(item_cs):
    for om in om_maplist:
        #if map_enabled
        cs_type = item_cs
        print cs_type
        return cs_type


def getAttrsDiff(item_d):
    global cs_diff
    cs_diff = "sRGB"
    if pm.checkBox("cbDif", q=True, v=True):
        cs_diff = item_d


def getAttrsNor(item_n):
    global cs_nor
    cs_nor = "sRGB"
    if pm.checkBox("cbNor", q=True, v=True):
        cs_nor = item_n


def getAttrsDis(item_dis):
    global cs_dis
    cs_dis = "sRGB"
    if pm.checkBox("cbDis", q=True, v=True):
        cs_dis = item_dis


# Setup aiStandardSurface
def materialSetup(ws):
    global cs_diff, cs_met, cs_rou, cs_nor, cs_dis
    if pm.checkBox("cbDif", q=True, v=True) or pm.checkBox("cbMet", q=True, v=True) or pm.checkBox("cbRou", q=True, v=True) or pm.checkBox("cbNor", q=True, v=True) or pm.checkBox("cbDis", q=True, v=True):
        ai_mat = pm.shadingNode("aiStandardSurface",
                                asShader=True, name=matname)

        # Diffuse
        if pm.checkBox("cbDif", q=True, v=True):
            try:
                pm.defaultNavigation(
                    ce=True, s=file_diff + ".outColor", d=ai_mat + ".baseColor")
                pm.setAttr(file_diff + ".colorSpace", cs_diff, type="string")
                pm.setAttr(file_diff + ".ignoreColorSpaceFileRules", 1)
                pm.setAttr(file_diff + ".fileTextureName",
                           txDiff, type="string")

                if pm.checkBox("cbALdiff", q=True, v=True):
                    pm.setAttr(file_diff + ".alphaIsLuminance", 1)
                elif pm.checkBox("cbALdiff", q=True, v=False):
                    pm.setAttr(file_diff + ".alphaIsLuminance", 0)

                if pm.checkBox("cbUdim", q=True, v=True):
                    pm.setAttr(file_diff + ".uvTilingMode", 3)
                elif pm.checkBox("cbUdim", q=True, v=False):
                    pm.setAttr(file_diff + ".uvTilingMode", 0)

            except NameError:
                pm.warning(
                    "DiffuseMap is not selected. Please select DiffuseMap")

        # Metalness
        if pm.checkBox("cbMet", q=True, v=True):
            try:
                pm.defaultNavigation(
                    ce=True, s=file_metal + ".outAlpha", d=ai_mat + ".metalness")
                pm.setAttr(file_metal + ".colorSpace", cs_met, type="string")
                pm.setAttr(file_metal + ".ignoreColorSpaceFileRules", 1)
                pm.setAttr(file_metal + ".fileTextureName",
                           txMetal, type="string")

                if pm.checkBox("cbALmet", q=True, v=True):
                    pm.setAttr(file_metal + ".alphaIsLuminance", 1)
                elif pm.checkBox("cbALmet", q=True, v=False):
                    pm.setAttr(file_metal + ".alphaIsLuminance", 0)

                if pm.checkBox("cbUdim", q=True, v=True):
                    pm.setAttr(file_metal + ".uvTilingMode", 3)
                elif pm.checkBox("cbUdim", q=True, v=False):
                    pm.setAttr(file_metal + ".uvTilingMode", 0)

            except NameError:
                pm.warning(
                    "MetalnessMap is not selected. Please select MetalnessMap")

        # Roughness
        if pm.checkBox("cbRou", q=True, v=True):
            try:
                pm.defaultNavigation(ce=True, s=file_rough + ".outAlpha",
                                     d=ai_mat + ".specularRoughness")
                pm.setAttr(file_rough + ".colorSpace", cs_rou, type="string")
                pm.setAttr(file_rough + ".alphaIsLuminance", 1)
                pm.setAttr(file_rough + ".ignoreColorSpaceFileRules", 1)
                pm.setAttr(file_rough + ".fileTextureName",
                           txRough, type="string")

                if pm.checkBox("cbALrou", q=True, v=True):
                    pm.setAttr(file_rough + ".alphaIsLuminance", 1)
                elif pm.checkBox("cbALrou", q=True, v=False):
                    pm.setAttr(file_rough + ".alphaIsLuminance", 0)

                if pm.checkBox("cbUdim", q=True, v=True):
                    pm.setAttr(file_rough + ".uvTilingMode", 3)
                elif pm.checkBox("cbUdim", q=True, v=False):
                    pm.setAttr(file_rough + ".uvTilingMode", 0)

            except NameError:
                pm.warning(
                    "RoughnessMap is not selected. Please select RoughnessMap")

        # Normal
        if pm.checkBox("cbNor", q=True, v=True):
            try:
                ai_normal = pm.shadingNode(
                    "aiNormalMap", asShader=True, name=matname + "_NormalMap")
                pm.defaultNavigation(ce=True, s=file_normal +
                                     ".outColor", d=ai_normal + ".input")
                pm.defaultNavigation(ce=True, s=ai_normal + ".outValue",
                                     d=ai_mat + ".normalCamera")
                pm.setAttr(file_normal + ".colorSpace", cs_nor, type="string")
                pm.setAttr(file_normal + ".ignoreColorSpaceFileRules", 1)
                pm.setAttr(file_normal + ".fileTextureName",
                           txNormal, type="string")

                if pm.checkBox("cbALnor", q=True, v=True):
                    pm.setAttr(file_normal + ".alphaIsLuminance", 1)
                elif pm.checkBox("cbALnor", q=True, v=False):
                    pm.setAttr(file_normal + ".alphaIsLuminance", 0)

                if pm.checkBox("cbUdim", q=True, v=True):
                    pm.setAttr(file_normal + ".uvTilingMode", 3)
                elif pm.checkBox("cbUdim", q=True, v=False):
                    pm.setAttr(file_normal + ".uvTilingMode", 0)

            except NameError:
                pm.warning(
                    "NormalMap is not selected. Please select NormalMap")

        # Displacement
        if pm.checkBox("cbDis", q=True, v=True):
            try:
                disp_shader = pm.shadingNode(
                    "displacementShader", asShader=True, name=matname + "_DisplacementShader")
                disp_SG = pm.sets(r=True, nss=True, em=True,
                                  name=matname + "_dsSG")
                pm.defaultNavigation(
                    ce=True, s=file_displace + ".outAlpha", d=disp_shader + ".displacement")
                pm.defaultNavigation(
                    ce=True, s=disp_shader + ".displacement", d=disp_SG + ".displacementShader")
                pm.defaultNavigation(ce=True, s=ai_mat +
                                     ".outColor", d=disp_SG + ".surfaceShader")
                pm.setAttr(file_displace + ".colorSpace",
                           cs_dis, type="string")
                pm.setAttr(file_displace + ".alphaIsLuminance", 1)
                pm.setAttr(file_displace + ".ignoreColorSpaceFileRules", 1)
                pm.setAttr(file_displace + ".fileTextureName",
                           txDisplace, type="string")

                if pm.checkBox("cbALdis", q=True, v=True):
                    pm.setAttr(file_displace + ".alphaIsLuminance", 1)
                elif pm.checkBox("cbALdis", q=True, v=False):
                    pm.setAttr(file_displace + ".alphaIsLuminance", 0)

                if pm.checkBox("cbUdim", q=True, v=True):
                    pm.setAttr(file_displace + ".uvTilingMode", 3)
                elif pm.checkBox("cbUdim", q=True, v=False):
                    pm.setAttr(file_displace + ".uvTilingMode", 0)

            except NameError:
                pm.warning(
                    "NormalMap is not selected. Please select NormalMap")

        else:
            pass

    else:
        pm.warning("Please select some checkbox.")


# List of maps to use
maplist = ["AO", "DIFFUSE", "DISPLACEMENT", "METALNESS", "NORMAL", "OPACITY", "ROUGHNESS", "TRANSMISSION"]

# ChangeUI
# List of checked checkboxes
def change_tab(ws):
    global map_enabled
    map_enabled = []
    for (cb, fl, map) in zip(cb_maps, fl_maplist, maplist):
        if pm.checkBox(cb, q=True, v=True):
            pm.frameLayout(fl, q=True, edit=True, cl=False, en=True)
            map_enabled.append(map)
        else:
            pm.frameLayout(fl, q=True, edit=True, cl=True, en=False)
    print "EnableTab: ", map_enabled


def createAll(ws):
    global matname
    getMatName(ws)
    if matname == "":
        pm.warning("Please enter material name")
    else:
        create_file_nodes(ws)
        #materialSetup(ws)


# ui setting
def open_ui():
    if pm.window("mainWin", ex=True):
        pm.deleteUI("mainWin", wnd=True)
    with pm.window("mainWin", t="ezMaterialBuilder") as wn:
        global txDiff, txMetal, txRough, txNormal, txDisplace, cb_maps, fl_maplist
        txDiff = ""
        txMetal = ""
        txRough = ""
        txNormal = ""
        txDisplace = ""
        cb_maps = []
        fl_maplist = []
        tf_maplist = []
        om_maplist = []

        with pm.columnLayout(w=610):
            ws = {}
            with pm.horizontalLayout(ratios=[1, 4], spacing=10):
                # Mesh map selection
                with pm.columnLayout():
                    with pm.frameLayout(l="Maps", bgs=True, w=120):
                        with pm.verticalLayout(spacing=10):
                            for map in maplist:
                                cb_map = "checkbox_" + map.lower()
                                cb_maps.append(cb_map)
                                pm.checkBox(cb_map, l=map, v=False, cc=pm.Callback(change_tab, ws))

                # Material settings
                with pm.columnLayout():
                    with pm.scrollLayout(w=460, height=280, vst=True):
                        # Common Settings
                        with pm.frameLayout(l="Common Settings", bgs=True, w=440):
                            with pm.verticalLayout(spacing=5):
                                with pm.horizontalLayout(ratios=[1, 4], spacing=5):
                                    pm.text(l="Material Name", al="right", rs=False)
                                    pm.textField("tf_matname", tx="", h=20)
                                with pm.horizontalLayout(ratios=[1, 1, 2, 1], spacing=5):
                                    pm.text(l="")
                                    pm.checkBox("cbUdim", l="UDIM")
                                    pm.checkBox(l="Ignore CS File Rules")
                                    pm.button(l="Auto append")

                        # Mesh map settings
                        for map in maplist:
                            fl_map = "framelayout_" + map.lower()
                            fl_maplist.append(fl_map)
                            tf_map = "textfield_" + map.lower()
                            tf_maplist.append(tf_map)
                            om_map = "optionmenu_" + map.lower()
                            om_maplist.append(om_map)

                            pm.frameLayout(fl_map, l=map, cll=True, cl=True, en=False, bgs=True, w=440)
                            with pm.verticalLayout(ratios=[1, 1, 1, 1], spacing=4):
                                with pm.horizontalLayout(ratios=[2, 7, 1], spacing=4):
                                    pm.text(l="Image Name", al="right", rs=False)
                                    pm.textField(tf_map, text="not selected",
                                                cc=pm.Callback(apply_map_path, ws, tf_map, map), h=20, w=230)
                                    pm.symbolButton("browser1", image="navButtonBrowse.png",
                                                    command=pm.Callback(select_map, ws, tf_map, map))

                                pm.text(" File Attributes", al="left", font='boldLabelFont')

                                with pm.horizontalLayout(ratios=[2, 7, 1], spacing=4):
                                    pm.text(l="Color Space", al="right")
                                    pm.optionMenu(om_map, en=True, acc=True, cc=set_attrs)
                                    pm.menuItem("mi_srgb", l="sRGB")
                                    pm.menuItem("mi_raw", l="Raw")

                                with pm.horizontalLayout(ratios=[1, 4], spacing=4):
                                    pm.text(l="")
                                    pm.checkBox("cbALdiff", l="Alpha is Luminance", v=False, en=True)

                    # Buttons
                    with pm.horizontalLayout(ratios=[1, 1], spacing=4):
                        pm.button(label="Build Material", w=220, command=pm.Callback(createAll, ws))
                        pm.button(label="Close", w=220, command=pm.Callback(createAll, ws))


def run():
    initAttrs()
    open_ui()


run()

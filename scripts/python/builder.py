import pymel.core as pm
import tex_detector as td


# Open explorer
def browserDiff(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapDiff = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textDiff = mapDiff[0]
        pm.textField("tfDiffuse", edit=1, text=textDiff)
    except TypeError:
        pass


def browserMetal(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapMetal = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textMetal = mapMetal[0]
        pm.textField("tfMetalness", edit=1, text=textMetal)
    except TypeError:
        pass


def browserRough(ws):
    try:
        imgFilter = "ImageFiles (*.*)"
        mapRough = pm.fileDialog2(ff=imgFilter, ds=1, fm=1)
        textRough = mapRough[0]
        pm.textField("tfRoughness", edit=1, text=textRough)
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


def setMetalMapPath(ws):
    global txMetal
    txMetal = ""
    text_in_m = pm.textField('tfMetalness', q=True, text=True)
    txMetal = text_in_m


def setRoughMapPath(ws):
    global txRough
    txRough = ""
    text_in_r = pm.textField('tfRoughness', q=True, text=True)
    txRough = text_in_r


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


def selectMetal(ws):
    browserMetal(ws)
    setMetalMapPath(ws)


def selectRough(ws):
    browserRough(ws)
    setRoughMapPath(ws)


def selectNormal(ws):
    browserNormal(ws)
    setNormalMapPath(ws)


def selectDisplace(ws):
    browserDisplace(ws)
    setDisplaceMapPath(ws)


# Import textures
def importTextureFile(ws):
    if pm.checkBox("cbDif", q=True, v=True) or pm.checkBox("cbMet", q=True, v=True) or pm.checkBox("cbRou", q=True, v=True) or pm.checkBox("cbNor", q=True, v=True) or pm.checkBox("cbDis", q=True, v=True):
        coord2d = pm.shadingNode(
            "place2dTexture", asUtility=True, name="Coords")
        if pm.checkBox("cbDif", q=True, v=True):
            global file_diff
            file_diff = pm.shadingNode("file", asTexture=True, name="Diffuse")
            pm.defaultNavigation(ce=True, s=coord2d, d=file_diff)

        if pm.checkBox("cbMet", q=True, v=True):
            global file_metal
            file_metal = pm.shadingNode(
                "file", asTexture=True, name="Metalness")
            pm.defaultNavigation(ce=True, s=coord2d, d=file_metal)

        if pm.checkBox("cbRou", q=True, v=True):
            global file_rough
            file_rough = pm.shadingNode(
                "file", asTexture=True, name="Roughness")
            pm.defaultNavigation(ce=True, s=coord2d, d=file_rough)

        if pm.checkBox("cbNor", q=True, v=True):
            global file_normal
            file_normal = pm.shadingNode("file", asTexture=True, name="Normal")
            pm.defaultNavigation(ce=True, s=coord2d, d=file_normal)

        if pm.checkBox("cbDis", q=True, v=True):
            global file_displace
            file_displace = pm.shadingNode(
                "file", asTexture=True, name="Displacement")
            pm.defaultNavigation(ce=True, s=coord2d, d=file_displace)

        else:
            pass
    else:
        pm.warning(
            "Please select some checkbox.")


def getMatName(ws):
    global matname
    matname = pm.textField("tf_matname", q=True, text=True)


def initAttrs():
    global cs_diff, cs_met, cs_rou, cs_nor, cs_dis
    cs_diff = "sRGB"
    cs_met = "sRGB"
    cs_rou = "sRGB"
    cs_nor = "sRGB"
    cs_dis = "sRGB"


def getAttrsDiff(item_d):
    global cs_diff
    cs_diff = "sRGB"
    if pm.checkBox("cbDif", q=True, v=True):
        cs_diff = item_d


def getAttrsMet(item_m):
    global cs_met
    cs_met = "sRGB"
    if pm.checkBox("cbMet", q=True, v=True):
        cs_met = item_m


def getAttrsRou(item_r):
    global cs_rou
    cs_rou = "sRGB"
    if pm.checkBox("cbRou", q=True, v=True):
        cs_rou = item_r


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


# ChangeUI
def changeDiffTab(ws):
    if pm.checkBox("cbDif", q=True, v=True):
        pm.frameLayout("fl_diff", q=True, edit=True, cl=False, en=True)
    else:
        pm.frameLayout("fl_diff", q=True, edit=True, cl=True, en=False)


def changeMetTab(ws):
    if pm.checkBox("cbMet", q=True, v=True):
        pm.frameLayout("fl_met", q=True, edit=True, cl=False, en=True)
    else:
        pm.frameLayout("fl_met", q=True, edit=True, cl=True, en=False)


def changeRouTab(ws):
    if pm.checkBox("cbRou", q=True, v=True):
        pm.frameLayout("fl_rou", q=True, edit=True, cl=False, en=True)
    else:
        pm.frameLayout("fl_rou", q=True, edit=True, cl=True, en=False)


def changeNorTab(ws):
    if pm.checkBox("cbNor", q=True, v=True):
        pm.frameLayout("fl_nor", q=True, edit=True, cl=False, en=True)
    else:
        pm.frameLayout("fl_nor", q=True, edit=True, cl=True, en=False)


def changeDisTab(ws):
    if pm.checkBox("cbDis", q=True, v=True):
        pm.frameLayout("fl_dis", q=True, edit=True, cl=False, en=True)
    else:
        pm.frameLayout("fl_dis", q=True, edit=True, cl=True, en=False)


def createAll(ws):
    global matname
    getMatName(ws)
    if matname == "":
        pm.warning("Please enter material name")
    else:
        importTextureFile(ws)
        materialSetup(ws)


# ui setting
def openUi():
    if pm.window("mainWin", ex=True):
        pm.deleteUI("mainWin", wnd=True)
    with pm.window("mainWin", t="ezCreateMaterial") as wn:
        global txDiff, txMetal, txRough, txNormal, txDisplace, frame_diff, frame_met, frame_rou, frame_nor, frame_dis
        txDiff = ""
        txMetal = ""
        txRough = ""
        txNormal = ""
        txDisplace = ""
        with pm.columnLayout():
            ws = {}
            with pm.horizontalLayout(ratios=[1, 4], spacing=10):
                # Mesh map selection
                with pm.columnLayout():
                    with pm.frameLayout(l="Mesh maps", bgs=True, w=110):
                        with pm.verticalLayout(ratios=[1, 1, 1, 1, 1], spacing=10):
                            pm.checkBox("cbDif", l="Diffuse", v=True,
                                        cc=pm.Callback(changeDiffTab, ws))
                            pm.checkBox("cbMet", l="Metalness", v=True,
                                        cc=pm.Callback(changeMetTab, ws))
                            pm.checkBox("cbRou", l="Roughness", v=True,
                                        cc=pm.Callback(changeRouTab, ws))
                            pm.checkBox("cbNor", l="Normal", v=True,
                                        cc=pm.Callback(changeNorTab, ws))
                            pm.checkBox("cbDis", l="Displacement", v=True,
                                        cc=pm.Callback(changeDisTab, ws))

                    with pm.frameLayout(l="Advanced", cll=True, cl=True, bgs=True, w=110):
                        with pm.verticalLayout(ratios=[1, 1, 1, 1, 1], spacing=10):
                            pm.checkBox("cbAO", l="AO", v=True,
                                        cc=pm.Callback(changeDiffTab, ws))
                            pm.checkBox("cbOpc", l="Opacity", v=True,
                                        cc=pm.Callback(changeDiffTab, ws))
                            pm.checkBox("cbCav", l="Cavity", v=True,
                                        cc=pm.Callback(changeDiffTab, ws))

                with pm.columnLayout():
                    # Common Settings
                    with pm.frameLayout(l="Common Settings", cll=True, bgs=True, w=440):
                        # with pm.rowColumnLayout(nc=2, cw=[(1,90),(2,300)]):
                        with pm.verticalLayout(spacing=5):
                            with pm.horizontalLayout(ratios=[1, 4], spacing=10):
                                pm.text(l="Material Name", al="left", rs=False)
                                pm.textField("tf_matname", tx="", h=20)
                            with pm.horizontalLayout(ratios=[1, 4], spacing=10):
                                pm.checkBox("cbUdim", l="UDIM")
                                pm.checkBox(l="Ignore CS File Rules")

                    # Diffuse Settings
                    with pm.frameLayout("fl_diff", l="Diffuse", cll=True, cl=True, bgs=True, w=440) as frame_diff:
                        with pm.verticalLayout(ratios=[1, 3], spacing=5):
                            with pm.horizontalLayout(ratios=[12, 1], spacing=10):
                                # pm.checkBox("cbDif", l="Enable", v=True, cc=pm.Callback(changeUI, ws))
                                pm.textField("tfDiffuse", text="not selected",
                                             cc=pm.Callback(setDiffMapPath, ws), h=20, w=230)
                                pm.symbolButton("browser1", image="navButtonBrowse.png",
                                                command=pm.Callback(selectDiff, ws))
                            with pm.frameLayout(l="File Attributes", en=True):
                                # pm.checkBox("cbUdim1", l="UDIM", v=False)
                                pm.optionMenu(
                                    "opm1", l="Color Space", en=True, acc=True, cc=getAttrsDiff)
                                pm.menuItem("miRgb1", l="sRGB")
                                pm.menuItem("miRaw1", l="Raw")
                                pm.checkBox("cbALdiff", l="Alpha is Luminance",
                                            v=False, en=True)

                    # Metalness Settings
                    with pm.frameLayout("fl_met", l="Metalness", cll=True, cl=True, bgs=True, w=440) as frame_met:
                        with pm.verticalLayout(ratios=[1, 3], spacing=5):
                            with pm.horizontalLayout(ratios=[12, 1], spacing=10):
                                # pm.checkBox("cbMet", l="Enable", v=True)
                                pm.textField("tfMetalness", text="not selected",
                                             cc=pm.Callback(setMetalMapPath, ws), h=20, w=230)
                                pm.symbolButton("browser2", image="navButtonBrowse.png",
                                                command=pm.Callback(selectMetal, ws))
                            with pm.frameLayout(l="File Attributes", en=True):
                                # pm.checkBox("cbUdim2", l="UDIM", v=False)
                                pm.optionMenu(
                                    "opm2", l="Color Space", en=True, acc=True, cc=getAttrsMet)
                                pm.menuItem("miRgb2", l="sRGB")
                                pm.menuItem("miRaw2", l="Raw")
                                pm.checkBox("cbALmet", l="Alpha is Luminance",
                                            v=False, en=True)

                    # Roughness Settings
                    with pm.frameLayout("fl_rou", l="Roughness", cll=True, cl=True, bgs=True, w=440) as frame_rou:
                        with pm.verticalLayout(ratios=[1, 3], spacing=5):
                            with pm.horizontalLayout(ratios=[12, 1], spacing=10):
                                # pm.checkBox("cbRou", l="Enable", v=True)
                                pm.textField("tfRoughness", text="not selected",
                                             cc=pm.Callback(setRoughMapPath, ws), h=20, w=230)
                                pm.symbolButton("browser3", image="navButtonBrowse.png",
                                                command=pm.Callback(selectRough, ws))
                            with pm.frameLayout(l="File Attributes", en=True):
                                # pm.checkBox("cbUdim3", l="UDIM", v=False)
                                pm.optionMenu(
                                    "opm3", l="Color Space", en=True, acc=True, cc=getAttrsRou)
                                pm.menuItem("miRgb3", l="sRGB")
                                pm.menuItem("miRaw3", l="Raw")
                                pm.checkBox("cbALrou", l="Alpha is Luminance",
                                            v=False, en=True)

                    # Normal Settings
                    with pm.frameLayout("fl_nor", l="Normal", cll=True, cl=True, bgs=True, w=440) as frame_nor:
                        with pm.verticalLayout(ratios=[1, 3], spacing=5):
                            with pm.horizontalLayout(ratios=[12, 1], spacing=10):
                                # pm.checkBox("cbNor", l="Enable", v=True)
                                pm.textField("tfNormal", text="not selected",
                                             cc=pm.Callback(setNormalMapPath, ws), h=20, w=230)
                                pm.symbolButton("browser4", image="navButtonBrowse.png",
                                                command=pm.Callback(selectNormal, ws))
                            with pm.frameLayout(l="File Attributes", en=True):
                                # pm.checkBox("cbUdim4", l="UDIM", v=False)
                                pm.optionMenu(
                                    "opm4", l="Color Space", en=True, acc=True, cc=getAttrsNor)
                                pm.menuItem("miRgb4", l="sRGB")
                                pm.menuItem("miRaw4", l="Raw")
                                pm.checkBox("cbALnor", l="Alpha is Luminance",
                                            v=False, en=True)

                    # Displacement Settings
                    with pm.frameLayout("fl_dis", l="Displacement", cll=True, cl=True, bgs=True, w=440) as frame_dis:
                        with pm.verticalLayout(ratios=[1, 3], spacing=5):
                            with pm.horizontalLayout(ratios=[12, 1], spacing=10):
                                pm.textField("tfDisplace", text="not selected",
                                             cc=pm.Callback(setDisplaceMapPath, ws), h=20, w=230)
                                pm.symbolButton("browser4", image="navButtonBrowse.png",
                                                command=pm.Callback(selectDisplace, ws))
                            with pm.frameLayout(l="File Attributes", en=True):
                                pm.optionMenu(
                                    "opm4", l="Color Space", en=True, acc=True, cc=getAttrsDis)
                                pm.menuItem("miRgb4", l="sRGB")
                                pm.menuItem("miRaw4", l="Raw")
                                pm.checkBox("cbALdis", l="Alpha is Luminance",
                                            v=False, en=True)

                    with pm.verticalLayout():
                        pm.button(label="Create Material", w=440,
                                  command=pm.Callback(createAll, ws))


def run():
    initAttrs()
    openUi()


run()

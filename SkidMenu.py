# ****************************************** S K I D     M E N U ******************************************

import maya.cmds as cmds
import maya.mel as mel

def createMenu():

	gMainWindow = mel.eval('$temp1 = $gMainWindow')
	SkidToolsMenu = cmds.menu(parent = gMainWindow, label = "Skid Tools")
	
	# UTILS
	cmds.menuItem(bld=True,l='UTILS')
	cmds.menuItem(parent = SkidToolsMenu, label = "Increment and Save", \
		image='SkidMenu_versionUp.png', \
		c='import commonTools; \
		reload(commonTools); \
		commonTools.versionUp()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Renamer", \
		image='SkidMenu_renamer.png', \
		c='import CompactRenamer as ComRen; \
		MCCR = ComRen.MainClassCompactRenamer(); \
		MCCR.comRenUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Init cameras", \
		image='SkidMenu_cam.png', \
		c='import commonTools; \
		reload(commonTools); \
		commonTools.initCam()')

	# ASSETS
	cmds.menuItem(divider=True)
	cmds.menuItem(bld=True,l='ASSETS')
	cmds.menuItem(parent = SkidToolsMenu, label = "Animation Tools", \
		image='SkidMenu_anim.png', \
		c='import animationUI; \
		reload(animationUI); \
		animationUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Assets Tools", \
		image='SkidMenu_assets.png', \
		c='import assetsUI; \
		reload(assetsUI); \
		assetsUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Lookdev Tools", \
		image='SkidMenu_lookdev.png', \
		c='import lookdevUI; \
		reload(lookdevUI); \
		lookdevUI.CreateUI()')
	# cmds.menuItem(parent = SkidToolsMenu, label = "Previz Tools", \
	# 	image='SkidMenu_previz.png', \
	# 	c='import previzUI; \
	# 	reload(previzUI); \
	# 	previzUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Rigging Tools", \
		image='SkidMenu_rig.png', en=False)

	# SHOTS
	cmds.menuItem(divider=True)
	cmds.menuItem(bld=True,l='SHOTS')
	cmds.menuItem(parent=SkidToolsMenu, label="Set Dress Tools", \
		image='SkidMenu_setDress.png', \
		c='import setDressUI; \
		reload(setDressUI)')
	cmds.menuItem(parent=SkidToolsMenu, label="Forest Tools", \
		image='SkidMenu_forest.png', \
		c='import forestUI; \
		reload(forestUI)')
	cmds.menuItem(parent = SkidToolsMenu, label = "Render Tools", \
		image='SkidMenu_render.png',
		c='import renderUI; \
		reload(renderUI); \
		renderUI.CreateUI()')
	
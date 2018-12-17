# ****************************************** S K I D     M E N U ******************************************

import maya.cmds as cmds
import maya.mel as mel

def createMenu():

	gMainWindow = mel.eval('$temp1 = $gMainWindow')
	SkidToolsMenu = cmds.menu(parent = gMainWindow, label = "Skid Tools")
	
	cmds.menuItem(parent = SkidToolsMenu, label = "Increment and Save", \
		c='import commonTools; \
		reload(commonTools); \
		commonTools.versionUp()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Renamer", \
		c='import CompactRenamer as ComRen; \
		MCCR = ComRen.MainClassCompactRenamer(); \
		MCCR.comRenUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Animation Tools", \
		c='import animationUI; \
		reload(animationUI); \
		animationUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Assets Tools", \
		c='import assetsUI; \
		reload(assetsUI); \
		assetsUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Lookdev Tools", \
		c='import lookdevUI; \
		reload(lookdevUI); \
		lookdevUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Previz Tools", \
		c='import previzUI; \
		reload(previzUI); \
		previzUI.CreateUI()')
	cmds.menuItem(parent = SkidToolsMenu, label = "Render Tools", \
		c='import renderUI; \
		reload(renderUI); \
		renderUI.CreateUI()',en=False)
	cmds.menuItem(parent = SkidToolsMenu, label = "Rigging Tools",en=False)
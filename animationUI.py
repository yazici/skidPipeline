# ****************************************** S K I D     A N I M     U I ******************************************

import maya.cmds as cmds
import maya.mel as mel
import os
import commonTools
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

animScriptsPath = '//Merlin/3d4/skid/09_dev/toolScripts/publish/animScripts'
riggedAssets = ['propsBrevell','characterEthan','propsEthanHelmet','propsWerner','propsAltonHelmet']
chosenRig = 'propsBrevell'
animationWindow = "animationWindow"

# ****************************************** F U N C T I O N S ******************************************

def chooseRig(item,*args):
	global chosenRig
	chosenRig = item

def callImportRig(*args):
	import commonTools
	reload(commonTools)
	commonTools.importAssetMa(chosenRig)

def callConstraintCar(*args):
	import animationTools
	reload(animationTools)
	animationTools.constraintCar(chosenRig)

def callToggleConstraintCar(*args):
	import animationTools
	reload(animationTools)
	animationTools.toggleConstraintCar(chosenRig)

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200,h=30)
	template.define(text,w=100,h=30)

	try :
		cmds.deleteUI(animationWindow)
	except RuntimeError :
		pass

	with window(animationWindow, title='Animation Tools',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():

				with frameLayout('Animation Plugins'):
					with columnLayout():
						button(l='bhGhost', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/bhGhost.mel"\'); \
							mel.eval(\'bhGhost()\')' %animScriptsPath)
						button(l='dkAnim', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/dkAnim-v0.7-.mel"\'); \
							mel.eval(\'dkAnim()\')' %animScriptsPath)
						button(l='arcTracker', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/arctracker110.mel"\'); \
							mel.eval(\'arctracker110()\')' %animScriptsPath)		

				with frameLayout('Animation Tools'):
					with rowColumnLayout():
						text(l='Current asset : ')
						with optionMenu(changeCommand=chooseRig):
							for asset in riggedAssets:
								menuItem(l=asset)
					with columnLayout():
						button(l='Import asset',c=callImportRig)
						button(l='Constraint asset to selected',c=callConstraintCar)
						button(l='Toggle constraint',c=callToggleConstraintCar)

						# button(l='Create Speed Attribute', \
						# 	c='import animationTools; \
						# 	reload(animationTools); \
						# 	animationTools.createSpeedAttribute()')

				with frameLayout('Playblast'):
					with columnLayout():
						button(l='Playblast Animation', \
							c='import animationTools; \
							reload(animationTools); \
							animationTools.playblastAnim()')
			
				# with frameLayout('Export'):
				# 	with columnLayout():
				# 		button(l='Export Selected', \
				# 			c='import animationTools; \
				# 			reload(animationTools); \
				# 			animationTools.exportAbcRfM()')
				# 		button(l='Publish Animations', \
				# 		c='import animationTools; \
				# 		reload(animationTools); \
				# 		animationTools.publishAnimations(%s)' % riggedAssets)

				with frameLayout('Nomenclatures'):
						button(l='Afficher nomenclatures',h=30, \
							c='import commonTools; \
							reload(commonTools); \
							commonTools.showNomenclatures()')

CreateUI()
import maya.cmds as cmds
import maya.mel as mel
import os
import commonTools
from pymel.core import *


# **************** GLOBAL VARIABLES ****************

animScriptsPath = '//Merlin/3d4/skid/09_dev/toolScripts/publish/animScripts'
riggedAssets = ['propsEthanHelmet','propsAltonHelmet','characterRay','characterRay_pos','propsBrevell','propsWerner','propsKriz']
chosenRig = []
animationWindow = "animationWindow"

# **************** FUNCTIONS ****************

def chooseRig(item,*args):
	global chosenRig
	chosenRig = item

def callImportRig(*args):
	import commonTools
	reload(commonTools)
	commonTools.importAssetMa(chosenRig)

# **************** INTERFACE ****************

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200)

	try :
		cmds.deleteUI(animationWindow)
	except RuntimeError :
		pass

	with window(animationWindow, title='Animation Tools',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():
				with frameLayout('Import rigg'):
					with rowColumnLayout():
						with optionMenu(changeCommand=chooseRig):
							for asset in riggedAssets:
								menuItem(l=asset)
							button(l='Import',w=100,h=25,c=callImportRig)

				with frameLayout('Animation Plugins'):
					with columnLayout():
						button(l='bhGhost',c='import maya.mel as mel; mel.eval(\'source "%s/bhGhost.mel"\'); mel.eval(\'bhGhost()\')' %animScriptsPath)
						# button(l='Open TweenMachine',c='mel.eval(\'source "%s/tweenMachine.mel"\')' %animScriptsPath)
						button(l='dkAnim',c='import maya.mel as mel; mel.eval(\'source "%s/dkAnim-v0.7-.mel"\'); mel.eval(\'dkAnim()\')' %animScriptsPath)
						button(l='arcTracker',c='import maya.mel as mel; mel.eval(\'source "%s/arctracker110.mel"\'); mel.eval(\'arctracker110()\')' %animScriptsPath)

				with frameLayout('Animation Tools'):
					with columnLayout():
						button(l='Create Speed Attribute',c='import animationTools; reload(animationTools); animationTools.createSpeedAttribute()')
						button(l='Playblast Animation',c='import animationTools; reload(animationTools); animationTools.playblastAnim()')
			
				with frameLayout('Export'):
					with columnLayout():
						button(l='Export Selected',c='import animationTools; reload(animationTools); animationTools.exportAbcRfM()')
						button(l='Publish Animations',c='import animationTools; reload(animationTools); animationTools.publishAnimations(%s)' % riggedAssets) #with backups and playblast
						
				with frameLayout('Nomenclatures'):
						button(label='Afficher nomenclatures',h=30,c='import commonTools; reload(commonTools); commonTools.showNomenclatures()')

CreateUI()
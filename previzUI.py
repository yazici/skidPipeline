# **************** SKID PREVIZ UI ****************

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import commonTools
import previzTools
from pymel.core import *

# **************** GLOBALS ****************

# **************** FUNCTIONS ****************

# def CreateUI(*args):
# 	if cmds.window("SkidPrevizTools", exists = True): #check to see if the window exists
# 		cmds.deleteUI("SkidPrevizTools")

# 	cmds.window("SkidPrevizTools", w = 300, h = 275)
# 	cmds.columnLayout(adjustableColumn=True, w=300)

# 	cmds.text(label='PREVIZ RENDER',h=25)
# 	cmds.button(label='Import shot alembics',w=300,h=50,c='import previzTools; reload(previzTools); previzTools.importShotAlembics()')
# 	cmds.button(label='Import shaders for alembics',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.importShaders()')
# 	cmds.button(label='Assign shaders',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.assignShaders()')
# 	cmds.button(label='Import Alembic as Reference',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.referenceAlembic()')
# 	cmds.button(label='Set Frame Range From Camera',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.setShot()')
# 	cmds.button(label='Publish shot',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.publishShot()')
	
# 	cmds.button(label='Nomenclatures',h=30,c='import commonTools; reload(commonTools); commonTools.showNomenclatures()')

# 	cmds.showWindow("SkidPrevizTools")

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200)

	try :
		cmds.deleteUI('SkidPrevizTools')
	except RuntimeError :
		pass

	with window('SkidPrevizTools', title='Previz Tools',menuBar=True,menuBarVisible=True) as win:
			with template:
				with columnLayout():
					with frameLayout('Previz render'):
						with columnLayout():
							button(label='Import shot alembics',w=300,h=50,c='import previzTools; reload(previzTools); previzTools.importShotAlembics()')
							button(label='Import shaders for alembics',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.importShaders()')
							button(label='Assign shaders',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.assignShaders()')
							button(label='Import Alembic as Reference',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.referenceAlembic()')
							button(label='Set Frame Range From Camera',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.setShot()')
							button(label='Publish shot',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.publishShot()')
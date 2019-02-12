# ****************************************** S K I D     A N I M     U I ******************************************

import maya.cmds as cmds
from pymel.core import *

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200)

	try :
		cmds.deleteUI('setDressWindow')
	except RuntimeError :
		pass

	with window('setDressWindow', title='Set Dress Tools',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():
				with frameLayout('References'):
					with rowColumnLayout():
						button(l='Unload references from selection',\
							c='import setDressTools; \
							reload(setDressTools); \
							setDressTools.unloadSelected()')

CreateUI()
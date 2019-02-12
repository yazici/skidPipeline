# ****************************************** S K I D     A S S E T S     U I ******************************************

import maya.cmds as cmds
from functools import partial
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

assetsWindow = 'assetsWindow'

# ****************************************** F U N C T I O N S ******************************************

def addID(ID,*args):
	sel = cmds.ls(selection=True)
	for i in sel :
		if '_ID' in i:
			cmds.warning(i+' already has an ID')
		else :
			cmds.rename(i,i+'_ID'+ID)
			# import assetsTools
			# assetsTools.fixShapesNames()

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200)
	template.define(textField,h=35)

	try :
		cmds.deleteUI(assetsWindow)
	except RuntimeError :
		pass

	with window(assetsWindow, title='Assets Tools',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():
				with frameLayout('Prepare geometries'):
					with columnLayout():
						button(label = 'Asset Checker', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.checkDatAss()')
						button(label='Fix duplicate names', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.duplicateNamesDialog()')
						button(label = 'Fix shapes names', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.fixShapesNames()')
						button(label = 'Fix Normals', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.fixNormals()')
						button(label = 'Select objects with no UV', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.selObjWithoutUV()')
				

				with frameLayout('Basic rig'):
					with columnLayout():
						button(l='Create basic rig for asset', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.basicAssetRig()')
				

				with frameLayout('Prepare for render'):
					with columnLayout():
						with rowLayout(numberOfColumns=3,ad3=2):
							button(l='Material ID',w=75,en=False)
							textField(w=170,enterCommand=lambda *args: addID(args[0]),aie=True)
							button(label='Remove',w=50, \
								c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.removeID()')
						with rowLayout(numberOfColumns=2):
							button(label='Attach Subdiv Scheme',w=149, \
								c='import commonTools; \
								reload(commonTools); \
								commonTools.RfMsubdivScheme(1)')
							button(label="Detach Subdiv Scheme",w=148, \
								c='import commonTools; \
								reload(commonTools); \
								commonTools.RfMsubdivScheme(0)')

				with frameLayout('Export / Publish Asset'):
					with columnLayout():
						with rowLayout(numberOfColumns=4,ad4=2):
							button(label='Export .ma',w=73, \
								c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.exportMayaAscii()')
							button(label='Export .abc',w=73, \
								c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.exportAbcRfM()')
							button(label='Export GPU',w=73, \
								c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.exportGPUcache()')
							button(label='Export RIB',w=74, \
								c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.exportRIBarchive()', \
								en=False)
						button(label='Publish asset', \
							c='import assetsTools; \
							reload(assetsTools); \
							assetsTools.publishAsset()', \
							en=False)

				with frameLayout('Nomenclatures'):
					with columnLayout():
						button(label='Nomenclatures',h=30, \
							c='import commonTools; \
							reload(commonTools); \
							commonTools.showNomenclatures()')
CreateUI()
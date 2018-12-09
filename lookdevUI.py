import maya.cmds as cmds
import os
from functools import partial
import commonTools
import lookdevTools
from pymel.core import *

# **************** GLOBAL VARIABLES ****************

lookdevWindow = "lookdevWindow"
lookdevScenePath = os.path.abspath('//merlin/3d4/skid/09_dev/toolScripts/lookdev/lookdevSetup/LookdevSetup.ma')
hdri_folder = os.path.abspath('//Merlin/3d4/skid/04_asset/SkidLibrary/HDRI')
hdri_files = os.listdir(hdri_folder)
grpName = 'LookdevSetup:GRP_LookdevSetup'
lookdevPreset = 'SKID_LookdevSetup'
scenePath = cmds.workspace(sn=True,q=True)

# **************** FUNCTIONS ****************

def chooseHDRfile(item,*args):
	resolveHDRpath = os.path.join(hdri_folder,item)
	cmds.setAttr('LookdevSetup:PxrDomeLight_HDRI.lightColorMap','%s' %resolveHDRpath,type='string')

# **************** INTERFACE ****************

def CreateUI(*args):
	# Try loading renderman and check version
	cmds.evalDeferred("cmds.loadPlugin(\"RenderMan_for_Maya.py\")")
	from rfm2.config import cfg
	rmanversion = cfg().rfm_env['versions']['rfm']
	print rmanversion
	if rmanversion != "22.1" :
		commonTools.areeeeett()
		cmds.evalDeferred("cmds.warning('Wrong Renderman for Maya version (installed version is %s), should be 22.1')" % rmanversion)
	else :
		# define template
		template = uiTemplate(force=True)
		template.define(button,h=35,w=300,align='left')
		template.define(optionMenu,h=35,w=300)
		template.define(frameLayout, borderVisible=True, labelVisible=True)
		template.define(text,h=25)
		template.define(rowLayout)

		try :
			cmds.deleteUI(lookdevWindow)
		except RuntimeError :
			pass

		with window(lookdevWindow, title="Skid Lookdev Tools",menuBar=True,menuBarVisible=True) as win:
			with template:
				with frameLayout(l='Project'):
					text('PROJECT IS SET TO')
					text(scenePath)

				with frameLayout('Scene Setup'):
					with columnLayout():
						with rowLayout(numberOfColumns=3,ad3=1):
							button(label='Import lookdev scene',w=198,c='import lookdevTools; reload(lookdevTools); lookdevTools.importLookdevScene()')
							button(label='Hide',w=48,c='import lookdevTools; reload(lookdevTools); lookdevTools.hideLookdevScene()')
							button(label='Reload',w=49,c='import lookdevTools; reload(lookdevTools); lookdevTools.reloadLookdevScene()')
						button(l='Load Render Settings',c='import commonTools; reload(commonTools); commonTools.loadRenderSettings("%s")' %lookdevPreset)
						# global chosenHDR
						optionMenu(changeCommand=chooseHDRfile)
						for file in hdri_files:
							menuItem(label=file)

				with frameLayout('Shading'):
					with columnLayout():
						with rowLayout(numberOfColumns=2,ad2=1):
							with columnLayout():
								button(l='Create PxrSurface network',c='import lookdevTools; reload(lookdevTools); lookdevTools.createPxrSurfaceNetwork()')
								button(l='Create PxrLayer network',c='import lookdevTools; reload(lookdevTools); lookdevTools.createPxrLayerNetwork()',en=False)
								button(l='Convert PxrSurface to PxrLayer',c='import lookdevTools; reload(lookdevTools); lookdevTools.convertPxrSurfaceToLayer()',en=False)

				with frameLayout('Turn'):
					with columnLayout():
						with rowLayout(numberOfColumns=2,ad2=1):
							button(label="Create turn locator",w=248,c='import lookdevTools; reload(lookdevTools); lookdevTools.create_turn_loc()')
							button(label="Delete",  w=49, c='import lookdevTools; reload(lookdevTools); lookdevTools.delete_turn_loc()')
						with rowLayout(numberOfColumns=3,ad3=2):
							button(label="%i frames" % 8, w=98,c='import lookdevTools; reload(lookdevTools); lookdevTools.change_frames_number(8)')
							button(label="%i frames" % 50, w=98,c='import lookdevTools; reload(lookdevTools); lookdevTools.change_frames_number(50)')
							button(label="%i frames" % 100, w=99,c='import lookdevTools; reload(lookdevTools); lookdevTools.change_frames_number(100)')

				with frameLayout('Nomenclatures'):
					button(label='Afficher nomenclatures',h=30,c='import commonTools; reload(commonTools); commonTools.showNomenclatures()')

CreateUI()
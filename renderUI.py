# ****************************************** S K I D    R E N D E R    U I ******************************************

import maya.cmds as cmds
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

pathTracerPreset = '.json'
unifiedPreset = '.json'

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	# Load Renderman and check version
	cmds.evalDeferred("cmds.loadPlugin(\"RenderMan_for_Maya.py\")")
	from rfm2.config import cfg
	rmanversion = cfg().rfm_env['versions']['rfm']
	print rmanversion
	if rmanversion != "22.1" :
		commonTools.areeeeett()
		cmds.evalDeferred("cmds.warning('Wrong Renderman for Maya version (installed version is %s), should be 22.1')" % rmanversion)
	else :
		template = uiTemplate('ExampleTemplate', force=True)
		template.define(button, w=300, h=35, align='left')
		template.define(frameLayout, borderVisible=True, labelVisible=True)
		template.define(rowColumnLayout,numberOfColumns=2)
		template.define(optionMenu,w=200)

		try :
			deleteUI('renderWindow')
		except RuntimeError :
			pass

		with window('renderWindow', title='Previz Tools',menuBar=True,menuBarVisible=True) as win:
				with template:
					with columnLayout():
						with frameLayout('Prepare Scene'):
							with columnLayout():
								button(label='Import shot alembics',w=300,h=50,c='import previzTools; reload(previzTools); previzTools.importShotAlembics()')
								button(label='Import shaders for alembics',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.importShaders()')
								button(label='Assign shaders',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.assignShaders()')
								button(label='Import Alembic as Reference',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.referenceAlembic()')
								button(label='Set Frame Range From Camera',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.setShot()')
								button(label='Publish shot',w=300,h=30,c='import previzTools; reload(previzTools); previzTools.publishShot()',en=False)
						with frameLayout('Rendering'):
							with columnLayout():
								button(l='Load Render Settings for PathTracer',c='import commonTools; reload(commonTools); commonTools.loadRenderSettings("%s")' %pathTracerPreset,en=False)
								button(l='Load Render Settings for Unified',c='import commonTools; reload(commonTools); commonTools.loadRenderSettings("%s")' %unifiedPreset,en=False)
CreateUI()
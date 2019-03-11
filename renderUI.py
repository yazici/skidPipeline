# ****************************************** S K I D    R E N D E R    U I ******************************************

import maya.cmds as cmds
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

pathTracerPreset = 'SKID_shot_PathTracer.json'
unifiedPreset = '.json'

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	# Load Renderman and check version
	cmds.evalDeferred("cmds.loadPlugin(\"RenderMan_for_Maya.py\")")
	from rfm2.config import cfg
	rmanversion = cfg().rfm_env['versions']['rfm']
	print rmanversion
	if rmanversion != "22.3" :
		commonTools.areeeeett()
		cmds.evalDeferred("cmds.warning('Wrong Renderman for Maya version (installed version is %s), should be 22.3')" % rmanversion)
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

		with window('renderWindow', title='Render Tools',menuBar=True,menuBarVisible=True) as win:
				with template:
					with columnLayout():

						with frameLayout('Importomatic'):
							with columnLayout():
								button(l='Import shot camera', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.importShotCamera()')
								button(l='Set Frame Range From Camera', \
									c='import previzTools;  \
									reload(previzTools); \
									previzTools.setShot()')

							with columnLayout():
								button(l='Import shot animations', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.importShotAlembics()')
								button(l='Import shaders for animations', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.importShaders()')
								button(l='Asign shaders for animations', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.assignShaders()')

							with columnLayout():
								button(l='Import shot casting', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.readCasting()')
								button(l='Import shot forest', \
									c='import renderTools; \
									reload(renderTools); \
									renderTools.importForest()')

						with frameLayout('Import'):
							with columnLayout():
								button(l='Import Alembic as Reference', \
									c='import previzTools; \
									reload(previzTools); \
									previzTools.referenceAlembic()')

						with frameLayout('Geometries'):
							with columnLayout() :
								with rowLayout(numberOfColumns=2):
										button(l='Attach Subdiv Scheme',w=149, \
											c='import commonTools; \
											reload(commonTools); \
											commonTools.RfMsubdivScheme(1)')
										button(l="Detach Subdiv Scheme",w=148, \
											c='import commonTools; \
											reload(commonTools); \
											commonTools.RfMsubdivScheme(0)')
								with rowLayout(numberOfColumns=2):
									button(l='Inherit Trace Bias',w=149, \
											c = 'import renderTools ; \
											reload(renderTools) ; \
											renderTools.autoBias(True)')
									button(l='Divide Bias by 10',w=148, \
											c = 'import renderTools ; \
											reload(renderTools) ; \
											renderTools.autoBias(False)')
								with rowLayout(numberOfColumns=2):
									button(l='Inherit Motion Samples',w=149, \
											c = 'import renderTools ; \
											reload(renderTools) ; \
											renderTools.motionSamples(True)')
									button(l='Add 1 motion sample',w=148, \
											c = 'import renderTools ; \
											reload(renderTools) ; \
											renderTools.motionSamples(False)')
								
						
						with frameLayout('Rendering'):
							with columnLayout():
								button(l='Load Render Settings for PathTracer', \
									c='import commonTools; \
									reload(commonTools); \
									commonTools.loadRenderSettings("%s")' %pathTracerPreset)
								button(l='Load Render Settings for Unified', \
									c='import commonTools; \
									reload(commonTools); \
									commonTools.loadRenderSettings("%s")' %unifiedPreset, \
									en=False)

						with frameLayout('Nomenclatures'):
							with columnLayout():
								button(label='Nomenclatures',h=30, \
									c='import commonTools; \
									reload(commonTools); \
									commonTools.showNomenclatures()')


								
CreateUI()
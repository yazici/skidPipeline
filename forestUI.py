# ****************************************** S K I D     F O R E S T     U I ******************************************

import maya.cmds as cmds
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

forestWindow = "forestWindow"

# ****************************************** F U N C T I O N S ******************************************

def call_fireHoudini(*_):
	VfocalLength = floatSliderGrp(focalLength,q=True,v=True)
	Vtop = floatSliderGrp(mtop,q=True,v=True)
	Vright = floatSliderGrp(mright, q=True, v=True)
	Vbot = floatSliderGrp(mbot,q=True,v=True)
 	Vleft= floatSliderGrp(mleft,q=True,v=True)
 	Vdepth = floatSliderGrp(depth,q=True,v=True)
 	import forestTools
 	reload(forestTools)
 	forestTools.fireHoudini(VfocalLength,Vtop,Vright,Vbot,Vleft,Vdepth)

# ****************************************** I N T E R F A C E ******************************************

template = uiTemplate('ExampleTemplate', force=True)
template.define(button, w=300, h=35, align='left')
template.define(frameLayout, borderVisible=True, labelVisible=True)
template.define(rowColumnLayout,numberOfColumns=1)
template.define(optionMenu,w=200)
template.define(floatSliderGrp,w=300,h=25,f=True,min=0.0,max=1.0,s=0.1,v=0.1,cl3=('left','left','left'),cw3=(80,80,140))

try :
	cmds.deleteUI(forestWindow)
except RuntimeError :
	pass

with window(forestWindow, title='Forest Tools',menuBar=True,menuBarVisible=True) as win:
	with template:
		with columnLayout():
			
			with frameLayout('Camera setup'):
				with rowColumnLayout():
					button(l='Import shot camera', \
						c='import renderTools; \
						reload(renderTools); \
						renderTools.importShotCamera()')
					button(l='Set Frame Range From Camera', \
						c='import previzTools;  \
						reload(previzTools); \
						previzTools.setShot()')

			with frameLayout('Create point cloud'):
				with rowColumnLayout():
					focalLength = floatSliderGrp(l='Focal Length',min=5,max=300,s=1,v=50)
					mtop = floatSliderGrp(l='Margin top')
					mright = floatSliderGrp(l='Margin right')
					mbot = floatSliderGrp(l='Margin bottom')
					mleft = floatSliderGrp(l='Margin left')
					depth = floatSliderGrp(l='Depth (m)',min=100,max=2000,s=10,v=500)
					b = cmds.button('Compute point cloud')
					button(b, e=True, c=call_fireHoudini)
			
			with frameLayout('Maya instancer'):
				with rowColumnLayout():
					# button(l='Load Houdini Engine for Maya', \
					# 	c='import forestTools; \
					# 	reload(forestTools); \
					# 	forestTools.loadHoudiniEngine()')
					button(l='Load point cloud', \
						c='import forestTools; \
						reload(forestTools); \
						forestTools.loadShotPoints()')
					button(l='Scatter !', \
						c='import forestTools; \
						reload(forestTools); \
						forestTools.createInstancer()')
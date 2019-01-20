# ****************************************** S K I D     F O R E S T     U I ******************************************

import maya.cmds as cmds
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

forestWindow = "forestWindow"

# ****************************************** F U N C T I O N S ******************************************

def call_fireHoudini(*_):
	Vtop = floatSliderGrp(mtop,q=True,v=True)
	Vright = floatSliderGrp(mright, q=True, v=True)
	Vbot = floatSliderGrp(mbot,q=True,v=True)
 	Vleft= floatSliderGrp(mleft,q=True,v=True)
 	import forestTools
 	reload(forestTools)
 	forestTools.fireHoudini(Vtop,Vright,Vbot,Vleft)

# ****************************************** I N T E R F A C E ******************************************

template = uiTemplate('ExampleTemplate', force=True)
template.define(button, w=300, h=35, align='left')
template.define(frameLayout, borderVisible=True, labelVisible=True)
template.define(rowColumnLayout,numberOfColumns=2)
template.define(optionMenu,w=200)
template.define(floatSliderGrp,w=300,h=30,f=True,min=0.0,max=1.0,s=0.1,v=0.1,cl3=('left','left','left'),cw3=(80,80,140))

try :
	cmds.deleteUI(forestWindow)
except RuntimeError :
	pass

with window(forestWindow, title='Forest Tools',menuBar=True,menuBarVisible=True) as win:
	with template:
		with columnLayout():
			with frameLayout('Point Cloud'):
				mtop = floatSliderGrp(l='Marge haut')
				mright = floatSliderGrp(l='Marge droite')
				mbot = floatSliderGrp(l='Marge bas')
				mleft = floatSliderGrp(l='Marge gauche')				
				b = cmds.button('print value')
				button(b, e=True, c=call_fireHoudini)
# ****************************************** S K I D     S E T D R E S S     T O O L S ******************************************

import maya.cmds as cmds

referenceNodes = cmds.ls(type='reference')

# ****************************************** F U N C T I O N S ******************************************

def RNfromSelection():
	'''This will select every master reference node for selected geometries that has a controller'''
	# 1. controllers from selection
	ctrls = []
	for n in cmds.ls(selection=True,referencedNodes=True) :
		if not 'ctrl' in n:
			pass
		else :
			ctrls.append(n)
	# 2. master reference node from ctrl
	rn = []
	for ctrl in ctrls:
		n = cmds.referenceQuery(ctrl,referenceNode=True,p=True)
		rn.append(n)
	return rn

def allRN():
	# Returns all Reference nodes in the scnene
	rn = []
	for n in cmds.ls():
		if not 'RN' in n:
			pass
		else:
			rn.append(n)
	return rn


def unloadSelected():
	for n in RNfromSelection():
		cmds.file(referenceNode=n,unloadReference=True)

def loadSelected():
	for n in RNfromSelection():
		cmds.file(referenceNode=n,loadReference=True)


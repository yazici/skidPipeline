# ****************************************** S K I D    R E N D E R    T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import commonTools,os

# ****************************************** G L O B A L S ******************************************



# ****************************************** F U N C T I O N S ******************************************

def readCasting():
	'''This will read the cast file for the current shot and import'''
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	shotName = os.path.split(scenePath)[1]
	castFile = scenePath+'/data/'+shotName+'.cast'

	# Load ATOM plugin
	cmds.loadPlugin('atomImportExport.mll')

	# Test if cast file exists
	if not os.path.exists(castFile):
		cmds.warning('Cast file does not exist for this shot. Should be : '+castFile)
		return

	# Test if atom file exists
	atomFile = scenePath+'/data/'+shotName+'.atom'
	if not os.path.isfile(atomFile):
		cmds.warning('Atom file does not exist for this shot. Should be : '+atomFile)
		return

	# User prompt before import
	with open(castFile) as f:
		for i, l in enumerate(f):
			pass
	lines = i+1
	message = 'You are about to import the shot casting which contains %s assets. This will take some time, consider heading to the nearest coffee machine. Continue ?'%lines
	confirm = cmds.confirmDialog(title='Import shot casting',message=message, button=['Continue','Cancel'], \
		defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel')
	if confirm != 'Continue':
		return

	# Read file
	with open(castFile) as f:
		cast = f.readlines()
		cast = [x.strip() for x in cast]
	f.close()

	# Create group
	masterGrp = cmds.group(em=True,name='importedCasting_grp')

	# Deduce file path and namespace
	ctrls = []
	for l in cast:
		l = l.split('.ma')
		asset = l[0]+'.ma'
		import re
		ns = os.path.split(l[0])[1]+re.sub('[^0-9]','',l[1])

		# Reference file
		print('// Importing : '+asset+' with namespace : '+ns+' //')
		cmds.file(asset,r=True,type='mayaAscii',ignoreVersion=True,gl=True,ns=ns,returnNewNodes=True)
		master = os.path.split(l[0])[1]
		master = ns+':'+master+'_rig:'+master+'_master'
		cmds.parent(master,masterGrp)

		# Apply ATOM transforms
		ctrls.append(ns+':'+os.path.split(l[0])[1]+'_rig:'+os.path.split(l[0])[1]+'_ctrl')
	# cmds.select(ctrls,r=True)
	cmds.select(clear=True)
	for ctrl in ctrls :
		cmds.select(ctrl,add=True)
	mel.eval('file -import -type "atomImport" -ra true -namespace "%s" -options ";;targetTime=3;option=insert;match=string;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=%s;" "%s";'%(ns,scenePath+'/data/',atomFile))


def openCastFile(castFile):
	'''This will open a window with the content of current shot casting'''
	from functools import partial
	if cmds.window(castFile,ex=True):
		cmds.deleteUI(castFile)
	cmds.window(castFile)
	cmds.columnLayout(adjustableColumn=True)
	file = open(castFile,'r') 
	readText = str(file.read())
	cmds.scrollField(tx=readText,ed=False,wordWrap=True,h=500,w=700)
	cmds.setParent("..")
	cmds.showWindow()

def importShotCamera():
	'''This will import the current shot camera'''
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	sceneName = os.path.split(scenePath)[1]

	cam = scenePath+'/abc/'+sceneName+'.abc'
	if not os.path.exists(cam):
		cmds.warning('No camera found, should be : '+cam)
	else :
		cmds.file(cam,r=True,type='Alembic',ignoreVersion=True,gl=True,ns=sceneName)
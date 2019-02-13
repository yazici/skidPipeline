# ****************************************** S K I D    R E N D E R    T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import commonTools,os

# ****************************************** G L O B A L S ******************************************



# ****************************************** F U N C T I O N S ******************************************

def importCast():
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	sceneName = os.path.split(scenePath)[1]
	castFile = scenePath+'/data/'+sceneName+'.cast'

	message = 'Import shot casting for ' + sceneName + ' ? (This can take some time)'
	confirm = cmds.confirmDialog(title='Publish shot casting',message=message, button=['Import','Open cast file','Cancel'], \
		defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel')
	if confirm == 'Cancel':
		return
	elif confirm == 'Open cast file':
		openCastFile(castFile)
		return
	
	# read castFile and put every line in a list
	with open(castFile) as f:
		fileList = f.readlines()
		fileList = [x.strip() for x in fileList]

	# if list contains bracket, set namespace
	# for f in fileList:
	toBlast = [k for k in rf if '{' in k]





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
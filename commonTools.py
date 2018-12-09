import maya.cmds as cmds
import datetime
import os
import sys

# ****************************************** GLOBALS ******************************************

assetPath = os.path.abspath('//Merlin/3d4/skid/04_asset')
shotPath = os.path.abspath('//Merlin/3d4/skid/05_shot')

# ****************************************** FUNCTIONS ******************************************

def versionUp(*args):
	# break full name with path on peaces: path, name, ext
	fullName = cmds.file(q=1,sn=1,shn=1)
	fullNamePath = cmds.file(q=1,sn=1)
	absName = os.path.dirname(fullNamePath)
	noExtName = fullName.split('.')[0]
	ext = fullName.split('.')[1]
	splitName = noExtName.split('_v')
	# increase version
	verIndex = len(splitName) - 1
	newVersion = str(int(splitName[verIndex]) + 1)
	padding = len(newVersion)
	zeros = len(splitName[verIndex]) - padding
	newVersion = '0'*zeros + newVersion
	# create new name with path and extension
	resolvedName = ''
	for i in range(0, verIndex):
		resolvedName += splitName[i] + '_v'
	finalNamePath = absName + '/' + resolvedName +  newVersion + '.' + ext

	#check if the file exists
	if cmds.file(finalNamePath, q=1, exists = 1) == 1:
		warningName = resolvedName +  newVersion + '.' + ext
		confirm = cmds.confirmDialog ( title='Increment and Save', message= warningName + ' already exists. Do you want to replace it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			print 'File saved to a new version with overwrite '
		else:
			sys.exit()
	else:
		print 'File saved to a new version'

	#save as new version
	cmds.file( rename= finalNamePath)
	cmds.file( save = True)

def currentShot(*args):
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	sceneName = os.path.split(scenePath)
	return sceneName[1]

def todaysDate(*args):
	now = datetime.datetime.now()
	year = str(now.year)
	if now.month < 10 :
		month = '0' + str(now.month)
	else :
	    month = str(now.month)
	if now.day < 10 :
	    day = '0' + str(now.day)
	else :
	    day = str(now.day)
	today =  year + month + day
	return today

def testSelection(*args):
	sel =  cmds.ls(selection = True)
	if not sel :
		cmds.warning('Nothing is selected')
		return
	else :
		return sel

def showNomenclatures(*args):
	from functools import partial
	nomenclaturesWindow = "Nomenclatures"
	if cmds.window(nomenclaturesWindow,ex=True):
		cmds.deleteUI(nomenclaturesWindow)
	cmds.window(nomenclaturesWindow)
	cmds.columnLayout( adjustableColumn=True )
	file = open('//Merlin/3d4/skid/09_dev/toolScripts/publish/_nomenclatures.txt','r') 
	nomenclaturesText = str(file.read())
	cmds.scrollField(tx=nomenclaturesText,ed=False,wordWrap=True,h=500,w=700)
	cmds.setParent("..")
	cmds.showWindow()

def RfMsubdivScheme(onOff,*args): # Argument must be boolean
	sel = cmds.ls(selection=True)
	for i in sel:
		cmds.setAttr(i+'.rman_subdivScheme',onOff)

def areeeeett(*args): # Easter egg
	import winsound
	import time
	import os
	import random
	import glob

	areeeeettPath = '//Merlin/3d4/skid/09_dev/toolScripts/areeeeett'

	cmds.window('areeeeett', title='ARREEEEEEEEEEEEETT')
	cmds.columnLayout()
	cmds.image(i='%s/areeeeett.jpg' %areeeeettPath)
	cmds.showWindow()
	soundsDirectory = os.path.abspath(areeeeettPath)
	sounds = glob.glob(soundsDirectory+'/*.wav')
	randomSound = random.choice(sounds)
	randomSound = os.path.join(soundsDirectory,randomSound)
	winsound.PlaySound(randomSound, winsound.SND_ASYNC)
	time.sleep(1.2)
	cmds.deleteUI('areeeeett')

def importAssetMa(asset,*args):
	if asset.startswith('props') == True:
		assetType = 'props'
	elif asset.startswith('character') == True:
		assetType = 'character'
	else :
		areeeeett()
		sys.exit()
	
	resolvePath = os.path.join(assetPath,assetType,asset,asset+'.ma')
	cmds.file(resolvePath,r=True,type='mayaAscii',ignoreVersion=True,gl=True,ns=asset)

def loadRenderSettings(context,*args): # Argument must be json file name
	import maya.app.renderSetup.views.renderSetupPreferences as prefs
	try :
		prefs.loadGlobalPreset(context)
		cmds.inViewMessage(amg='Render settings preset <hl>'+context+'</hl> successfuly loaded.',pos='midCenter',fade=True)
	except EnvironmentError:
		commonTools.areeeeett()
		cmds.warning('File '+context+'.json does not exist')
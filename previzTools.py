# **************** SKID PREVIZ TOOLS ****************

import maya.cmds as cmds
import maya.mel as mel
import maya.utils
from functools import partial
import os
import sys
import commonTools


# **************** GLOBALS ****************

sel =  cmds.ls(selection = True) #create a variable with the selected object
SkidAssets = os.path.abspath('//Merlin/3d4/skid/04_asset')
animaticPath = os.path.abspath('//Merlin/3d4/skid/07_editing/input/02_animatic3D')
animaticBackupPath = os.path.join(animaticPath,'backup')

# **************** FUNCTIONS ****************

def exportAbcRfM(*args): #Export alembic avec attributes
	try:
		import sys
		rmScripts = os.path.abspath('C:/Program Files/Pixar/RenderManForMaya-22.1/scripts/rfm2/utils')
		sys.path.insert(0,rmScripts)
		import abc_support
		abc_support.export(False, True)
	except NameError:
		import maya.cmds
		import maya.utils
		maya.utils.executeDeferred('''maya.cmds.loadPlugin('RenderMan_for_Maya.py')''')

def playblastAnim(*args):
	#check if version already has playblast
	sceneFullName = cmds.file(q=1,sn=1,shn=1)
	videoPath = os.path.abspath(cmds.workspace(sn=True,q=True)+'/video/'+sceneFullName)
	playblastPath = videoPath.split('.ma')
	playblastPath = playblastPath[0]
	playblastPath = os.path.abspath(playblastPath)+'.mov'
	playblastPath = os.path.abspath(playblastPath)
	if os.path.isfile(playblastPath):
		confirm = cmds.confirmDialog ( title='Playblast', message= 'A playblast already exists for this version. Do you want to replace it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			pass
		else:
			sys.exit()
	else:
		pass

	#_____Pre_____
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	sceneName = os.path.split(scenePath)
	# shotCameraName = sceneName[1]
	completeName = sceneName[1]
	# cmds.select(shotCameraName + ':' + shotCameraName)
	# completeName = shotCameraName + ':' + shotCameraName
	# On garde en memoire les reglages de camera pour les resetter en post
	camDFG = cmds.getAttr(completeName+'.displayFilmGate')
	camDR = cmds.getAttr(completeName+'.displayResolution')
	camDGM = cmds.getAttr(completeName+'.displayGateMask')
	camOS = cmds.getAttr(completeName+'.overscan')
	#On les set pour le playblast
	cmds.setAttr(completeName+'.displayFilmGate',0)
	cmds.setAttr(completeName+'.displayResolution',0)
	cmds.setAttr(completeName+'.displayGateMask',0)
	camDriven = cmds.listConnections(completeName+'.overscan',plugs=True)
	if camDriven != None:
		for i in camDriven :
			cmds.disconnectAttr(i,completeName+'.overscan')
	else:
		pass
	# cmds.setAttr(completeName+'.overscan',l=False)
	cmds.setAttr(completeName+'.overscan',1)
	cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
	cmds.setAttr('hardwareRenderingGlobals.multiSampleCount',16)
	# cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable",1)
	cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount',32)
	mel.eval('setObjectDetailsVisibility(0);') #Desactive Object Details
	mel.eval('setCameraNamesVisibility(1);') #Active Camera Name
	mel.eval('setCurrentFrameVisibility(1);') #Active Current Frame
	mel.eval('setFocalLengthVisibility(1);') #Active longueur focale

	#Playblast
	cmds.playblast(format="qt",filename=playblastPath,forceOverwrite=True,sequenceTime=0,clearCache=1,viewer=0,showOrnaments=1,offScreen=True,fp=4,percent=100,compression="H.264",quality=100,widthHeight=[2048,858])


	#Post
	cmds.setAttr(completeName+'.displayFilmGate',camDFG)
	cmds.setAttr(completeName+'.displayResolution',camDR)
	cmds.setAttr(completeName+'.displayGateMask',camDGM)
	cmds.setAttr(completeName+'.overscan',camOS)

	cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
	cmds.setAttr('hardwareRenderingGlobals.multiSampleCount',8)
	cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable",0)
	cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount',4)
	cmds.currentTime('1001')
	cmds.select(clear=True)
	
	#Play playblast
	from os import startfile
	startfile(playblastPath)

def createAnimaticBackupPath(*args):
	backupShotPath = os.path.join(animaticBackupPath,commonTools.currentShot(),commonTools.todaysDate())
	if not os.path.exists(backupShotPath):
		os.makedirs(backupShotPath)
		return backupShotPath
	else:
		return backupShotPath

def backupAnimatic(*args):
	from shutil import copyfile
	shotFrames = [s for s in os.listdir(animaticPath) if commonTools.currentShot() in s]
	counter = 0
	for i in shotFrames :
		srcPath = os.path.join(animaticPath,i)
		dstPath = os.path.join(createAnimaticBackupPath(),i)
		copyfile(srcPath,dstPath)
		counter += 1
	return counter

def publishShot(*arg):
	confirm = cmds.confirmDialog( title='Previz Playblast', message='This will replace any frames previously rendered for this shot', button=['Continue','Abort'], defaultButton='Continue', cancelButton='Abort', dismissString='Abort' )
	if confirm != 'Continue':
		pass
	else :
		backupAnimatic()
		#Pre
		scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
		sceneName = os.path.split(scenePath)
		shotCameraName = sceneName[1]
		cmds.select(shotCameraName + ':' + shotCameraName)
		completeName = shotCameraName + ':' + shotCameraName
		# On garde en memoire les reglages de camera pour les resetter en post
		camDFG = cmds.getAttr(completeName+'.displayFilmGate')
		camDR = cmds.getAttr(completeName+'.displayResolution')
		camDGM = cmds.getAttr(completeName+'.displayGateMask')
		camOS = cmds.getAttr(completeName+'.overscan')
		#On les set pour le playblast
		cmds.setAttr(completeName+'.displayFilmGate',0)
		cmds.setAttr(completeName+'.displayResolution',0)
		cmds.setAttr(completeName+'.displayGateMask',0)
		camDriven = cmds.listConnections(completeName+'.overscan',plugs=True)
		if camDriven != None:
			for i in camDriven :
				cmds.disconnectAttr(i,completeName+'.overscan')
		else:
			pass
		# cmds.setAttr(completeName+'.overscan',l=False)
		cmds.setAttr(completeName+'.overscan',1)
		cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
		cmds.setAttr('hardwareRenderingGlobals.multiSampleCount',16)
		cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable",1)
		cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount',32)
		mel.eval('setObjectDetailsVisibility(0);') #Desactive Object Details
		mel.eval('setCameraNamesVisibility(0);') #Active Camera Name
		mel.eval('setCurrentFrameVisibility(0);') #Desactive Current Frame
		mel.eval('setFocalLengthVisibility(1);') #Active longueur focale
		
		#Playblast
		shotpreviz = os.path.abspath('//merlin/3D4/skid/07_editing/input/02_animatic3D/')
		scenePath = os.path.abspath(cmds.workspace(sn=True,q=True)) #On va chercher le chemin du projet
		sceneName = os.path.split(scenePath)
		playblastPath = os.path.join(shotpreviz,sceneName[1]) #Le path complet pour le playblast
		cmds.playblast(format="image",filename=playblastPath,forceOverwrite=True,sequenceTime=0,clearCache=1,viewer=0,showOrnaments=1,offScreen=True,fp=4,percent=100,compression="jpg",quality=70,widthHeight=[2048,858])
		
		#Post
		cmds.setAttr(completeName+'.displayFilmGate',camDFG)
		cmds.setAttr(completeName+'.displayResolution',camDR)
		cmds.setAttr(completeName+'.displayGateMask',camDGM)
		cmds.setAttr(completeName+'.overscan',camOS)
		
		cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
		cmds.setAttr('hardwareRenderingGlobals.multiSampleCount',8)
		cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable",0)
		cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount',4)
		cmds.currentTime('1001')
		cmds.select(clear=True)

def referenceAlembic(*args):
	mel.eval('projectViewer AlembicReference;')

def setShot(*args):
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	sceneName = os.path.split(scenePath)
	shotCameraName = sceneName[1] + ':' + sceneName[1] + '_AlembicNode'
	shotStartFrame = cmds.getAttr(shotCameraName + '.startFrame')
	shotEndFrame = cmds.getAttr(shotCameraName + '.endFrame')
	
	cmds.currentTime('1001')
	cmds.playbackOptions(min=shotStartFrame,max=shotEndFrame,ast=shotStartFrame,aet=shotEndFrame)

def importShotAlembics(*args):
	import glob
	#Lister tout les alembics dans le dossier abc du shot
	availableAlembics = []
	currentShot = cmds.workspace(q=True,rd=True)
	abcPath = os.path.join(currentShot,'abc')
	os.chdir(abcPath)
	abcList = glob.glob("*.abc")
	for i in abcList:
		asset = i.replace('.abc','')
		availableAlembics.append(asset)
	#On check si certains alembics sont deja importes et on separe les alembics deja importes de ceux a importer
	dontImport = []
	toImport = []
	for i in availableAlembics:
		importedName = i+'RN'
		if cmds.objExists(importedName) == True:
			dontImport.append(i)
		else :
			toImport.append(i)
	#User prompt pour continuer ou non
	lenToImport = len(toImport)
	if lenToImport == 0:
		cmds.inViewMessage(amg='No alembic file to import',pos='midCenter',fade=True)
	else :
		confirm = cmds.confirmDialog(title='Import Shot Alembics', message='Found '+str(lenToImport)+' alembic files to import. Continue ?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			for i in toImport:
				resolvePath = os.path.join(abcPath,i+'.abc')
				resolvePath = os.path.abspath(resolvePath)
				# print resolvePath
				cmds.file(resolvePath,r=True,type='Alembic',ignoreVersion=True,gl=True,ns=i)
		else :
			pass

def importShaders(*args):
	import glob
	#Lister tout les alembics dans le dossier abc du shot
	availableAlembics = []
	currentShot = cmds.workspace(q=True,rd=True)
	abcPath = os.path.join(currentShot,'abc')
	os.chdir(abcPath)
	abcList = glob.glob('*.abc')
	for i in abcList:
		asset = i.replace('.abc','')
		availableAlembics.append(asset)
	#Virer de la liste la camera du shot
	currentShot = os.path.basename(os.path.normpath(cmds.workspace(q=True,rd=True)))
	shotCamera = currentShot
	if shotCamera in availableAlembics: availableAlembics.remove(shotCamera)
	#virer le nom du shot dans le nom des alembics

	#Separer shaders deja importes de ceux disponibles
	dontImport = []
	toImport = []
	for i in availableAlembics :
		#On vire le nom du shot present devant le nom des alembics
		scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
		sceneName = os.path.split(scenePath)
		completeName = sceneName[1]+'_'
		i = i.replace(completeName,'')
		i = i+'_shdRN'
		if cmds.objExists(i) == True:
			dontImport.append(i)
		else :
			toImport.append(i)
	# print toImport
	#Verifier que le fichier de shader existe et est publie
	shadersToImport = []
	for i in toImport:
		scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
		sceneName = os.path.split(scenePath)
		completeName = sceneName[1]+'_'
		i = i.replace(completeName,'')
		i = i.replace('_shdRN','')
		if 'props' in i:
			resolvePath = os.path.join(SkidAssets,'props',i,i+'_shd.ma')
			assetType = 'props'
		elif 'character' in i:
			resolvePath = os.path.join(SkidAssets,'character',i,i+'_shd.ma')
			assetType = 'character'
		else :
			cmds.warning('Could not resolve path for '+i)
			return

		check = os.path.exists(resolvePath)
		if check == True :
			shadersToImport.append(i)
		else :
			cmds.warning('Path does not exist for '+i)
			print resolvePath
			pass
	#User prompt pour continuer ou non
	lenToImport = len(shadersToImport)
	if lenToImport == 0:
		cmds.inViewMessage(amg='No shader to import',pos='midCenter',fade=True)
	else :
		confirm = cmds.confirmDialog(title='Import Shaders', message='Found '+str(lenToImport)+' shader files to import. Continue ?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			for i in shadersToImport:
				resolvePath = os.path.join(SkidAssets,assetType,i,i+'_shd.ma')
				cmds.file(resolvePath,r=True,type='mayaAscii',ignoreVersion=True,gl=True,ns=i+'_shd')
		else :
			pass

def assignShaders(*args):
	#Dabord on liste les geometries qui ont un ID
	geometries = cmds.ls("*_ID*",r=True,tr=True)
	#On check quon a bien des geometries
	if not geometries:
		cmds.warning('Could not find any object with ID, make sure your object names look like : "assetNameSpace:objectName_IDsomething"')
	else :
		#user prompt pour continuer
		confirm = cmds.confirmDialog(title='Assign Shaders', message='Found '+str(len(geometries))+' object with ID. Continue ?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			for i in geometries:
				#On split le mot cle de l'ID
				ID = i.split('_ID', 1)[-1]
				#On split le namespace
				nameSpace = i.split(':',)[0]
				# puis on reconstruie le nom du shading group :
				SG = nameSpace+'_shd:'+ID+'_SG'
				# puis on assigne le shading group a la geo qui lui correspond
				try :
					cmds.sets(i,e=True,forceElement=SG)
				except TypeError :
					cmds.warning('Could not find matching Shading Group for '+i+', make sure your Shading Group name is : '+SG)
		else :
			pass

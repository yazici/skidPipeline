# ****************************************** S K I D     A N I M     T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import commonTools
import os
import sys
from pymel.core import *

# ****************************************** F U N C T I O N S ******************************************

def createSpeedAttribute(*args):
	sel = cmds.ls(selection=True)
	if len(sel) != 1 :
		cmds.warning('One object must be selected')
	else :
		sel = sel[0]
		cmds.addAttr(sel,ln='speed',nn='Speed (kmh)',at='double',dv=0,h=False,k=True)
		cmds.expression(s="float $lastPosX = `getAttr -t (frame-1) "+sel+".tx`;\nfloat $lastPosY = `getAttr -t (frame-1) "+sel+".ty`;\nfloat $lastPosZ = `getAttr -t (frame-1) "+sel+".tz`;\n\nfloat $tempSpeed = abs (mag (<<"+sel+".translateX,"+sel+".translateY,"+sel+".translateZ>>)- mag (<<$lastPosX,$lastPosY,$lastPosZ>>) );\n\n"+sel+".speed = ((($tempSpeed/100)*24)*3.6)",ae=1,uc='all')
		cmds.select(sel,r=True)

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

def playblastAnim(*args): #Playblast avec version
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

def publishAnimations(riggedAssets,*args):
	cmds.loadPlugin( 'AbcExport.mll' )
	from shutil import copyfile
	import glob
	end = cmds.playbackOptions(q=True,max=True)
	confirm = cmds.confirmDialog( title='Publish Animations', message='This will replace any animation previously published for this shot \nCurrent frame range is : 1001 to %s' %end, button=['Continue','Abort'], defaultButton='Continue', cancelButton='Abort', dismissString='Abort' )
	if confirm != 'Continue':
		pass
	else :
		# create backup folder if doesnt exist
		shotsPath = '//Merlin/3d4/skid/05_shot'
		abcPath = os.path.abspath(os.path.join(shotsPath,commonTools.currentShot(),'abc'))
		animationBackupPath = os.path.join(abcPath,'backup',commonTools.todaysDate())
		if not os.path.exists(animationBackupPath):
			os.makedirs(animationBackupPath)
		# backup already published to date folder
		abcFiles = glob.glob('%s/*.abc' %abcPath)
		for file in abcFiles :
			srcPath = file
			dstPath = os.path.join(animationBackupPath,os.path.split(file)[1])
			copyfile(srcPath,dstPath)
		# do playblast
		cmds.select(clear=True)
		playblastAnim()
		# list assets that are present in this shot
		toExport = []
		for asset in riggedAssets :
			if cmds.objExists(asset+':'+asset+'_grp') == True:
				toExport.append(asset)
		# export des assets
		for asset in toExport :
			cmds.select(asset+':'+asset+'_grp',r=True)
			
			exportPath = os.path.abspath(os.path.join(abcPath,asset))
			# cette putain de fonction qui marche pas en python
			sel = cmds.ls(selection=True,l=True)
			start = str(1001)
			end = str(cmds.playbackOptions(q=True,max=True))
			root = str(sel[0])
			save_name = str('%s.abc' %exportPath)
			# putain de commande completement petee merci l api maya
			command = "-frameRange " + start + " " + end +" -attrPrefix rman__torattr -attrPrefix rman__riattr -attrPrefix rman_emitFaceIDs -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root " + root + " -file " + save_name
			cmds.AbcExport(j=command)
			print '%s has been exported successfuly (probably)' %asset
		
		# export de la camera
		cmds.select(commonTools.currentShot(),r=True)
		exportPath = os.path.abspath(os.path.join(abcPath,commonTools.currentShot()))
		sel = cmds.ls(selection=True,l=True)
		start = str(1001)
		end = str(cmds.playbackOptions(q=True,max=True))
		root = str(sel[0])
		save_name = str('%s.abc' %exportPath)
		command = "-frameRange " + start + " " + end +" -attrPrefix rman__torattr -attrPrefix rman__riattr -attrPrefix rman_emitFaceIDs -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root " + root + " -file " + save_name
		cmds.AbcExport(j=command)
		print '%s has been exported successfuly (probably)' %commonTools.currentShot()
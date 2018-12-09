# **************** SKID LOOKDEV TOOLS ****************

import maya.cmds as cmds
import maya.mel as mel
import os
from functools import partial
import commonTools


# **************** GLOBAL VARIABLES ****************

lookdevScenePath = os.path.abspath('//merlin/3d4/skid/09_dev/toolScripts/lookdev/lookdevSetup/LookdevSetup.ma')
hdri_folder = os.path.abspath('//Merlin/3d4/skid/04_asset/SkidLibrary/HDRI')
grpName = 'LookdevSetup:GRP_LookdevSetup'

# **************** FUNCTIONS ****************

def importLookdevScene(*arg):
	if cmds.objExists(grpName):
		pass
	else :
		cmds.file(lookdevScenePath,r=True,type='mayaAscii',ignoreVersion=True,gl=True,mergeNamespacesOnClash=False,namespace="LookdevSetup",options="v=0;p=17;f=0")

def hideLookdevScene(*arg):
	if cmds.objExists(grpName):
		testVis = cmds.getAttr(grpName+'.visibility')
		if testVis == True:
			cmds.hide(grpName)
		else :
			cmds.showHidden(grpName)
	else :
		pass

def reloadLookdevScene(*arg):
	if cmds.objExists(grpName):
		cmds.file(lookdevScenePath,rr=True)
		importLookdevScene()
	else :
		pass

def create_turn_loc(*arg):
	locatorName = 'turn_locator'
	delete_turn_loc()
	cmds.spaceLocator(name=locatorName)
	cmds.setAttr(locatorName+'.localScaleX',50)
	cmds.setAttr(locatorName+'.localScaleY',50)
	cmds.setAttr(locatorName+'.localScaleZ',50)
	cmds.setKeyframe(locatorName,at='rotateY',t=1,v=0)
	cmds.setKeyframe(locatorName,at='rotateY',t=101,v=360)
	cmds.selectKey(clear=True)
	cmds.selectKey(locatorName,time=(1,101),at='rotateY')
	cmds.keyTangent(itt='linear',ott='linear')
	cmds.currentTime(1)
	cmds.playbackOptions(min=1,max=100)
	cmds.selectKey(clear=True)
	cmds.select(clear=True)
	#set render settings end frame
	cmds.setAttr('defaultRenderGlobals.endFrame',100)


def change_frames_number(frameNbr,*args): #argument must be integer
	locatorName = 'turn_locator'
	cmds.cutKey(locatorName,at='rotateY',option='keys',cl=True)
	cmds.setKeyframe(locatorName,at='rotateY',t=1,v=0)
	cmds.setKeyframe(locatorName,at='rotateY',t=frameNbr+1,v=360)
	cmds.selectKey(locatorName,t=(1,frameNbr+1),at='rotateY')
	cmds.keyTangent(itt='linear', ott='linear')
	cmds.playbackOptions(min=1,max=frameNbr,ast=1,aet=frameNbr)
	cmds.selectKey(clear=True)
	cmds.select(clear=True)
	cmds.setAttr('defaultRenderGlobals.endFrame',frameNbr)

def delete_turn_loc(*arg):
	locatorName = 'turn_locator'
	try:
		cmds.delete(locatorName)
	except ValueError:
		pass

def open_hdri_folder(*arg):
	os.startfile(hdri_folder)

def loadRenderSettings(context,*args): #argument must be json file name
	import maya.app.renderSetup.views.renderSetupPreferences as prefs
	try :
		prefs.loadGlobalPreset(context) #surement a remplacer par global
		cmds.inViewMessage(amg='Render settings preset <hl>'+context+'</hl> successfuly loaded.',pos='midCenter',fade=True)
	except EnvironmentError:
		commonTools.areeeeett()
		cmds.warning('Context '+context+' does not exist. Qui a delete ce putain de fichier json !?.')

def turnLights(*args):
	hdriTurnGrp = '|LookdevSetup:GRP_LookdevSetup|LookdevSetup:GRP_LIGHTING|LookdevSetup:GRP_HDRI'
	if cmds.objExists(hdriTurnGrp) == False:
		cmds.warning('LookdevSetup:GRP_HDRI was not found, please take a nerf gun and shoot Clement because he fucked up')
		return
	else:
		cmds.select(hdriTurnGrp)

def createPxrSurfaceNetwork(*args):
	# Prendre nom de l asset avec le currentWorkspace
	# PxrSurface and Shading Group
	psurf = cmds.shadingNode('PxrSurface', asShader=True, skipSelect=True) 
	sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,name=psurf + 'SG')
	cmds.connectAttr('%s.outColor' %psurf ,'%s.rman__surface' %sg)
	cmds.connectAttr('lambert1.outColor','%s.surfaceShader' %sg)

	# Set Attributes to Skid default values
	cmds.setAttr('%s.specularFresnelMode' % psurf,1)
	cmds.setAttr('%s.roughSpecularFresnelMode' % psurf,1)
	cmds.setAttr('%s.clearcoatFresnelMode' % psurf,2)
	cmds.setAttr('%s.subsurfaceType' % psurf,5)
	cmds.setAttr('%s.subsurfaceDmfp' % psurf,3)
	cmds.setAttr('%s.subsurfaceDirectionality' % psurf,0.5)
	cmds.setAttr('%s.subsurfaceResolveSelfIntersections' % psurf,1)
	cmds.setAttr('%s.singlescatterMfp' % psurf,3)
	cmds.setAttr('%s.singlescatterDirectionality' % psurf,0.5)
	cmds.setAttr('%s.singlescatterBlur' % psurf,0.5)
	cmds.setAttr('%s.singlescatterContinuationRayMode' % psurf,2)
	cmds.setAttr('%s.singlescatterMaxContinuationHits' % psurf,4)
	cmds.setAttr('%s.singlescatterDirectGainMode' % psurf,2)
	# cmds.setAttr('%s.mwWalkable' % psurf,1) # manifold walk a discuter

	# Displacement
	disp = cmds.shadingNode('PxrDisplace', asShader=True, skipSelect=True)
	cmds.setAttr("%s.enabled" %disp,0)
	cmds.connectAttr('%s.outColor' %disp,'%s.displacementShader' %sg)
	disptrans = cmds.shadingNode('PxrDispTransform', asShader=True, skipSelect=True)
	cmds.setAttr('%s.dispRemapMode' %disptrans,2)
	cmds.setAttr('%s.dispHeight' %disptrans,0.1)
	cmds.setAttr('%s.dispDepth' %disptrans,0.1)
	cmds.connectAttr('%s.resultF' %disptrans,'%s.dispScalar' %disp)


	# PxrTextures
	difCol = cmds.shadingNode('PxrTexture',name='PxrTexture_difCol', asTexture=True, skipSelect=True)
	cmds.setAttr('%s.linearize' %difCol,1)
	# cmds.setAttr('%s.filename' %difCol,'tex/',type="string") # Surement besoin de rajouter workspace et resolve texture name
	cmds.connectAttr('%s.resultRGB'%difCol,'%s.diffuseColor'%psurf,f=True)

	specCol = cmds.shadingNode('PxrTexture',name='PxrTexture_specCol', asTexture=True, skipSelect=True)
	cmds.setAttr('%s.linearize' %specCol,1)
	cmds.connectAttr('%s.resultRGB'%specCol,'%s.specularEdgeColor'%psurf,f=True)

	specRough = cmds.shadingNode('PxrTexture',name='PxrTexture_specRough', asTexture=True, skipSelect=True)
	cmds.connectAttr('%s.resultR'%specRough,'%s.specularRoughness'%psurf,f=True)

	normal = cmds.shadingNode('PxrNormalMap',name='PxrNormalMap_normal', asTexture=True, skipSelect=True)
	cmds.setAttr('%s.adjustAmount' %normal,1)
	cmds.setAttr('%s.disable' %normal,1)
	cmds.connectAttr(normal+'.resultN', psurf+'.bumpNormal',f=True)

	disptex = cmds.shadingNode('PxrTexture',name='PxrTexture_disp', asTexture=True, skipSelect=True)
	cmds.connectAttr('%s.resultR'%disptex,'%s.dispScalar'%disptrans,f=True)

def createPxrLayerNetwork(*args):
	pass
	# lmix = cmds.shadingNode('PxrLayerMixer', asTexture=True, skipSelect=True)
	# lyr1 = cmds.shadingNode('PxrLayer', asTexture=True, skipSelect=True)
	# lyr2 = cmds.shadingNode('PxrLayer', asTexture=True, skipSelect=True)
	# cmds.connectAttr('%s.pxrMaterialOut' % lmix, '%s.inputMaterial' % node)
	# cmds.connectAttr('%s.pxrMaterialOut' % lyr1, '%s.baselayer' % lmix)
	# cmds.connectAttr('%s.pxrMaterialOut' % lyr2, '%s.layer1' % lmix)

def convertPxrSurfaceToLayer(*args):
	pass
	# fullnames = []
	# for attribute in attributes :
	# 	fullname = cmds.getAttr(psurf+'.'+attribute)
	# 	fullnames.append(str(fullname))
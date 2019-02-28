# ****************************************** S K I D     F O R E S T     T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import os, subprocess

# ****************************************** G L O B A L S ******************************************



# ****************************************** F U N C T I O N S ******************************************

def fireHoudini(mtop,mright,mbot,mleft,depth,*args):
	'''This function opens a headless version of houdini and computes
	a point cloud for trees instancing depending on the shot camera position and movements.
	Arguments are camera frustrum margins and should be a float between 0 and 1'''
	
	# User prompt before firing up
	confirmTxt = 'Please check your frame range and margins are right before you continue.'
	confirm = cmds.confirmDialog(title='Compute point cloud',message=confirmTxt,button=['Continue','Cancel'], \
		defaultButton='Continue',cancelButton='Cancel',dismissString='Cancel')
	if confirm != 'Continue':
		return
	# Check current shot
	currentWorkspace = os.path.abspath(cmds.workspace(sn=True,q=True))
	currentShot = str(os.path.split(currentWorkspace)[1])
	# Get Frame range
	fstart = cmds.playbackOptions(ast=True,q=True)
	fend = cmds.playbackOptions(aet=True,q=True)
	# Fire headless Houdini 
	houScript = '//Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.py'
	print(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft,depth)
	# os.system('hython %s %s %s %s %s %s %s %s'%(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft))
	# os.system('hython //Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.py')
	subprocess.call('hython %s %s %s %s %s %s %s %s %s'%(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft,depth))

def loadHoudiniEngine(*args):
	# Load Houdini Engine for Maya and check if version is at least 17
	try :
		cmds.loadPlugin('houdiniEngine')
	except :
		cmds.warning('Could not load Houdini Engine')
		return False
	EngineVersion = mel.eval('houdiniEngine -hv;')
	if not '17.' in EngineVersion :
		cmds.warning('Wrong Houdini Engine version (installed version is '+EngineVersion+'), should be at least version 17')
		return False
	else :
		return True

def loadShotPoints(*args):
	'''This function will load the generated point cloud in Maya via Houdini Engine.
	It will then copy each point and their attribute to a new point cloud to get rid of Houdini Engine.'''

	# Load Houdini Engine
	if loadHoudiniEngine() == False:
		return

	# Check if point cloud exists
	currentWorkspace = os.path.abspath(cmds.workspace(sn=True,q=True))
	currentShot = str(os.path.split(currentWorkspace)[1])
	bgeoPath = '//Merlin/3d4/skid/05_shot/%s/geo/fileCache/%s_instancerPts.bgeo.sc'%(currentShot,currentShot)
	if not os.path.isfile(bgeoPath):
		cmds.warning('Point cloud not found for %s'%currentShot)
		return

	# Set persp far clip plane
	cmds.setAttr('perspShape.farClipPlane',1000000)

	# Set current time to first frame
	fstart = cmds.playbackOptions(ast=True,q=True)
	cmds.currentTime(fstart)

	# Load the bgeo importer
	toolBgeoToMaya = os.path.abspath('//merlin/3d4/skid/04_asset/hda/toolBgeoToMaya_v2.hdanc')
	cmds.houdiniAsset(la=[toolBgeoToMaya,'Object/toolBgeoToMaya'])
	# Set file path to shot points
	cmds.setAttr('toolBgeoToMaya1.houdiniAssetParm.houdiniAssetParm_file',bgeoPath,type="string")
	# Sync asset
	# cmds.evalDeferred('cmds.houdiniAsset(syn="toolBgeoToMaya1")')
	cmds.houdiniAsset(syn="toolBgeoToMaya1")


	# Duplicate point cloud to get rid of houdini engine
	pointCloud = 'file_bgeoToMaya_0'
	pointCloud_s = pointCloud+'Shape'
	vAttrToTransfer = ['rgbPP','radiusPP']
	dAttrToTransfer = ['particleId']
	newNameSuffix = '_dupli'

	# Get particle count
	nbPart = cmds.particle(pointCloud,q=True,ct=True)

	# Create new particle system with suffix
	tmp = cmds.particle(n=pointCloud+newNameSuffix)
	dupliPartXf = tmp[0]
	dupliPartShp = tmp[1]

	# Create vector attributes on the new system
	for attr in vAttrToTransfer:
		try :
			cmds.addAttr(dupliPartShp,ln=attr,dt='vectorArray')
		except RuntimeError :
			cmds.warning('Cant create attribute %s'%attr)
		try :
			cmds.addAttr(dupliPartShp,ln=attr+'0',dt='vectorArray')
		except RuntimeError :
			cmds.warning('Cant create attribute '+attr+'0')
		# L'attr0 doit etre la valeur initiale, ca ne fonctionne pas sans la creation
	cmds.setAttr(dupliPartShp+'.isDynamic',False)

	# Fill new particle system with positions
	for i in range(nbPart):
		wPos = cmds.getParticleAttr('%s.pt[%s]'%(pointCloud_s,i),at='position',array=True)
		cmds.emit(o=dupliPartXf,pos=[wPos[0],wPos[1],wPos[2]])

	# Transfer vector attributes
	for attr in vAttrToTransfer :
		try :
			for i in range(nbPart) :
				attrValue = cmds.getParticleAttr('%s.pt[%s]'%(pointCloud_s,i),at=attr,array=True)
				cmds.particle(e=True,at=attr,order=i,vv=[attrValue[0],attrValue[1],attrValue[2]])
		except :
			cmds.warning('Could not Transfer attribute : '+attr)



	# Transfer double attributes



	# for attr in dAttrToTransfer :
	# 	try :
	# 		for i in range(nbPart) :
	# 			attrValue = cmds.getParticleAttr('%s.pt[%s]'%(pointCloud_s,i),at=attr,)
				# cmds.particle




	# Delete unwanted nodes
	cmds.delete('toolBgeoToMaya1')

	# Rename particle system and group
	newname = 'forest_instancing_pc'
	cmds.rename(tmp[0],newname)
	masterGRP = 'FOREST_INSTANCING_GRP'
	try :
		cmds.select(masterGRP,r=True)
	except ValueError :
		cmds.group(newname,name=masterGRP)
	else :
		cmds.parent(newname,masterGRP)

	# Set nucleus (yes we have to keep it for some reason)
	cmds.setAttr('nucleus1.startFrame',fstart)
	cmds.parent('nucleus1',masterGRP)

def createInstancer(*args):
	'''This function will create an instancer and instance the selected geometries'''
	# Save selection to add to instancer
	sel = cmds.ls(selection=True)
	instancer = cmds.particleInstancer('forest_instancing_pcShape', \
		levelOfDetail='BoundingBox',addObject=True,object=sel, \
		scale='radiusPP', \
		objectIndex='particleId', \
		rotation='rgbPP')
	# Rename instancer and group
	instancer = cmds.rename(instancer,'forest_instancing_instancer')
	masterGRP = 'FOREST_INSTANCING_GRP'
	try :
		cmds.select(masterGRP,r=True)
	except ValueError :
		cmds.group(instancer,name=masterGRP)
	else :
		cmds.parent(instancer,masterGRP)
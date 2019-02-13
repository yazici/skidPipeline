# ****************************************** S K I D     A S S E T S     T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import sys
import os
import commonTools
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

sel =  [] #create a variable with the selected object

# ****************************************** F U N C T I O N S ******************************************

def setObject(*args):
	'''This will set the selected asset to world zero'''
	if commonTools.testSelection() == None:
		sys.exit
	else :
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)#freeze transforms
		cmds.xform(cp=True) #center pivot
		cmds.move(rpr=True) #move to world center
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)#freeze transforms
		cmds.delete(all=True, ch=True) #delete history
		cmds.inViewMessage( amg='Ton asset <hl>'+str(sel)+'</hl> a ete mis a zero, bro.', pos='midCenter', fade=True )

def fixNormals (*arg):
	''' Fix normal for every selected objects'''
	if commonTools.testSelection() == None:
		cmds.warning('Nothing is selected')
	else :
		sel = commonTools.testSelection()
		selAD = cmds.listRelatives(sel,ad=True)
		selShapes = cmds.listRelatives(sel,shapes=True,fullPath=True) # List selected shapes
		for i in selAD: # Fix normal angles
			cmds.polyNormalPerVertex(i,ufn=True) # Unlock normals
			cmds.polySetToFaceNormal(i) # Set to face
			cmds.polySoftEdge(i,a=60) # Set normal angle to 60
		for i in selShapes: # Disable opposite normals
			cmds.setAttr('%s.doubleSided' % i,0)
			cmds.setAttr('%s.opposite' % i,0)
			cmds.setAttr('%s.doubleSided' % i,1)
		cmds.select(clear=True)
		cmds.select(sel,r=True)
		cmds.inViewMessage( amg='Done ! Remember to delete history.', pos='midCenter', fade=True )

def duplicateNamesDialog(*args):
	confirm = cmds.confirmDialog(title='Rename duplicate names',message='Do you want to rename every object with duplicate names or just select them ?', button=['Rename','Select','Cancel'], defaultButton='Select', cancelButton='Cancel', dismissString='Cancel')
	if confirm == 'Rename':
		renameDuplicates(1)
	elif confirm == 'Select':
		renameDuplicates(2)

def renameDuplicates(action,*args):
	'''Find all objects that have the same shortname as another
	We can indentify them because they have | in the name'''
	import re
	duplicates = [f for f in cmds.ls() if '|' in f]
	if action == 1:
		# Sort them by hierarchy so that we don't rename a parent before a child.
		duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)
		# If we have duplicates, rename them
		if duplicates:
			for name in duplicates:
				# Extract the base name
				m = re.compile("[^|]*$").search(name) 
				shortname = m.group(0)
				
				# Extract the numeric suffix
				m2 = re.compile(".*[^0-9]").match(shortname) 
				if m2:
					stripSuffix = m2.group(0)
				else:
					stripSuffix = shortname
				
				# Rename, adding '#' as the suffix, which tells maya to find the next available number
				newname = cmds.rename(name, (stripSuffix + "#")) 
				print "renamed %s to %s" % (name, newname)
				
			return "Renamed %s objects with duplicated name." % len(duplicates)
		else:
			return "No Duplicates"
	elif action == 2:
		cmds.select(clear=True)
		for i in duplicates:
			cmds.select(i,add=True)

def selObjWithoutUV(*args):
	'''Select every object with no UV'''
	ObjWithoutUV = []
	allGeos = cmds.ls(typ="mesh")
	for i in allGeos:
		cmds.select(i)
		if cmds.polyEvaluate(uvShell=True) == 0: 
			ObjWithoutUV.append(i)
	cmds.select(clear=True)
	for i in ObjWithoutUV:
		cmds.select(i,add=True)
	if len(ObjWithoutUV) == 0:
		cmds.inViewMessage( amg='Every object have UVs', pos='midCenter',fade=True )
	elif len(ObjWithoutUV) == 1:
		cmds.inViewMessage( amg='%s object has no UV' %len(ObjWithoutUV) \
			,pos='midCenter',fade=True )
	else :
		cmds.inViewMessage( amg='%s objects have no UV' %len(ObjWithoutUV) \
			,pos='midCenter',fade=True )
	return ObjWithoutUV

def checkDatAss(*args):
	'''This is a general asset checker that will test everything is ready
	for the asset to be publish (the user is free to take the warnings
	into account or dismiss them) :'''
	import maya.OpenMaya as om
	import fnmatch
	import commonTools
	reload(commonTools)
	green = (0,.6,.2)
	red = (.7,0,0)

	# Test group name is correct
	correctName = commonTools.currentShot()+'*_grp' # Wild card to enable model variations
	filtered = fnmatch.filter(cmds.ls(), correctName)
	if not filtered :
		cmds.warning('No matching group was found. Master group should look like : %s (where * can be replaced by anything)'%correctName)
		return
	else :
		sel = filtered
		cleanGrp = green

	# Test group is not empty
	if not cmds.listRelatives(sel):
		cmds.warning('%s is empty'%sel)
		return

	# Test if scene contains instances
	instances = []
	iterDag = om.MItDag(om.MItDag.kBreadthFirst)
	while not iterDag.isDone():
		instanced = om.MItDag.isInstanced(iterDag)
		if instanced :
			instances.append(iterDag.fullPathName())
		iterDag.next()
	if instances:
		cmds.warning('Your scene contains instances, please convert them to objects before you can continue')
		cmds.select(instances,r=True)
		return

	# Test if scene contains duplicate names
	duplicates = []
	duplicates = [f for f in cmds.ls() if '|' in f]
	if not duplicates :
		cleanDuplicates = green
	else :
		cleanDuplicates = red
		cmds.warning('Your asset contains duplicate names. You need to fix them before you can continue')
		duplicateNamesDialog()
		return

	# Test if master group is at world zero
	correctTransforms = '([(0.0, 0.0, 0.0)], [(0.0, 0.0, 0.0)], [(1.0, 1.0, 1.0)])'
	correctPivots = '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'

	transforms = (cmds.getAttr('%s.translate' % sel[0]), \
		cmds.getAttr('%s.rotate' % sel[0]),\
		cmds.getAttr('%s.scale' % sel[0]))
	for i in sel:
		pivots = cmds.xform(i,pivots=True,query=True)
		if str(transforms) != correctTransforms or str(pivots) != correctPivots:
			cleanWorldZero = red
		else :
			cleanWorldZero = green

	# Test freeze scales
	notFreezed = []
	selAllTransforms = cmds.listRelatives(sel,ad=True,typ='transform')
	correctScale = '[(1.0, 1.0, 1.0)]'
	for i in selAllTransforms:
		if str(cmds.getAttr('%s.scale'%i)) != correctScale:
			notFreezed.append(i)
	if notFreezed :
		cleanScales = red
	else :
		cleanScales = green

	# Test nGones
	testClean = []
	cmds.select(sel,r=True)
	testClean = mel.eval('polyCleanupArgList 4 { "0","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };')	
	cmdNGones = 'mel.eval(\'polyCleanupArgList 4 { "0","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };\')'
	if testClean:
		cleanNGones = red
	else :
		cleanNGones = green

	# Test nonManifold
	testNonMani = []
	cmds.select(sel,r=True)
	testNonMani = mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0","0" };')
	cmdNonManifold = 'mel.eval(\'polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0","0" };\')'
	if testNonMani:
		cleanNonManifold = red
	else :
		cleanNonManifold = green

	# Test Edges with zero length
	testEdgesZero = []
	cmds.select(sel,r=True)
	testEdgesZero = mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","1","1e-05","0","1e-05","0","-1","0","0" };')
	cmdEdgesZeroLength = 'mel.eval(\'polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","1","1e-05","0","1e-05","0","-1","0","0" };\')'
	if testEdgesZero :
		cleanEdgesZeroLength = red
	else :
		cleanEdgesZeroLength = green

	# Test faces with zero geometry area
	cmds.select(sel,r=True)
	testClean = mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","1","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };')
	cmdFacesZeroArea = 'mel.eval(\'polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","1","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };\')'
	if testClean:
		cleanFacesZeroArea = red
	else :
		cleanFacesZeroArea = green

	# Test UVs with zero map area
	cmds.select(sel,r=True)
	testClean = mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","1","1e-05","0","-1","0","0" };')
	cmdUVsZeroArea = 'mel.eval(\'polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","1","1e-05","0","-1","0","0" };\')'
	if testClean:
		cleanUVsZeroArea = red
	else :
		cleanUVsZeroArea = green

	# Test Objects with no UV
	if len(selObjWithoutUV()) !=0:
		cleanWithoutUvs = red
	else :
		cleanWithoutUvs = green

	# Test objects opposite normals
	selAllShapes = cmds.listRelatives(selAllTransforms,shapes=True)
	withOpposites = []
	for i in selAllShapes:
		try :
			if cmds.getAttr('%s.opposite'%i) == 1:
				withOpposites.append(i)
		except:
			pass
	if len(withOpposites) != 0:
		cleanOpposites = red
	else :
		cleanOpposites = green

	# Test unwanted nodes
	unwantedTypes = ['pointEmitter','nParticle','nCloth','nucleus']
	unwanted = []
	for i in unwantedTypes:
		nodes = cmds.ls(typ=i)
		if nodes:
			for n in nodes:
				unwanted.append(n)
	if unwanted:
		cleanUnwanted = red
	else :
		cleanUnwanted = green

	# Test if empty transform nodes
	allNodes = cmds.listRelatives(sel,ad=True)
	emptyTransforms = []
	print allNodes
	for i in allNodes:
		if not cmds.listRelatives(i,ad=True) and cmds.ls(i,typ='shape'):
			emptyTransforms.append(i)
	if emptyTransforms:
		cleanemptyTransforms = red
	else :
		cleanemptyTransforms = green

	# Restore selection
	cmds.select(sel,r=True)

	# Create Window with results
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=100, h=25, align='left',l='Select',c='cmds.select("%s",r=True)' % sel[0])
	template.define(frameLayout, borderVisible=True, labelVisible=True,w=300)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(text,h=25,w=200)

	try :
		cmds.deleteUI('checkDatAss')
	except RuntimeError :
		pass

	with window('checkDatAss', title='Check Dat Ass(et)',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():
				with frameLayout('Naming'):
					with rowColumnLayout():
						text(l='Master Group',bgc=cleanGrp)
						button()

						text(l='Duplicate names',bgc=cleanDuplicates)
						button()

				with frameLayout('Transforms'):
					with rowColumnLayout():
						text(l='Centered to world zero',bgc=cleanWorldZero)
						button()

						text(l='Freeze Scales',bgc=cleanScales)
						button(c='notFreezed = %s; \
							cmds.select(clear=True); \
							cmds.select(notFreezed,add=True)' % notFreezed)

				with frameLayout('Geometries'):
					with rowColumnLayout():
						text(l='nGones',bgc=cleanNGones)
						button(c='%s'%cmdNGones)

						text(l='Nonmanifold',bgc=cleanNonManifold)
						button(c='%s'%cmdNonManifold)

						text(l='Edges with zero length',bgc=cleanEdgesZeroLength)
						button(c='%s'%cmdEdgesZeroLength)

						text(l='Faces with zero geometry area',bgc=cleanFacesZeroArea)
						button(c='%s'%cmdFacesZeroArea)

						# text(l='UVs with zero map area',bgc=cleanUVsZeroArea)
						# button(c='%s'%cmdUVsZeroArea)

						text(l='Objects with no UV',bgc=cleanWithoutUvs)
						button(c='import assetsTools; \
								reload(assetsTools); \
								assetsTools.selObjWithoutUV()')

						text(l='Objects with opposite normals',bgc=cleanOpposites)
						button(c='withOpposites = %s; \
							cmds.select(clear=True); \
							cmds.select(withOpposites,add=True)' % withOpposites)

				with frameLayout('Unwanted nodes'):
					with rowColumnLayout():
						text(l='Unwanted nodes',bgc=cleanUnwanted)
						button(c='unwanted = %s; \
							cmds.select(clear=True); \
							cmds.select(unwanted,add=True)' % unwanted)
						
						# text(l='Empty Transform nodes',bgc=cleanemptyTransforms)
						# button(c='emptyTransforms = %s; \
						# 	cmds.select(clear=True); \
						# 	cmds.select(emptyTransforms,add=True)' % emptyTransforms)

	

def addID(ID,*args):
	sel = cmds.ls(selection=True)
	for i in sel :
		if '_ID' in i:
			cmds.warning(i+' already has an ID')
		else :
			cmds.rename(i,i+'_ID'+ID)
			fixShapesNames()

def removeID(*args):
	sel = cmds.ls(selection=True)
	for i in sel :
		if '_ID' in i:
			objectName, sep, IDname = i.partition('_ID')
			cmds.rename(i,objectName)
			fixShapesNames()
		else :
			cmds.warning('no ID found for '+i)

def exportRIBarchive(*args):
	pass

def fixShapesNames(*args):
	sel = cmds.ls(sl=True)
	shapes = cmds.listRelatives(sel,s=True,fullPath=True)
	if not shapes:
		cmds.warning('No shape were found in selection')
	else:
		for shape in shapes :
			cmds.rename(shape, "{0}Shape".format(cmds.listRelatives(shape, parent=True)[0]))

def exportMayaAscii(*args):
	import maya.mel as mel
	mel.eval('ExportSelection;')

def exportAbcRfM(*args): #Export alembic avec attributes renderman
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

def exportGPUcache(*args):
	try:
		import sys
		rmScripts = os.path.abspath('C:/Program Files/Pixar/RenderManForMaya-22.1/scripts/rfm2/utils')
		sys.path.insert(0,rmScripts)
		import abc_support
		abc_support.export(True, True)
	except NameError:
		import maya.cmds
		import maya.utils
		maya.utils.executeDeferred('''maya.cmds.loadPlugin('RenderMan_for_Maya.py')''')

def createAssetBackupDir(*args):
	publishedPath = os.path.abspath(cmds.workspace(sn=True,q=True))
	backupAssetPath = os.path.join(publishedPath,'backup',todaysDate())
	if not os.path.exists(backupAssetPath):
		os.makedirs(backupAssetPath)
		return backupAssetPath
	else:
		return backupAssetPath

def backupPublishedAsset(*args):
	publishedPath = os.path.abspath(cmds.workspace(sn=True,q=True))
	publishedAsset = os.path.join(publishedPath,currentShot())
	filetypes = ['.ma','.abc','.rib']
	from shutil import copyfile
	for i in filetypes:
		srcFile = publishedAsset + i
		dstFile = os.path.join(createAssetBackupDir(),currentShot()+i)
		try :
			copyfile(srcFile,dstFile)
			print 'Successfully backed up '+srcFile+' to '+dstFile
		except :
			cmds.warning('No '+i+' file previously published for '+currentShot())
	publishAsset()

def publishAsset(*args):
	pass

def basicAssetRig(*args):
	'''This will create a basic rig for every variation of the asset so it can be
	used during shot layout. The controller size is set using the object bounding box'''
	import fnmatch
	import commonTools
	reload(commonTools)

	# 1. Test if asset is in the scene and has a correct name
	curAsset = commonTools.currentShot()
	correctName = '%s*:%s*_grp'%(curAsset,curAsset)
	filtered = fnmatch.filter(cmds.ls(), correctName)
	if not filtered :
		wmessage = 'No matching group was found. Master group should look like : %s (where * can be replaced by anything)'%correctName
		cmds.warning(wmessage)
		return
	else :
		sel = filtered
	
	for var in sel:
		# 2. Test if scene has multiple variations
		varName, sep, rest = var.partition(':')

		# 3. get bbox info
		bbox = cmds.exactWorldBoundingBox(var)
		averageScale = (abs(bbox[0])+abs(bbox[3])+abs(bbox[2])+abs(bbox[5]))/4

		# 4. Create controlers
		ctrl = cmds.circle()
		cmds.setAttr(ctrl[0]+'.scaleX',averageScale)
		cmds.setAttr(ctrl[0]+'.scaleZ',averageScale)
		cmds.setAttr(ctrl[0]+'.scaleY',averageScale)
		cmds.setAttr(ctrl[0]+'.rotateX',90)
		cmds.makeIdentity(ctrl,a=True)
		cmds.delete(ctrl,constructionHistory=True)
		ctrl = cmds.rename(ctrl[0],varName+'_ctrl')
		cmds.parent(var,ctrl)
		# 5. create offsets and groups
		off = cmds.group(ctrl,n=varName+'_off')
		cmds.group(off,n=varName+'_master')
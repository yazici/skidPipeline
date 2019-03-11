# ****************************************** S K I D    R E N D E R    T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import commonTools,os

# ****************************************** G L O B A L S ******************************************

deltaAbc = ['propsBrevell','propsWerner','propsEthanHelmet','propsAltonHelmet','characterEthan']

# ****************************************** F U N C T I O N S ******************************************

def readCasting(*args):
	'''This will read the cast file for the current shot and import'''
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	shotName = os.path.split(scenePath)[1]
	castFile = scenePath+'/data/'+shotName+'_setDress.cast'

	# Load ATOM plugin
	cmds.loadPlugin('atomImportExport.mll')

	# Init cameras
	# commonTools.initCam()

	# Test if cast file exists
	if not os.path.exists(castFile):
		cmds.warning('Cast file does not exist for this shot. Should be : '+castFile)
		return

	# Test if atom file exists
	atomFile = scenePath+'/data/'+shotName+'_setDress.atom'
	if not os.path.isfile(atomFile):
		cmds.warning('Atom file does not exist for this shot. Should be : '+atomFile)
		return

	# User prompt before import
	with open(castFile) as f:
		for i, l in enumerate(f):
			pass
	lines = i+1
	message = 'You are about to import the shot casting which contains %s assets. This will take some time, consider heading to the nearest coffee machine. Continue ?'%lines
	confirm = cmds.confirmDialog(title='Import shot casting',message=message, button=['Continue','Open .cast file','Cancel'], \
		defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel')
	if confirm == 'Open .cast file':
		openCastFile(castFile)
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
		asset,ns = l.split()

		# Reference file
		print('// Importing : '+asset+' with namespace : '+ns+' //')
		cmds.file(asset,r=True,type='mayaAscii',ignoreVersion=True,gl=True,ns=ns,returnNewNodes=True)

		# Group
		# master = ns + '_master'
		# try :
		# 	cmds.parent(master,masterGrp)
		# except ValueError :
		# 	cmds.warning('Could not parent master : '+master)

		# Apply ATOM transforms
		ctrls.append(ns+':'+os.path.split(l[0])[1]+'_rig:'+os.path.split(l[0])[1]+'_ctrl')
	# cmds.select(ctrls,r=True)
	cmds.select(clear=True)
	for ctrl in ctrls :
		try :
			cmds.select(ctrl,add=True)
		except ValueError :
			pass
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

def importShotAlembics(*args):
	'''This will import the animated alembic files for the current shot'''
	
	abcPath = cmds.workspace(q=True,rd=True) + 'abc/'
	toImport = []
	for i in deltaAbc :
		if os.path.exists(abcPath + i + '.abc') : # If animation is published...
			if cmds.objExists(i+'RN') == True: # If already in scene continue to next abc
				continue
			else :
				toImport.append(i)

	if not toImport :
		cmds.warning('No more animation to import')
	else :
		confirm = cmds.confirmDialog(title='Import Shot animations', \
			message='Found '+str(len(toImport))+' animation files to import. Continue ?', \
			button=['Continue','Cancel'], \
			defaultButton='Continue', \
			cancelButton='Cancel', \
			dismissString='Cancel' )
		if confirm == 'Continue':
			for i in toImport:
				resolvePath = os.path.join(abcPath,i+'.abc')
				resolvePath = os.path.abspath(resolvePath)
				# print resolvePath
				cmds.file(resolvePath,r=True,type='Alembic',ignoreVersion=True,gl=True,ns=i)
			

def importShaders(*args):
	'''This will import the corresponding shaders for the imported animations'''
	# List imported animations except if shader is already imported
	imported = []
	for i in deltaAbc :
		if cmds.objExists(i+'RN') == True and cmds.objExists(i+'_shdRN') == False :
			imported.append(i)

	# print(imported)

	# Verify if shader is published
	shdToImport = []
	shdToImportNS = []
	for i in imported:
		if i.startswith('props') == True:
			assetType = 'props'
		elif i.startswith('character') == True:
			assetType = 'character'
		else :
			cmds.warning('Could not resolve path for '+i)

		resolvePath = '//Merlin/3d4/skid/04_asset/' + assetType + '/' + i + '/' + i + '_shd.ma'
		check = os.path.exists(resolvePath)

		if not os.path.exists(resolvePath) :
			cmds.warning('Could not find published shaders for '+i)
		else :
			shdToImport.append(resolvePath)
			shdToImportNS.append(i+'_shd')

	# User prompt
	if not shdToImport :
		cmds.warning('No more shader to import')
	else :
		confirm = cmds.confirmDialog(title='Import Shaders', \
			message='Found '+str(len(shdToImport))+' shader files to import. Continue ?', \
			button=['Continue','Cancel'], \
			defaultButton='Continue', \
			cancelButton='Cancel', \
			dismissString='Cancel' )
		if confirm == 'Continue':
			for (i,ns) in zip(shdToImport,shdToImportNS) :
				print('Importing : ' + i)
				print('With namespace : '+ns)
				cmds.file(i,r=True,type='mayaAscii',ignoreVersion=True,gl=True,ns=ns)

def assignShaders(*args):
	'''This will automatically assign shaders depending on asset (based on namespace)
	 and depending on object (based on ID)'''

	# List objects with ID
	geometries = cmds.ls("*_ID*",r=True,tr=True)

	if geometries :
		# User prompt
		confirm = cmds.confirmDialog(title='Assign Shaders', \
			message='Found '+str(len(geometries))+' object with ID. Continue ?', \
			button=['Continue','Cancel'], \
			defaultButton='Continue', \
			cancelButton='Cancel', \
			dismissString='Cancel' )

		if confirm == 'Continue':
			for i in geometries:
				# On split le mot cle de l'ID
				ID = i.split('_ID', 1)[-1]
				# On split le namespace
				nameSpace = i.split(':',)[0]
				# Puis on reconstruie le nom du shading group :
				SG = nameSpace+'_shd:'+ID+'_SG'
				# Puis on assigne le shading group a la geo qui lui correspond
				try :
					cmds.sets(i,e=True,forceElement=SG)
				except TypeError :
					cmds.warning('Could not find matching Shading Group for '+i+', make sure your Shading Group name is : '+SG)
	else :
		cmds.warning('Could not find any object with ID')


def importForest(*args):
	'''This will import a generated RIB containing the instanced forest'''
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	shotName = os.path.split(scenePath)[1]

	ribFile = scenePath + '/geo/' + shotName + '_forest.rib'

	if not os.path.exists(ribFile) :
		cmds.warning('Could not find ' + ribFile)
	else :
		# Maya sucks so much that they included the import keyword in their command
		mel.eval('file -import -type "RIB"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "%s_forest"  -pr  -importTimeRange "combine" "%s";'%(shotName,ribFile))
		cmds.group(shotName+'_forest',n='FOREST_GRP')


# rename

def autoBias(auto,*args): # Argument must be boolean
	sel = cmds.ls(selection=True)
	sel = cmds.listRelatives(shapes=True)
	if auto == True :
		for i in sel :
			cmds.setAttr(i+'.rman_traceBias',0.01)
			cmds.setAttr(i+'.rman_autoBias',-1)
		cmds.inViewMessage(amg='Trace Bias set to Auto for %s objects' % (len(sel)), \
			pos='midCenter',fade=True )
	else :
		for i in sel :
			cmds.setAttr(i+'.rman_autoBias',0)
			val = cmds.getAttr(i+'.rman_traceBias')
			cmds.setAttr(i+'.rman_traceBias',val/10)
			print(i+'.rman_traceBias   set to  '+str(val/10))
		
		cmds.inViewMessage( \
			amg='Trace Bias divided by 10 for %s objects. Check script editor for values' % (len(sel)), \
			pos='midCenter',fade=True )

def motionSamples(inherit,*args): # Argument must be boolean
	sel = cmds.ls(selection=True)
	sel = cmds.listRelatives(shapes=True)
	if inherit == True :
		for i in sel :
			cmds.setAttr(i+'.rman_motionSamples',-1)
		cmds.inViewMessage(amg='Motion Samples set to inherit for %s objects' % (len(sel)), \
			pos='midCenter',fade=True )
	else :
		
		for i in sel :
			val = cmds.getAttr(i+'.rman_motionSamples')
			if val < 2 :
				cmds.setAttr(i+'.rman_motionSamples',2)
				val = 2
			cmds.setAttr(i+'.rman_motionSamples',val+1)
			print(i+'.rman_motionSamples   set to  '+str(val+1))
		
		cmds.inViewMessage( \
			amg='Added one motion sample for %s objects. Check script editor for values' % (len(sel)), \
			pos='midCenter',fade=True )
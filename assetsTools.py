# **************** SKID ASSETS TOOLS ****************

import maya.cmds as cmds
import maya.mel as mel
import maya.utils
from functools import partial
import sys
import os
import commonTools

# **************** GLOBALS ****************

sel =  [] #create a variable with the selected object

# **************** FUNCTIONS ****************

def setObject(*args): #Mise a zero de l asset
	if commonTools.testSelection() == None:
		sys.exit
	else :
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)#freeze transforms
		cmds.xform(cp=True) #center pivot
		cmds.move(rpr=True) #move to world center
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)#freeze transforms
		cmds.delete(all=True, ch=True) #delete history
		cmds.inViewMessage( amg='Ton asset <hl>'+str(sel)+'</hl> a ete mis a zero, bro.', pos='midCenter', fade=True )

def fixNormals (*arg): #Regler les problemes de normal angle
	if commonTools.testSelection() == None:
		cmds.warning('Nothing is selected')
	else :
		sel = commonTools.testSelection()
		selAD = cmds.listRelatives(sel,ad=True)
		for i in selAD:
			cmds.polyNormalPerVertex(i,ufn=True)
			cmds.polySetToFaceNormal(i) # probablement fait freeze aussi
			cmds.polySoftEdge(i,a=60)
		cmds.select(clear=True)
		cmds.select(sel,r=True)

def cleanup(*args):
	pass
	#cmds.polyCleanupArgList (4 ( "1","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0","0" ))

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
	for shape in shapes :
		cmds.rename(shape, "{0}Shape".format(cmds.listRelatives(shape, parent=True)[0]))

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

def prePublishAsset(*args):
	# On test que la selection soit bien au bon format
	correctName = currentShot()+'_grp' #le nom que doit avoir le groupe maitre
	if len(testSelection()) > 1:
		cmds.warning('Only one object must be selected for publish')
	elif len(testSelection()) == 1 and testSelection()[0] == correctName:
		assetFile = currentShot()+'.ma'
		publishPath = os.path.join(cmds.workspace(sn=True,q=True),assetFile)
		if os.path.exists(publishPath):
			cmds.warning('Asset already has published version, backing up previous version...')
			backupPublishedAsset()
		else :
			pass
		publishAsset()
	else :
		cmds.warning('Selected group should look like : '+correctName)

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

def renameDuplicates(*args):
    import re
    duplicates = [f for f in cmds.ls() if '|' in f]
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)
    if duplicates:
        for name in duplicates:
            m = re.compile("[^|]*$").search(name) 
            shortname = m.group(0)
            m2 = re.compile(".*[^0-9]").match(shortname) 
            if m2:
                stripSuffix = m2.group(0)
            else:
                stripSuffix = shortname
            newname = cmds.rename(name, (stripSuffix + "#")) 
            print "renamed %s to %s" % (name, newname)
        return False
    else:
        return True

def checkAssetStatus(*args):
	pass
	# check
	# Delete all history (sauf pour les riggs)
	# Mise a zero
	# Verif(Freeze scales) sauf pour les locators
	# rename shapes
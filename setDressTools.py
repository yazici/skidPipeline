# ****************************************** S K I D     S E T D R E S S     T O O L S ******************************************

import maya.cmds as cmds
import os,shutil,datetime
import commonTools

referenceNodes = cmds.ls(type='reference')

# ****************************************** F U N C T I O N S ******************************************

def RNfromSelection():
	'''This will select every master reference node for selected geometries that has a controller'''
	# 1. controllers from selection
	ctrls = []
	for n in cmds.ls(selection=True,referencedNodes=True) :
		if not 'ctrl' in n:
			pass
		else :
			ctrls.append(n)
	# 2. master reference node from ctrl
	rn = []
	for ctrl in ctrls:
		n = cmds.referenceQuery(ctrl,referenceNode=True,p=True)
		rn.append(n)
	return rn

def allRN():
	# Returns all Reference nodes in the scnene
	rn = []
	for n in cmds.ls():
		if not 'RN' in n:
			pass
		else:
			rn.append(n)
	return rn


def unloadSelected():
	for n in RNfromSelection():
		cmds.file(referenceNode=n,unloadReference=True)

# def loadSelected():
# 	for n in RNfromSelection():
# 		cmds.file(referenceNode=n,loadReference=True)

def loadAllReferences():
	sel = cmds.ls(selection=True)
	rn = []
	for i in sel :
		print(i)
		rn.append(cmds.referenceQuery(i,filename=True))
	for i in rn :
		print(i)
		cmds.file(i,force=True,reference=True,loadReferenceDepth='all')

def writeCasting():
	'''This will write a file containing all the file path of the reference assets for this shot
	and their respective namespace'''

	scenePath = cmds.workspace(sn=True,q=True)
	scenePath = scenePath.replace(os.sep, '/')
	sceneName = os.path.split(scenePath)[1]
	castFile = scenePath+'/data/'+sceneName+'_setDress.cast'

	# 1. Lister toutes les references dans le groupe SETDRESS_GRP
	setDress  = cmds.listRelatives('SETDRESS_GRP',allDescendents=True)

	rn = []
	for n in setDress:
		try :
			rn.append(cmds.referenceQuery(n,referenceNode=True))
		except RuntimeError :
			pass

	# 3. Merge duplicates
	rn = list(dict.fromkeys(rn))
	
	# 4. Blast sets	
	for n in rn:
		if not ':' in n :
			rn.remove(n)

	# 5. Keep only rig level references
	for n in rn:
		if not n.endswith('rigRN') :
			rn.remove(n)


	# print(rn)

	# 9. if .cast file already exists : backup and delete
	ts = datetime.datetime.now()
	ts = '%s%s%s_%s%s%s'%(ts.year,ts.month,ts.day,ts.hour,ts.minute,ts.second)
	backupFile = scenePath+'/data/backup/'+sceneName+'_'+ts+'.cast'	
	
	if os.path.isfile(castFile):
		shutil.copyfile(castFile,backupFile)
		os.remove(castFile)

	# # 10. cast file authoring
	with open(castFile,'w') as f:
		for i in rn :
			namespace = str(i)
			path = cmds.referenceQuery(i,filename=True,withoutCopyNumber=True)
			f.write("%s %s\n" %(path,namespace))
		f.close()

	# 11. Inview message
	print('\n// Result: '+castFile+' //')
	cmds.inViewMessage( \
		amg='Casting has bee written to <hl>'+sceneName+'/data/'+sceneName+'_setDress.cast</hl>', \
		pos='midCenter', \
		fade=True)
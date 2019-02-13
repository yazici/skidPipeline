# ****************************************** S K I D     S E T D R E S S     T O O L S ******************************************

import maya.cmds as cmds
import os,shutil,datetime

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

def loadSelected():
	for n in RNfromSelection():
		cmds.file(referenceNode=n,loadReference=True)

def writeCasting():
	# 1. Lister tout les nodes dans le groupe SETDRESS_GRP
	nodes = cmds.listRelatives('SETDRESS_GRP',ad=True)

	# 2. Fetch reference node from nodes
	rn = []
	for n in nodes:
		try :
			rn.append(cmds.referenceQuery(n,referenceNode=True))
		except RuntimeError :
			pass

	# Delete duplicates
	rn = list(dict.fromkeys(rn))
	
	# blasts sets
	for n in rn:
		if not ':' in n :
			rn.remove(n)

	# Fetch filename from reference nodes
	rf = []
	for n in rn:
		try :
			rf.append(cmds.referenceQuery(n,filename=True))
			# ,withoutCopyNumber=True
		except RuntimeError :
			pass

	# Blast modeling-level and rig-level references
	# for f in rf:
	# 	typeToBlast = ['rig.ma','.abc']
	# 	for t in typeToBlast :
	# 		if not t in n :
	# 			pass
	# 		else :
	# 			rf.remove(f)
	res = [k for k in rf if 'rig.ma' in k]
	print(res)



	# Creer dossier data et backup
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	if not os.path.exists(scenePath+'/data/backup'):
		os.makedirs(scenePath+'/data/backup')

	# Ecrire le cast dans un fichier .cast
	sceneName = os.path.split(scenePath)[1]
	castFile = scenePath+'/data/'+sceneName+'.cast'

	# if .cast file already exists : backup and delete
	ts = datetime.datetime.now()
	ts = '%s%s%s_%s%s%s'%(ts.year,ts.month,ts.day,ts.hour,ts.minute,ts.second)
	backupFile = scenePath+'/data/backup/'+sceneName+'_'+ts+'.cast'	
	
	if os.path.isfile(castFile):
		shutil.copyfile(castFile,backupFile)
		os.remove(castFile)

	# .cast file authoring
	
	with open(castFile,'w') as f:
		for item in rf:
			f.write("%s\n" % item)
		f.close()

	# Inview message
	print('\n.cast file : ')
	print(castFile)
	print('\nbackup .cast file : ')
	print(backupFile)
	cmds.inViewMessage(amg='Casting has bee written to <hl>'+castFile+'</hl>',pos='midCenter',fade=True)
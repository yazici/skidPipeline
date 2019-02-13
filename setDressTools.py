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

def loadSelected():
	for n in RNfromSelection():
		cmds.file(referenceNode=n,loadReference=True)

def writeCasting():
	scenePath = os.path.abspath(cmds.workspace(sn=True,q=True))
	scenePath = scenePath.replace(os.sep, '/')
	sceneName = os.path.split(scenePath)[1]

	message = 'You are about to publish a shot casting for ' + sceneName + ' . this will backup and replace any previously published casting.'
	confirm = cmds.confirmDialog(title='Publish shot casting',message=message, button=['Continue','Cancel'], \
		defaultButton='Continue', cancelButton='Cancel', dismissString='Cancel')
	if confirm != 'Continue':
		return

	# 1. Lister tout les nodes dans le groupe SETDRESS_GRP
	nodes = cmds.listRelatives('SETDRESS_GRP',ad=True)

	# 2. Fetch reference node from nodes
	rn = []
	for n in nodes:
		try :
			rn.append(cmds.referenceQuery(n,referenceNode=True))
		except RuntimeError :
			pass

	# 3. Delete duplicates
	rn = list(dict.fromkeys(rn))
	
	# 4. Blast sets
	for n in rn:
		if not ':' in n :
			rn.remove(n)

	# 5. Fetch filename from parent reference nodes
	rf = []
	for n in rn:
		try :
			rf.append(cmds.referenceQuery(n,filename=True,parent=True))
			# ,withoutCopyNumber=True
		except RuntimeError :
			pass

	# 6. Blast modeling-level and rig-level references
	toBlast = [k for k in rf if 'abc' in k] 
	rf = list(set(rf) - set(toBlast))

	toBlast = [k for k in rf if 'rig' in k] 
	rf = list(set(rf) - set(toBlast))


	# 7. Creer dossier data et backup
	if not os.path.exists(scenePath+'/data/backup'):
		os.makedirs(scenePath+'/data/backup')

	# 8. Ecrire le cast dans un fichier .cast
	
	castFile = scenePath+'/data/'+sceneName+'.cast'

	# 9. if .cast file already exists : backup and delete
	ts = datetime.datetime.now()
	ts = '%s%s%s_%s%s%s'%(ts.year,ts.month,ts.day,ts.hour,ts.minute,ts.second)
	backupFile = scenePath+'/data/backup/'+sceneName+'_'+ts+'.cast'	
	
	if os.path.isfile(castFile):
		shutil.copyfile(castFile,backupFile)
		os.remove(castFile)

	# 10. .cast file authoring
	with open(castFile,'w') as f:
		for item in rf:
			f.write("%s\n" % item)
		f.close()

	# 11. Inview message
	print('\n.cast file : ')
	print(castFile)
	print('\nbackup .cast file : ')
	print(backupFile)
	cmds.inViewMessage(amg='Casting has bee written to <hl>'+sceneName+'/data/'+sceneName+'.cast</hl>',pos='midCenter',fade=True)
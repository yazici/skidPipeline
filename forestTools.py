# ****************************************** S K I D     F O R E S T     T O O L S ******************************************

import maya.cmds as cmds
import maya.mel as mel
import os, subprocess

# ****************************************** G L O B A L S ******************************************



# ****************************************** F U N C T I O N S ******************************************

def fireHoudini(mtop,mright,mbot,mleft,*args):
	'''This function opens a headless version of houdini and computes
	a point cloud for trees instancing depending on the shot camera position and movements.
	Arguments are camera frustrum margins and should be a float between 0 and 1'''
	
	# User prompt before firing up
	confirmTxt = 'This process can take some minutes. Please check your frame range and margins are right before you continue.'
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
	print(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft)
	# os.system('hython %s %s %s %s %s %s %s %s'%(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft))
	# os.system('hython //Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.py')
	subprocess.call('hython %s %s %s %s %s %s %s %s'%(houScript,currentShot,fstart,fend,mtop,mright,mbot,mleft))

def checkHoudiniEngine(*args):
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

'''
def loadShotPoints(*args):
	# This function will load the generated point cloud in Maya via Houdini Engine
	if checkHoudiniEngine() == False:
		return
	toolBgeoToMaya = os.path.abspath('//merlin/3d4/skid/04_asset/hda/toolBgeoToMaya.hda')
	cmds.houdiniAsset(la=[toolBgeoToMaya,'Object/toolBgeoToMaya'])
	#set file path to shot points
	currentWorkspace = os.path.abspath(cmds.workspace(sn=True,q=True))
	currentShot = os.path.split(currentWorkspace)[1]
	pointsFromHoudini = currentWorkspace+'/geo/fileCache'+currentShot+'.fc_pointsToMaya.$F4.bgeo.sc'
	cmds.setAttr('toolBgeoToMaya1.houdiniAssetParm.houdiniAssetParm_file',pointsFromHoudini,type="string")
	cmds.evalDeferred('cmds.houdiniAsset(syn="toolBgeoToMaya1")') #sync


	# Nom du sys de part cree par l'asset - a rentrer a la main pour le moment
	string $hdaPartXf = "file_bgeoToMaya_0";
	# // List des attr a transferer - a rentrer a la main pour le moment
	string $vectorAttrListToTransfert[] = {"rgbPP", "radiusPP", "particleId "};
	# // New name suffixe - a rentrer a la main
	string $newNameSuffixe = "dupli";


	# // On recupere le nom de la shape du sys de part
	$ShpList = `listRelatives -s $hdaPartXf`;
	string $hdaPartShp = $ShpList[0];

	# // compte le nb de particules
	$nbPart = `particle -q -ct $hdaPartXf`;

	# // Creation du nouveau sys de part av le suffixe dans le nom
	$tmp = `particle -n ($hdaPartXf+"_"+$newNameSuffixe)`;
	$dupliPartXf = $tmp[0];
	$dupliPartShp = $tmp[1];

	# // On cree tous les attr sur le nouveau system
	for($attr in $vectorAttrListToTransfert)
		addAttr -ln $attr -dt vectorArray $dupliPartShp;
		addAttr -ln ($attr+"0") -dt vectorArray $dupliPartShp;
		# // le attr0 doit etre la valeur initiale, ca ne fonctionne pas sans la creation.

	# // On remplit le nouveau sys en recuperant la pos des particules
	for($i=0; $i<$nbPart; $i++)
		$wPos = `getParticleAttr -at position -array true ($hdaPartShp+".pt["+$i+"]")`;
		emit -o $dupliPartXf -pos $wPos[0] $wPos[1] $wPos[2];

	# // On transfere les attr type vector
	for($i=0; $i<$nbPart; $i++) {
		for($attr in $vectorAttrListToTransfert)
			$attrValue = `getParticleAttr -at $attr -array true ($hdaPartShp+".pt["+$i+"]")`;
			# // setParticleAttr -at $attr -vv $attrValue[0] $attrValue[1] $attrValue[2] ($dupliPartShp+".pt["+$i+"]");
			particle -e -at $attr -order $i -vv $attrValue[0] $attrValue[1] $attrValue[2];
'''
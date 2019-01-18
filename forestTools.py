import maya.cmds as cmds
import maya.mel as mel
import os


def fireHoudini(*args):
	houScript = '//Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.py'
	# Check current shot
	currentWorkspace = os.path.abspath(cmds.workspace(sn=True,q=True))
	currentShot = os.path.split(currentWorkspace)[1]
	# Fire headless Houdini 
	os.system('hython createInstancerPoints.py %s %s %s' currentShot,arg1,arg2)

def checkHoudiniEngine(*args):
	cmds.loadPlugin('houdiniEngine')
	EngineVersion = mel.eval('houdiniEngine -hv;')
	if not '17.' in EngineVersion :
		cmds.warning('Wrong Houdini Engine version (installed version is '+EngineVersion+'), should be at least version 17')
		return False
	else :
		return True

def loadShotPoints(*args):
	toolBgeoToMaya = os.path.abspath('//merlin/3d4/skid/04_asset/hda/toolBgeoToMaya.hda')
	cmds.houdiniAsset(la=[toolBgeoToMaya,'Object/toolBgeoToMaya'])
	#set file path to shot points
	currentWorkspace = os.path.abspath(cmds.workspace(sn=True,q=True))
	currentShot = os.path.split(currentWorkspace)[1]
	pointsFromHoudini = currentWorkspace+'/geo/fileCache'+currentShot+'.fc_pointsToMaya.$F4.bgeo.sc'
	cmds.setAttr('toolBgeoToMaya1.houdiniAssetParm.houdiniAssetParm_file',pointsFromHoudini,type="string")
	cmds.evalDeferred('cmds.houdiniAsset(syn="toolBgeoToMaya1")') #sync


	# Nom du sys de part cree par l'asset - à rentrer à la main pour le moment
	string $hdaPartXf = "file_bgeoToMaya_0";
	# // List des attr à transferer - à rentrer à la main pour le moment
	string $vectorAttrListToTransfert[] = {"rgbPP", "radiusPP", "particleId "};
	# // New name suffixe - à rentrer à la main
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
		# // le attr0 doit etre la valeur initiale, ca ne fonctionne pas sans la création.

	# // On remplit le nouveau sys en recupérant la pos des particules
	for($i=0; $i<$nbPart; $i++)
		$wPos = `getParticleAttr -at position -array true ($hdaPartShp+".pt["+$i+"]")`;
		emit -o $dupliPartXf -pos $wPos[0] $wPos[1] $wPos[2];

	# // On transfere les attr type vector
	for($i=0; $i<$nbPart; $i++) {
		for($attr in $vectorAttrListToTransfert)
			$attrValue = `getParticleAttr -at $attr -array true ($hdaPartShp+".pt["+$i+"]")`;
			# // setParticleAttr -at $attr -vv $attrValue[0] $attrValue[1] $attrValue[2] ($dupliPartShp+".pt["+$i+"]");
			particle -e -at $attr -order $i -vv $attrValue[0] $attrValue[1] $attrValue[2];

	if checkHoudiniEngine() == True:
		loadShotPoints()
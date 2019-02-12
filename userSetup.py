import maya.cmds as cmds
import os

# Load msetProject
import mSetProject
mSetProject.main()

# Load Skid Environment
def SkidPlugin():
	SkidToolsPath = os.path.abspath('//Merlin/3d4/skid/09_dev/toolScripts/publish')
	if os.path.exists(SkidToolsPath):
		#run setup
		import mayaSetup	
		mayaSetup.setupTools()	
	else:
		print 'ERROR : SkidTools path doesnt exist. Please contact Val and bring him coffee because he will need some'

scriptJobNum = cmds.scriptJob(event = ["NewSceneOpened", SkidPlugin])


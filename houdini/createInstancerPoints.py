# hython createInstancerPoints.py 'seq0010_sh0050'


import sys, os

# Get params from shell command
currentShot = sys.argv[1] # Current shot (camera name)
fstart = float(sys.argv[2]) # Start Frame
fend = float(sys.argv[3]) # End Frame
mtop = float(sys.argv[4]) # Margin top
mright = float(sys.argv[5]) # Margin right
mbot = float(sys.argv[6]) # Margin bot
mleft = float(sys.argv[7]) # Margin left
depth = float(sys.argv[8]) # Depth
focalLength = float(sys.argv[9]) # focalLength

# Convert margins to houdini values
mright += 1
mtop += 1
mleft = - mleft
mbot = - mbot

print('Generating instancer with arguments :\n')
print('currentShot : '+currentShot,type(currentShot))
print('fstart : ',fstart,type(fstart))
print('fend : ',fend,type(fend))
print('mtop : ',mtop,type(mtop))
print('mright : ',mright,type(mright))
print('mbot : ',mbot,type(mbot))
print('mleft : ',mleft,type(mleft))
print('depth : ',depth,type(depth))
print('focalLength : ',focalLength,type(focalLength))


# 1. Load scene containing setGleitenstrassen, toolCamImport
houScenePath = '//Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.hipnc'
hou.hipFile.load(houScenePath,suppress_save_prompt=True)
obj = hou.node('/obj')
print('Scene contents :')
for node in obj.allItems():
    print node.path()
print('Loaded scene succesfully')


# 2. Set toolCamImport to current shot
# Verify if camera alembic exists :
abcPath = '//Merlin/3d4/skid/05_shot/%s/abc/%s.abc'%(currentShot,currentShot)
if not os.path.isfile(abcPath):
	print('%s was not found. Please export your camera from Maya before you can continue.'%abcPath)
	os.system('pause')
	sys.exit()
cam = '/obj/CameraImport1/'
hou.parm(cam+'fileName').set(abcPath)
hou.parm(cam+'buildHierarchy').pressButton()
# Modify camera focal length and fetch
hou.parm('/obj/CameraImport1/renderCam/focal').set(str(focalLength))
# Set camera fetch transform
fetchPath = '/obj/CameraImport1/fetch1/'
hou.parm(fetchPath + 'fetchobjpath').set('../shotCamera/'+str(currentShot))


# 3. Set up volume parameters
volumePath = '/obj/instance_pointClouds_GEO/volume1/'
# camPath = '%sshotCamera/%s/%sShape'%(cam,currentShot,currentShot)
# hou.parm(volumePath+'camera').set(camPath)
# Set margins
hou.parm(volumePath+'winxmin').set(str(mleft))
hou.parm(volumePath+'winxmax').set(str(mright))
hou.parm(volumePath+'winymin').set(str(mbot))
hou.parm(volumePath+'winymax').set(str(mtop))
hou.parm(volumePath+'zmax').set(str(depth))
print('Volume setup done')


# 4. Set framerange
hou.playbar.setFrameRange(fstart,fend)
hou.playbar.setPlaybackRange(fstart,fend)
hou.setFrame(fend)
print('Frame range set to : %s - %s'%(fstart,fend))


# 5. Filecache
fcPath = '/obj/instance_pointClouds_GEO/fc_pointsToMaya/'
bgeoPath = '//Merlin/3d4/skid/05_shot/%s/geo/fileCache/%s_instancerPts.bgeo.sc'%(currentShot,currentShot)
hou.parm(fcPath+'file').set(str(bgeoPath))
print('Caching instancer points to : '+bgeoPath)
hou.parm(fcPath+'execute').pressButton()


# 6. Check if bgeo exists
if not os.path.isfile(bgeoPath):
	print('Point cloud cache FAILED for '+currentShot)
	os.system('pause')
	hou.exit(exit_code=1, suppress_save_prompt=True)
else :
	print('Point cloud was succesfully cached for %s, cache path is :'%currentShot)
	print(bgeoPath)
	os.system('pause')
	hou.exit(exit_code=0, suppress_save_prompt=True)
# hython createInstancerPoints.py 'seq0010_sh0050'

import sys, os

# Get params from shell command
currentShot = sys.argv[1] # Current shot (camera name)
fstart = sys.argv[2] # Start Frame
fend = sys.argv[3] # End Frame
mtop = sys.argv[4] # Margin top
mright = sys.argv[5] # Margin right
mbot = sys.argv[6] # Margin bot
mleft = sys.argv[7] # Margin left

print('Generating instancer points for %s' %currentShot)

# hou.hipFile


# 1. Load setGleitenstrassen, toolCamImport
hdaPath = '//merlin/3d4/skid/04_asset/hda/'
hdaFiles = 'setGleitenstrasse.hdanc','toolCamImport.hdanc'
# for hda in hdaFiles:
# 	hou.hda.installFile(hdaPath+hda)
hou.hda.installFile(hdaPath+hdaFiles[1]) # temp pour pas load gleiten

# print hou.hda.loadedFiles()


# 2. Set shot camera
hou.parm('/obj/CameraImport1/fileName').set('$SHOT/%s/abc/%s.abc'(currentShot,currentShot))
# Build / update hierarchy


# 3. Set up volume parameters
volume = '/obj/setGleitenstrasse1//***/volume1'
# Set camera name
hou.parm(volume+'/camera').set('/obj/CameraImport1')
# Convert margins to houdini's weird values
mright += 1
mtop += 1
mleft = - mleft
mbot = - mbot
# Set margins
hou.parm(volume+'/winxmin').set(mleft)
hou.parm(volume+'/winxmax').set(mright)
hou.parm(volume+'/winymin').set(mbot)
hou.parm(volume+'/winymax').set(mtop)

# 4. Set framerange
hou.playbar.setFrameRange(fstart,fend)
hou.playbar.setPlaybackRange(fstart,fend)
hou.setFrame(fend)
# Verifier que le timeshift a bien $FEND en value


# 5. Filecache
bgeoPath = hou.parm.('').eval()
print('Caching instancer points to : %s'%bgeoPath)


# 6. Check if bgeo exists
if not os.path.exist(bgeoPath):
	print('Something went wrong')
	hou.exit(exit_code=1, suppress_save_prompt=True)
else :
	print('Instancer points were succesfully cached for %s'%currentShot)
	hou.exit(exit_code=0, suppress_save_prompt=True)


# 7. Pause and quit
os.system('pause')
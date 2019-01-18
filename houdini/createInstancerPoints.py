# hython createInstancerPoints.py 'seq0010_sh0050'

import sys, hou

# Get params from shell command
currentShot = sys.argv[1]
# renderNode = sys.argv[2]
# startFrame = sys.argv[3]
# endFrame = sys.argv[4]
# jobPriority = sys.argv[5]

print 'Generating instancer points for %s' %currentShot

# hou.hipFile


# 1. Load setGleitenstrassen, toolCamImport
hdaPath = '//merlin/3d4/skid/04_asset/hda/'
hdaFiles = 'setGleitenstrasse.hdanc','toolCamImport.hdanc'
# for hda in hdaFiles:
# 	hou.hda.installFile(hdaPath+hda)
hou.hda.installFile(hdaPath+hdaFiles[1]) # temp pour pas load gleiten

# print hou.hda.loadedFiles()

# 2. Load shot camera
hou.parm('/obj/CameraImport1/fileName').set('$SHOT/%s/abc/%s.abc'(currentShot,currentShot))

# 3. Change camera in volume

# 4. Filecache

# 5. quit
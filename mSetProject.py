# -*- coding: utf-8 -*-
'''
===================================================================================

    mSetProject

===================================================================================
    ver 2.02     2016/08/01
    ver 2.01     2016/05/13
    ver 2.00     2016/05/10
    Author:     Martin Yara
    www.skymill.co.jp
   
    Based on Tod's research http://www.toadstorm.com/blog/?p=427
    
-----------------------------------------------------------------------------------
    Automatically Set Project before Opening a file
-----------------------------------------------------------------------------------
   INSTALL
 
   - Copy this file to your scripts Folder
   - Open your scripts/userSetup.py inside your Maya Folder with an text editor or NotePad
      (ex: C:\Users\myara\Documents\maya\scripts\userSetup.py)
   - If userSetup.py doesn't exists, create one with your NotePad
   - Add the follow command to the userSetup.py
   
import mSetProject
mSetProject.main()
   
   UNINSTALL
   
   - Delete this file and those 2 lines from your userSetup.py
-----------------------------------------------------------------------------------
History

2.0.0 First release
2.0.1 Added support for Japanese Characters. Changed the viewport message mode in 2014.
2.0.2 Fixed bug where it reOpens the scene if Maya finds errors in the Scene.

'''
import pymel.core as pm
import os
import maya.OpenMaya as om
from maya import cmds

callbackID = None

def lookForWorkspace( scenePath, limit=10 ):
    #limit is the number of steps it will look up to
    fol = scenePath[0 : scenePath.rfind( os.path.basename(scenePath) ) ]
    scenePathsplit = scenePath.split("/")

    #Use : ##  for i in range(len(scenePathsplit)-1): ##
    #to search in all directories (until it hits the drive letter)
    
    for i in range( limit ):
        fol = fol[0 : fol.rfind( os.path.basename(fol) ) -1]
        if fol[-1:] != ":" and os.path.exists(fol + "/workspace.mel"):
            return fol
    #if found, return Folder
    #if not, return None
    
 
def setProj(retCode, fileObject, clientData):
    global callbackID
    path = fileObject.rawFullName()
    
    #----JAPANESE CHARACTER WORKAROUND-------------------------
    # Convert path to string
    # If it fails, it means it has some non-english characters
    # I haven't found a way to determinate all the encoding types that Maya supports
    # so I'm assuming they are Shift_JIS characters
    #-----------------------------------------------------------
    J = False
    
    #Convert Path to string
    try:
        path = str(path)
    #If it fails, assume it is Japanese encoding
    except:
        J = True
        path = path.encode('shift_jis')

    curWS = cmds.workspace( query=True, fullName=True )
    if J==True: curWS = curWS.encode('shift_jis')
    
    newWS = lookForWorkspace( path )
    
    if newWS != None and curWS != newWS:
        pm.mel.setProject( newWS )
 
        print "======================================================================"
        print " mSetProject"
        print "----------------------------------------------------------------------"
        print " set Project to " + newWS
        print "======================================================================"
        
        printPath( newWS )
    
    om.MScriptUtil.setBool(retCode,True)
    
def printPath( path ):
    #change / with \\ in path:
    pathTXT = path.replace("/","\\")
    #get Maya Version (Display in viewport is only supported by 2014 and later
    MayaVer = pm.versions.current() / 100

    #Display path in viewport:
    if MayaVer >= 2014:
        cmds.inViewMessage( amg='Project Changed to: \n <hl>' + pathTXT + '</hl>.', pos='topCenter', fade=True )
        
        #Maya 2014 can also use inViewMessage but it seems buggy (not always work)
        if MayaVer == 2014:
            cmds.headsUpMessage( 'Project Changed to : ' + pathTXT, time=2.0 )
    else:
        cmds.headsUpMessage( 'Project Changed to : ' + pathTXT, time=2.0 )
 
def main():
    global callbackID
    callbackID = om.MSceneMessage.addCheckFileCallback(om.MSceneMessage.kBeforeOpenCheck, setProj)
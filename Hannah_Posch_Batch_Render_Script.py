## Hannah Posch - Render View Window Batch Render (Spring 2015)
## Code was written to enhance Maya batch render function, as sometimes scene files result in batch render error, or render slower during 
## Maya batch render due to less CPU usage, and this code allows user to utilize the render window for batch rendering.
## Note: Render 1 shot via camera perspective wanted for batch render in render view before beginning. 
## Note: All project settings and camera settings should be complete.
## Instructions: Import code into Maya Script Editor Python tab, select script and press execute. Batch Render window settings will open. 
## Fill out necessary info for frame range, file output and image size. Renderable camera will be the camera last rendered in render view.
## Note: Rendered images will save to Maya 'set project' directory.

## Import command library
import maya.cmds as cmds
import maya.OpenMaya as api
import maya.mel as mel

 
## set the default name for the window
winName = 'myWindow'
cancel_render = 0

## if the window already exists, delete it
if cmds.window( winName, q=True, exists=True ):
    cmds.deleteUI( winName )
 
## create window
win = cmds.window( winName, title='Batch Render' )
 
## create layout
col = cmds.columnLayout( adjustableColumn=True, columnAlign="left" )
 
## create controls
## Render Options
cmds.text( label='Batch render in render window' )


## Start/End Frame
cmds.text( label='\n\nFrame Range' )
cmds.intFieldGrp('sf', label='Start Frame:', value1=1 )
cmds.intFieldGrp( 'ef', label='End Frame:', value1=100 )


## File Output
cmds.text( label='\n\nFile Output' )
preText = cmds.textFieldGrp( 'fnp', label='File name prefix:', text='not set; using scene name' )
fileType = cmds.optionMenuGrp( 'ft',label='Image Format:' )
cmds.menuItem( label='Maya IFF (iff)' )
cmds.menuItem( label='JPEG (jpg)' )
cmds.menuItem( label='PNG (png)' )
cmds.menuItem( label='PSD Layered (psd)' )
cmds.menuItem( label='TIFF (tif)' )
frame_amin_ext = cmds.optionMenuGrp('fae', label='Frame/Animation ext:')
cmds.menuItem( label='name.#.ext' )
cmds.menuItem( label='name.ext.#' )
cmds.menuItem( label='name.#' )
cmds.menuItem( label='name#.ext' )
cmds.menuItem( label='name_#.ext' )

## Renderable Camera
cmds.text( label='\n\nRenderable Camera' )
camType = cmds.optionMenuGrp( 'cam_type',label='Renderable Camera:')
cmds.menuItem( label='persp' )
cmds.menuItem( label='\n' )
cmds.menuItem( label='front' )
cmds.menuItem( label='side' )
cmds.menuItem( label='top' )

## Image Size
cmds.text( label='\n\nImage Size' )
cmds.intFieldGrp( 'image_w',label='Width:', value1= 1920 )
cmds.intFieldGrp( 'image_h',label='Height:', value1= 1080 )


#Batch Render Buttons
cmds.button( label='Batch Render', command='buttonMethod()' )

 
# show window
cmds.showWindow( win )



    
    
 
   
    
   

#Create Button Method for the Batch Render button
def buttonMethod():
        
    
    #Getting Start and Stop Numbers
    startNum = int(cmds.intFieldGrp('sf', query = True, value1 = True))
    endNum = int(cmds.intFieldGrp('ef', query = True, value1 = True))
    
    
    #Error checking puts up a warning dialog box
    if (startNum > endNum):
        cmds.confirmDialog(title = 'Warning', message='Start Frame is greater than End Frame')
        return 
        
              
    # Getting File name prefix
    
    my_fnp = cmds.textFieldGrp('fnp',query = True, text = True)
    
    found_it = my_fnp.find('not set') # find will return 0 if found and -1 if not found
    
    if (found_it == -1): # did not find 'not set' so the user wants a prefix       
        cmds.setAttr ("defaultRenderGlobals.imageFilePrefix",my_fnp,type="string")
        
        

        
    ## setting image/file type
    my_ft = int(cmds.optionMenuGrp('ft', query = True, select = True))
          
    if (my_ft == 1):
        cmds.setAttr ("defaultRenderGlobals.imageFormat",7) # IFF format
        my_file_type = "iff"
    if (my_ft == 2):
        cmds.setAttr ("defaultRenderGlobals.imageFormat",8) # JPEG format
        my_file_type = "jpg"
    if (my_ft == 3):
        cmds.setAttr ("defaultRenderGlobals.imageFormat",32) # PNG format
        my_file_type = "png"
    if (my_ft == 4):
        cmds.setAttr ("defaultRenderGlobals.imageFormat",31) # PSD format
        my_file_type = "psd"
    if (my_ft == 5):
        cmds.setAttr ("defaultRenderGlobals.imageFormat",3) # TIFF format
        my_file_type = "tiff"
        
        
    # Getting the Frame Animation extension
    my_fae = int(cmds.optionMenuGrp('fae', query = True, select = True))
    if (my_fae == 1): # the user wants name.#.ext
        cmds.setAttr ("defaultRenderGlobals.outFormatControl",0)
        cmds.setAttr ("defaultRenderGlobals.periodInExt",1)
        cmds.setAttr ("defaultRenderGlobals.outFormatExt",my_file_type,type="string")
        cmds.setAttr ("defaultRenderGlobals.useFrameExt",1)
        cmds.setAttr ("defaultRenderGlobals.putFrameBeforeExt",1)
    if (my_fae == 2): # the user wants name.ext.#
        cmds.setAttr ("defaultRenderGlobals.outFormatControl",2)
        cmds.setAttr ("defaultRenderGlobals.periodInExt",1)
        cmds.setAttr ("defaultRenderGlobals.outFormatExt",my_file_type,type="string")
        cmds.setAttr ("defaultRenderGlobals.useFrameExt",0) 
        cmds.setAttr ("defaultRenderGlobals.putFrameBeforeExt",0)
    if (my_fae == 3): # the user wants name.#
        cmds.setAttr ("defaultRenderGlobals.outFormatControl",1)
        cmds.setAttr ("defaultRenderGlobals.useFrameExt",0) 
        cmds.setAttr ("defaultRenderGlobals.putFrameBeforeExt",1)   
    if (my_fae == 4): # the user wants name#.ext
        cmds.setAttr ("defaultRenderGlobals.outFormatControl",2)
        cmds.setAttr ("defaultRenderGlobals.periodInExt",0)
        cmds.setAttr ("defaultRenderGlobals.outFormatExt",my_file_type,type="string")
        cmds.setAttr ("defaultRenderGlobals.useFrameExt",1) 
        cmds.setAttr ("defaultRenderGlobals.putFrameBeforeExt",1)       
    if (my_fae == 5): # the user wants name_#.ext
        cmds.setAttr ("defaultRenderGlobals.outFormatControl",2)
        cmds.setAttr ("defaultRenderGlobals.periodInExt",2)
        cmds.setAttr ("defaultRenderGlobals.outFormatExt",my_file_type,type="string")
        cmds.setAttr ("defaultRenderGlobals.useFrameExt",1) 
        cmds.setAttr ("defaultRenderGlobals.putFrameBeforeExt",1)        
        
        
        
    # Getting the Resolution values
    my_image_h = int(cmds.intFieldGrp('image_h', query = True, value1 = True))        
    cmds.setAttr ("defaultResolution.height",my_image_h)    
    my_image_w = int(cmds.intFieldGrp('image_w', query = True, value1 = True))        
    cmds.setAttr ("defaultResolution.width",my_image_w)
    
    #Getting Camera Type
    my_cam_type = int(cmds.optionMenuGrp('cam_type', query = True, select = True))
    if (my_cam_type == 1): # user wants persp
        cmds.setAttr ("frontShape.renderable",0)          
        cmds.setAttr ("perspShape.renderable",1)
        cmds.setAttr ("sideShape.renderable",0)
        cmds.setAttr ("topShape.renderable",0)
    if (my_cam_type == 2): # user wants nothing
        cmds.setAttr ("frontShape.renderable",0)          
        cmds.setAttr ("perspShape.renderable",0)
        cmds.setAttr ("sideShape.renderable",0)
        cmds.setAttr ("topShape.renderable",0)   
    if (my_cam_type == 3): # user wants front
        cmds.setAttr ("frontShape.renderable",1)          
        cmds.setAttr ("perspShape.renderable",0)
        cmds.setAttr ("sideShape.renderable",0)
        cmds.setAttr ("topShape.renderable",0)   
    if (my_cam_type == 4): # user wants side
        cmds.setAttr ("frontShape.renderable",0)          
        cmds.setAttr ("perspShape.renderable",0)
        cmds.setAttr ("sideShape.renderable",1)
        cmds.setAttr ("topShape.renderable",0)   
    if (my_cam_type == 5): # user wants top
        cmds.setAttr ("frontShape.renderable",0)          
        cmds.setAttr ("perspShape.renderable",0)
        cmds.setAttr ("sideShape.renderable",0)
        cmds.setAttr ("topShape.renderable",1)   
        
        
    # set up progress Window
    cmds.progressWindow ( title='Rendering...',progress=1, status='Rendering...',isInterruptable=True)     
    frTotal = float(endNum - startNum)
        
        
        
    mel.eval('currentTime %s ;'%(startNum))
    while (startNum <= endNum):
       
        mel.eval('renderWindowRender redoPreviousRender renderView;')
        startNum += 1
        mel.eval('currentTime %s ;'%(startNum))
        if cmds.progressWindow (q=True, isCancelled=True):
            break
        prog = (startNum/frTotal) * 100
        cmds.progressWindow(e=True, progress=prog)      
    
    
    print "Finished"
    cmds.progressWindow (endProgress=True)
    return 1
    
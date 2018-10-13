# Hannah Posch - Object Manipulator Window (Spring 2015)
## Code was written to create an easy window with a few of my most used commands when building a scene.
## Instructions: Import code into Maya Script Editor Python tab, select script and press execute. Object Manipulator Window will open. 
## Fill out necessary info for the duplicate, rename, search and replace, and the group objects portions if needed
## and press the buttons to execute that portion's commands.

# Import command library
import maya.cmds as cmds
import maya.OpenMaya as api


# set the default name for the window
winName = 'myWindow'
 
# if the window already exists, delete it
if cmds.window( winName, q=True, exists=True ):
    cmds.deleteUI( winName )
 
# create window
win = cmds.window( winName, title='Object Manipulator Window' )
 
# create layout
col = cmds.columnLayout( adjustableColumn=True )
 
# create controls
cmds.text( label='Duplicate a single selected object' )
cmds.text( label='\n\nSelect object to be duplicated' )

startNum = cmds.intFieldGrp( 'numDup', label='Number of duplicates:', value1= 1 )
startNum2 = cmds.intFieldGrp( 'numtrans', label='Translate:', numberOfFields=3, value1= 0, value2=0, value3=0 )
startNum3 = cmds.intFieldGrp( 'numrotate', label='Rotate:', numberOfFields=3, value1= 0, value2=0, value3=0)
startNum4 = cmds.intFieldGrp( 'numscale', label='Scale:', numberOfFields=3, value1=1, value2=1, value3=1 )

cmds.button( label='Duplicate', command='buttonMethod3()' )

cmds.text( label='Rename selected objects' )
cmds.text( label='\n\nEnter new prefix and start index for new name' )


preText3 = cmds.textFieldGrp( label='Prefix:', text='default' )
preText4 = cmds.textFieldGrp( label='Suffix:', text='none' )
startNum5 = cmds.intFieldGrp( label='Start Index:', value1= 1 )

cmds.button( label='Rename', command='buttonMethod()' )

cmds.text( label='Search and replace object name' )
cmds.text( label='\n\nEnter object name from outliner and new replacement name' )

preText5 = cmds.textFieldGrp( label='Name of object:', text='default' )
preText6 = cmds.textFieldGrp( label='Replacement name:', text='new default name' )

cmds.button( label='Search and replace', command='buttonMethod2()' )

cmds.text( label='Group selected objects' )
cmds.text( label='\n\nSelect objects to be grouped' )

preText7 = cmds.textFieldGrp( label='Name of group:', text='default group name' )

cmds.button( label='Group', command='buttonMethod4()' )
 
# show window
cmds.showWindow( win )


#Create Duplicate Method
def duplicateObjs( numD=1, numTransX=0, numTransY=0, numTransZ=0, numRotX=0, numRotY=0, numRotZ=0, numSclX=0, numSclY=0, numSclZ=0 ):
    
    
    #Main code for duplicating
    
    #Get selected objects
    sel = cmds.ls( sl=True )
    
    #Error checking for one object
    if not sel:
       api.MGlobal.displayError( 'Please select at least one object to duplicate.' )
       return
    if ( len( sel ) >= 2 ) :
       api.MGlobal.displayError( 'Please select only one object to duplicate.' )
       return
       
    #Code to duplicate object
    transX = 0
    transY = 0
    transZ = 0
    rotX = 0
    rotY = 0
    rotZ = 0
    sclX = 0
    sclY = 0
    sclZ = 0
    
    for s in sel:
        cmds.duplicate( s )
        transX = transX + numTransX
        transY = transY + numTransY
        transZ = transZ + numTransZ
        cmds.move( transX, transY, transZ, r=True )
        rotX = rotX + numRotX
        rotY = rotY + numRotY
        rotz = rotZ + numRotZ
        cmds.rotate( rotX, rotY, rotZ, r=True )
        sclX = sclX + numSclX
        sclY = sclY + numSclY
        sclZ = sclZ + numSclZ
        cmds.scale( sclX, sclY, sclZ, r=True )
        
        for d in range( 1, numD ) :
            cmds.duplicate( st=True)
      
#Create Button Method for duplication
def buttonMethod3():
    
    numD = int( cmds.intFieldGrp( 'numDup', query = True, value1 = True ) )
    numTransX = int( cmds.intFieldGrp( 'numtrans', query=True, value1=True ) )
    numTransY = int( cmds.intFieldGrp( 'numtrans', query=True, value2=True ) )   
    numTransZ = int( cmds.intFieldGrp( 'numtrans', query=True, value3=True ) )
    numRotX = int( cmds.intFieldGrp( 'numrotate', query=True, value1=True ) )
    numRotY = int( cmds.intFieldGrp( 'numrotate', query=True, value2=True ) )
    numRotZ = int( cmds.intFieldGrp( 'numrotate', query=True, value3=True ) )
    numSclX = int( cmds.intFieldGrp( 'numscale', query=True, value1=True ) )
    numSclY = int( cmds.intFieldGrp( 'numscale', query=True, value2=True ) )
    numSclZ = int( cmds.intFieldGrp( 'numscale', query=True, value3=True ) )
   
    
    duplicateObjs( numD, numTransX, numTransY, numTransZ, numRotX, numRotY, numRotZ, numSclX, numSclY, numSclZ )

#Create Rename Method
def renameObjs( prefix='default', suffix='none', num=1 ):

    
    # Main code for renaming
    
    # Create new name
    newName = prefix + '_' + suffix + '_' + str( num )
    
    # Get selected objects
    sel = cmds.ls( sl=True )
    
    #Error Checking
    if not sel:
       api.MGlobal.displayError( 'Please select at least one object.' )
       return
    
    # Check to see if object name exists and rename
 
    for s in sel:
        print s
        while cmds.objExists( newName ):
            num += 1
            newName = prefix + '_' + suffix + '_' + str(num)
        print 'Renaming'
        print 'Object Renamed' + ' ' + newName
        if ( suffix != 'none' ):
            newName = prefix + '_' + suffix + '_' + str(num)
        else:    
            newName = prefix + '_' + str( num )
        cmds.rename( s, newName )
        api.MGlobal.displayInfo( 'Object renamed value of' + ' ' + newName )

#Create Button Method for renaming
def buttonMethod():
        
    name = cmds.textFieldGrp( preText3, q=True, text=True )
    secondname = cmds.textFieldGrp( preText4, q=True, text=True)
    int = cmds.intFieldGrp( startNum5, q=True, value1=True )

    renameObjs( prefix=name, suffix=secondname, num=int )
    
#Create Search Method
def searchObjs ( searchName='default', newreplaceName='new default name' ):
    
    #Main code for searching
    #Select an object if it exists
    #Print a warning if it doesn't exist.
    if cmds.objExists( searchName ):
      cmds.select( searchName )
      cmds.rename( searchName, newreplaceName )
      api.MGlobal.displayInfo( 'Object renamed value of' + ' ' + newreplaceName )
      
    else:
      api.MGlobal.displayError( 'Object does not exist.' )
      return



#Create Button Method for searching
def buttonMethod2():
    
    searchName = cmds.textFieldGrp( preText5, q=True, text=True )
    newreplaceName = cmds.textFieldGrp( preText6, q=True, text=True )
    
    searchObjs ( searchName, newreplaceName )
    
#Create Group Method
def groupObjs( defaultGrpName='default group name' ):

    #Main code for grouping
    
    #Get selected objects
    sel = cmds.ls( sl=True )
    
    #Error Checking
    if not sel:
       api.MGlobal.displayError( 'Please select at least one object.' )
       return
       
    cmds.group( name=defaultGrpName )


#Create button method for grouping  
def buttonMethod4():
    
    grpName = cmds.textFieldGrp( preText7, q=True, text=True)
    
    groupObjs( defaultGrpName=grpName ) 
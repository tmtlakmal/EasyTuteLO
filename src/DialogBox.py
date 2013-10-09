'''
Created on Sep 28, 2013

@author: lakmal
'''
#from com.sun.star.awt import Rectangle
#from com.sun.star.awt import WindowDescriptor
import uno 
#from com.sun.star.awt.WindowClass import MODALTOP
#from com.sun.star.awt.VclWindowPeerAttribute import OK, OK_CANCEL, YES_NO, YES_NO_CANCEL, RETRY_CANCEL, DEF_OK, DEF_CANCEL, DEF_RETRY, DEF_YES, DEF_NO
import DocumentHandler as dh 

def TestDialogs():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    doc = desktop.getCurrentComponent()
    if not hasattr(doc, "Text"):
        doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )  
    oDialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel",ctx)
    print(oDialogModel)
    oDialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog",ctx)
    oDialog.setModel(oDialogModel)
    oDialogControl = oDialog.getControls()
    sPropNames = ['Height','Moveable','Name','PositionX','PositionY','Step','TabIndex','Title','Width']
    #sValues = [uno.Any('Numeric',380),uno.Any('bool',True),uno.Any("MyTestDialog"),uno.Any(102),41,0,0,'OpenOffice',250]
    #oDialogModel.setPropertyValues(sPropNames,sValues)
    oDialogModel.Height = 100
    oDialogModel.Moveable = True
    oDialogModel.Name="MyTestDialog"
    oDialogModel.PositionX = 102
    oDialogModel.PositionY = 41
    oDialogModel.Step = 0
    oDialogModel.TabIndex= 0
    oDialogModel.Title = "Select The Formula Resources"
    oDialogModel.Width =250
    oButtonModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlButtonModel",ctx)
    #oUnoControlModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogElement",ctx)
    #parentWin = oDialogModel.CurrentController.Frame.ContainerWindow
    
    createCheckBox(ctx,oDialogModel)
    #oDialogModel.insertByName("CheckBox2",addCheckBox(ctx,"formula2",0))
    oDialog.setVisible(False)
    oToolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
    oDialog.createPeer(oToolkit,oToolkit.getDesktopWindow())
    print(oDialog.execute())
    print(oDialogControl)
    

def TestLayout():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    doc = desktop.getCurrentComponent()
    if not hasattr(doc, "Text"):
        doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )   
    contFrame =doc.getCurrentController().getFrame()
    loutmgr=contFrame.LayoutManager
    a = desktop.getComponents()
    b = a.createEnumeration()
    while b.hasMoreElements(): 
        element = b.nextElement()
        try:
            for prop in element.getPropertySetInfo().getProperties():
                print(prop)
        except Exception :
            print("exempted")
    print(contFrame.getName())
    a1 = contFrame.getContainerWindow()
    print(a1)
    #loutmgr.doLayout()
    #elems = loutmgr.getElements()   
    #for e in elems:  
    #    print(e.getPropertyValue("ResourceURL")) 
    #uiconfmgr = doc.getUIConfigurationManager()
    #wstconf = smgr.createInstanceWithContext( "com.sun.star.ui.WindowStateConfiguration",ctx)
    #print(wstconf)
    #wndw =loutmgr.getDockingAreaAcceptor().getContainerWindow()
    #for a in wndw.getProperties():
    #    print(a)
    uiEl = uno.createUnoStruct("com.sun.star.ui.XUIElement")
    uiEl.Frame = contFrame
    uiEl.ResourceURL = "private:resource/dockingwindow/testdockwindow"
    uiEl.Type =7
    #print(uiEl)
    point = uno.createUnoStruct( "com.sun.star.awt.Point")
    point.X=50
    point.Y=50
    dockingArea = uno.Enum("com.sun.star.ui.DockingArea","DOCKINGAREA_RIGHT")
    loutmgr.dockWindow("private:resource/dockingwindow/testdockwindow",dockingArea,point)

def createWindow(ctx,parentWin,height,width,positionX,positionY,serviceName):
    smgr = ctx.ServiceManager
    Rectangle =uno.createUnoStruct("com.sun.star.awt.Rectangle")
    Rectangle.Width =width
    Rectangle.Height=height
    Rectangle.X=positionX
    Rectangle.Y=positionY
    WindowDescriptor = uno.createUnoStruct("com.sun.star.awt.WindowDescriptor") 
    WindowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP")
    aDescriptor = WindowDescriptor
    aDescriptor.Type = WindowClass
    aDescriptor.WindowServiceName = serviceName
    aDescriptor.ParentIndex = -1
    aDescriptor.Parent = parentWin
    aDescriptor.Bounds = Rectangle
    tk = aDescriptor.Parent.getToolkit()
    return tk.createWindow(aDescriptor)

def createCheckBox(ctx,oDialogModel):
    smgr = ctx.ServiceManager
    oCheckBoxModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlCheckBoxModel")
    oDialogModel.insertByName("CheckBox1",oCheckBoxModel)
    oCheckBoxModel.Height =10
    oCheckBoxModel.Width =50
    oCheckBoxModel.PositionX =50
    oCheckBoxModel.PositionY =50
    oCheckBoxModel.Label ="Formula1"

def addCheckBox(ctx,parentwin,height,width,positionX,positionY,serviceName,label,state):
    smgr = ctx.ServiceManager
    
    oCheckBoxModel = createWindow(ctx,parentwin,height,width,positionX,positionY,serviceName)
    oCheckBoxModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlCheckBoxModel",ctx)
    oCheckBoxModel.setPropertyValue("Label", label)
    #oCheckBoxModel.setPropertyValue("PositionX", positionX)
    #oCheckBoxModel.setPropertyValues("PositionY", positionY)
    oCheckBoxModel.setPropertyValue("State", state)
    return oCheckBoxModel


def createListBox(ctx,width,height,x,y):
    smgr = ctx.ServiceManager
    Rectangle=uno.createUnoStruct("com.sun.star.awt.Rectangle")
    Rectangle.Width =width
    Rectangle.Height=height
    Rectangle.X=x
    Rectangle.Y=y
    WindowDescriptor = uno.createUnoStruct("com.sun.star.awt.WindowDescriptor") 
    WindowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP") 
    VclWindowPeerAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK")
    
def TestMessageBox():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    Rectangle =uno.createUnoStruct("com.sun.star.awt.Rectangle")
    Rectangle.Width =100
    Rectangle.Height=100
    Rectangle.X=0
    Rectangle.Y=300
    WindowDescriptor = uno.createUnoStruct("com.sun.star.awt.WindowDescriptor") 
    WindowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP")      
    print(WindowClass)
    VclWindowPeerAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK")
    print(VclWindowPeerAttribute)
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    doc = desktop.getCurrentComponent()
    if not hasattr(doc, "Text"):
        doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )    
    parentwin = doc.CurrentController.Frame.ContainerWindow
 
    s = "This is a test"
    t = "Test"
    # res = MessageBox(parentwin, s, t, "querybox", VclWindowPeerAttribute.YES_NO_CANCEL + VclWindowPeerAttribute.DEF_NO)
 
    #s = res
    MsgType = "messbox".lower()
 
    #available msg types
    MsgTypes = ("messbox", "infobox", "errorbox", "warningbox", "querybox")
 
    if not ( MsgType in MsgTypes ):
        MsgType = "messbox"
    print(WindowClass)
    #describe window properties.
    aDescriptor = WindowDescriptor
    aDescriptor.Type = WindowClass
    aDescriptor.WindowServiceName = "listbox"
    aDescriptor.ParentIndex = -1
    aDescriptor.Parent = parentwin
    aDescriptor.Bounds = Rectangle
    aDescriptor.WindowAttributes=uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.YES_NO_CANCEL")
#     aDescriptor.WindowAttributes= 1
    tk = aDescriptor.Parent.getToolkit()
    #msgbox.execute()
    lstbox = tk.createWindow(aDescriptor)
    lstbox.addItem("added",0)
    lstbox.addItem("added",1)
    lstbox.makeVisible(1)
    print(lstbox)
    lstbox.Visible=True
    lstbox.setProperty('Dropdown',True)
    lstbox.setProperty('Focus',True)
    lstbox.setProperty('Enabled',True)
    #lstbox.invalidate(16384)
    a=lstbox.getProperties()
    for b in a:
        print(b)
    listbox = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlListBoxModel",ctx)
    #lsPropSet = listbox.createInstance("com.sun.star.beans.XMultiPropertySet")
    #listbox.Enable=True;
    print(lstbox.hasFocus())
    print(lstbox.getOutputSize())
    itemList = uno.createUnoStruct("com.sun.star.awt.XItemList")
    print(itemList)
    #listbox.insertItem=(1,'red','')
    items=[]
    items.append("item1")
    items.append("item2")
    print(listbox.StringItemList)
    listbox.StringItemList = uno.ByteSequence("item1item2")
    print(listbox.StringItemList)

    #msgbox.setMessageText(s)
    #if t :
    #    msgbox.setCaptionText(t)
 
#    return msgbox.execute()
 
# Show a message box with the UNO based toolkit

#TestMessageBox()
TestDialogs()
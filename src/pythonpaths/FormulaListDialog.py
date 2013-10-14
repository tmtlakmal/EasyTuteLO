'''
Created on Oct 7, 2013

@author: lakmal
'''

import uno,wap,unohelper
from com.sun.star.awt import XActionListener
from PIL import Image
import FileHandler as fh

class MyActionListener( unohelper.Base, XActionListener ):
    def __init__(self, eventObject):
        self.eventObject = eventObject                          #save the parent dialog of the button object
       
    def actionPerformed(self, actionEvent):
        oControl = actionEvent.Source                           #get the name of the object which created the event
        name = oControl.getModel().getPropertyValue("Name")     
        if(name=="SelectFormulaButton"):                        #if the event is from the select formula button
            query = self.eventObject.getControl("selectFormulaList").getSelectedItem()
            query = query.split("\n")[0]                        #get the formula selected                           
            txtList = FormulaListDialog().textDetailsAboutFormula(query)
                                                                #get the text details related to the formula
            imgList = FormulaListDialog().imageDetailsAboutFormula(query)
                                                                #get the image details related to the formula
            if not (txtList[0][0]=="N"):                        #if an exception is not thrown
                oDialog = FormulaListDialog().createAvailableResourcesDialog(query,txtList, imgList)
                oDialog.execute()                               #execute the available resources dialog
                self.eventObject.endExecute()                   #finish the dialog
        elif(name=="GetResourcesButton"):                       #if the event is created by the get resources button
            count=1                                             
            selectedItems=[]                                    #initially the selected items is null
            selectedImages=[]                                   #initially the selected images list is null
            query = self.eventObject.getControl("formulaLabel").getModel().getPropertyValue("Label")
                                                                #retrieve the query name from the parent dialog
            while (True):                                       #loop until the checkboxes are finished
                control =self.eventObject.getControl("text"+`count`)
                if(control==None):                              #if no check box is found break
                    break
                if(control.getState()==1):                      #if a selected checkbox is found append as true
                    selectedItems.append(True)
                else:
                    selectedItems.append(False)                 #if a non selected check box is found append as false
                count+=1
            count=0
            while (True):                                       #do the same thing for image check boxes
                control =self.eventObject.getControl("image"+`count`)
                if(control==None):
                    break
                if(control.getState()==1):
                    selectedImages.append(True)
                else:
                    selectedImages.append(False)                
                count+=1  
            fh.FileHandler().addDetailsFileData(query, selectedItems, selectedImages)  
                                                                #add details to the file
            self.eventObject.endExecute()                       #finish executing the dialog
            
    
                    
class FormulaListDialog():
    
    def actionpppp(self,event):
        print(event.source)
    
    def createWaitingMessageBox(self):
        #localContext = uno.getComponentContext()
        #resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        #ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        ctx=uno.getComponentContext()
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()                     #get the current active document 
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        parentwin = doc.CurrentController.Frame.ContainerWindow
        vclAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK") 
        windowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP") 
        rectangle = self.createRectangle(50, 100, 300, 200)     #create dialog rectangle
        windowService ="messbox"                                #type of the dialog
        msgbox = self.createMessageBox(ctx, smgr,windowClass, parentwin, rectangle, windowService, vclAttribute)
                                                                #create dialog according to the attributes given
        msgbox.setMessageText("Fetching Data from Wolfram Alpha Math Engine")
        msgbox.setCaptionText("In Progress")                    #set title and message
        return msgbox
    
    def createSelectTextMessageBox(self):                       #create the select text message box
        #localContext = uno.getComponentContext()
        #resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        #ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        ctx=uno.getComponentContext()
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()                     #get the current active component
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        parentwin = doc.CurrentController.Frame.ContainerWindow
        vclAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK") 
        windowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP") 
        rectangle = self.createRectangle(50, 100, 300, 200)
        windowService ="messbox"
        msgbox = self.createMessageBox(ctx, smgr,windowClass, parentwin, rectangle, windowService, vclAttribute)
        msgbox.setMessageText(" Select A Text and Press Button")
        msgbox.setCaptionText("No Text")
        return msgbox
    
    def createFormulaListDialog(self,formulaList):              #create formula list dialog
        #localContext = uno.getComponentContext()
        #resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        #ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        ctx=uno.getComponentContext()
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()                     #get the active document
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        oDialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog",ctx)      
        oDialogModel = self.createDialog(ctx,smgr,100,True,"DialogFormulaList",100,100,0,0,"Formula List",100)
        self.createDialogButton(oDialogModel, "SelectFormulaButton", 15, 50, 25, 80, "Select Formula")
        self.createListBox(oDialogModel, "selectFormulaList", 60, 80, 10, 10)
                                                                #create the list box to add formulas
        oDialog.setModel(oDialogModel)  
        oDialog.setVisible(False)
        oButton = oDialog.getControl("SelectFormulaButton")
        #oButton.setActionCommand("commanded")
        oButton.addActionListener(MyActionListener(oDialog))
        oToolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        oDialog.createPeer(oToolkit,oToolkit.getDesktopWindow()) 
        self.addFormulasToList(formulaList, oDialog)            #add formulas to list box
        return oDialog
    
    def createAvailableResourcesDialog(self,query,textList,imagesList):
        #localContext = uno.getComponentContext()
        #resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        #ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        ctx=uno.getComponentContext()
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        oDialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog",ctx)      
        oDialogModel = self.createDialog(ctx,smgr,120,True,"DialogResourceList",100,100,0,0,"Resource List",200)        
        self.createLabel(oDialogModel, "formulaLabel", query, 10, 100, 5, 5)  
        oDialog.setVisible(False)
        self.createDialogButton(oDialogModel, "GetResourcesButton", 15, 50, 25, 100, "Get Resources")
        txtEnd = self.addTextCheckBoxesToDialog(textList, oDialogModel)                 #get the end of the text
        imgEnd = self.addImageTextBoxesToDialog(query,txtEnd,imagesList, oDialogModel)  #get the end of the images
        oDialogModel.Width =imgEnd                                          #set the dialog width
        oDialogModel.Height = max(100,txtEnd+25)                            #set the dialog height
        oDialog.setModel(oDialogModel)
        oButton1 = oDialog.getControl("GetResourcesButton")
        oButton1.getModel().PositionY = txtEnd+5                            #reposition the button
        oButton1.setActionCommand("commanded")
        oButton1.addActionListener(MyActionListener(oDialog))
        oToolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        oDialog.createPeer(oToolkit,oToolkit.getDesktopWindow()) 
        return oDialog     
    
    def createDialog(self,ctx,smgr,height,moveable,name,posX,posY,step,tabIndex,title,width):
        #smgr=ctx.ServiceManger                                     #set attributes of the dialog
        oDialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel",ctx)
        oDialogModel.Height = height
        oDialogModel.Moveable = moveable
        oDialogModel.Name=name
        oDialogModel.PositionX = posX
        oDialogModel.PositionY = posY
        oDialogModel.Step = step
        oDialogModel.TabIndex= tabIndex
        oDialogModel.Title = title
        oDialogModel.Width = width
        return oDialogModel
    
    def createMessageBox(self,ctx,smgr,windowClass,parentwin,rectangle,windowService,vclAttribute):
                                                                    #set the attributes of the messagebox
        aDescriptor = uno.createUnoStruct("com.sun.star.awt.WindowDescriptor")        
        #       aDescriptor = WindowDescriptor
        aDescriptor.Type = windowClass
        aDescriptor.WindowServiceName = windowService
        aDescriptor.ParentIndex = -1
        aDescriptor.Parent = parentwin
        aDescriptor.Bounds = rectangle
        aDescriptor.WindowAttributes=vclAttribute
        tk = aDescriptor.Parent.getToolkit()
        msgbox = tk.createWindow(aDescriptor)
        return msgbox
        
    def createRectangle(self,height,width,xPos,yPos):               #create a rectangle according to the parameters
        Rectangle =uno.createUnoStruct("com.sun.star.awt.Rectangle")
        Rectangle.Width =width
        Rectangle.Height=height
        Rectangle.X=xPos
        Rectangle.Y=yPos
        return Rectangle
           
    def createDialogButton(self,oDialogModel,buttonName,height,width,posX,posY,label):
                                                                    #create dialog button according to the given parameters
        #oButton = oDialogModel.createInstance("com.sun.star.awt.UnoControlButton")   
        oButtonModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
        #oButton.setModel(oButtonModel)
        oDialogModel.insertByName(buttonName,oButtonModel)
        oButtonModel.Name =buttonName
        oButtonModel.Height =height
        oButtonModel.Width =width
        oButtonModel.PositionX =posX
        oButtonModel.PositionY =posY
        oButtonModel.Label =label
        
    def createListBox(self,oDialogModel,listBoxName,height,width,posX,posY): 
                                                                    #create a list box according to the given parameters   
        oListBoxModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
        oDialogModel.insertByName(listBoxName,oListBoxModel)
        oListBoxModel.Height =height
        oListBoxModel.Width =width
        oListBoxModel.PositionX =posX
        oListBoxModel.PositionY =posY
    
    def createCheckBox(self,oDialogModel,checkBoxName,label,height,width,posX,posY):    
                                                                    #create the checkbox according to the parameters
        oCheckBoxModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlCheckBoxModel")
        oDialogModel.insertByName(checkBoxName,oCheckBoxModel)
        oCheckBoxModel.Height =height
        oCheckBoxModel.Width =width
        oCheckBoxModel.PositionX =posX
        oCheckBoxModel.PositionY =posY
        oCheckBoxModel.Name = checkBoxName
        oCheckBoxModel.Label = label
        
    def createLabel(self,oDialogModel,labelName,label,height,width,posX,posY): 
                                                                    #create the label according to the given parameters   
        oFixedTextModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        oDialogModel.insertByName(labelName,oFixedTextModel)
        oFixedTextModel.Height =height
        oFixedTextModel.Width =width
        oFixedTextModel.PositionX =posX
        oFixedTextModel.PositionY =posY
        oFixedTextModel.Name = labelName
        oFixedTextModel.Label = label
    
    def addFormulasToList(self,formulaList,oDialog):                #add formulas to the formula list list box
        listBox = oDialog.getControl("selectFormulaList")
        count =len(formulaList)
        for formula in formulaList:
            print(formula)
            listBox.addItem(formula,count)
            count+=1
    
    def addTextCheckBoxesToDialog(self,textList,oDialogModel):
        y=15                                                        #add pain text checkboxes to the dialog
        x=5
        count=1
        for txt in textList:
            name = "text"+`count`
            print(name)
            self.createCheckBox(oDialogModel,name , txt, 10, 100, x, y)
            y+=15
            count+=1
        return y
            
    def addImageTextBoxesToDialog(self,query,txtEnd,imageList,oDialogModel):
        y=15                                                        #add image checkboxes to the dialog
        count=1
        x=105
        for img in imageList:
            print(img)
            imageFilePath = fh.FileHandler().createImageFilePathForTheQuery(query, img)
            imageURL = "file:///"+imageFilePath
            thmbFilePath=fh.FileHandler().createThumbImageFilePathForTheQuery(query, img)
            thumbImageURL = "file:///"+thmbFilePath
            print(imageURL)
            im = Image.open(imageFilePath)
            dim =150
            size=(dim,dim)                                          #create thumbnails
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(thmbFilePath)
            imtb = Image.open(thmbFilePath)
            self.createCheckBox(oDialogModel,img , img, 150, 75, x, y)
            self.setCheckBoxImageURL(oDialogModel, img, thumbImageURL)
            x+=80
            count+=1   
        return x
    
    
    def setCheckBoxImageURL(self,oDialogModel,name,imageURL):       #set the imageurl to a checkbox
        imgChkBox = oDialogModel.getByName(name)
        imgChkBox.ImageURL = imageURL
        
           
    def textDetailsAboutFormula(self,query):                        #get the formual text details from file
        fileName = fh.FileHandler().createFilePathForTheQuery(query)
        try:
            f = open(fileName, 'r') 
            resArray =f.readlines()
            res = ''.join(resArray)
            f.close()
            textList=[]
            waeqr = wap.WolframAlphaQueryResult(res)                #get from titles
            for pod in waeqr.Pods():
                podObject = wap.Pod(pod)
                for subPod in podObject.Subpods():
                    subPodObject = wap.Subpod(subPod)
                    if(subPodObject.Plaintext()!=[[]]):
                        title = subPodObject.Title()
                        if(title[0]!=''):
                            textList.append(title[0])
                        else:
                            textList.append(podObject.Title()[0])
            return textList
        except Exception:
            textList=["No Text Found"]
            print("exeption thrown")
            return textList       
    
    
    
    def imageDetailsAboutFormula(self,query):                       #get the formula image details from file
        fileName = fh.FileHandler().createFilePathForTheQuery(query)
        try:
            f = open(fileName, 'r') 
            resArray =f.readlines()
            res = ''.join(resArray)
            f.close()
            imageList=[]
            waeqr = wap.WolframAlphaQueryResult(res)                #get from images
            count = 0
            for pod in waeqr.Pods():
                podObject = wap.Pod(pod)
                for subPod in podObject.Subpods():
                    subPodObject = wap.Subpod(subPod)
                    if(subPodObject.Img()!=[[]]):
                        imageList.append("image"+`count`)
                        count +=1
            return imageList
        except Exception:
            imageList=["No Text Found"]
            print("exeption thrown")
            return imageList 
        
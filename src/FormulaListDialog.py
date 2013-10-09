'''
Created on Oct 7, 2013

@author: lakmal
'''
import uno
from com.sun.star.awt import XActionListener
from PIL import Image
import unohelper
import os ,wap
import DocumentHandler as dh
import WolframParser as wp

class MyActionListener( unohelper.Base, XActionListener ):
    def __init__(self, eventObject):
        self.eventObject = eventObject
       
    def actionPerformed(self, actionEvent):
        oControl = actionEvent.Source
        #oControl.disable()
        name = oControl.getModel().getPropertyValue("Name")
        print(name)
        if(name=="SelectFormulaButton"):
            query = self.eventObject.getControl("selectFormulaList").getSelectedItem()
            newList=[] 
            txtList = FormulaListDialog().textDetailsAboutFormula(query)
            if not (txtList[0][0]=="N"):  
                for t in txtList:
                    newList.append(t[0])
                oDialog = FormulaListDialog().createAvailableResourcesDialog(query,newList, [])
                oDialog.execute()
                self.eventObject.endExecute()        
        elif(name=="GetResourcesButton"):
            count=1
            selectedItems=[]
            selectedImages=[]
            query = self.eventObject.getControl("formulaLabel").getModel().getPropertyValue("Label")
            print("this is label"+query)
            while (True):
                control =self.eventObject.getControl("text"+`count`)
                if(control==None):
                    break
                if(control.getState()==1):
                    selectedItems.append(True)
                else:
                    selectedItems.append(False)                
                count+=1
            count=0
            while (True):
                print("hh")
                control =self.eventObject.getControl("image"+`count`)
                if(control==None):
                    break
                if(control.getState()==1):
                    selectedImages.append(True)
                else:
                    selectedImages.append(False)                
                count+=1  
            f = open('details.txt','w')
            f.write(query+"\n")
            f.close()
            f = open('details.txt','a')
            for s in selectedItems:
                if(s):
                    f.write("True\n")
                else: 
                    f.write("False\n") 
            f.close() 
            f = open('images.txt','w')
            f.write(query+"\n")
            f.close()
            f = open('images.txt','a')
            for s in selectedImages:
                if(s):
                    f.write("True\n")
                else: 
                    f.write("False\n") 
            f.close()   
            self.eventObject.endExecute()
            #self.addresources(query, selectedItems)
            
    
                    
class FormulaListDialog():
    
    def actionpppp(self,event):
        print(event.source)
    
    def createWaitingMessageBox(self):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        parentwin = doc.CurrentController.Frame.ContainerWindow
        #vclAttribute=uno.getConstantByName("com.sun.star.awt.WindowAttribute.CLO") 
        vclAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK") 
        windowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP") 
        rectangle = self.createRectangle(50, 100, 300, 200)
        windowService ="messbox"
        msgbox = self.createMessageBox(ctx, smgr,windowClass, parentwin, rectangle, windowService, vclAttribute)
        msgbox.setMessageText("Fetching Data from Wolfram Alpha Math Engine")
        msgbox.setCaptionText("In Progress")
        return msgbox
    
    def createSelectTextMessageBox(self):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        parentwin = doc.CurrentController.Frame.ContainerWindow
        #vclAttribute=uno.getConstantByName("com.sun.star.awt.WindowAttribute.CLO") 
        vclAttribute = uno.getConstantByName("com.sun.star.awt.VclWindowPeerAttribute.OK") 
        windowClass = uno.Enum("com.sun.star.awt.WindowClass","MODALTOP") 
        rectangle = self.createRectangle(50, 100, 300, 200)
        windowService ="messbox"
        msgbox = self.createMessageBox(ctx, smgr,windowClass, parentwin, rectangle, windowService, vclAttribute)
        msgbox.setMessageText(" Select A Text and Press Button")
        msgbox.setCaptionText("No Text")
        return msgbox
    
    def createFormulaListDialog(self,formulaList):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        oDialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog",ctx)      
        oDialogModel = self.createDialog(ctx,smgr,100,True,"DialogFormulaList",100,100,0,0,"Formula List",100)
        self.createDialogButton(oDialogModel, "SelectFormulaButton", 15, 50, 25, 80, "Select Formula")
        self.createListBox(oDialogModel, "selectFormulaList", 60, 80, 10, 10)
        oDialog.setModel(oDialogModel)  
        oDialog.setVisible(False)
        oButton = oDialog.getControl("SelectFormulaButton")
        #oButton.setActionCommand("commanded")
        oButton.addActionListener(MyActionListener(oDialog))
        oToolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        oDialog.createPeer(oToolkit,oToolkit.getDesktopWindow()) 
        self.addFormulasToList(formulaList, oDialog) 
        return oDialog
    
    def createAvailableResourcesDialog(self,query,textList,imagesList):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        oDialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog",ctx)      
        oDialogModel = self.createDialog(ctx,smgr,300,True,"DialogResourceList",100,100,0,0,"Resource List",200)        
        self.createLabel(oDialogModel, "formulaLabel", query, 10, 100, 5, 5)  
        oDialog.setVisible(False)
        txtEnd = self.addTextCheckBoxesToDialog(textList, oDialogModel) 
        imgEnd = self.addImageTextBoxesToDialog(query,txtEnd,imagesList, oDialogModel)
        oDialogModel.Width =max([imgEnd,txtEnd])
        self.createDialogButton(oDialogModel, "GetResourcesButton", 15, 50, 25, 220, "Get Resources")
        self.createDialogButton(oDialogModel, "BackToFormulaButton", 15, 50, 100, 220, "Back")
        oDialog.setModel(oDialogModel)
        oButton1 = oDialog.getControl("GetResourcesButton")
        oButton1.setActionCommand("commanded")
        oButton1.addActionListener(MyActionListener(oDialog))
        oButton2 = oDialog.getControl("BackToFormulaButton")
        oButton2.addActionListener(MyActionListener(oDialog))
        oToolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        oDialog.createPeer(oToolkit,oToolkit.getDesktopWindow()) 
        return oDialog     
    
    def createDialog(self,ctx,smgr,height,moveable,name,posX,posY,step,tabIndex,title,width):
        #smgr=ctx.ServiceManger 
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
        
    def createRectangle(self,height,width,xPos,yPos):
        Rectangle =uno.createUnoStruct("com.sun.star.awt.Rectangle")
        Rectangle.Width =width
        Rectangle.Height=height
        Rectangle.X=xPos
        Rectangle.Y=yPos
        return Rectangle
           
    def createDialogButton(self,oDialogModel,buttonName,height,width,posX,posY,label):
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
        oListBoxModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
        oDialogModel.insertByName(listBoxName,oListBoxModel)
        oListBoxModel.Height =height
        oListBoxModel.Width =width
        oListBoxModel.PositionX =posX
        oListBoxModel.PositionY =posY
    
    def createCheckBox(self,oDialogModel,checkBoxName,label,height,width,posX,posY):    
        oCheckBoxModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlCheckBoxModel")
        oDialogModel.insertByName(checkBoxName,oCheckBoxModel)
        oCheckBoxModel.Height =height
        oCheckBoxModel.Width =width
        oCheckBoxModel.PositionX =posX
        oCheckBoxModel.PositionY =posY
        oCheckBoxModel.Name = checkBoxName
        oCheckBoxModel.Label = label
        
    def createLabel(self,oDialogModel,labelName,label,height,width,posX,posY):    
        oFixedTextModel = oDialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
        oDialogModel.insertByName(labelName,oFixedTextModel)
        oFixedTextModel.Height =height
        oFixedTextModel.Width =width
        oFixedTextModel.PositionX =posX
        oFixedTextModel.PositionY =posY
        oFixedTextModel.Name = labelName
        oFixedTextModel.Label = label
    
    def addFormulasToList(self,formulaList,oDialog):
        listBox = oDialog.getControl("selectFormulaList")
        count =len(formulaList)
        for formula in formulaList:
            print(formula)
            listBox.addItem(formula,count)
            count+=1
    
    def addTextCheckBoxesToDialog(self,textList,oDialogModel):
        y=15
        x=5
        count=1
        for txt in textList:
            name = "text"+`count`
            print(name)
            self.createCheckBox(oDialogModel,name , txt, 10, 75, x, y)
            x+=80
            count+=1
        return x
            
    def addImageTextBoxesToDialog(self,query,txtEnd,imageList,oDialogModel):
        y=80
        count=1
        x=5
        for img in imageList:
            print(img)
            imageFilePath = os.sys.path[0]+"/equationFiles/"+query+img+".gif"
            imageURL = "file:///"+imageFilePath
            thmbFilePath=os.sys.path[0]+"/equationFiles/"+query+img+"thumb.gif"
            thumbImageURL = "file:///"+thmbFilePath
            print(imageURL)
            im = Image.open(imageFilePath)
            dim =150
            size=(dim,dim)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(thmbFilePath)
            imtb = Image.open(thmbFilePath)
            height = imtb.size[1]
            print(y)
            self.createCheckBox(oDialogModel,img , img, 150, 75, x, y)
            self.setCheckBoxImageURL(oDialogModel, img, thumbImageURL)
            print(y)
            print(y)
            x+=80
            count+=1   
        return x
    
    
    def setCheckBoxImageURL(self,oDialogModel,name,imageURL):
        imgChkBox = oDialogModel.getByName(name)
        imgChkBox.ImageURL = imageURL
        
           
    def textDetailsAboutFormula(self,query):
        fileName = os.sys.path[0]+"/equationFiles/"+query.lower()+".txt"
        try:
            f = open(fileName, 'r') 
            resArray =f.readlines()
            res = ''.join(resArray)
            f.close()
            textList=[]
            waeqr = wap.WolframAlphaQueryResult(res)
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
    
    def imageDetailsAboutFormula(self,query):
        fileName = os.sys.path[0]+"/equationFiles/"+query.lower()+".txt"
        try:
            f = open(fileName, 'r') 
            resArray =f.readlines()
            res = ''.join(resArray)
            f.close()
            imageList=[]
            waeqr = wap.WolframAlphaQueryResult(res)
            count = 0
            for pod in waeqr.Pods():
                podObject = wap.Pod(pod)
                for subPod in podObject.Subpods():
                    subPodObject = wap.Subpod(subPod)
                    if(subPodObject.Img()!=[[]]):
                        image = subPodObject.Img()
                        imageList.append("image"+`count`)
                        count +=1
            return imageList
        except Exception:
            imageList=["No Text Found"]
            print("exeption thrown")
            return imageList      
#formulaList=["int x dx"]         
#a= FormulaListDialog().createFormulaListDialog(formulaList) 
#a.execute()       
a =FormulaListDialog().imageDetailsAboutFormula("int x dx")  
for b in a:
    print(b)
        
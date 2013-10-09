'''
Created on Sep 12, 2013

@author: lakmal
'''
import sys

##Load our rdflib files if the user already has a
#local copy of rdflib installed
#bundle_path = None
#for part in sys.path:
#    if part.count("uno_packages") and part.count("cache") and part.\
#      count("pythonpath"):
#        bundle_path = part
#        break
#if bundle_path:
#    sys.path.insert(1, bundle_path)
import urllib
import threading
import wap
from pythonpaths import Communicator as com
from pythonpaths import WolframParser as wp
from pythonpaths import DocumentHandler as dh
import os
import uno
import unohelper
from com.sun.star.frame import XDispatch, XDispatchProvider
from com.sun.star.lang import XInitialization, XServiceInfo
from com.sun.star.task import XJob
import FormulaListDialog as flD
from com.sun.star.awt import XActionListener
from com.sun.star.awt import XMouseListener

implementation_name = "org.libreoffice.EasyTuteLO.TutorialBuilder" # as defined in Factory.xcu
implementation_services = ("org.libreoffice.EasyTuteLO.TutorialBuilder",)



            
class MyMouseListener(unohelper.Base,XMouseListener): 
    def mousePressed(self,mouseEvent):
        oControl = mouseEvent.Source()
        print(oControl)       
        

class TutorialBuilder(unohelper.Base, XInitialization, XServiceInfo,
              XDispatchProvider, XDispatch, XJob):
    
    
        
    def getNewString(self, theString ) :
        if not theString or len(theString) ==0 :
            return ""
        # should we tokenize on "."?
        if theString[0].isupper() and len(theString)>=2 and theString[1].isupper() :
        # first two chars are UC => first UC, rest LC
            newString=theString.capitalize();
        elif theString[0].isupper():
        # first char UC => all to LC
            newString=theString.lower()
        else: # all to UC.
            newString=theString.upper()
        return newString;
    
    def getSelectedText(self,xModel ): 
        xSelectionSupplier = xModel.getCurrentController()
     
        #see section 7.5.1 of developers' guide
        xIndexAccess = xSelectionSupplier.getSelection()
        count = xIndexAccess.getCount();
        #xTextRange = xIndexAccess.getByIndex(count);
        #theString = xTextRange.getString();
        for i in range(count) :
            xTextRange = xIndexAccess.getByIndex(i);
            theString = xTextRange.getString();    
        return theString
    
    def addFormulasToStorage(self,query):
        fileName = os.sys.path[0]+"/equationFiles/equationList.txt" 
        with open(fileName, "a") as myfile:
            myfile.write(query.lower()+"\n")

    def readFormulaStorage(self):
        try:
            fileName = os.sys.path[0]+"/equationFiles/equationList.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Formula Storage file"
    
    
    
    def setWaitingMessage(self):
        msgbox =flD.FormulaListDialog().createWaitingMessageBox()
        msgbox.execute()
    
    def selectFormulaButtonClicked(self,oActionEvent):
        print(oActionEvent)
    
    def addFormulaData(self):
        dochand=dh.DocumentHandler()       
        doc=dochand.createWriterDocument()
        text = doc.Text
        cursor = text.createTextCursor()
        query = self.getSelectedText(doc)
        query = query.lower()
        if(query!=""):
            if (self.checkAvailabilityOfFormula(query)):
                fileName = os.sys.path[0]+"/equationFiles/"+query+".txt"                   
                resultReader = wp.WolframMathResultReader(fileName) #read the stored result
                if(resultReader.getExistingTotalResult()):                       #get all the resources related to the result
                    listDialog = flD.FormulaListDialog()
                    textList = listDialog.textDetailsAboutFormula(query)
                    imagesList = listDialog.imageDetailsAboutFormula(query)
                    oDialog =listDialog.createAvailableResourcesDialog(query, textList, imagesList)
                    oDialog.execute() 
                    self.loadRequestedResources(resultReader, dochand, doc,text,cursor)   
            else:
                com.APICommunicator().configureAndGetResult(query)
                fileName = os.sys.path[0]+"/equationFiles/"+query+".txt" 
                resultReader = wp.WolframMathResultReader(fileName)
                if(resultReader.getTotalResult()):
                    self.addFormulasToStorage(query)
                    listDialog = flD.FormulaListDialog()
                    textList = listDialog.textDetailsAboutFormula(query)
                    imagesList = []
                    oDialog =listDialog.createAvailableResourcesDialog(query, textList, imagesList)
                    oDialog.execute()
                
        else:
            oDialog =flD.FormulaListDialog().createSelectTextMessageBox()
            oDialog.execute()
            
    def checkAvailabilityOfFormula(self,query):
        res = self.readFormulaStorage()
        for r in res:
            r = r.split("\n")[0]
            if(r.lower()==query.lower()):
                return True;
        return False   
    
    def readDetailsFile(self):
        try:
            fileName = os.sys.path[0]+"/details.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Details file"
    
    def readImagesFile(self):
        try:
            fileName = os.sys.path[0]+"/images.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Details file"
        
    def loadRequestedResources(self,resultReader,dochand,doc,text,cursor):
        details = self.readDetailsFile()
        print(details[1])
        count=1
        for res in resultReader.plainTexts:                 #add formulas
            print(res)
            if(count==len(details)):
                break
            if(details[count]=="True\n"):
                try:
                    dochand.addFormulaToWriterDocument(doc,cursor,res)
                except Exception:
                    print(res)
            count+=1 
        count=1
        images = self.readImagesFile()    
        for img in resultReader.imageFileNames:             #add images to the document
            if(count==len(images)):
                break
            if(images[count]=="True\n"):
                try:
                    imageUrl = "file:///"+img
                    dochand.addImageToWriterDocument(doc,cursor, imageUrl)
                except Exception:
                    print(res)
            count+=1
        
    
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
                            textList.append(title)
                        else:
                            textList.append(podObject.Title())
            return textList
        except Exception:
            textList=["No Text Found"]
            print("exeption thrown")
            return textList    
                            
   
        
                   
               
                
               
#####################################################      
# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper ()

# add the FormatFactory class to the implementation container,
# which the loader uses to register/instantiate the component.
g_ImplementationHelper.addImplementation (TutorialBuilder,
                    implementation_name,
                    implementation_services,
                    )
TutorialBuilder().addFormulaData()
#print(TutorialBuilder().checkAvailabilityOfFormula("int x*sinx dx"))
#print(urllib.quote("int x dx"))
#TutorialBuilder().textDetailsAboutFormula("int x dx")
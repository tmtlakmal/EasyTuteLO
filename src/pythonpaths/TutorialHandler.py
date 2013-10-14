'''
Created on Sep 12, 2013

@author: lakmal
'''

import FileHandler as fh
import Communicator as com
import WolframParser as wp
import DocumentHandler as dh
import FormulaListDialog as flD
import os
import unohelper

implementation_name = "org.libreoffice.EasyTuteLO.TutorialBuilder" # as defined in Factory.xcu
implementation_services = ("org.libreoffice.EasyTuteLO.TutorialBuilder",)

       

class TutorialHandler(unohelper.Base):
    
    
    def getSelectedText(self,xModel ):                              #get the highlighted text from document
        try: 
            xSelectionSupplier = xModel.getCurrentController()
            xIndexAccess = xSelectionSupplier.getSelection()
            count = xIndexAccess.getCount();
            for i in range(count) :
                xTextRange = xIndexAccess.getByIndex(i);
                theString = xTextRange.getString();    
            return theString
        except Exception:
            oDialog =flD.FormulaListDialog().createSelectTextMessageBox()
            oDialog.execute()
    
    
    def setWaitingMessage(self):                                    #get the waiting message text box and execute
        msgbox =flD.FormulaListDialog().createWaitingMessageBox()
        msgbox.execute()
    
           
    def checkAvailabilityOfFormula(self,query):                     #check the availablility of the given formula
        res = fh.FileHandler().readFormulaStorage()
        for r in res:
            r = r.split("\n")[0]
            if(r.lower()==query.lower()):
                return True;
        return False   
    
        
    def loadRequestedResources(self,resultReader,dochand,doc,text,cursor):
        details = fh.FileHandler().readDetailsFile()                #load the resources according to the request
        print(resultReader.plainTexts)
        count=1
        for res in resultReader.plainTexts:                         #add formulas
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
        images = fh.FileHandler().readImagesFile()    
        for img in resultReader.imageFileNames:                     #add images to the document
            if(count==len(images)):
                break
            if(images[count]=="True\n"):
                try:
                    imageUrl = "file:///"+img
                    dochand.addImageToWriterDocument(doc,cursor, imageUrl)
                except Exception:
                    print(res)
            count+=1
        fh.FileHandler().clearDetailsFile()                         #clear files
        fh.FileHandler().clearImagesFile()
      
         
    def addFormulaData(self):                                       #add formula data main procedure
        dochand=dh.DocumentHandler()       
        doc=dochand.createWriterDocument()
        text = doc.Text
        cursor = text.createTextCursor()
        query = self.getSelectedText(doc)
        query = query.lower()
        if(query!=""):
            if (self.checkAvailabilityOfFormula(query)):
                fileName = fh.FileHandler().createFilePathForTheQuery(query)                 
                resultReader = wp.WolframMathResultReader(fileName) #read the stored result
                if(resultReader.getExistingTotalResult()):          #get all the resources related to the result
                    listDialog = flD.FormulaListDialog()
                    textList = listDialog.textDetailsAboutFormula(query)
                    imagesList = listDialog.imageDetailsAboutFormula(query)
                    oDialog =listDialog.createAvailableResourcesDialog(query, textList, imagesList)
                    oDialog.execute() 
                    res = fh.FileHandler().readDetailsFile()
                    if(len(res)>0):
                        self.loadRequestedResources(resultReader, dochand, doc,text,cursor)   
            else:
                com.APICommunicator().configureAndGetResult(query)  #get a total new result
                fileName = fh.FileHandler().createFilePathForTheQuery(query)
                text.insertString(cursor,os.sys.path[1],0)
                resultReader = wp.WolframMathResultReader(fileName)
                if(resultReader.getTotalResult()):
                    fh.FileHandler().addFormulasToStorage(query)
                    listDialog = flD.FormulaListDialog()
                    textList = listDialog.textDetailsAboutFormula(query)
                    imagesList = listDialog.imageDetailsAboutFormula(query)
                    oDialog =listDialog.createAvailableResourcesDialog(query, textList, imagesList)
                    oDialog.execute()
                    res = fh.FileHandler().readDetailsFile()
                    if(len(res)>0):
                        self.loadRequestedResources(resultReader, dochand, doc,text,cursor)   
    
                
        else:                                                       #if wrong input indicate the message
            oDialog =flD.FormulaListDialog().createSelectTextMessageBox()
            oDialog.execute()
    
    def addPreviousFormulaData(self):                               #add previous formula data
        dochand=dh.DocumentHandler()       
        doc=dochand.createWriterDocument()                          
        text = doc.Text
        cursor = text.createTextCursor()
        formulaList = fh.FileHandler().readFormulaStorage()
        oDialog = flD.FormulaListDialog().createFormulaListDialog(formulaList)
        oDialog.execute()
        res = fh.FileHandler().readDetailsFile()                    #if result is available create resources dialog
        if(len(res)>0):
            query = res[0].split("\n")[0]
            query = query.lower()
            fileName = fh.FileHandler().createFilePathForTheQuery(query)                  
            resultReader = wp.WolframMathResultReader(fileName)
            resultReader.getExistingTotalResult()
            self.loadRequestedResources(resultReader, dochand, doc,text,cursor)
        

TutorialHandler().addFormulaData()                  
               

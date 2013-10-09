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

from pythonpaths import Communicator as com
from pythonpaths import WolframParser as wp
from pythonpaths import DocumentHandler as dh
import os
import unohelper


implementation_name = "org.openoffice.comp.pyuno.demo.HelloWorld" # as defined in Factory.xcu
implementation_services = ("vnd.sun.star.uno-component",)


class TutorialBuilder(unohelper.Base):
    def __init__(self, ctx):
        self.ctx = ctx
        
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
    
    def capitalisePython(self,xModel ): 
        xSelectionSupplier = xModel.getCurrentController()
     
        #see section 7.5.1 of developers' guide
        xIndexAccess = xSelectionSupplier.getSelection()
        count = xIndexAccess.getCount();
        for i in range(count) :
            xTextRange = xIndexAccess.getByIndex(i);
            #print "string: " + xTextRange.getString();
            theString = xTextRange.getString();
            if len(theString)==0 :
                # sadly we can have a selection where nothing is selected
                # in this case we get the XWordCursor and make a selection!
                xText = xTextRange.getText();
                xWordCursor = xText.createTextCursorByRange(xTextRange);
                if not xWordCursor.isStartOfWord():
                    xWordCursor.gotoStartOfWord(False);
                xWordCursor.gotoNextWord(True);
                theString = xWordCursor.getString();
                newString = self.getNewString(theString);
                if newString :
                    xWordCursor.setString(newString);
                    xSelectionSupplier.select(xWordCursor);
            else :
                newString = self.getNewString( theString );
                if newString:
                    xTextRange.setString(newString);
                    xSelectionSupplier.select(xTextRange)
        return theString
    
    def addFormulaData(self):
        dochand=dh.DocumentHandler()       
        doc=dochand.createWriterDocument()
        text = doc.Text
        text.insertString("this is the statement")
        query = self.capitalisePython(doc)
        communicator = com.APICommunicator()                #create the communicator
        communicator.setConfiguration()                     #set the configuartion using config file
        communicator.checkConfiguration()                   #check whether the configuration is ok
        communicator.getResult(query)                       #query from wolfram API
        fileName = query+".txt"                             
        resultReader = wp.WolframMathResultReader(fileName) #read the stored result
        resultReader.getTotalResult()                       #get all the resources related to the result
        #resultReader.parseWolframResultToLibre()           #the parsing is not happening yet
                          #create the document
        text = doc.Text
        cursor = text.createTextCursor()
        for res in resultReader.plainTexts:                 #add formulas
            try:
                dochand.addFormulaToWriterDocument(doc,cursor,res)
                text.insertString( cursor, "\n\n", 0 )
            except Exception:
                print(res)  
        for img in resultReader.imageFileNames:             #add images to the document
            try:
                imageUrl = "file://"+os.path.dirname(__file__)+"/"+img
                dochand.addImageToWriterDocument(doc,cursor, imageUrl)
                text.insertString( cursor, "\n\n", 0 )
            except Exception:
                print(img)
                   
   
               
#####################################################      
# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper ()

# add the FormatFactory class to the implementation container,
# which the loader uses to register/instantiate the component.
g_ImplementationHelper.addImplementation (TutorialBuilder,
                    implementation_name,
                    implementation_services,
                    )
#import uno
#localContext = uno.getComponentContext()
#print(localContext)
#smgr = localContext.ServiceManager
#a= smgr.createInstanceWithContext("org.openoffice.comp.pyuno.demo.HelloWorld",localContext)
#a.addFormulaData()
#print(a)

'''
Created on Oct 2, 2013

@author: lakmal
'''
import Communicator as com
import WolframParser as wp
import DocumentHandler as dh
import os
import unohelper

class TutorialBuilder():
    def __init__ ( self ):
        pass
        
    def getUiElements(self):
        
    
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
        #text.insertString("this is the statement")
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
                
TutorialBuilder().addFormulaData()
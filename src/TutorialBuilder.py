'''
Created on Sep 12, 2013

@author: lakmal
'''

import Communicator as com
import WolframParser as wp
import DocumentHandler as dh
import os

def addFormulaData(query):
    communicator = com.APICommunicator()
    communicator.setConfiguration()
    communicator.checkConfiguration()
    communicator.getResult(query)
    fileName = query+".txt"
    resultReader = wp.WolframMathResultReader(fileName)
    resultReader.getTotalResult()
    #resultReader.parseWolframResultToLibre()           #the parsing is not happening yet
    dochand=dh.DocumentHandler()
    doc=dochand.createWriterDocument()
    text = doc.Text
    cursor = text.createTextCursor()
    print("HolyHawks")
    for res in resultReader.plainTexts:
        try:
            dochand.addFormulaToWriterDocument(doc,cursor,res)
            text.insertString( cursor, "\n\n", 0 )
        except Exception:
            print(res)  
    for img in resultReader.imageFileNames:
        try:
            imageUrl = "file://"+os.path.dirname(__file__)+"/"+img
            dochand.addImageToWriterDocument(doc,cursor, imageUrl)
            text.insertString( cursor, "\n\n", 0 )
        except Exception:
            print(img)
        
addFormulaData("int x*sinx dx")
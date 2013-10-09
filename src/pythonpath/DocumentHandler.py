'''
Created on Sep 9, 2013

@author: lakmal
'''
import uno
import unohelper



class DocumentHandler():    

    def createWriterDocument(self):                       #get the doc from the scripting context which is made available to all scripts
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        return doc
    
    def addImageToWriterDocument(self,doc,cursor,url):            
        text = doc.Text
        oShape = doc.createInstance( "com.sun.star.text.GraphicObject" )
        oShape.GraphicURL = url
        text.insertTextContent(cursor,oShape,uno.Bool(1)) 
        
    def addFormulaToWriterDocument(self,doc,cursor,formula):
        text = doc.Text 
        formulaObject=doc.createInstance("com.sun.star.text.TextEmbeddedObject")
        formulaObject.CLSID = "078B7ABA-54FC-457F-8551-6147e776a997"
        text.insertTextContent( cursor, formulaObject, 0 )
        formulaObject.getEmbeddedObject().Formula=formula
    


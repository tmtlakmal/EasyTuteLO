'''
Created on Oct 5, 2013

@author: lakmal
'''
import uno

class FormulaListHandler():
    
    def createFormulaList(self):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        doc = desktop.getCurrentComponent()
        if not hasattr(doc, "Text"):
            doc = desktop.loadComponentFromURL( "private:factory/swriter","_blank", 0, () )
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)

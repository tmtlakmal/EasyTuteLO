'''
Created on Oct 13, 2013

@author: lakmal
'''
import unittest
from pythonpaths import DocumentHandler
import uno


class TestDocumentHandler(unittest.TestCase):


    def testCreateWriterDocument(self):
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        smgr = ctx.ServiceManager
        docHand = DocumentHandler.DocumentHandler()
        test = smgr.createInstanceWithContext("com.sun.star.test.XSimpleTest",ctx)
        print(test)
        test.testInvariant("XDocument",docHand.createWriterDocument())
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateWriterDocument']
    unittest.main()
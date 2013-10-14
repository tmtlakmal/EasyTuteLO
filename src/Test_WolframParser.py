'''
Created on Aug 31, 2013

@author: lakmal
'''
from pythonpaths import WolframParser as wp
import unittest
import os

class TestWolframMathresultReader(unittest.TestCase):
                                                    #test class for WolframMathResultsReader class

    def testReadFile(self):                         #test case for read file method
        reader = wp.WolframMathResultReader("SampleResponse4.txt")
        self.assertEqual(reader.readFile(),"testResponse")
        reader = wp.WolframMathResultReader("SampleResponse3.txt")
        self.assertEqual(reader.readFile(),"NoSuchFile")

    def testGetSuccess(self):                       #test case for the get success method
        reader = wp.WolframMathResultReader("SampleResponse1.txt")
        self.assertEqual(reader.getSuccess(),'true')
        reader = wp.WolframMathResultReader("SampleResponse2.txt")
        self.assertEqual(reader.getSuccess(),'false')
        reader = wp.WolframMathResultReader("SampleResponse4.txt")
        self.assertEqual(reader.getSuccess(),'false')
        
    def testGetScanner(self):                       #test case for the get scanner method
        reader = wp.WolframMathResultReader("SampleResponse1.txt")
        reader.setVariables(reader.readFile())
        self.assertEqual(reader.getScanner(),'Identity')
        reader = wp.WolframMathResultReader("SampleResponse5.txt")
        reader.setVariables(reader.readFile())
        self.assertEqual(reader.getScanner(),'Integral')
        reader = wp.WolframMathResultReader("SampleResponse6.txt")
        reader.setVariables(reader.readFile())
        self.assertEqual(reader.getScanner(),'Derivative')
        
        
    def testSetNeedyData(self):                     #test case for the set needy data method
        reader = wp.WolframMathResultReader("SampleResponse1.txt")
        reader.setVariables(reader.readFile())
        reader.setNeedyData()
        self.assertEqual(reader.plainTexts[0],"y''(x)+y(x) = 0")
        self.assertEqual(reader.plainTexts[1],"second-order linear ordinary differential equation")
        self.assertEqual(reader.plainTexts[2],"y''(x) = -y(x)")
        self.assertEqual(reader.plainTexts[3],"y(x) = c_2 sin(x)+c_1 cos(x)")
        self.assertEqual(reader.images[0],"http://www5a.wolframalpha.com/Calculate/MSP/MSP19821f2462618ag8eei3000022e46e907f7hb7d1?MSPStoreType=image/gif&s=33")
        self.assertEqual(reader.images[4],"http://www5a.wolframalpha.com/Calculate/MSP/MSP19861f2462618ag8eei30000457ahabf08a3fg42?MSPStoreType=image/gif&s=33")
        
    def testGetName(self):                          #test case for getName method
        reader = wp.WolframMathResultReader("SampleResponse1.txt")
        self.assertEqual(reader.getName(),'SampleResponse1')
        reader = wp.WolframMathResultReader("SampleResponse2.txt")
        self.assertEqual(reader.getName(),'SampleResponse2')
        
    def testRetrieveImages(self):                   #test case for retrieveImages method
        reader = wp.WolframMathResultReader("SampleResponse1.txt")
        reader.setVariables(reader.readFile())
        reader.setNeedyData()
        reader.retrieveImages()
        for i in range (0,5):
            self.assertEqual(os.path.exists("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/SampleResponse1image"+`i`+".gif"),True)
            os.remove("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/SampleResponse1image"+`i`+".gif")
        
    
    def testGetTotalResult(self):                   #test case for getTotalResult method
        reader = wp.WolframMathResultReader("SampleResponse5.txt")
        reader.getTotalResult()
        for i in range (0,len(reader.images)):
            self.assertEqual(os.path.exists("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/SampleResponse5image"+`i`+".gif"),True)
            os.remove("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/SampleResponse5image"+`i`+".gif")
        
        reader = wp.WolframMathResultReader("SampleResponse6.txt")
        for i in range (0,5):
            self.assertEqual(os.path.exists("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/SampleResponse6image"+`i`+".gif"),False)
        
    def testParseWolframResultToLibre(self):        #test case from parse WolframResultToLibre method
        reader = wp.WolframMathResultReader("SampleResponse5.txt")
        reader.setVariables(reader.readFile())
        reader.setNeedyData()
        reader.parseWolframResultToLibre()
        for i in range(0,len(reader.parsedResult)):
            self.assertEqual(reader.parsedResult[i],"parsed"+str(reader.plainTexts[i]))  
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

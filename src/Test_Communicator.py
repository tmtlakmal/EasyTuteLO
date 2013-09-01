'''
Created on Sep 1, 2013

@author: lakmal
'''

import unittest,os
import Communicator as com

class Test_APICommunicator(unittest.TestCase):
    
    def testAPICommunicator(self):              #test case for API configuration
        a=com.APICommunicator('configuration1.txt')
        self.assertEquals(a.isFileConfigured(),True)
        a=com.APICommunicator('configuration2.txt')
        self.assertEquals(a.isFileConfigured(),False)
        a=com.APICommunicator()
        self.assertEquals(a.isFileConfigured(),True)
        os.rename("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configuration.txt","/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configurationBack.txt")
        a=com.APICommunicator()
        self.assertEquals(a.isFileConfigured(),False)
        os.rename("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configurationBack.txt","/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configuration.txt")






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
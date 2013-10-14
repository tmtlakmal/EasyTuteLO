'''
Created on Sep 1, 2013

@author: lakmal
'''

import unittest,os
from pythonpaths import Communicator as com

class Test_APICommunicator(unittest.TestCase):
    
    
    
    def testAPICommunicator(self):              #test case for API configuration
        a=com.APICommunicator('configuration1.txt')
        self.assertEquals(a.isFileConfigured(),False)
        a=com.APICommunicator('configuration2.txt')
        self.assertEquals(a.isFileConfigured(),False)
        a=com.APICommunicator()
        self.assertEquals(a.isFileConfigured(),True)
        #os.rename("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configuration.txt","/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configurationBack.txt")
        a=com.APICommunicator()
        self.assertEquals(a.isFileConfigured(),True)
        #os.rename("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configurationBack.txt","/home/lakmal/workspace/EasyTuteLO/WolframCom/src/configuration.txt")

    def testConfigurationSet(self):             #test case to check configuration
        a=com.APICommunicator()  
        a.setConfiguration()
        self.assertEquals(a.getAppID(),"4WKYHL-AWUQL4GWA3")
        self.assertEquals(a.getHost(),"http://api.wolframalpha.com/v2/query?")

    def testCheckConfiguartion(self):           #test case to check configuration 
        a=com.APICommunicator() 
        try: 
            a.setConfiguration()
            self.assertEquals(a.isConfigured(), True)
        except Exception:
            self.assertEquals(a.isConfigured(), False)
        a=com.APICommunicator("configuration1.txt") 
        try: 
            a.setConfiguration()
            self.assertEquals(a.isConfigured(), False)
        except Exception:
            self.assertEquals(a.isConfigured(), False)
            
    def testGetResult(self):                    #test case to get result method
        a=com.APICommunicator() 
        try:
            a.setConfiguration()
            s="int x*cosx dx"
            a.getResult(s)
            self.assertEquals(os.path.exists("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/"+s+".txt"),True)
            os.remove("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/"+s+".txt")
        except Exception:
            self.assertEquals(os.path.exists("/home/lakmal/workspace/EasyTuteLO/WolframCom/src/"+s+".txt"),False)
            print("connection or configuration problem")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
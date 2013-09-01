'''
Created on Aug 31, 2013

@author: lakmal
'''
#!/usr/bin/env python

class APICommunicator:        
    
    def __init__(self,fileName='configuration.txt'):    #create a communicator
        self.fileConfigured=False
        res=self.readConfigFile(fileName)               #default...checkconfiguration.txt
        if(res!="No config file"):                      #if no configuration file found set ...is not configured
            self.fileConfigured=True 
            self.configData = res          
        else:
            self.configData = ''                        #if no config file ..config data is null
    
    def readConfigFile(self,fileName):                  #read config file
        try:
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No config file"
    
    def isFileConfigured(self):                         #check whether the communicator config file is configured
        return self.fileConfigured
            
    def setConfiguration(self):
        pass
        

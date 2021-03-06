'''
Created on Aug 31, 2013

@author: lakmal
'''
#!/usr/bin/env python
import wap
import os
import urllib
import FileHandler as fh

universalFilePath="/home/lakmal/Documents/EasyTuteLO"

class APICommunicator:        
    
    def __init__(self,fileName='configuration.txt'):    #create a communicator
        self.fileConfigured=False
        self.configured = False
        res=self.readConfigFile(fileName)               #default...checkconfiguration.txt
        if(res!="No config file"):                      #if no configuration file found set ...is not configured
            self.fileConfigured=True 
            self.configData = res          
        else:
            self.configData = ''                        #if no config file ..config data is null
    
    def readConfigFile(self,fileName):                  #read config file
        try:
            print(os.sys.path[0])
            fileName = universalFilePath+"/"+fileName
            print(fileName)
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No config file"
    
    def isFileConfigured(self):                         #check whether the communicator config file is configured
        return self.fileConfigured
            
    def setConfiguration(self):                         #set variables in configuration file
        if(self.isFileConfigured()):
            for s in self.configData:
                tokens = s.split("=")
                if(tokens[0]=="appid"):                 #set appid
                    self.appid = tokens[1].split("\n")[0]
                elif(tokens[0]=="host"):                #set host
                    self.host = tokens[1].split("\n")[0] 
                else:
                    print(s)
            self.configured=True
            self.waeo = wap.WolframAlphaEngine(self.appid,self.host)
            #self.checkConfiguration()                   #set configured true
        else:
            print("The file is not configured.")
            
    def checkConfiguration(self):                       #if configuration is proper set configured
        waeo = wap.WolframAlphaEngine(self.appid,self.host)
        waeq = wap.WolframAlphaQuery("pi",self.appid)
        waeq.ToURL()
        try:
            waeqr = wap.WolframAlphaQueryResult(waeo.PerformQuery(waeq.Query))
            if(waeqr.IsSuccess()):               
                self.waeo = waeo
                self.configured=True
            else:
                self.configured=False
        except Exception:
            print("connection failure")
        
            
    def isConfigured(self):                             #check whether the communicator is configured
        return self.configured
    
    def getAppID(self):                                 #method to get appid
        return self.appid
    
    def getHost(self):                                  #method to get host
        return self.host
    
    
                
    def getResult(self,query):                          #method to get result
        if(self.isConfigured()):
            self.stepInput=''
            txtFilePath = fh.FileHandler().createFilePathForTheQuery(query)
            query=urllib.quote(query)                   #quote the url
            waeq = wap.WolframAlphaQuery(query,self.appid)
            waeq.Async = False
            waeq.ToURL()                                #get result from wolfram alpha
            result = self.waeo.PerformQuery(waeq.Query)
            print(result)
            f = open(txtFilePath,'w')                   #write the result to a file
            f.write(result)
            f.close()
            self.getStepInput(result)                   #get the step input by reading the file
            waeq = wap.WolframAlphaQuery(query,self.appid)
            if(self.stepInput!=''):                     #get the result with step by solution 
                waeq.AddPodState(self.stepInput)
            waeq.Async = False
            waeq.ToURL()                                #query the step wise solution result
            result = self.waeo.PerformQuery(waeq.Query)
            print(txtFilePath)                          #write the result into file
            f = open(txtFilePath,'w')
            f.write(result)
            f.close()  
            
    def getStepInput(self,result):                      #get the step input line from the result file
        waeqr = wap.WolframAlphaQueryResult(result)
        for pod in waeqr.Pods():
            waep = wap.Pod(pod)
            for state in waep.PodStates():
                for stateData in state:
                    if(stateData[0]=='state'):
                        if(stateData[2][1]=='Step-by-step solution'):
                            self.stepInput = stateData[1][1]
        
    
    def readFile(self,query):                     #read the file and give the result - 
        try:  
            fPath=os.sys.path[0][0:len(os.sys.path[0])-12]+"/equationFiles/"+query.lower()+'.txt'
            print(fPath)                             
            f = open(fPath, 'r')
            result = f.read()
            return result
        except IOError:                             #if the file is not existing return NoSuchFile
            return "NoSuchFile"      
        
    def configureAndGetResult(self,query):          #set the configuartion and get result
        self.setConfiguration()
        self.getResult(query)   


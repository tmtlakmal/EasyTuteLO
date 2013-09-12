'''
Created on Aug 31, 2013

@author: lakmal
'''
#!/usr/bin/env python
import wap

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
            self.checkConfiguration()                   #set configured true
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
            try:
                waeq = wap.WolframAlphaQuery(query,self.appid)
                waeq.Async = False
                waeq.ToURL()
                result = self.waeo.PerformQuery(waeq.Query)
                waeqr = wap.WolframAlphaQueryResult(result)
                for pod in waeqr.Pods():
                    waep = wap.Pod(pod)
                    if(waep.PodStates()[0][1][2][1]=='Step-by-step solution'):
                        self.stepinput = waep.PodStates()[0][1][1][1]
                        break
                waeq = wap.WolframAlphaQuery(query,self.appid)
                waeq.AddPodState(self.stepinput)
                waeq.Async = False
                waeq.ToURL()
                result = self.waeo.PerformQuery(waeq.Query)
                f = open(query+'.txt','w')
                f.write(result)
                f.close()
            except Exception:
                print("connection problem") 

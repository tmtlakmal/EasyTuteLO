'''
Created on Aug 31, 2013

@author: lakmal
'''
import wap
import urllib

class WolframMathResultReader:
    
    def __init__(self,fileName):            #create the reader for a particular file
        self.fileName = fileName
        self.images = []
        self.plainTexts=[]
        self.parsedResult=[]
        self.imageFileNames=[]
        self.name = self.fileName[0:len(self.fileName)-4]
                 
    def getSuccess(self):                   # if the content in the file is valid success
        result = self.readFile()
        try:
            waQueryResult = wap.WolframAlphaQueryResult(result)
            return waQueryResult.IsSuccess()[0]
        except Exception:                   # if any error occured while parsing return false
            return 'false'
            
           
    def readFile(self):                     #read the file and give the result - 
        try:                                
            f = open(self.fileName, 'r')
            result = f.read()
            return result
        except IOError:                     #if the file is not existing return NoSuchFile
            return "NoSuchFile"
    
    def setVariables(self,result):          #setting the variables read 
        self.WolframAlphaQueryResult = wap.WolframAlphaQueryResult(result)
        
            
    def getScanner(self):                   #get the scanner of the first pod
        firstPod = wap.Pod(self.WolframAlphaQueryResult.Pods()[0]) 
        return firstPod.Scanner()[0]
    
    def setNeedyData(self):                 #set the images and plain texts into arrays       
        for pod in self.WolframAlphaQueryResult.Pods():
            podNew = wap.Pod(pod)
            for subpod in podNew.Subpods():
                subpodNew = wap.Subpod(subpod)
                self.plainTexts.append(subpodNew.Plaintext()[0])
                self.images.append(dict(subpodNew.Img()[0])['src'])
                                            #set the src of the images and plain text details

    def getName(self):                      #get the name of the reader// this is used to name image files
        return self.name
    
    def retrieveImages(self):               #retrieving images from wolfram
        count=0
        try:
            for imgUrl in self.images:
                imageFileName=self.name+'image'+`count`+'.gif'
                self.imageFileNames.append(imageFileName)
                f = open(imageFileName,'wb')
                f.write(urllib.urlopen(imgUrl).read())
                f.close()
                count+=1
        except Exception:
            print("Exception occured")
    
    def getTotalResult(self):               #getTotalResult from wolfram including images
        self.setVariables(self.readFile())
        self.setNeedyData()    
        self.retrieveImages()   
       
    def parseWolframResultToLibre(self):    #parse results and assign to parsed results
        for res in self.plainTexts:
            ##code to parse each result comes here
            s = str(res)
            self.parsedResult.append("parsed"+s)
         
     

'''
Created on Oct 13, 2013

@author: lakmal
'''
import hashlib

universalFilePath="/home/lakmal/Documents/EasyTuteLO"

class FileHandler():
    
    def createFilePathForTheQuery(self,query):
        query = query.lower()
        queryHash = hashlib.md5(query)
        fileName = universalFilePath+"/equationFiles/"+queryHash.hexdigest()+".txt"
        return fileName
    
    def createImageFilePathForTheQuery(self,query,img):
        query =query.lower()
        queryHash = hashlib.md5(query)
        fileName = universalFilePath+"/equationFiles/"+queryHash.hexdigest()+img+".gif"
        return fileName 
    
    def createThumbImageFilePathForTheQuery(self,query,img):
        query =query.lower()
        queryHash = hashlib.md5(query)
        fileName = universalFilePath+"/equationFiles/"+queryHash.hexdigest()+img+"thumb.gif"
        return fileName
    
    def addFormulasToStorage(self,query):
        fileName = universalFilePath+"/equationFiles/equationList.txt" 
        with open(fileName, "a") as myfile:
            myfile.write(query.lower()+"\n")
            myfile.close()

    def readFormulaStorage(self):
        try:
            fileName = universalFilePath+"/equationFiles/equationList.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Formula Storage file"
        
    def readDetailsFile(self):
        try:
            fileName = universalFilePath+"/details.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Details file"
    
    def clearDetailsFile(self):
        try:
            fileName = universalFilePath+"/details.txt" 
            f = open(fileName, 'w') 
            f.write("")
            f.close()
        except Exception:                               #if the file not found return "No config file"
            return "No Details file"
    
    def clearImagesFile(self):
        try:
            fileName = universalFilePath+"/images.txt" 
            f = open(fileName, 'w') 
            f.write("")
            f.close()
        except Exception:                               #if the file not found return "No config file"
            return "No Images file"
    
    def readImagesFile(self):
        try:
            fileName = universalFilePath+"/images.txt" 
            f = open(fileName, 'r') 
            res =f.readlines()
            f.close()
            return res
        except Exception:                               #if the file not found return "No config file"
            return "No Details file"
        
    def addDetailsFileData(self,query,selectedItems,selectedImages):
        detailsFilePath = universalFilePath+"/details.txt" 
        imagesFilePath = universalFilePath+"/images.txt" 
        f = open(detailsFilePath,'w')
        f.write(query+"\n")
        f.close()
        f = open(detailsFilePath,'a')
        for s in selectedItems:
            if(s):
                f.write("True\n")
            else: 
                f.write("False\n") 
        f.close() 
        f = open(imagesFilePath,'w')
        f.write(query+"\n")
        f.close()
        f = open(imagesFilePath,'a')
        for s in selectedImages:
            if(s):
                f.write("True\n")
            else: 
                f.write("False\n") 
        f.close() 
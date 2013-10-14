'''
Created on Sep 12, 2013

@author: lakmal
'''


from pythonpaths import TutorialHandler as th
import unohelper

implementation_name = "org.libreoffice.EasyTuteLO.TutorialBuilder" # as defined in Factory.xcu
implementation_services = ("org.libreoffice.EasyTuteLO.TutorialBuilder",)

       

class TutorialBuilder():                                #tutorial builder class
    def just(self):
        pass
    
    
    
def AddFormulaData():                                   #add formula data method
    th.TutorialHandler().addFormulaData()

def AddPreviousFormulaData():                           #add previous formula data method
    th.TutorialHandler().addPreviousFormulaData()
    
           
      
         

        
                                  
#####################################################      
# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper ()

# add the FormatFactory class to the implementation container,
# which the loader uses to register/instantiate the component.
g_ImplementationHelper.addImplementation (TutorialBuilder,
                    implementation_name,
                    implementation_services,
                    )
AddFormulaData()
#print(TutorialBuilder().checkAvailabilityOfFormula("int x*sinx dx"))
#print(urllib.quote("int x dx"))
#TutorialBuilder().textDetailsAboutFormula("int x dx")
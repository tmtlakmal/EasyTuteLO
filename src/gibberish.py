
import urllib
import wap

def readFile():
    f = open('sampleResponse.txt', 'r')
    res = f.read()
    return res

def getFromWolfram():
    inputsta='y"+y=0'
    appid = '4WKYHL-AWUQL4GWA3' # Use your app id
    waeo = wap.WolframAlphaEngine(appid,'http://api.wolframalpha.com/v2/query?')
    waeq = wap.WolframAlphaQuery(inputsta,appid)
    waeq.ScanTimeout = '3.0'
    waeq.AddPodState('DifferentialEquationSolution__Step-by-step solution')
    waeq.Async = False
    waeq.ToURL() # After configuring the waeq must call ToURL()
    #print(waeq.Query)
    result = waeo.PerformQuery(waeq.Query) # result is in xml format
    return result

def WolframPyToJson():
    #waeqr = wap.WolframAlphaQueryResult(getFromWolfram())
    waeqr = wap.WolframAlphaQueryResult(readFile())
    jsonResult = waeqr.JsonResult()
    a = jsonResult.decode()
    print(a)
    print(a[0])
    #print(jsonResult.)
    print(jsonResult[2])
    print(jsonResult[3])

def WolframPy():
    #from urllib import request  
    #url = "http://api.wolframalpha.com/v2/query?input=pi&appid=4WKYHL-AWUQL4GWA3"
    #urllib.getproxies()
    #fp = request.urlopen(url)
    #fp = urllib.urlopen(url)
    #data = fp.read()
    #f = open('workfile', 'w')
    #f.write(data)
    #n = int(data)
    #giveTheInt = [n]
    #print(giveTheInt)
    #print(data)
    
    result = getFromWolfram()
    #result = readFile()
    print(result)
    waeqr = wap.WolframAlphaQueryResult(result)
    #desktop = XSCRIPTCONTEXT.getDesktop()
    #model = desktop.getCurrentComponent()
    #if not hasattr(model, "Text"):
    #    model = desktop.loadComponentFromURL("private:factory/swriter","_blank", 0, () )
    #text = model.Text
    #cursor = text.createTextCursor()
    for pod in waeqr.Pods():
        waep = wap.Pod(pod)
        xtit = waep.Title()
        for u in xtit:
            #text.insertString( cursor, u, 0 )
            print(u)
            if(u=='Plots of sample individual solutions'):
                plotSub = waep.Subpods()
                for pltpod in plotSub:
                    spod = wap.Subpod(pltpod)
                    imgData = spod.Img()
                    a=dict(imgData.pop())
                    print(a['src'])
                    imgurl = a['src']
                    f = open('00000001.gif','wb')
                    f.write(urllib.urlopen(imgurl).read())
                    f.close()
                    print("done")
                    
        #text.insertString( cursor, "Hello World", 0 )
        print(waep.Title())
    #text.insertString( cursor, "Hello World", 0 )

def getInputFromDoc():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    doc = desktop.getCurrentComponent()
    if not hasattr(doc, "Math"):
        doc = desktop.loadComponentFromURL( "private:factory/smath","_blank", 0, () )
    formula=doc.createInstance("com.sun.star.formula.FormulaProperties")
    formula.Formula="int x dx"
#WolframPy()
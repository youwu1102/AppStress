#-*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys
import os
import time
from libs.GlobalVariable import GlobalVariable
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.dom.minidom import Document
import wx.lib.agw.customtreectrl as CT
import datetime,wx,threading,commands,subprocess,shutil
import xml.dom.minidom
from libs.UiFrame import Frame

#
# #写入默认路径地址
# class QGP_Path():
#     def __init__(self):
#         LOCATION = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '..'))
#         self.PATH_TESTCASES = '%s\\repository\\testcases' %LOCATION
#         self.PATH_JAVA_JAR = 'C:\\QGPAutomationV2.0.0_BASIC\\resource\\UiRobotium'
#         self.PATH_JAVA_CLASS = os.path.join(self.PATH_JAVA_JAR,'src')
#         self.PATH_TEMPLATE = os.path.join(self.PATH_JAVA_CLASS,'template','Template.java')
#         self.NAME_JAVA_JAR = 'wuyou'
#         self.NUMBER_ANDROID_ID = '10'
#         self.PATH_LOGS = '%s\\repository\\logs' %LOCATION
#         self.PATH_RESULTS = '%s\\repository\\results' %LOCATION
#         self.PATH_DOCS='%s\\docs' %LOCATION
#         self.PATH_PLANS ='%s\\repository\\plans' %LOCATION
#         self.PATH_ANT = '%s\\resource\\apache-ant-1.9.4\\bin' %LOCATION
#
# class RedirectText(object):
#     def __init__(self,aWxTextCtrl):
#         self.out=aWxTextCtrl
#
#     def write(self,string):
#         self.out.AppendText(string)
#
# class CreatDir():
#     def __init__(self):
#         pass
#     def creatDir(self,name):
#         os.mkdir('%s\%s' %(QGP_Path().PATH_RESULTS,name))
#         os.makedirs('%s\%s\Device' %(QGP_Path().PATH_LOGS,name))
#         os.makedirs('%s\%s\Host' %(QGP_Path().PATH_LOGS,name))
#
#
#
# #获取连接的所有手机的serialno
# class DevicesList():
#     #默认配置均为No Device
#     def __init__(self):
#         self.devices_List = ['No Device', 'No Device', 'No Device', 'No Device']
#     #获取连接的手机的serialno
#     def getDevicesList(self):
#         list=[]
#         devices  = subprocess.Popen ('adb devices', stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
#         for line in iter(devices.stdout.readline, ''):
#             if 'device' in line:
#                 if 'List of devices attached' in line:
#                     pass
#                 else:
#                     list.append(line.strip('\r\n')[:-7])
#             elif 'offline' in line:
#                 pass
#             elif 'unauthorized' in line:
#                 pass
#             else:
#                 pass
#         for x in range(len(list)):
#             self.devices_List[x]=list[x]
#
#左侧树构造


#
# class TestCasePlan():
#     QGP=QGP_Path()
#     def __init__(self):
#         pass
#     def establishTestPlan(self,TestCase,TestPlanName = 'testplan'):
#         doc = Document()
#         if TestCase==[]:
#             print "Please select some Test Case"
#         else:
#             PREVIOUS_PACKAGE_NAME=''
#             PREVIOUS_CLASS_NAME=''
#             testPlan = doc.createElement('TestPlan')
#             testPlan.setAttribute('name',TestPlanName)
#             for x in range(len(TestCase)):
#                 if TestCase[x][0] != PREVIOUS_PACKAGE_NAME:
#                     testPackage=doc.createElement('TestPackage')
#                     testPackage.setAttribute('name',TestCase[x][0])
#                     PREVIOUS_PACKAGE_NAME=testPackage.getAttribute('name')
#                     testClass=doc.createElement('TestClass')
#                     testClass.setAttribute('name',TestCase[x][1])
#                     PREVIOUS_CLASS_NAME=TestCase[x][1]
#                     testCase=doc.createElement('TestCase')
#                     testCase.setAttribute('name',TestCase[x][2])
#                     testClass.appendChild(testCase)
#                     testPackage.appendChild(testClass)
#                     testPlan.appendChild(testPackage)
#                 else:
#                     if TestCase[x][1] != PREVIOUS_CLASS_NAME:
#                         testClass=doc.createElement('TestClass')
#                         testClass.setAttribute('name',TestCase[x][1])
#                         PREVIOUS_CLASS_NAME=TestCase[x][1]
#                         testCase=doc.createElement('TestCase')
#                         testCase.setAttribute('name',TestCase[x][2])
#                         testClass.appendChild(testCase)
#                         testPackage.appendChild(testClass)
#                     else:
#                         testCase=doc.createElement('TestCase')
#                         testCase.setAttribute('name',TestCase[x][2])
#                         testClass.appendChild(testCase)
#             doc.appendChild(testPlan)
#             # f = open('%s\\%s.xml'% (QGP.PATH_PLANS,TestPlanName),'w')
#             # f.write(doc.toprettyxml(indent = '',encoding='utf-8'))
#             # f.close()
#             return doc
#
#     def readTestPlan(self,TestPlanName = 'testplan'):
#         testPlanList=[]
#         QGP=QGP_Path()
#         dom = xml.dom.minidom.parse('%s\\%s.xml'% (QGP.PATH_PLANS,TestPlanName))
#         root = dom.documentElement
#         TestPackageList = root.getElementsByTagName('TestPackage')
#         for x in range(len(TestPackageList)):
#             TestPackage=TestPackageList[x]
#             TestClassList=TestPackage.getElementsByTagName('TestClass')
#             for y in range(len(TestClassList)):
#                 TestClass=TestClassList[y]
#                 TestCaseList = TestClass.getElementsByTagName('TestCase')
#                 for z in range(len(TestCaseList)):
#                     TestCase=TestCaseList[z]
#                     PATH =  '%s\\%s\\%s\\%s' %(QGP.PATH_TESTCASES,TestPackage.getAttribute('name'),TestClass.getAttribute('name'),TestCase.getAttribute('name'))
#                     testPlanList.append(PATH)
#         return testPlanList
# class writeTestCase:
#     def __init__(self):
#         pass
#     def writeToJAVA(self,TestCaseList):
#         QGP=QGP_Path()
#         PATH=QGP_Path().PATH_TESTCASES
#         PATH_JAVA_CLASS=QGP_Path().PATH_JAVA_CLASS
#         files_Package = os.listdir(PATH)
#         for testPackage in files_Package:
#             if os.path.isdir(os.path.join(PATH, testPackage)):
#                 #print testPackage
#                 if testPackage not in os.listdir(PATH_JAVA_CLASS):
#                     os.mkdir('%s\\%s' %(PATH_JAVA_CLASS,testPackage))
#                 files_Class= os.listdir(os.path.join(PATH, testPackage))
#                 for testClass in files_Class:
#                     if os.path.isdir(os.path.join(PATH, testPackage,testClass)):
#                         TestClass=open('%s\\%s\\%s.java'%(PATH_JAVA_CLASS,testPackage,testClass.replace('-','')),'w')
#                         Template=open(QGP_Path().PATH_TEMPLATE,'r')
#                         for line in Template:
#                             if 'package Template;' in line:
#                                 TestClass.writelines('package %s;\r\n' %testPackage)
#                             elif 'public class Template extends UiAutomatorTestCase' in line:
#                                 TestClass.writelines('public class %s extends UiAutomatorTestCase\r\n' %testClass.replace('-',''))
#                             elif ('//start' in line):
#                                 for files_Case in TestCaseList:
#                                     a=files_Case[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')
#                                     if a[0]==testPackage and a[1]==testClass:
#                                         Case=open(files_Case,'r')
#                                         TestClass.writelines('    public void test%s() throws UiObjectNotFoundException\r' % a[2][:-4].replace('-',''))
#                                         TestClass.writelines('    {\r')
#                                         for l in Case:
#                                             TestClass.writelines('       '+l.strip('	').strip('﻿'))
#                                         TestClass.writelines('    }\r')
#                                         TestClass.writelines('\r\n')
#                                         Case.close
#
#                             else:
#                                 TestClass.writelines(line)
#                         Template.close()
#                         TestClass.close()
#
#
# #先把所有的初始文件写成模板
#     def writeDefault(self):
#         PATH=QGP_Path().PATH_TESTCASES
#         PATH_JAVA_CLASS=QGP_Path().PATH_JAVA_CLASS
#         files_Package = os.listdir(PATH)
#         for testPackage in files_Package:
#             if os.path.isdir(os.path.join(PATH, testPackage)):
#                 #print testPackage
#                 if testPackage not in os.listdir(PATH_JAVA_CLASS):
#                     os.mkdir('%s\\%s' %(PATH_JAVA_CLASS,testPackage))
#                 files_Class= os.listdir(os.path.join(PATH, testPackage))
#                 for testClass in files_Class:
#                     if os.path.isdir(os.path.join(PATH, testPackage,testClass)):
#                         TestClass=open('%s\\%s\\%s.java'%(PATH_JAVA_CLASS,testPackage,testClass.replace('-','')),'w')
#                         Template=open(QGP_Path().PATH_TEMPLATE,'r')
#                         for line in Template:
#                             if 'package Template;' in line:
#                                 TestClass.writelines('package %s;\r\n' %testPackage)
#                             elif 'public class Template extends UiAutomatorTestCase' in line:
#                                 TestClass.writelines('public class %s extends UiAutomatorTestCase\r\n' %testClass.replace('-',''))
#                             else:
#                                 TestClass.writelines(line)
#                         Template.close()
#                         TestClass.close()
# class MainTest():
#     def buildJAR(self):
#         self.buildPass=False
#         print os.popen('android create uitest-project -n %s -t %s -p %s' % (QGP_Path().NAME_JAVA_JAR,
#                                                                             QGP_Path().NUMBER_ANDROID_ID,
#                                                                             QGP_Path().PATH_JAVA_JAR)).read()
#
#         #os.system('cd %s\\' %QGP_Path().PATH_ANT)
#         data  = subprocess.Popen ('ant build -buildfile %s//build.xml' % QGP_Path().PATH_JAVA_JAR, stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE, shell = True)
#         for line in iter(data.stdout.readline, ''):
#             time.sleep(0.1)
#             if 'BUILD SUCCESSFUL' in line:
#                 self.buildPass=True
#             print line.strip('\r\n')
#
#
#     def getClass(self):
#         PLAN=TestCasePlan().readTestPlan('testplan')
#         CLASS=[]
#         for path in PLAN:
#             array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
#             if array_path[1] not in CLASS:
#                 CLASS.append(array_path[1])
#         #print CLASS
#         return CLASS
#     def getPackage(self):
#         PLAN=TestCasePlan().readTestPlan('testplan')
#         PACKAGE=[]
#         for path in PLAN:
#             array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
#             if array_path[0] not in PACKAGE:
#                 PACKAGE.append(array_path[0])
#         #print PACKAGE
#         return PACKAGE
#
#     def runTest(self,StartTime):
#         os.system('adb -s %s push %s\\bin\\%s.jar data/local/tmp' % (serial_number,QGP_Path().PATH_JAVA_JAR,QGP_Path().NAME_JAVA_JAR))
#         TestClass=self.getClass()
#         TestPackage=self.getPackage()
#         t=TimeFormat()
#         Part=[]
#         out=outputFormat()
#         out.setValue2Zero()
#         out.PackageStartFormat(TestPackage[0])
#         if len(TestClass)==1:
#             self.class_now=TestClass[0]
#             f = open('%s\%s\Host\%s.txt' %(QGP_Path().PATH_LOGS,StartTime,TestClass[0]),'w')
#             f.write('StartTime=%s\r\n' %t.getTime())
#             cmd = 'adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,TestPackage[0],TestClass[0].replace('-',''))
#             #print cmd
#             dataRun = subprocess.Popen (cmd , stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
#             Thread_Log=threading.Thread(target=self.LogThread)
#             Thread_Log.start()
#             out.ClassStartFormat(TestClass[0])
#             out.setClassValue2Zero()
#             for line in iter(dataRun.stdout.readline, ''):
#                 f.writelines(line)
#                 Part.append(line)
#                 if 'INSTRUMENTATION_STATUS_CODE:' in line:
#                     out.lineFormat(Part)
#                     Part=[]
#
#             out.ClassEndFormat(TestClass[0])
#             f.write('EndTime=%s\r\n'  %t.getTime())
#             f.close()
#             out.PackageEndFormat(TestPackage[0])
#         else:
#             for Class in TestClass:
#                 os.system('adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,'ChangeCountry',Class.replace('-','')))
#                 # for x in range(20):
#                 #     print x
#                 #     time.sleep(10)
#                 self.class_now=Class
#                 os.system('adb -s %s push %s\\bin\\%s.jar data/local/tmp' % (serial_number,QGP_Path().PATH_JAVA_JAR,QGP_Path().NAME_JAVA_JAR))
#                 Thread_Log=threading.Thread(target=self.LogThread)
#                 Thread_Log.start()
#                 f = open('%s\%s\Host\%s.txt' %(QGP_Path().PATH_LOGS,StartTime,Class),'w')
#                 f.write('StartTime=%s\r\n' %t.getTime())
#                 dataRun = subprocess.Popen ('adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,TestPackage[0],Class.replace('-','')), stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
#                 out.ClassStartFormat(Class)
#                 out.setClassValue2Zero()
#                 for line in iter(dataRun.stdout.readline, ''):
#                     f.writelines(line)
#                     Part.append(line)
#                     if 'INSTRUMENTATION_STATUS_CODE:' in line:
#                         out.lineFormat(Part)
#                         Part=[]
#
#                 out.ClassEndFormat(Class)
#                 f.write('EndTime=%s\r\n'  %t.getTime())
#                 f.close()
#                 #time.sleep(180)
#             out.PackageEndFormat(TestPackage[0])
#
#     def LogThread(self):
#         os.system('adb -s %s logcat -v time >%s/%s/Device/%s_logcat.txt' %(serial_number,QGP_Path().PATH_LOGS,self.start_time,self.class_now))
#
#     def main(self):
#         self.buildJAR()
#         if self.buildPass==True:
#             t=TimeFormat()
#             self.start_time=t.getTime()
#             CreatDir().creatDir(self.start_time)
#
#
#             self.runTest(self.start_time)
#             res=Result()
#             #wuyou
#             logPart=res.dLogPart(self.start_time)
#             self.logforXml=[]
#             for x in range(len(logPart)):
#                 self.logforXml.append(res.dicTest(logPart[x]))
#             res.xml(self.logforXml,self.start_time)
#             out = outputFormat()
#             out.End()
#
#             #os.system('adb -s %s  reboot' % serial_number)
#
#         else:
#             print 'please check the information'
#
# class TimeFormat():
#     def __init__(self):
#         pass
#     def getTime(self):
#         Time_Format = time.strftime('%Y.%m.%d_%H.%M.%S',time.localtime(time.time()))
#         return Time_Format
#
#     def getDataTime(self):
#         DATA=datetime.datetime.now()
#         DATA_Format = DATA.strftime('%a %b %d %H:%M:%S %Y')
#         return DATA_Format
#     def getLogResultTime(self):
#         ResultTime_Format = time.strftime('%m-%d  %H:%M:%S',time.localtime(time.time()))
#         return ResultTime_Format
#
# class Result():
#     def __init__(self):
#         pass
#     def dicTest(self,logPart):
#         test={}
#         a=[]
#         for x in range(len(logPart)):
#             if 'INSTRUMENTATION_STATUS: id'in logPart[x]:
#                 test['id']=logPart[x][27:].strip('\r\n')
#             elif 'INSTRUMENTATION_STATUS: test' in logPart[x]:
#                 test['test']=logPart[x][29:].strip('\r\n')
#             elif 'INSTRUMENTATION_STATUS: numtests' in logPart[x]:
#                 test['numtests']=logPart[x][33:].strip('\r\n')
#             elif  'INSTRUMENTATION_STATUS: stream' in logPart[x]:
#                 test['stream']=logPart[x][31:].strip('\r\n')
#             elif  'INSTRUMENTATION_STATUS: class' in logPart[x]:
#                 test['class']=logPart[x][30:].strip('\r\n')
#             elif  'INSTRUMENTATION_STATUS: stack' in logPart[x]:
#                 test['stack']=logPart[x][30:].strip('\r\n')
#                 for y in range(len(logPart)-x-1):
#                     if '	at' in logPart[y+x+1]:
#                         a.append(logPart[y+x+1].strip('\t'))
#                     else:
#                         break
#                 test['FailReason']=a
#
#             elif  'INSTRUMENTATION_STATUS_CODE:' in logPart[x]:
#                 test['CODE']=logPart[x][29:].strip('\r\n')
#         return test
#
#
#     result=[]
#     def getResult(self,Start_Time):
#         self.result=[]
#         result_path='%s\%s\Host' %(QGP_Path().PATH_LOGS,Start_Time)
#         #result_path='%s\%s\Host' %(LOG_PATH,'2015.05.26_17.00.10')
#         list=os.listdir(result_path)
#         for file in list:
#             if file[-4:] == '.txt':
#                 self.result.append(file)
#         return self.result
#
#
#
#     def dLogPart(self,Start_Time):
#         files = self.getResult(Start_Time)
#         ALL=[]
#         Part=[]
#         for log in files:
#             file = open('%s\%s\Host\%s' %(QGP_Path().PATH_LOGS,Start_Time,log),'r')
#         #file = open('%s\%s\Host\%s.txt' %(LOG_PATH,'2015.05.26_17.00.10','ForExample'),'r')
#
#             for line in file:
#                 if 'INSTRUMENTATION_STATUS_CODE:' in line:
#                     Part.append(line)
#                     ALL.append(Part)
#                     Part=[]
#                 elif 'EndTime=' in line:
#                     if self.EndTime < line[8:]:
#                         self.EndTime=line[8:].strip('\r\n')
#                 elif 'StartTime=' in line:
#                     if self.StartTime > line[10:]:
#                         self.StartTime=line[10:].strip('\r\n')
#
#
#                 Part.append(line)
#             file.close()
#
#         return ALL
#     StartTime='9999999999999'
#     EndTime=''
#     def getCurrentlTime(self):
#         DATA=datetime.datetime.now()
#         DATA_Format = DATA.strftime('%a %b %d %H:%M:%S %Y')
#         return DATA_Format
#
#     def xml(self,log4xml,Start_Time):
#         Total,Pass,Fail=0,0,-len(self.result)
#         for x in range(len(log4xml)):
#             if log4xml[x].get('CODE') == '1':
#                 Total+=1
#             elif log4xml[x].get('CODE') == '0':
#                 Pass+=1
#             elif log4xml[x].get('CODE') == '-2' or log4xml[x].get('CODE') == '-1':
#                 Fail+=1
#
#         testPlan = 'wait for write'
#
#         Hosename=os.popen('Hostname').read()
#
#
#
#         doc = Document()
#         abc = doc.createProcessingInstruction("xml-stylesheet","type=\"text/xsl\" href=\"cts_result.xsl\"")
#         doc.appendChild(abc)
#         Result = doc.createElement('TestResult')
#         Result.setAttribute('testPlan', testPlan)
#         Result.setAttribute('starttime', self.StartTime)
#         Result.setAttribute('endtime', self.EndTime)
#         Result.setAttribute('suite', 'QGP_Automation')
#         doc.appendChild(Result)
#
#
#
#         DeviceInfo = doc.createElement('DeviceInfo')
#
#         Result.appendChild(DeviceInfo)
#         BuildInfo =doc.createElement('BuildInfo')
#         BuildInfo.setAttribute('productName', ADB_getValue().product_Name)
#         BuildInfo.setAttribute('productModel', ADB_getValue().product_Model)
#         BuildInfo.setAttribute('deviceID', serial_number)
#         BuildInfo.setAttribute('AUVersion', ADB_getValue().version_AU)
#         BuildInfo.setAttribute('METAVersion', ADB_getValue().version_Meta)
#         BuildInfo.setAttribute('AndroidVersion', ADB_getValue().version_Release)
#         BuildInfo.setAttribute('AndroidAPILevel', ADB_getValue().version_SDK)
#
#
#         DeviceInfo.appendChild(BuildInfo)
#         HostInfo =doc.createElement('HostInfo')
#         HostInfo.setAttribute('name', Hosename)
#         HostInfo.setAttribute('osversion', 'wait for write')
#         HostInfo.setAttribute('osname', 'wait for write')
#         Result.appendChild(HostInfo)
#         Summary=doc.createElement('Summary')
#         Summary.setAttribute('total',str(Total))
#         Summary.setAttribute('pass',str(Pass))
#         Summary.setAttribute('failed',str(Fail))
#         Result.appendChild(Summary)
#         for y in range(len(self.result)):
#             TestPackage=doc.createElement('TestPackage')
#             TestPackage.setAttribute('name',self.result[y][:-4])
#             aaa=self.result[y][:-4].replace('-','')
#             TestPackage.setAttribute('appPackageName',self.result[y][:-4])#wuyou
#             TestSuite=doc.createElement('TestSuite')
#             TestCase =doc.createElement('TestCase')
#             for x in range(len(log4xml)):
#                 CLASS = log4xml[x].get('class')
#                 if CLASS !=None:
#                     className=CLASS.split('.')
#                     if className[1]==aaa:
#
#                         if log4xml[x].get('CODE') == '1':
#                             pass
#                         elif log4xml[x].get('CODE') == '-1':
#                             Test=doc.createElement('Test')
#                             Test.setAttribute('name',log4xml[x].get('test'))
#                             Test.setAttribute('result','fail')
#                             FailedScene=doc.createElement('FailedScene')
#                             FailedScene.setAttribute('message',log4xml[x].get('stack'))
#                             Test.appendChild(FailedScene)
#                             a1=log4xml[x].get('FailReason')
#                             if a1 !=None:
#                                 StackTrace=doc.createElement('StackTrace')
#                                 testR=doc.createTextNode(a1[0])
#                                 StackTrace.appendChild(testR)
#                                 FailedScene.appendChild(StackTrace)
#                                 TestCase.appendChild(Test)
#                         elif log4xml[x].get('CODE') == '0':
#                             Test=doc.createElement('Test')
#                             Test.setAttribute('name',log4xml[x].get('test'))
#                             Test.setAttribute('result','pass')
#                             TestCase.appendChild(Test)
#                         elif log4xml[x].get('CODE') == '-2':
#                             Test=doc.createElement('Test')
#                             Test.setAttribute('name',log4xml[x].get('test'))
#                             Test.setAttribute('result','fail')
#                             FailedScene=doc.createElement('FailedScene')
#                             FailedScene.setAttribute('message',log4xml[x].get('stack'))
#                             Test.appendChild(FailedScene)
#                             a1=log4xml[x].get('FailReason')
#                             if a1 !=None:
#                                 #print a1
#                                 StackTrace=doc.createElement('StackTrace')
#                                 testR=doc.createTextNode(a1[0])
#                                 StackTrace.appendChild(testR)
#                                 FailedScene.appendChild(StackTrace)
#                                 TestCase.appendChild(Test)
#                     else:
#                         pass
#
#             TestSuite.appendChild(TestCase)
#
#             TestPackage.appendChild(TestSuite)
#
#             Result.appendChild(TestPackage)
#
#         #f = open('C:\\Users\\c_youwu\\Desktop\\result\\testResult.xml','w')
#
#         f = open('%s\\%s\\testResult.xml' % (QGP_Path().PATH_RESULTS,Start_Time) , 'w')
#         f.write(doc.toprettyxml(indent = '',encoding='utf-8'))
#         f.close()
#
#         self.coverFiles(QGP_Path().PATH_DOCS,'%s\%s' % (QGP_Path().PATH_RESULTS,Start_Time))
#
#     def coverFiles(self,sourceDir,targetDir):
#         for file in os.listdir(sourceDir):
#             sourceFile = os.path.join(sourceDir,  file)
#             targetFile = os.path.join(targetDir,  file)
#             if os.path.isfile(sourceFile):
#                 open(targetFile, "wb").write(open(sourceFile, "rb").read())



if __name__ == "__main__":
    app = wx.App()
    f = Frame()
    f.Show()
    app.MainLoop()


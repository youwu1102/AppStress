#-*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.dom.minidom import Document
import wx.lib.agw.customtreectrl as CT
import datetime,wx,threading,commands,subprocess,shutil
import xml.dom.minidom



#写入默认路径地址
class QGP_Path():
    def __init__(self):
        LOCATION = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '..'))
        self.PATH_TESTCASES = '%s\\repository\\testcases' %LOCATION
        self.PATH_JAVA_JAR = 'C:\\QGPAutomationV2.0.0_BASIC\\resource\\UiRobotium'
        self.PATH_JAVA_CLASS = os.path.join(self.PATH_JAVA_JAR,'src')
        self.PATH_TEMPLATE = os.path.join(self.PATH_JAVA_CLASS,'template','Template.java')
        self.NAME_JAVA_JAR = 'wuyou'
        self.NUMBER_ANDROID_ID = '10'
        self.PATH_LOGS = '%s\\repository\\logs' %LOCATION
        self.PATH_RESULTS = '%s\\repository\\results' %LOCATION
        self.PATH_DOCS='%s\\docs' %LOCATION
        self.PATH_PLANS ='%s\\repository\\plans' %LOCATION
        self.PATH_ANT = '%s\\resource\\apache-ant-1.9.4\\bin' %LOCATION

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.AppendText(string)

#构造可视化的图形界面
class Frame(wx.Frame):
    def __init__(self):
        QGP = QGP_Path()
        DEV = DevicesList()
        TREE = TestCaseTree()
        wx.Frame.__init__(self, None, -1, title="UiAutomator",size = (1000,600))
        self.Center()
        self.panel = wx.Panel(self, -1)


        self.Main_Box = wx.BoxSizer( wx.HORIZONTAL)#整个界面，水平布局
        self.Left_Box = wx.BoxSizer( wx.VERTICAL)#左边界面，主要放置 Tree和PLAN的导入导出
        self.Right_Box = wx.BoxSizer( wx.VERTICAL)#右边界面，主要放置 文本输出和基本按键


        #左边界面模块开始
        #---------树模块开始
        self.TestCase_TREE = CT.CustomTreeCtrl(self.panel,agwStyle=wx.TR_DEFAULT_STYLE|CT.TR_AUTO_CHECK_PARENT|CT.TR_AUTO_CHECK_CHILD)
        self.TestCase_TREE_ROOT = self.TestCase_TREE.AddRoot('TestCase')
        self.TestCase_TREE_ROOT.Expand()


        TREE.showTestCase(self.TestCase_TREE,self.TestCase_TREE_ROOT,QGP.PATH_TESTCASES)
        #---------树模块结束
        self.Left_Above_Box = wx.BoxSizer( wx.HORIZONTAL)#左下界面，import和outport
        #---------左下界面模块开始

        self.Import_Button = wx.Button(self.panel,-1,'Import',size=(-1,50))#导入XML按钮
        self.Bind(wx.EVT_BUTTON, self.OnImport, self.Import_Button)
        self.Export_Button = wx.Button(self.panel,-1,'Export',size=(-1,50))#导出选项到XML按钮
        self.Bind(wx.EVT_BUTTON, self.OnExport, self.Export_Button)

        self.Left_Above_Box.Add(self.Import_Button,1,wx.EXPAND)
        self.Left_Above_Box.Add(self.Export_Button,1,wx.EXPAND)

        #---------左下界面模块结束
        self.Left_Box.Add(self.TestCase_TREE,1,wx.EXPAND)
        self.Left_Box.Add(self.Left_Above_Box,0,wx.EXPAND)


        #左边界面模块结束

        #右边界面模块开始
        #------------文本显示模块开始
        self.multiText = wx.TextCtrl(self.panel, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText.SetInsertionPointEnd()
        self.redir=RedirectText(self.multiText)
        sys.stdout=self.redir
        #------------文本显示模块结束
        self.Right_Above_Box = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，主要包含 Devicelist 和StartButton
        self.Right_Above_Box_VERTICAL = wx.BoxSizer( wx.VERTICAL)#右下BUTTONBOX，垂直布局，主要包含 下面两个水平布局框架
        self.Right_Above_Box_HORIZONTAL_1 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Start和Stop
        self.Right_Above_Box_HORIZONTAL_2 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Report和空白
        #------------右下显示模块开始

        DEV.getDevicesList()
        self.Device_Box = wx.RadioBox(self.panel, -1, "Device", wx.DefaultPosition,wx.DefaultSize,DEV.devices_List, 1, wx.RA_SPECIFY_COLS)#显示设备列表
        self.Bind(wx.EVT_RADIOBOX, self.OnChoice, self.Device_Box)
        global serial_number
        serial_number = self.Device_Box.GetItemLabel(self.Device_Box.Selection)

        self.Start_Button = wx.Button(self.panel,-1,'START',size=(-1,40))#开始运行
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.Start_Button)
        self.Result_Button = wx.Button(self.panel,-1,'RESULT',size=(-1,40))#打开报告
        self.Bind(wx.EVT_BUTTON, self.OnResult, self.Result_Button)
        self.Stop_Button = wx.Button(self.panel,-1,'STOP',size=(-1,40))#停止运行

        self.Refresh_Button = wx.Button(self.panel,-1,'REFRESH',size=(-1,40))#重新加载页面
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.Refresh_Button)

        self.Right_Above_Box_HORIZONTAL_1.Add(self.Start_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_1.Add(self.Stop_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Result_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Refresh_Button,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_1,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_2,1,wx.EXPAND)
        self.Right_Above_Box.Add(self.Device_Box,3,wx.EXPAND)
        self.Right_Above_Box.Add(self.Right_Above_Box_VERTICAL,7,wx.EXPAND|wx.TOP,5)


        #------------右下显示模块结束
        self.Right_Box.Add(self.multiText,1,wx.EXPAND)
        self.Right_Box.Add(self.Right_Above_Box,0,wx.EXPAND)
        #右边界面模块结束


        self.Main_Box.Add(self.Left_Box,3,wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM,5)
        self.Main_Box.Add(self.Right_Box,7,wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.BOTTOM,5)
        self.panel.SetSizer(self.Main_Box)

    def OnChoice(self,event):
        if self.Device_Box.GetItemLabel(self.Device_Box.Selection) == 'No Device':
            self.Start_Button.Disable()
        else:
            self.Start_Button.Enable()

    def OnRefresh(self,event):
        TREE = TestCaseTree()
        self.TestCase_TREE_ROOT.DeleteChildren(self.TestCase_TREE)
        TREE.showTestCase(self.TestCase_TREE,self.TestCase_TREE_ROOT,QGP_Path().PATH_TESTCASES)
        self.TestCase_TREE_ROOT.Expand()



    planName = 'testplan'
    def OnStart(self,event):
        TREE = TestCaseTree()
        Main=MainTest()
        serial_number = self.Device_Box.GetItemLabel(self.Device_Box.Selection)
        if TREE.getTreeSelect(self.TestCase_TREE) == []:
            print 'Please select some test case'
        else:
            self.getPLANwirteJAVA(self.planName)
            Thread_Test = threading.Thread(target=Main.main)
            Thread_Test.start()
        self.planName='testplan'

    def OnExport(self,event):
        QGP=QGP_Path()
        TREE = TestCaseTree()
        PLAN = TestCasePlan()
        if TREE.getTreeSelect(self.TestCase_TREE) != []:
            dlg = wx.FileDialog(self,
                                message="Save Test Plan",
                                wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
                                defaultDir=QGP.PATH_PLANS,
                                style=wx.SAVE
                                )
            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                for path in paths:
                    plan_name = path[len(QGP.PATH_PLANS)+1:-4]
                    file_name = path
                DOC=PLAN.establishTestPlan(TREE.getTreeSelect(self.TestCase_TREE),TestPlanName=plan_name)
                file=open(file_name,'w')
                file.write(DOC.toprettyxml(indent = '',encoding='utf-8'))
                file.close()
            dlg.Destroy()
        else:
            print 'Please select some Test Case'

    def OnImport(self,event):
        QGP=QGP_Path()
        TREE = TestCaseTree()
        PLAN = TestCasePlan()
        dlg = wx.FileDialog(self,
                            message="Select Test Plan",
                            wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
                            defaultDir=QGP.PATH_PLANS,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            filename=""
            paths = dlg.GetPaths()
            for path in paths:
                filename=filename+path
        dlg.Destroy()
        aaa = filename[len(QGP.PATH_PLANS)+1:-4]

        TREE=TestCaseTree()
        TREE.setTreeSelect(self.TestCase_TREE,aaa)




    def OnResult(self,event):
        os.system('start %s' % QGP_Path().PATH_RESULTS)



    def getPLANwirteJAVA(self,planName):
        TREE = TestCaseTree()
        PLAN = TestCasePlan()
        QGP = QGP_Path()
        WR=writeTestCase()
        DOC = PLAN.establishTestPlan(TREE.getTreeSelect(self.TestCase_TREE))#根据树选择建立以个testplan的XML文档
        XML = open('%s\\%s.xml'% (QGP.PATH_PLANS,'testplan'),'w')#打开一个文档 名字为TESTPLAN
        XML.write(DOC.toprettyxml(indent = '',encoding='utf-8'))#写入DOC
        XML.close()
        testplan=PLAN.readTestPlan(planName)#获取Plan得到的值
        WR.writeToJAVA(testplan)
class CreatDir():
    def __init__(self):
        pass
    def creatDir(self,name):
        os.mkdir('%s\%s' %(QGP_Path().PATH_RESULTS,name))
        os.makedirs('%s\%s\Device' %(QGP_Path().PATH_LOGS,name))
        os.makedirs('%s\%s\Host' %(QGP_Path().PATH_LOGS,name))


#获取手机信息
class ADB_getValue():
    def __init__(self):
        # wuyou:以下参数均可以自己定义增加修改
        self.product_Model = self.getValue('ro.product.model', serial_number)
        self.product_Name = self.getValue('ro.product.name', serial_number)
        self.build_Fingerprint = self.getValue('ro.build.fingerprint', serial_number)
        self.version_AU = self.getValue('ro.build.au_rev', serial_number)
        self.version_Meta = self.getValue('gsm.version.baseband', serial_number)
        self.version_SDK = self.getValue('ro.build.version.sdk', serial_number)
        self.version_Release = self.getValue('ro.build.version.release', serial_number)


    def assignmentValue(self,serial_number):
        #对参数赋值
        self.product_Model = self.getValue('ro.product.model', serial_number)
        self.product_Name = self.getValue('ro.product.name', serial_number)
        self.build_Fingerprint = self.getValue('ro.build.fingerprint', serial_number)
        self.version_AU = self.getValue('ro.build.au_rev', serial_number)
        self.version_Meta = self.getValue('gsm.version.baseband', serial_number)
        self.version_SDK = self.getValue('ro.build.version.sdk', serial_number)
        self.version_Release = self.getValue('ro.build.version.release', serial_number)

    def getValue(self, cmd, serialno):
        #格式化输入输出
        return os.popen('adb -s %s shell getprop %s' % (serialno,cmd)).read().strip('\r\n')

#获取连接的所有手机的serialno
class DevicesList():
    #默认配置均为No Device
    def __init__(self):
        self.devices_List = ['No Device', 'No Device', 'No Device', 'No Device']
    #获取连接的手机的serialno
    def getDevicesList(self):
        list=[]
        devices  = subprocess.Popen ('adb devices', stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
        for line in iter(devices.stdout.readline, ''):
            if 'device' in line:
                if 'List of devices attached' in line:
                    pass
                else:
                    list.append(line.strip('\r\n')[:-7])
            elif 'offline' in line:
                pass
            elif 'unauthorized' in line:
                pass
            else:
                pass
        for x in range(len(list)):
            self.devices_List[x]=list[x]

#左侧树构造
class TestCaseTree():

    def __init__(self):
        pass

    def showTestCase(self,Tree,ParenNode,Path):
        display = False
        files_Package = os.listdir(Path)
        for testPackage in files_Package:
            if os.path.isdir(os.path.join(Path, testPackage)):
                folder_Package = Tree.AppendItem(ParenNode,testPackage,1)
                files_Class = os.listdir(os.path.join(Path, testPackage))
                for testClass in files_Class:
                    if os.path.isdir(os.path.join(Path, testPackage,testClass)):
                        folder_Class = Tree.AppendItem(folder_Package,testClass,1)
                        files_Case = os.listdir(os.path.join(Path, testPackage,testClass))
                        for testCase in files_Case:
                            if os.path.isdir(os.path.join(Path, testPackage,testClass,testCase)):
                                pass
                            else:
                                if testCase[-4:] == '.txt':
                                    Tree.AppendItem(folder_Class,testCase,1)
                                else:
                                    if display == True:
                                        Tree.AppendItem(folder_Class,testCase,0)
                    else:
                        if display == True:
                           Tree.AppendItem(folder_Package,testClass,0)
            else:
                if display == True:
                    Tree.AppendItem(ParenNode,testPackage,0)

    def getTreeSelect(self,Tree):
        TestCase=[]
        treeRoot = Tree.GetRootItem()
        (item,cookie) = Tree.GetFirstChild(treeRoot)
        for x in range(Tree.GetChildrenCount(treeRoot)):
            if Tree.GetItemText(item)[-4:] == '.txt':
                TestSuite=self.getSelectCasePath(item,Tree)
                if TestSuite != []:
                    TestCase.append(TestSuite)
            item=Tree.GetNext(item)
        return TestCase

    def getSelectCasePath(self,item,Tree):
        path=[]
        if Tree.IsItemChecked(item):
            while Tree.GetItemParent(item):
                path.append(Tree.GetItemText(item))
                item=Tree.GetItemParent(item)
        path.reverse()
        return path
    def setTreeSelect(self,Tree,testplan):
        PLAN = TestCasePlan()
        treeRoot = Tree.GetRootItem()
        plan=PLAN.readTestPlan(testplan)
        (all,cookie) = Tree.GetFirstChild(treeRoot)
        Tree.CheckItem(all,False)
        for path in plan:
            array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
            (testPackage,cookie) = Tree.GetFirstChild(treeRoot)

            for num_package in range(Tree.GetChildrenCount(treeRoot,False)):
                if Tree.GetItemText(testPackage) == array_path[0]:
                    #print Tree.GetItemText(testPackage)
                    (testClass,cookie) = Tree.GetFirstChild(testPackage)
                    for num_class in range(Tree.GetChildrenCount(testPackage,False)):
                        if Tree.GetItemText(testClass) == array_path[1]:
                            #print Tree.GetItemText(testClass)
                            (testCase,cookie) = Tree.GetFirstChild(testClass)
                            for num_case in range(Tree.GetChildrenCount(testClass,False)):
                                if Tree.GetItemText(testCase) == array_path[2]:
                                    #print Tree.GetItemText(testCase)
                                    Tree.CheckItem(testCase)
                                    Tree.Expand(testClass)
                                    Tree.Expand(testPackage)
                                    break
                                else:
                                    (testCase,cookie) = Tree.GetNextChild(testClass,cookie)
                            break
                        else:
                            (testClass,cookie) = Tree.GetNextChild(testPackage,cookie)
                    break
                else:
                    (testPackage,cookie) = Tree.GetNextChild(treeRoot,cookie)



class TestCasePlan():
    QGP=QGP_Path()
    def __init__(self):
        pass
    def establishTestPlan(self,TestCase,TestPlanName = 'testplan'):
        doc = Document()
        if TestCase==[]:
            print "Please select some Test Case"
        else:
            PREVIOUS_PACKAGE_NAME=''
            PREVIOUS_CLASS_NAME=''
            testPlan = doc.createElement('TestPlan')
            testPlan.setAttribute('name',TestPlanName)
            for x in range(len(TestCase)):
                if TestCase[x][0] != PREVIOUS_PACKAGE_NAME:
                    testPackage=doc.createElement('TestPackage')
                    testPackage.setAttribute('name',TestCase[x][0])
                    PREVIOUS_PACKAGE_NAME=testPackage.getAttribute('name')
                    testClass=doc.createElement('TestClass')
                    testClass.setAttribute('name',TestCase[x][1])
                    PREVIOUS_CLASS_NAME=TestCase[x][1]
                    testCase=doc.createElement('TestCase')
                    testCase.setAttribute('name',TestCase[x][2])
                    testClass.appendChild(testCase)
                    testPackage.appendChild(testClass)
                    testPlan.appendChild(testPackage)
                else:
                    if TestCase[x][1] != PREVIOUS_CLASS_NAME:
                        testClass=doc.createElement('TestClass')
                        testClass.setAttribute('name',TestCase[x][1])
                        PREVIOUS_CLASS_NAME=TestCase[x][1]
                        testCase=doc.createElement('TestCase')
                        testCase.setAttribute('name',TestCase[x][2])
                        testClass.appendChild(testCase)
                        testPackage.appendChild(testClass)
                    else:
                        testCase=doc.createElement('TestCase')
                        testCase.setAttribute('name',TestCase[x][2])
                        testClass.appendChild(testCase)
            doc.appendChild(testPlan)
            # f = open('%s\\%s.xml'% (QGP.PATH_PLANS,TestPlanName),'w')
            # f.write(doc.toprettyxml(indent = '',encoding='utf-8'))
            # f.close()
            return doc

    def readTestPlan(self,TestPlanName = 'testplan'):
        testPlanList=[]
        QGP=QGP_Path()
        dom = xml.dom.minidom.parse('%s\\%s.xml'% (QGP.PATH_PLANS,TestPlanName))
        root = dom.documentElement
        TestPackageList = root.getElementsByTagName('TestPackage')
        for x in range(len(TestPackageList)):
            TestPackage=TestPackageList[x]
            TestClassList=TestPackage.getElementsByTagName('TestClass')
            for y in range(len(TestClassList)):
                TestClass=TestClassList[y]
                TestCaseList = TestClass.getElementsByTagName('TestCase')
                for z in range(len(TestCaseList)):
                    TestCase=TestCaseList[z]
                    PATH =  '%s\\%s\\%s\\%s' %(QGP.PATH_TESTCASES,TestPackage.getAttribute('name'),TestClass.getAttribute('name'),TestCase.getAttribute('name'))
                    testPlanList.append(PATH)
        return testPlanList
class writeTestCase:
    def __init__(self):
        pass
    def writeToJAVA(self,TestCaseList):
        QGP=QGP_Path()
        PATH=QGP_Path().PATH_TESTCASES
        PATH_JAVA_CLASS=QGP_Path().PATH_JAVA_CLASS
        files_Package = os.listdir(PATH)
        for testPackage in files_Package:
            if os.path.isdir(os.path.join(PATH, testPackage)):
                #print testPackage
                if testPackage not in os.listdir(PATH_JAVA_CLASS):
                    os.mkdir('%s\\%s' %(PATH_JAVA_CLASS,testPackage))
                files_Class= os.listdir(os.path.join(PATH, testPackage))
                for testClass in files_Class:
                    if os.path.isdir(os.path.join(PATH, testPackage,testClass)):
                        TestClass=open('%s\\%s\\%s.java'%(PATH_JAVA_CLASS,testPackage,testClass.replace('-','')),'w')
                        Template=open(QGP_Path().PATH_TEMPLATE,'r')
                        for line in Template:
                            if 'package Template;' in line:
                                TestClass.writelines('package %s;\r\n' %testPackage)
                            elif 'public class Template extends UiAutomatorTestCase' in line:
                                TestClass.writelines('public class %s extends UiAutomatorTestCase\r\n' %testClass.replace('-',''))
                            elif ('//start' in line):
                                for files_Case in TestCaseList:
                                    a=files_Case[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')
                                    if a[0]==testPackage and a[1]==testClass:
                                        Case=open(files_Case,'r')
                                        TestClass.writelines('    public void test%s() throws UiObjectNotFoundException\r' % a[2][:-4].replace('-',''))
                                        TestClass.writelines('    {\r')
                                        for l in Case:
                                            TestClass.writelines('       '+l.strip('	').strip('﻿'))
                                        TestClass.writelines('    }\r')
                                        TestClass.writelines('\r\n')
                                        Case.close

                            else:
                                TestClass.writelines(line)
                        Template.close()
                        TestClass.close()


#先把所有的初始文件写成模板
    def writeDefault(self):
        PATH=QGP_Path().PATH_TESTCASES
        PATH_JAVA_CLASS=QGP_Path().PATH_JAVA_CLASS
        files_Package = os.listdir(PATH)
        for testPackage in files_Package:
            if os.path.isdir(os.path.join(PATH, testPackage)):
                #print testPackage
                if testPackage not in os.listdir(PATH_JAVA_CLASS):
                    os.mkdir('%s\\%s' %(PATH_JAVA_CLASS,testPackage))
                files_Class= os.listdir(os.path.join(PATH, testPackage))
                for testClass in files_Class:
                    if os.path.isdir(os.path.join(PATH, testPackage,testClass)):
                        TestClass=open('%s\\%s\\%s.java'%(PATH_JAVA_CLASS,testPackage,testClass.replace('-','')),'w')
                        Template=open(QGP_Path().PATH_TEMPLATE,'r')
                        for line in Template:
                            if 'package Template;' in line:
                                TestClass.writelines('package %s;\r\n' %testPackage)
                            elif 'public class Template extends UiAutomatorTestCase' in line:
                                TestClass.writelines('public class %s extends UiAutomatorTestCase\r\n' %testClass.replace('-',''))
                            else:
                                TestClass.writelines(line)
                        Template.close()
                        TestClass.close()
class MainTest():
    def buildJAR(self):
        self.buildPass=False
        print os.popen('android create uitest-project -n %s -t %s -p %s' % (QGP_Path().NAME_JAVA_JAR,
                                                                            QGP_Path().NUMBER_ANDROID_ID,
                                                                            QGP_Path().PATH_JAVA_JAR)).read()

        #os.system('cd %s\\' %QGP_Path().PATH_ANT)
        data  = subprocess.Popen ('ant build -buildfile %s//build.xml' % QGP_Path().PATH_JAVA_JAR, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell = True)
        for line in iter(data.stdout.readline, ''):
            time.sleep(0.1)
            if 'BUILD SUCCESSFUL' in line:
                self.buildPass=True
            print line.strip('\r\n')


    def getClass(self):
        PLAN=TestCasePlan().readTestPlan('testplan')
        CLASS=[]
        for path in PLAN:
            array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
            if array_path[1] not in CLASS:
                CLASS.append(array_path[1])
        #print CLASS
        return CLASS
    def getPackage(self):
        PLAN=TestCasePlan().readTestPlan('testplan')
        PACKAGE=[]
        for path in PLAN:
            array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
            if array_path[0] not in PACKAGE:
                PACKAGE.append(array_path[0])
        #print PACKAGE
        return PACKAGE

    def runTest(self,StartTime):
        os.system('adb -s %s push %s\\bin\\%s.jar data/local/tmp' % (serial_number,QGP_Path().PATH_JAVA_JAR,QGP_Path().NAME_JAVA_JAR))
        TestClass=self.getClass()
        TestPackage=self.getPackage()
        t=TimeFormat()
        Part=[]
        out=outputFormat()
        out.setValue2Zero()
        out.PackageStartFormat(TestPackage[0])
        if len(TestClass)==1:
            self.class_now=TestClass[0]
            f = open('%s\%s\Host\%s.txt' %(QGP_Path().PATH_LOGS,StartTime,TestClass[0]),'w')
            f.write('StartTime=%s\r\n' %t.getTime())
            cmd = 'adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,TestPackage[0],TestClass[0].replace('-',''))
            #print cmd
            dataRun = subprocess.Popen (cmd , stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
            Thread_Log=threading.Thread(target=self.LogThread)
            Thread_Log.start()
            out.ClassStartFormat(TestClass[0])
            out.setClassValue2Zero()
            for line in iter(dataRun.stdout.readline, ''):
                f.writelines(line)
                Part.append(line)
                if 'INSTRUMENTATION_STATUS_CODE:' in line:
                    out.lineFormat(Part)
                    Part=[]

            out.ClassEndFormat(TestClass[0])
            f.write('EndTime=%s\r\n'  %t.getTime())
            f.close()
            out.PackageEndFormat(TestPackage[0])
        else:
            for Class in TestClass:
                os.system('adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,'ChangeCountry',Class.replace('-','')))
                # for x in range(20):
                #     print x
                #     time.sleep(10)
                self.class_now=Class
                os.system('adb -s %s push %s\\bin\\%s.jar data/local/tmp' % (serial_number,QGP_Path().PATH_JAVA_JAR,QGP_Path().NAME_JAVA_JAR))
                Thread_Log=threading.Thread(target=self.LogThread)
                Thread_Log.start()
                f = open('%s\%s\Host\%s.txt' %(QGP_Path().PATH_LOGS,StartTime,Class),'w')
                f.write('StartTime=%s\r\n' %t.getTime())
                dataRun = subprocess.Popen ('adb -s %s shell uiautomator runtest %s.jar -c %s.%s' % (serial_number,QGP_Path().NAME_JAVA_JAR,TestPackage[0],Class.replace('-','')), stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
                out.ClassStartFormat(Class)
                out.setClassValue2Zero()
                for line in iter(dataRun.stdout.readline, ''):
                    f.writelines(line)
                    Part.append(line)
                    if 'INSTRUMENTATION_STATUS_CODE:' in line:
                        out.lineFormat(Part)
                        Part=[]

                out.ClassEndFormat(Class)
                f.write('EndTime=%s\r\n'  %t.getTime())
                f.close()
                #time.sleep(180)
            out.PackageEndFormat(TestPackage[0])

    def LogThread(self):
        os.system('adb -s %s logcat -v time >%s/%s/Device/%s_logcat.txt' %(serial_number,QGP_Path().PATH_LOGS,self.start_time,self.class_now))

    def main(self):
        self.buildJAR()
        if self.buildPass==True:
            t=TimeFormat()
            self.start_time=t.getTime()
            CreatDir().creatDir(self.start_time)


            self.runTest(self.start_time)
            res=Result()
            #wuyou
            logPart=res.dLogPart(self.start_time)
            self.logforXml=[]
            for x in range(len(logPart)):
                self.logforXml.append(res.dicTest(logPart[x]))
            res.xml(self.logforXml,self.start_time)
            out = outputFormat()
            out.End()

            #os.system('adb -s %s  reboot' % serial_number)

        else:
            print 'please check the information'
class outputFormat():
    def __init__(self):
        pass
    def setValue2Zero(self):
        self.newCaseFlag = False
        self.classPass=0
        self.classFail=0
        self.packagePass=0
        self.packageFail=0
    def setClassValue2Zero(self):
        self.newCaseFlag = False
        self.classPass=0
        self.classFail=0

    def dicPart(self,logPart):
        test={}
        a=[]
        for x in range(len(logPart)):
            if 'INSTRUMENTATION_STATUS: test' in logPart[x]:
                test['test']=logPart[x][29:].strip('\r\n')
            elif  'INSTRUMENTATION_STATUS: stack' in logPart[x]:
                test['stack']=logPart[x][30:].strip('\r\n')
                for y in range(len(logPart)-x-1):
                    if '	at' in logPart[y+x+1]:
                        a.append(logPart[y+x+1].strip('\t'))
                    else:
                        break
                test['FailReason']=a
            elif  'INSTRUMENTATION_STATUS_CODE:' in logPart[x]:
                test['CODE']=logPart[x][29:].strip('\r\n')
        return test

    def lineFormat(self,Part):
        t=TimeFormat()
        DirPart=self.dicPart(Part)
        if len(DirPart)==1:
            pass
        else:
            if DirPart.get('CODE') == '1':
                pass
            elif DirPart.get('CODE') == '0':
                print '%s /%s:  %s      ---pass' %(t.getLogResultTime(),serial_number,DirPart.get('test')[4:])
                self.classPass+=1
                self.packagePass+=1

            elif DirPart.get('CODE') == '-1'or DirPart.get('CODE') == '-2':
                print '%s /%s:  %s      ---fail' %(t.getLogResultTime(),serial_number,DirPart.get('test')[4:])
                print '***FailReason:  %s' %DirPart.get('stack')
                FailReason=DirPart.get('FailReason')
                for reason in FailReason:
                    time.sleep(0.1)
                    print '******%s' %reason.strip('\r\r\n')
                self.classFail+=1
                self.packageFail+=1
        # if 'INSTRUMENTATION_STATUS: test' in line:
        #     self.testCase=line[33:].strip('\r\n')
        #     self.newCaseFlag=True
        # elif 'INSTRUMENTATION_STATUS_CODE: 1' in line:
        #     pass
        # elif 'INSTRUMENTATION_STATUS_CODE: 0' in line and self.newCaseFlag==True:
        #     print '%s /%s:  %s: Pass' %(t.getLogResultTime(),serial_number,self.testCase)
        #     self.newCaseFlag=False
        #     self.classPass+=1
        #     self.packagePass+=1
        # elif 'INSTRUMENTATION_STATUS_CODE: -2' in line and self.newCaseFlag==True:
        #     print '%s /%s:  %s: Fail' %(t.getLogResultTime(),serial_number,self.testCase)
        #     self.newCaseFlag=False
        #     self.classFail+=1
        #     self.packageFail+=1
        #
        # elif 'INSTRUMENTATION_STATUS_CODE: -1' in line and self.newCaseFlag==True:
        #     print '%s /%s:  %s: Fail' %(t.getLogResultTime(),serial_number,self.testCase)
        #     self.newCaseFlag=False
        #     self.classFail+=1
        #     self.packageFail+=1

    def PackageStartFormat(self,packageName):
        t=TimeFormat()
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------' %(t.getLogResultTime(),serial_number)
        time.sleep(0.3)
        print '%s /%s:  Test package %s started' %(t.getLogResultTime(),serial_number,packageName)

    def ClassStartFormat(self,className):
        t=TimeFormat()
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)
        time.sleep(0.3)
        print '%s /%s:  Test class %s started' %(t.getLogResultTime(),serial_number,className)
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)
    def ClassEndFormat(self,className):
        t=TimeFormat()
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)
        time.sleep(0.3)
        print '%s /%s:  %s class complete: Passed %s, Failed %s'%(t.getLogResultTime(),serial_number,className,self.classPass,self.classFail)


    def PackageEndFormat(self,packageName):
        t=TimeFormat()
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)
        time.sleep(0.3)
        print '%s /%s:  %s package complete: Passed %s, Failed %s' %(t.getLogResultTime(),serial_number,packageName,self.packagePass,self.packageFail)
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)
    def End(self):
        t=TimeFormat()
        time.sleep(0.3)
        print '%s /%s:  All tests have been completed.Please check the test report' %(t.getLogResultTime(),serial_number)
        time.sleep(0.3)
        print '%s /%s:  -----------------------------------------------------------------------------'%(t.getLogResultTime(),serial_number)

class TimeFormat():
    def __init__(self):
        pass
    def getTime(self):
        Time_Format = time.strftime('%Y.%m.%d_%H.%M.%S',time.localtime(time.time()))
        return Time_Format

    def getDataTime(self):
        DATA=datetime.datetime.now()
        DATA_Format = DATA.strftime('%a %b %d %H:%M:%S %Y')
        return DATA_Format
    def getLogResultTime(self):
        ResultTime_Format = time.strftime('%m-%d  %H:%M:%S',time.localtime(time.time()))
        return ResultTime_Format

class Result():
    def __init__(self):
        pass
    def dicTest(self,logPart):
        test={}
        a=[]
        for x in range(len(logPart)):
            if 'INSTRUMENTATION_STATUS: id'in logPart[x]:
                test['id']=logPart[x][27:].strip('\r\n')
            elif 'INSTRUMENTATION_STATUS: test' in logPart[x]:
                test['test']=logPart[x][29:].strip('\r\n')
            elif 'INSTRUMENTATION_STATUS: numtests' in logPart[x]:
                test['numtests']=logPart[x][33:].strip('\r\n')
            elif  'INSTRUMENTATION_STATUS: stream' in logPart[x]:
                test['stream']=logPart[x][31:].strip('\r\n')
            elif  'INSTRUMENTATION_STATUS: class' in logPart[x]:
                test['class']=logPart[x][30:].strip('\r\n')
            elif  'INSTRUMENTATION_STATUS: stack' in logPart[x]:
                test['stack']=logPart[x][30:].strip('\r\n')
                for y in range(len(logPart)-x-1):
                    if '	at' in logPart[y+x+1]:
                        a.append(logPart[y+x+1].strip('\t'))
                    else:
                        break
                test['FailReason']=a

            elif  'INSTRUMENTATION_STATUS_CODE:' in logPart[x]:
                test['CODE']=logPart[x][29:].strip('\r\n')
        return test


    result=[]
    def getResult(self,Start_Time):
        self.result=[]
        result_path='%s\%s\Host' %(QGP_Path().PATH_LOGS,Start_Time)
        #result_path='%s\%s\Host' %(LOG_PATH,'2015.05.26_17.00.10')
        list=os.listdir(result_path)
        for file in list:
            if file[-4:] == '.txt':
                self.result.append(file)
        return self.result



    def dLogPart(self,Start_Time):
        files = self.getResult(Start_Time)
        ALL=[]
        Part=[]
        for log in files:
            file = open('%s\%s\Host\%s' %(QGP_Path().PATH_LOGS,Start_Time,log),'r')
        #file = open('%s\%s\Host\%s.txt' %(LOG_PATH,'2015.05.26_17.00.10','ForExample'),'r')

            for line in file:
                if 'INSTRUMENTATION_STATUS_CODE:' in line:
                    Part.append(line)
                    ALL.append(Part)
                    Part=[]
                elif 'EndTime=' in line:
                    if self.EndTime < line[8:]:
                        self.EndTime=line[8:].strip('\r\n')
                elif 'StartTime=' in line:
                    if self.StartTime > line[10:]:
                        self.StartTime=line[10:].strip('\r\n')


                Part.append(line)
            file.close()

        return ALL
    StartTime='9999999999999'
    EndTime=''
    def getCurrentlTime(self):
        DATA=datetime.datetime.now()
        DATA_Format = DATA.strftime('%a %b %d %H:%M:%S %Y')
        return DATA_Format

    def xml(self,log4xml,Start_Time):
        Total,Pass,Fail=0,0,-len(self.result)
        for x in range(len(log4xml)):
            if log4xml[x].get('CODE') == '1':
                Total+=1
            elif log4xml[x].get('CODE') == '0':
                Pass+=1
            elif log4xml[x].get('CODE') == '-2' or log4xml[x].get('CODE') == '-1':
                Fail+=1

        testPlan = 'wait for write'

        Hosename=os.popen('Hostname').read()



        doc = Document()
        abc = doc.createProcessingInstruction("xml-stylesheet","type=\"text/xsl\" href=\"cts_result.xsl\"")
        doc.appendChild(abc)
        Result = doc.createElement('TestResult')
        Result.setAttribute('testPlan', testPlan)
        Result.setAttribute('starttime', self.StartTime)
        Result.setAttribute('endtime', self.EndTime)
        Result.setAttribute('suite', 'QGP_Automation')
        doc.appendChild(Result)



        DeviceInfo = doc.createElement('DeviceInfo')

        Result.appendChild(DeviceInfo)
        BuildInfo =doc.createElement('BuildInfo')
        BuildInfo.setAttribute('productName', ADB_getValue().product_Name)
        BuildInfo.setAttribute('productModel', ADB_getValue().product_Model)
        BuildInfo.setAttribute('deviceID', serial_number)
        BuildInfo.setAttribute('AUVersion', ADB_getValue().version_AU)
        BuildInfo.setAttribute('METAVersion', ADB_getValue().version_Meta)
        BuildInfo.setAttribute('AndroidVersion', ADB_getValue().version_Release)
        BuildInfo.setAttribute('AndroidAPILevel', ADB_getValue().version_SDK)


        DeviceInfo.appendChild(BuildInfo)
        HostInfo =doc.createElement('HostInfo')
        HostInfo.setAttribute('name', Hosename)
        HostInfo.setAttribute('osversion', 'wait for write')
        HostInfo.setAttribute('osname', 'wait for write')
        Result.appendChild(HostInfo)
        Summary=doc.createElement('Summary')
        Summary.setAttribute('total',str(Total))
        Summary.setAttribute('pass',str(Pass))
        Summary.setAttribute('failed',str(Fail))
        Result.appendChild(Summary)
        for y in range(len(self.result)):
            TestPackage=doc.createElement('TestPackage')
            TestPackage.setAttribute('name',self.result[y][:-4])
            aaa=self.result[y][:-4].replace('-','')
            TestPackage.setAttribute('appPackageName',self.result[y][:-4])#wuyou
            TestSuite=doc.createElement('TestSuite')
            TestCase =doc.createElement('TestCase')
            for x in range(len(log4xml)):
                CLASS = log4xml[x].get('class')
                if CLASS !=None:
                    className=CLASS.split('.')
                    if className[1]==aaa:

                        if log4xml[x].get('CODE') == '1':
                            pass
                        elif log4xml[x].get('CODE') == '-1':
                            Test=doc.createElement('Test')
                            Test.setAttribute('name',log4xml[x].get('test'))
                            Test.setAttribute('result','fail')
                            FailedScene=doc.createElement('FailedScene')
                            FailedScene.setAttribute('message',log4xml[x].get('stack'))
                            Test.appendChild(FailedScene)
                            a1=log4xml[x].get('FailReason')
                            if a1 !=None:
                                StackTrace=doc.createElement('StackTrace')
                                testR=doc.createTextNode(a1[0])
                                StackTrace.appendChild(testR)
                                FailedScene.appendChild(StackTrace)
                                TestCase.appendChild(Test)
                        elif log4xml[x].get('CODE') == '0':
                            Test=doc.createElement('Test')
                            Test.setAttribute('name',log4xml[x].get('test'))
                            Test.setAttribute('result','pass')
                            TestCase.appendChild(Test)
                        elif log4xml[x].get('CODE') == '-2':
                            Test=doc.createElement('Test')
                            Test.setAttribute('name',log4xml[x].get('test'))
                            Test.setAttribute('result','fail')
                            FailedScene=doc.createElement('FailedScene')
                            FailedScene.setAttribute('message',log4xml[x].get('stack'))
                            Test.appendChild(FailedScene)
                            a1=log4xml[x].get('FailReason')
                            if a1 !=None:
                                #print a1
                                StackTrace=doc.createElement('StackTrace')
                                testR=doc.createTextNode(a1[0])
                                StackTrace.appendChild(testR)
                                FailedScene.appendChild(StackTrace)
                                TestCase.appendChild(Test)
                    else:
                        pass

            TestSuite.appendChild(TestCase)

            TestPackage.appendChild(TestSuite)

            Result.appendChild(TestPackage)

        #f = open('C:\\Users\\c_youwu\\Desktop\\result\\testResult.xml','w')

        f = open('%s\\%s\\testResult.xml' % (QGP_Path().PATH_RESULTS,Start_Time) , 'w')
        f.write(doc.toprettyxml(indent = '',encoding='utf-8'))
        f.close()

        self.coverFiles(QGP_Path().PATH_DOCS,'%s\%s' % (QGP_Path().PATH_RESULTS,Start_Time))

    def coverFiles(self,sourceDir,targetDir):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
            targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(sourceFile):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())



if __name__ == "__main__":
    app = wx.App()
    f=Frame()
    f.Show()

    app.MainLoop()


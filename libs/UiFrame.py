#-*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import wx
import wx.lib.agw.customtreectrl as CT




class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="China App Stress",size = (1000,600))
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


       # TREE.showTestCase(self.TestCase_TREE,self.TestCase_TREE_ROOT,QGP.PATH_TESTCASES)
        #---------树模块结束
        self.Left_Above_Box = wx.BoxSizer( wx.HORIZONTAL)#左下界面，import和outport
        #---------左下界面模块开始

        self.Import_Button = wx.Button(self.panel,-1,'Import',size=(-1,50))#导入XML按钮
#        self.Bind(wx.EVT_BUTTON, self.OnImport, self.Import_Button)
        self.Export_Button = wx.Button(self.panel,-1,'Export',size=(-1,50))#导出选项到XML按钮
        #self.Bind(wx.EVT_BUTTON, self.OnExport, self.Export_Button)

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
#        self.redir=RedirectText(self.multiText)
#        sys.stdout=self.redir
        #------------文本显示模块结束
        self.Right_Above_Box = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，主要包含 Devicelist 和StartButton
        self.Right_Above_Box_VERTICAL = wx.BoxSizer( wx.VERTICAL)#右下BUTTONBOX，垂直布局，主要包含 下面两个水平布局框架
        self.Right_Above_Box_HORIZONTAL_1 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Start和Stop
        self.Right_Above_Box_HORIZONTAL_2 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Report和空白
        #------------右下显示模块开始

#        DEV.getDevicesList()
#        self.Device_Box = wx.RadioBox(self.panel, -1, "Device", wx.DefaultPosition,wx.DefaultSize,DEV.devices_List, 1, wx.RA_SPECIFY_COLS)#显示设备列表
#        self.Bind(wx.EVT_RADIOBOX, self.OnChoice, self.Device_Box)
        global serial_number
#        serial_number = self.Device_Box.GetItemLabel(self.Device_Box.Selection)

        self.Start_Button = wx.Button(self.panel,-1,'START',size=(-1,40))#开始运行
#        self.Bind(wx.EVT_BUTTON, self.OnStart, self.Start_Button)
        self.Result_Button = wx.Button(self.panel,-1,'RESULT',size=(-1,40))#打开报告
       # self.Bind(wx.EVT_BUTTON, self.OnResult, self.Result_Button)
        self.Stop_Button = wx.Button(self.panel,-1,'STOP',size=(-1,40))#停止运行

        self.Refresh_Button = wx.Button(self.panel,-1,'REFRESH',size=(-1,40))#重新加载页面
      #  self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.Refresh_Button)

        self.Right_Above_Box_HORIZONTAL_1.Add(self.Start_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_1.Add(self.Stop_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Result_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Refresh_Button,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_1,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_2,1,wx.EXPAND)
#        self.Right_Above_Box.Add(self.Device_Box,3,wx.EXPAND)
        self.Right_Above_Box.Add(self.Right_Above_Box_VERTICAL,7,wx.EXPAND|wx.TOP,5)


        #------------右下显示模块结束
        self.Right_Box.Add(self.multiText,1,wx.EXPAND)
        self.Right_Box.Add(self.Right_Above_Box,0,wx.EXPAND)
        #右边界面模块结束


        self.Main_Box.Add(self.Left_Box,3,wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM,5)
        self.Main_Box.Add(self.Right_Box,7,wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.BOTTOM,5)
        self.panel.SetSizer(self.Main_Box)

    # def OnChoice(self,event):
    #     if self.Device_Box.GetItemLabel(self.Device_Box.Selection) == 'No Device':
    #         self.Start_Button.Disable()
    #     else:
    #         self.Start_Button.Enable()
    #
    # def OnRefresh(self,event):
    #     TREE = TestCaseTree()
    #     self.TestCase_TREE_ROOT.DeleteChildren(self.TestCase_TREE)
    #     TREE.showTestCase(self.TestCase_TREE,self.TestCase_TREE_ROOT,QGP_Path().PATH_TESTCASES)
    #     self.TestCase_TREE_ROOT.Expand()
    #
    #
    #
    # planName = 'testplan'
    # def OnStart(self,event):
    #     TREE = TestCaseTree()
    #     Main=MainTest()
    #     serial_number = self.Device_Box.GetItemLabel(self.Device_Box.Selection)
    #     if TREE.getTreeSelect(self.TestCase_TREE) == []:
    #         print 'Please select some test case'
    #     else:
    #         self.getPLANwirteJAVA(self.planName)
    #         Thread_Test = threading.Thread(target=Main.main)
    #         Thread_Test.start()
    #     self.planName='testplan'
    #
    # def OnExport(self,event):
    #     QGP=QGP_Path()
    #     TREE = TestCaseTree()
    #     PLAN = TestCasePlan()
    #     if TREE.getTreeSelect(self.TestCase_TREE) != []:
    #         dlg = wx.FileDialog(self,
    #                             message="Save Test Plan",
    #                             wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
    #                             defaultDir=QGP.PATH_PLANS,
    #                             style=wx.SAVE
    #                             )
    #         if dlg.ShowModal() == wx.ID_OK:
    #             paths = dlg.GetPaths()
    #             for path in paths:
    #                 plan_name = path[len(QGP.PATH_PLANS)+1:-4]
    #                 file_name = path
    #             DOC=PLAN.establishTestPlan(TREE.getTreeSelect(self.TestCase_TREE),TestPlanName=plan_name)
    #             file=open(file_name,'w')
    #             file.write(DOC.toprettyxml(indent = '',encoding='utf-8'))
    #             file.close()
    #         dlg.Destroy()
    #     else:
    #         print 'Please select some Test Case'
    #
    # def OnImport(self,event):
    #     QGP=QGP_Path()
    #     TREE = TestCaseTree()
    #     PLAN = TestCasePlan()
    #     dlg = wx.FileDialog(self,
    #                         message="Select Test Plan",
    #                         wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
    #                         defaultDir=QGP.PATH_PLANS,
    #                         style=wx.OPEN
    #                         )
    #     if dlg.ShowModal() == wx.ID_OK:
    #         filename=""
    #         paths = dlg.GetPaths()
    #         for path in paths:
    #             filename=filename+path
    #     dlg.Destroy()
    #     aaa = filename[len(QGP.PATH_PLANS)+1:-4]
    #
    #     TREE=TestCaseTree()
    #     TREE.setTreeSelect(self.TestCase_TREE,aaa)
    #
    #
    #
    #
    # def OnResult(self,event):
    #     os.system('start %s' % QGP_Path().PATH_RESULTS)
    #
    #
    #
    # def getPLANwirteJAVA(self,planName):
    #     TREE = TestCaseTree()
    #     PLAN = TestCasePlan()
    #     QGP = QGP_Path()
    #     WR=writeTestCase()
    #     DOC = PLAN.establishTestPlan(TREE.getTreeSelect(self.TestCase_TREE))#根据树选择建立以个testplan的XML文档
    #     XML = open('%s\\%s.xml'% (QGP.PATH_PLANS,'testplan'),'w')#打开一个文档 名字为TESTPLAN
    #     XML.write(DOC.toprettyxml(indent = '',encoding='utf-8'))#写入DOC
    #     XML.close()
    #     testplan=PLAN.readTestPlan(planName)#获取Plan得到的值
    #     WR.writeToJAVA(testplan)
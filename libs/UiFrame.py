# -*- encoding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import wx
import wx.lib.agw.customtreectrl as CT
from TestCaseTree import TestCaseTree
from TestCasePlan import TestCasePlan
from GlobalVariable import GlobalVariable
from TestExecution import TestExecution
from Utility import Utility

class RedirectText(object):
    def __init__(self, wx_text_ctrl):
        self.out = wx_text_ctrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="China App Stress", size=(1000, 600))
        self.Center()
        self.panel = wx.Panel(self, -1)
        self.main_box = wx.BoxSizer( wx.HORIZONTAL)#整个界面，水平布局
        self.left_box = wx.BoxSizer( wx.VERTICAL)#左边界面，主要放置 Tree和PLAN的导入导出
        self.right_box = wx.BoxSizer( wx.VERTICAL)#右边界面，主要放置 文本输出和基本按键

        #左边界面模块开始
        #---------树模块开始
        self.test_case_tree = CT.CustomTreeCtrl(self.panel, agwStyle=wx.TR_DEFAULT_STYLE | CT.TR_AUTO_CHECK_PARENT | CT.TR_AUTO_CHECK_CHILD)
        self.test_case_tree_root = self.test_case_tree.AddRoot('TestCase')
        TestCaseTree.append_test_case(tree=self.test_case_tree, parent=self.test_case_tree_root, case_path=GlobalVariable.cases_folder)
        self.test_case_tree_root.Expand()
        #---------树模块结束

        self.left_above_box = wx.BoxSizer( wx.HORIZONTAL)#左下界面，import和outport
        #---------左下界面模块开始
        self.import_button = wx.Button(self.panel, -1, 'Import', size=(-1,50))#导入XML按钮
        self.Bind(wx.EVT_BUTTON, self.on_import, self.import_button)
        self.export_button = wx.Button(self.panel, -1, 'Export', size=(-1,50))#导出选项到XML按钮
        self.Bind(wx.EVT_BUTTON, self.on_export, self.export_button)
        self.left_above_box.Add(self.import_button, 1, wx.EXPAND)
        self.left_above_box.Add(self.export_button, 1, wx.EXPAND)
        #---------左下界面模块结束
        self.left_box.Add(self.test_case_tree, 1, wx.EXPAND)
        self.left_box.Add(self.left_above_box, 0, wx.EXPAND)
        #左边界面模块结束


        #右边界面模块开始
        #------------文本显示模块开始
        self.message_box = wx.TextCtrl(self.panel, -1, "",
                                       style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.message_box.SetInsertionPointEnd()
        redir = RedirectText(self.message_box)
        sys.stdout = redir

        #------------文本显示模块结束
        self.Right_Above_Box = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，主要包含 Devicelist 和StartButton
        self.Right_Above_Box_VERTICAL = wx.BoxSizer( wx.VERTICAL)#右下BUTTONBOX，垂直布局，主要包含 下面两个水平布局框架
        self.Right_Above_Box_HORIZONTAL_1 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Start和Stop
        self.Right_Above_Box_HORIZONTAL_2 = wx.BoxSizer( wx.HORIZONTAL)#右下界面模块，水平布局，Report和空白
        #------------右下显示模块开始

#        DEV.getDevicesList()
#        self.Device_Box = wx.RadioBox(self.panel, -1, "Device", wx.DefaultPosition,wx.DefaultSize,DEV.devices_List, 1, wx.RA_SPECIFY_COLS)#显示设备列表
#        self.Bind(wx.EVT_RADIOBOX, self.OnChoice, self.Device_Box)
#        serial_number = self.Device_Box.GetItemLabel(self.Device_Box.Selection)

        self.start_button = wx.Button(self.panel, -1, 'START', size=(-1,40)) #开始运行
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_button)
        self.Result_Button = wx.Button(self.panel,-1,'RESULT',size=(-1,40)) #打开报告
       # self.Bind(wx.EVT_BUTTON, self.OnResult, self.Result_Button)
        self.Stop_Button = wx.Button(self.panel,-1,'STOP',size=(-1,40))#停止运行

        self.Refresh_Button = wx.Button(self.panel,-1,'REFRESH',size=(-1,40))#重新加载页面
      #  self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.Refresh_Button)

        self.Right_Above_Box_HORIZONTAL_1.Add(self.start_button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_1.Add(self.Stop_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Result_Button,1,wx.EXPAND)
        self.Right_Above_Box_HORIZONTAL_2.Add(self.Refresh_Button,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_1,1,wx.EXPAND)
        self.Right_Above_Box_VERTICAL.Add(self.Right_Above_Box_HORIZONTAL_2,1,wx.EXPAND)
#        self.Right_Above_Box.Add(self.Device_Box,3,wx.EXPAND)
        self.Right_Above_Box.Add(self.Right_Above_Box_VERTICAL,7,wx.EXPAND|wx.TOP,5)


        #------------右下显示模块结束
        self.right_box.Add(self.message_box,1,wx.EXPAND)
        self.right_box.Add(self.Right_Above_Box,0,wx.EXPAND)
        #右边界面模块结束


        self.main_box.Add(self.left_box,3,wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM,5)
        self.main_box.Add(self.right_box,7,wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.BOTTOM,5)
        self.panel.SetSizer(self.main_box)

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

    def on_start(self, event):
        if not Utility.test_status_check(self.test_case_tree):
            return
        Utility.test_initialization()
        case_list = TestCaseTree.get_tree_select(tree=self.test_case_tree)
        device_list = ['ce58ac0d']
        for device in device_list:
            test_thread = TestExecution(device, case_list, self.message)
            test_thread.setDaemon(True)
            test_thread.start()


    def on_export(self, event):
        test_cases = TestCaseTree.get_tree_select(self.test_case_tree)
        if test_cases:
            dlg = wx.FileDialog(self,
                                message="Save Test Plan",
                                wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
                                defaultDir=GlobalVariable.plans_folder,
                                style=wx.SAVE
                                )
            if dlg.ShowModal() == wx.ID_OK:
                xml_path = dlg.GetPaths()[0]
                TestCasePlan.save(test_cases=TestCaseTree.get_tree_select(self.test_case_tree), save_path=xml_path)

            dlg.Destroy()
        else:
            print 'Please select some Test Case'

    def on_import(self, event):
        dlg = wx.FileDialog(self,
                            message="Select Test Plan",
                            wildcard="Test Plan (*.xml)|*.xml|All files (*.*)|*.*",
                            defaultDir=GlobalVariable.plans_folder,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            xml_path = dlg.GetPaths()[0]
            TestCaseTree.set_tree_select(tree=self.test_case_tree, test_cases=TestCasePlan.read(test_plan=xml_path))
        dlg.Destroy()




    def message(self, msg):
        self.message_box.AppendText(msg)
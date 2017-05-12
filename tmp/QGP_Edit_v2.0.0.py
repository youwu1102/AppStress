#-*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime,wx,threading,commands,subprocess,shutil
import xlrd


#写入默认路径地址
class QGP_Path():
    def __init__(self):
        LOCATION = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '..'))
        self.PATH_TESTCASES = '%s\\repository\\testcases' %LOCATION
        self.PATH_JAVA_JAR = '%s\\resource\\UiRobotium' %LOCATION
        self.PATH_JAVA_CLASS = '%s\\resource\\UiRobotium\\src' %LOCATION
        self.PATH_TEMPLATE = '%s\\resource\\UiRobotium\\src\\Template\\Template.java' %LOCATION
        self.NAME_JAVA_JAR = 'wuyou'
        self.NUMBER_ANDROID_ID = '10'
        self.PATH_LOGS = '%s\\repository\\logs' %LOCATION
        self.PATH_RESULTS = '%s\\repository\\results' %LOCATION
        self.PATH_DOCS='%s\\docs' %LOCATION
        self.PATH_PLANS ='%s\\repository\\plans' %LOCATION
        self.PATH_ANT = '%s\\resource\\apache-ant-1.9.4\\bin' %LOCATION
        self.PATH_FILE_ACTION = '%s\\others\\Actions.xlsx' %LOCATION
class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.AppendText(string)



class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="TestCaseEdit",size = (800,800))
        self.Center()
        self.panel = wx.Panel(self, -1)
        self.language = 3 # 2为 英语   3为中文


        self.Main_Box = wx.BoxSizer(wx.VERTICAL)
        self.Button_Box = wx.BoxSizer(wx.HORIZONTAL) #OPEN+SAVE+DEBUG
        self.Above_Box = wx.BoxSizer(wx.HORIZONTAL)#TREE+Edit界面
        self.Above_Left_Box = wx.BoxSizer(wx.VERTICAL)
        x, y = -1, 45

        self.Save_Button = wx.Button(self.panel, -1, 'SAVE', size=(x,y))
        self.Debug_Button = wx.Button(self.panel, -1, 'DEBUG', size=(x,y))
        self.Open_Button = wx.Button(self.panel, -1, 'OPEN', size=(x,y))
        self.Bind(wx.EVT_BUTTON, self.OnDebug, self.Debug_Button)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.Open_Button)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save_Button)

        self.Button_Box.Add(self.Open_Button,1,wx.EXPAND|wx.RIGHT,5)
        self.Button_Box.Add(self.Save_Button,1,wx.EXPAND|wx.ALIGN_CENTER)
        self.Button_Box.Add(self.Debug_Button,1,wx.EXPAND|wx.LEFT,5)

        TREE = ActionTree()
        QGP=QGP_Path()
        self.Action_Tree = wx.TreeCtrl(self.panel,size=(300,-1),style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_LINES_AT_ROOT)
        self.Action_Tree.SetBackgroundColour('#ECFFFF')
        self.Action_Tree_ROOT = self.Action_Tree.AddRoot('Script command')
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnDoubleClick, self.Action_Tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.OnClick,self.Action_Tree)
        TREE.ShowAction(self.Action_Tree,self.Action_Tree_ROOT)

        self.EditCase_mText = wx.TextCtrl(self.panel, -1, "", style=wx.TE_MULTILINE)
        self.EditCase_mText.SetBackgroundColour('#FFFFE0')



        self.Above_Left_Box.Add(self.Action_Tree,1,wx.EXPAND|wx.BOTTOM,5)
        self.Above_Left_Box.Add(self.Button_Box,0,wx.EXPAND)
        self.Above_Box.Add(self.Above_Left_Box,1,wx.EXPAND)
        self.Above_Box.Add(self.EditCase_mText,3,wx.EXPAND|wx.LEFT,5)



        self.Bottom_Box = wx.Notebook(self.panel, -1, size=wx.DefaultSize, style=wx.BK_DEFAULT)
        self.Description = wx.StaticText(self.Bottom_Box, -1,'Welcome', style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_THEME)
        self.Description.SetBackgroundColour('#F0F0F0')
        self.Debug_Log = wx.TextCtrl(self.Bottom_Box, -1, '', style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.Bottom_Box.AddPage(self.Description,'Description')
        self.Bottom_Box.AddPage(self.Debug_Log,'Debug Log')

        self.redir = RedirectText(self.Debug_Log)
        sys.stdout = self.redir

        self.Main_Box.Add(self.Above_Box,5,wx.EXPAND|wx.ALL,5)
        self.Main_Box.Add(self.Bottom_Box,2,wx.EXPAND|wx.ALL,5)
        self.panel.SetSizer(self.Main_Box)
        exc = Excel()
        self.aSheets = exc.read_sheet()
        self.dExcelValue = exc.creat_Dir()



    def OnDebug(self,event):
        self.write2JAVA()
        Thread_Test = threading.Thread(target=self.main)
        Thread_Test.start()

    def OnDoubleClick(self,event):
        if self.GetTreeSelect() in self.aSheets:
            self.ExpandTree()
        else:
            parent = self.GetTreeSelectParent()
            value = self.dExcelValue.get(parent)
            self.Type = self.GetSelectType(self.INDEX)
            aValue = value[self.INDEX]
            if self.Type==0:
                self.EditCase_mText.WriteText(aValue[1]+'\r\n')
            elif self.Type == 1:
                self.TransferBoolean(aValue)
            elif self.Type == 2:
                self.TransferString(aValue)
            elif self.Type == 3:
                self.TransferInteger(aValue)
            elif self.Type == 4:
                self.TransferStringBoolean(aValue)
    wildcard = "testCase (*.txt)|*.txt|All files (*.*)|*.*"
    def OnOpen(self,event):
        QGP=QGP_Path()
        dlg = wx.FileDialog(self,
                            message="select TestCase",
                            wildcard=self.wildcard,
                            defaultDir=QGP.PATH_TESTCASES,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            filename=""
            paths = dlg.GetPaths()
            for path in paths:
                filename=filename+path

            file=open(filename,'r')
            for line in file:
                self.EditCase_mText.WriteText(line)
            file.close()

        dlg.Destroy()

    def OnSave(self,event):
        QGP=QGP_Path()
        dlg = wx.FileDialog(self,
                            message="Save testCase",
                            wildcard=self.wildcard,
                            defaultDir=QGP.PATH_TESTCASES,
                            style=wx.SAVE
                            )
        if dlg.ShowModal() == wx.ID_OK:
            filename=""
            paths = dlg.GetPaths()
            for path in paths:
                filename=filename+path
            file=open(filename,'w')
            file.write(self.EditCase_mText.GetValue())
            file.close()
            self.EditCase_mText.SetValue('')
        dlg.Destroy()



    def OnClick(self,event):
        if self.GetTreeSelect() in self.aSheets:
            self.Description.SetLabel('双击展开/折叠以供选择方法，单击具体方法可以在此查看介绍,双击具体方法可以插入命令')
        else:
            self.INDEX=self.GetActionIndex()
            self.ShowDescription(self.INDEX)

    def write2JAVA(self):
        QGP = QGP_Path()
        Template = open(QGP.PATH_TEMPLATE,'r')
        TestClass = open('%s\\%s\\%s.java'%(QGP.PATH_JAVA_CLASS,'Demo1','Mydebug'),'w')
        for line in Template:
            if 'package Template;' in line:
                TestClass.writelines('package %s;\r\n' %'Demo1')
            elif 'public class Template extends UiAutomatorTestCase' in line:
                TestClass.writelines('public class %s extends UiAutomatorTestCase\r\n' %'Mydebug')
            elif ('//start' in line):
                TestClass.writelines('    public void test%s() throws UiObjectNotFoundException\r' % 'DebugDemo')
                TestClass.writelines('    {\r')
                TestClass.write(self.EditCase_mText.GetValue())
                TestClass.writelines('    }\r')

            else:
                TestClass.writelines(line)
        Template.close()
        TestClass.close()


    def buildJAR(self):
        QGP = QGP_Path()
        self.buildPass=False
        print os.popen('android create uitest-project -n %s -t %s -p %s' % (QGP.NAME_JAVA_JAR,
                                                                            QGP.NUMBER_ANDROID_ID,
                                                                            QGP.PATH_JAVA_JAR)).read()

        #os.system('cd %s\\' %QGP_Path().PATH_ANT)
        data  = subprocess.Popen ('ant build -buildfile %s//build.xml' % QGP.PATH_JAVA_JAR, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell = True)
        for line in iter(data.stdout.readline, ''):
            time.sleep(0.1)
            if 'BUILD SUCCESSFUL' in line:
                self.buildPass=True
            print line.strip('\r\n')

    def main(self):
        self.buildJAR()
        if self.buildPass==True:
            self.runTest()
        else:
            print 'please check the information'

    def runTest(self):
        QGP = QGP_Path()
        os.system('adb push %s\\bin\\%s.jar data/local/tmp' % (QGP.PATH_JAVA_JAR,QGP.NAME_JAVA_JAR))
        dataRun = subprocess.Popen ('adb shell uiautomator runtest %s.jar -c %s.%s' % (QGP.NAME_JAVA_JAR,'Demo1','Mydebug'), stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
        for line in iter(dataRun.stdout.readline, ''):
            print line.strip('\r\n')
            time.sleep(0.1)
    def GetActionIndex(self):
        select = self.GetTreeSelect()
        parent = self.GetTreeSelectParent()
        value = self.dExcelValue.get(parent)
        for index in range(len(value)):
            if select == str(value[index][0]):   #一般用不上 除非遇上数字被转换成STR的时候 需要用这条
                return index

    def ExpandTree(self):#展开树，如果已经展开，则折叠
        node = self.Action_Tree.Selection
        IsExpanded = self.Action_Tree.IsExpanded(node)
        if IsExpanded == True:
            self.Action_Tree.Collapse(node)
        else:
            self.Action_Tree.Expand(node)

    def GetTreeSelect(self):#获取当前选择的文字
        return self.Action_Tree.GetItemText(self.Action_Tree.Selection)

    def GetTreeSelectParent(self):#获取当前选择的父节点的文字
        node = self.Action_Tree.Selection
        parent = self.Action_Tree.GetItemParent(node)
        return self.Action_Tree.GetItemText(parent)


    def ShowDescription(self,x):
        parent = self.GetTreeSelectParent()
        value = self.dExcelValue.get(parent)

        self.Description.SetLabel(value[x][self.language])

    def GetSelectType(self,x):
        parent = self.GetTreeSelectParent()
        value = self.dExcelValue.get(parent)
        return int(value[x][4])

    def TransferBoolean(self,value):
        dialog = Dialog(self.Type)
        result = dialog.ShowModal()#显示模式对话框
        if result == wx.ID_OK:
            self.EditCase_mText.WriteText(value[1] %dialog.GetBooleanValue()+'\r\n')
        else:
            pass
        dialog.Destroy()

    def TransferString(self,value):
        dialog = Dialog(self.Type)
        result = dialog.ShowModal()#显示模式对话框
        if result == wx.ID_OK:
            self.EditCase_mText.WriteText(value[1] %dialog.GetStringValue()+'\r\n')
        else:
            pass
        dialog.Destroy()

    def TransferInteger(self,value):
        dialog = Dialog(self.Type)
        result = dialog.ShowModal()#显示模式对话框
        if result == wx.ID_OK:
            self.EditCase_mText.WriteText(value[1] % dialog.GetIntergerValue()+'\r\n')
        else:
            pass
        dialog.Destroy()

    def TransferStringBoolean(self,value):
        dialog = Dialog(self.Type)
        result = dialog.ShowModal()#显示模式对话框
        if result == wx.ID_OK:
            self.EditCase_mText.WriteText(value[1] % (dialog.GetStringValue(),dialog.GetBooleanValue())+'\r\n')
        else:
            pass
        dialog.Destroy()

class Dialog(wx.Dialog):
    def __init__(self,Type):#初始化对话框
        wx.Dialog.__init__(self, None, -1, 'Variable',
                size=(300, 225))
        self.BooleanValue = 'true'
        self.Center()
        if Type == 0:
            pass
        elif Type == 1:
            self.Boolean()
        elif Type == 2:
            self.String()
        elif Type == 3:
            self.Integer()
        elif Type == 4:
            self.String()
            self.Boolean()

        OK_Button = wx.Button\
            (self, wx.ID_OK, "OK",
             pos=(50, 160),size = (80,30))
        Cancel_Button   = wx.Button\
            (self, wx.ID_CANCEL, "Cancel",
             pos=(170, 160),size = (80,30))




    def String(self):
        sVar_String = wx.StaticText(self, -1,'String:',pos = (10,20), style=wx.TE_READONLY)
        Font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        sVar_String.SetFont(Font)
        self.Edit_String = wx.TextCtrl(self, -1, "", pos = (78,19),size = (200,20))

    def Boolean(self):
        sVar_Boolean = wx.StaticText(self, -1,'Boolean:',pos = (10,70), style=wx.TE_READONLY)
        Font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        sVar_Boolean.SetFont(Font)
        self.True_Radio = wx.RadioButton(self, -1, "True", pos=(99, 72), style=wx.RB_GROUP)
        self.False_Radio = wx.RadioButton(self, -1, "False", pos=(180, 72))
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio_True, self.True_Radio)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio_False, self.False_Radio)


    def Integer(self):
        sVar_Integer = wx.StaticText(self, -1,'Integer:',pos = (10,120), style=wx.TE_READONLY)
        Font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        sVar_Integer.SetFont(Font)
        self.Edit_Interger = wx.TextCtrl(self, -1, "", pos = (78,119),size = (200,20))

    def GetStringValue(self):
        return self.Edit_String.GetValue()

    def GetIntergerValue(self):
        return self.Edit_Interger.GetValue()


    def OnRadio_True(self,event):
        self.BooleanValue = 'true'

    def OnRadio_False(self,event):
        self.BooleanValue = 'false'

    def GetBooleanValue(self):
        return self.BooleanValue





class ActionTree():
    def __init__(self):
        pass

    def ShowAction(self,Tree,ParenNode):#显示方法树
        exc=Excel()
        sheets=exc.read_sheet()
        for sheet in sheets:
            eSheet = Tree.AppendItem(ParenNode,sheet)
            row_Values = exc.read_Row_Values(sheet)
            for row_Value in row_Values:
                #Tree.AppendItem(eSheet,row_Value[0])
                Tree.AppendItem(eSheet,str(row_Value[0])) #一般用不上 除非遇上数字被转换成STR的时候 需要用这条



class Excel():
    def __init__(self):
        pass

    def read_sheet(self):
        QGP=QGP_Path()
        data = xlrd.open_workbook(QGP.PATH_FILE_ACTION)
        sheet_name=[]
        for x in range(99):
            try:
                table = data.sheet_by_index(x)
                if table.name != 'Introduction':
                    sheet_name.append(table.name)
                else:
                    pass

            except Exception,e:
                break
        return sheet_name

    def read_Row_Values(self, sheet_name):
        QGP=QGP_Path()
        data = xlrd.open_workbook(QGP.PATH_FILE_ACTION)
        table =data.sheet_by_name(sheet_name)
        nrows = table.nrows
        row_values=[]
        for i in range(nrows):
            if table.row_values(i)[0]== 'Action Name':
                pass
            else:
                row_values.append(table.row_values(i))
        return row_values

    def creat_Dir(self):
        xls={}
        sheets=self.read_sheet()
        for sheet in sheets:
            xls[sheet]=self.read_Row_Values(sheet)
        return xls





if __name__ == "__main__":
    app = wx.App()
    f=Frame()
    f.Show()

    app.MainLoop()
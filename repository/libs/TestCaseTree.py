__author__ = 'c_youwu'


class TestCaseTree():
    def __init__(self):
        pass

    def showTestCase(self,tree, ParenNode,Path):
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

# -*- encoding:UTF-8 -*-
from os import listdir
from os.path import isdir, join


class TestCaseTree(object):
    @staticmethod
    def append_test_case(tree, parent, case_path):
        cases = listdir(case_path)
        for case in cases:
            if isdir(join(case_path, case)):
                child = tree.AppendItem(parent, case, 1)
                TestCaseTree.append_test_case(tree=tree, parent=child, case_path=join(case_path, case))
            else:
                if case.endswith('.xml'):
                    tree.AppendItem(parent, case, 1)

    @staticmethod
    def get_tree_select(tree):
        case_list = []
        tree_root = tree.GetRootItem()
        (item, cookie) = tree.GetFirstChild(tree_root)
        for x in xrange(tree.GetChildrenCount(tree_root)):
            if tree.GetItemText(item).endwith('.xml') and tree.IsItemChecked(item):
                tmp = []
                while tree.GetItemParent(item):
                    item = tree.GetItemParent(item)
                    tmp.append(item)
                    TestSuite=self.getSelectCasePath(item, tree)

                item=tree.GetNext(item)


    # def getTreeSelect(self,Tree):
    #     TestCase=[]
    #     treeRoot = Tree.GetRootItem()
    #     (item,cookie) = Tree.GetFirstChild(treeRoot)
    #     for x in range(Tree.GetChildrenCount(treeRoot)):
    #         if Tree.GetItemText(item)[-4:] == '.txt':
    #             TestSuite=self.getSelectCasePath(item,Tree)
    #             if TestSuite != []:
    #                 TestCase.append(TestSuite)
    #         item=Tree.GetNext(item)
    #     return TestCase
    #
    # def getSelectCasePath(self,item,Tree):
    #     path=[]
    #     if Tree.IsItemChecked(item):
    #         while Tree.GetItemParent(item):
    #             path.append(Tree.GetItemText(item))
    #             item=Tree.GetItemParent(item)
    #     path.reverse()
    #     return path
    # def setTreeSelect(self,Tree,testplan):
    #     PLAN = TestCasePlan()
    #     treeRoot = Tree.GetRootItem()
    #     plan=PLAN.readTestPlan(testplan)
    #     (all,cookie) = Tree.GetFirstChild(treeRoot)
    #     Tree.CheckItem(all,False)
    #     for path in plan:
    #         array_path = path[len(QGP_Path().PATH_TESTCASES)+1:].split('\\')#分割PLAN 并去删除前面重复的地方
    #         (testPackage,cookie) = Tree.GetFirstChild(treeRoot)
    #
    #         for num_package in range(Tree.GetChildrenCount(treeRoot,False)):
    #             if Tree.GetItemText(testPackage) == array_path[0]:
    #                 #print Tree.GetItemText(testPackage)
    #                 (testClass,cookie) = Tree.GetFirstChild(testPackage)
    #                 for num_class in range(Tree.GetChildrenCount(testPackage,False)):
    #                     if Tree.GetItemText(testClass) == array_path[1]:
    #                         #print Tree.GetItemText(testClass)
    #                         (testCase,cookie) = Tree.GetFirstChild(testClass)
    #                         for num_case in range(Tree.GetChildrenCount(testClass,False)):
    #                             if Tree.GetItemText(testCase) == array_path[2]:
    #                                 #print Tree.GetItemText(testCase)
    #                                 Tree.CheckItem(testCase)
    #                                 Tree.Expand(testClass)
    #                                 Tree.Expand(testPackage)
    #                                 break
    #                             else:
    #                                 (testCase,cookie) = Tree.GetNextChild(testClass,cookie)
    #                         break
    #                     else:
    #                         (testClass,cookie) = Tree.GetNextChild(testPackage,cookie)
    #                 break
    #             else:
    #                 (testPackage,cookie) = Tree.GetNextChild(treeRoot,cookie)

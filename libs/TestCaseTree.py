# -*- encoding:UTF-8 -*-
from os import listdir
from os.path import isdir, join
from GlobalVariable import GlobalVariable


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
            if tree.GetItemText(item).endswith('.xml') and tree.IsItemChecked(item):
                case_list.append(TestCaseTree.__get_case_path(item=item, tree=tree))
            item = tree.GetNext(item)
        return case_list

    @staticmethod
    def __get_case_path(item, tree):
        tmp = []
        case_path = GlobalVariable.cases_folder
        while tree.GetItemParent(item):
            tmp.append(tree.GetItemText(item))
            item = tree.GetItemParent(item)
        for x in tmp[::-1]:
            case_path = join(case_path, x)
        return case_path

    
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

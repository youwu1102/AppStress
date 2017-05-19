# -*- encoding:UTF-8 -*-
from os import listdir
from os.path import isdir, join
from GlobalVariable import GlobalVariable
from os import sep

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
    def set_tree_select(tree, test_cases):
        root = tree.GetRootItem()
        TestCaseTree.__set_all_item_unselected(tree=tree, root=root)
        for test_case in test_cases:
            test_case = test_case.replace(GlobalVariable.cases_folder, '')
            TestCaseTree.__set_item_select(item=root, path_array=test_case.split(sep)[1:], tree=tree)

    @staticmethod
    def __set_item_select(item, path_array, tree):
        child_count = tree.GetChildrenCount(item, False)
        (child, cookie) = tree.GetFirstChild(item)
        for i in xrange(child_count):
            if tree.GetItemText(child) == path_array[0] and not path_array[0].endswith('.xml'):
                tree.Expand(child)
                TestCaseTree.__set_item_select(item=child, path_array=path_array[1:], tree=tree)
            elif tree.GetItemText(child) == path_array[0] and path_array[0].endswith('.xml'):
                tree.CheckItem(child, True)
                break
            (child, cookie) = tree.GetNextChild(item, cookie)

    @staticmethod
    def __set_all_item_unselected(tree, root):
        child_count = tree.GetChildrenCount(root, False)
        (child, cookie) = tree.GetFirstChild(root)
        for i in xrange(child_count):
            tree.CheckItem(child, False)
            (child, cookie) = tree.GetNextChild(root, cookie)

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

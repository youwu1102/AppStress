# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
from GlobalVariable import GlobalVariable
from os.path import join, exists
from os import makedirs
from Case import Case
from TestCaseTree import TestCaseTree
from TimeFormat import TimeFormat
from Logic import CheckModule


class Utility(object):
    @staticmethod
    def test_case_parse(case_path):
        return Case.parse(case_path=case_path)

    @staticmethod
    def test_status_check(tree):
        case_list = TestCaseTree.get_tree_select(tree)
        if not case_list:
            Utility._print('Please check the test cases and try again.')
            return False
        test_case = Utility.__test_case_check(case_list)
        if not test_case:
            Utility._print('Please check the message above.')
            return False
        return test_case

    @staticmethod
    def test_initialization():
        Utility.__set_log_path()


    @staticmethod
    def __set_log_path():
        GlobalVariable.test_start_time = TimeFormat.time()
        GlobalVariable.test_log_path = join(GlobalVariable.log_folder, TimeFormat.timestamp())  # 如果是PC的话保存在当前目录的下LOG文件夹然后加上当前的时间戳
        makedirs(GlobalVariable.test_log_path)  # 在PC上创建LOG文件夹

    @staticmethod
    def create_folder(folder_path):
        if not exists(folder_path):
            makedirs(folder_path)
        return folder_path




    @staticmethod
    def _print(msg):
        msg = TimeFormat.timestamp() + ' SYSTEM: ' + str(msg)
        print msg

    @staticmethod
    def __test_case_check(case_list):
        Utility._print('Check if the test cases are written correctly.')
        case_check = CheckModule(Utility._print, cases=case_list)
        case_check.run()
        return case_check.get_status()



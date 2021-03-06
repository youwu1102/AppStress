# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
from GlobalVariable import GlobalVariable
from os.path import join, exists
from os import popen, makedirs
import re
from time import sleep
from Case import Case
from TestCaseTree import TestCaseTree
from TimeFormat import TimeFormat


class Utility(object):

    pid_expression = re.compile(r'\d+')

    @staticmethod
    def run_command_on_pc(output,cmd, except_result='', except_true=True, need_output=False):
        """
        这个方法只是在本机上运行，只有pc模式下用到 或者部分SSH
        cmd 需要执行的命令  必填项
        action_info 操作说明，非空则打印具体的操作，非必填项
        except_result 期望出现的字符串，非空则去执行判断，与except_true相互配合 ，非必填项
        except_true except_result，默认为True，如果修改成False的话，意思相当于不期望出现的字符串
        举例 run_command_on_device('ps | grep python', action_info='', except_result='python', except_true=False)
        代表在手机中执行了  ps | grep python  命令
        如果结果中包含Python 字样  则返回 False
        即可以理解为 希望结果中不出现Python字样
        """
        output.info('I run the command: %s' % cmd)
        actual_result = popen(cmd).read().strip('\r\n')
        if need_output and not except_result:
            output.info('I get the command output: %s' % actual_result)
            return actual_result
        if except_result:
            return Utility.check_result(except_result=except_result, except_true=except_true, actual_result=actual_result)
        return True

    @staticmethod
    def run_command_on_device(output, cmd, except_result='', except_true=True, need_output=False):
        """
        方法根据3种execution_mode ：ssh , pc, device 来控制操作的方法
        总共传递4个参数
        cmd 需要执行的命令  必填项
        action_info 操作说明，非空则打印具体的操作，非必填项
        except_result 期望出现的字符串，非空则去执行判断，与except_true相互配合 ，非必填项
        except_true except_result，默认为True，如果修改成False的话，意思相当于不期望出现的字符串
        举例 run_command_on_device('ps | grep python', action_info='', except_result='python', except_true=False)
        代表在手机中执行了  ps | grep python  命令
        如果结果中包含Python 字样  则返回 False
        即可以理解为 希望结果中不出现Python字样
        """
        cmd = '%s shell \"%s\"' % (GlobalVariable.adb_exe, cmd)
        output.info('I run the command: %s' % cmd)
        actual_result = popen(cmd).read().strip('\r\n')
        if need_output and not except_result:
            output.info('I get the command output: %s' % actual_result)
            return actual_result
        if except_result:
            return Utility.check_result(except_result=except_result, except_true=except_true, actual_result=actual_result)
        return True

    @staticmethod
    def check_result(output,except_result, except_true, actual_result):
        """
        参考上方 run_command_on_device 中描述
        """
        if except_true:
            if except_result in actual_result:
                Print.info('I except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return True
            else:
                Print.error('I except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return False
        else:
            if except_result in actual_result:
                Print.error('I do not except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return False
            else:
                Print.info('I do not except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return True

    @staticmethod
    def stop_process_on_device(process_name, not_matching=''):
        Print.info('I want to terminate the process \"%s\"' % process_name)
        pids = Utility.get_process_id_on_device(process_name=process_name, not_matching=not_matching)
        for pid in pids:
            Utility.run_command_on_device(cmd='kill %s' % pid)

    @staticmethod
    def get_process_id_on_device(process_name, not_matching=''):
        pids = []
        if not_matching:
            result = Utility.run_command_on_device(
                cmd='ps | grep %s | grep -v grep |grep -v %s' % (process_name, not_matching), need_output=True)
            for line in result.split('\r\n'):
                for re_result in Utility.pid_expression.finditer(line):
                    pids.append(re_result.group())
                    break
        else:
            result = Utility.run_command_on_device(cmd='ps | grep %s | grep -v grep' % process_name, need_output=True)
            for line in result.split('\r\n'):
                for re_result in Utility.pid_expression.finditer(line):
                    pids.append(re_result.group())
                    break
        return pids

    @staticmethod
    def push_file_to_device(local, remote):
        cmd = '{adb} push {local} {remote}'.format(adb=GlobalVariable.adb_exe, local=local, remote=remote)
        Utility.run_command_on_pc(cmd)
        sleep(1)

    @staticmethod
    def pull_file_to_pc(remote, local):
        cmd = '{adb} pull {remote} {local}'.format(adb=GlobalVariable.adb_exe, local=local, remote=remote)
        Utility.run_command_on_pc(cmd)
        sleep(1)

    @staticmethod
    def test_case_parse(case_path):
        return Case.parse(case_path=case_path)

    @staticmethod
    def test_status_check(tree):
        case_list = TestCaseTree.get_tree_select(tree)
        if not case_list:
            Utility._print('Please check the test cases and try again')
            return False
        test_case = Utility.__test_case_check(case_list)
        if not test_case:
            Utility._print('Please check the test cases and try again')
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
    def convert_expression(left, expression, right):
        if expression == "<":
            return left < right
        elif expression == "<=":
            return left <= right
        elif expression == ">":
            return left > right
        elif expression == ">=":
            return left >= right
        elif expression == "==":
            return left == right
        elif expression == "in":
            return left in right
        elif expression == "!=":
            return left != right
        else:
            print expression

    @staticmethod
    def _print(msg):
        msg = TimeFormat.timestamp() + ' SYSTEM: ' + str(msg)
        print msg

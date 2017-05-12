# -*- encoding:UTF-8 -*-
from os.path import join, abspath
import sys

class GlobalVariable(object):
    print sys.argv[0]

    working_directory = join(p)

    host_utils = join(working_directory, 'repository', 'HostUtils')
    target_utils = join(working_directory, 'repository', 'TargetUtils')

    adb_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    aapt_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    fastboot_exe = join(host_utils, 'sdk_tools', 'fastboot.exe')

    uiautomator_jar = 'C:\\Development\\Work\\wuyou_work1\\UiTest\\bin\\Demo.jar'


if __name__ == '__main__':
    print GlobalVariable.host_utils
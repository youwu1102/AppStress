# -*- encoding:UTF-8 -*-
from os.path import join, abspath, dirname, exists
import sys

class GlobalVariable(object):

    working_directory = abspath(dirname(sys.argv[0]))

    resource_folder = join(working_directory, 'resource')

    host_utils = join(resource_folder, 'HostUtils')
    target_utils = join(resource_folder, 'TargetUtils')

    adb_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    aapt_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    fastboot_exe = join(host_utils, 'sdk_tools', 'fastboot.exe')

    test_policy = 'random'
    test_loop = ''

if __name__ == '__main__':
    print GlobalVariable.host_utils
# -*- encoding:UTF-8 -*-
from os.path import join, abspath, dirname, exists
import sys

class GlobalVariable(object):
    working_directory = abspath(dirname(sys.argv[0]))

    resource_folder = join(working_directory, 'resource')
    repository_folder = join(working_directory, 'repository')
    log_folder = join(working_directory, 'log')
    cases_folder = join(repository_folder, 'cases')
    plans_folder = join(repository_folder, 'plans')
    host_utils = join(resource_folder, 'HostUtils')
    target_utils = join(resource_folder, 'TargetUtils')

    adb_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    aapt_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    fastboot_exe = join(host_utils, 'sdk_tools', 'fastboot.exe')
    test_start_time = 0
    test_policy = 'random'
    test_loop = 0
    test_time = 50 * 60 * 60
    background_test = []

    test_log_path = ''
if __name__ == '__main__':
    print GlobalVariable.host_utils